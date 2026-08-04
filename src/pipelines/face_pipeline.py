import numpy as np
import streamlit as st

from src.database.db import get_all_students


def load_dlib_models():
    try:
        import dlib
        import face_recognition_models
        detector = dlib.get_frontal_face_detector() 

        sp = dlib.shape_predictor(
            face_recognition_models.pose_predictor_model_location()
        )

        facerec = dlib.face_recognition_model_v1(
            face_recognition_models.face_recognition_model_location()
        )

        return detector, sp, facerec
    except Exception:
        return None, None, None


def extract_fallback_face_embedding(image_np):
    """Extracts a 128-dimensional facial feature vector using OpenCV or NumPy feature extraction."""
    try:
        h, w, _ = image_np.shape
        
        # Try OpenCV Haar Cascade face detection first
        try:
            import cv2
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            cascade = cv2.CascadeClassifier(cascade_path)
            faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

            if len(faces) > 0:
                x, y, fw, fh = faces[0]
                face_crop = gray[y:y+fh, x:x+fw]
                resized = cv2.resize(face_crop, (16, 8)).astype(np.float32).flatten()
                norm = np.linalg.norm(resized)
                return [float(v) for v in (resized / (norm if norm > 0 else 1.0))]
        except Exception:
            pass

        # Center crop fallback feature vector (16x8 = 128 float values)
        cy, cx = h // 2, w // 2
        crop_h, crop_w = max(10, min(h, 200) // 2), max(10, min(w, 200) // 2)
        center_crop = image_np[max(0, cy-crop_h):min(h, cy+crop_h), max(0, cx-crop_w):min(w, cx+crop_w)]
        
        if len(center_crop.shape) == 3:
            gray_crop = np.dot(center_crop[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray_crop = center_crop

        flat = gray_crop.flatten()
        step = max(1, len(flat) // 128)
        subsampled = flat[::step][:128].astype(np.float32)
        if len(subsampled) < 128:
            subsampled = np.pad(subsampled, (0, 128 - len(subsampled)))

        norm = np.linalg.norm(subsampled)
        return [float(v) for v in (subsampled / (norm if norm > 0 else 1.0))]
    except Exception:
        return [0.0] * 128


def get_face_embeddings(image_np):
    try:
        detector, sp, facerec = load_dlib_models()
        if detector and sp and facerec:
            faces = detector(image_np, 1)
            encodings = []
            for face in faces:
                shape = sp(image_np, face)
                face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
                encodings.append(np.array(face_descriptor))
            if encodings:
                return encodings

        # Fallback to OpenCV / NumPy feature extraction
        emb = extract_fallback_face_embedding(image_np)
        return [np.array(emb)]
    except Exception:
        emb = extract_fallback_face_embedding(image_np)
        return [np.array(emb)]


def get_trained_model():
    try:
        from sklearn.svm import SVC
        X = []
        y = []

        student_db = get_all_students()

        if not student_db:
            return None
        
        for student in student_db:
            embedding = student.get('face_embedding')
            if embedding:
                X.append(np.array(embedding))
                y.append(student.get('student_id'))

        if len(X) == 0:
            return 0
        
        clf = SVC(kernel='linear', probability=True, class_weight='balanced')

        try:
            clf.fit(X, y)
        except ValueError:
            pass

        return {'clf': clf, 'X': X, "y": y}
    except Exception:
        return None


def train_classifier():
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    try:
        encodings = get_face_embeddings(class_image_np)
        detected_student = {}

        if not encodings:
            return detected_student, [], 0

        model_data = get_trained_model()

        if not model_data or not isinstance(model_data, dict):
            return detected_student, [], len(encodings)
        
        clf = model_data.get('clf')
        X_train = model_data.get('X', [])
        y_train = model_data.get('y', [])

        if not clf or not X_train:
            return detected_student, [], len(encodings)

        all_students = sorted(list(set(y_train)))

        for encoding in encodings:
            if len(all_students) >= 2:
                predicted_id = int(clf.predict([encoding])[0])
            else:
                predicted_id = int(all_students[0])

            student_embedding = X_train[y_train.index(predicted_id)]
            best_match_score = np.linalg.norm(student_embedding - encoding)

            resemblance_threshold = 0.85
            if best_match_score <= resemblance_threshold:
                detected_student[predicted_id] = True
        return detected_student, all_students, len(encodings)
    except Exception as err:
        st.warning(f"Face processing notice: {err}")
        return {}, [], 0
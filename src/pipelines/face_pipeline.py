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
    except Exception as err:
        return None, None, None


def get_face_embeddings(image_np):
    try:
        detector, sp, facerec = load_dlib_models()
        if not detector or not sp or not facerec:
            return []

        faces = detector(image_np, 1)
        encodings = []

        for face in faces:
            shape = sp(image_np, face)
            face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
            encodings.append(np.array(face_descriptor))
        return encodings
    except Exception:
        return []


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

            resemblance_threshold = 0.6
            if best_match_score <= resemblance_threshold:
                detected_student[predicted_id] = True
        return detected_student, all_students, len(encodings)
    except Exception as err:
        st.warning(f"Face processing notice: {err}")
        return {}, [], 0
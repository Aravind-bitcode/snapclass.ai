import streamlit as st 
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np

try:
    from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier, extract_fallback_face_embedding
except Exception:
    def predict_attendance(img): return {}, [], 0
    def get_face_embeddings(img): return []
    def train_classifier(): return False
    def extract_fallback_face_embedding(img): return [0.0] * 128

try:
    from src.pipelines.voice_pipeline import get_voice_embedding
except Exception:
    def get_voice_embedding(audio_bytes): return None

from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject, student_login_by_name
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            if 'student_data' in st.session_state:
                del st.session_state.student_data
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('➕ Enroll in Subject', type='primary', use_container_width=True):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    seen_sids = set()
    rendered_count = 0
    for i, sub_node in enumerate(subjects):
        sub = sub_node.get('subjects', {})
        if not sub:
            continue
        sid = sub.get('subject_id')
        if not sid or sid in seen_sids:
            continue
        seen_sids.add(sid)
        
        stats = stats_map.get(sid, {"total": 0, "attended": 0})
        
        def make_unenroll_button(s_id, s_name, idx):
            def unenroll_button():
                if st.button("🗑️ Unenroll from course", key=f"unenroll_{s_id}_{idx}", type='tertiary', use_container_width=True):
                    unenroll_student_to_subject(student_id, s_id)
                    st.toast(f'Unenrolled from {s_name} successfully!')
                    st.rerun()
            return unenroll_button

        with cols[rendered_count % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=make_unenroll_button(sid, sub['name'], i)
            )
        rendered_count += 1
    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout() 

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using FaceID", text_alignment="center")

    st.space()
    st.space()

    show_registration = st.session_state.get('show_student_registration', False)

    # Allow direct registration toggle
    reg_col1, reg_col2 = st.columns([3, 1])
    with reg_col2:
        btn_label = "Hide Registration" if show_registration else "Register New Student"
        if st.button(btn_label, type="tertiary", key="toggle_reg_btn"):
            st.session_state.show_student_registration = not show_registration
            st.rerun()

    photo_source = st.camera_input("Position your face in the center", key="student_face_cam")

    if photo_source:
        try:
            photo_source.seek(0)
            img = np.array(Image.open(photo_source))
        except Exception:
            img = None

        if img is not None:
            with st.spinner('AI is scanning..'):
                detected, all_ids, num_faces = predict_attendance(img)

                if num_faces == 0:
                    st.warning('Face not found!')
                elif num_faces > 1:
                    st.warning('Multiple faces found')
                else:
                    if detected:
                        student_id = list(detected.keys())[0]
                        all_students = get_all_students()
                        student = next((s for s in all_students if s['student_id'] == student_id), None)

                        if student:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = student
                            st.toast(f'Welcome Back {student["name"]}')
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info('Face not recognized! You might be a new student!')
                        show_registration = True
                        st.session_state.show_student_registration = True

    if show_registration or st.session_state.get('show_student_registration'):
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Aravind Johindkumar', key="new_student_name_input")

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your voice for voice-only attendance")

            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase like "I am present, My name is Aravind."', key="new_student_audio_input")
            except Exception:
                pass

            if st.button('✨ Create Account', type='primary', key="create_student_account_btn"):
                if new_name:
                    if photo_source:
                        with st.spinner('Creating profile..'):
                            try:
                                photo_source.seek(0)
                                img = np.array(Image.open(photo_source))
                            except Exception:
                                img = None

                            if img is not None:
                                encodings = get_face_embeddings(img)
                                if encodings:
                                    face_emb = encodings[0].tolist()
                                else:
                                    face_emb = extract_fallback_face_embedding(img)

                                voice_emb = None
                                if audio_data:
                                    try:
                                        audio_data.seek(0)
                                        voice_bytes = audio_data.read()
                                        if voice_bytes:
                                            voice_emb = get_voice_embedding(voice_bytes)
                                    except Exception:
                                        voice_emb = None

                                response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                                if response_data and len(response_data) > 0:
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = response_data[0]
                                    st.session_state.show_student_registration = False
                                    st.toast(f'Profile Created! Hi {new_name}!')
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error('Database response error. Please try clicking Create Account again.')
                            else:
                                st.error('Please capture a photo using the camera input above first.')
                    else:
                        st.warning('Please capture a photo using the camera above first before creating an account!')
                else:
                    st.warning('Please enter your name!')

    footer_dashboard()
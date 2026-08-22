import streamlit as st
from src.database.db import enroll_student_to_subject, get_subject_by_code, get_student_subjects
import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll (e.g. CS101, AI202, DS301)')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', use_container_width=True):
        if join_code:
            subject = get_subject_by_code(join_code.strip())
            if subject:
                student_id = st.session_state.student_data['student_id']
                existing_subjects = get_student_subjects(student_id)
                already_enrolled = any(
                    s.get('subject_id') == subject['subject_id'] or 
                    s.get('subjects', {}).get('subject_id') == subject['subject_id'] 
                    for s in existing_subjects
                )

                if already_enrolled:
                    st.warning('You are already enrolled in this subject')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success(f"Successfully enrolled in {subject['name']}!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error('Subject code not found! Try demo codes: CS101, AI202, DS301')
        else:
            st.warning('Please enter a subject code')
"""
SnapClass AI — Automated Attendance System
==========================================

Layman Explanation:
-------------------
This is the main entry point file for SnapClass AI, a Streamlit web application that 
automates school attendance using face recognition (dlib/OpenCV) and voice biometrics.

What this file does:
1. Configures the Streamlit browser page title and logo.
2. Checks user login state (Teacher, Student, or Unauthenticated Visitor).
3. Routes the user to the correct UI screen (Teacher Dashboard, Student Portal, or Home Screen).
4. Handles QR Code dynamic joining: when a student scans a classroom QR code containing a 'join-code',
   it automatically prompts the enrollment dialog to join the subject.
"""

import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
from PIL import Image
import os

def get_page_icon():
    """Fetches the project logo image safely from local assets or fallback URL."""
    logo_path = os.path.join(os.path.dirname(__file__), "src", "assets", "logo.jpg")
    try:
        if os.path.exists(logo_path):
            return Image.open(logo_path)
    except Exception:
        pass
    return "https://i.ibb.co/YTYGn5qV/logo.png"

def main():
    """Main application router and session state manager."""
    st.set_page_config(
        page_title='SnapClass - Capturing Attendance seamlessly with AI',
        page_icon=get_page_icon()
    )

    # Initialize user login role in Streamlit session state if not already set
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # Render appropriate screen based on user role
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
            
        case None:
            home_screen()

    # Dynamic QR Code joining handler
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

if __name__ == "__main__":
    main()
import streamlit as st
import base64
import os

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.jpg")

def get_logo_url():
    try:
        if os.path.exists(LOGO_PATH):
            with open(LOGO_PATH, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        pass
    return "https://i.ibb.co/YTYGn5qV/snapclass-logo.png"


def header_home():
    logo_url = get_logo_url()

    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 30px; margin-top: 30px;">    
            <img src="{logo_url}" style="height:140px; width:140px; border-radius: 18px; object-fit: cover; border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 4px 20px rgba(0,0,0,0.2);" />
            <h1 style="text-align:center; color: #E0E3FF; margin-top: 15px;">SNAP</br>CLASS</h1>
        </div>
            """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = get_logo_url()

    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; gap:18px; margin-top: 30px;">    
            <img src="{logo_url}" style="height:100px; width:100px; border-radius: 16px; object-fit: cover; border: 1px solid rgba(88, 101, 242, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.15);" />
            <h2 style="text-align:left; color: #5865F2; margin:0;">SNAP</br>CLASS</h2>
        </div>
            """, unsafe_allow_html=True)
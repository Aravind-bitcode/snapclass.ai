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
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 25px; margin-top: 20px;">    
            <img src="{logo_url}" style="height:130px; width:130px; border-radius: 20px; object-fit: cover; border: 2px solid rgba(129, 140, 248, 0.4); box-shadow: 0 8px 30px rgba(99, 102, 241, 0.3);" />
            <h1 style="text-align:center; font-size: 3.2rem !important; margin-top: 15px; background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SNAP<br/>CLASS</h1>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = get_logo_url()
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 20px;">    
            <img src="{logo_url}" style="height:90px; width:90px; border-radius: 18px; object-fit: cover; border: 2px solid rgba(129, 140, 248, 0.4); box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25);" />
            <h2 style="text-align:left; font-size: 2.2rem !important; margin: 0; background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SNAP<br/>CLASS</h2>
        </div>
    """, unsafe_allow_html=True)
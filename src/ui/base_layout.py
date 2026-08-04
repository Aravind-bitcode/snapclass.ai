import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: #0B0F19 !important;
            }
            
            .stApp div[data-testid="stColumn"] {
                background-color: #1E293B !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
                padding: 2.5rem !important;
                border-radius: 2.5rem !important;
                text-align: center !important;
            }
        </style>
        """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background: #0B0F19 !important;
            }
        </style>
        """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800;900&family=Outfit:wght@400;500;600;700&display=swap');
                
            /* Hide top toolbar */
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top: 2rem !important;    
                max-width: 1000px !important;
            }

            h1 {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 900 !important;
                font-size: 3.2rem !important; 
                line-height: 1.1 !important;
                color: #F8FAFC !important;
                letter-spacing: -0.02em !important;
                margin-bottom: 0.5rem !important;
            }

            h2 {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.8rem !important; 
                line-height: 1.2 !important;
                color: #F8FAFC !important;
                margin-bottom: 0.5rem !important;
            }   
            h3, h4, p, label, span {
                font-family: 'Outfit', sans-serif !important;   
                color: #F1F5F9 !important;
            }

            .stButton > button {
                border-radius: 1.25rem !important;
                background-color: #6366F1 !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                padding: 0.6rem 1.2rem !important;
                border: none !important;
                transition: transform 0.2s ease-in-out !important;
            }

            .stButton > button[kind="secondary"] {
                background-color: #EC4899 !important;
                color: #FFFFFF !important;
            }

            .stButton > button[kind="tertiary"] {
                background-color: #334155 !important;
                color: #FFFFFF !important;
            }

            .stButton > button:hover {
                transform: scale(1.03) !important;
            }

            /* Password input visibility toggle button override */
            div[data-baseweb="input"] button {
                background-color: transparent !important;
                border: none !important;
                padding: 4px 8px !important;
                border-radius: 6px !important;
                font-size: 0.75rem !important;
            }
            div[data-baseweb="input"] button:hover {
                transform: none !important;
                background-color: rgba(255, 255, 255, 0.1) !important;
            }

            /* Image centering */
            .stApp img {
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
        </style>
        """, unsafe_allow_html=True)
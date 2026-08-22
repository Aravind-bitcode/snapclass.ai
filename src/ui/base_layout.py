import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%) !important;
                color: #F8FAFC !important;
            }
            
            .stApp div[data-testid="stColumn"] {
                background: rgba(30, 41, 59, 0.85) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                padding: 2.5rem !important;
                border-radius: 2rem !important;
                backdrop-filter: blur(20px) !important;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%) !important;
                color: #F8FAFC !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');
                
            /* Hide top toolbar */
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top: 2rem !important;    
                padding-bottom: 2rem !important;
            }

            h1 {
                font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                font-size: 3rem !important; 
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            h2 {
                font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.8rem !important; 
                line-height: 1.2 !important;
                color: #F8FAFC !important;
                margin-bottom: 0.5rem !important;
            }   
            
            h3, h4, p, label {
                font-family: 'Outfit', sans-serif !important;   
                color: #E2E8F0 !important;
            }

            /* Streamlit Inputs */
            .stTextInput input, .stSelectbox div[data-baseweb="select"] {
                background: rgba(15, 23, 42, 0.8) !important;
                color: #F8FAFC !important;
                border: 1px solid rgba(129, 140, 248, 0.3) !important;
                border-radius: 1rem !important;
            }

            /* Clean Password Eye Icon Toggle Styling */
            div[data-baseweb="input"] button,
            button[aria-label="Show password"],
            button[aria-label="Hide password"],
            div[data-testid="stTextInput"] button {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                padding: 0 8px !important;
                margin: 0 !important;
                border-radius: 50% !important;
                color: transparent !important;
                font-size: 0 !important;
                min-height: auto !important;
                width: auto !important;
                position: relative !important;
                cursor: pointer !important;
            }

            div[data-baseweb="input"] button *,
            button[aria-label="Show password"] *,
            button[aria-label="Hide password"] * {
                display: none !important;
            }

            div[data-baseweb="input"] button::after,
            button[aria-label="Show password"]::after,
            button[aria-label="Hide password"]::after {
                content: "👁️" !important;
                font-size: 1.2rem !important;
                color: #818CF8 !important;
                display: inline-block !important;
                line-height: 1 !important;
                transition: transform 0.2s ease !important;
            }

            div[data-baseweb="input"] button:hover::after,
            button[aria-label="Show password"]:hover::after,
            button[aria-label="Hide password"]:hover::after {
                color: #C084FC !important;
                transform: scale(1.15) !important;
            }

            /* Streamlit Top-Level Action Buttons Only */
            .stButton > button,
            div[data-testid="stFormSubmitButton"] > button {
                border-radius: 1.2rem !important;
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
                color: #FFFFFF !important;
                padding: 12px 24px !important;
                font-size: 1.05rem !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 700 !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4) !important;
                transition: all 0.25s ease-in-out !important;
            }

            .stButton > button p,
            div[data-testid="stFormSubmitButton"] > button p {
                color: #FFFFFF !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.05rem !important;
                margin: 0 !important;
            }

            .stButton > button[kind="secondary"],
            div[data-testid="stFormSubmitButton"] > button[kind="secondary"] {
                border-radius: 1.2rem !important;
                background: linear-gradient(135deg, #EC4899 0%, #D946EF 100%) !important;
                color: #FFFFFF !important;
                padding: 12px 24px !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                box-shadow: 0 4px 16px rgba(236, 72, 153, 0.4) !important;
            }

            .stButton > button[kind="secondary"] p {
                color: #FFFFFF !important;
            }

            .stButton > button[kind="tertiary"],
            div[data-testid="stFormSubmitButton"] > button[kind="tertiary"] {
                border-radius: 1.2rem !important;
                background: rgba(30, 41, 59, 0.95) !important;
                color: #F8FAFC !important;
                padding: 12px 24px !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }

            .stButton > button[kind="tertiary"] p {
                color: #F8FAFC !important;
            }

            .stButton > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover {
                transform: translateY(-2px) scale(1.02) !important;
                box-shadow: 0 6px 22px rgba(99, 102, 241, 0.55) !important;
            }
        </style>
    """, unsafe_allow_html=True)
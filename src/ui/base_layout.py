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
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
                
            /* Hide top toolbar */
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top: 1.5rem !important;    
            }

            h1 {
                font-family: "Climate Crisis", sans-serif !important;
                font-size: 3.5rem !important; 
                line-height: 1.1 !important;
                color: #F8FAFC !important;
                margin-bottom: 0rem !important;
            }

            h2 {
                font-family: "Outfit", sans-serif !important;
                font-weight: 700 !important;
                font-size: 2rem !important; 
                line-height: 1.2 !important;
                color: #F8FAFC !important;
                margin-bottom: 0.5rem !important;
            }   
            h3, h4, p, label, span {
                font-family: "Outfit", sans-serif !important;   
                color: #F1F5F9 !important;
            }

            button {
                border-radius: 1.5rem !important;
                background-color: #6366F1 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background-color: #EC4899 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: #334155 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button:hover {
                transform: scale(1.05);
            }
        </style>
        """, unsafe_allow_html=True)
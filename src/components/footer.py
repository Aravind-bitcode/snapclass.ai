import streamlit as st

def footer_home():

    st.markdown(f"""
    
            <div style="margin-top: 30px; display: flex; gap: 6px; justify-content: center;">    
                <p style="font-weight:bold; color: white;">Created with ❤️ by Aravind</p>
            </div>
                """, unsafe_allow_html=True)
    

def footer_dashboard():

    st.markdown(f"""
    
            <div style="margin-top: 30px; display: flex; gap: 6px; justify-content: center;">    
                <p style="font-weight:bold; color: black;">Created with ❤️ by Aravind</p>
            </div>
                """, unsafe_allow_html=True)
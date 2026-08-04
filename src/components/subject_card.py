import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    stats_html = ""
    if stats:
        badges = ""
        for icon, label, value in stats:
            badges += f'<div style="background: #FCE7F3; color: #9D174D; border: 1px solid #FBCFE8; padding: 6px 14px; border-radius: 12px; font-size: 0.9rem; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;"><span>{icon}</span><span style="color: #831843; font-weight: 800;">{value}</span><span style="color: #9D174D; font-weight: 600;">{label}</span></div>'
        stats_html = f'<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">{badges}</div>'

    card_html = f'<div style="background: #FFFFFF; border-left: 8px solid #EB459E; padding: 25px; border-radius: 20px; border: 1px solid #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px; color: #0F172A; font-family: system-ui, -apple-system, sans-serif;"><h3 style="margin: 0 0 10px 0; color: #0F172A; font-size: 1.5rem; font-weight: 700;">{name}</h3><p style="color: #475569; margin: 10px 0 15px 0; font-size: 0.95rem; font-weight: 500;">Code : <span style="background: #EEF2FF; color: #4338CA; padding: 4px 10px; border-radius: 6px; font-weight: 700; border: 1px solid #C7D2FE;">{code}</span> <span style="margin: 0 8px; color: #94A3B8;">|</span> Section : <strong style="color: #1E293B;">{section}</strong></p>{stats_html}</div>'

    st.markdown(card_html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
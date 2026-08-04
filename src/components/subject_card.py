import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    stats_html = ""
    if stats:
        badges = ""
        for icon, label, value in stats:
            badges += f'<div style="background: rgba(236, 72, 153, 0.15); color: #F472B6; border: 1px solid rgba(236, 72, 153, 0.3); padding: 6px 14px; border-radius: 12px; font-size: 0.9rem; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;"><span>{icon}</span><span style="color: #F472B6; font-weight: 800;">{value}</span><span style="color: #FBCFE8; font-weight: 600;">{label}</span></div>'
        stats_html = f'<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">{badges}</div>'

    card_html = f'<div style="background: #1E293B; border-left: 8px solid #EC4899; padding: 25px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 10px 25px rgba(0,0,0,0.4); margin-bottom: 20px; color: #F8FAFC; font-family: system-ui, -apple-system, sans-serif;"><h3 style="margin: 0 0 10px 0; color: #F8FAFC; font-size: 1.5rem; font-weight: 700;">{name}</h3><p style="color: #94A3B8; margin: 10px 0 15px 0; font-size: 0.95rem; font-weight: 500;">Code : <span style="background: #312E81; color: #818CF8; padding: 4px 10px; border-radius: 6px; font-weight: 700; border: 1px solid #4338CA;">{code}</span> <span style="margin: 0 8px; color: #64748B;">|</span> Section : <strong style="color: #E2E8F0;">{section}</strong></p>{stats_html}</div>'

    st.markdown(card_html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
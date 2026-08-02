import streamlit as st
import os

try:
    from supabase import create_client, Client
except Exception:
    try:
        from supabase_py import create_client, Client
    except Exception:
        create_client = None
        Client = None

def init_supabase():
    """
    Initializes Supabase Client using publishable client credentials.
    Uses safe publishable key: sb_publishable_KZf7Wmmce3LWgxJjcstRTg_U3Slj8Wd
    """
    if not create_client:
        return None
        
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "https://vhlgqlrrbaojjskbgmya.supabase.co")
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "sb_publishable_KZf7Wmmce3LWgxJjcstRTg_U3Slj8Wd")
    
    if url and key:
        try:
            return create_client(url, key)
        except Exception:
            return None
    return None

supabase: Client = init_supabase()
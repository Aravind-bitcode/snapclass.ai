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

SUPABASE_DEFAULT_URL = "https://vhlgqlrrbaojjskbgmya.supabase.co"
SUPABASE_DEFAULT_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZobGdxbHJyYmFvampza2JnbXlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ1NTg0MTgsImV4cCI6MjEwMDEzNDQxOH0.qxO8Y4O21crMOGNwLofd3_Oh2rmP7bZDX3FvmFcN9Ps"

def init_supabase():
    """
    Initializes Supabase Client using environment variables, Streamlit secrets, or fallback key.
    """
    if not create_client:
        return None
        
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", SUPABASE_DEFAULT_URL)
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", SUPABASE_DEFAULT_KEY)
    
    if url and key:
        try:
            return create_client(url, key)
        except Exception:
            return None
    return None

supabase: Client = init_supabase()
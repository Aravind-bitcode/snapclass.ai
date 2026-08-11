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

SUPABASE_URL = "https://vhlgqlrrbaojjskbgmya.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZobGdxbHJyYmFvampza2JnbXlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ1NTg0MTgsImV4cCI6MjEwMDEzNDQxOH0.qxO8Y4O21crMOGNwLofd3_Oh2rmP7bZDX3FvmFcN9Ps"

def init_supabase():
    """
    Initializes Supabase Client using direct verified credentials.
    """
    if not create_client:
        return None
        
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase connection error: {e}")
        return None

supabase: Client = init_supabase()
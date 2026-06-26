import streamlit as st
import requests

SUPABASE_URL = "https://smbcicbjpgexxaizbtgo.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtYmNpY2JqcGdleHhhaXpidGdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0ODM0NDMsImV4cCI6MjA5ODA1OTQ0M30.5GCWg-puUahs15-NMLSGF1L9LcrlJXBKD0QUaL5BuVA"

def _url():
    return st.secrets.get("SUPABASE_URL", SUPABASE_URL)

def _key():
    return st.secrets.get("SUPABASE_ANON_KEY", ANON_KEY)

def _h(token=None):
    h = {"apikey": _key(), "Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def login(email: str, password: str) -> dict | None:
    r = requests.post(
        f"{_url()}/auth/v1/token?grant_type=password",
        headers=_h(),
        json={"email": email, "password": password},
        timeout=10,
    )
    if r.status_code == 200:
        return r.json()
    return None

def get_user_role(user_id: str, access_token: str) -> str:
    r = requests.get(
        f"{_url()}/rest/v1/profiles?user_id=eq.{user_id}&select=role",
        headers=_h(access_token),
        timeout=10,
    )
    if r.status_code == 200 and r.json():
        return r.json()[0].get("role", "readonly")
    return "readonly"

def get_all_users(access_token: str) -> list:
    r = requests.get(
        f"{_url()}/rest/v1/profiles?select=*",
        headers=_h(access_token),
        timeout=10,
    )
    return r.json() if r.status_code == 200 else []

def create_user(email: str, password: str, name: str, role: str, service_key: str) -> bool:
    r = requests.post(
        f"{_url()}/auth/v1/admin/users",
        headers={**_h(), "Authorization": f"Bearer {service_key}"},
        json={"email": email, "password": password, "email_confirm": True,
              "user_metadata": {"name": name, "role": role}},
        timeout=10,
    )
    if r.status_code == 200:
        user_id = r.json().get("id")
        requests.post(
            f"{_url()}/rest/v1/profiles",
            headers={**_h(), "Authorization": f"Bearer {service_key}"},
            json={"user_id": user_id, "email": email, "name": name, "role": role},
            timeout=10,
        )
        return True
    return False

def delete_user(user_id: str, service_key: str) -> bool:
    r = requests.delete(
        f"{_url()}/auth/v1/admin/users/{user_id}",
        headers={**_h(), "Authorization": f"Bearer {service_key}"},
        timeout=10,
    )
    if r.status_code == 200:
        requests.delete(
            f"{_url()}/rest/v1/profiles?user_id=eq.{user_id}",
            headers={**_h(), "Authorization": f"Bearer {service_key}"},
            timeout=10,
        )
        return True
    return False

def logout():
    for key in ["user", "role", "access_token", "user_id", "user_name"]:
        st.session_state.pop(key, None)

def require_auth():
    if "user" not in st.session_state:
        st.switch_page("app.py")
        st.stop()
    return st.session_state.get("role", "readonly")

def require_admin():
    role = require_auth()
    if role != "admin":
        st.error("No tienes permisos para acceder a esta sección.")
        st.stop()
    return role

import streamlit as st
import requests

SUPABASE_URL = "https://smbcicbjpgexxaizbtgo.supabase.co"
SUPABASE_KEY = "sb_publishable_4Nz0IG2hkMP6M-8HNrAuAQ_hwYbA5qz"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json",
}

def login(email: str, password: str) -> dict | None:
    """Authenticate user with Supabase Auth."""
    r = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers=HEADERS,
        json={"email": email, "password": password},
        timeout=10,
    )
    if r.status_code == 200:
        return r.json()
    return None

def get_user_role(user_id: str, access_token: str) -> str:
    """Get user role from profiles table."""
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/profiles?user_id=eq.{user_id}&select=role",
        headers={**HEADERS, "Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if r.status_code == 200 and r.json():
        return r.json()[0].get("role", "readonly")
    return "readonly"

def get_all_users(access_token: str) -> list:
    """Get all users from profiles table (admin only)."""
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/profiles?select=*",
        headers={**HEADERS, "Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    return r.json() if r.status_code == 200 else []

def create_user(email: str, password: str, name: str, role: str, service_key: str) -> bool:
    """Create a new user via Supabase Admin API (requires service key)."""
    r = requests.post(
        f"{SUPABASE_URL}/auth/v1/admin/users",
        headers={**HEADERS, "Authorization": f"Bearer {service_key}"},
        json={"email": email, "password": password, "email_confirm": True,
              "user_metadata": {"name": name, "role": role}},
        timeout=10,
    )
    if r.status_code == 200:
        user_id = r.json().get("id")
        # Insert into profiles
        requests.post(
            f"{SUPABASE_URL}/rest/v1/profiles",
            headers={**HEADERS, "Authorization": f"Bearer {service_key}"},
            json={"user_id": user_id, "email": email, "name": name, "role": role},
            timeout=10,
        )
        return True
    return False

def delete_user(user_id: str, service_key: str) -> bool:
    """Delete a user (requires service key)."""
    r = requests.delete(
        f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}",
        headers={**HEADERS, "Authorization": f"Bearer {service_key}"},
        timeout=10,
    )
    if r.status_code == 200:
        requests.delete(
            f"{SUPABASE_URL}/rest/v1/profiles?user_id=eq.{user_id}",
            headers={**HEADERS, "Authorization": f"Bearer {service_key}"},
            timeout=10,
        )
        return True
    return False

def logout():
    """Clear session state."""
    for key in ["user", "role", "access_token", "user_id", "user_name"]:
        st.session_state.pop(key, None)

def require_auth():
    """
    Call at top of every page.
    Returns role string if authenticated, else stops execution.
    """
    if "user" not in st.session_state:
        st.switch_page("app.py")
        st.stop()
    return st.session_state.get("role", "readonly")

def require_admin():
    """
    Call at top of admin-only pages.
    Stops execution if not admin.
    """
    role = require_auth()
    if role != "admin":
        st.error("No tienes permisos para acceder a esta sección.")
        st.stop()
    return role

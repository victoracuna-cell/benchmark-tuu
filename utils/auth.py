import streamlit as st
import hashlib
import hmac
import json
import requests
import base64
from datetime import datetime, timezone

# ── Helpers GitHub ──
def _gh_headers():
    token = st.secrets.get("GITHUB_TOKEN", "")
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

def _users_url():
    repo = st.secrets.get("GITHUB_REPO", "")
    return f"https://api.github.com/repos/{repo}/contents/data/users.json"

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def _load_users() -> dict:
    r = requests.get(_users_url(), headers=_gh_headers(), timeout=10)
    if r.status_code == 200:
        content = base64.b64decode(r.json()["content"]).decode()
        return json.loads(content)
    return {"users": []}

def _save_users(data: dict, msg: str = "chore: update users") -> bool:
    payload = json.dumps(data, ensure_ascii=False, indent=2).encode()
    content_b64 = base64.b64encode(payload).decode()
    r_get = requests.get(_users_url(), headers=_gh_headers(), timeout=10)
    sha = r_get.json().get("sha") if r_get.status_code == 200 else None
    body = {"message": msg, "content": content_b64}
    if sha:
        body["sha"] = sha
    r = requests.put(_users_url(), headers=_gh_headers(), json=body, timeout=10)
    return r.status_code in (200, 201)

# ── Auth functions ──
def login(email: str, password: str) -> dict | None:
    data = _load_users()
    pw_hash = _hash_password(password)
    for u in data.get("users", []):
        if u["email"].lower() == email.lower() and u["password_hash"] == pw_hash:
            return u
    return None

def get_all_users() -> list:
    return _load_users().get("users", [])

def create_user(email: str, password: str, name: str, role: str) -> bool:
    data = _load_users()
    # Check if email already exists
    if any(u["email"].lower() == email.lower() for u in data.get("users", [])):
        return False
    data.setdefault("users", []).append({
        "email": email,
        "name": name,
        "role": role,
        "password_hash": _hash_password(password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return _save_users(data, f"chore: add user {email}")

def delete_user(email: str) -> bool:
    data = _load_users()
    before = len(data.get("users", []))
    data["users"] = [u for u in data.get("users", []) if u["email"].lower() != email.lower()]
    if len(data["users"]) < before:
        return _save_users(data, f"chore: remove user {email}")
    return False

def update_password(email: str, new_password: str) -> bool:
    data = _load_users()
    for u in data.get("users", []):
        if u["email"].lower() == email.lower():
            u["password_hash"] = _hash_password(new_password)
            return _save_users(data, f"chore: update password {email}")
    return False

def logout():
    for key in ["user", "role", "user_name", "user_email"]:
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

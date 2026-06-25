import streamlit as st
import requests
import json
import base64
from datetime import datetime, timezone

GITHUB_API = "https://api.github.com"

def _headers():
    token = st.secrets.get("GITHUB_TOKEN", "")
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

def _repo_info():
    return st.secrets.get("GITHUB_REPO", ""), st.secrets.get("GITHUB_PATH", "data/benchmark.json")

def load_data() -> dict:
    repo, path = _repo_info()
    if not repo:
        return {}
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    r = requests.get(url, headers=_headers(), timeout=10)
    if r.status_code == 404:
        return {}
    if r.status_code != 200:
        st.error(f"Error leyendo datos de GitHub: {r.status_code}")
        return {}
    content = r.json().get("content", "")
    decoded = base64.b64decode(content).decode("utf-8")
    return json.loads(decoded)

def save_data(data: dict, commit_msg: str = "chore: update benchmark data") -> bool:
    repo, path = _repo_info()
    if not repo:
        st.error("Configura GITHUB_REPO en los secrets de Streamlit.")
        return False

    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    content_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    sha = None
    existing = requests.get(url, headers=_headers(), timeout=10)
    if existing.status_code == 200:
        sha = existing.json().get("sha")

    payload = {"message": commit_msg, "content": content_b64}
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=_headers(), json=payload, timeout=15)
    if r.status_code in (200, 201):
        return True
    st.error(f"Error guardando en GitHub: {r.status_code} — {r.text[:200]}")
    return False

def get_competitor_names(data: dict) -> list[str]:
    return list(data.get("competitors", {}).keys())

def upsert_competitor(data: dict, key: str, payload: dict) -> dict:
    if "competitors" not in data:
        data["competitors"] = {}
    if key not in data["competitors"]:
        data["competitors"][key] = {}
    data["competitors"][key].update(payload)
    return data

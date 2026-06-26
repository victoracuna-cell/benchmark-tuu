import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.auth import require_admin, get_all_users, create_user, delete_user
from utils.ui import render_sidebar

st.set_page_config(page_title="Usuarios · Benchmark TUU", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
require_admin()
render_sidebar()

st.markdown('<p style="font-size:1.75rem;font-weight:700;color:#0a0a0a;letter-spacing:-0.04em;margin-bottom:0.25rem;">Gestión de usuarios</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:0.7rem;color:#888;margin-bottom:1.5rem;">Crea, elimina y administra el acceso al benchmark.</p>', unsafe_allow_html=True)

access_token = st.session_state.get("access_token", "")
service_key = st.secrets.get("SUPABASE_SERVICE_KEY", "")

if not service_key:
    st.warning("Agrega `SUPABASE_SERVICE_KEY` en los Secrets de Streamlit para crear/eliminar usuarios.")

# ── Crear usuario ──
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">Crear nuevo usuario</div>', unsafe_allow_html=True)

with st.form("create_user_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_name = st.text_input("Nombre")
    with col2:
        new_email = st.text_input("Correo electrónico")
    with col3:
        new_role = st.selectbox("Rol", ["readonly", "admin"],
                                format_func=lambda r: "Solo lectura" if r == "readonly" else "Administrador")
    new_password = st.text_input("Contraseña temporal", type="password")
    submitted = st.form_submit_button("Crear usuario", type="primary")

if submitted:
    if not all([new_name, new_email, new_password, service_key]):
        st.error("Completa todos los campos y asegúrate de tener el SUPABASE_SERVICE_KEY configurado.")
    else:
        if create_user(new_email, new_password, new_name, new_role, service_key):
            st.success(f"Usuario {new_email} creado con rol '{new_role}'.")
            st.rerun()
        else:
            st.error("Error creando usuario. Verifica el service key y que el correo no exista.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Lista de usuarios ──
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">Usuarios activos</div>', unsafe_allow_html=True)

users = get_all_users(access_token)

if not users:
    st.info("No hay usuarios registrados en la tabla profiles, o no tienes permisos para verlos.")
else:
    for u in users:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        role = u.get("role", "readonly")
        with col1:
            st.markdown(f'<span style="font-size:13px;font-weight:500;color:#333;">{u.get("name", "—")}</span><br><span style="font-size:11px;color:#888;">{u.get("email","—")}</span>', unsafe_allow_html=True)
        with col2:
            color = "#0128c9" if role == "admin" else "#888"
            label = "Administrador" if role == "admin" else "Solo lectura"
            st.markdown(f'<span style="font-size:12px;color:{color};font-weight:500;">{"🔑" if role == "admin" else "👁"} {label}</span>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<span style="font-size:11px;color:#bbb;">{u.get("created_at","")[:10]}</span>', unsafe_allow_html=True)
        with col4:
            uid = u.get("user_id", "")
            if uid != st.session_state.get("user_id") and service_key:
                if st.button("Eliminar", key=f"del_{uid}"):
                    if delete_user(uid, service_key):
                        st.success("Usuario eliminado.")
                        st.rerun()
        st.markdown('<hr style="border:none;border-top:1px solid #f5f5f5;margin:6px 0;">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

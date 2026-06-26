import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.auth import require_admin, get_all_users, create_user, delete_user, update_password
from utils.ui import render_sidebar

st.set_page_config(page_title="Usuarios · Benchmark TUU", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
require_admin()
render_sidebar()

st.markdown('<p style="font-size:1.75rem;font-weight:700;color:#0a0a0a;letter-spacing:-0.04em;margin-bottom:0.25rem;">Gestión de usuarios</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:0.7rem;color:#888;margin-bottom:1.5rem;">Crea, elimina y administra el acceso al benchmark.</p>', unsafe_allow_html=True)

# ── Crear usuario ──
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">Crear nuevo usuario</div>', unsafe_allow_html=True)
with st.form("create_user_form"):
    col1, col2, col3 = st.columns(3)
    with col1: new_name  = st.text_input("Nombre")
    with col2: new_email = st.text_input("Correo electrónico")
    with col3:
        new_role = st.selectbox("Rol", ["readonly", "admin"],
                                format_func=lambda r: "Solo lectura" if r == "readonly" else "Administrador")
    new_password = st.text_input("Contraseña", type="password")
    if st.form_submit_button("Crear usuario", type="primary"):
        if not all([new_name, new_email, new_password]):
            st.error("Completa todos los campos.")
        elif create_user(new_email, new_password, new_name, new_role):
            st.success(f"Usuario {new_email} creado.")
            st.rerun()
        else:
            st.error("El correo ya existe o hubo un error.")
st.markdown('</div>', unsafe_allow_html=True)

# ── Lista usuarios ──
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">Usuarios activos</div>', unsafe_allow_html=True)
users = get_all_users()
if not users:
    st.info("No hay usuarios todavía.")
else:
    for u in users:
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        role  = u.get("role", "readonly")
        color = "#0128c9" if role == "admin" else "#888"
        label = "Administrador" if role == "admin" else "Solo lectura"
        with c1:
            st.markdown(f'<span style="font-size:13px;font-weight:500;color:#333;">{u.get("name","—")}</span><br>'
                        f'<span style="font-size:11px;color:#888;">{u.get("email","—")}</span>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<span style="font-size:12px;color:{color};font-weight:500;">{"🔑" if role=="admin" else "👁"} {label}</span>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<span style="font-size:11px;color:#bbb;">{u.get("created_at","")[:10]}</span>', unsafe_allow_html=True)
        with c4:
            if u.get("email") != st.session_state.get("user_email"):
                if st.button("Eliminar", key=f"del_{u['email']}"):
                    if delete_user(u["email"]):
                        st.success("Eliminado.")
                        st.rerun()
        st.markdown('<hr style="border:none;border-top:1px solid #f5f5f5;margin:6px 0;">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Cambiar contraseña propia ──
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">Cambiar mi contraseña</div>', unsafe_allow_html=True)
with st.form("change_pw"):
    new_pw  = st.text_input("Nueva contraseña", type="password")
    new_pw2 = st.text_input("Confirmar contraseña", type="password")
    if st.form_submit_button("Cambiar contraseña"):
        if new_pw != new_pw2:
            st.error("Las contraseñas no coinciden.")
        elif len(new_pw) < 6:
            st.error("Mínimo 6 caracteres.")
        elif update_password(st.session_state["user_email"], new_pw):
            st.success("Contraseña actualizada.")
        else:
            st.error("Error actualizando.")
st.markdown('</div>', unsafe_allow_html=True)

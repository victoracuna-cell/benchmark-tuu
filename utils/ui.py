import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.auth import logout

def render_sidebar():
    with st.sidebar:
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

        role = st.session_state.get("role", "readonly")
        user_name = st.session_state.get("user_name", "Usuario")
        role_label = "Administrador" if role == "admin" else "Solo lectura"
        role_color = "#0128c9" if role == "admin" else "#888"

        st.markdown(f"""
        <div class="sb-logo-row">
            <div class="sb-dot"></div>
            <div class="sb-brand">Benchmark TUU</div>
        </div>
        <div style="padding: 0 1.25rem 1.25rem;">
            <div style="font-size:12px;font-weight:500;color:#333;">{user_name}</div>
            <div style="font-size:11px;color:{role_color};margin-top:2px;">
                {'🔑' if role == 'admin' else '👁'} {role_label}
            </div>
        </div>
        <div class="sb-caption">Análisis competitivo · Chile</div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section">Vistas</div>', unsafe_allow_html=True)
        st.page_link("app.py", label="Dashboard")

        if role == "admin":
            st.markdown('<div class="sb-section">Administración</div>', unsafe_allow_html=True)
            st.page_link("pages/1_actualizar.py", label="Actualizar datos")
            st.page_link("pages/2_editar.py",     label="Editar manual")
            st.page_link("pages/3_exportar.py",   label="Exportar")
            st.page_link("pages/4_usuarios.py",   label="Gestión de usuarios")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        if st.button("Cerrar sesión", use_container_width=True):
            logout()
            st.query_params["logout"] = "true"
            st.rerun()

        st.markdown("""
        <div class="sb-footer">
            Browserless · Groq · GitHub<br>
            Datos en tiempo real
        </div>
        """, unsafe_allow_html=True)

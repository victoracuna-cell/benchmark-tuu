import streamlit as st
from utils.auth import login, get_user_role, logout
from utils.styles import GLOBAL_CSS

def render_login():
    """Full-page login screen."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #f8faff !important; }
    .login-wrap {
        max-width: 400px; margin: 6vh auto 0;
        background: #fff; border: 1px solid #ebebeb;
        border-radius: 18px; padding: 2.5rem 2.25rem;
    }
    .login-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 2rem; }
    .login-dot { width: 10px; height: 10px; border-radius: 50%; background: #0128c9; }
    .login-brand { font-size: 1rem; font-weight: 600; color: #0128c9; letter-spacing: -0.01em; }
    .login-title { font-size: 1.4rem; font-weight: 700; color: #0a0a0a;
                   letter-spacing: -0.03em; margin-bottom: 0.25rem; }
    .login-sub { font-size: 0.78rem; color: #888; margin-bottom: 1.75rem; }
    </style>
    <div class="login-wrap">
        <div class="login-logo">
            <div class="login-dot"></div>
            <div class="login-brand">Benchmark TUU</div>
        </div>
        <div class="login-title">Iniciar sesión</div>
        <div class="login-sub">Análisis competitivo · Mercado de pagos Chile</div>
    </div>
    """, unsafe_allow_html=True)

    # Use columns to center the form
    _, col, _ = st.columns([1, 2, 1])
    with col:
        with st.container(border=False):
            email = st.text_input("Correo electrónico", placeholder="correo@empresa.cl",
                                  label_visibility="collapsed" if False else "visible")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")

            if st.button("Ingresar", type="primary", use_container_width=True):
                if not email or not password:
                    st.error("Ingresa tu correo y contraseña.")
                else:
                    with st.spinner("Verificando..."):
                        result = login(email, password)
                    if result:
                        access_token = result.get("access_token")
                        user = result.get("user", {})
                        user_id = user.get("id")
                        user_meta = user.get("user_metadata", {})

                        role = get_user_role(user_id, access_token)

                        st.session_state["user"] = email
                        st.session_state["user_id"] = user_id
                        st.session_state["user_name"] = user_meta.get("name", email.split("@")[0])
                        st.session_state["role"] = role
                        st.session_state["access_token"] = access_token
                        st.rerun()
                    else:
                        st.error("Correo o contraseña incorrectos.")

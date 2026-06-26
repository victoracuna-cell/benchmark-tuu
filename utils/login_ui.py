import streamlit as st
from utils.auth import login
from utils.styles import GLOBAL_CSS

def render_login():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #f8faff !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    .login-header {
        text-align: center;
        padding: 4rem 0 2rem;
    }
    .login-logo-row {
        display: flex; align-items: center; justify-content: center;
        gap: 10px; margin-bottom: 1rem;
    }
    .login-dot { width: 10px; height: 10px; border-radius: 50%; background: #0128c9; }
    .login-brand { font-size: 1rem; font-weight: 600; color: #0128c9; }
    .login-title {
        font-size: 1.6rem; font-weight: 700; color: #0a0a0a;
        letter-spacing: -0.03em; margin-bottom: 0.35rem;
    }
    .login-sub { font-size: 0.78rem; color: #888; }
    </style>
    <div class="login-header">
        <div class="login-logo-row">
            <div class="login-dot"></div>
            <div class="login-brand">Benchmark TUU</div>
        </div>
        <div class="login-title">Iniciar sesión</div>
        <div class="login-sub">Análisis competitivo · Mercado de pagos Chile</div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        email    = st.text_input("Correo electrónico", placeholder="correo@empresa.cl")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Ingresar", type="primary", use_container_width=True):
            if not email or not password:
                st.error("Ingresa tu correo y contraseña.")
                return
            with st.spinner("Verificando..."):
                user = login(email, password)
            if user:
                st.session_state["user"]       = user["email"]
                st.session_state["user_email"] = user["email"]
                st.session_state["user_name"]  = user.get("name", email.split("@")[0])
                st.session_state["role"]       = user.get("role", "readonly")
                st.rerun()
            else:
                st.error("Correo o contraseña incorrectos.")

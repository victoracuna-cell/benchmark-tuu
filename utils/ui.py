import streamlit as st
from utils.styles import GLOBAL_CSS

def render_sidebar():
    with st.sidebar:
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-logo-row">
            <div class="sb-dot"></div>
            <div class="sb-brand">Benchmark TUU</div>
        </div>
        <div class="sb-caption">Análisis competitivo · Chile</div>

        <div class="sb-section">Principal</div>
        """, unsafe_allow_html=True)

        st.page_link("app.py",               label="Dashboard")
        st.page_link("pages/1_actualizar.py", label="Actualizar datos")
        st.page_link("pages/2_editar.py",     label="Editar manual")
        st.page_link("pages/3_exportar.py",   label="Exportar")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="sb-footer">
            Browserless · Groq · GitHub<br>
            Datos en tiempo real
        </div>
        """, unsafe_allow_html=True)

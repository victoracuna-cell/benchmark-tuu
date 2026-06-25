import streamlit as st
from utils.styles import GLOBAL_CSS
from datetime import date

def render_sidebar():
    with st.sidebar:
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-logo-row">
            <div class="sb-dot"></div>
            <div class="sb-brand">Benchmark TUU</div>
        </div>
        <div class="sb-caption">Análisis competitivo · Chile</div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section">Principal</div>', unsafe_allow_html=True)
        st.page_link("app.py",               label="Dashboard",        icon="⊞")
        st.page_link("pages/1_actualizar.py", label="Actualizar datos", icon="↻")
        st.page_link("pages/2_editar.py",     label="Editar manual",    icon="✎")
        st.page_link("pages/3_exportar.py",   label="Exportar",         icon="↓")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-section">Vistas</div>', unsafe_allow_html=True)
        st.page_link("app.py", label="Comisiones",  icon="%")
        st.page_link("app.py", label="Hardware",    icon="□")
        st.page_link("app.py", label="Documentos",  icon="≡")
        st.page_link("app.py", label="Simulador",   icon="◈")

        st.markdown(f"""
        <div class="sb-footer">
            Tavily · Groq · GitHub<br>
            Datos scrapeados en vivo
        </div>
        """, unsafe_allow_html=True)

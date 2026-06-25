import streamlit as st
from utils.styles import GLOBAL_CSS

def render_sidebar():
    with st.sidebar:
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
        st.markdown("""
        <div style="padding: 0.5rem 0.75rem 1.5rem;">
            <div class="sidebar-logo">📊 Benchmark TUU</div>
            <div class="sidebar-caption">Análisis competitivo · Chile</div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link("app.py",               label="  Dashboard",        icon="🏠")
        st.page_link("pages/1_actualizar.py", label="  Actualizar datos", icon="🔄")
        st.page_link("pages/2_editar.py",     label="  Editar manual",    icon="✏️")
        st.page_link("pages/3_exportar.py",   label="  Exportar",         icon="📥")

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        st.markdown("""
        <div style="padding: 0.5rem 0.75rem; font-size: 11px; color: #8292b0; line-height: 1.6;">
            Fuentes: sitios oficiales<br>
            Storage: GitHub JSON<br>
            Scraping: Tavily API
        </div>
        """, unsafe_allow_html=True)

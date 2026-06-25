import streamlit as st

st.set_page_config(
    page_title="Benchmark TUU",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import GLOBAL_CSS
from utils.github_storage import load_data
from utils.ui import render_sidebar

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

render_sidebar()

from utils.github_storage import load_data
data = load_data()

st.markdown('<p class="page-title">📊 Benchmark TUU vs Competencia</p>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Análisis competitivo · Mercado de pagos Chile 2025–2026 · Datos scrapeados desde sitios oficiales</p>', unsafe_allow_html=True)

if not data or not data.get("competitors"):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.info("Sin datos todavía. Ve a **Actualizar datos** en el menú para hacer el primer scraping.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

last_updated = data.get("last_updated", "—")
competitors = data.get("competitors", {})
n_comp = len([k for k in competitors if k != "tuu"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Competidores", n_comp)
col2.metric("Dimensiones", 7)
col3.metric("Segmentos", 3)
col4.metric("Actualizado", last_updated[:10] if last_updated != "—" else "—")

st.markdown("<br>", unsafe_allow_html=True)

tabs = st.tabs(["Resumen", "Comisiones", "Hardware", "Documentos", "Abono", "Gestión", "Soporte", "Financieros", "Simulador"])

from views import resumen, comisiones, hardware, documentos, abono, gestion, soporte, financieros, simulador

with tabs[0]: resumen.render(data)
with tabs[1]: comisiones.render(data)
with tabs[2]: hardware.render(data)
with tabs[3]: documentos.render(data)
with tabs[4]: abono.render(data)
with tabs[5]: gestion.render(data)
with tabs[6]: soporte.render(data)
with tabs[7]: financieros.render(data)
with tabs[8]: simulador.render(data)

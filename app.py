import streamlit as st

st.set_page_config(
    page_title="Benchmark TUU",
    page_icon="●",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import GLOBAL_CSS
from utils.login_ui import render_login
from utils.auth import logout
from utils.ui import render_sidebar
from datetime import date

# ── Auth gate ──
if "user" not in st.session_state:
    render_login()
    st.stop()

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

from utils.github_storage import load_data
from utils.scoring import COMPETITOR_ORDER, weighted_total, get_all_scores

data = load_data()
competitors = data.get("competitors", {}) if data else {}
last_updated = data.get("last_updated", "") if data else ""
last_date = last_updated[:10] if last_updated else "—"

st.markdown(f"""
<div class="page-header">
  <div>
    <div class="page-title">Benchmark <span>TUU</span></div>
    <div class="page-sub">
      <span class="dot-cyan"></span>
      TUU vs 5 competidores · 7 dimensiones
    </div>
  </div>
  <div class="page-date">{date.today().strftime('%d %b %Y')}<br>actualizado {last_date}</div>
</div>
""", unsafe_allow_html=True)

if not competitors:
    st.info("Sin datos todavía. Ve a **Actualizar datos** en el menú para hacer el primer scraping.")
    st.stop()

all_scores = get_all_scores(data)
ordered = [c for c in COMPETITOR_ORDER if c in competitors]
totals = {c: weighted_total(all_scores.get(c, {})) for c in ordered}
tuu = competitors.get("tuu", {})
tuu_com = tuu.get("comisiones", {}).get("debito_pct", "—")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="metric-hero">', unsafe_allow_html=True)
    st.metric("Comisión TUU", f"{tuu_com}%" if isinstance(tuu_com, float) else tuu_com, "más baja del mercado")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.metric("Score general", f"{totals.get('tuu', 0):.1f}", "sobre 5 puntos")
with c3:
    st.metric("Competidores", len([c for c in ordered if c != "tuu"]))
with c4:
    st.metric("Dimensiones", 7)

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

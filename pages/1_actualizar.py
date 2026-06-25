import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.github_storage import load_data, save_data, upsert_competitor
from utils.tavily_scraper import tavily_extract, COMPETITOR_SEEDS
from utils.ui import render_sidebar
import json

st.set_page_config(page_title="Actualizar · Benchmark TUU", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown('<p class="page-title">🔄 Actualizar datos</p>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Extrae datos actualizados desde los sitios oficiales usando Tavily + Claude para estructurarlos.</p>', unsafe_allow_html=True)

data = load_data()

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
with st.form("scrape_form"):
    col1, col2 = st.columns(2)
    with col1:
        selected_comps = st.multiselect(
            "Competidores a actualizar",
            options=list(COMPETITOR_SEEDS.keys()),
            default=list(COMPETITOR_SEEDS.keys()),
            format_func=lambda k: COMPETITOR_SEEDS[k]["name"],
        )
    with col2:
        dimensiones = st.multiselect(
            "Dimensiones",
            ["comisiones","hardware","documentos","abono","gestion","soporte","financieros"],
            default=["comisiones","hardware","documentos","abono","gestion","soporte","financieros"],
        )
    submitted = st.form_submit_button("🚀 Iniciar scraping", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

if submitted and selected_comps:
    progress = st.progress(0, text="Iniciando...")
    total_steps = len(selected_comps)

    for i, comp_key in enumerate(selected_comps):
        seed = COMPETITOR_SEEDS[comp_key]
        comp_name = seed["name"]
        progress.progress(i / total_steps, text=f"Scrapeando {comp_name}...")

        with st.status(f"Procesando {comp_name}...", expanded=False) as status:
            pages_to_fetch = list(seed["pages"].values())
            extracted = tavily_extract(pages_to_fetch, query="precios comisiones tarifas boleta factura garantía soporte")
            raw_text = "\n\n".join([r.get("raw_content", "") or "" for r in extracted])[:6000]

            from anthropic import Anthropic
            client = Anthropic()
            system = """Eres un extractor de datos estructurados. Extrae datos de una empresa de pagos chilena y devuelve SOLO JSON válido sin bloques de código:
{
  "name": "Nombre",
  "comisiones": {"debito_pct": 1.49, "credito_pct": 1.49, "prepago_pct": null, "internacional_pct": null, "cargo_fijo": null, "mensualidad_red": null, "notas_comisiones": ""},
  "hardware": {"modelo_principal": "", "precio_lista_clp": null, "precio_oferta_clp": null, "modalidad": "compra", "mensualidad": null, "pantalla": "", "impresora": "", "conectividad": "", "garantia": "", "notas": ""},
  "documentos": {"boleta": "", "costo_boleta_mes": null, "factura": "", "costo_factura_mes": null, "guia_despacho": "", "notas": ""},
  "abono": {"plazo_estandar": "", "abono_inmediato": "", "costo_abono_inmediato": null, "destino": "", "fines_de_semana": "", "notas": ""},
  "gestion": {"pos": "", "catalogo": "", "inventario": "", "agenda": "", "multilocal": "", "reportes": "", "app_movil": "", "notas": ""},
  "soporte": {"canales": "", "horario": "", "garantia": "", "tiempo_respuesta": "", "sla": "", "notas": ""},
  "financieros": {"adelanto": "", "monto_max_adelanto": null, "credito": "", "cuotas_sin_interes": "", "comision_cuotas": null, "notas": ""},
  "scores": {"comisiones": 3.0, "hardware": 3.0, "documentos": 3.0, "abono": 3.0, "gestion": 3.0, "soporte": 3.0, "financieros": 3.0}
}
Scores del 1 al 5. Usa null para datos desconocidos."""

            msg = client.messages.create(
                model="claude-sonnet-4-6", max_tokens=2000, system=system,
                messages=[{"role": "user", "content": f"Empresa: {comp_name}\n\nContenido:\n{raw_text}"}]
            )
            try:
                extracted_json = json.loads(msg.content[0].text)
                data = upsert_competitor(data, comp_key, extracted_json)
                status.update(label=f"✅ {comp_name} — datos extraídos", state="complete")
            except Exception as e:
                status.update(label=f"⚠️ {comp_name} — error: {e}", state="error")

    progress.progress(1.0, text="Guardando en GitHub...")
    if save_data(data, f"chore: scraping — {', '.join(selected_comps)}"):
        st.success("✅ Todos los datos guardados en GitHub correctamente.")
    else:
        st.error("Error guardando. Revisa los secrets de Streamlit.")

st.divider()
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("**Estado actual de los datos**")
if data and data.get("competitors"):
    for comp_key, info in data["competitors"].items():
        with st.expander(f"{info.get('name', comp_key)}"):
            st.json(info)
else:
    st.info("Sin datos guardados todavía.")
st.markdown('</div>', unsafe_allow_html=True)

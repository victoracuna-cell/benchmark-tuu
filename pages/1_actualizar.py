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
st.markdown('<p class="page-subtitle">Extrae datos desde sitios oficiales con Tavily · Estructura con Llama 3 vía Groq (gratis)</p>', unsafe_allow_html=True)

data = load_data()

SYSTEM_PROMPT = """Eres un extractor de datos estructurados. Extrae datos de una empresa de pagos chilena y devuelve SOLO JSON válido, sin bloques de código, sin explicaciones, sin texto adicional. Solo el JSON:
{
  "name": "Nombre empresa",
  "comisiones": {"debito_pct": 1.49, "credito_pct": 1.49, "prepago_pct": null, "internacional_pct": null, "cargo_fijo": null, "mensualidad_red": null, "notas_comisiones": ""},
  "hardware": {"modelo_principal": "", "precio_lista_clp": null, "precio_oferta_clp": null, "modalidad": "compra", "mensualidad": null, "pantalla": "", "impresora": "", "conectividad": "", "garantia": "", "notas": ""},
  "documentos": {"boleta": "", "costo_boleta_mes": null, "factura": "", "costo_factura_mes": null, "guia_despacho": "", "notas": ""},
  "abono": {"plazo_estandar": "", "abono_inmediato": "", "costo_abono_inmediato": null, "destino": "", "fines_de_semana": "", "notas": ""},
  "gestion": {"pos": "", "catalogo": "", "inventario": "", "agenda": "", "multilocal": "", "reportes": "", "app_movil": "", "notas": ""},
  "soporte": {"canales": "", "horario": "", "garantia": "", "tiempo_respuesta": "", "sla": "", "notas": ""},
  "financieros": {"adelanto": "", "monto_max_adelanto": null, "credito": "", "cuotas_sin_interes": "", "comision_cuotas": null, "notas": ""},
  "scores": {"comisiones": 3.0, "hardware": 3.0, "documentos": 3.0, "abono": 3.0, "gestion": 3.0, "soporte": 3.0, "financieros": 3.0}
}
Scores del 1 al 5 (5 = mejor del mercado). Usa null para datos desconocidos. Devuelve SOLO el JSON, nada más."""

def call_groq(comp_name: str, raw_text: str) -> dict:
    from groq import Groq
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Empresa: {comp_name}\n\nContenido web:\n{raw_text}"}
        ]
    )
    raw = completion.choices[0].message.content.strip()
    # Llama a veces devuelve bloques ```json ``` — los limpiamos
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1].lstrip("json").strip() if len(parts) > 1 else raw
    return json.loads(raw)

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
        st.markdown("**Modelo**")
        st.caption("Llama 3.3 70B · Groq · Gratis")
    submitted = st.form_submit_button("🚀 Iniciar scraping", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

if submitted and selected_comps:
    progress = st.progress(0, text="Iniciando...")

    for i, comp_key in enumerate(selected_comps):
        seed = COMPETITOR_SEEDS[comp_key]
        comp_name = seed["name"]
        progress.progress(i / len(selected_comps), text=f"Scrapeando {comp_name}...")

        with st.status(f"Procesando {comp_name}...", expanded=False) as status:
            try:
                pages_to_fetch = list(seed["pages"].values())
                extracted = tavily_extract(
                    pages_to_fetch,
                    query="precios comisiones tarifas boleta factura garantía soporte abono"
                )
                raw_text = "\n\n".join([r.get("raw_content", "") or "" for r in extracted])[:6000]

                if not raw_text.strip():
                    status.update(label=f"⚠️ {comp_name} — sin contenido extraído", state="error")
                    continue

                structured = call_groq(comp_name, raw_text)
                data = upsert_competitor(data, comp_key, structured)
                status.update(label=f"✅ {comp_name} — listo", state="complete")

            except json.JSONDecodeError as e:
                status.update(label=f"⚠️ {comp_name} — JSON inválido: {e}", state="error")
            except Exception as e:
                status.update(label=f"⚠️ {comp_name} — error: {e}", state="error")

    progress.progress(1.0, text="Guardando en GitHub...")
    if save_data(data, f"chore: scraping — {', '.join(selected_comps)}"):
        st.success("✅ Datos guardados en GitHub.")
        st.balloons()
    else:
        st.error("No se pudo guardar en GitHub. Revisa los secrets.")

st.divider()
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("**Estado actual de los datos**")
data_actual = load_data()
if data_actual and data_actual.get("competitors"):
    cols = st.columns(3)
    for idx, (comp_key, info) in enumerate(data_actual["competitors"].items()):
        with cols[idx % 3]:
            with st.expander(f"{info.get('name', comp_key)}"):
                scores = info.get("scores", {})
                if scores:
                    for dim, val in scores.items():
                        st.caption(f"{dim}: {val}")
                st.json(info, expanded=False)
else:
    st.info("Sin datos todavía. Ejecuta el scraping arriba.")
st.markdown('</div>', unsafe_allow_html=True)

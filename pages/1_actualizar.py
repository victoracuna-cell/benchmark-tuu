import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.github_storage import load_data, save_data, upsert_competitor
from utils.firecrawl_scraper import scrape_competitor, scrape_with_browserless, COMPETITOR_SEEDS
from utils.ui import render_sidebar
import json
import requests

st.set_page_config(page_title="Actualizar · Benchmark TUU", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown('<p style="font-size:1.75rem;font-weight:700;color:#0a0a0a;letter-spacing:-0.04em;margin-bottom:0.25rem;">Actualizar datos</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:0.7rem;color:#888;margin-bottom:1.5rem;">Extrae desde sitios oficiales con Firecrawl · Estructura con Llama 3.3 vía Groq</p>', unsafe_allow_html=True)

data = load_data()

SYSTEM_PROMPT = """Eres un extractor de datos estructurados. Extrae datos de una empresa de pagos chilena y devuelve SOLO JSON válido, sin bloques de código, sin explicaciones. Solo el JSON:
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
Scores 1-5 (5=mejor del mercado). null para datos desconocidos. SOLO el JSON."""

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
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1].lstrip("json").strip() if len(parts) > 1 else raw
    return json.loads(raw)

# ── Test conexiones ──
with st.expander("Verificar conexiones", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Test Browserless"):
            import re
            key = st.secrets.get("BROWSERLESS_API_KEY", "")
            st.write(f"Key: `{'Sí — ' + key[:10] + '...' if key else 'NO encontrado'}`")
            r = requests.post(
                "https://chrome.browserless.io/content",
                params={"token": key},
                json={"url": "https://www.tuu.cl/precios", "waitFor": 2000},
                timeout=25,
            )
            st.write(f"HTTP: `{r.status_code}`")
            if r.status_code == 200:
                text = re.sub(r'<[^>]+>', ' ', r.text)
                text = re.sub(r'\s+', ' ', text).strip()
                st.success(f"Browserless OK — {len(text)} chars extraídos")
                st.text(text[:300] + "...")
            else:
                st.error(f"Error: {r.text[:200]}")
    with col2:
        if st.button("Test Groq"):
            try:
                from groq import Groq
                key = st.secrets.get("GROQ_API_KEY", "")
                st.write(f"Key: `{'Sí — ' + key[:8] + '...' if key else 'NO encontrado'}`")
                client = Groq(api_key=key)
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", max_tokens=10,
                    messages=[{"role": "user", "content": "Responde: OK"}]
                )
                st.success(f"Groq OK — {r.choices[0].message.content}")
            except Exception as e:
                st.error(f"Error: {e}")

# ── Formulario scraping ──
st.markdown('<div class="card">', unsafe_allow_html=True)
with st.form("scrape_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_comps = st.multiselect(
            "Competidores a actualizar",
            options=list(COMPETITOR_SEEDS.keys()),
            default=list(COMPETITOR_SEEDS.keys()),
            format_func=lambda k: COMPETITOR_SEEDS[k]["name"],
        )
    with col2:
        st.markdown("**Modelo**")
        st.caption("Llama 3.3 70B · Groq")
    submitted = st.form_submit_button("Iniciar scraping", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

if submitted and selected_comps:
    progress = st.progress(0, text="Iniciando...")
    total = len(selected_comps)

    for i, comp_key in enumerate(selected_comps):
        seed = COMPETITOR_SEEDS[comp_key]
        comp_name = seed["name"]
        progress.progress(i / total, text=f"Procesando {comp_name}...")

        with st.status(f"{comp_name}", expanded=True) as status:
            try:
                status.write(f"Scrapeando {len(seed['pages'])} páginas con Firecrawl...")
                raw_text = scrape_competitor(seed)

                if not raw_text.strip():
                    status.update(label=f"{comp_name} — sin contenido extraído", state="error")
                    continue

                status.write(f"{len(raw_text)} chars extraídos · estructurando con Groq...")
                structured = call_groq(comp_name, raw_text)
                data = upsert_competitor(data, comp_key, structured)
                status.update(label=f"{comp_name} — listo", state="complete")

            except json.JSONDecodeError as e:
                status.update(label=f"{comp_name} — JSON inválido: {e}", state="error")
            except Exception as e:
                status.update(label=f"{comp_name} — {type(e).__name__}: {e}", state="error")

    progress.progress(1.0, text="Guardando en GitHub...")
    if save_data(data, f"chore: scraping — {', '.join(selected_comps)}"):
        st.success("Datos guardados en GitHub.")
        st.balloons()
    else:
        st.error("No se pudo guardar en GitHub.")

st.divider()
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">Estado actual</div>', unsafe_allow_html=True)
data_actual = load_data()
if data_actual and data_actual.get("competitors"):
    cols = st.columns(3)
    for idx, (comp_key, info) in enumerate(data_actual["competitors"].items()):
        with cols[idx % 3]:
            with st.expander(info.get("name", comp_key)):
                scores = info.get("scores", {})
                for dim, val in scores.items():
                    st.caption(f"{dim}: {val}")
                st.json(info, expanded=False)
else:
    st.info("Sin datos todavía. Ejecuta el scraping arriba.")
st.markdown('</div>', unsafe_allow_html=True)

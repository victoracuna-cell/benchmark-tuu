import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.github_storage import load_data, save_data, upsert_competitor
from utils.tavily_scraper import COMPETITOR_SEEDS
from utils.ui import render_sidebar
import json
import requests

st.set_page_config(page_title="Actualizar · Benchmark TUU", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown('<p style="font-size:1.75rem;font-weight:700;color:#0a0a0a;letter-spacing:-0.04em;margin-bottom:0.25rem;">Actualizar datos</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:0.7rem;color:#888;margin-bottom:1.5rem;">Extrae desde sitios oficiales con Tavily · Estructura con Llama 3.3 vía Groq</p>', unsafe_allow_html=True)

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
Scores 1-5 (5=mejor). null para datos desconocidos. SOLO el JSON."""

def tavily_search(query: str) -> tuple[str, str]:
    """Returns (content, debug_info)"""
    key = st.secrets.get("TAVILY_API_KEY", "")
    if not key:
        return "", "ERROR: TAVILY_API_KEY no encontrado en secrets"

    try:
        r = requests.post("https://api.tavily.com/search", json={
            "api_key": key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 5,
            "include_raw_content": True,
        }, timeout=25)

        debug = f"HTTP {r.status_code}"
        if r.status_code != 200:
            return "", f"{debug} — {r.text[:200]}"

        results = r.json().get("results", [])
        debug += f" · {len(results)} resultados"

        parts = []
        for res in results:
            text = res.get("raw_content") or res.get("content") or ""
            if text:
                parts.append(f"URL: {res.get('url','')}\n{text}")

        content = "\n\n---\n\n".join(parts)[:6000]
        debug += f" · {len(content)} chars"
        return content, debug

    except Exception as e:
        return "", f"Exception: {type(e).__name__}: {e}"

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

# ── Debug panel ──
with st.expander("Verificar conexiones antes de scraping", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Test Tavily"):
            key = st.secrets.get("TAVILY_API_KEY", "")
            st.write(f"Key presente: `{'Sí — ' + key[:8] + '...' if key else 'NO'}`")
            content, debug = tavily_search("TUU Chile máquina pagos precios")
            st.write(f"Resultado: `{debug}`")
            if content:
                st.success("Tavily funciona correctamente")
                st.text(content[:300] + "...")
            else:
                st.error("Tavily no retornó contenido")
    with col2:
        if st.button("Test Groq"):
            try:
                from groq import Groq
                key = st.secrets.get("GROQ_API_KEY", "")
                st.write(f"Key presente: `{'Sí — ' + key[:8] + '...' if key else 'NO'}`")
                client = Groq(api_key=key)
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=20,
                    messages=[{"role": "user", "content": "Responde solo: OK"}]
                )
                st.success(f"Groq OK — respuesta: {r.choices[0].message.content}")
            except Exception as e:
                st.error(f"Error Groq: {e}")

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
                query = f"{comp_name} Chile precios comisiones tarifas máquina POS boleta electrónica"
                raw_text, debug = tavily_search(query)
                status.write(f"Tavily: {debug}")

                if not raw_text.strip():
                    status.update(label=f"{comp_name} — sin contenido ({debug})", state="error")
                    continue

                status.write(f"Estructurando con Groq...")
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

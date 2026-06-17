import streamlit as st
import json
import anthropic
from firecrawl import FirecrawlApp
from datetime import datetime
import pandas as pd
import time

st.set_page_config(
    page_title="Benchmark POS Chile — TUU",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Fondo general */
.stApp { background: #F7F8FA; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E8EAF0;
}
[data-testid="stSidebar"] .stMarkdown h2 {
    font-size: 13px;
    font-weight: 600;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 1.5rem;
}

/* Inputs */
[data-testid="stTextInput"] input {
    border-radius: 8px !important;
    border: 1.5px solid #E0E4EA !important;
    font-size: 13px !important;
    background: #F9FAFB !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #1D9E75 !important;
    background: #fff !important;
}

/* Botón primario */
.stButton > button[kind="primary"] {
    background: #1D9E75 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0.6rem 1.2rem !important;
    color: #fff !important;
    transition: background 0.2s;
}
.stButton > button[kind="primary"]:hover {
    background: #0F6E56 !important;
}
.stButton > button[kind="secondary"] {
    border-radius: 8px !important;
    border: 1.5px solid #E0E4EA !important;
    font-size: 13px !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #E8EAF0;
    width: fit-content;
}
[data-testid="stTabs"] button[role="tab"] {
    border-radius: 7px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    color: #6B7280 !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: #1D9E75 !important;
    color: #fff !important;
}

/* Métricas */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    border: 1px solid #E8EAF0;
}
[data-testid="stMetricLabel"] { font-size: 12px !important; color: #6B7280 !important; font-weight: 500 !important; }
[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 600 !important; color: #1A1A2E !important; }

/* Cards empresa */
[data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"] {
    gap: 0;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E8EAF0;
}

/* Progress */
[data-testid="stProgress"] > div > div {
    background: #1D9E75 !important;
    border-radius: 4px !important;
}

/* Expander */
[data-testid="stExpander"] {
    border: 1px solid #E8EAF0 !important;
    border-radius: 10px !important;
    background: #fff !important;
}

/* Alerts / info */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 14px !important;
}

/* Download buttons */
[data-testid="stDownloadButton"] button {
    border-radius: 8px !important;
    border: 1.5px solid #E0E4EA !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    width: 100%;
}

/* Header hero */
.hero {
    background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF8 100%);
    border: 1px solid #D1FAE5;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
}
.hero h1 { font-size: 28px; font-weight: 700; color: #1A1A2E; margin: 0 0 6px 0; }
.hero p { color: #6B7280; font-size: 15px; margin: 0; }

/* Company card */
.company-card {
    background: #FFFFFF;
    border: 1px solid #E8EAF0;
    border-radius: 14px;
    padding: 1.25rem;
    height: 100%;
    transition: box-shadow 0.2s;
}
.company-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
.company-card.tuu {
    border: 2px solid #1D9E75;
    background: linear-gradient(135deg, #FFFFFF, #F0FDF8);
}
.company-name { font-size: 15px; font-weight: 600; color: #1A1A2E; margin-bottom: 2px; }
.company-domain { font-size: 11px; color: #9CA3AF; margin-bottom: 10px; }
.company-resumen { font-size: 12px; color: #6B7280; line-height: 1.5; margin-bottom: 12px; min-height: 40px; }
.company-stat { display: flex; justify-content: space-between; align-items: center; padding: 5px 0; border-bottom: 1px solid #F3F4F6; font-size: 12px; }
.company-stat:last-child { border-bottom: none; }
.stat-label { color: #9CA3AF; }
.stat-val { font-weight: 600; color: #1A1A2E; }
.badge { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 20px; margin-bottom: 8px; }
.badge-tuu { background: #D1FAE5; color: #065F46; }
.score-row { display: flex; align-items: center; gap: 8px; margin-top: 10px; font-size: 11px; color: #9CA3AF; }
.score-bar { flex: 1; height: 4px; background: #F3F4F6; border-radius: 2px; overflow: hidden; }
.score-fill { height: 100%; border-radius: 2px; }
.score-fill-green { background: #1D9E75; }
.score-fill-blue { background: #378ADD; }

/* Insight cards */
.insight { border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 10px; }
.insight-oportunidad { background: #F0FDF8; border-left: 4px solid #1D9E75; }
.insight-ventaja { background: #EFF6FF; border-left: 4px solid #378ADD; }
.insight-alerta { background: #FFFBEB; border-left: 4px solid #F59E0B; }
.insight-title { font-size: 13px; font-weight: 600; color: #1A1A2E; margin-bottom: 4px; }
.insight-desc { font-size: 12px; color: #6B7280; line-height: 1.6; }

/* Resumen ejecutivo */
.resumen-box {
    background: #FFFFFF;
    border: 1px solid #E8EAF0;
    border-left: 4px solid #1D9E75;
    border-radius: 0 12px 12px 0;
    padding: 1.25rem 1.5rem;
    font-size: 14px;
    color: #374151;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}

/* Sidebar brand */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid #E8EAF0;
    margin-bottom: 1rem;
}
.sidebar-brand-name { font-size: 15px; font-weight: 700; color: #1A1A2E; }
.sidebar-brand-sub { font-size: 11px; color: #9CA3AF; }

/* Log area */
.log-box {
    background: #0F172A;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #94A3B8;
    line-height: 2;
}

/* Ocultar el menú hamburguesa y footer de Streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Datos ─────────────────────────────────────────────────────────────────────
SITES = {
    "tuu.cl": {"urls": ["https://tuu.cl", "https://tuu.cl/precios"], "label": "TUU", "emoji": "⭐"},
    "transbank.cl": {"urls": ["https://www.transbank.cl/pos"], "label": "Transbank", "emoji": "🏦"},
    "mercadopago.cl": {"urls": ["https://www.mercadopago.cl/point"], "label": "Mercado Pago", "emoji": "💛"},
    "sumup.cl": {"urls": ["https://www.sumup.com/es-cl/"], "label": "SumUp", "emoji": "🔵"},
    "compraqui.cl": {"urls": ["https://www.compraqui.cl"], "label": "Compraquí", "emoji": "🟢"},
    "getnet.cl": {"urls": ["https://www.getnet.cl"], "label": "Getnet", "emoji": "🟠"},
    "redelcom.cl": {"urls": ["https://www.redelcom.cl"], "label": "Redelcom", "emoji": "🔴"},
}

DEFAULTS = ["transbank.cl", "mercadopago.cl", "sumup.cl", "compraqui.cl"]

ANALYSIS_PROMPT = """Eres un analista de mercado experto en medios de pago y POS en Chile.
Analiza el contenido scrapeado y extrae información estructurada.
Responde SOLO con JSON válido, sin markdown ni backticks.

{
  "companies": [
    {
      "name": "nombre",
      "domain": "dominio.cl",
      "tipo": "POS/PSP/Adquirente",
      "precio_dispositivo": "precio CLP o 'Arriendo' o 'N/D'",
      "comision_debito": "% + IVA o 'N/D'",
      "comision_credito": "% + IVA o 'N/D'",
      "comision_unica": "% si aplica o null",
      "mensualidad": "monto o 'Sin mensualidad' o 'N/D'",
      "plazo_abono": "ej: '1 día hábil'",
      "boleta_electronica": true/false/null,
      "factura_electronica": true/false/null,
      "conectividad": ["wifi","4g"],
      "impresora": true/false/null,
      "cuotas": true/false/null,
      "apple_pay_google_pay": true/false/null,
      "inventario": true/false/null,
      "link_pago": true/false/null,
      "ecommerce": true/false/null,
      "app_movil": true/false/null,
      "score_precio": 1-10,
      "score_funcionalidades": 1-10,
      "ventajas": ["ventaja 1", "ventaja 2"],
      "desventajas": ["desventaja 1"],
      "resumen": "2 frases propuesta de valor"
    }
  ],
  "insights": [
    {"tipo": "oportunidad|ventaja|alerta", "titulo": "título", "descripcion": "2-3 frases con datos"}
  ],
  "resumen_ejecutivo": "Párrafo de 4-5 frases con conclusiones principales"
}"""


def scrape_site(app, urls):
    combined = []
    for url in urls:
        try:
            result = app.scrape_url(url, formats=["markdown"])
            content = result.markdown if hasattr(result, "markdown") else str(result)
            if content:
                combined.append(f"[URL: {url}]\n{content[:3000]}")
        except Exception as e:
            combined.append(f"[URL: {url}]\nError: {str(e)}")
    return "\n\n".join(combined)


def analyze_with_claude(anthropic_key, scraped_data):
    client = anthropic.Anthropic(api_key=anthropic_key)
    blocks = [
        f"{'='*50}\n{SITES.get(d,{}).get('label',d)} ({d})\n{'='*50}\n{c}"
        for d, c in scraped_data.items()
    ]
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4000,
        system=ANALYSIS_PROMPT,
        messages=[{"role": "user", "content":
            f"Analiza estos datos de POS/pagos en Chile. TUU es la referencia.\n\n{''.join(blocks)}\n\nUsa 'N/D' si no encontrás un dato."}]
    )
    text = response.content[0].text.strip().replace("```json","").replace("```","").strip()
    return json.loads(text)


def b(val):
    return "✅" if val is True else "❌" if val is False else "❓"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div>
            <div class="sidebar-brand-name">📊 Benchmark POS</div>
            <div class="sidebar-brand-sub">Firecrawl + Claude Opus 4.6</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("## 🔑 API Keys")
    fc_key = st.text_input("Firecrawl", type="password", placeholder="fc-...", label_visibility="collapsed")
    st.caption("Firecrawl API key (fc-...)")
    anthropic_key = st.text_input("Anthropic", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    st.caption("Anthropic API key (sk-ant-...)")

    st.markdown("## 🏢 Competidores")
    selected = ["tuu.cl"]
    for domain, info in SITES.items():
        if domain == "tuu.cl":
            continue
        if st.checkbox(f"{info['emoji']} {info['label']}", value=domain in DEFAULTS):
            selected.append(domain)

    custom = st.text_input("➕ Agregar URL", placeholder="https://...", label_visibility="collapsed")
    st.caption("URL personalizada (opcional)")

    st.markdown("---")
    keys_ok = bool(fc_key and anthropic_key and fc_key.startswith("fc-"))
    run = st.button("🚀 Iniciar benchmark", type="primary", use_container_width=True, disabled=not keys_ok)
    if not keys_ok:
        st.caption("⚠️ Completá ambas API keys primero")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📊 Benchmark competitivo TUU</h1>
    <p>Análisis automatizado de precios, funcionalidades y planes del mercado POS en Chile</p>
</div>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = None
if "raw" not in st.session_state:
    st.session_state.raw = None

# ── Scraping ──────────────────────────────────────────────────────────────────
if run:
    domains = selected.copy()
    if custom:
        clean = custom.replace("https://","").replace("http://","").rstrip("/")
        SITES[clean] = {"urls": [custom], "label": clean, "emoji": "🌐"}
        domains.append(clean)

    fc_app = FirecrawlApp(api_key=fc_key)
    scraped = {}

    col_prog, _ = st.columns([2, 1])
    with col_prog:
        prog = st.progress(0, text="Iniciando...")
        status = st.empty()
        logs = []

    for i, domain in enumerate(domains):
        info = SITES.get(domain, {"urls": [f"https://{domain}"], "label": domain})
        pct = int((i / (len(domains) + 1)) * 85)
        prog.progress(pct, text=f"Scrapeando {info['label']}...")
        logs.append(f"⏳ {info['label']} ({domain})")
        status.markdown('<div class="log-box">' + "<br>".join(logs) + "</div>", unsafe_allow_html=True)
        try:
            content = scrape_site(fc_app, info["urls"])
            scraped[domain] = content
            logs[-1] = f"✅ {info['label']} — {len(content):,} caracteres"
        except Exception as e:
            scraped[domain] = f"Error: {str(e)}"
            logs[-1] = f"❌ {info['label']} — {str(e)}"
        status.markdown('<div class="log-box">' + "<br>".join(logs) + "</div>", unsafe_allow_html=True)
        time.sleep(0.3)

    prog.progress(88, text="Analizando con Claude Opus 4.6...")
    logs.append("🤖 Enviando a Claude para análisis estructurado...")
    status.markdown('<div class="log-box">' + "<br>".join(logs) + "</div>", unsafe_allow_html=True)

    try:
        result = analyze_with_claude(anthropic_key, scraped)
        result["_meta"] = {"generado_en": datetime.now().isoformat(), "sitios": domains}
        st.session_state.data = result
        st.session_state.raw = scraped
        logs.append(f"✅ Análisis completo — {len(result.get('companies',[]))} empresas")
        status.markdown('<div class="log-box">' + "<br>".join(logs) + "</div>", unsafe_allow_html=True)
        prog.progress(100, text="¡Listo!")
        time.sleep(0.8)
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error en análisis: {e}")
        st.stop()

# ── Dashboard ─────────────────────────────────────────────────────────────────
if st.session_state.data:
    data = st.session_state.data
    companies = data.get("companies", [])
    tuu = next((c for c in companies if c.get("domain") == "tuu.cl"), companies[0] if companies else {})
    meta = data.get("_meta", {})

    if meta.get("generado_en"):
        ts = datetime.fromisoformat(meta["generado_en"]).strftime("%-d de %B %Y, %H:%M")
        st.caption(f"Última actualización: {ts}")

    # Métricas
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Empresas", len(companies))
    m2.metric("Comisión TUU", tuu.get("comision_unica") or tuu.get("comision_debito") or "N/D")
    m3.metric("Score precio", f"{tuu.get('score_precio','—')}/10")
    m4.metric("Score funciones", f"{tuu.get('score_funcionalidades','—')}/10")
    m5.metric("Insights", len(data.get("insights", [])))

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Visión general",
        "💰 Precios",
        "⚙️ Funcionalidades",
        "🎯 Insights",
        "📥 Exportar"
    ])

    # TAB 1 ─ Visión general
    with tab1:
        if data.get("resumen_ejecutivo"):
            st.markdown(f'<div class="resumen-box"><strong>Resumen ejecutivo —</strong> {data["resumen_ejecutivo"]}</div>', unsafe_allow_html=True)

        cols = st.columns(len(companies))
        for i, c in enumerate(companies):
            is_tuu = c.get("domain") == "tuu.cl"
            sp = int(c.get("score_precio", 5)) * 10
            sf = int(c.get("score_funcionalidades", 5)) * 10
            info = SITES.get(c.get("domain",""), {})
            with cols[i]:
                st.markdown(f"""
                <div class="company-card {'tuu' if is_tuu else ''}">
                    {'<span class="badge badge-tuu">⭐ Referencia</span>' if is_tuu else ''}
                    <div class="company-name">{info.get('emoji','🏢')} {c.get('name','N/D')}</div>
                    <div class="company-domain">{c.get('domain','')}</div>
                    <div class="company-resumen">{c.get('resumen','')}</div>
                    <div class="company-stat"><span class="stat-label">Dispositivo</span><span class="stat-val">{c.get('precio_dispositivo','N/D')}</span></div>
                    <div class="company-stat"><span class="stat-label">Comisión</span><span class="stat-val">{c.get('comision_unica') or c.get('comision_debito') or 'N/D'}</span></div>
                    <div class="company-stat"><span class="stat-label">Mensualidad</span><span class="stat-val">{c.get('mensualidad','N/D')}</span></div>
                    <div class="company-stat"><span class="stat-label">Abono</span><span class="stat-val">{c.get('plazo_abono','N/D')}</span></div>
                    <div class="score-row">
                        <span style="min-width:42px">Precio</span>
                        <div class="score-bar"><div class="score-fill score-fill-green" style="width:{sp}%"></div></div>
                        <span style="min-width:24px;text-align:right">{c.get('score_precio','?')}/10</span>
                    </div>
                    <div class="score-row">
                        <span style="min-width:42px">Func.</span>
                        <div class="score-bar"><div class="score-fill score-fill-blue" style="width:{sf}%"></div></div>
                        <span style="min-width:24px;text-align:right">{c.get('score_funcionalidades','?')}/10</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # TAB 2 ─ Precios
    with tab2:
        rows = []
        for c in companies:
            rows.append({
                "Empresa": c.get("name","N/D"),
                "Dispositivo": c.get("precio_dispositivo","N/D"),
                "Com. débito": c.get("comision_debito","N/D"),
                "Com. crédito": c.get("comision_credito","N/D"),
                "Com. única": c.get("comision_unica") or "—",
                "Mensualidad": c.get("mensualidad","N/D"),
                "Plazo abono": c.get("plazo_abono","N/D"),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=300)

        st.markdown("#### Ventajas y desventajas")
        vcols = st.columns(len(companies))
        for i, c in enumerate(companies):
            with vcols[i]:
                with st.container(border=True):
                    st.markdown(f"**{c.get('name','')}**")
                    for v in c.get("ventajas", []):
                        st.markdown(f"<span style='color:#1D9E75;font-size:13px'>✅ {v}</span>", unsafe_allow_html=True)
                    for d in c.get("desventajas", []):
                        st.markdown(f"<span style='color:#E24B4A;font-size:13px'>❌ {d}</span>", unsafe_allow_html=True)

    # TAB 3 ─ Funcionalidades
    with tab3:
        features = [
            ("boleta_electronica","Boleta electrónica"),
            ("factura_electronica","Factura electrónica"),
            ("impresora","Impresora integrada"),
            ("cuotas","Pagos en cuotas"),
            ("apple_pay_google_pay","Apple / Google Pay"),
            ("inventario","Gestión de inventario"),
            ("link_pago","Link de pago"),
            ("ecommerce","E-commerce"),
            ("app_movil","App móvil"),
        ]
        fd = {"Funcionalidad": [lbl for _, lbl in features]}
        for c in companies:
            fd[c.get("name", c.get("domain"))] = [b(c.get(k)) for k, _ in features]
        st.dataframe(pd.DataFrame(fd), use_container_width=True, hide_index=True)

        st.markdown("#### Conectividad")
        cd = {"Empresa": [], "Conectividad": []}
        for c in companies:
            cd["Empresa"].append(c.get("name","N/D"))
            cd["Conectividad"].append(", ".join(c.get("conectividad",[])) or "N/D")
        st.dataframe(pd.DataFrame(cd), use_container_width=True, hide_index=True)

    # TAB 4 ─ Insights
    with tab4:
        insights = data.get("insights", [])
        if not insights:
            st.info("No se generaron insights en este análisis.")
        for ins in insights:
            tipo = ins.get("tipo","info")
            icon = {"oportunidad":"🎯","ventaja":"✅","alerta":"⚠️"}.get(tipo,"•")
            st.markdown(f"""
            <div class="insight insight-{tipo}">
                <div class="insight-title">{icon} {ins.get('titulo','')}</div>
                <div class="insight-desc">{ins.get('descripcion','')}</div>
            </div>""", unsafe_allow_html=True)

    # TAB 5 ─ Exportar
    with tab5:
        st.markdown("#### Descargar resultados")
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "📥 JSON completo",
                data=json.dumps(data, ensure_ascii=False, indent=2),
                file_name=f"benchmark_tuu_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json", use_container_width=True
            )
        with c2:
            md = [f"# Benchmark TUU — {datetime.now().strftime('%d/%m/%Y')}\n",
                  f"## Resumen ejecutivo\n\n{data.get('resumen_ejecutivo','')}\n",
                  "## Precios\n",
                  "| Empresa | Dispositivo | Com. débito | Com. crédito | Com. única | Mensualidad | Abono |",
                  "|---|---|---|---|---|---|---|"]
            for c in companies:
                md.append(f"| **{c.get('name')}** | {c.get('precio_dispositivo','N/D')} | {c.get('comision_debito','N/D')} | {c.get('comision_credito','N/D')} | {c.get('comision_unica') or '—'} | {c.get('mensualidad','N/D')} | {c.get('plazo_abono','N/D')} |")
            md.append("\n## Funcionalidades\n")
            md.append("| Funcionalidad | " + " | ".join(c.get("name","?") for c in companies) + " |")
            md.append("|---|" + "---|" * len(companies))
            for key, lbl in features:
                md.append(f"| {lbl} | " + " | ".join(b(c.get(key)) for c in companies) + " |")
            md.append("\n## Insights\n")
            for ins in data.get("insights",[]):
                icon = {"oportunidad":"🎯","ventaja":"✅","alerta":"⚠️"}.get(ins.get("tipo"),"•")
                md.append(f"### {icon} {ins.get('titulo')}\n\n{ins.get('descripcion')}\n")
            st.download_button(
                "📝 Markdown para Notion",
                data="\n".join(md),
                file_name=f"benchmark_tuu_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown", use_container_width=True
            )

        if st.session_state.raw:
            st.markdown("#### Raw data scrapeada")
            for domain, content in st.session_state.raw.items():
                lbl = SITES.get(domain, {}).get("label", domain)
                with st.expander(f"📄 {lbl} ({domain})"):
                    st.text(content[:2000] + ("..." if len(content) > 2000 else ""))

else:
    # Estado vacío
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: #9CA3AF;">
        <div style="font-size:48px; margin-bottom:1rem;">👈</div>
        <div style="font-size:16px; font-weight:600; color:#374151; margin-bottom:8px;">Configurá el benchmark</div>
        <div style="font-size:14px;">Ingresá tus API keys y seleccioná los competidores en el panel izquierdo</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ ¿Cómo funciona?"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**1. Scraping**\n\nFirecrawl extrae el contenido de cada sitio web en formato limpio, incluyendo páginas de precios y funcionalidades.")
        with c2:
            st.markdown("**2. Análisis con IA**\n\nClaude Opus 4.6 procesa el contenido y extrae datos estructurados: comisiones, precios, funcionalidades y genera insights estratégicos.")
        with c3:
            st.markdown("**3. Dashboard**\n\nVizualizás las comparativas en tablas interactivas y exportás todo en JSON o Markdown para compartir con tu equipo.")

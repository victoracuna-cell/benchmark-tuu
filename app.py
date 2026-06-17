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
    .tuu-highlight { background: #E6F1FB; border-left: 4px solid #378ADD; padding: 0.5rem 1rem; border-radius: 0 8px 8px 0; }
    .insight-card { padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; }
    .insight-oportunidad { background: #E1F5EE; border-left: 4px solid #1D9E75; }
    .insight-ventaja { background: #E6F1FB; border-left: 4px solid #378ADD; }
    .insight-alerta { background: #FAEEDA; border-left: 4px solid #BA7517; }
    .metric-label { font-size: 12px; color: #666; margin-bottom: 4px; }
    [data-testid="stSidebar"] { background: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

SITES = {
    "tuu.cl": {
        "urls": ["https://tuu.cl", "https://tuu.cl/precios"],
        "label": "TUU",
        "emoji": "⭐"
    },
    "transbank.cl": {
        "urls": ["https://www.transbank.cl/pos"],
        "label": "Transbank",
        "emoji": "🏦"
    },
    "mercadopago.cl": {
        "urls": ["https://www.mercadopago.cl/point"],
        "label": "Mercado Pago",
        "emoji": "💛"
    },
    "sumup.cl": {
        "urls": ["https://www.sumup.com/es-cl/"],
        "label": "SumUp",
        "emoji": "🔵"
    },
    "compraqui.cl": {
        "urls": ["https://www.compraqui.cl"],
        "label": "Compraquí",
        "emoji": "🟢"
    },
    "getnet.cl": {
        "urls": ["https://www.getnet.cl"],
        "label": "Getnet",
        "emoji": "🟠"
    },
    "redelcom.cl": {
        "urls": ["https://www.redelcom.cl"],
        "label": "Redelcom",
        "emoji": "🔴"
    },
}

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
      "ventajas": ["ventaja 1"],
      "desventajas": ["desventaja 1"],
      "resumen": "2 frases propuesta de valor"
    }
  ],
  "insights": [
    {
      "tipo": "oportunidad|ventaja|alerta",
      "titulo": "título",
      "descripcion": "2-3 frases con datos"
    }
  ],
  "resumen_ejecutivo": "Párrafo de 4-5 frases con conclusiones"
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
    blocks = []
    for domain, content in scraped_data.items():
        label = SITES.get(domain, {}).get("label", domain)
        blocks.append(f"{'='*50}\n{label} ({domain})\n{'='*50}\n{content}")

    user_msg = f"""Analiza estos datos de sitios POS/pagos en Chile. TUU es la referencia.

{''.join(blocks)}

Extrae precios, comisiones, funcionalidades. Usa 'N/D' si no encontrás un dato."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4000,
        system=ANALYSIS_PROMPT,
        messages=[{"role": "user", "content": user_msg}]
    )
    text = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def bool_to_emoji(val):
    if val is True:
        return "✅"
    if val is False:
        return "❌"
    return "❓"


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://tuu.cl/favicon.ico", width=32)
    st.title("Benchmark POS Chile")
    st.caption("Powered by Firecrawl + Claude")
    st.divider()

    st.subheader("🔑 API Keys")
    fc_key = st.text_input("Firecrawl API Key", type="password", placeholder="fc-...")
    anthropic_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")

    st.divider()
    st.subheader("🏢 Competidores")
    st.caption("TUU siempre se incluye como referencia")

    selected_domains = ["tuu.cl"]
    for domain, info in SITES.items():
        if domain == "tuu.cl":
            continue
        if st.checkbox(f"{info['emoji']} {info['label']}", value=domain in ["transbank.cl", "mercadopago.cl", "sumup.cl", "compraqui.cl"]):
            selected_domains.append(domain)

    custom_url = st.text_input("➕ URL personalizada", placeholder="https://...")

    st.divider()
    run = st.button("🚀 Iniciar benchmark", type="primary", use_container_width=True, disabled=not (fc_key and anthropic_key))
    if not fc_key or not anthropic_key:
        st.caption("⚠️ Ingresá ambas API keys para continuar")

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("📊 Benchmark competitivo TUU")
st.caption(f"Análisis de precios, funcionalidades y planes del mercado POS en Chile")

if "benchmark_data" not in st.session_state:
    st.session_state.benchmark_data = None
if "scraped_raw" not in st.session_state:
    st.session_state.scraped_raw = None

if run:
    if not fc_key.startswith("fc-"):
        st.error("API key de Firecrawl inválida (debe comenzar con fc-)")
        st.stop()

    domains_to_scrape = selected_domains.copy()
    if custom_url:
        clean = custom_url.replace("https://", "").replace("http://", "").rstrip("/")
        SITES[clean] = {"urls": [custom_url], "label": clean, "emoji": "🌐"}
        domains_to_scrape.append(clean)

    fc_app = FirecrawlApp(api_key=fc_key)
    scraped = {}

    st.info(f"Analizando {len(domains_to_scrape)} sitios... esto puede tomar 1-2 minutos.")
    progress = st.progress(0, text="Iniciando scraping...")
    log_area = st.empty()
    logs = []

    for i, domain in enumerate(domains_to_scrape):
        info = SITES.get(domain, {"urls": [f"https://{domain}"], "label": domain})
        pct = int((i / len(domains_to_scrape)) * 80)
        progress.progress(pct, text=f"Scrapeando {info['label']}...")
        logs.append(f"⏳ Scrapeando {info['label']} ({domain})...")
        log_area.code("\n".join(logs))

        try:
            content = scrape_site(fc_app, info["urls"])
            scraped[domain] = content
            logs[-1] = f"✅ {info['label']} — {len(content):,} caracteres"
        except Exception as e:
            scraped[domain] = f"Error: {str(e)}"
            logs[-1] = f"❌ {info['label']} — {str(e)}"

        log_area.code("\n".join(logs))
        time.sleep(0.3)

    progress.progress(85, text="Analizando con Claude Opus 4.6...")
    logs.append("🤖 Enviando a Claude para análisis...")
    log_area.code("\n".join(logs))

    try:
        data = analyze_with_claude(anthropic_key, scraped)
        data["_meta"] = {
            "generado_en": datetime.now().isoformat(),
            "sitios": domains_to_scrape
        }
        st.session_state.benchmark_data = data
        st.session_state.scraped_raw = scraped
        logs.append(f"✅ Análisis completo — {len(data.get('companies', []))} empresas procesadas")
        log_area.code("\n".join(logs))
        progress.progress(100, text="¡Listo!")
        time.sleep(0.5)
        st.rerun()
    except Exception as e:
        st.error(f"Error en análisis con Claude: {e}")
        st.stop()

# ── Dashboard ─────────────────────────────────────────────────────────────────
if st.session_state.benchmark_data:
    data = st.session_state.benchmark_data
    companies = data.get("companies", [])
    tuu = next((c for c in companies if c.get("domain") == "tuu.cl"), companies[0] if companies else {})

    meta = data.get("_meta", {})
    if meta.get("generado_en"):
        st.caption(f"Análisis generado el {datetime.fromisoformat(meta['generado_en']).strftime('%d/%m/%Y a las %H:%M')}")

    # Métricas resumen
    cols = st.columns(5)
    cols[0].metric("Empresas analizadas", len(companies))
    cols[1].metric("Comisión TUU", tuu.get("comision_unica") or tuu.get("comision_debito") or "N/D")
    cols[2].metric("Score precio TUU", f"{tuu.get('score_precio', 'N/D')}/10")
    cols[3].metric("Score funciones TUU", f"{tuu.get('score_funcionalidades', 'N/D')}/10")
    cols[4].metric("Insights generados", len(data.get("insights", [])))

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Visión general",
        "💰 Precios y comisiones",
        "⚙️ Funcionalidades",
        "🎯 Insights",
        "📥 Exportar"
    ])

    # Tab 1: Visión general
    with tab1:
        if data.get("resumen_ejecutivo"):
            st.markdown(f"""<div class="tuu-highlight"><strong>Resumen ejecutivo</strong><br>{data['resumen_ejecutivo']}</div>""", unsafe_allow_html=True)
            st.markdown("")

        cols = st.columns(len(companies))
        for i, company in enumerate(companies):
            is_tuu = company.get("domain") == "tuu.cl"
            with cols[i]:
                with st.container(border=True):
                    info = SITES.get(company.get("domain", ""), {})
                    emoji = info.get("emoji", "🏢")
                    st.markdown(f"### {emoji} {company.get('name', 'N/D')}")
                    if is_tuu:
                        st.badge("Referencia", color="blue")
                    st.caption(company.get("domain", ""))
                    st.caption(company.get("resumen", ""))
                    st.markdown(f"**Precio dispositivo:** {company.get('precio_dispositivo', 'N/D')}")
                    st.markdown(f"**Comisión:** {company.get('comision_unica') or company.get('comision_debito') or 'N/D'}")
                    st.markdown(f"**Abono:** {company.get('plazo_abono', 'N/D')}")
                    st.progress(int(company.get("score_precio", 5)) / 10, text=f"Precio: {company.get('score_precio','?')}/10")
                    st.progress(int(company.get("score_funcionalidades", 5)) / 10, text=f"Funciones: {company.get('score_funcionalidades','?')}/10")

    # Tab 2: Precios
    with tab2:
        price_data = []
        for c in companies:
            price_data.append({
                "Empresa": c.get("name", "N/D"),
                "Dispositivo": c.get("precio_dispositivo", "N/D"),
                "Com. débito": c.get("comision_debito", "N/D"),
                "Com. crédito": c.get("comision_credito", "N/D"),
                "Com. única": c.get("comision_unica") or "—",
                "Mensualidad": c.get("mensualidad", "N/D"),
                "Plazo abono": c.get("plazo_abono", "N/D"),
            })
        df = pd.DataFrame(price_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Ventajas y desventajas")
        cols = st.columns(len(companies))
        for i, c in enumerate(companies):
            with cols[i]:
                st.markdown(f"**{c.get('name')}**")
                for v in c.get("ventajas", []):
                    st.markdown(f"✅ {v}")
                for d in c.get("desventajas", []):
                    st.markdown(f"❌ {d}")

    # Tab 3: Funcionalidades
    with tab3:
        features = [
            ("boleta_electronica", "Boleta electrónica"),
            ("factura_electronica", "Factura electrónica"),
            ("impresora", "Impresora integrada"),
            ("cuotas", "Pagos en cuotas"),
            ("apple_pay_google_pay", "Apple/Google Pay"),
            ("inventario", "Gestión de inventario"),
            ("link_pago", "Link de pago"),
            ("ecommerce", "E-commerce"),
            ("app_movil", "App móvil"),
        ]

        func_data = {"Funcionalidad": [label for _, label in features]}
        for c in companies:
            func_data[c.get("name", c.get("domain"))] = [
                bool_to_emoji(c.get(key)) for key, _ in features
            ]

        df_func = pd.DataFrame(func_data)
        st.dataframe(df_func, use_container_width=True, hide_index=True)

        st.subheader("Conectividad")
        conn_data = {"Empresa": [], "Conectividad": []}
        for c in companies:
            conn_data["Empresa"].append(c.get("name", "N/D"))
            conn_data["Conectividad"].append(", ".join(c.get("conectividad", [])) or "N/D")
        st.dataframe(pd.DataFrame(conn_data), use_container_width=True, hide_index=True)

    # Tab 4: Insights
    with tab4:
        insights = data.get("insights", [])
        if not insights:
            st.info("No se generaron insights.")
        for ins in insights:
            tipo = ins.get("tipo", "info")
            icon = {"oportunidad": "🎯", "ventaja": "✅", "alerta": "⚠️"}.get(tipo, "•")
            css_class = f"insight-{tipo}"
            st.markdown(
                f"""<div class="insight-card {css_class}">
                    <strong>{icon} {ins.get('titulo')}</strong><br>
                    {ins.get('descripcion')}
                </div>""",
                unsafe_allow_html=True
            )

    # Tab 5: Exportar
    with tab5:
        st.subheader("Exportar resultados")

        col1, col2 = st.columns(2)

        with col1:
            json_export = json.dumps(data, ensure_ascii=False, indent=2)
            st.download_button(
                "📥 Descargar JSON completo",
                data=json_export,
                file_name=f"benchmark_tuu_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

        with col2:
            # Generar Markdown
            md_lines = [
                f"# Benchmark competitivo TUU — {datetime.now().strftime('%d/%m/%Y')}\n",
                f"**Generado con:** Firecrawl + Claude Opus 4.6\n",
                f"## Resumen ejecutivo\n\n{data.get('resumen_ejecutivo', 'N/D')}\n",
                "## Precios y comisiones\n",
                "| Empresa | Dispositivo | Com. débito | Com. crédito | Com. única | Mensualidad | Abono |",
                "|---------|-------------|-------------|--------------|------------|-------------|-------|",
            ]
            for c in companies:
                md_lines.append(
                    f"| **{c.get('name')}** | {c.get('precio_dispositivo','N/D')} | "
                    f"{c.get('comision_debito','N/D')} | {c.get('comision_credito','N/D')} | "
                    f"{c.get('comision_unica') or '—'} | {c.get('mensualidad','N/D')} | {c.get('plazo_abono','N/D')} |"
                )
            md_lines.append("\n## Funcionalidades\n")
            headers = "| Funcionalidad | " + " | ".join(c.get("name","?") for c in companies) + " |"
            sep = "|---|" + "---|" * len(companies)
            md_lines.extend([headers, sep])
            for key, label in features:
                row = f"| {label} | " + " | ".join(bool_to_emoji(c.get(key)) for c in companies) + " |"
                md_lines.append(row)
            md_lines.append("\n## Insights\n")
            for ins in data.get("insights", []):
                icon = {"oportunidad": "🎯", "ventaja": "✅", "alerta": "⚠️"}.get(ins.get("tipo"), "•")
                md_lines.append(f"### {icon} {ins.get('titulo')}\n\n{ins.get('descripcion')}\n")

            st.download_button(
                "📝 Descargar Markdown",
                data="\n".join(md_lines),
                file_name=f"benchmark_tuu_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.divider()
        st.subheader("Raw data scrapeada")
        if st.session_state.scraped_raw:
            for domain, content in st.session_state.scraped_raw.items():
                with st.expander(f"📄 {SITES.get(domain, {}).get('label', domain)} ({domain})"):
                    st.text(content[:2000] + ("..." if len(content) > 2000 else ""))

else:
    st.info("👈 Configurá las API keys y seleccioná los competidores en el panel izquierdo para comenzar.")
    with st.expander("ℹ️ ¿Cómo funciona?"):
        st.markdown("""
        1. **Firecrawl** scrapeea los sitios web de TUU y sus competidores, extrayendo el contenido en formato limpio
        2. **Claude Opus 4.6** analiza todo el contenido y extrae datos estructurados: precios, comisiones, funcionalidades
        3. El dashboard muestra comparativas interactivas que podés exportar en JSON o Markdown

        **Sitios analizados:** TUU, Transbank, Mercado Pago, SumUp, Compraquí, Getnet, Redelcom

        **Necesitás:**
        - API key de [Firecrawl](https://firecrawl.dev) (fc-...)
        - API key de [Anthropic](https://console.anthropic.com) (sk-ant-...)
        """)

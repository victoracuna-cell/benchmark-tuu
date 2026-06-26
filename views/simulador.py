import streamlit as st
import plotly.graph_objects as go
from utils.scoring import COMPETITOR_ORDER, COMPETITOR_COLORS

PERFILES = {
    "PyME (~$1M/mes, ticket ~$5.000)":       {"ventas_mes": 1_000_000, "ticket": 5_000},
    "Mediano ($5M/mes, ticket ~$12.000)":      {"ventas_mes": 5_000_000, "ticket": 12_000},
    "Gran comercio ($20M/mes, ticket ~$25k)": {"ventas_mes": 20_000_000, "ticket": 25_000},
}

def render(data: dict):
    competitors = data.get("competitors", {})
    ordered = [c for c in COMPETITOR_ORDER if c in competitors]

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Simulador de costo total anual**")
    st.caption("Incluye comisiones, mensualidades, documentos tributarios y hardware amortizado a 3 años.")

    col1, col2, col3 = st.columns(3)
    with col1:
        perfil_key = st.selectbox("Perfil", list(PERFILES.keys()))
    perfil = PERFILES[perfil_key]
    with col2:
        ventas_mes = st.number_input("Ventas mensuales ($)", value=perfil["ventas_mes"], step=500_000, format="%d")
    with col3:
        pct_credito = st.slider("% pagos con crédito", 0, 100, 40)
    st.markdown('</div>', unsafe_allow_html=True)

    pct_debito = 100 - pct_credito
    ventas_debito = ventas_mes * pct_debito / 100
    ventas_credito = ventas_mes * pct_credito / 100
    ventas_anual = ventas_mes * 12

    results = []
    for comp in ordered:
        info = competitors[comp]
        com = info.get("comisiones", {})
        docs = info.get("documentos", {})
        hw = info.get("hardware", {})
        debito_pct = com.get("debito_pct") or 0
        credito_pct = com.get("credito_pct") or 0
        cargo_fijo = com.get("cargo_fijo") or 0
        mens_red = _parse(com.get("mensualidad_red")) or 0
        txs_mes = ventas_mes / max(perfil["ticket"], 1)
        comision_mes = (ventas_debito * debito_pct / 100) + (ventas_credito * credito_pct / 100) + (cargo_fijo * txs_mes)
        comision_anual = comision_mes * 12
        docs_anual = ((_parse(docs.get("costo_boleta_mes")) or 0) + (_parse(docs.get("costo_factura_mes")) or 0)) * 12
        mens_anual = mens_red * 12
        hw_val = _parse(hw.get("precio_oferta_clp")) or _parse(hw.get("precio_lista_clp")) or 0
        hw_am = hw_val / 3
        total = comision_anual + docs_anual + mens_anual + hw_am
        results.append({"comp": comp, "name": info.get("name", comp),
                        "comision_anual": comision_anual, "docs_anual": docs_anual,
                        "mens_anual": mens_anual, "hw_am": hw_am, "total": total,
                        "pct": total / ventas_anual * 100 if ventas_anual else 0})
    results.sort(key=lambda r: r["total"])

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    fig = go.Figure()
    cats = [("Comisiones", "comision_anual", "#1E3A5F"),
            ("Documentos", "docs_anual", "#3B82F6"),
            ("Mensualidades", "mens_anual", "#EF4444"),
            ("Hardware (3 años)", "hw_am", "#8B5CF6")]
    for cat, key, color in cats:
        fig.add_trace(go.Bar(
            name=cat, x=[r["name"] for r in results], y=[r[key] for r in results],
            marker_color=color, marker_line_width=0,
        ))
    fig.update_layout(
        barmode="stack", height=340,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", color="#1E3A5F"),
        yaxis=dict(title="$ CLP anuales", gridcolor="rgba(30,58,95,0.07)"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(size=12)),
        margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    cols = st.columns(len(results))
    tuu_total = next((r["total"] for r in results if r["comp"] == "tuu"), None)
    for i, r in enumerate(results):
        delta = None
        if r["comp"] != "tuu" and tuu_total:
            diff = r["total"] - tuu_total
            delta = f"{'+'  if diff > 0 else ''}{diff:,.0f} vs TUU"
        cols[i].metric(r["name"], f"${r['total']:,.0f}", f"{r['pct']:.2f}% ventas", delta_color="off")
        if delta:
            cols[i].caption(delta)

    st.caption("Estimación. Hardware amortizado 3 años. No incluye IVA sobre comisiones.")

def _parse(val):
    if val is None: return None
    if isinstance(val, (int, float)): return float(val)
    s = str(val).replace("$","").replace(".","").replace(",","").strip()
    try: return float(s)
    except: return None

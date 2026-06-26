import streamlit as st
import plotly.graph_objects as go
from utils.scoring import COMPETITOR_ORDER, COMPETITOR_COLORS

TUU_BLUE = "#0128c9"
TUU_CYAN = "#affffd"
GRAY = "#d8d8d8"

def _bar_chart(data, competitors, ordered, field, title):
    names, vals, colors = [], [], []
    for c in ordered:
        v = competitors[c].get("comisiones", {}).get(field)
        if v is not None:
            names.append(competitors[c].get("name", c))
            vals.append(v)
            colors.append(TUU_BLUE if c == "tuu" else GRAY)
    if not vals:
        st.caption("Sin datos.")
        return
    fig = go.Figure(go.Bar(
        x=names, y=vals, marker_color=colors, marker_line_width=0,
        text=[f"{v:.2f}%" for v in vals], textposition="outside",
        textfont=dict(size=11, color="#555"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(title=None, range=[0, max(vals)*1.35], gridcolor="#f5f5f5",
                   tickfont=dict(size=10, color="#bbb"), ticksuffix="%"),
        xaxis=dict(tickfont=dict(size=11, color="#555"), tickangle=0),
        height=240, margin=dict(t=10, b=10, l=10, r=10),
        font=dict(family="Inter, sans-serif"),
        bargap=0.45,
    )
    st.plotly_chart(fig, use_container_width=True)

def render(data: dict):
    competitors = data.get("competitors", {})
    ordered = [c for c in COMPETITOR_ORDER if c in competitors]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Comisión por transacción · sin IVA · tarifa base nuevos comercios</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<p style="font-size:11px;font-weight:600;color:#333;margin-bottom:8px;">Débito nacional</p>', unsafe_allow_html=True)
        _bar_chart(data, competitors, ordered, "debito_pct", "Débito")
    with col2:
        st.markdown('<p style="font-size:11px;font-weight:600;color:#333;margin-bottom:8px;">Crédito nacional</p>', unsafe_allow_html=True)
        _bar_chart(data, competitors, ordered, "credito_pct", "Crédito")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Tabla completa</div>', unsafe_allow_html=True)
    rows = []
    fields = {
        "Débito %": "debito_pct", "Crédito %": "credito_pct",
        "Prepago %": "prepago_pct", "Internacional %": "internacional_pct",
        "Cargo fijo/tx": "cargo_fijo", "Mensualidad red": "mensualidad_red",
        "Notas": "notas_comisiones",
    }
    for comp in ordered:
        info = competitors[comp]
        com = info.get("comisiones", {})
        row = {"Empresa": info.get("name", comp)}
        for label, key in fields.items():
            v = com.get(key)
            row[label] = f"{v:.2f}%" if isinstance(v, float) else (str(v) if v else "—")
        rows.append(row)
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.caption("Fuente: sitios oficiales scrapeados vía Tavily · junio 2026")
    st.markdown('</div>', unsafe_allow_html=True)

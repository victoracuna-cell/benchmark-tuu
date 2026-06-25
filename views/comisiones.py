import streamlit as st
import plotly.graph_objects as go
from utils.scoring import COMPETITOR_ORDER, COMPETITOR_COLORS

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="sans-serif", color="#1E3A5F"),
    margin=dict(t=10, b=10, l=10, r=10),
)

def _bar(names, vals, colors, ymax):
    fig = go.Figure(go.Bar(
        x=names, y=vals, marker_color=colors,
        text=[f"{v:.2f}%" for v in vals], textposition="outside",
        marker_line_width=0,
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        yaxis=dict(title="%", range=[0, ymax * 1.35], gridcolor="rgba(30,58,95,0.07)", tickfont=dict(size=11)),
        xaxis=dict(tickfont=dict(size=12)),
        height=280,
        bargap=0.4,
    )
    return fig

def render(data: dict):
    competitors = data.get("competitors", {})
    ordered = [c for c in COMPETITOR_ORDER if c in competitors]

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Comisiones por transacción** · Sin IVA · Tarifa base para nuevos comercios")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Débito nacional")
        names, vals, colors = [], [], []
        for c in ordered:
            v = competitors[c].get("comisiones", {}).get("debito_pct")
            if v:
                names.append(competitors[c].get("name", c))
                vals.append(v); colors.append(COMPETITOR_COLORS.get(c, "#888"))
        if vals:
            st.plotly_chart(_bar(names, vals, colors, max(vals)), use_container_width=True)

    with col2:
        st.markdown("##### Crédito nacional")
        names, vals, colors = [], [], []
        for c in ordered:
            v = competitors[c].get("comisiones", {}).get("credito_pct")
            if v:
                names.append(competitors[c].get("name", c))
                vals.append(v); colors.append(COMPETITOR_COLORS.get(c, "#888"))
        if vals:
            st.plotly_chart(_bar(names, vals, colors, max(vals)), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Tabla completa de comisiones**")
    rows = []
    fields = {"Débito %": "debito_pct", "Crédito %": "credito_pct", "Prepago %": "prepago_pct",
              "Internacional %": "internacional_pct", "Cargo fijo/tx": "cargo_fijo",
              "Mensualidad red": "mensualidad_red", "Notas": "notas_comisiones"}
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

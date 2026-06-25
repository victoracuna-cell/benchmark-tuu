import streamlit as st
import plotly.graph_objects as go
from utils.scoring import DIMENSIONS, DIM_LABELS, COMPETITOR_ORDER, COMPETITOR_COLORS, weighted_total, get_all_scores, score_color

def render(data: dict):
    competitors = data.get("competitors", {})
    if not competitors:
        st.info("Sin datos. Ve a **Actualizar datos** para comenzar.")
        return

    all_scores = get_all_scores(data)
    ordered = [c for c in COMPETITOR_ORDER if c in competitors]
    totals = {c: weighted_total(all_scores.get(c, {})) for c in ordered}
    sorted_comp = sorted(ordered, key=lambda c: totals[c], reverse=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Ranking general** — score ponderado sobre 5")
    cols = st.columns(len(sorted_comp))
    for i, comp in enumerate(sorted_comp):
        info = competitors[comp]
        total = totals[comp]
        tuu_total = totals.get("tuu", 0)
        delta = f"{round(total - tuu_total, 2):+.2f} vs TUU" if comp != "tuu" else "Referencia"
        cols[i].metric(info.get("name", comp), f"{total:.1f} / 5", delta, delta_color="inverse" if comp != "tuu" else "off")
    st.markdown('</div>', unsafe_allow_html=True)

    col_radar, col_table = st.columns([3, 2])

    with col_radar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**Radar comparativo**")
        dim_labels = [DIM_LABELS[d].split(" ", 1)[1] for d in DIMENSIONS]
        fig = go.Figure()
        for comp in ordered:
            scores = all_scores.get(comp, {})
            values = [scores.get(d, 0) for d in DIMENSIONS]
            values_c = values + [values[0]]
            labels_c = dim_labels + [dim_labels[0]]
            info = competitors[comp]
            fig.add_trace(go.Scatterpolar(
                r=values_c, theta=labels_c, fill="toself",
                name=info.get("name", comp),
                line_color=COMPETITOR_COLORS.get(comp, "#888"),
                opacity=0.75 if comp != "tuu" else 1.0,
                line_width=3 if comp == "tuu" else 1.5,
            ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], gridcolor="rgba(30,58,95,0.08)", tickfont=dict(size=10, color="#8292b0")),
                angularaxis=dict(gridcolor="rgba(30,58,95,0.08)"),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            height=400,
            margin=dict(t=20, b=60, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5, font=dict(size=12)),
            font=dict(family="sans-serif", color="#1E3A5F"),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_table:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**Score por dimensión**")
        rows = []
        for dim in DIMENSIONS:
            row = {"Dimensión": DIM_LABELS[dim]}
            for comp in ordered:
                s = all_scores.get(comp, {}).get(dim)
                info = competitors[comp]
                row[info.get("name", comp)] = f"{score_color(s)} {s:.1f}" if s is not None else "—"
            rows.append(row)
        st.dataframe(rows, use_container_width=True, hide_index=True, height=300)
        st.markdown('</div>', unsafe_allow_html=True)

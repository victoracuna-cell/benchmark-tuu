import streamlit as st
import plotly.graph_objects as go
from utils.scoring import DIMENSIONS, DIM_LABELS, COMPETITOR_ORDER, COMPETITOR_COLORS, weighted_total, get_all_scores, score_color

def render(data: dict):
    competitors = data.get("competitors", {})
    if not competitors:
        st.info("Sin datos. Ve a Actualizar datos para comenzar.")
        return

    all_scores = get_all_scores(data)
    ordered = [c for c in COMPETITOR_ORDER if c in competitors]
    totals = {c: weighted_total(all_scores.get(c, {})) for c in ordered}
    sorted_comp = sorted(ordered, key=lambda c: totals[c], reverse=True)

    col_radar, col_rank = st.columns([3, 2], gap="medium")

    with col_radar:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">Radar comparativo</div>', unsafe_allow_html=True)
        dim_labels = [DIM_LABELS[d].split(" ", 1)[-1] for d in DIMENSIONS]
        fig = go.Figure()
        for comp in ordered:
            scores = all_scores.get(comp, {})
            values = [float(scores.get(d) or 0) for d in DIMENSIONS]
            values_c = values + [values[0]]
            labels_c = dim_labels + [dim_labels[0]]
            info = competitors[comp]
            is_tuu = comp == "tuu"
            fig.add_trace(go.Scatterpolar(
                r=values_c, theta=labels_c, fill="toself",
                name=info.get("name", comp),
                line_color=COMPETITOR_COLORS.get(comp, "#ccc"),
                opacity=1.0 if is_tuu else 0.4,
                line_width=2.5 if is_tuu else 1,
                fillcolor="rgba(1,40,201,0.08)" if is_tuu else "rgba(0,0,0,0.02)",
            ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], gridcolor="#f0f0f0",
                                tickfont=dict(size=9, color="#bbb"), tickvals=[1,2,3,4,5]),
                angularaxis=dict(gridcolor="#f0f0f0", tickfont=dict(size=10, color="#555")),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True, height=380,
            margin=dict(t=10, b=50, l=30, r=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5,
                       font=dict(size=11, color="#555")),
            font=dict(family="Inter, -apple-system, sans-serif"),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_rank:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">Ranking general</div>', unsafe_allow_html=True)
        for i, comp in enumerate(sorted_comp):
            info = competitors[comp]
            total = totals[comp]
            is_tuu = comp == "tuu"
            name = info.get("name", comp)
            if is_tuu:
                st.markdown(
                    '<div style="display:flex;align-items:center;gap:10px;padding:9px 10px;'
                    'background:#f5f7ff;border:1px solid rgba(1,40,201,0.12);border-radius:8px;margin-bottom:4px;">'
                    f'<span style="font-size:11px;font-weight:700;color:#0128c9;width:16px;">{i+1}</span>'
                    f'<span style="font-size:13px;font-weight:600;color:#0128c9;flex:1;">{name}</span>'
                    '<span style="font-size:9px;background:#affffd;color:#0128c9;font-weight:700;'
                    'padding:2px 7px;border-radius:99px;margin-right:4px;">l\u00edder</span>'
                    f'<span style="font-size:13px;font-weight:700;color:#0128c9;">{total:.1f}</span>'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div style="display:flex;align-items:center;gap:10px;padding:9px 10px;'
                    'border-bottom:1px solid #f5f5f5;">'
                    f'<span style="font-size:11px;color:#bbb;width:16px;font-weight:600;">{i+1}</span>'
                    f'<span style="font-size:12px;color:#555;flex:1;">{name}</span>'
                    f'<span style="font-size:12px;color:#555;font-weight:500;">{total:.1f}</span>'
                    '</div>',
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:0.75rem;">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">Score TUU por dimensi\u00f3n</div>', unsafe_allow_html=True)
        tuu_scores = all_scores.get("tuu", {})

        DIM_ICONS = {
            "comisiones": "fi-rr-percentage",
            "hardware":   "fi-rr-mobile",
            "documentos": "fi-rr-document",
            "abono":      "fi-rr-time-fast",
            "gestion":    "fi-rr-dashboard",
            "soporte":    "fi-rr-headset",
            "financieros":"fi-rr-credit-card",
        }

        for dim in DIMENSIONS:
            s = tuu_scores.get(dim, 0) or 0
            filled = int(round(s))
            dots = ""
            for d in range(5):
                if d < filled - 1:
                    dots += '<div style="width:18px;height:4px;border-radius:99px;background:#0128c9;"></div>'
                elif d == filled - 1:
                    dots += '<div style="width:18px;height:4px;border-radius:99px;background:#affffd;border:1px solid #0128c9;"></div>'
                else:
                    dots += '<div style="width:18px;height:4px;border-radius:99px;background:#f0f0f0;"></div>'
            label = DIM_LABELS[dim].split(" ", 1)[-1]
            icon = DIM_ICONS.get(dim, "fi-rr-apps")
            st.markdown(
                '<div class="stat-icon-row">'
                f'<div class="stat-icon-box"><i class="fi {icon}"></i></div>'
                f'<span class="stat-label">{label}</span>'
                f'<div style="display:flex;gap:3px;">{dots}</div>'
                f'<span class="stat-value" style="margin-left:8px;">{s:.1f}</span>'
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

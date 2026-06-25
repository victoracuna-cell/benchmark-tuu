import streamlit as st
from utils.scoring import COMPETITOR_ORDER

def _render_table(data, section_key, fields):
    competitors = data.get("competitors", {})
    ordered = [c for c in COMPETITOR_ORDER if c in competitors]
    rows = []
    for comp in ordered:
        info = competitors[comp]
        section = info.get(section_key, {})
        row = {"Empresa": info.get("name", comp)}
        for label, key in fields.items():
            v = section.get(key)
            row[label] = str(v) if v is not None else "—"
        rows.append(row)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.caption("Fuente: sitios oficiales scrapeados vía Tavily.")
    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from utils.styles import GLOBAL_CSS
import json
import csv
import io
from utils.github_storage import load_data
from utils.ui import render_sidebar
from utils.scoring import COMPETITOR_ORDER, DIMENSIONS, DIM_LABELS

st.set_page_config(page_title="Exportar · Benchmark TUU", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
from utils.auth import require_admin
require_admin()

render_sidebar()

st.title("📥 Exportar datos")

data = load_data()
competitors = data.get("competitors", {})

if not competitors:
    st.info("Sin datos para exportar.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### JSON completo")
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    st.download_button(
        "⬇️ Descargar benchmark.json",
        data=json_str,
        file_name="benchmark_tuu.json",
        mime="application/json",
    )

with col2:
    st.markdown("#### CSV — scores por dimensión")
    ordered = [c for c in COMPETITOR_ORDER if c in competitors]
    output = io.StringIO()
    writer = csv.writer(output)
    header = ["Empresa"] + [DIM_LABELS[d] for d in DIMENSIONS] + ["Total"]
    writer.writerow(header)
    for comp in ordered:
        info = competitors[comp]
        scores = info.get("scores", {})
        vals = [scores.get(d, "") for d in DIMENSIONS]
        total = round(sum(v for v in vals if isinstance(v, (int, float))) / max(len([v for v in vals if isinstance(v, (int, float))]), 1), 2)
        writer.writerow([info.get("name", comp)] + vals + [total])
    st.download_button(
        "⬇️ Descargar scores.csv",
        data=output.getvalue(),
        file_name="benchmark_scores.csv",
        mime="text/csv",
    )

st.divider()
st.markdown("#### Vista previa del JSON guardado")
st.json(data)

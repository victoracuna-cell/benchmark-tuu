import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.github_storage import load_data, save_data
from utils.ui import render_sidebar
from utils.tavily_scraper import COMPETITOR_SEEDS
import json

st.set_page_config(page_title="Editar datos · Benchmark TUU", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
from utils.auth import require_admin
require_admin()

render_sidebar()

st.title("✏️ Editar datos manualmente")
st.caption("Corrige o completa datos que el scraping no pudo extraer.")

data = load_data()
competitors = data.get("competitors", {})

comp_key = st.selectbox(
    "Competidor",
    options=list(COMPETITOR_SEEDS.keys()),
    format_func=lambda k: COMPETITOR_SEEDS[k]["name"],
)

current = competitors.get(comp_key, {})

st.markdown(f"#### Editando: {COMPETITOR_SEEDS[comp_key]['name']}")
st.caption("Edita el JSON directamente. Guarda cuando termines.")

edited_str = st.text_area(
    "Datos JSON",
    value=json.dumps(current, ensure_ascii=False, indent=2),
    height=600,
)

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("💾 Guardar cambios", type="primary"):
        try:
            edited = json.loads(edited_str)
            if "competitors" not in data:
                data["competitors"] = {}
            data["competitors"][comp_key] = edited
            if save_data(data, f"fix: manual edit — {comp_key}"):
                st.success("Guardado en GitHub.")
            else:
                st.error("Error guardando.")
        except json.JSONDecodeError as e:
            st.error(f"JSON inválido: {e}")
with col2:
    if st.button("🗑️ Borrar este competidor"):
        if comp_key in data.get("competitors", {}):
            del data["competitors"][comp_key]
            if save_data(data, f"chore: remove {comp_key}"):
                st.success(f"{comp_key} eliminado.")
            else:
                st.error("Error guardando.")

st.divider()
st.markdown("##### Referencia de estructura esperada")
st.json({
    "name": "Nombre empresa",
    "comisiones": {"debito_pct": 1.49, "credito_pct": 1.49, "notas_comisiones": ""},
    "hardware": {"modelo_principal": "", "precio_oferta_clp": None, "modalidad": "compra"},
    "documentos": {"boleta": "incluida", "costo_boleta_mes": None, "factura": "incluida"},
    "abono": {"plazo_estandar": "1 día hábil", "abono_inmediato": "sí"},
    "gestion": {"pos": "sí", "catalogo": "sí", "inventario": "sí", "agenda": "sí"},
    "soporte": {"canales": "", "horario": "", "garantia": ""},
    "financieros": {"adelanto": "sí", "credito": "no", "cuotas_sin_interes": "sí"},
    "scores": {"comisiones": 4.5, "hardware": 4.0, "documentos": 5.0, "abono": 4.0, "gestion": 5.0, "soporte": 3.5, "financieros": 4.0},
})

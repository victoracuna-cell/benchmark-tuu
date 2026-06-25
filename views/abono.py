import streamlit as st
from views._table import _render_table

def render(data: dict):
    st.subheader("Abono y liquidez")
    _render_table(data, "abono", {
        "Plazo estándar": "plazo_estandar",
        "Abono inmediato": "abono_inmediato",
        "Costo abono inmediato": "costo_abono_inmediato",
        "Destino del abono": "destino",
        "Fines de semana": "fines_de_semana",
        "Notas": "notas",
    })

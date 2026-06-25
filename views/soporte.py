import streamlit as st
from views._table import _render_table

def render(data: dict):
    st.subheader("Soporte y garantía")
    _render_table(data, "soporte", {
        "Canales disponibles": "canales",
        "Horario de atención": "horario",
        "Garantía del equipo": "garantia",
        "Tiempo respuesta estimado": "tiempo_respuesta",
        "SLA documentado": "sla",
        "Notas": "notas",
    })

import streamlit as st
from views._table import _render_table

def render(data: dict):
    st.subheader("Documentos tributarios")
    _render_table(data, "documentos", {
        "Boleta electrónica": "boleta",
        "Costo boleta/mes": "costo_boleta_mes",
        "Factura electrónica": "factura",
        "Costo factura/mes": "costo_factura_mes",
        "Guía de despacho": "guia_despacho",
        "Notas SII": "notas",
    })

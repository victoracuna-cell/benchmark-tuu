import streamlit as st
from views._table import _render_table

def render(data: dict):
    st.subheader("Funcionalidades de gestión de negocio")
    _render_table(data, "gestion", {
        "Punto de venta (POS)": "pos",
        "Catálogo de productos": "catalogo",
        "Inventario": "inventario",
        "Agenda / reservas": "agenda",
        "Multilocal / sucursales": "multilocal",
        "Reportes de venta": "reportes",
        "App móvil": "app_movil",
        "Notas": "notas",
    })

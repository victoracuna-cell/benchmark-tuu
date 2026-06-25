import streamlit as st
from views._table import _render_table

def render(data: dict):
    st.markdown("**Hardware · Precio y modelo**")
    _render_table(data, "hardware", {
        "Modelo principal": "modelo_principal",
        "Precio lista": "precio_lista_clp",
        "Precio oferta": "precio_oferta_clp",
        "Modalidad": "modalidad",
        "Mensualidad": "mensualidad",
        "Pantalla": "pantalla",
        "Impresora": "impresora",
        "Conectividad": "conectividad",
        "Garantía": "garantia",
        "Notas": "notas",
    })

import streamlit as st
from views._table import _render_table

def render(data: dict):
    st.subheader("Productos financieros")
    _render_table(data, "financieros", {
        "Adelanto de ventas": "adelanto",
        "Monto máx. adelanto": "monto_max_adelanto",
        "Crédito": "credito",
        "Cuotas sin interés (cliente)": "cuotas_sin_interes",
        "Comisión por cuotas": "comision_cuotas",
        "Notas": "notas",
    })

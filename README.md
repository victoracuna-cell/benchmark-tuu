# Benchmark competitivo TUU — Streamlit App

Análisis automatizado de precios, funcionalidades y planes de POS en Chile usando Firecrawl + Claude.

## Deploy en Streamlit Cloud (gratis)

### 1. Subir a GitHub

```bash
git init
git add .
git commit -m "benchmark tuu inicial"
git remote add origin https://github.com/TU_USUARIO/benchmark-tuu.git
git push -u origin main
```

### 2. Deploy en Streamlit Cloud

1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Conectar tu cuenta de GitHub
3. Seleccionar el repo y el archivo `app.py`
4. Click en **Deploy**

### 3. Agregar API keys como secrets (recomendado)

En Streamlit Cloud → Settings → Secrets, agregar:

```toml
FIRECRAWL_API_KEY = "fc-..."
ANTHROPIC_API_KEY = "sk-ant-..."
```

Si usás secrets, modificá `app.py` para leerlos así:
```python
import streamlit as st
fc_key = st.secrets.get("FIRECRAWL_API_KEY", "")
anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", "")
```

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```
benchmark_tuu_streamlit/
├── app.py              # App principal
├── requirements.txt    # Dependencias
└── README.md
```

## Sitios analizados

- TUU (referencia) — tuu.cl
- Transbank — transbank.cl
- Mercado Pago — mercadopago.cl
- SumUp — sumup.com/es-cl
- Compraquí — compraqui.cl
- Getnet — getnet.cl
- Redelcom — redelcom.cl
- URL personalizada (opcional)

## Qué analiza

| Categoría | Datos |
|-----------|-------|
| Precios | Precio dispositivo, comisiones débito/crédito, mensualidad |
| Tiempos | Plazo de abono |
| Funciones | Boleta/factura, impresora, cuotas, NFC, inventario, links de pago, ecommerce |
| Scores | Precio 1-10, Funcionalidades 1-10 |
| Insights | Oportunidades, ventajas y alertas estratégicas para TUU |

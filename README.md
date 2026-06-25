# Benchmark TUU vs Competencia

App de análisis competitivo para el mercado de pagos en Chile. Datos extraídos desde sitios oficiales vía Tavily, estructurados con Claude y guardados en este mismo repositorio como JSON.

## Stack
- **Frontend**: Streamlit
- **Scraping**: Tavily API
- **Estructuración de datos**: Claude API (claude-sonnet-4-6)
- **Storage**: GitHub (este repo, archivo `data/benchmark.json`)
- **Deploy**: Streamlit Cloud

## Setup

### 1. Fork o clona este repo en GitHub

### 2. Crea la carpeta de datos
```bash
mkdir -p data
echo '{}' > data/benchmark.json
git add data/benchmark.json
git commit -m "chore: init benchmark data"
git push
```

### 3. Crea un GitHub Personal Access Token
Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
Permisos necesarios: `repo` (lectura y escritura de contenido)

### 4. Obtén tus API keys
- **Tavily**: https://tavily.com — plan gratuito disponible
- **Anthropic**: https://console.anthropic.com

### 5. Deploy en Streamlit Cloud
1. Ve a https://share.streamlit.io
2. Conecta tu repo
3. App file: `app.py`
4. En **Settings > Secrets**, agrega:

```toml
GITHUB_TOKEN   = "ghp_..."
GITHUB_REPO    = "tu-usuario/tu-repo"
GITHUB_PATH    = "data/benchmark.json"
TAVILY_API_KEY = "tvly-..."
ANTHROPIC_API_KEY = "sk-ant-..."
```

## Uso

### Primera vez
1. Ve a **Actualizar datos** en el menú lateral
2. Selecciona todos los competidores y dimensiones
3. Haz clic en **Iniciar scraping**
4. El proceso tarda ~2-3 minutos y guarda automáticamente en GitHub

### Actualizar datos
Repite el paso anterior cuando quieras refrescar los datos. Cada actualización hace un commit al repo con timestamp.

### Editar manualmente
Si el scraping no captura algún dato, ve a **Editar manualmente** y ajusta el JSON directamente.

## Estructura del JSON
```json
{
  "last_updated": "2026-06-25T...",
  "competitors": {
    "tuu": {
      "name": "TUU",
      "comisiones": { "debito_pct": 1.49, "credito_pct": 1.49, ... },
      "hardware": { "modelo_principal": "PRO 2", "precio_oferta_clp": 44900, ... },
      "documentos": { "boleta": "incluida", "factura": "incluida", ... },
      "abono": { "plazo_estandar": "1 día hábil", "abono_inmediato": "sí", ... },
      "gestion": { "pos": "sí", "catalogo": "sí", "inventario": "sí", ... },
      "soporte": { "canales": "WhatsApp, teléfono", "garantia": "2 años", ... },
      "financieros": { "adelanto": "sí", "monto_max_adelanto": 15000000, ... },
      "scores": { "comisiones": 5.0, "hardware": 4.5, ... }
    },
    "transbank": { ... },
    "mercadopago": { ... },
    "klap": { ... },
    "getnet": { ... },
    "flow": { ... }
  }
}
```

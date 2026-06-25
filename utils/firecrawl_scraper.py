import streamlit as st
import requests

FIRECRAWL_API = "https://api.firecrawl.dev/v1"

def _key():
    return st.secrets.get("FIRECRAWL_API_KEY", "")

def scrape_url(url: str) -> str:
    """Scrape a single URL with Firecrawl, returns markdown content."""
    r = requests.post(
        f"{FIRECRAWL_API}/scrape",
        headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json"},
        json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
        timeout=30,
    )
    if r.status_code != 200:
        return ""
    data = r.json()
    return data.get("data", {}).get("markdown", "") or ""

def scrape_competitor(seed: dict) -> str:
    """Scrape all pages for a competitor, return combined content (max 6000 chars)."""
    pages = seed.get("pages", {})
    parts = []
    for name, url in pages.items():
        content = scrape_url(url)
        if content:
            parts.append(f"### {name}\nURL: {url}\n\n{content}")
    combined = "\n\n---\n\n".join(parts)
    return combined[:6000]

COMPETITOR_SEEDS = {
    "tuu": {
        "name": "TUU",
        "pages": {
            "precios":  "https://www.tuu.cl/precios",
            "pago":     "https://www.tuu.cl/pago",
            "adelanto": "https://www.tuu.cl/adelanto",
            "cuotas":   "https://www.tuu.cl/cuotas-tuu",
        },
    },
    "transbank": {
        "name": "Transbank",
        "pages": {
            "tarifas":  "https://publico.transbank.cl/tarifas",
            "ayuda":    "https://ayuda.transbank.cl/tarifas-vender-transbank",
        },
    },
    "mercadopago": {
        "name": "Mercado Pago",
        "pages": {
            "lectores": "https://www.mercadopago.cl/herramientas-para-vender/lectores-point",
        },
    },
    "klap": {
        "name": "Klap",
        "pages": {
            "tarifas": "https://www.klap.cl/home-comercios/tarifas/tarifas-pos",
        },
    },
    "getnet": {
        "name": "Getnet (Santander)",
        "pages": {
            "tarifario": "https://www.getnet.cl/tarifario",
        },
    },
    "flow": {
        "name": "Flow",
        "pages": {
            "precios": "https://www.flow.cl/precios.php",
        },
    },
}

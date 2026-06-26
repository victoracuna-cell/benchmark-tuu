import streamlit as st
import requests

TAVILY_API = "https://api.tavily.com"

def _key():
    return st.secrets.get("TAVILY_API_KEY", "")

def tavily_extract(urls: list[str], query: str = "") -> list[dict]:
    """Extract content using Tavily extract endpoint."""
    key = _key()
    if not key:
        return []
    try:
        r = requests.post(
            f"{TAVILY_API}/extract",
            json={
                "api_key": key,
                "urls": urls,
                "extract_depth": "advanced",
                "format": "markdown",
            },
            timeout=30,
        )
        if r.status_code != 200:
            return []
        data = r.json()
        return data.get("results", [])
    except Exception:
        return []

def tavily_search(query: str, country: str = "Chile", max_results: int = 5) -> list[dict]:
    """Search using Tavily search endpoint as fallback."""
    key = _key()
    if not key:
        return []
    try:
        r = requests.post(
            f"{TAVILY_API}/search",
            json={
                "api_key": key,
                "query": query,
                "search_depth": "advanced",
                "max_results": max_results,
                "include_raw_content": True,
                "country": country,
            },
            timeout=20,
        )
        if r.status_code != 200:
            return []
        return r.json().get("results", [])
    except Exception:
        return []

def get_content_for_competitor(seed: dict, comp_name: str) -> str:
    """
    Try extract first, fall back to search if no content returned.
    Returns combined raw text (max 6000 chars).
    """
    pages = list(seed.get("pages", {}).values())

    # Try extract
    extracted = tavily_extract(pages, query="precios comisiones tarifas boleta factura soporte garantía abono")
    raw_parts = [r.get("raw_content", "") or "" for r in extracted if r.get("raw_content")]

    # If extract returned nothing, fall back to search
    if not raw_parts:
        search_results = tavily_search(
            f"{comp_name} Chile precios comisiones tarifas máquina POS boleta electrónica",
            max_results=5,
        )
        raw_parts = [r.get("raw_content", "") or r.get("content", "") for r in search_results]

    combined = "\n\n".join(raw_parts)
    return combined[:6000]


COMPETITOR_SEEDS = {
    "tuu": {
        "name": "TUU",
        "url": "https://www.tuu.cl",
        "pages": {
            "precios":  "https://www.tuu.cl/precios",
            "pago":     "https://www.tuu.cl/pago",
            "adelanto": "https://www.tuu.cl/adelanto",
            "cuotas":   "https://www.tuu.cl/cuotas-tuu",
            "abono":    "https://www.tuu.cl/abono-inmediato",
        },
    },
    "transbank": {
        "name": "Transbank",
        "url": "https://www.transbank.cl",
        "pages": {
            "tarifas":       "https://publico.transbank.cl/tarifas",
            "ayuda_tarifas": "https://ayuda.transbank.cl/tarifas-vender-transbank",
        },
    },
    "mercadopago": {
        "name": "Mercado Pago",
        "url": "https://www.mercadopago.cl",
        "pages": {
            "lectores": "https://www.mercadopago.cl/herramientas-para-vender/lectores-point",
        },
    },
    "klap": {
        "name": "Klap",
        "url": "https://www.klap.cl",
        "pages": {
            "tarifas_pos": "https://www.klap.cl/home-comercios/tarifas/tarifas-pos",
            "tiendas":     "https://www.klap.cl/home-comercios/tiendas-locales-comerciales",
        },
    },
    "getnet": {
        "name": "Getnet (Santander)",
        "url": "https://www.getnet.cl",
        "pages": {
            "tarifario": "https://www.getnet.cl/tarifario",
        },
    },
    "flow": {
        "name": "Flow",
        "url": "https://www.flow.cl",
        "pages": {
            "precios": "https://www.flow.cl/precios.php",
        },
    },
}

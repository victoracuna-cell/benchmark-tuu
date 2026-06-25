import streamlit as st
import requests

TAVILY_API = "https://api.tavily.com"

def _key():
    return st.secrets.get("TAVILY_API_KEY", "")

def tavily_search(query: str, country: str = "Chile", max_results: int = 5) -> list[dict]:
    r = requests.post(f"{TAVILY_API}/search", json={
        "api_key": _key(),
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "country": country,
    }, timeout=20)
    if r.status_code != 200:
        return []
    return r.json().get("results", [])

def tavily_extract(urls: list[str], query: str = "") -> list[dict]:
    r = requests.post(f"{TAVILY_API}/extract", json={
        "api_key": _key(),
        "urls": urls,
        "extract_depth": "advanced",
        "query": query,
    }, timeout=30)
    if r.status_code != 200:
        return []
    return r.json().get("results", [])

def tavily_map(url: str, max_depth: int = 2, limit: int = 30) -> list[str]:
    r = requests.post(f"{TAVILY_API}/map", json={
        "api_key": _key(),
        "url": url,
        "max_depth": max_depth,
        "limit": limit,
        "instructions": "Find pages about pricing, plans, fees, commissions, tarifas, precios, hardware, soporte",
    }, timeout=30)
    if r.status_code != 200:
        return []
    return r.json().get("results", [])

COMPETITOR_SEEDS = {
    "tuu": {
        "name": "TUU",
        "url": "https://www.tuu.cl",
        "pages": {
            "precios": "https://www.tuu.cl/precios",
            "pago": "https://www.tuu.cl/pago",
            "adelanto": "https://www.tuu.cl/adelanto",
            "cuotas": "https://www.tuu.cl/cuotas-tuu",
            "abono": "https://www.tuu.cl/abono-inmediato",
        }
    },
    "transbank": {
        "name": "Transbank",
        "url": "https://www.transbank.cl",
        "pages": {
            "tarifas": "https://publico.transbank.cl/tarifas",
            "ayuda_tarifas": "https://ayuda.transbank.cl/tarifas-vender-transbank",
        }
    },
    "mercadopago": {
        "name": "Mercado Pago",
        "url": "https://www.mercadopago.cl",
        "pages": {
            "lectores": "https://www.mercadopago.cl/herramientas-para-vender/lectores-point",
        }
    },
    "klap": {
        "name": "Klap",
        "url": "https://www.klap.cl",
        "pages": {
            "tarifas_pos": "https://www.klap.cl/home-comercios/tarifas/tarifas-pos",
            "tiendas": "https://www.klap.cl/home-comercios/tiendas-locales-comerciales",
        }
    },
    "getnet": {
        "name": "Getnet (Santander)",
        "url": "https://www.getnet.cl",
        "pages": {
            "tarifario": "https://www.getnet.cl/tarifario",
        }
    },
    "flow": {
        "name": "Flow",
        "url": "https://www.flow.cl",
        "pages": {
            "precios": "https://www.flow.cl/precios.php",
        }
    },
}

import streamlit as st
import requests
import re

BROWSERLESS_API = "https://chrome.browserless.io"

def _bl_key():
    return st.secrets.get("BROWSERLESS_API_KEY", "")

def _tavily_key():
    return st.secrets.get("TAVILY_API_KEY", "")

def _clean_html(html: str) -> str:
    html = re.sub(r'<(script|style|nav|footer|header|svg)[^>]*>.*?</\1>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html

def scrape_with_tavily_extract(urls: list, query: str = "") -> str:
    """Use Tavily extract — best for sites that block bots (TUU, Transbank)."""
    key = _tavily_key()
    if not key:
        return ""
    try:
        r = requests.post("https://api.tavily.com/extract", json={
            "api_key": key,
            "urls": urls,
            "extract_depth": "advanced",
        }, timeout=30)
        if r.status_code != 200:
            return ""
        results = r.json().get("results", [])
        parts = [res.get("raw_content", "") or "" for res in results if res.get("raw_content")]
        return "\n\n---\n\n".join(parts)[:6000]
    except Exception:
        return ""

def scrape_with_browserless(url: str) -> str:
    """Browserless — best for JS-heavy sites (Mercado Pago, Klap)."""
    key = _bl_key()
    if not key:
        return ""
    try:
        r = requests.post(
            f"{BROWSERLESS_API}/content",
            params={"token": key},
            json={"url": url},
            timeout=35,
        )
        if r.status_code != 200:
            return ""
        return _clean_html(r.text)
    except Exception:
        return ""

def scrape_with_tavily_search(query: str, domain: str = "") -> str:
    """Tavily search — emergency fallback."""
    key = _tavily_key()
    if not key:
        return ""
    try:
        payload = {
            "api_key": key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 4,
            "include_raw_content": True,
        }
        if domain:
            payload["include_domains"] = [domain]
        r = requests.post("https://api.tavily.com/search", json=payload, timeout=20)
        if r.status_code != 200:
            return ""
        results = r.json().get("results", [])
        parts = [res.get("raw_content") or res.get("content", "") for res in results]
        return "\n\n---\n\n".join(p for p in parts if p)[:6000]
    except Exception:
        return ""

def scrape_competitor(seed: dict) -> str:
    """
    Scrape using the best strategy per competitor:
    - method: "tavily_extract" → for sites that block bots (TUU, Transbank)
    - method: "browserless"    → for JS-heavy sites (Mercado Pago, Klap)
    - Falls back to tavily_search if primary fails
    """
    name = seed.get("name", "")
    pages = seed.get("pages", {})
    method = seed.get("method", "browserless")
    domain = seed.get("url", "").replace("https://", "").replace("http://", "").split("/")[0]
    fallback_query = seed.get("fallback_query", f"{name} Chile precios comisiones tarifas POS")

    combined = ""

    if method == "tavily_extract":
        urls = list(pages.values())
        combined = scrape_with_tavily_extract(urls, query="precios comisiones tarifas boleta factura abono garantía soporte")

    elif method == "browserless":
        parts = []
        wait = seed.get("wait_for", 3000)
        for page_name, url in pages.items():
            content = scrape_with_browserless(url, wait_for=wait)
            if content and len(content) > 300:
                parts.append(f"### {page_name}\n{content[:1800]}")
        combined = "\n\n---\n\n".join(parts)

    # Fallback if primary got nothing
    if len(combined) < 400:
        combined = scrape_with_tavily_search(fallback_query, domain=domain)

    return combined[:6000]


COMPETITOR_SEEDS = {
    "tuu": {
        "name": "TUU",
        "url": "https://www.tuu.cl",
        "method": "tavily_extract",   # Tavily extrae perfecto de TUU
        "fallback_query": "TUU tuu.cl Chile precios comisiones máquina POS boleta factura adelanto abono inmediato 2025",
        "pages": {
            "precios":     "https://www.tuu.cl/precios",
            "pago":        "https://www.tuu.cl/pago",
            "adelanto":    "https://www.tuu.cl/adelanto",
            "cuotas":      "https://www.tuu.cl/cuotas-tuu",
            "abono":       "https://www.tuu.cl/abono-inmediato",
            "punto_venta": "https://www.tuu.cl/punto-de-venta",
        },
    },
    "transbank": {
        "name": "Transbank",
        "url": "https://publico.transbank.cl",
        "method": "tavily_extract",   # ayuda.transbank.cl es HTML estático
        "fallback_query": "Transbank Chile comisiones débito crédito 2025 tarifas POS Mobile Smart arriendo boleta",
        "pages": {
            "tarifas_ayuda": "https://ayuda.transbank.cl/tarifas-vender-transbank",
            "tarifas_pub":   "https://publico.transbank.cl/tarifas",
            "mobile_pos":    "https://publico.transbank.cl/productos-y-servicios/soluciones-para-ventas-presenciales/mobile-pos",
            "boleta":        "https://publico.transbank.cl/productos-y-servicios/otras-soluciones-para-negocio/boleta-electronica",
        },
    },
    "mercadopago": {
        "name": "Mercado Pago",
        "url": "https://www.mercadopago.cl",
        "method": "browserless",      # JS pesado, necesita render completo
        "wait_for": 4000,
        "fallback_query": "Mercado Pago Chile Point Smart Mini comisiones débito crédito precio boleta factura 2025",
        "pages": {
            "lectores": "https://www.mercadopago.cl/herramientas-para-vender/lectores-point",
            "costos":   "https://www.mercadopago.cl/ayuda/costos-de-vender_2244",
        },
    },
    "klap": {
        "name": "Klap",
        "url": "https://www.klap.cl",
        "method": "browserless",      # JS pesado
        "wait_for": 3500,
        "fallback_query": "Klap Chile tarifas POS comisiones débito crédito arriendo mensualidad boleta electrónica 2025",
        "pages": {
            "tarifas": "https://www.klap.cl/home-comercios/tarifas/tarifas-pos",
            "home":    "https://www.klap.cl/home-comercios",
        },
    },
    "getnet": {
        "name": "Getnet (Santander)",
        "url": "https://www.getnet.cl",
        "method": "tavily_extract",
        "fallback_query": "Getnet Santander Chile POS tarifas comisiones precio máquina pago 2025",
        "pages": {
            "tarifario": "https://www.getnet.cl/tarifario",
            "home":      "https://www.getnet.cl",
        },
    },
    "flow": {
        "name": "Flow",
        "url": "https://www.flow.cl",
        "method": "tavily_extract",
        "fallback_query": "Flow Chile precios comisiones pasarela pagos online tarifas 2025",
        "pages": {
            "precios":  "https://www.flow.cl/precios.php",
        },
    },
}

DIMENSIONS = [
    "comisiones",
    "hardware",
    "documentos",
    "abono",
    "gestion",
    "soporte",
    "financieros",
]

DIM_LABELS = {
    "comisiones": "💸 Comisiones",
    "hardware": "🖥️ Hardware",
    "documentos": "🧾 Documentos tributarios",
    "abono": "⏱️ Abono y liquidez",
    "gestion": "🛠️ Gestión de negocio",
    "soporte": "🎧 Soporte y garantía",
    "financieros": "💳 Productos financieros",
}

COMPETITOR_ORDER = ["tuu", "transbank", "mercadopago", "klap", "getnet", "flow"]

COMPETITOR_COLORS = {
    "tuu": "#2563EB",
    "transbank": "#DC2626",
    "mercadopago": "#059669",
    "klap": "#7C3AED",
    "getnet": "#EA580C",
    "flow": "#0891B2",
}

def score_color(score: float) -> str:
    if score >= 4:
        return "🟢"
    if score >= 3:
        return "🟡"
    return "🔴"

def get_score(data: dict, competitor: str, dimension: str) -> float | None:
    return data.get("competitors", {}).get(competitor, {}).get("scores", {}).get(dimension)

def get_all_scores(data: dict) -> dict:
    result = {}
    for comp, info in data.get("competitors", {}).items():
        result[comp] = info.get("scores", {})
    return result

def weighted_total(scores: dict, weights: dict | None = None) -> float:
    if weights is None:
        weights = {d: 1.0 for d in DIMENSIONS}
    total = 0.0
    w_sum = 0.0
    for dim in DIMENSIONS:
        s = scores.get(dim)
        w = weights.get(dim, 1.0)
        if s is not None:
            total += s * w
            w_sum += w
    return round(total / w_sum, 2) if w_sum > 0 else 0.0

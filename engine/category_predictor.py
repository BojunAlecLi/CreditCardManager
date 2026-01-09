"""Rule-first category predictor (MVP Layer A)."""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Prediction:
    category: str
    confidence: float
    reason_codes: List[str]


def predict_category(context: Dict) -> Prediction:
    """
    Predicts a purchase category using simple rules.

    context keys (suggested):
    - poi_category
    - local_time
    - amount
    - user_history
    """
    poi_category = context.get("poi_category")
    amount = context.get("amount", 0)
    local_time = context.get("local_time")

    reason_codes: List[str] = []

    if poi_category:
        reason_codes.append("Near POI category match")
        return Prediction(category=poi_category, confidence=0.72, reason_codes=reason_codes)

    if amount < 15:
        reason_codes.append("Low amount bucket")
        return Prediction(category="coffee", confidence=0.46, reason_codes=reason_codes)

    if 20 <= amount <= 60 and local_time in {"lunch", "dinner"}:
        reason_codes.append("Meal time and amount bucket")
        return Prediction(category="restaurant", confidence=0.54, reason_codes=reason_codes)

    if amount >= 800:
        reason_codes.append("High amount bucket")
        return Prediction(category="travel", confidence=0.4, reason_codes=reason_codes)

    reason_codes.append("Fallback default")
    return Prediction(category="general", confidence=0.3, reason_codes=reason_codes)


def top_k(prediction: Prediction, k: int = 3) -> List[Tuple[str, float]]:
    """Returns a dummy top-k list; replace with model probabilities later."""
    base = [(prediction.category, prediction.confidence)]
    remainder = [("grocery", 0.12), ("transit", 0.08)]
    return (base + remainder)[:k]


if __name__ == "__main__":
    sample_context = {
        "poi_category": "restaurant",
        "amount": 42.5,
        "local_time": "dinner",
    }
    pred = predict_category(sample_context)
    print(pred)
    print(top_k(pred))

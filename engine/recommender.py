"""End-to-end recommendation pipeline (MVP)."""

import json
from dataclasses import asdict
from typing import Dict, List

from engine.category_predictor import predict_category
from engine.explanations import build_explanations
from engine.reward_optimizer import Card, UserPreferences, recommend_card


def load_cards(path: str) -> List[Card]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    cards = []
    for item in raw:
        cards.append(
            Card(
                id=item["id"],
                name=item["name"],
                reward_rules=item["reward_rules"],
                constraints=item["constraints"],
            )
        )
    return cards


def load_prefs(path: str) -> UserPreferences:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return UserPreferences(
        mode=raw["mode"],
        weights=raw["weights"],
        bonus_progress=raw["bonus_progress"],
    )


def recommend(context: Dict, cards: List[Card], prefs: UserPreferences) -> Dict:
    prediction = predict_category(context)
    accepts_amex = context.get("accepts_amex", True)
    card = recommend_card(
        cards,
        prediction.category,
        context.get("amount", 0.0),
        prefs,
        accepts_amex=accepts_amex,
    )
    explanations = build_explanations(prediction.category, prediction.reason_codes)

    return {
        "recommended_card_id": card.id,
        "predicted_category": prediction.category,
        "confidence": prediction.confidence,
        "reason_codes": explanations,
    }


def amount_bucket(amount: float) -> str:
    if amount < 15:
        return "under_15"
    if amount < 60:
        return "under_60"
    if amount < 300:
        return "under_300"
    return "over_300"


def log_recommendation(context: Dict, output: Dict) -> Dict:
    return {
        "context": context,
        "output": output,
        "followed": None,
    }


def to_record(context: Dict, output: Dict) -> Dict:
    record = log_recommendation(context, output)
    record["context"]["amount_bucket"] = amount_bucket(context.get("amount", 0.0))
    return record


if __name__ == "__main__":
    cards = load_cards("data/sample_datasets/cards.json")
    prefs = load_prefs("data/sample_datasets/user_prefs.json")

    ctx = {
        "poi_category": "restaurant",
        "amount": 42.5,
        "local_time": "dinner",
    }

    output = recommend(ctx, cards, prefs)
    print(output)
    print("log_record:")
    print(json.dumps(to_record(ctx, output), indent=2))

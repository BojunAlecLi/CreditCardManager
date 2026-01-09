"""Reward decision engine using weighted utility."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Card:
    id: str
    name: str
    reward_rules: Dict[str, float]
    constraints: Dict[str, bool]


@dataclass
class UserPreferences:
    mode: str
    weights: Dict[str, float]
    bonus_progress: Dict[str, float]


def expected_rewards(card: Card, category: str, amount: float) -> float:
    alias_map = {
        "coffee": "restaurant",
        "pet_store": "general",
        "pharmacy": "general",
    }
    resolved = alias_map.get(category, category)
    multiplier = card.reward_rules.get(resolved, card.reward_rules.get("general", 1.0))
    return amount * multiplier


def utility_score(
    card: Card,
    category: str,
    amount: float,
    prefs: UserPreferences,
) -> float:
    base = expected_rewards(card, category, amount)

    # Simple weights: bump if bonus chase or fee break-even is important.
    bonus_weight = prefs.weights.get("bonus_chase", 0.0)
    fee_weight = prefs.weights.get("fee_break_even", 0.0)

    bonus_progress = prefs.bonus_progress.get(card.id, 0.0)
    bonus_boost = (1.0 - bonus_progress) * bonus_weight * amount

    return base + bonus_boost + fee_weight


def recommend_card(
    cards: List[Card],
    category: str,
    amount: float,
    prefs: UserPreferences,
    accepts_amex: bool = True,
) -> Card:
    best = None
    best_score = float("-inf")
    for card in cards:
        if card.constraints.get("requires_amex", False) and not accepts_amex:
            continue
        score = utility_score(card, category, amount, prefs)
        if score > best_score:
            best_score = score
            best = card
    if not best:
        raise ValueError("No eligible card found")
    return best

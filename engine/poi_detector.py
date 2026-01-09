"""Mock POI detector using local merchant data and simple heuristics."""

import json
import math
from typing import Dict, List, Optional, Tuple


Merch = Dict[str, object]


def load_merchants(path: str) -> List[Merch]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def distance_km(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    lat1, lon1 = a
    lat2, lon2 = b
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 111


def detect_poi_category(
    lat: float,
    lng: float,
    merchants: List[Merch],
    max_km: float = 0.3,
) -> Optional[Dict[str, object]]:
    """
    Returns best merchant match if within max_km; otherwise None.
    """
    best = None
    best_km = float("inf")
    for merch in merchants:
        geo = merch.get("geo", {})
        m_lat = geo.get("lat")
        m_lng = geo.get("lng")
        if m_lat is None or m_lng is None:
            continue
        km = distance_km((lat, lng), (m_lat, m_lng))
        if km < best_km:
            best_km = km
            best = merch

    if best and best_km <= max_km:
        return {
            "place_id": best.get("place_id"),
            "name": best.get("name"),
            "category": best.get("category"),
            "distance_km": round(best_km, 3),
        }
    return None


def fallback_category(lat: float, lng: float) -> str:
    """Deterministic fallback based on coordinates."""
    buckets = ["restaurant", "pet_store", "grocery", "coffee", "pharmacy", "general"]
    key = int(abs(lat * 1000) + abs(lng * 1000)) % len(buckets)
    return buckets[key]

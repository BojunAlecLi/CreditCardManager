"""Fake location generator to simulate movement across a city grid."""

import random
from dataclasses import dataclass
from typing import List, Tuple

from engine.poi_detector import detect_poi_category, fallback_category, load_merchants


@dataclass
class LocationHit:
    lat: float
    lng: float
    category: str
    confidence: float
    source: str


def generate_grid(
    center: Tuple[float, float],
    span: float = 0.02,
    step: float = 0.005,
) -> List[Tuple[float, float]]:
    lat0, lng0 = center
    points = []
    lat = lat0 - span
    while lat <= lat0 + span:
        lng = lng0 - span
        while lng <= lng0 + span:
            points.append((round(lat, 6), round(lng, 6)))
            lng += step
        lat += step
    return points


def simulate_locations(
    merchants_path: str,
    center: Tuple[float, float] = (43.65, -79.38),
    span: float = 0.02,
    step: float = 0.005,
    seed: int = 7,
) -> List[LocationHit]:
    random.seed(seed)
    merchants = load_merchants(merchants_path)
    hits: List[LocationHit] = []

    for lat, lng in generate_grid(center, span, step):
        match = detect_poi_category(lat, lng, merchants)
        if match:
            hits.append(
                LocationHit(
                    lat=lat,
                    lng=lng,
                    category=str(match["category"]),
                    confidence=0.82,
                    source="poi_match",
                )
            )
        else:
            hits.append(
                LocationHit(
                    lat=lat,
                    lng=lng,
                    category=fallback_category(lat, lng),
                    confidence=0.35,
                    source="fallback",
                )
            )

    return hits


if __name__ == "__main__":
    results = simulate_locations("data/sample_datasets/merchants.json")
    for hit in results[:10]:
        print(hit)

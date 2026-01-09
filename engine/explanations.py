"""Human-readable explanation generator."""

from typing import List


def build_explanations(predicted_category: str, reason_codes: List[str]) -> List[str]:
    explanations = []
    if predicted_category:
        explanations.append(f"Predicted category: {predicted_category}")
    for code in reason_codes:
        explanations.append(code)
    return explanations

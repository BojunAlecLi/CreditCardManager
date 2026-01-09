"""Simple CLI for the MVP recommender."""

import argparse
import json

from engine.recommender import load_cards, load_prefs, recommend


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart Card Picker CLI")
    parser.add_argument("--amount", type=float, required=True)
    parser.add_argument("--poi-category", type=str, default=None)
    parser.add_argument("--local-time", type=str, default=None)
    parser.add_argument("--accepts-amex", action="store_true")
    parser.add_argument("--cards", type=str, default="data/sample_datasets/cards.json")
    parser.add_argument("--prefs", type=str, default="data/sample_datasets/user_prefs.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    context = {
        "amount": args.amount,
        "poi_category": args.poi_category,
        "local_time": args.local_time,
        "accepts_amex": args.accepts_amex,
    }

    cards = load_cards(args.cards)
    prefs = load_prefs(args.prefs)
    output = recommend(context, cards, prefs)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

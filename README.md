# Smart Card Picker (Canada-focused)

Mobile assistant that recommends the best credit card to use before a purchase, based on predicted purchase category and user priorities.

## Repo layout

- app/ - mobile UI surfaces (placeholder)
- engine/ - category prediction, reward optimization, explanations, pipeline
- data/ - schemas and sample datasets
- docs/ - PRD, API contracts, mapping tables, architecture

## Quick start (local)

This repo is a scaffold. The engine is runnable Python modules with stubbed logic.

- Python 3.10+
- Run a quick demo:

```
python3 -m engine.recommender
```

- Or use the CLI:

```
python3 -m engine.cli --amount 42.50 --poi-category restaurant --local-time dinner --accepts-amex
```

## MVP goals

- Recommend a card with confidence + reasons
- Learn from posted transactions
- Support user priority modes (points vs cashback vs bonus chase)

## Non-goals (for now)

- Automatic Apple Pay card switching
- Perfect MCC prediction
- Full banking integration

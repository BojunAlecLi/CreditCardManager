# Smart Card Picker (Canada-focused)

Mobile assistant that recommends the best credit card to use before a purchase, based on predicted purchase category and user priorities.

## Repo layout

- app/ - mock UI for adding cards and detecting benefits
- engine/ - category prediction, reward optimization, explanations, pipeline
- data/ - schemas and sample datasets
- docs/ - PRD, API contracts, mapping tables, architecture

## Quick start (local)

### Mock UI

Open `app/index.html` in a browser.

### Engine demo

- Python 3.10+
- Run a quick demo:

```
python3 -m engine.recommender
```

- Or use the CLI:

```
python3 -m engine.cli --amount 42.50 --poi-category restaurant --local-time dinner --accepts-amex
```

- Or use a lat/lng with mock POI detection:

```
python3 -m engine.cli --amount 18.00 --lat 43.648 --lng -79.382 --accepts-amex
```

- Simulate locations:

```
python3 -m engine.location_simulator
```

## MVP goals

- Recommend a card with confidence + reasons
- Learn from posted transactions
- Support user priority modes (points vs cashback vs bonus chase)

## Non-goals (for now)

- Automatic Apple Pay card switching
- Perfect MCC prediction
- Full banking integration

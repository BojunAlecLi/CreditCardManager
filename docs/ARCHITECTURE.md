# Architecture Notes

## Layer A (Rules)
- POI category -> predicted category
- Amount/time heuristics
- Category -> reward optimization

## Layer B (Learning)
- Start with lightweight model (logistic regression)
- Features: time bucket, amount bucket, POI category, user history
- Train per-user with global priors

## Data Flow
1. Context -> category prediction
2. Prediction + prefs -> reward optimizer
3. Output -> recommendation log
4. Posted transaction -> feedback to model

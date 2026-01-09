# API Contracts (Local)

## Recommend

Request
```
{
  "timestamp": "2025-01-01T12:00:00Z",
  "amount": 42.50,
  "location": {"lat": 43.65, "lng": -79.38},
  "local_time": "lunch"
}
```

Response
```
{
  "recommended_card_id": "cobalt",
  "predicted_category": "restaurant",
  "confidence": 0.78,
  "reason_codes": ["Near POI category match", "Meal time and amount bucket"]
}
```

## Log Recommendation

Request
```
{
  "context": {"amount": 42.50, "local_time": "lunch"},
  "output": {"recommended_card_id": "cobalt"},
  "followed": true
}
```

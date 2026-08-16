# polymarket

ML pipeline for polymarket recommendation system.

## What is included

- Data gathering from local JSON and/or remote JSON endpoint
- Data normalization for user bet events
- Recommendation model combining:
  - user-based collaborative filtering (similar users)
  - popularity fallback
- FastAPI endpoint for recommendations

## Installation

```bash
pip install -r requirements.txt
```

## Run API

```bash
uvicorn app:app --reload
```

Optional environment variables:

- `BETS_DATA_PATH` - path to JSON file containing bet events
- `BETS_DATA_URL` - URL returning JSON array of bet events

If no source is provided, the API uses built-in sample data.

## API

`GET /recommendations/{user_id}?k=5`

Response:

```json
{
  "user_id": "u1",
  "recommendations": [
    {"market_id": "m4", "score": 3.5}
  ]
}
```

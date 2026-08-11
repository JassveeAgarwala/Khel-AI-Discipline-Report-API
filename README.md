# Khel AI Discipline Report API

## Objective

This API measures bowling discipline from raw delivery data. It detects wides and no-balls, calculates legal and illegal delivery rates, generates an innings discipline score, and provides separate discipline statistics for each bowler.

## Files

```text
main.py
schemas.py
services.py
Readme.md
requirements.txt
sample_input.json
```

## Install and Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

## Main Endpoint

```http
POST /discipline-report
```

## Complete Endpoint

```text
https://YOUR-RENDER-URL.onrender.com/discipline-report
```

## Request Example

```json
{
  "innings_id": "innings-001",
  "deliveries": [
    {
      "delivery_id": "ball-001",
      "bowler": "Mitchell Starc",
      "batter": "Rohit Sharma",
      "over_number": 0,
      "ball_number": 1,
      "batter_runs": 0,
      "extras": {
        "wides": 1
      }
    }
  ]
}
```

## Discipline Rule

The discipline score starts at 100.

```text
Each wide delivery: -2 points
Each no-ball delivery: -3 points
Minimum score: 0
```

Formula:

```text
Score = 100 - (wide deliveries × 2) - (no-ball deliveries × 3)
```

Ratings:

```text
95–100: Excellent
85–94: Good
70–84: Needs improvement
Below 70: Poor
```

## Response

The API returns:

- Total deliveries.
- Legal deliveries.
- Illegal deliveries.
- Wide deliveries.
- No-ball deliveries.
- Wide runs.
- No-ball runs.
- Legal delivery rate.
- Illegal delivery rate.
- Discipline score.
- Rating.
- Recommendations.
- Individual bowler statistics.

## Render Deployment

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
uvicorn main:app --host 0.0.0.0 --port $PORT
```

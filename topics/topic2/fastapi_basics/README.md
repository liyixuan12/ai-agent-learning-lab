# Topic 2 — FastAPI Financial Demo

## Run

```bash
cd topics/topic2/fastapi_basics
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints

| Method | Path | Notes |
|--------|------|--------|
| GET | `/health` | Liveness |
| POST | `/analyze-company` | JSON body: `name`, `ticker`, `sector`, `revenue_growth`, `pe_ratio`, `debt_ratio` |
| POST | `/upload-document` | Returns `501` until a later topic |
| POST | `/ask` | Returns `501` until Topic 3+ |

Analysis logic lives in `topics/topic1/topic1_final_project.py` and is loaded by `app/services/analyze.py`.

## Example

```bash
curl -s http://127.0.0.1:8000/health

curl -s -X POST http://127.0.0.1:8000/analyze-company \
  -H "Content-Type: application/json" \
  -d '{"name":"NVIDIA","ticker":"NVDA","sector":"Semiconductor","revenue_growth":0.35,"pe_ratio":55,"debt_ratio":0.25}'
```

## Tests

```bash
pytest
```

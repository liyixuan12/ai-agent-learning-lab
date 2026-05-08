"""FastAPI application entrypoint."""

from fastapi import FastAPI

from src.financial_analyzer import analyze_company_stub

app = FastAPI(title="FinSight AI API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze-company")
def analyze_company(payload: dict):
    name = payload.get("name", "unknown")
    return analyze_company_stub(name)

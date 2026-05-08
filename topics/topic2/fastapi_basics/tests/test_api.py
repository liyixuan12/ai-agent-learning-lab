from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "ok"


def test_analyze_company():
    payload = {
        "name": "Apple",
        "ticker": "AAPL",
        "sector": "Technology",
        "revenue_growth": 0.08,
        "pe_ratio": 28,
        "debt_ratio": 0.35,
    }
    r = client.post("/analyze-company", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Apple"
    assert "growth_level" in data
    assert "risk_level" in data
    assert "summary" in data
    assert "Moderate growth" in data["summary"] or "growth" in data["summary"].lower()


def test_upload_document_stub():
    r = client.post("/upload-document", json={"filename": "q.pdf"})
    assert r.status_code == 501


def test_ask_stub():
    r = client.post("/ask", json={"question": "What is revenue?"})
    assert r.status_code == 501

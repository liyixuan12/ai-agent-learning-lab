from src.financial_analyzer import analyze_company_stub


def test_analyze_company_stub():
    out = analyze_company_stub("TEST")
    assert out["company"] == "TEST"

"""Domain analysis: delegates to Topic 1 rule-based logic."""

import importlib.util
from pathlib import Path

from app.schemas.company import AnalyzeCompanyResponse, CompanySnapshot


def _load_topic1_final_project():
    """Load topics/topic1/topic1_final_project.py without packaging topic1 as a package."""
    topics_dir = Path(__file__).resolve().parents[4]
    path = topics_dir / "topic1" / "topic1_final_project.py"
    spec = importlib.util.spec_from_file_location("topic1_final_project", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Topic 1 module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_t1 = _load_topic1_final_project()


def analyze_company_snapshot(payload: CompanySnapshot) -> AnalyzeCompanyResponse:
    company_dict = payload.model_dump()
    summary = _t1.generate_company_summary(company_dict)
    growth_level = _t1.classify_growth(company_dict["revenue_growth"])
    risk_level = _t1.classify_risk(company_dict["pe_ratio"], company_dict["debt_ratio"])
    return AnalyzeCompanyResponse(
        name=payload.name,
        ticker=payload.ticker,
        sector=payload.sector,
        growth_level=growth_level,
        risk_level=risk_level,
        summary=summary,
    )

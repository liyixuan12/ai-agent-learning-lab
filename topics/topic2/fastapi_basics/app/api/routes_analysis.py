from fastapi import APIRouter

from app.schemas.company import AnalyzeCompanyResponse, CompanySnapshot
from app.services.analyze import analyze_company_snapshot

router = APIRouter(tags=["analysis"])


@router.post("/analyze-company", response_model=AnalyzeCompanyResponse)
def analyze_company(payload: CompanySnapshot) -> AnalyzeCompanyResponse:
    return analyze_company_snapshot(payload)

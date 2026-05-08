"""Pydantic models for company analysis API."""

from pydantic import BaseModel, Field


class CompanySnapshot(BaseModel):
    """Request body aligned with Topic 1 company dict fields."""

    name: str = Field(..., description="Company display name")
    ticker: str = Field(..., description="Stock ticker symbol")
    sector: str = Field(..., description="Industry sector")
    revenue_growth: float = Field(..., description="YoY revenue growth as decimal, e.g. 0.08 for 8%")
    pe_ratio: float = Field(..., description="Price-to-earnings ratio")
    debt_ratio: float = Field(..., description="Debt ratio (0–1 scale)")


class AnalyzeCompanyResponse(BaseModel):
    """Stable JSON shape for analyze-company responses."""

    name: str
    ticker: str
    sector: str
    growth_level: str
    risk_level: str
    summary: str

"""Run one company analysis request with structured output validation."""

import json

from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Literal

from llm_client import get_client, get_model_name
from prompt_templates import PROMPT_VERSION, SYSTEM_PROMPT, build_user_prompt


class AnalysisResult(BaseModel):
    """Structured analysis result schema."""

    company: str = Field(min_length=1, max_length=120)
    growth_level: Literal["high", "medium", "low"]
    valuation_view: Literal["overvalued", "fair", "undervalued"]
    risk_level: Literal["high", "medium", "low"]
    key_points: list[str] = Field(min_length=2, max_length=6)
    disclaimer: str = Field(min_length=10, max_length=200)

    @field_validator("key_points")
    @classmethod
    def validate_key_points(cls, value: list[str]) -> list[str]:
        if any(not item.strip() for item in value):
            raise ValueError("key_points cannot contain empty items.")
        return value

    @field_validator("disclaimer")
    @classmethod
    def validate_disclaimer(cls, value: str) -> str:
        if "不构成投资建议" not in value:
            raise ValueError("disclaimer must include '不构成投资建议'.")
        return value


class CompanySnapshot(BaseModel):
    """Input payload schema used by prompt builder."""

    name: str = Field(min_length=1, max_length=120)
    ticker: str = Field(min_length=1, max_length=12)
    sector: str = Field(min_length=1, max_length=60)
    revenue_growth: float = Field(ge=-1.0, le=5.0)
    pe_ratio: float = Field(ge=0.0, le=500.0)
    debt_ratio: float = Field(ge=0.0, le=1.0)


def analyze_company(payload: dict | CompanySnapshot) -> AnalysisResult:
    """Call LLM and parse output into AnalysisResult."""
    snapshot = CompanySnapshot.model_validate(payload)

    client = get_client()
    model = get_model_name()
    prompt = f"{SYSTEM_PROMPT}\n\n{build_user_prompt(snapshot.model_dump())}"

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    content = response.text
    if not content:
        raise ValueError("Empty response content from model.")

    # Gemini may return fenced JSON; normalize before parsing.
    content = content.strip()
    if content.startswith("```"):
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model output is not valid JSON: {exc}") from exc

    try:
        return AnalysisResult.model_validate(data)
    except ValidationError as exc:
        raise ValueError(f"Model output failed schema validation: {exc}") from exc


if __name__ == "__main__":
    sample_company = {
        "name": "NVIDIA",
        "ticker": "NVDA",
        "sector": "Semiconductor",
        "revenue_growth": 0.35,
        "pe_ratio": 55,
        "debt_ratio": 0.25,
    }
    result = analyze_company(sample_company)
    print(f"Prompt version: {PROMPT_VERSION}")
    print(result.model_dump_json(indent=2, ensure_ascii=False))

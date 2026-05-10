"""Topic 6 · FastAPI 最小 API Key 鉴权示例。

跑法（在仓库根目录）：
    # 1) 在 .env 里加：
    #    SERVER_API_KEY=dev-secret-please-change-me
    # 2) 启动：
    .venv/bin/uvicorn topics.topic6.auth_demo:app --port 8001 --reload
    # 3) 验证：
    curl -i http://localhost:8001/health
    curl -i -X POST http://localhost:8001/analyze-company \
        -H 'Content-Type: application/json' \
        -d '{"name":"Acme"}'
    curl -i -X POST http://localhost:8001/analyze-company \
        -H 'Content-Type: application/json' \
        -H "X-API-Key: dev-secret-please-change-me" \
        -d '{"name":"Acme"}'

学习点：
- /health 不鉴权（健康检查通常需要对外可见）。
- /analyze-company 必须带 X-API-Key 请求头。
- 错误信息只说 "Invalid or missing API key"，不暴露任何细节。
- 返回值里始终带 disclaimer，符合金融 Demo 的合规底线。
"""

from __future__ import annotations

import os

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

SERVER_API_KEY = os.getenv("SERVER_API_KEY")

DISCLAIMER = (
    "本回答仅用于学习和研究目的，不构成任何金融投资建议。"
    "信息可能不完整或过时，决策前请咨询持牌专业人士。"
)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not SERVER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server is misconfigured: SERVER_API_KEY missing.",
        )
    if x_api_key != SERVER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


class AnalyzeCompanyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    ticker: str | None = Field(default=None, pattern=r"^[A-Z]{1,5}$")


app = FastAPI(title="Topic 6 Auth Demo", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze-company", dependencies=[Depends(require_api_key)])
def analyze_company(req: AnalyzeCompanyRequest) -> dict:
    summary = (
        f"{req.name} 是一家示例公司。"
        "（这里通常会接入 Topic 4 的 RAG 流水线生成结构化分析。）"
    )
    return {
        "company": req.name,
        "ticker": req.ticker,
        "summary": summary,
        "disclaimer": DISCLAIMER,
    }

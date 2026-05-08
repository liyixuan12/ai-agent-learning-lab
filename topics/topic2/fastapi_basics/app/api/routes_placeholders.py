"""Stub endpoints reserved for later topics (RAG / LLM)."""

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(tags=["future"])


class UploadDocumentBody(BaseModel):
    filename: str = Field(..., description="Original filename")
    content_type: Optional[str] = Field(None, description="MIME type")


class AskBody(BaseModel):
    question: str = Field(..., description="User question")
    context: Optional[str] = Field(None, description="Optional extra context")


@router.post("/upload-document", status_code=501)
def upload_document(_payload: UploadDocumentBody):
    return {
        "detail": "Not implemented in Topic 2. Wire storage and RAG in a later topic.",
        "status": "not_implemented",
    }


@router.post("/ask", status_code=501)
def ask(_payload: AskBody):
    return {
        "detail": "Not implemented in Topic 2. Connect LLM in Topic 3+.",
        "status": "not_implemented",
    }

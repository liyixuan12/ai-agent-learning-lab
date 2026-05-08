"""Minimal RAG demo: retrieval + prompt assembly + answer generation."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import requests

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None  # type: ignore[assignment]

from load_docs import load_text_file
from chunk_embed import Chunk, chunk_by_section, chunk_text, rank_chunks

ENV_CANDIDATES: list[Path] | None = None


def candidate_env_paths() -> list[Path]:
    """Return candidate .env paths for this repo."""
    base_dir = Path(__file__).resolve().parents[2]
    return [
        base_dir / ".env",
        base_dir / "topics" / "topic3" / "llm_prompt_basics" / ".env",
        base_dir / "topics" / "topic4" / ".env",
    ]


def load_environment() -> str | None:
    """Load GEMINI_* env vars from a suitable .env file (if available)."""
    global ENV_CANDIDATES
    if load_dotenv is None:
        ENV_CANDIDATES = candidate_env_paths()
        return None

    ENV_CANDIDATES = candidate_env_paths()
    for env_path in ENV_CANDIDATES:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return str(env_path)
    return None


def build_prompt(question: str, contexts: list[str]) -> str:
    """Build grounded QA prompt with retrieved contexts."""
    context_block = "\n\n".join(
        [f"[Context {idx + 1}]\n{ctx}" for idx, ctx in enumerate(contexts)]
    )
    return f"""
你是金融研究助理。请只基于提供的上下文回答问题，不要编造。
如果上下文没有足够信息，请明确回答“资料不足”。
请用中文回答，并在结尾加一句：仅用于学习交流，不构成投资建议。

问题：
{question}

可用上下文：
{context_block}
""".strip()


def answer_with_llm(prompt: str) -> str:
    """Call Gemini if API key exists; otherwise return fallback message."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        tried = ", ".join(str(p) for p in (ENV_CANDIDATES or candidate_env_paths()))
        return (
            "未检测到有效 `GEMINI_API_KEY`，已完成检索与提示词拼装，但暂时无法调用模型。\n"
            f"尝试读取的 `.env` 路径：{tried}"
        )

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    # Prefer SDK if available; otherwise call Gemini REST API directly.
    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text or "模型未返回文本。"
    except ImportError:
        pass

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_name}:generateContent?key={api_key}"
    )
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return f"模型返回结构未知：{data}"


def build_chunks(document: str, strategy: str) -> list[Chunk]:
    """Build chunks for retrieval: fixed-size window vs structure-aware sections."""
    if strategy == "fixed":
        return chunk_text(document, chunk_size=450, overlap=70)
    if strategy == "section":
        return chunk_by_section(document, max_chunk_size=600, overlap=70)
    raise ValueError(f"Unknown strategy: {strategy}")


def run_demo(question: str, *, strategy: str, top_k: int, dry_run: bool = False) -> None:
    """Run end-to-end local RAG pipeline for one chunking strategy."""
    load_environment()
    base_dir = Path(__file__).resolve().parents[2]
    sample_doc = base_dir / "data" / "raw" / "sample_10k.txt"

    document = load_text_file(sample_doc)
    chunks = build_chunks(document, strategy)
    retrieved = rank_chunks(question, chunks, top_k=top_k)
    contexts = [chunk.text for chunk, score in retrieved if score > 0]

    if not contexts:
        print("没有检索到相关片段，请换个更具体的问题。")
        return

    prompt = build_prompt(question, contexts)
    answer = "[Dry run] 已跳过 LLM 调用（仅检索与 Prompt 预览）。" if dry_run else answer_with_llm(prompt)

    print(f"\n--- Chunking: {strategy} | total_chunks={len(chunks)} | top_k={top_k} ---")
    print("\n=== Top Retrieved Chunks ===")
    for idx, (chunk, score) in enumerate(retrieved, start=1):
        sec = f" | section={chunk.section}" if chunk.section else ""
        print(f"{idx}. {chunk.chunk_id} | score={score:.4f}{sec}")
        print(chunk.text[:220].replace("\n", " ") + "...\n")

    print("=== Final Prompt (Preview) ===")
    print(prompt[:800] + "\n...")

    print("\n=== Answer ===")
    print(answer)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Topic 4 RAG demo: compare fixed-size vs section-based chunking."
    )
    parser.add_argument(
        "--strategy",
        choices=("fixed", "section", "both"),
        default="fixed",
        help="Chunking strategy: fixed window, section-aware, or run both for comparison.",
    )
    parser.add_argument(
        "--question",
        default="What are the main drivers of revenue growth and margin improvement?",
        help="User question for retrieval and QA.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of chunks to pass into the prompt.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip LLM call; compare chunking and retrieval only.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    strategies = ("fixed", "section") if args.strategy == "both" else (args.strategy,)
    for i, strat in enumerate(strategies):
        if args.strategy == "both" and i > 0:
            print("\n" + "=" * 72 + "\n")
        if args.strategy == "both":
            print(f"### EXPERIMENT RUN: strategy={strat!r} ###")
        run_demo(args.question, strategy=strat, top_k=args.top_k, dry_run=args.dry_run)

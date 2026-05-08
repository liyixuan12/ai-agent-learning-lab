"""Chunking and lightweight embedding utilities for Topic 4."""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Iterable


@dataclass
class Chunk:
    """One chunk of text with metadata."""

    chunk_id: str
    text: str
    start_char: int
    end_char: int
    section: str | None = None


# Titles used by `data/raw/sample_10k.txt` (structure-aware chunking demo).
DEFAULT_FINANCIAL_SECTION_TITLES: tuple[str, ...] = (
    "Business Overview",
    "Revenue and Growth",
    "Profitability",
    "Liquidity and Balance Sheet",
    "Risk Factors",
    "Management Discussion",
)


def _section_title_pattern(titles: tuple[str, ...]) -> re.Pattern[str]:
    inner = "|".join(re.escape(t) for t in titles)
    return re.compile(rf"(?m)^({inner})\s*$")


def _slug_section(title: str) -> str:
    return title.lower().replace(" ", "_")


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 80,
    *,
    base_offset: int = 0,
    chunk_id_prefix: str = "chunk",
) -> list[Chunk]:
    """Split text into overlapping fixed-size chunks.

    `base_offset` maps local indices into positions in a larger document (used when
    splitting a long section after structure-aware splitting).
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []
    start = 0
    idx = 0
    stride = chunk_size - overlap
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        block = text[start:end].strip()
        if block:
            chunks.append(
                Chunk(
                    chunk_id=f"{chunk_id_prefix}_{idx}",
                    text=block,
                    start_char=base_offset + start,
                    end_char=base_offset + end,
                )
            )
            idx += 1
        start += stride
    return chunks


def chunk_by_section(
    text: str,
    *,
    max_chunk_size: int = 600,
    overlap: int = 70,
    section_titles: tuple[str, ...] = DEFAULT_FINANCIAL_SECTION_TITLES,
) -> list[Chunk]:
    """Split by known section headings; long sections are re-split with `chunk_text`.

    If no section headings match, falls back to fixed-size `chunk_text` on the whole doc.
    """
    pattern = _section_title_pattern(section_titles)
    matches = list(pattern.finditer(text))
    if not matches:
        return chunk_text(text, chunk_size=max_chunk_size, overlap=overlap)

    chunks: list[Chunk] = []
    first_start = matches[0].start()
    if first_start > 0:
        preamble = text[:first_start].strip()
        if preamble:
            slug = "document_header"
            if len(preamble) <= max_chunk_size:
                chunks.append(
                    Chunk(
                        chunk_id=f"section_{slug}__0",
                        text=preamble,
                        start_char=0,
                        end_char=first_start,
                        section="Document Header",
                    )
                )
            else:
                sub = chunk_text(
                    preamble,
                    chunk_size=max_chunk_size,
                    overlap=overlap,
                    base_offset=0,
                    chunk_id_prefix=f"section_{slug}",
                )
                for c in sub:
                    chunks.append(
                        Chunk(
                            chunk_id=c.chunk_id,
                            text=c.text,
                            start_char=c.start_char,
                            end_char=c.end_char,
                            section="Document Header",
                        )
                    )

    for i, match in enumerate(matches):
        title = match.group(1)
        slug = _slug_section(title)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if not body:
            continue
        if len(body) <= max_chunk_size:
            chunks.append(
                Chunk(
                    chunk_id=f"section_{slug}__0",
                    text=body,
                    start_char=start,
                    end_char=end,
                    section=title,
                )
            )
        else:
            sub = chunk_text(
                body,
                chunk_size=max_chunk_size,
                overlap=overlap,
                base_offset=start,
                chunk_id_prefix=f"section_{slug}",
            )
            for c in sub:
                chunks.append(
                    Chunk(
                        chunk_id=c.chunk_id,
                        text=c.text,
                        start_char=c.start_char,
                        end_char=c.end_char,
                        section=title,
                    )
                )
    return chunks


def tokenize(text: str) -> list[str]:
    """A tiny tokenizer for demo retrieval."""
    return re.findall(r"[a-zA-Z0-9\u4e00-\u9fff]+", text.lower())


def embed_text(text: str) -> dict[str, float]:
    """Create a normalized sparse bag-of-words vector."""
    tokens = tokenize(text)
    if not tokens:
        return {}
    counts: dict[str, float] = {}
    for tk in tokens:
        counts[tk] = counts.get(tk, 0.0) + 1.0
    norm = math.sqrt(sum(v * v for v in counts.values()))
    if norm == 0:
        return counts
    return {k: v / norm for k, v in counts.items()}


def cosine_sim(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """Cosine similarity for sparse vectors."""
    if not vec_a or not vec_b:
        return 0.0
    if len(vec_a) > len(vec_b):
        vec_a, vec_b = vec_b, vec_a
    return sum(value * vec_b.get(token, 0.0) for token, value in vec_a.items())


def rank_chunks(query: str, chunks: Iterable[Chunk], top_k: int = 3) -> list[tuple[Chunk, float]]:
    """Rank chunks by cosine similarity to query."""
    query_vec = embed_text(query)
    scored: list[tuple[Chunk, float]] = []
    for chunk in chunks:
        score = cosine_sim(query_vec, embed_text(chunk.text))
        scored.append((chunk, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]

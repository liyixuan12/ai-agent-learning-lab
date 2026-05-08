"""Utilities for loading and normalizing raw financial documents."""

from __future__ import annotations

from pathlib import Path
import re


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph boundaries."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse repeated spaces/tabs but keep line breaks.
    text = re.sub(r"[ \t]+", " ", text)
    # Collapse many blank lines to at most two.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_text_file(file_path: str | Path) -> str:
    """Load plain-text financial document."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError(f"Unsupported text format: {path.suffix}")
    content = path.read_text(encoding="utf-8")
    return normalize_text(content)


if __name__ == "__main__":
    sample = Path(__file__).resolve().parents[2] / "data" / "raw" / "sample_10k.txt"
    text = load_text_file(sample)
    print(f"Loaded characters: {len(text)}")
    print("--- Preview ---")
    print(text[:500])

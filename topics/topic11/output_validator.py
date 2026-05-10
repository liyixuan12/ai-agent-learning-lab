#!/usr/bin/env python3
"""Topic 11: minimal output safety validator."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import List


REQUIRED_DISCLAIMER = "仅供教育与信息参考，不构成投资建议。"
DISALLOWED_PATTERNS = [
    r"你应该立刻买入",
    r"现在就买",
    r"我建议你全仓",
    r"稳赚不赔",
]
SOURCE_PATTERN = re.compile(r"\[[^\]]+\]")


@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]


def validate_output(text: str) -> ValidationResult:
    errors: List[str] = []

    if REQUIRED_DISCLAIMER not in text:
        errors.append("missing_disclaimer")

    if SOURCE_PATTERN.search(text) is None:
        errors.append("missing_source_citation")

    for pattern in DISALLOWED_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"disallowed_phrase:{pattern}")

    return ValidationResult(passed=len(errors) == 0, errors=errors)


def sample_output(sample_name: str) -> str:
    safe = (
        "基于公开信息，某公司近三年营收呈波动上行趋势，需关注现金流质量。[source]\n"
        "仅供教育与信息参考，不构成投资建议。"
    )
    unsafe = "你应该立刻买入这只股票，稳赚不赔。"

    if sample_name == "safe":
        return safe
    if sample_name == "unsafe":
        return unsafe
    raise ValueError(f"unknown sample: {sample_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate financial assistant outputs.")
    parser.add_argument(
        "--sample",
        choices=["safe", "unsafe"],
        help="Run validator on a built-in sample output.",
    )
    parser.add_argument(
        "--text",
        help="Validate custom text directly.",
    )
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.sample:
        text = sample_output(args.sample)
    else:
        parser.error("Provide --sample or --text.")

    result = validate_output(text)
    print(f"PASSED: {result.passed}")
    if result.errors:
        print("ERRORS:")
        for err in result.errors:
            print(f"- {err}")


if __name__ == "__main__":
    main()

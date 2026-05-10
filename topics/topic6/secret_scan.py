"""Topic 6 · 仓库密钥自查（教学级，不替代 gitleaks / trufflehog）。

跑法（在仓库根目录）：
    .venv/bin/python topics/topic6/secret_scan.py .

它做什么：
- 递归扫常见文本文件（默认 .py/.md/.yml/.yaml/.json/.toml/.txt 与 .env*）。
- 跳过 .git/、.venv/、node_modules/、__pycache__/、dist/、build/。
- 用启发式正则匹配常见 Key 形态。
- 命中后只打印「文件:行号」与该行片段（最多前 80 字符），不打印完整 Key。

注意：
- 占位符（如 your_gemini_api_key_here）也会命中，需要人工判断。
- 任何「真实泄漏」的第一步永远是去服务商控制台吊销。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SUSPICIOUS_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("OpenAI", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}")),
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub Token", re.compile(r"ghp_[A-Za-z0-9]{36,}")),
    ("Slack Token", re.compile(r"xox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("Generic Bearer", re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}")),
    ("Private Key Header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----")),
]

INCLUDE_SUFFIXES = {
    ".py", ".md", ".yml", ".yaml", ".json", ".toml", ".txt",
    ".ini", ".cfg", ".sh", ".env",
}
EXCLUDE_DIR_NAMES = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    "dist", "build", ".pytest_cache", ".mypy_cache",
}


def should_scan(path: Path) -> bool:
    if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
        return False
    if path.name.startswith(".env"):
        return True
    return path.suffix in INCLUDE_SUFFIXES


def _mask_match(value: str) -> str:
    """对匹配到的 secret 做脱敏：保留前 6 位，其余用 *** 代替。"""
    if len(value) <= 8:
        return value[:2] + "***"
    return value[:6] + "***"


def _redact_line(line: str, pat: re.Pattern[str]) -> str:
    """把一整行里所有匹配 pat 的子串替换为脱敏版本。"""
    return pat.sub(lambda m: _mask_match(m.group(0)), line)


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return hits
    for lineno, line in enumerate(content.splitlines(), start=1):
        for label, pat in SUSPICIOUS_PATTERNS:
            if pat.search(line):
                redacted = _redact_line(line.strip(), pat)[:80]
                hits.append((lineno, label, redacted))
                break
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Educational secret scanner.")
    parser.add_argument("root", nargs="?", default=".", help="Directory to scan.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Path does not exist: {root}")
        return 2

    total_files = 0
    total_hits = 0
    for path in root.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        total_files += 1
        hits = scan_file(path)
        if hits:
            rel = path.relative_to(root)
            for lineno, label, snippet in hits:
                total_hits += 1
                print(f"  [{label}] {rel}:{lineno}  →  {snippet}")

    print()
    print(f"Scanned {total_files} files. Hits: {total_hits}.")
    if total_hits == 0:
        print("OK：没有发现疑似密钥。继续保持。")
        return 0
    print("⚠️  请人工核查每条命中：")
    print("   - 占位符（your_xxx_here / example）可以忽略。")
    print("   - 真实 Key 立即去服务商吊销，再处理 Git 历史。")
    return 1


if __name__ == "__main__":
    sys.exit(main())

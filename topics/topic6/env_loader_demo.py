"""Topic 6 · 安全加载 .env 的最小演示。

跑法（在仓库根目录）：
    .venv/bin/python topics/topic6/env_loader_demo.py

学习点：
1. 不加载 .env 时拿不到 GEMINI_API_KEY，会触发 RuntimeError。
2. 用 python-dotenv 加载后，os.getenv 才能读到。
3. 打印时只显示前 6 个字符 + ***，演示「日志脱敏」。
4. 区分「程序需要的环境变量缺失」与「Key 真的不对」是两类不同错误。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REQUIRED_KEYS = ["GEMINI_API_KEY"]


def mask(value: str) -> str:
    """日志友好地脱敏：只露前 6 位。"""
    if not value:
        return "<empty>"
    if len(value) <= 8:
        return value[:2] + "***"
    return value[:6] + "***"


def show_env_state(label: str) -> None:
    print(f"\n[{label}]")
    for k in REQUIRED_KEYS:
        v = os.getenv(k)
        print(f"  {k} = {mask(v) if v else '<missing>'}")


def load_dotenv_safely() -> None:
    """优先用 python-dotenv；没装就退化为手动解析 .env。"""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
        print(f"\nLoaded via python-dotenv: {env_path}")
    except ImportError:
        if not env_path.exists():
            print(f"\n.env not found at {env_path}; nothing to load.")
            return
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())
        print(f"\nLoaded manually (dotenv missing): {env_path}")


def main() -> int:
    print("Step 1 — 在加载 .env 之前看看进程环境（可能为空）：")
    show_env_state("before load_dotenv")

    print("\nStep 2 — 调用 load_dotenv：")
    load_dotenv_safely()
    show_env_state("after load_dotenv")

    print("\nStep 3 — 校验必需变量是否齐全：")
    missing = [k for k in REQUIRED_KEYS if not os.getenv(k)]
    if missing:
        print(f"  ❌ 缺少: {missing}")
        print("     修复：复制 .env.example -> .env，并填入真实值。")
        return 1

    print("  ✅ 所有必需环境变量已就绪。")
    print("\n下一步建议：把这段 load_dotenv + 校验逻辑封装到 src/llm_client.py，")
    print("           让所有 Topic 的脚本共用同一个入口。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

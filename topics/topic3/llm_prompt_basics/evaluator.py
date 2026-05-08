"""Batch evaluation script for Topic 3 prompt quality checks."""

from run_company_analysis import analyze_company


SAMPLES = [
    {
        "name": "NVIDIA",
        "ticker": "NVDA",
        "sector": "Semiconductor",
        "revenue_growth": 0.35,
        "pe_ratio": 55,
        "debt_ratio": 0.25,
    },
    {
        "name": "Stable Utility Co",
        "ticker": "SUC",
        "sector": "Utilities",
        "revenue_growth": 0.04,
        "pe_ratio": 18,
        "debt_ratio": 0.55,
    },
    {
        "name": "High Debt Retail Inc",
        "ticker": "HDR",
        "sector": "Retail",
        "revenue_growth": -0.08,
        "pe_ratio": 12,
        "debt_ratio": 0.82,
    },
    {
        "name": "Cloud Growth Ltd",
        "ticker": "CGL",
        "sector": "Software",
        "revenue_growth": 0.27,
        "pe_ratio": 68,
        "debt_ratio": 0.20,
    },
    {
        "name": "Industrial Value Corp",
        "ticker": "IVC",
        "sector": "Industrials",
        "revenue_growth": 0.10,
        "pe_ratio": 14,
        "debt_ratio": 0.40,
    },
]


def main() -> None:
    total = len(SAMPLES)
    parse_success = 0
    disclaimer_hit = 0

    for sample in SAMPLES:
        try:
            result = analyze_company(sample)
            parse_success += 1
            if "不构成投资建议" in result.disclaimer:
                disclaimer_hit += 1
            print(f"[OK] {sample['ticker']} -> risk={result.risk_level}")
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {sample['ticker']} -> {exc}")

    parse_rate = parse_success / total if total else 0
    disclaimer_rate = disclaimer_hit / total if total else 0

    print("\n=== Evaluation Summary ===")
    print(f"Total samples: {total}")
    print(f"JSON parse success: {parse_success}/{total} ({parse_rate:.0%})")
    print(f"Disclaimer hit: {disclaimer_hit}/{total} ({disclaimer_rate:.0%})")


if __name__ == "__main__":
    main()

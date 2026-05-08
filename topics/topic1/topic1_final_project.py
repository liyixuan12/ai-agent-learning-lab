"""
Topic 1 Final Mini Project: Company Growth and Risk Analyzer
主题 1 最终小项目：公司增长与风险分析器
"""

companies = [
    {
        "name": "Apple",
        "ticker": "AAPL",
        "sector": "Technology",
        "revenue_growth": 0.08,
        "pe_ratio": 28,
        "debt_ratio": 0.35,
    },
    {
        "name": "NVIDIA",
        "ticker": "NVDA",
        "sector": "Semiconductor",
        "revenue_growth": 0.35,
        "pe_ratio": 55,
        "debt_ratio": 0.25,
    },
    {
        "name": "Tesla",
        "ticker": "TSLA",
        "sector": "Automotive",
        "revenue_growth": 0.18,
        "pe_ratio": 45,
        "debt_ratio": 0.65,
    },
]


def classify_growth(revenue_growth):
    if revenue_growth > 0.2:
        return "High growth"
    if revenue_growth >= 0.05:
        return "Moderate growth"
    return "Low growth"


def classify_risk(pe_ratio, debt_ratio):
    if pe_ratio > 40 and debt_ratio > 0.6:
        return "High risk"
    if pe_ratio > 40 or debt_ratio > 0.6:
        return "Medium risk"
    return "Low risk"


def generate_company_summary(company):
    growth_level = classify_growth(company["revenue_growth"])
    risk_level = classify_risk(company["pe_ratio"], company["debt_ratio"])

    return (
        f"{company['name']} ({company['ticker']}) is in {company['sector']} sector. "
        f"Growth: {growth_level}. Risk: {risk_level}."
    )


if __name__ == "__main__":
    for company in companies:
        print(generate_company_summary(company))

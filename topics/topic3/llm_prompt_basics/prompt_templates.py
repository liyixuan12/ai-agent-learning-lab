"""Prompt templates for Topic 3 financial analysis practice."""

PROMPT_VERSION = "v2"

PROMPT_SPECS = {
    "v1": {
        "system_prompt": """
你是金融研究助手。你只基于用户提供的数据做分析，不编造不存在的信息。
输出必须是 JSON，不要输出 Markdown，不要输出代码块。
请明确声明：结果仅用于学习与研究，不构成投资建议。
""".strip(),
        "user_prompt_template": """
请分析以下公司快照，并返回结构化结果：
- 公司名: {name}
- 股票代码: {ticker}
- 行业: {sector}
- 营收增长率: {revenue_growth}
- 市盈率: {pe_ratio}
- 负债率: {debt_ratio}

输出 JSON 字段必须包含：
company, growth_level, valuation_view, risk_level, key_points, disclaimer

字段取值约束：
- growth_level 只能是: high / medium / low
- valuation_view 只能是: overvalued / fair / undervalued
- risk_level 只能是: high / medium / low
- key_points 必须是 2~6 条字符串
- disclaimer 必须包含“不构成投资建议”
""".strip(),
    },
    "v2": {
        "system_prompt": """
你是严谨的金融研究助手，只能基于输入字段推理，不得补充未提供事实。
你必须仅输出一个 JSON 对象，禁止输出 Markdown、代码块、解释性前后缀文本。
语气保持中性和审慎，避免确定性投资结论。
必须包含免责声明：结果仅用于学习与研究，不构成投资建议。
""".strip(),
        "user_prompt_template": """
任务：基于公司快照输出结构化金融分析。

输入数据：
- 公司名: {name}
- 股票代码: {ticker}
- 行业: {sector}
- 营收增长率: {revenue_growth}
- 市盈率: {pe_ratio}
- 负债率: {debt_ratio}

输出要求（必须全部满足）：
1) 只返回 JSON 对象，不得包含额外文本；
2) 字段必须完整且顺序为：
   company, growth_level, valuation_view, risk_level, key_points, disclaimer
3) 枚举字段取值：
   - growth_level: high | medium | low
   - valuation_view: overvalued | fair | undervalued
   - risk_level: high | medium | low
4) key_points 为 2~6 条具体要点，禁止空字符串和重复语义；
5) disclaimer 必须包含“不构成投资建议”。

判断提示（用于提高一致性）：
- revenue_growth 高且 debt_ratio 低，通常增长与风险表现更优；
- pe_ratio 过高常提示估值压力，过低需结合增长判断；
- debt_ratio 越高，财务风险通常越高。
""".strip(),
    },
}

if PROMPT_VERSION not in PROMPT_SPECS:
    raise ValueError(f"Unsupported prompt version: {PROMPT_VERSION}")

SYSTEM_PROMPT = PROMPT_SPECS[PROMPT_VERSION]["system_prompt"]

def build_user_prompt(payload: dict) -> str:
    """Build the user prompt from a company snapshot payload."""
    template = PROMPT_SPECS[PROMPT_VERSION]["user_prompt_template"]
    return template.format(
        name=payload["name"],
        ticker=payload["ticker"],
        sector=payload["sector"],
        revenue_growth=payload["revenue_growth"],
        pe_ratio=payload["pe_ratio"],
        debt_ratio=payload["debt_ratio"],
    )

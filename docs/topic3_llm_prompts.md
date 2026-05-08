# Topic 3 LLM 与 Prompt Engineering 实战教学文档

本文档是 Topic 3 的完整动手教程，目标是让你从「会调用模型」进阶到「能稳定产出结构化金融分析结果」。

你将完成三件事：

- 从 Python 调用 LLM，形成可复用客户端。
- 设计高质量提示词模板（system + user + few-shot）。
- 让模型输出可解析 JSON，并建立基础评估方法。

---

## 1. 文档定位与学习顺序

| 顺序 | 材料 | 用途 |
|------|------|------|
| 1 | `docs/coding_study_roadmap.md` Topic 3 小节 | 理解本主题目标与检查项 |
| 2 | **本文** | 完整理论 + 代码实操 |
| 3 | `docs/topic4_rag_notes.md`（后续） | 把 Prompt 能力接到 RAG |

---

## 2. 学完后你应具备的能力

- 能独立完成 `LLM API -> Prompt -> JSON Output -> Python 解析` 全流程。
- 能写出可复用的金融分析提示词模板，并解释每段提示词的作用。
- 能识别并修复常见问题：幻觉、格式漂移、输出不完整、风险表述过度。
- 能对模型结果做最小可行评估（正确性、结构合规、可读性、免责声明）。

---

## 3. Topic 3 的核心概念

### 3.1 LLM 调用的最小闭环

一个可上线的最小闭环通常是：

1. 构造消息（system / user）。
2. 调用模型接口。
3. 获取文本或 JSON。
4. 校验输出结构。
5. 失败时重试或降级处理。

### 3.2 Prompt 的三层结构

- **System Prompt**：定义角色、边界、输出原则。
- **User Prompt**：本次任务输入（公司数据、问题、约束）。
- **Few-shot 示例（可选）**：给模型看 1-2 个样例，稳定风格与结构。

### 3.3 为什么金融场景要强调结构化输出

金融场景经常需要下游系统继续处理结果（API 返回、前端展示、数据库入库）。  
如果只返回自然语言段落，后续解析成本高且容易出错。  
因此 Topic 3 的主线是：**让模型说“人话”之前先产出“机器可读”结构。**

---

## 4. 目录建议（可直接照建）

```text
docs/
    topic3_llm_prompts.md
topics/topic3/llm_prompt_basics/
    requirements.txt
    .env.example
    prompt_templates.py
    llm_client.py
    run_company_analysis.py
    evaluator.py
```

---

## 5. 先决条件与环境准备

### 5.1 先决条件

- 已完成 Topic 1 与 Topic 2，理解公司分析字段（增长、估值、负债等）。
- 本地 Python 3.10+（建议）。
- 已有一个可用的 LLM API Key。

### 5.2 `requirements.txt` 示例

```txt
google-genai
python-dotenv
pydantic
```

### 5.3 `.env.example` 示例

```bash
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

> 注意：真实 `.env` 不要提交到 GitHub，记得在 `.gitignore` 中忽略。

---

## 6. Prompt 模板设计（金融分析版）

下面是一套可直接复用的模板思路。

### 6.1 System Prompt（角色与边界）

```text
你是金融研究助手。你只基于用户提供的数据做分析，不编造不存在的信息。
输出必须是 JSON，不要输出 Markdown，不要输出代码块。
你需要明确提示：结果仅用于学习与研究，不构成投资建议。
```

### 6.2 User Prompt（任务输入）

```text
请分析以下公司快照，并返回结构化结果：
- 公司名: {name}
- 股票代码: {ticker}
- 行业: {sector}
- 营收增长率: {revenue_growth}
- 市盈率: {pe_ratio}
- 负债率: {debt_ratio}

输出 JSON 字段必须包含：
company, growth_level, valuation_view, risk_level, key_points, disclaimer
```

### 6.3 Few-shot 示例（可选但推荐）

你可以额外给一个输入输出样例，帮助模型稳定字段名、语气和颗粒度。  
Few-shot 不宜太多，1-2 个通常就够。

---

## 7. Python 调用与结构化解析（核心实操）

### 7.1 `prompt_templates.py` 示例

```python
SYSTEM_PROMPT = """
你是金融研究助手。你只基于用户提供的数据做分析，不编造不存在的信息。
输出必须是 JSON，不要输出 Markdown，不要输出代码块。
请明确声明：结果仅用于学习与研究，不构成投资建议。
""".strip()


def build_user_prompt(payload: dict) -> str:
    return f"""
请分析以下公司快照，并返回结构化结果：
- 公司名: {payload["name"]}
- 股票代码: {payload["ticker"]}
- 行业: {payload["sector"]}
- 营收增长率: {payload["revenue_growth"]}
- 市盈率: {payload["pe_ratio"]}
- 负债率: {payload["debt_ratio"]}

输出 JSON 字段必须包含：
company, growth_level, valuation_view, risk_level, key_points, disclaimer
""".strip()
```

### 7.2 `llm_client.py` 示例

```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables.")
    return genai.Client(api_key=api_key)


def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
```

### 7.3 `run_company_analysis.py` 示例

```python
import json
from pydantic import BaseModel, Field
from llm_client import get_client, get_model_name
from prompt_templates import SYSTEM_PROMPT, build_user_prompt


class AnalysisResult(BaseModel):
    company: str = Field(...)
    growth_level: str = Field(...)
    valuation_view: str = Field(...)
    risk_level: str = Field(...)
    key_points: list[str] = Field(...)
    disclaimer: str = Field(...)


def analyze_company(payload: dict) -> AnalysisResult:
    client = get_client()
    model = get_model_name()
    prompt = f"{SYSTEM_PROMPT}\n\n{build_user_prompt(payload)}"

    resp = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    content = resp.text.strip()
    if content.startswith("```"):
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(content)
    return AnalysisResult.model_validate(data)


if __name__ == "__main__":
    sample = {
        "name": "NVIDIA",
        "ticker": "NVDA",
        "sector": "Semiconductor",
        "revenue_growth": 0.35,
        "pe_ratio": 55,
        "debt_ratio": 0.25,
    }
    result = analyze_company(sample)
    print(result.model_dump_json(indent=2, ensure_ascii=False))
```

---

## 8. 结果评估方法（Topic 3 最关键）

### 8.1 四维最小评估标准

每次迭代 Prompt 至少检查这 4 项：

1. **结构合规**：是否总能返回合法 JSON，字段齐全。
2. **任务正确性**：结论是否和输入数据逻辑一致（例如高 PE 不应总被说成低估）。
3. **可解释性**：`key_points` 是否具体，不空泛。
4. **安全边界**：是否包含“不构成投资建议”免责声明。

### 8.2 `evaluator.py` 简化思路

可以写一个小脚本，批量跑 5-10 组样本并统计：

- JSON 解析成功率
- 字段完整率
- 是否命中免责声明
- 人工主观评分（1-5）

---

## 9. 常见问题与解决策略

| 问题 | 典型表现 | 解决方式 |
|------|----------|----------|
| 输出不是 JSON | 返回自然语言段落或 Markdown | 在 system prompt 强调“仅 JSON”；降低温度；增加 few-shot |
| JSON 字段缺失 | 少 `disclaimer` 或 `key_points` | 在 user prompt 明确“字段必须包含”；加校验失败重试 |
| 结论不稳定 | 同输入多次输出差异很大 | 降低 `temperature`，固定模板和词汇 |
| 幻觉 | 编造未提供财务数据 | 明确“只基于输入字段，不可虚构” |
| 表述越界 | 给出确定性投资建议 | 强制加入免责声明 + 风险措辞模板 |

---

## 10. 与 Topic 2 / Topic 4 的衔接

### 10.1 接 Topic 2（FastAPI）

你可以把 `analyze_company()` 放到 Topic 2 的服务层，替代或补充规则模型，形成：

- `/analyze-company-rule`（规则版）
- `/analyze-company-llm`（LLM 版）

这样可以横向对比：可解释性、稳定性、成本、响应延迟。

### 10.2 接 Topic 4（RAG）

Topic 4 会把「用户输入」升级为「检索出的文档上下文 + 用户问题」。  
Prompt 结构不变，只是 user prompt 增加 `retrieved_context` 字段。

---

## 11. 完成检查表（可直接打勾）

- [ ] 我已能从 Python 成功调用 LLM API。
- [ ] 我已创建至少 1 套金融分析 Prompt 模板（system + user）。
- [ ] 我已实现 JSON 输出解析与 Pydantic 校验。
- [ ] 我已做过至少 5 组样本测试并记录结果。
- [ ] 我已在输出中加入“非投资建议”免责声明。
- [ ] 我已记录至少 2 次 Prompt 迭代及改进原因。

---

## 12. 反思模板（学习日志直接复用）

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my Financial AI Demo:
这对我的金融 AI Demo 的帮助是：

What prompt changes improved output the most:
哪次提示词改动提升最大：

Next improvement:
下一步改进：
```

---

## 12.5 Prompt 迭代记录（Version Log）

### v1（基线版）

- 目标：先实现最小可用闭环，确保模型能返回 JSON。
- 设计：仅包含角色约束、JSON 约束、字段名约束和免责声明要求。
- 已知问题：在部分样本上会出现字段漂移或枚举值不稳定（如输出 `moderate`）。

### v2（当前版）

- 迭代原因：提升结构稳定性与可评估性，减少 Pydantic 校验失败率。
- 关键改动：
  - 更强 system 约束：强调“只输出一个 JSON 对象、禁止前后缀文本”；
  - 明确字段顺序与枚举合法值，降低字段漂移；
  - 增加 `key_points` 质量要求（2~6 条、避免空字符串和重复语义）；
  - 增加启发式判断提示（增长/估值/负债），提高推理一致性。
- 预期收益：
  - JSON 解析成功率更高；
  - schema 校验失败（特别是枚举字段）更少；
  - 输出可读性与解释性更稳定。

> 代码中的版本入口：`topics/topic3/llm_prompt_basics/prompt_templates.py` 的 `PROMPT_VERSION`。

## 13. 一页速记（面试可讲）

- Topic 3 的本质是把「模型能力」变成「工程可用能力」。
- 工程可用的标准不是“看起来聪明”，而是“输出稳定、结构可解析、边界清楚”。
- Prompt 不是一次性写完，而是通过小样本评估持续迭代。
- 金融场景必须显式加入风险边界与免责声明。

---

**文档版本**：Topic 3 教学版 v1，可在你开始 Topic 4 时继续扩展为 `Prompt + RAG` 联合模板。

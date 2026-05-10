# Topic 9 — Agent 工作流设计实战

> 范围：本目录是 Topic 9 的实操区。目标是让你的金融 AI Demo 从「能调一次模型 + 能查一次文档」升级成「**一个能自己决定先做什么、再做什么、什么时候问人、出错怎么办的 Agent**」。
>
> 这是从 Topic 1–8 单点能力（Python / FastAPI / LLM / RAG / MCP）走向 **「Agent 系统设计」** 的关键一跃，也是 2025–2026 年 AI 应用工程岗最常被追问的部分：「**你的 Agent 出错了怎么办？怎么知道该调哪个工具？怎么不让它乱花钱 / 乱删数据？**」
>
> 本文件聚焦五件事：**1) Agent 工作流的最小心智模型；2) 何时规划、何时直接回答；3) 三层记忆怎么分；4) 在哪儿插人工确认（HITL）；5) 工具失败时怎么安全恢复。**

---

## 1. 学完这一节你应具备的能力

- 用一句话讲清楚「Agent 工作流」是什么、和「单次 LLM 调用」的本质区别。
- 写出一个简单的**路由策略（Router Policy）**：什么问题该直接回答、什么问题该走多步规划、什么问题该调工具。
- 设计**三层记忆**（会话短期 / 项目中期 / 持久长期），并知道每一层放什么、不放什么。
- 在高风险动作（删数据、发邮件、下单、跨账号写入、超额消费）前插入**人工确认（HITL）**门禁。
- 在工具超时 / 报错 / 返回空 / 返回幻觉时，按一份**失败恢复 Playbook** 选择「重试 / 回退 / 降级 / 放弃」。
- 在面试里能用 60 秒讲清楚「**你这个 Agent 出错了会怎么办**」。

---

## 2. 本目录结构

```text
topics/topic9/
├── README.md                # 本文件，完整教学
├── workflow_policy.py       # 可运行：路由 + 计划器 + 工具调度的最小实现
├── memory_store.py          # 可运行：三层记忆（session / project / durable）
├── hitl_rules.md            # 人工确认规则与示例对话
└── failure_recovery.md      # 失败处理 Playbook（超时 / 报错 / 空结果 / 幻觉）

# 复用仓库已有
src/financial_analyzer.py   # Topic 1 的规则型分析（被本主题包装成 tool）
src/rag_pipeline.py         # Topic 4 的检索（被本主题包装成 tool）
src/llm_client.py           # Topic 3 的 LLM 调用（被本主题用于回答）
topics/topic8/mcp_server_demo.py  # 可选：把本主题的 Agent 暴露成 MCP Server
```

> 与 Topic 7、Topic 8 一样，这里的 `*.py` 是「**最小可跑**」的范例：跑通后可以挪到 `src/agent/` 下作为最终项目的一部分，或被 Topic 8 的 MCP Server 复用。

---

## 3. Agent 工作流的最小心智模型

```text
                ┌─────────────────────────────┐
                │        User Query           │
                └──────────────┬──────────────┘
                               │
                       ┌───────▼────────┐
                       │  ROUTER 策略   │   ← 这一步在 §5 讲
                       │ direct ? plan ?│
                       └───────┬────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
        direct answer     plan + execute   refuse / clarify
              │                │
              │        ┌───────▼────────┐
              │        │  PLANNER       │   ← §6
              │        │ 拆 N 步动作    │
              │        └───────┬────────┘
              │                │
              │        ┌───────▼────────┐
              │        │  EXECUTOR      │   ← §7
              │        │ 调工具 + 记录  │
              │        └───────┬────────┘
              │                │
              │        ┌───────▼────────┐
              │        │  HITL 门禁     │   ← §9
              │        │ 高风险？让人审 │
              │        └───────┬────────┘
              │                │
              │        ┌───────▼────────┐
              │        │ FAILURE GUARD  │   ← §10
              │        │ retry/fallback │
              │        └───────┬────────┘
              │                │
              └────────────────┼────────────────┐
                               ▼                │
                       ┌────────────────┐       │
                       │   ANSWER + 引用│ ←─────┘
                       └────────────────┘
```

记住三件事：

1. **Agent 不是一个大模型，是一个有控制流的程序**。LLM 只是其中一个「可调用模块」；真正决定行为的是你写的策略。
2. **每一步都要可解释、可记录、可回放**。否则出问题没法 debug，更没法在面试里讲故事。
3. **质量 / 速度 / 成本三角永远在权衡**——多一次 plan、多一次 retrieve、多一次 retry 都意味着钱和延迟。设计就是选取舍。

---

## 4. 第 1 课 — 「单次 LLM 调用」 vs「Agent 工作流」

### 4.1 单次调用够用的时候，别上 Agent

| 你的需求 | 推荐 | 原因 |
|---|---|---|
| 「把这段话翻译成英文」 | **单次 LLM 调用** | 一次完成，没有外部依赖 |
| 「按这个 schema 抽取实体」 | **单次 LLM 调用 + JSON mode** | Topic 3 的范式 |
| 「读这份文档回答问题」 | **RAG（一次检索 + 一次生成）** | Topic 4 的范式 |
| 「用 Apple 的财报回答风险因子」 | **RAG，仍然不是 Agent** | 工具调用顺序固定，没有分支 |

> **判断标准**：如果整个流程的工具调用顺序是**写死的**，那就不需要 Agent，更不需要「让模型自己决定下一步」。

### 4.2 必须上 Agent 的时候

| 场景 | 为什么需要 Agent |
|---|---|
| 「分析 Apple，要参考最新财报，但用户没说哪一年」 | 需要先决策「查哪一年 → 查到了再总结」 |
| 「我要看 Top 5 风险因子，并和去年对比」 | 多步骤，且每步取决于上一步的结果 |
| 「回答金融问题，必要时引用文档；不必要时直接答」 | **要不要查文档**这件事本身就是决策 |
| 「执行一段操作，可能写文件 / 调 API / 花钱」 | 需要 HITL + 失败恢复 |

> **判断标准**：流程里有「**取决于上一步结果的分支**」「**可能要走 N 步也可能 1 步**」「**有副作用**」三者之一——上 Agent。

### 4.3 在本仓库 Demo 里的具体定位

```text
Topic 1–4：单点能力（Python / API / LLM / RAG）
Topic 5–7：工程基础（Git / 安全 / 容器）
Topic 8：把能力暴露成 MCP Tool（让 LLM 客户端能调）
Topic 9：写「调度大脑」     ← 本主题
        把 Topic 1 的规则分析、Topic 4 的检索、Topic 3 的 LLM
        组合成一个能自己决定流程的 Agent。
Topic 10：评测和观测「这个大脑做的对不对」
Topic 11：给这个大脑装护栏（防越界）
Topic 12：把它讲成产品
```

**Topic 9 的核心交付物 = 一份「这个 Demo 在背后是怎么决策的」的可解释、可运行说明**。

---

## 5. 第 2 课 — Router 策略：先决定要不要规划

最常见的初学者错误：**所有问题都让 LLM 先规划再执行**。结果是简单问题花 3 倍 token、3 倍时间，还更容易出错。

### 5.1 三档路由

```text
┌─────────────────────────────────────────────┐
│ ROUTE A：DIRECT_ANSWER（不调工具，直接答）   │
│   - 闲聊 / 解释概念 / 改写文本                │
│   - 例：「什么是 ROE？」                      │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ ROUTE B：SINGLE_TOOL（确定单工具，直接调）    │
│   - 已知要查文档 / 已知要算指标               │
│   - 例：「查 Apple 10-K 的 risk factors」     │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ ROUTE C：PLAN_AND_EXECUTE（多步规划）         │
│   - 多步骤、互相依赖、需要对比 / 汇总         │
│   - 例：「分析 Apple 最近 3 年风险演变趋势」  │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ ROUTE D：REFUSE / CLARIFY                    │
│   - 越界（投资建议）/ 信息不足                │
│   - 例：「我该买 Apple 吗？」                 │
└─────────────────────────────────────────────┘
```

### 5.2 怎么选路由（两种实现方式）

**方式 A：规则路由（轻量、可解释、推荐先用）**

```python
def route(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["should i buy", "我该买", "predict price"]):
        return "REFUSE"          # 投资建议红线，结合 Topic 11
    if any(k in q for k in ["compare", "trend", "演变", "对比", "近 3 年"]):
        return "PLAN"
    if any(k in q for k in ["10-k", "财报", "risk factor", "风险因子"]):
        return "SINGLE_TOOL"     # 直接走 retrieve_docs
    return "DIRECT"
```

**方式 B：LLM 路由（灵活、贵一些、产品成熟后用）**

让一个**便宜小模型**（gpt-4o-mini / Gemini Flash）只做一件事——返回 `{"route": "PLAN"}`。
注意：路由模型本身一定要 **JSON-only 输出**，否则你又给自己埋了个解析坑。

### 5.3 推荐做法（对你这个 Demo）

> 先写规则路由（10 行代码、零成本），跑 30 个 query 看错分多少；
> 错分超过 10% 再考虑切 LLM 路由。**绝对不要一上来就 LLM 路由**——你会调试到怀疑人生。

`workflow_policy.py` 里有完整可跑的规则路由实现。

---

## 6. 第 3 课 — Planner：多步任务怎么拆

### 6.1 一个好的 Plan 长什么样

不是一段散文，是一个**结构化的步骤列表**，每一步都包含：

```jsonc
{
  "step": 1,
  "intent": "查 Apple 2023 10-K 的风险因子段落",
  "tool": "retrieve_docs",
  "args": {"query": "Apple 2023 risk factors", "top_k": 5},
  "expects": "5 段相关文本，包含 'Risk Factors' 字样",
  "fallback_step": null
}
```

**为什么每一步都要写 `expects`？**——没有「期望」就没法判断「失败」，也就没法触发 §10 的恢复策略。

### 6.2 两种规划风格

| 风格 | 代表 | 适用场景 |
|---|---|---|
| **Plan-then-Execute（先规划完再执行）** | LangChain Plan-and-Execute、ReWOO | 多步、可并行、想省 token |
| **ReAct（边想边做，每步决定下一步）** | ReAct paper、Anthropic Tools loop | 不确定性高、依赖动态结果 |

**对你 Demo 的建议：先用 Plan-then-Execute**——它更可解释、更容易写测试（Topic 10 用得上）；ReAct 的灵活性等你有评测体系再上。

### 6.3 一个具体例子（金融场景）

> 用户：「**对比 Apple 和 Microsoft 最近 2 年风险因子的差异，我担心 AI 监管**」

```text
Plan:
  Step 1: retrieve_docs(query="Apple 2023 risk factors AI regulation", top_k=5)
  Step 2: retrieve_docs(query="Apple 2024 risk factors AI regulation", top_k=5)
  Step 3: retrieve_docs(query="Microsoft 2023 risk factors AI regulation", top_k=5)
  Step 4: retrieve_docs(query="Microsoft 2024 risk factors AI regulation", top_k=5)
  Step 5: llm_summarize(inputs=[step1..step4],
                       template="对比并指出 AI 监管相关风险演变")
  Step 6: append_disclaimer()           ← 复用 Topic 6 的免责声明
```

注意：**Step 1–4 是可以并发的**（它们之间没有数据依赖）。一个真实工程级 Agent 应当感知这一点。`workflow_policy.py` 提供了一个并发执行的最小实现。

### 6.4 什么时候 Planner 反而坏事

- **Plan 不准时**——LLM 拍脑袋拆出 5 步，结果第 1 步就走错。
  → 解法：**让 plan 先经过路由**——只有 ROUTE C 才进 plan。
- **Plan 比答案还长**——简单问题被强行 over-plan。
  → 解法：在 Planner 里加一条硬约束「步数 ≤ 3 才执行，否则退回 SINGLE_TOOL」。
- **Plan 自动展开成无限循环**——某一步失败 → 再 plan → 再失败。
  → 解法：**每个 plan 设最大重 plan 次数**（推荐 ≤ 2），超出直接降级到 §10 的「告诉用户做不到」。

---

## 7. 第 4 课 — Executor：调工具的工程细节

### 7.1 工具描述就是「给模型看的接口文档」

如果你做完 Topic 8（MCP），这件事已经做了一半——你的工具的 docstring + type hint 就是 schema。这里要强调几点 Topic 8 没讲透的：

- **每个工具都要写「什么时候用」+「什么时候不用」**。这一句决定了 LLM 80% 的工具选择行为。
- **参数命名要直白**。`q` 不如 `query`，`k` 不如 `top_k`，`year` 不如 `fiscal_year`。
- **返回值带 `source` 和 `confidence`**。便于上层判断要不要再 retry / fallback。

### 7.2 单步执行的最小骨架

```python
def execute_step(step: dict) -> dict:
    tool = TOOLS[step["tool"]]
    try:
        result = tool(**step["args"])
        return {"ok": True, "step": step, "result": result}
    except TimeoutError as e:
        return {"ok": False, "step": step, "error": "timeout", "raw": str(e)}
    except Exception as e:
        return {"ok": False, "step": step, "error": "exception", "raw": str(e)}
```

`workflow_policy.py` 里有完整版本，包括日志、trace_id 和耗时统计——这部分会直接喂给 Topic 10 的可观测性。

### 7.3 工具的「单一职责」

一个常见的反模式是写一个 `do_finance(action, **kwargs)` 大工具，让 LLM 自己拼 action。**别这样**：

- LLM 用得很差（参数空间太大）
- 测不动（每个 action 都要单独单测）
- HITL 门禁也难写（无法按工具粒度限制）

**正确做法**：每个动作一个工具——`retrieve_docs`、`analyze_company`、`compute_growth_rate`、`generate_report`。粒度大致相当于 Topic 8 里你愿意 `@mcp.tool()` 的颗粒度。

---

## 8. 第 5 课 — 三层记忆：什么放短期，什么放持久

```text
┌───────────────────────────────────┐
│  L1：Session（会话内）             │  生命期：一次对话
│   - 当前 query 的中间结果           │  存储：内存 dict / list
│   - 最近 N 轮对话                  │  示例：上一步 retrieve 的 chunks
└───────────────────────────────────┘
┌───────────────────────────────────┐
│  L2：Project（项目内）             │  生命期：本次任务/项目
│   - 用户偏好（关注哪些公司）        │  存储：本地 JSON / SQLite
│   - 已经分析过的公司缓存            │  示例：分析过的 Apple 报告摘要
└───────────────────────────────────┘
┌───────────────────────────────────┐
│  L3：Durable（持久 / 跨会话）       │  生命期：永久（直到删除）
│   - RAG 向量库本身                 │  存储：Chroma / FAISS
│   - 训练事实 / 公司主数据           │  示例：所有公司基本信息表
└───────────────────────────────────┘
```

### 8.1 三层各自的「使用纪律」

| 层 | 该放 | **不该放** |
|---|---|---|
| L1 Session | 中间结果、当前对话上下文 | 用户密码、长期偏好 |
| L2 Project | 用户偏好、已分析缓存、自定义 prompt | 大型语料、模型权重 |
| L3 Durable | 向量库、公司主数据、审计日志 | 临时聊天、未脱敏的用户原话 |

### 8.2 为什么必须分层

- **不分层 → 全塞进 LLM context** → 每次对话都贵一倍、慢一倍、还容易爆窗口。
- **不分层 → 全持久化** → 用户聊天里的随口一句被永久保存，**Topic 6 / Topic 11 的隐私护栏会被一锤打穿**。
- **不分层 → 全 in-memory** → 进程重启全没了，第二天用户问「上次我们聊到哪儿了」直接歇菜。

### 8.3 一个具体例子

> 用户：「**记住我重点关注 Apple 和 Microsoft，以后默认就分析它俩**」

| 应该写到哪 | 内容 |
|---|---|
| L2 Project | `{"watchlist": ["AAPL", "MSFT"]}` |
| L1 Session | 「用户刚刚说了 watchlist，记得本轮回答也用上」 |
| ❌ L3 Durable | 不用，这是用户偏好不是世界事实 |

`memory_store.py` 提供这三层的最小实现（dict + JSON + SQLite stub），你可以直接拿去拼到最终 Demo 里。

---

## 9. 第 6 课 — Human-in-the-Loop（HITL）：在哪儿插确认门

> 一句话：**只要这一步出错会让用户损失（钱、数据、声誉、合规），就必须让人按一下「Approve」**。

### 9.1 在金融 Demo 里的高风险动作清单

| 动作 | 默认要求 |
|---|---|
| 删除任何用户数据 | ✅ 必须确认 |
| 调用收费 API（OpenAI / 数据源）超过预算阈值 | ✅ 必须确认 |
| 把分析结果发给第三方（邮件、Slack、Webhook） | ✅ 必须确认 |
| 写入向量库 / 数据库 | ⚠️ 默认确认，可配置免确认 |
| 调用「分析」「检索」类只读工具 | ❌ 不需要确认 |
| 在本地写入临时文件 | ❌ 不需要确认（但要记录） |

### 9.2 HITL 在工作流里的位置

```text
EXECUTOR ──► 检查 step.tool 是否在 RISKY_TOOLS
                │
                ├─ 否 ──► 直接执行
                └─ 是 ──► 暂停，输出
                          "我准备调用 X(args=Y)，是否继续？(y/n)"
                          ↓
                        用户输入
                          ↓
                        y → 执行
                        n → 中止 + 记录拒绝原因
```

详细规则、降级策略、拒绝后怎么继续流程，写在 `hitl_rules.md` 里。

### 9.3 关键设计决策

- **白名单 vs 黑名单**：高风险用**白名单**——「只有列出的工具才会触发 HITL」对人类好读；新增工具时**默认算高风险**最安全。
- **批准粒度**：`tool + args` 一起批，不要只批 tool 名（不然 LLM 改个参数就绕过去了）。
- **批准时效**：批准后 60 秒内有效，过期需重批。**绝不**「永久批准这个工具」——那等于没有 HITL。
- **离线 / CI 模式**：在自动化测试里 HITL 必须**默认拒绝**，否则一个失控的脚本就能把生产数据删光。

---

## 10. 第 7 课 — 工具失败：超时 / 报错 / 空结果 / 幻觉

### 10.1 失败有几种？

```text
┌─────────────┬────────────────────────┬──────────────────────────────┐
│   失败类型  │       症状             │       默认处理               │
├─────────────┼────────────────────────┼──────────────────────────────┤
│ Timeout     │ 超过预算时间没返回     │ 重试 1 次（backoff），再失败→降级 │
│ Exception   │ 抛错（网络/解析/401）  │ 区分可恢复 vs 不可恢复       │
│ Empty       │ 返回空 list / null     │ 改 query 再试 1 次，再空→告知用户 │
│ Hallucinated│ 返回看起来对但是错的   │ 加引用校验 / cross-check     │
└─────────────┴────────────────────────┴──────────────────────────────┘
```

### 10.2 一张「重试 / 回退 / 降级 / 放弃」决策表

| 情况 | 重试 | 回退到另一工具 | 降级回答 | 放弃并告知 |
|---|---|---|---|---|
| 单次 timeout | ✅ ≤2 次 | ❌ | ❌ | ❌ |
| 连续 timeout | ❌ | ✅（缓存 / 备用 API） | ✅ | ❌ |
| 401 / 鉴权错 | ❌ | ❌ | ❌ | ✅（让用户检查 key） |
| 4xx 参数错 | ❌（重写 args 后才能重试） | ❌ | ❌ | ✅（让 LLM 改 plan） |
| 5xx 服务端错 | ✅ ≤2 次（带 jitter） | ✅ | ✅ | ❌ |
| 检索为空 | ✅ ≤1 次（改 query） | ❌ | ✅（说"未找到，仅基于公开信息回答"） | ❌ |
| 检索结果不相关 | ❌ | ❌ | ✅ | ❌ |
| 输出疑似幻觉 | ❌ | ✅（加引用校验工具） | ✅（带"可能不准确"） | ❌ |

完整 Playbook 在 `failure_recovery.md`，每条都附了示例对话。

### 10.3 三个不要踩的坑

- ❌ **无限重试**：永远要有上限。`retries = 2` 通常够；超过就降级。
- ❌ **静默吞错**：错误必须**进 trace**，否则 Topic 10 评测时根本看不到「Agent 其实坏了」。
- ❌ **回退到更危险的工具**：失败回退路径必须**安全等级 ≤ 原工具**。例如不要因为「`retrieve_docs` 没结果」就回退到「让 LLM 凭记忆瞎答」——那是把幻觉伪装成回答，更糟。

---

## 11. 第 8 课 — 把这一切串起来跑一次

打开两个文件配合看：

1. **`workflow_policy.py`** — 一个能跑的迷你 Agent。包含：
   - 规则版 Router
   - 一个简单的 Planner（基于关键词的 stub，可以换 LLM）
   - 同步 + 并发两种 Executor
   - HITL hook（只在高风险工具触发）
   - 重试 / 回退装饰器

2. **`memory_store.py`** — 三层记忆的最小实现：
   - L1：Python `list`/`dict`
   - L2：JSON 文件持久化（`./.topic9/project_memory.json`）
   - L3：stub 接口，留好 ChromaDB / SQLite 接入点

跑一下：

```bash
python topics/topic9/workflow_policy.py
```

预期会看到三种路由各跑一遍：

```text
[ROUTE=DIRECT]  Q: 什么是 ROE
                A: ROE 是 ...

[ROUTE=SINGLE]  Q: 帮我查 Apple 10-K 的风险因子
                Plan: [retrieve_docs]
                Result: [...] (来自 Topic 4 的 retrieve_stub)

[ROUTE=PLAN]    Q: 对比 Apple 和 Microsoft 近 2 年风险演变
                Plan: [retrieve_docs x4, llm_summarize, append_disclaimer]
                Step 1: ok (...)
                Step 2: ok (...)
                ...

[ROUTE=REFUSE]  Q: 我该买 Apple 吗
                A: 抱歉，本工具不提供个性化投资建议。(结合 Topic 11)
```

---

## 12. 注意事项 / 常见坑

### 12.1 设计层面

- **工作流是程序，不是 prompt**。你写代码控制流程；LLM 只在你明确指定的步骤参与。「让 LLM 自己想」的部分越少，越好 debug、越省钱。
- **每一步都要可观测**。trace_id、耗时、输入输出、是否 HITL、最终是否成功——这些数据是 Topic 10 的输入。
- **失败比成功更值得测**。别只测 happy path——超时、空结果、幻觉、HITL 拒绝，都要有用例。
- **Plan 不一定要由 LLM 出**。**很多任务规则就够了**——硬编码的 plan 比 LLM 生成的 plan 稳定 10 倍，且免费。

### 12.2 安全（结合 Topic 6 / Topic 11）

- HITL 必须前置，**不要事后补救**——「先调了再问要不要继续」是最危险的反模式。
- 工具白名单 vs 黑名单：**用白名单**。新增工具默认禁用，需要显式 enable。
- 不要把用户原话原封不动塞进系统 prompt——它**就是**注入向量（Topic 11 详谈）。

### 12.3 工程

- **trace 用 JSON 行格式（jsonl）落盘**，每行一个 step，便于 grep / pandas 分析。
- **Plan 也要落盘**——你想看一周后某个 query 当时的 plan 是什么，没记录就完了。
- **资源池有上限**：并发执行听起来美好，但同时 10 个 retrieve 把你的 API 配额烧完不到 1 分钟。**每个工具单独限流**。

### 12.4 LLM 行为

- **模型的「计划质量」会随版本漂移**——你今天调好的 prompt，明天换模型可能就 plan 偏了。**这就是 Topic 10 golden set 存在的理由**。
- **路由错分不可怕，错得可解释才可怕**——保证每个 query 都有 trace 写明「为什么走了这条路由」，而不是「LLM 自己决定的」。
- **不要让 Agent 在长会话里「越聊越自由」**。每个新 query 都重新走一次 Router——别让上轮的高权限延续。

---

## 13. 推荐练习（按顺序做）

1. **跑通 `workflow_policy.py`**

   不改任何代码，先跑一遍看四种路由分别是什么样。理解每条 trace 行的意思。

2. **加一种新路由**

   在 Router 里加一种 `COMPARE_COMPANIES`（多公司对比），并写出对应的 plan 模板。跑 5 个例子。

3. **接入真 RAG**

   把 `retrieve_docs` 从 stub 换成 Topic 4 的真实实现。验证 ROUTE B / C 都能拿到真片段。

4. **设计 1 条 HITL 规则**

   在 `hitl_rules.md` 选一条写完整：动作、阈值、UI 提示词、批准时效、被拒绝后的降级路径。

5. **故意制造 3 种失败**

   - 让 `retrieve_docs` 抛 timeout（time.sleep + 抛异常）
   - 让它返回空 list
   - 让 LLM 输出明显的幻觉（hardcode 一个错答案）

   按 `failure_recovery.md` 的策略验证 Agent 的恢复行为。

6. **写一段 60 秒的「我的 Agent 怎么决策」**（选做，面试用）

   面试很常被问「你为什么用 plan-and-execute 不用 ReAct」「你的 Agent 出错了怎么办」。先在 README 写下答案，临场就不会卡。

7. **可选：把 Agent 暴露成 MCP Tool**

   在 Topic 8 的 `mcp_server_demo.py` 里加一个 `@mcp.tool() def ask_agent(query: str)`，内部调本 Agent。这样 Cursor 一句话就能触发整个工作流——一份 Agent 多家客户端复用。

---

## 14. 升级路线（Topic 9 → Topic 9+）

- **Plan-and-Execute → ReAct**：当 query 不确定性变大、依赖动态外部状态时，切到 ReAct 风格。但前提是 Topic 10 评测体系已经搭好。
- **Multi-Agent**：把单 Agent 拆成 Researcher / Analyst / Critic 多个角色，各自有自己的 system prompt 和工具集。**不要在评测体系建立前做这件事**——bug 难 debug 10 倍。
- **状态机化**：用 LangGraph / 自己实现的小 state machine 把工作流写死成图。比纯函数式更易测、更易可视化。
- **持久任务**：把长任务（5 分钟以上）拆成 step，存进队列；用户可以离开再回来看。
- **Cost & Latency Budget**：每个 query 设全局预算（如 「最多花 0.05 美元、20 秒」），超了直接降级。这是产品级 Agent 的硬要求。

---

## 15. 自测检查表

- [ ] 我能用一句话讲清楚「Agent 工作流」和「单次 LLM 调用」的区别。
- [ ] 我能解释什么时候不需要 Agent（流程写死即可）。
- [ ] 我实现了至少 3 条规则路由，并能解释每条的取舍。
- [ ] 我写了一个 plan-and-execute 的 Planner，限制了最大步数。
- [ ] 我能区分 L1/L2/L3 三层记忆，每层各举 1 个该放和不该放的例子。
- [ ] 我至少在一个高风险工具前实现了 HITL 检查点。
- [ ] 我对至少 3 种工具失败模式有明确的恢复策略。
- [ ] 每一步执行都进了 trace（jsonl 落盘 / 控制台打印）。
- [ ] 我没有让任何「失败回退」走到比原步骤更危险的路径上去。
- [ ] 我能在 60 秒内讲清楚「这个 Agent 出错了会怎么办」。

---

## 16. 反思模板

```text
What workflow decisions worked well:
哪些工作流决策效果最好：

Where the agent made wrong tool choices:
Agent 在工具选择上哪里出错了：

How human-in-the-loop improved safety:
人工介入如何提升了安全性：

What failure mode surprised me the most:
最让我意外的失败模式是哪种：

Next improvement:
下一步改进：
```

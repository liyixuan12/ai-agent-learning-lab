# Topic 8 — MCP（Model Context Protocol）实战 [可选 / 加分项]

> 范围：本目录是 Topic 8 的实操区。目标是让你的金融 AI Demo 不只是「自己一个 FastAPI 接口」，而是**把分析能力暴露成一种 Cursor / Claude Desktop / 其他 LLM 客户端可以直接调用的标准化「工具」**。
>
> 这是 Roadmap 里的可选主题，不影响 Demo 跑通；但在 2025–2026 年 AI 应用工程师面试里，**「你了解 MCP 吗？写过 MCP Server 吗？」是高频问题**。会一点点就足以拉开差距。
>
> 本文件聚焦四件事：**1) MCP 是什么、解决什么问题；2) 什么时候应该用、什么时候不该用；3) 怎么把现有 `src/` 里的金融分析 / RAG 检索包装成 MCP Tool；4) 怎么在 Cursor 里接进来。**

---

## 1. 学完这一节你应具备的能力

- 用一句话讲清楚 MCP 是什么，以及它和「直接调 OpenAI / Gemini Function Calling」「直接调 FastAPI 接口」的区别。
- 区分 MCP 的三类核心能力：**Tools（让模型调函数）/ Resources（让模型读数据）/ Prompts（可复用提示词模板）**。
- 用 Python `mcp` SDK 写一个最小 MCP Server，把 `src/financial_analyzer.py` 暴露成一个 Tool。
- 把 Topic 4 的 RAG 检索流水线（`src/rag_pipeline.py`）包装成第二个 Tool，让 Claude / Cursor 能「自己决定要不要查文档」。
- 在 Cursor 或 Claude Desktop 里加一条 MCP 配置，调用你写的 Server。
- 判断一个新需求该用 **MCP** 还是用 **REST API（FastAPI）** 还是用 **直接 Function Calling**。

---

## 2. 本目录结构

```text
topics/topic8/
├── README.md                       # 本文件，完整教学
├── mcp_server_demo.py              # 最小 MCP Server：暴露 analyze_company / retrieve_docs
├── mcp_client_demo.py              # 用 Python 客户端调用自己写的 Server（验证用）
└── cursor_mcp_config.example.json  # Cursor / Claude Desktop 的 MCP 配置范例

# 复用仓库已有
src/financial_analyzer.py          # 已有：规则型公司分析
src/rag_pipeline.py                # 已有：RAG 检索（Topic 4）
src/llm_client.py                  # 已有：LLM 调用（Topic 3）
```

> 与 Topic 7 一样，本目录的 `*.example.json` / `*_demo.py` 都是范例，跑通后可以挪到仓库根的 `mcp/` 目录或合并进 `src/`。

---

## 3. MCP 的最小心智模型

```text
       ┌──────────────────────┐
       │   LLM Host / Client  │   ←  Cursor / Claude Desktop / 你写的 Agent
       │  (Claude / GPT / …)  │
       └──────────┬───────────┘
                  │ MCP 协议 (JSON-RPC over stdio / HTTP / SSE)
        ┌─────────┴──────────┐
        ▼                    ▼
┌────────────────┐    ┌────────────────┐
│  MCP Server A  │    │  MCP Server B  │   ←  你写的 / 别人写的
│ (你的金融工具) │    │ (filesystem)   │
└───────┬────────┘    └───────┬────────┘
        │                     │
        ▼                     ▼
   你的 src/, RAG       本地文件系统
```

记住三件事：

1. **MCP 是「LLM 客户端 ↔ 工具服务端」之间的标准协议**。不是模型，不是 API 框架，是协议（类比 LSP 之于编辑器、USB 之于设备）。
2. **Server 提供能力，Host 决定何时调用**。你只负责写「这是什么工具、参数是什么、做什么」；要不要调由 LLM 在对话中自己决定。
3. **一份 Server 可以被 N 个 Host 复用**。你给 Demo 写的 MCP Server，今天 Cursor 用它写代码，明天 Claude Desktop 用它做问答，后天你自己的 Agent 用它跑分析——**写一次，到处用**。

---

## 4. 第 1 课 — MCP 到底是什么、解决了什么问题

### 4.1 一句话定义

> **MCP（Model Context Protocol）是 Anthropic 在 2024 年底开源的一个协议，规定「LLM 应用如何以标准化方式访问外部工具与数据源」。**

类比：

| 类比 | 含义 |
|---|---|
| LSP（Language Server Protocol） | 让任何编辑器都能用同一个语言服务（Pylance、rust-analyzer） |
| USB-C | 让任何笔记本都能接同一个充电器、显示器 |
| **MCP** | **让任何 LLM 应用都能接同一份「工具/数据源」** |

### 4.2 没有 MCP 之前我们怎么做？

通常是这三种之一，每一种都有痛点：

```text
方案 A：直接在 Prompt 里塞数据
  痛：上下文窗口有限；数据多了模型抓不准；每次都要重新塞。

方案 B：用 OpenAI / Gemini 的 Function Calling
  痛：每家厂商 schema 不一样；切换模型要重写工具定义；
       工具是写死在你的 Agent 代码里，别人复用不了。

方案 C：自己起 FastAPI 接口给 Agent 调
  痛：你得自己写鉴权、自己定 schema、自己处理流式；
       而且每接入一个新 Host（Cursor / Claude / 你自己的 UI）
       都要写一份「胶水代码」把工具描述告诉 LLM。
```

### 4.3 MCP 把这件事标准化

写一个 MCP Server，**自动**得到下面这些好处：

- 工具的「名字、描述、参数 schema」用 JSON-RPC 标准方式暴露 → 任何 MCP Host 都能发现。
- Cursor、Claude Desktop、Continue、Cline 都能直接接入，不用为每家写一遍。
- 同一个 Server 可以同时跑在「stdio 模式」（本地子进程）和「HTTP/SSE 模式」（远程服务）。
- 已经有大量现成 Server 可以复用（filesystem / git / postgres / slack / github / chromadb …），生态在快速膨胀。

### 4.4 协议本身长什么样（看一眼就行）

底层是 **JSON-RPC 2.0**。Host 启动 Server 后，会先握手：

```jsonc
// Host → Server
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {...}}

// Server → Host：我支持哪些能力
{"jsonrpc": "2.0", "id": 1, "result": {"capabilities": {"tools": {}, "resources": {}}}}

// Host → Server：把你的工具列出来
{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

// Server → Host
{"jsonrpc": "2.0", "id": 2, "result": {"tools": [
  {"name": "analyze_company", "description": "...", "inputSchema": {...}}
]}}

// 模型决定调用 → Host → Server
{"jsonrpc": "2.0", "id": 3, "method": "tools/call",
 "params": {"name": "analyze_company", "arguments": {"name": "Apple"}}}
```

**好消息**：你**永远不用手写**这些 JSON——Python SDK 全帮你封装好。下面就开始写真东西。

---

## 5. 第 2 课 — 什么时候应该用 MCP，什么时候不该用（重点）

这一节是这一章最重要的部分。**MCP 不是万能锤**，用错地方会让项目变复杂。

### 5.1 什么时候**应该**用 MCP

| 场景 | 为什么 MCP 合适 |
|---|---|
| 你想让 **Cursor / Claude Desktop / 别人的 Agent** 调用你的工具 | 这本来就是 MCP 的设计目标——一份 Server 多家客户端复用 |
| 工具是**只服务于 LLM 的内部能力**（不直接给最终用户） | 不需要 REST 那种「公开接口」，stdio 的 MCP 最简单 |
| 你想给 LLM 一个「**可发现、自描述**」的工具集合 | MCP 的 `tools/list` 自带 schema，模型能自己看懂 |
| 多个工具要**共享同一个鉴权 / 状态 / 数据库连接** | MCP Server 是长进程，可以维护这些，比无状态 REST 更方便 |
| 你在做**金融研究助手 Agent**，希望它能「自己判断什么时候查 RAG、什么时候算财务指标」 | 这正是本仓库 Demo 的形态，详见 §7、§8 的例子 |

### 5.2 什么时候**不该**用 MCP（直接用别的更省事）

| 场景 | 推荐方案 | 原因 |
|---|---|---|
| 给前端 / Streamlit / 移动 App 用 | **FastAPI（Topic 2）** | MCP 不是给最终用户的；浏览器不会说 MCP |
| 接 webhook / 第三方回调 | **FastAPI** | 第三方不会用 MCP 协议来推消息 |
| 你只想「让一次性脚本调用 GPT」 | **直接调 SDK（Topic 3）** | 加 MCP 反而是过度工程 |
| 你只在**一个固定 Agent**里用，永远不复用 | **OpenAI / Gemini Function Calling** | 厂商原生工具更直接，少一层协议 |
| 工具是「公开 SaaS 接口」要给陌生开发者 | **REST + OpenAPI** | 生态成熟、有鉴权 / 限流标准 |

### 5.3 一张决策表（拿不准的时候看这张）

```text
我要把这个能力暴露给「谁」？
│
├─ 浏览器 / 移动端 / 第三方开发者
│       └─►  REST API (FastAPI)，写 OpenAPI 文档
│
├─ 我自己的一个 Agent 脚本
│       └─►  直接调函数；最多用厂商 Function Calling
│
└─ 多个 LLM 客户端（Cursor + Claude Desktop + 我的 Agent）
        └─►  ✅ MCP Server
```

> **一个特别值得记住的判断**：如果你发现自己在不同 Agent 项目里**反复写「告诉 LLM 这是什么工具」的胶水**——那就是 MCP 该出场的时候。

### 5.4 在本仓库 Demo 里的具体定位

```text
            ┌─ FastAPI (Topic 2) ──── 给 Streamlit UI 和外部用户  ✅ 保留
本仓库代码 ─┤
            └─ MCP Server (Topic 8) ─ 给 Cursor / Claude Desktop / 我自己的 Agent  ✅ 新增

  共用：src/financial_analyzer.py、src/rag_pipeline.py、src/llm_client.py
```

**两层并存、共用底层 `src/`**。这是真实工程里非常常见的形态——同一份业务逻辑，用 REST 服务最终用户，用 MCP 服务 LLM 客户端。

---

## 6. 第 3 课 — MCP 的三个核心能力：Tools / Resources / Prompts

| 能力 | 一句话 | 类比 | 在金融 Demo 里的例子 |
|---|---|---|---|
| **Tools** | 让 LLM **执行** 一个有副作用 / 计算的函数 | 「动作」 | `analyze_company(name)`、`retrieve_docs(query, top_k)` |
| **Resources** | 让 LLM **读取** 一份数据（只读、可寻址） | 「文件」 | `data/raw/sample_10k.txt`、某公司的财报全文 |
| **Prompts** | 提供**可复用的提示词模板** | 「样板信」 | 「财报摘要」「风险因子提取」标准 Prompt（来自 Topic 3） |

记忆口诀：**Tool 是动词，Resource 是名词，Prompt 是模板**。

### Resources vs Tools 的边界（容易混）

- **能用 URI 寻址、读了就完事 → Resource**。
  例：`finsight://company/AAPL/10k_2024` 返回一份文本。
- **要做计算、有参数、可能有副作用 → Tool**。
  例：`analyze_company(name="AAPL", year=2024)` 返回结构化分析。

> 拿不准？写成 **Tool** 永远不会错；Resource 只是 Tool 的一个特例。

---

## 7. 第 4 课 — 写第一个 MCP Server：把 `analyze_company_stub` 暴露出去

我们要把仓库已有的 `src/financial_analyzer.py` 包装成一个 MCP Tool。这就是**最具体的例子 #1**。

### 7.1 安装依赖

```bash
pip install "mcp[cli]>=1.0"
```

> 也可以加进 `requirements.txt`：
>
> ```text
> # Topic 8 / MCP (optional)
> mcp[cli]>=1.0
> ```

### 7.2 写 Server（`topics/topic8/mcp_server_demo.py`）

```python
"""最小 MCP Server：把 src/ 里的金融能力暴露成 Tool。

跑法（stdio 模式，给 Cursor / Claude Desktop 用）：
    python topics/topic8/mcp_server_demo.py

跑法（开发调试 + 浏览器 Inspector）：
    mcp dev topics/topic8/mcp_server_demo.py
"""

from mcp.server.fastmcp import FastMCP

from src.financial_analyzer import analyze_company_stub
from src.rag_pipeline import retrieve_stub

mcp = FastMCP("finsight-ai")


@mcp.tool()
def analyze_company(name: str) -> dict:
    """对一家公司做规则型基础分析。

    Args:
        name: 公司名（如 "Apple"、"NVIDIA"）。

    Returns:
        包含公司名与初步状态的字典。后续会接入真实财务指标。
    """
    return analyze_company_stub(name)


@mcp.tool()
def retrieve_docs(query: str, top_k: int = 3) -> list[str]:
    """在已索引的金融文档里检索与 query 最相关的若干段落。

    Args:
        query: 用户的自然语言问题。
        top_k: 返回多少个片段（默认 3）。
    """
    chunks = retrieve_stub(query)
    return chunks[:top_k]


@mcp.resource("finsight://disclaimer")
def disclaimer() -> str:
    """金融免责声明（来自 Topic 6）。任何调用方都应当显式展示。"""
    return (
        "本工具仅用于学习与研究目的，不构成任何投资建议。"
        "数据可能过时或不准确，请以官方披露为准。"
    )


if __name__ == "__main__":
    mcp.run()
```

读这段代码的关键点：

| 元素 | 作用 |
|---|---|
| `FastMCP("finsight-ai")` | 创建 Server，名字会显示在 Cursor/Claude 的工具面板里 |
| `@mcp.tool()` | 把一个普通 Python 函数注册为 Tool |
| **函数的 docstring 和类型注解** | **就是 LLM 看到的工具描述和参数 schema**——所以 docstring 要写清楚 |
| `@mcp.resource("uri")` | 注册一个 Resource，URI 是寻址用的 |
| `mcp.run()` | 默认 stdio 模式（最常用） |

> **重要**：MCP SDK 会**直接读 docstring 和 type hints 生成给 LLM 看的工具描述**。这意味着你写文档字符串的功夫，就是「调教模型怎么用工具」的功夫——和 Topic 3 的提示词工程是同一件事。

### 7.3 用 Inspector 跑一下（最快的验证方式）

```bash
mcp dev topics/topic8/mcp_server_demo.py
```

会打开一个浏览器界面（MCP Inspector），你能：
- 看到 `analyze_company`、`retrieve_docs` 两个 Tool；
- 直接点一个 Tool、填参数、看返回；
- 看到 `finsight://disclaimer` 这个 Resource 的内容。

**这是开发 MCP Server 时最有用的工具，强烈建议每加一个 Tool 就用 Inspector 点一遍**。

---

## 8. 第 5 课 — 把 RAG 流水线也变成 MCP Tool（具体例子 #2）

上面 §7 的 `retrieve_docs` 已经做了这件事，但当前 `retrieve_stub` 是空实现。这一节讲「真实 RAG 怎么接进来」——也就是把 Topic 4 的成果接到 Topic 8。

```python
# topics/topic8/mcp_server_demo.py 的进阶版本（节选）

from mcp.server.fastmcp import FastMCP

# 假设你在 Topic 4 已经做好了一个真正可检索的 pipeline
from topics.topic4.chunk_embed import retrieve_top_k  # ← Topic 4 的产物
from topics.topic4.load_docs import load_corpus

mcp = FastMCP("finsight-ai")

# 启动时一次性加载语料 + 建索引（避免每次工具调用都重建）
_corpus = load_corpus("data/raw/")


@mcp.tool()
def retrieve_docs(query: str, top_k: int = 3) -> list[dict]:
    """在金融文档语料中检索与 query 最相关的片段。

    返回值每个元素含：
      - text:     片段原文
      - source:   来源文件名
      - score:    相似度分数 (0-1)

    场景示例：
      - 用户问 "Apple 2023 年的主要风险因子是什么"
        → LLM 自动调用本工具检索 risk factors 段落 → 用检索结果作答（grounded）
    """
    hits = retrieve_top_k(_corpus, query, k=top_k)
    return [
        {"text": h.text, "source": h.source, "score": h.score}
        for h in hits
    ]
```

### 8.1 这个例子妙在哪

不需要改任何 LLM 提示词，**Cursor / Claude 在和你聊财报问题时会自己决定**：

> 用户：「我在看 Apple 的 10-K，帮我提一下 risk factors。」
>
> Claude 自己想：「这个我不确定，需要看原文。我看到 `finsight-ai` 这个 MCP Server 提供 `retrieve_docs` 工具——调它。」
>
> 调用 → 拿到 3 段检索结果 → 基于这 3 段写答案 → 在末尾自动 cite source。

**你只暴露了一个工具，得到的是「带检索能力的 Claude」**——这就是 MCP 比手写 RAG 集成省事的地方。

---

## 9. 第 6 课 — 在 Cursor / Claude Desktop 里接入

### 9.1 Claude Desktop 配置

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）：

```jsonc
{
  "mcpServers": {
    "finsight-ai": {
      "command": "python",
      "args": [
        "/Users/qili/Desktop/financial-ai-coding-study/topics/topic8/mcp_server_demo.py"
      ],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

重启 Claude Desktop，工具栏（🔨 图标）里会出现 `analyze_company`、`retrieve_docs`。直接对话就能触发。

### 9.2 Cursor 配置

Cursor 现在原生支持 MCP，编辑项目根 `.cursor/mcp.json`（或全局 `~/.cursor/mcp.json`）：

```jsonc
{
  "mcpServers": {
    "finsight-ai": {
      "command": "python",
      "args": ["${workspaceFolder}/topics/topic8/mcp_server_demo.py"]
    }
  }
}
```

然后在 Cursor 聊天里：

> 「@finsight-ai 帮我分析一下 NVIDIA」
>
> Cursor 会调用你 MCP Server 里的 `analyze_company` 并把结果嵌入对话。

### 9.3 用 Python 客户端验证（不依赖 Cursor / Claude）

如果你想自己验证、不开 Cursor，可以写一个最小 Python 客户端（`mcp_client_demo.py`）：

```python
"""用 Python 客户端调用本地 MCP Server，验证工具是否注册成功。"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(
        command="python",
        args=["topics/topic8/mcp_server_demo.py"],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            result = await session.call_tool(
                "analyze_company", {"name": "Apple"}
            )
            print("Result:", result.content)


if __name__ == "__main__":
    asyncio.run(main())
```

跑：

```bash
python topics/topic8/mcp_client_demo.py
```

预期输出：

```text
Tools: ['analyze_company', 'retrieve_docs']
Result: [TextContent(type='text', text='{"company": "Apple", "status": "stub"}')]
```

**这一步通了**，意味着你的 Server 已经是个标准 MCP Server，**任何**支持 MCP 的客户端都能接入。

---

## 10. 第 7 课 — MCP vs FastAPI vs Function Calling 的区别（面试常问）

| 维度 | MCP | FastAPI (Topic 2) | OpenAI/Gemini Function Calling |
|---|---|---|---|
| 谁是消费方 | LLM 客户端（Cursor / Claude / 自家 Agent） | 任何 HTTP 客户端（前端 / 第三方） | 一次性 Agent 自己 |
| 协议 | JSON-RPC over stdio / HTTP / SSE，**标准化** | HTTP REST + OpenAPI | 厂商私有 schema |
| 工具描述给 LLM 看 | ✅ 自动（schema + docstring） | ❌ 需要你额外写一份给 LLM 的描述 | ✅ 自动（但绑定厂商） |
| 跨厂商复用 | ✅ Claude / GPT / Cursor / Continue 通吃 | 需要适配 | ❌ 换厂商要重写 |
| 鉴权 / 限流 / 多租户 | 弱（看具体 transport） | ✅ 成熟 | 不适用 |
| 状态 / 长连接 | ✅ 进程级 | ❌ 无状态 | ❌ 无状态 |
| 学习成本 | 低（SDK 几行就跑起来） | 低 | 极低 |
| **典型用途** | **「让我的 Agent / Cursor 多一个能力」** | **「让全世界 / 我的前端调我的服务」** | **「在一段代码里让模型调一次函数」** |

> 面试时一句话回答：「**FastAPI 给最终用户用，MCP 给 LLM 客户端用，Function Calling 给一次性 Agent 用。三者并不冲突，可以共存——同一份业务逻辑可以同时被三种方式包装。**」

---

## 11. 注意事项 / 常见坑

### 11.1 设计层面

- **工具不要做太大**。一个 Tool 做一件事；让 LLM 自己组合。一个「全能工具」对模型反而更难用。
- **docstring 决定模型行为**。把「什么时候用」「什么时候不用」「参数边界」明确写在 docstring 里，比改代码更有效。
- **Resource 不是必须的**。教学顺序：先把 Tools 跑通，再考虑 Resources / Prompts。
- **金融场景下，所有「分析类」Tool 的返回里都建议自动带一段 disclaimer**（结合 Topic 6）。

### 11.2 安全（结合 Topic 6）

- MCP Server 通常以**你的本地用户身份**运行——它能读你的文件、调你的 API。**不要随便装陌生 Server**，等于给一个进程开了你电脑的权。
- 不要在 Tool 里直接执行 LLM 传来的 shell 命令，**永远校验参数**。Pydantic 的类型注解会帮你，但不要依赖它做安全校验。
- API Key 走环境变量（Topic 6 已经讲过），**不要写进 MCP 配置 JSON 的明文**。Claude Desktop 配置里写 `${VAR}`，让它从环境读。
- 日志脱敏：MCP Inspector 会显示完整请求/响应——演示前确认里面没有真实用户数据。

### 11.3 工程

- **stdio 模式 vs HTTP/SSE 模式**：本地用 stdio（简单、快、安全）；多用户 / 远程 / 容器化才考虑 HTTP/SSE。
- **冷启动开销**：如果 Server 启动要加载 RAG 索引，stdio 模式下每次 Cursor 调用都不会重启（长进程），但调试时记得 `mcp dev` 是会重启的。
- **不要把 MCP Server 当成业务 API**。如果你发现自己在 MCP Server 里写鉴权、写多租户、写限流——**它该是 FastAPI**，不是 MCP。
- **CI 里别跑真 MCP**。给 `analyze_company` 写普通单元测试就够；不需要为 MCP 写端到端测试（除非你的项目就是卖 MCP Server）。

### 11.4 LLM 行为

- 模型不一定会调你以为它会调的工具。**调教方式：把工具描述写得更直白**，比如把 `retrieve_docs` 的 description 改成「**当用户问财报、风险因子、业务细节时必须调用本工具，不要凭记忆回答**」。
- Cursor 默认会要求用户**手动确认**每个工具调用。这是好事（安全），但意味着你不能假设「Tool 一定被调用了」。
- 如果一段时间后 Cursor / Claude 都不调你的工具，先去 Inspector 里手动调一次，确认 Server 没坏；再去检查 docstring 是否写明「什么场景该调」。

---

## 12. 推荐练习（按顺序做）

1. **跑通最小 Server**

   按 §7 写好 `mcp_server_demo.py`，用 `mcp dev` 打开 Inspector，**手动**调用 `analyze_company("Apple")`，确认能拿到 `{"company": "Apple", "status": "stub"}`。

2. **Python 客户端验证**

   按 §9.3 写好 `mcp_client_demo.py`，能列出 2 个 Tool 并成功调用。

3. **接入 Cursor**

   写 `.cursor/mcp.json`，重启 Cursor。在聊天里输入「帮我分析 Apple」，确认 Cursor 自动调用了 `analyze_company`。

4. **接入 Topic 4 的真实 RAG**

   把 §8 的进阶版替换 `retrieve_stub`，让 `retrieve_docs` 真的能查 `data/raw/sample_10k.txt`。在 Cursor 里问「Apple 的风险因子是什么」，看它会不会自己调 `retrieve_docs`。

5. **加一个 Resource**

   把 `data/raw/sample_10k.txt` 暴露成 `finsight://corpus/sample_10k`，让 Claude Desktop 能直接「@」它读全文。

6. **写一段「为什么我的 Demo 同时有 FastAPI 和 MCP」**（选做，1 页）

   面试很常被问「你怎么决定一个能力放 FastAPI 还是放 MCP」。先在 README 里写下你的判断逻辑，比临场想清楚得多。

---

## 13. 升级路线（Topic 8 → Topic 8+）

- **HTTP/SSE 模式**：把本地 stdio Server 改成 SSE，部署到 Render / Fly.io，让远程 Agent 也能用。
- **MCP + Docker**（接 Topic 7）：把 Server 容器化，`docker run` 起来，本地 Cursor 通过 stdio 转发到容器。
- **多 Server 协同**：同时挂 `finsight-ai`（你的）+ `filesystem`（官方）+ `git`（官方），让 Claude 能「读文件 + 查仓库 + 跑分析」组合操作。
- **官方 MCP Server 生态**：`@modelcontextprotocol/server-postgres`、`server-slack`、`server-github` 等等，挑一个嵌进你的工作流。
- **OAuth / 多租户**：当 Server 真的要给多人用，按 MCP 规范实现 OAuth 流程（这是 2025 年的活跃区，规范在演进）。
- **Server 写成 SaaS**：Anthropic、Cloudflare、Composio 等都在做托管 MCP Server 平台，了解一下生态。

---

## 14. 自测检查表

- [ ] 我能用一句话讲清楚 MCP 是什么、和 FastAPI / Function Calling 的区别。
- [ ] 我知道什么场景该用 MCP、什么场景不该用（§5 的决策表能背）。
- [ ] 我能区分 Tools / Resources / Prompts 三者。
- [ ] 我用 `FastMCP` 写过一个能跑的 Server，至少有 1 个 Tool。
- [ ] 我用 `mcp dev` 在 Inspector 里调用过自己的 Tool。
- [ ] 我用 Python 客户端调用过自己的 Server，验证过 `tools/list` 返回正确。
- [ ] 我在 Cursor 或 Claude Desktop 配置里加了我的 Server，并真的成功被 LLM 调用。
- [ ] 我把 Topic 4 的 RAG 流水线包装成了 MCP Tool（或至少写好了路径）。
- [ ] 我的 Server 没有把 API Key 写进配置明文（结合 Topic 6）。
- [ ] 我的 README 里写明了「为什么这个项目同时有 FastAPI 和 MCP」。

---

## 15. 反思模板

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

When I would actually choose MCP over a plain FastAPI endpoint:
我什么时候会真的选 MCP 而不是普通 FastAPI 接口：

How this improves my project / interview story:
这如何提升我的项目 / 面试故事：

Next improvement:
下一步改进：
```

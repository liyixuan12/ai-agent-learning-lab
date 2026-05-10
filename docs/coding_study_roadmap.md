# Financial AI Demo Coding Study Roadmap

# 金融 AI Demo 编程学习路线

## 1. Learning Goal

## 1. 学习目标

My main goal is to build a Financial AI Demo and use it as a portfolio project for AI Product Manager / AI Application Developer roles.  
我的主要目标是搭建一个金融 AI Demo，并将其作为 AI 产品经理 / AI 应用开发岗位的作品集项目。

This learning plan focuses on practical coding ability, project thinking, and AI application development.  
这份学习计划重点关注实用编程能力、项目思维和 AI 应用开发能力。

The final goal is not only to learn Python syntax, but also to build a complete demo that includes:  
最终目标不只是学习 Python 语法，而是完成一个包含以下内容的完整 Demo：

- Financial data processing  
金融数据处理
- Rule-based financial analysis  
规则型金融分析
- LLM / RAG-based question answering  
基于 LLM / RAG 的问答
- API design with FastAPI  
使用 FastAPI 设计接口
- Simple frontend or demo interface  
简单前端或 Demo 展示界面
- GitHub documentation  
GitHub 项目文档
- Basic deployment or Docker support  
基础部署或 Docker 支持

---

## 2. Recommended Tech Stack

## 2. 推荐技术栈


| Area                 | Tool / Language                                    | Purpose                                      |
| -------------------- | -------------------------------------------------- | -------------------------------------------- |
| Programming Language | Python                                             | Main language for AI application development |
| Data Analysis        | pandas, NumPy                                      | Financial data processing                    |
| Visualization        | matplotlib / Plotly                                | Basic charts and financial trends            |
| Backend API          | FastAPI                                            | Build API endpoints                          |
| LLM / RAG            | OpenAI API / DeepSeek API / LangChain / LlamaIndex | AI question answering and document analysis  |
| Vector Database      | ChromaDB / FAISS                                   | Store and retrieve document embeddings       |
| Frontend Demo        | Streamlit                                          | Build a simple interactive demo              |
| Database             | SQLite / PostgreSQL                                | Store structured data                        |
| Version Control      | Git + GitHub                                       | Track learning and project progress          |
| Deployment           | Render / Railway / Hugging Face Spaces             | Online demo deployment                       |
| Containerization     | Docker                                             | Reproducible project environment             |


---

## 3. Overall Learning Path

## 3. 总体学习路线

```text
Topic 1: Coding Basics
        ↓
Topic 2: Software Architecture (FastAPI)
        ↓
Topic 3: LLM & Prompt Engineering
        ↓
Topic 4: RAG Basics
        ↓
Topic 5: Version Control & GitHub
        ↓
Topic 6: Privacy & Security
        ↓
Topic 7: Microservices & Containerization [Optional]
        ↓
Topic 8: MCP (Model Context Protocol) [Optional]
        ↓
Topic 9: Agent Workflow Design
        ↓
Topic 10: Agent Evaluation & Observability
        ↓
Topic 11: Guardrails & Responsible AI
        ↓
Topic 12: AI Product Management
        ↓
Final Project: FinSight AI Demo (RAG-based financial research assistant)
```

顺序说明：先打好 Python 与 API 基础，再独立练习 LLM 调用与提示词设计，接着做 RAG 检索链路；版本管理、安全与合规贯穿展示与上线前检查；容器化与 MCP 为可选加分项（前者解决「在哪儿跑」，后者解决「让别的 LLM 客户端怎么用」）；再进入 Agent 工作流设计、评测观测、护栏治理与产品管理，让 Demo 从“能跑”走向“可控、可评估、可讲故事”。  
**进度一览见文末 [Progress Tracker](#progress-tracker--学习进度追踪)。**

---

# Topic 1: Coding Basics

# 主题 1：编程基础

## Core Content

## 核心内容

Variables, data types, if statements, loops, functions, OOP  
变量、数据类型、条件判断、循环、函数、面向对象编程

## Learning Goal

## 学习目标

After this topic, I should be able to write basic Python scripts and understand how to use code to solve simple financial analysis problems.  
完成本主题后，我应该能够编写基础 Python 脚本，并理解如何用代码解决简单金融分析问题。

## Key Skills

## 关键能力

- Create and use variables  
创建和使用变量
- Work with strings, numbers, lists, and dictionaries  
使用字符串、数字、列表和字典
- Write if-else decision logic  
编写 if-else 判断逻辑
- Use loops to process multiple companies or stock prices  
使用循环处理多家公司或股票价格
- Write reusable functions  
编写可复用函数
- Understand basic classes and objects  
理解基础类和对象

## Practice Outputs

## 练习产出

- Company basic information script  
公司基础信息脚本
- Stock price list analysis  
股票价格列表分析
- Revenue growth classification  
营收增长分类
- Risk classification function  
风险分类函数
- Company Growth and Risk Analyzer mini project  
公司增长与风险分析器小项目

## Suggested Files

## 建议文件

```text
topic1_coding_basics.md
topic1_exercises.py
topic1_final_project.py
```

## Completion Checklist

## 完成检查表

- I understand variables and basic data types  
我理解变量和基础数据类型
- I can use lists and dictionaries  
我会使用列表和字典
- I can write if-else statements  
我会写 if-else 条件判断
- I can use for loops  
我会使用 for 循环
- I can write simple functions  
我会写简单函数
- I understand basic OOP concepts  
我理解基础面向对象概念
- I completed the Company Growth and Risk Analyzer  
我完成了公司增长与风险分析器

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my Financial AI Demo:
这对我的金融 AI Demo 的帮助是：

Next improvement:
下一步改进：
```

---

# Topic 2: Software Architecture

# 主题 2：软件架构

## Core Content

## 核心内容

How projects are structured, tech stacks, system design, kinds of APIs, data flow, databases, testing, deployment  
项目结构、技术栈、系统设计、API 类型、数据流、数据库、测试、部署

## Learning Goal

## 学习目标

After this topic, I should understand how a real AI application is structured from data input to AI output.  
完成本主题后，我应该理解一个真实 AI 应用如何从数据输入到 AI 输出进行组织。

## Key Skills

## 关键能力

- Understand basic project structure  
理解基础项目结构
- Understand frontend, backend, database, and AI module relationships  
理解前端、后端、数据库和 AI 模块之间的关系
- Understand REST API basics  
理解 REST API 基础
- Learn FastAPI project structure  
学习 FastAPI 项目结构
- Understand data flow in an AI application  
理解 AI 应用中的数据流
- Learn basic testing and deployment concepts  
学习基础测试和部署概念

## Practice Outputs

## 练习产出

- Draw a system architecture diagram  
画出系统架构图
- FastAPI Financial API: health check plus financial / company analysis endpoints  
FastAPI 金融 API：健康检查及金融 / 公司分析相关接口
- Build a simple FastAPI backend  
构建简单 FastAPI 后端
- Create API endpoints for company analysis  
创建公司分析接口
- Connect rule-based analysis with API response  
将规则型分析和 API 返回结果连接起来

## Suggested Files

## 建议文件

```text
topic2_software_architecture.md
fastapi_basics/
    main.py
    requirements.txt
    README.md
```

## Example API Design

## 示例 API 设计

```text
GET /health
POST /analyze-company
POST /upload-document
POST /ask
```

## Completion Checklist

## 完成检查表

- I understand what an API is  
我理解 API 是什么
- I understand request and response  
我理解请求和响应
- I can create a simple FastAPI app  
我可以创建一个简单 FastAPI 应用
- I can design basic endpoints  
我可以设计基础接口
- I understand basic project structure  
我理解基础项目结构
- I can explain the data flow of my demo  
我可以解释我的 Demo 的数据流

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my Financial AI Demo:
这对我的金融 AI Demo 的帮助是：

Next improvement:
下一步改进：
```

---

# Topic 3: LLM & Prompt Engineering

# 主题 3：大语言模型与提示工程

## Core Content

## 核心内容

Calling LLM APIs, prompt design, structured output (JSON / schema), basic evaluation for financial analysis tasks  
调用 LLM API、提示词设计、结构化输出（JSON / 模式约束）、面向金融分析任务的基础效果评估

## Learning Goal

## 学习目标

After this topic, I should be able to call an LLM from Python, design reusable prompts for financial analysis, and parse structured model outputs safely.  
完成本主题后，我应能从 Python 调用 LLM、设计可复用的金融分析提示词，并安全解析模型的结构化输出。

## Key Skills

## 关键能力

- Configure API client and handle keys via environment variables  
配置 API 客户端并通过环境变量管理密钥
- Write clear system / user prompts for analysis tasks  
为分析任务编写清晰的 system / user 提示词
- Request JSON or schema-constrained responses where appropriate  
在适当时请求 JSON 或受模式约束的回复
- Iterate prompts using small examples (few-shot)  
用小样本（few-shot）迭代提示词
- Recognize limits: hallucination, disclosure, not investment advice  
认识局限：幻觉、表述边界、不构成投资建议

## Practice Outputs

## 练习产出

- Financial Analysis Prompt Templates (reusable markdown or Python strings)  
金融分析提示词模板（可复用的 Markdown 或 Python 字符串）
- Small script: call API → print / save structured result  
小脚本：调用 API → 打印或保存结构化结果

## Suggested Files

## 建议文件

```text
docs/topic3_llm_prompts.md
topics/topic3/prompt_templates/
    analysis_summary.txt
    risk_factors.json_schema_hint.md
src/llm_client.py   # 可与最终项目合并
```

## Completion Checklist

## 完成检查表

- I can call the chosen LLM API from Python  
我能用 Python 调用所选 LLM API
- I designed at least one financial analysis prompt template  
我至少设计了一套金融分析提示词模板
- I can obtain structured or parse-friendly output  
我能获得结构化或易于解析的输出
- I documented limitations and non-advice disclaimer in prompts or notes  
我在提示词或笔记中说明了局限性与非投资建议声明

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my Financial AI Demo:
这对我的金融 AI Demo 的帮助是：

Next improvement:
下一步改进：
```

---

# Topic 4: RAG Basics

# 主题 4：RAG 基础

## Core Content

## 核心内容

Document loading, chunking, embeddings, vector store, retrieval and optional reranking; connecting retrieved context to LLM prompts  
文档加载、文本切分、向量嵌入、向量库、检索与可选重排序；将检索上下文与 LLM 提示词结合

## Learning Goal

## 学习目标

After this topic, I should be able to load financial documents, chunk them, embed and store vectors, retrieve relevant passages, and answer questions grounded in those passages.  
完成本主题后，我应能加载金融文档、切分、嵌入并入库、检索相关段落，并基于段落 grounded 地回答问答。

## Key Skills

## 关键能力

- Load text / PDF (library-dependent) and normalize text  
加载文本 / PDF（依库而定）并规范化文本
- Choose chunk size and overlap for financial reports  
为财报等选择块大小与重叠
- Create embeddings and persist in a vector database (e.g. Chroma / FAISS)  
创建向量并持久化到向量数据库（如 Chroma / FAISS）
- Build a minimal retrieval → prompt → answer pipeline  
搭建最小「检索 → 提示 → 回答」流水线
- Debug retrieval quality (empty hits, wrong chunks)  
调试检索质量（无命中、错误片段）

## Practice Outputs

## 练习产出

- Financial Document Q&A Prototype (CLI or notebook acceptable)  
金融文档问答原型（命令行或 Jupyter 均可）

## Suggested Files

## 建议文件

```text
docs/topic4_rag_notes.md
topics/topic4/
    load_docs.py
    chunk_embed.py
    rag_qa_demo.py
data/raw/sample_10k.txt   # 示例文档（注意版权与用途）
```

## Completion Checklist

## 完成检查表

- I can load and chunk at least one real or sample financial document  
我能加载并切分至少一份真实或示例金融文档
- I store embeddings and run similarity search  
我能存储嵌入并进行相似度检索
- I connect retrieval results to an LLM prompt and get an answer  
我能将检索结果接入 LLM 提示词并得到回答
- I note limitations (OCR, long tables, stale data)  
我记录了局限（OCR、长表、数据时效等）

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my Financial AI Demo:
这对我的金融 AI Demo 的帮助是：

Next improvement:
下一步改进：
```

---

# Topic 5: Version Control & GitHub

# 主题 5：版本控制与 GitHub

## Core Content

## 核心内容

Git fundamentals, branching, pull requests, collaboration workflows  
Git 基础、分支、Pull Request、协作流程

## Learning Goal

## 学习目标

After this topic, I should be able to manage my project with Git and present it professionally on GitHub.  
完成本主题后，我应该能够使用 Git 管理项目，并在 GitHub 上专业地展示项目。

## Key Skills

## 关键能力

- Understand Git and GitHub  
理解 Git 和 GitHub
- Initialize a repository  
初始化仓库
- Commit changes  
提交代码变更
- Create branches  
创建分支
- Push code to GitHub  
推送代码到 GitHub
- Write professional README files  
编写专业 README 文件

## Practice Outputs

## 练习产出

- fCreate a GitHub repository  
创建 GitHub 仓库
- Upload learning outputs from Topics 1–4 (and ongoing API / RAG code)  
上传主题 1–4 的学习产出（以及进行中的 API / RAG 代码）
- Write project README  
编写项目 README
- Add screenshots and project structure  
添加截图和项目结构
- Use meaningful commit messages  
使用清晰的 commit 信息

## Suggested Files

## 建议文件

```text
README.md
.gitignore
requirements.txt
docs/
screenshots/
```

## Example Commit Messages

## 示例 Commit 信息

```text
Add Topic 1 coding basics notes
Add company risk analyzer mini project
Create FastAPI health endpoint
Update README with project structure
```

## Completion Checklist

## 完成检查表

- I can use `git init`  
我会使用 `git init`
- I can use `git add` and `git commit`  
我会使用 `git add` 和 `git commit`
- I can push code to GitHub  
我可以把代码推送到 GitHub
- I understand branches  
我理解分支
- I can write a useful README  
我可以写一个有用的 README
- My project is visible and understandable on GitHub  
我的项目在 GitHub 上清晰可见

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my job application:
这对我的求职有什么帮助：

Next improvement:
下一步改进：
```

---

# Topic 6: Privacy & Security

# 主题 6：隐私与安全

## Core Content

## 核心内容

Authentication, hosting options, database security, deployment security  
身份认证、托管方式、数据库安全、部署安全

## Learning Goal

## 学习目标

After this topic, I should understand the basic privacy and security risks in AI applications, especially financial AI demos.  
完成本主题后，我应该理解 AI 应用中的基础隐私和安全风险，尤其是金融 AI Demo 中的安全问题。

## Key Skills

## 关键能力

- Understand API key security  
理解 API Key 安全
- Use environment variables  
使用环境变量
- Avoid exposing secrets on GitHub  
避免在 GitHub 暴露密钥
- Understand basic authentication  
理解基础身份认证
- Understand database access control  
理解数据库访问控制
- Add financial disclaimer  
添加金融免责声明

## Practice Outputs

## 练习产出

- Create `.env` file  
创建 `.env` 文件
- Add `.env` to `.gitignore`  
将 `.env` 加入 `.gitignore`
- Load API keys securely  
安全读取 API Key
- Write financial disclaimer in README  
在 README 中写金融免责声明
- Understand basic login / token concept  
理解基础登录 / Token 概念

## Suggested Files

## 建议文件

```text
.env
.env.example
.gitignore
security_notes.md
```

## Example Security Notes

## 示例安全说明

```text
This project is for educational and research purposes only.
It does not provide financial investment advice.
API keys should be stored in environment variables and never committed to GitHub.
```

```text
本项目仅用于学习和研究目的。
本项目不构成任何金融投资建议。
API Key 应存储在环境变量中，不应提交到 GitHub。
```

## Completion Checklist

## 完成检查表

- I understand why API keys should not be exposed  
我理解为什么 API Key 不能暴露
- I can use `.env` files  
我会使用 `.env` 文件
- I can create `.gitignore`  
我会创建 `.gitignore`
- I understand basic authentication concepts  
我理解基础身份认证概念
- I added a financial disclaimer  
我添加了金融免责声明
- My GitHub repo does not contain secrets  
我的 GitHub 仓库不包含密钥

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my Financial AI Demo:
这对我的金融 AI Demo 的帮助是：

Next improvement:
下一步改进：
```

---

# Topic 7: Microservices & Containerization [Optional]

# 主题 7：微服务与容器化 [可选]

## Core Content

## 核心内容

Docker, container security, CI/CD, production deployment  
Docker、容器安全、CI/CD、生产部署

## Learning Goal

## 学习目标

After this topic, I should be able to package my AI demo so that it can run in a reproducible environment.  
完成本主题后，我应该能够将 AI Demo 打包，使其可以在可复现的环境中运行。

This topic is optional for my current goal, but learning the basics of Docker can make my project more professional.  
这个主题对于我当前目标是可选的，但学习 Docker 基础可以让项目看起来更专业。

## Key Skills

## 关键能力

- Understand what Docker is  
理解 Docker 是什么
- Write a simple Dockerfile  
编写简单 Dockerfile
- Build and run a Docker image  
构建并运行 Docker 镜像
- Understand container environment variables  
理解容器中的环境变量
- Understand basic CI/CD idea  
理解基础 CI/CD 思想

## Practice Outputs

## 练习产出

- Create a Dockerfile  
创建 Dockerfile
- Run FastAPI app in Docker  
在 Docker 中运行 FastAPI 应用
- Create simple GitHub Actions workflow  
创建简单 GitHub Actions 工作流
- Document Docker commands in README  
在 README 中记录 Docker 命令

## Suggested Files

## 建议文件

```text
Dockerfile
docker-compose.yml
.github/workflows/
    basic-check.yml
```

## Example Docker Commands

## 示例 Docker 命令

```bash
docker build -t financial-ai-demo .
docker run -p 8000:8000 financial-ai-demo
```

## Completion Checklist

## 完成检查表

- I understand Docker images and containers  
我理解 Docker 镜像和容器
- I can write a simple Dockerfile  
我可以写简单 Dockerfile
- I can run my app in Docker  
我可以在 Docker 中运行应用
- I understand basic CI/CD concepts  
我理解基础 CI/CD 概念
- I documented how to run the project  
我记录了如何运行项目

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this improves my project:
这如何提升我的项目：

Next improvement:
下一步改进：
```

---

# Topic 8: MCP (Model Context Protocol) [Optional]

# 主题 8：MCP 模型上下文协议 [可选]

## Core Content

## 核心内容

What MCP is, when to use it vs REST / Function Calling, the three primitives (Tools / Resources / Prompts), writing a minimal MCP server with the Python SDK, and connecting it to Cursor or Claude Desktop  
MCP 是什么、什么时候选用 MCP 而不是 REST / Function Calling、三大原语（Tools / Resources / Prompts）、用 Python SDK 写一个最小 MCP Server，并接入 Cursor 或 Claude Desktop

## Learning Goal

## 学习目标

After this topic, I should be able to wrap my existing financial analysis and RAG retrieval as MCP tools so that any MCP-compatible LLM client (Cursor, Claude Desktop, my own agent) can call them through a standardized protocol.  
完成本主题后，我应能把现有的金融分析与 RAG 检索能力包装成 MCP 工具，让任何兼容 MCP 的 LLM 客户端（Cursor、Claude Desktop、我自己的 Agent）都能通过标准协议调用。

This topic is optional for the demo itself, but it is a high-signal differentiator for AI engineering interviews in 2025–2026.  
这个主题对 Demo 本身是可选的，但在 2025–2026 年的 AI 工程岗面试里是含金量很高的差异化能力。

## Key Skills

## 关键能力

- Explain MCP in one sentence and contrast it with FastAPI and vendor function calling  
用一句话解释 MCP，并与 FastAPI、厂商 Function Calling 做对比
- Decide when MCP is the right tool and when it is over-engineering  
判断什么场景该用 MCP、什么场景属于过度设计
- Write a minimal MCP server with `FastMCP` exposing one or more tools  
用 `FastMCP` 写一个最小 MCP Server，至少暴露一个 Tool
- Wrap existing `src/financial_analyzer.py` and `src/rag_pipeline.py` as MCP tools  
把仓库已有的 `src/financial_analyzer.py` 与 `src/rag_pipeline.py` 包装成 MCP Tool
- Configure Cursor / Claude Desktop to load the local server and verify with MCP Inspector  
在 Cursor / Claude Desktop 中配置加载本地 Server，并用 MCP Inspector 验证

## Practice Outputs

## 练习产出

- Minimal MCP server (`topics/topic8/mcp_server_demo.py`) exposing `analyze_company` and `retrieve_docs`  
最小 MCP Server（`topics/topic8/mcp_server_demo.py`），暴露 `analyze_company` 与 `retrieve_docs`
- Python client (`topics/topic8/mcp_client_demo.py`) that lists tools and calls them  
Python 客户端（`topics/topic8/mcp_client_demo.py`），列出工具并完成调用
- Cursor / Claude Desktop config snippet committed (without secrets)  
提交 Cursor / Claude Desktop 配置片段（不含密钥）

## Suggested Files

## 建议文件

```text
topics/topic8/
    README.md
    mcp_server_demo.py
    mcp_client_demo.py
    cursor_mcp_config.example.json
```

## Example Workflow

## 示例工作流

```text
User in Cursor: "Help me check the risk factors for Apple's latest 10-K"
            │
            ▼
Cursor (MCP Host) calls the `finsight-ai` MCP server
            │
            ▼
MCP server runs `retrieve_docs("Apple risk factors")`
  → returns top-3 grounded chunks
            │
            ▼
Claude / GPT inside Cursor writes a grounded answer with source citations
```

## Completion Checklist

## 完成检查表

- I can explain in one sentence what MCP is and what problem it solves  
我能用一句话讲清楚 MCP 是什么、解决什么问题
- I can list at least one situation where MCP is the right choice and one where it is not  
我能至少各举一个该用 MCP 与不该用 MCP 的具体场景
- I wrote a minimal MCP server using `FastMCP`  
我用 `FastMCP` 写了一个最小 MCP Server
- I verified my server with MCP Inspector (`mcp dev ...`)  
我用 MCP Inspector（`mcp dev ...`）验证过我的 Server
- I successfully called my MCP server from Cursor or Claude Desktop  
我从 Cursor 或 Claude Desktop 成功调用了我的 MCP Server
- I did **not** put API keys directly into the MCP config JSON  
我**没有**把 API Key 直接写进 MCP 配置 JSON
- I wrote one paragraph in my README explaining why this project has both FastAPI and MCP  
我在 README 中写了一段话解释为什么这个项目同时存在 FastAPI 和 MCP

## Reflection

## 学习反思

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

When I would actually choose MCP over a plain FastAPI endpoint:
我什么时候会真的选 MCP 而不是普通 FastAPI 接口：

How this improves my interview story:
这如何提升我的面试故事：

Next improvement:
下一步改进：
```

---

# Topic 9: Agent Workflow Design

# 主题 9：Agent 工作流设计

## Core Content

## 核心内容

Tool calling orchestration, planning vs direct answer strategy, short-term and long-term memory design, human-in-the-loop checkpoints, and tool failure recovery  
工具调用编排、规划式回答 vs 直接回答策略、短期与长期记忆设计、人类介入（HITL）检查点、工具失败恢复机制

## Learning Goal

## 学习目标

After this topic, I should be able to design an agent workflow that chooses tools reliably, plans when tasks are complex, remembers important context, requests human approval at critical steps, and recovers safely from tool failures.  
完成本主题后，我应能设计一个可靠的 Agent 工作流：在复杂任务时先规划、在关键节点请求人工确认、保留关键上下文记忆，并在工具失败时安全恢复。

## Key Skills

## 关键能力

- Define when the agent should call tools and when it should answer directly  
定义 Agent 何时应调用工具、何时应直接回答
- Build a simple planner policy (multi-step tasks require plan, simple tasks go direct)  
建立简单规划策略（多步骤任务先计划，简单任务直接执行）
- Design memory layers (session memory, project memory, durable notes)  
设计记忆分层（会话记忆、项目记忆、持久笔记）
- Add human-in-the-loop gates for destructive or high-risk actions  
为高风险或破坏性操作增加人工确认门槛
- Implement retry / fallback / degrade patterns for tool failures  
实现工具失败时的重试 / 回退 / 降级策略

## Practice Outputs

## 练习产出

- `agent_workflow_design.md` with decision flowcharts  
包含决策流程图的 `agent_workflow_design.md`
- A runnable workflow demo showing plan-first and direct-answer paths  
可运行的工作流示例，展示“先规划”和“直接回答”两条路径
- Failure playbook documenting timeout/error recovery actions  
记录超时与报错恢复动作的故障处理手册

## Suggested Files

## 建议文件

```text
topics/topic9/
    README.md
    workflow_policy.py
    memory_store.py
    hitl_rules.md
    failure_recovery.md
```

## Completion Checklist

## 完成检查表

- I can explain with examples when planning is better than direct answering  
我能举例说明何时应先规划、何时可直接回答
- I can describe at least two memory scopes and their tradeoffs  
我能说明至少两种记忆范围及其取舍
- I implemented at least one human approval checkpoint  
我实现了至少一个人工确认检查点
- I can recover from at least one simulated tool failure  
我能从至少一种模拟工具失败中恢复

## Reflection

## 学习反思

```text
What workflow decisions worked well:
哪些工作流决策效果最好：

Where the agent made wrong tool choices:
Agent 在工具选择上哪里出错了：

How human-in-the-loop improved safety:
人工介入如何提升了安全性：

Next improvement:
下一步改进：
```

---

# Topic 10: Agent Evaluation & Observability

# 主题 10：Agent 评测与可观测性

## Core Content

## 核心内容

Golden test sets, RAG evaluation, tool-call accuracy, tracing, and cost/latency tracking  
黄金测试集、RAG 评测、工具调用准确率、链路追踪、成本与时延跟踪

## Learning Goal

## 学习目标

After this topic, I should be able to evaluate my agent with repeatable tests, observe execution traces end-to-end, and quantify quality-speed-cost tradeoffs.  
完成本主题后，我应能通过可复现测试评估 Agent 质量，追踪端到端执行链路，并量化质量-速度-成本之间的权衡。

## Key Skills

## 关键能力

- Build a golden dataset with expected outputs and pass criteria  
构建包含期望输出与通过标准的黄金数据集
- Define RAG metrics (retrieval hit rate, grounding quality, answer faithfulness)  
定义 RAG 指标（检索命中率、引用贴合度、答案忠实度）
- Measure tool-call precision/recall and argument correctness  
评估工具调用的精准率/召回率与参数正确性
- Add request tracing with step-level logs and IDs  
增加逐步骤日志与请求 ID 的链路追踪
- Track token cost and latency by scenario  
按场景跟踪 token 成本与响应时延

## Practice Outputs

## 练习产出

- `golden_set.jsonl` with representative financial questions  
包含代表性金融问题的 `golden_set.jsonl`
- Evaluation report comparing at least two prompt/workflow versions  
至少两版提示词/工作流对比评测报告
- Dashboard or markdown report for trace, cost, and latency trends  
追踪、成本、时延趋势看板或 markdown 报告

## Suggested Files

## 建议文件

```text
topics/topic10/
    README.md
    golden_set.jsonl
    eval_runner.py
    rag_eval.md
    observability_metrics.md
```

## Completion Checklist

## 完成检查表

- I can run one command/script to reproduce evaluation results  
我可以用一条命令/脚本复现实验结果
- I can explain at least three quality metrics for my agent  
我能解释至少三个 Agent 质量指标
- I can identify one major bottleneck from traces or metrics  
我能从链路或指标中定位一个主要瓶颈
- I can report cost and latency for a fixed test set  
我能针对固定测试集输出成本与时延报告

## Reflection

## 学习反思

```text
What metrics changed after optimization:
优化后哪些指标发生了变化：

What regressions were caught by the golden set:
黄金测试集发现了哪些回归问题：

What observability data was most useful:
最有价值的可观测数据是什么：

Next improvement:
下一步改进：
```

---

# Topic 11: Guardrails & Responsible AI

# 主题 11：护栏与负责任 AI

## Core Content

## 核心内容

Prompt injection defense, financial advice boundaries, output validation, permission design, and risk documentation  
提示词注入防护、金融建议边界、输出校验、权限设计、风险文档化

## Learning Goal

## 学习目标

After this topic, I should be able to define and implement safety boundaries so my financial AI assistant is useful but does not cross policy, compliance, or trust limits.  
完成本主题后，我应能为金融 AI 助手建立并落实安全边界，让系统在可用的同时不越过策略、合规和信任底线。

## Key Skills

## 关键能力

- Detect and mitigate common prompt injection patterns  
识别并缓解常见提示词注入模式
- Define what is educational analysis vs prohibited personalized investment advice  
明确“教育性分析”与“禁止的个性化投资建议”的边界
- Validate outputs for structure, citation, and disclaimer requirements  
对输出进行结构、引用、免责声明校验
- Design least-privilege tool permissions for agent actions  
按最小权限原则设计 Agent 工具权限
- Write risk documentation and incident response notes  
编写风险文档与异常响应说明

## Practice Outputs

## 练习产出

- Guardrail policy document (`guardrails_policy.md`)  
护栏策略文档（`guardrails_policy.md`）
- Injection test cases with expected safe behavior  
提示注入测试用例及期望安全行为
- Output validator rules for financial disclaimer and citation checks  
包含免责声明与引用检查的输出校验规则

## Suggested Files

## 建议文件

```text
topics/topic11/
    README.md
    guardrails_policy.md
    injection_tests.jsonl
    output_validator.py
    risk_register.md
```

## Completion Checklist

## 完成检查表

- I can demonstrate one blocked injection and one safe fallback answer  
我能演示一次被拦截的注入攻击和一次安全降级回复
- I can explain my financial advice boundary in one clear paragraph  
我能用一段清晰文字解释金融建议边界
- I validate critical outputs before returning to users  
我会在返回给用户前校验关键输出
- I documented key risks and mitigation owners/actions  
我记录了关键风险及其负责人/缓解动作

## Reflection

## 学习反思

```text
Where guardrails were too strict or too loose:
护栏哪里过严或过松：

What risky behavior was prevented:
防住了哪些高风险行为：

What policy is still ambiguous:
还有哪些策略边界不够清晰：

Next improvement:
下一步改进：
```

---

# Topic 12: AI Product Management

# 主题 12：AI 产品管理

## Core Content

## 核心内容

PRD writing, user journey mapping, MVP scope definition, product metrics, cost-quality tradeoff, and demo storytelling  
PRD 编写、用户旅程设计、MVP 范围定义、产品指标、成本-质量权衡、Demo 讲述能力

## Learning Goal

## 学习目标

After this topic, I should be able to frame my technical demo as a product: who it serves, what pain it solves, what MVP includes/excludes, how success is measured, and how to tell a convincing story.  
完成本主题后，我应能把技术 Demo 讲成产品：服务谁、解决什么问题、MVP 包含/不包含什么、如何衡量成功，以及如何清晰讲述产品故事。

## Key Skills

## 关键能力

- Write a concise PRD for a financial AI assistant feature  
为金融 AI 助手功能写简明 PRD
- Map user journey from first query to actionable output  
绘制从首次提问到可执行输出的用户旅程
- Define MVP scope and explicit out-of-scope items  
定义 MVP 范围并明确不做项
- Select north-star and supporting product metrics  
选择北极星指标及配套指标
- Explain cost-quality tradeoffs to stakeholders  
向干系人解释成本-质量权衡
- Present a compelling demo narrative for interviews or reviews  
为面试或评审呈现有说服力的 Demo 叙事

## Practice Outputs

## 练习产出

- One-page PRD for your final demo  
最终 Demo 的一页 PRD
- User journey map and MVP scope table  
用户旅程图与 MVP 范围表
- Metrics sheet with baseline and target values  
含基线与目标值的指标表
- 5-minute demo storytelling script  
5 分钟 Demo 讲述脚本

## Suggested Files

## 建议文件

```text
topics/topic12/
    README.md
    prd.md
    user_journey.md
    mvp_scope.md
    metrics_plan.md
    demo_storytelling.md
```

## Completion Checklist

## 完成检查表

- I can clearly explain user, pain point, and core value in under 60 seconds  
我能在 60 秒内清晰说出用户、痛点与核心价值
- I defined an MVP with clear in-scope and out-of-scope boundaries  
我定义了清晰的 MVP 范围与边界
- I selected measurable product metrics and target values  
我选定了可衡量的产品指标与目标值
- I prepared a concise demo story aligned with interview expectations  
我准备了符合面试预期的精炼 Demo 故事

## Reflection

## 学习反思

```text
What product insight changed my implementation priorities:
哪些产品洞察改变了我的实现优先级：

What metric best reflects user value:
哪个指标最能反映用户价值：

How I balance quality with budget/latency:
我如何在质量与预算/时延间取舍：

Next improvement:
下一步改进：
```

---

# Final Project: Financial AI Demo

# 最终项目：金融 AI Demo

## Project Name

## 项目名称

FinSight AI: RAG-based Financial Research Assistant  
FinSight AI：基于 RAG 的金融研究助手

## Project Goal

## 项目目标

Build an AI-powered financial research assistant that can process company-related information and generate structured analysis.  
构建一个 AI 金融研究助手，能够处理公司相关信息，并生成结构化分析。

## Core Features

## 核心功能

- Upload or load financial documents  
上传或读取金融文档
- Extract and store company information  
提取并存储公司信息
- Analyze basic financial indicators  
分析基础财务指标
- Retrieve relevant document chunks with RAG  
使用 RAG 检索相关文档片段
- Generate structured company analysis with LLM  
使用 LLM 生成结构化公司分析
- Provide API endpoints with FastAPI  
使用 FastAPI 提供接口
- Provide a simple UI with Streamlit  
使用 Streamlit 提供简单界面
- Document everything on GitHub  
在 GitHub 上完整记录项目

## Target User

## 目标用户

Students, job applicants, junior analysts, or AI product learners who want to quickly understand company information.  
希望快速理解公司信息的学生、求职者、初级分析师或 AI 产品学习者。

## Product Value

## 产品价值

This demo shows how AI can help users collect, retrieve, summarize, and structure financial information.  
这个 Demo 展示了 AI 如何帮助用户收集、检索、总结和结构化金融信息。

It does not replace professional financial analysis or investment advice.  
它不替代专业金融分析或投资建议。

## Suggested Project Structure

## 建议项目结构

```text
financial-ai-demo/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── docs/
│   ├── coding_study_roadmap.md
│   ├── topic1_coding_basics.md
│   ├── topic2_software_architecture.md
│   ├── topic3_llm_prompts.md
│   ├── topic4_rag_notes.md
│   ├── security_notes.md
│   └── architecture_diagram.png
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── data_exploration.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── financial_analyzer.py
│   ├── rag_pipeline.py
│   ├── llm_client.py
│   └── report_generator.py
│
├── api/
│   └── main.py
│
├── app/
│   └── streamlit_app.py
│
├── tests/
│   └── test_financial_analyzer.py
│
└── Dockerfile
```

---

## Final Project Checklist

## 最终项目检查表

### Coding

### 编程

- Python scripts are readable  
Python 脚本清晰可读
- Functions are reusable  
函数可复用
- Project has clear structure  
项目结构清晰
- Basic error handling is included  
包含基础错误处理

### AI / RAG

### AI / RAG

- Documents can be loaded  
文档可以被读取
- Text can be chunked  
文本可以被切分
- Embeddings can be created  
可以创建向量嵌入
- Relevant content can be retrieved  
可以检索相关内容
- LLM can generate structured answers  
LLM 可以生成结构化回答

### API

### 接口

- FastAPI app runs locally  
FastAPI 应用可以本地运行
- `/health` endpoint works  
`/health` 接口可用
- `/analyze-company` endpoint works  
`/analyze-company` 接口可用
- API response is structured  
API 返回结构清晰

### GitHub

### GitHub

- README explains the project clearly  
README 清楚解释项目
- Installation steps are included  
包含安装步骤
- Usage examples are included  
包含使用示例
- Screenshots are included  
包含截图
- Financial disclaimer is included  
包含金融免责声明

### Security

### 安全

- API keys are not committed  
API Key 未提交到仓库
- `.env` is ignored  
`.env` 已被忽略
- `.env.example` is provided  
提供 `.env.example`
- Financial disclaimer is visible  
金融免责声明清晰可见

### Deployment

### 部署

- App can run locally  
应用可以本地运行
- Optional Dockerfile is provided  
提供可选 Dockerfile
- Optional online demo is available  
可选：提供在线 Demo

---

# Weekly Study Schedule

# 每周学习安排

## 10 Hours per Week Version

## 每周 10 小时版本


| Time  | Focus                           |
| ----- | ------------------------------- |
| 3 hrs | Python basics and exercises     |
| 2 hrs | FastAPI / software architecture |
| 2 hrs | LLM / RAG project development   |
| 1 hr  | GitHub documentation            |
| 1 hr  | Security and deployment basics  |
| 1 hr  | Review and reflection           |


---

## Intensive 10-Day MVP Version

## 10 天快速 MVP 版本


| Day    | Task                                                        |
| ------ | ----------------------------------------------------------- |
| Day 1  | Python basics: variables, lists, dictionaries               |
| Day 2  | If statements, loops, functions                             |
| Day 3  | Mini project: company growth and risk analyzer              |
| Day 4  | Learn FastAPI basics                                        |
| Day 5  | Build simple financial analysis API                         |
| Day 6  | Learn RAG basics and document chunking                      |
| Day 7  | Connect LLM API and generate structured answers             |
| Day 8  | Build simple Streamlit interface                            |
| Day 9  | Write README, add screenshots, improve project structure    |
| Day 10 | Final cleanup, GitHub upload, demo presentation preparation |


---

# Progress Tracker

# 学习进度追踪


| Topic                                                | Status      | Output                              | Notes                                                              |
| ---------------------------------------------------- | ----------- | ----------------------------------- | ------------------------------------------------------------------ |
| Topic 1: Coding Basics                               | Not Started | Company Growth and Risk Analyzer    | Python basics, list, dict, if, loop, function, OOP                 |
| Topic 2: Software Architecture                       | Not Started | FastAPI Financial API               | API, data flow, project structure, backend basics                  |
| Topic 3: LLM & Prompt Engineering                    | Not Started | Financial Analysis Prompt Templates | LLM API call, prompt design, structured output                     |
| Topic 4: RAG Basics                                  | Not Started | Financial Document Q&A Prototype    | document loading, chunking, embeddings, vector database, retrieval |
| Topic 5: Version Control & GitHub                    | Not Started | GitHub Repository and README        | Git workflow, commits, branches, README, portfolio presentation    |
| Topic 6: Privacy & Security                          | In Progress | `.env`, `.gitignore`, API Key Auth, Disclaimer | API key security, FastAPI auth, secret scan, financial disclaimer  |
| Topic 7: Microservices & Containerization [Optional] | In Progress | Multi-stage Dockerfile, Compose stack, CI build | Non-root container, .dockerignore, compose for API+UI+Chroma, CI   |
| Topic 8: MCP (Model Context Protocol) [Optional]     | Not Started | MCP Server exposing analyze_company + retrieve_docs | FastMCP, Tools/Resources/Prompts, Cursor & Claude Desktop integration |
| Topic 9: Agent Workflow Design                       | In Progress | Workflow policy + 3-layer memory + HITL rules + failure playbook | Router, plan-and-execute, session/project/durable memory, HITL gate, retry/fallback/degrade |
| Topic 10: Agent Evaluation & Observability           | In Progress | Golden set + eval report + tracing metrics      | RAG evaluation, tool-call accuracy, tracing, cost/latency tracking |
| Topic 11: Guardrails & Responsible AI                | Not Started | Guardrail policy + output validator + risk register | Prompt injection defense, advice boundary, permission design |
| Topic 12: AI Product Management                      | Not Started | PRD + user journey + metrics + demo storytelling | MVP scope, product metrics, cost-quality tradeoff, communication |
| Final Project                                        | Not Started | FinSight AI Demo                    | RAG-based financial research assistant                             |


状态栏可自行改为 `In Progress` / `Done`。产出物名称与上文各主题 **Practice Outputs** 一致。  
**双语：** Topic 1–12 与终项目对应关系见上文第三节「总体学习路线」。

---

# Learning Notes Template

# 学习笔记模板

For each section, I will use the following format:  
每个小节我都会使用以下格式记录：

```markdown
## Topic / Concept  
## 主题 / 概念

### What I learned  
### 我学到了什么

### My understanding  
### 我的理解

### Code example  
### 代码示例

### Practice  
### 练习

### Output  
### 输出结果

### Mistakes and fixes  
### 错误与修正

### How this helps my Financial AI Demo  
### 这对我的金融 AI Demo 有什么帮助

### Reflection  
### 反思
```

---

# Final Reflection

# 总结反思

```text
What I have built:
我已经完成了什么：

What I can explain in an interview:
我可以在面试中解释什么：

What still needs improvement:
我还需要改进什么：

How this project supports my AI Product Manager / AI Application Developer transition:
这个项目如何支持我转型 AI 产品经理 / AI 应用开发：
```


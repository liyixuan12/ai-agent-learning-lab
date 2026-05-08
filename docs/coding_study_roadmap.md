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
Final Project: FinSight AI Demo (RAG-based financial research assistant)
```

顺序说明：先打好 Python 与 API 基础，再独立练习 LLM 调用与提示词设计，接着做 RAG 检索链路；版本管理、安全与合规贯穿展示与上线前检查；容器化为可选加分项。  
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
| Topic 6: Privacy & Security                          | Not Started | `.env`, `.gitignore`, Disclaimer    | API key security, financial disclaimer, secure deployment basics   |
| Topic 7: Microservices & Containerization [Optional] | Optional    | Dockerized Demo                     | Dockerfile, containerized FastAPI app, reproducible environment    |
| Final Project                                        | Not Started | FinSight AI Demo                    | RAG-based financial research assistant                             |


状态栏可自行改为 `In Progress` / `Done`。产出物名称与上文各主题 **Practice Outputs** 一致。  
**双语：** Topic 1–7 与终项目对应关系见上文第三节「总体学习路线」。

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


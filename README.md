# AI Agent 学习实验室 · FinSight AI（金融 Demo）

本仓库（`ai-agent-learning-lab`）面向「金融场景 AI 应用」作品集：从 Python 与 FastAPI 基础，到 LLM / RAG，再延伸到 **Agent 工作流、评测与可观测、护栏与负责任 AI、以及 AI 产品管理**。完整目标、技术栈、每周安排与 **进度追踪表** 见：

**[docs/coding_study_roadmap.md](docs/coding_study_roadmap.md)**

---

## 学习路径在仓库里怎么对应

路线图中的 **Topic 1–12** 与 `topics/topicN/` 一一对应；其中 **Topic 9–12** 是从「能调用模型」到「能交付可控 Agent 产品」的主线，建议在完成 LLM/RAG（Topic 3–4）并衔接版本管理与安全（Topic 5–6）后系统学习：

| Topic | 侧重点 | 入门文档 |
| ----- | ------ | -------- |
| **9** Agent 工作流 | 路由策略、三层记忆、HITL、失败恢复 | [topics/topic9/README.md](topics/topic9/README.md) |
| **10** 评测与可观测 | 黄金集、RAG/工具评测、Tracing、成本延迟 | [topics/topic10/README.md](topics/topic10/README.md) |
| **11** 护栏与负责任 AI | 注入防御、输出校验、风险登记 | [topics/topic11/README.md](topics/topic11/README.md) |
| **12** AI 产品管理 | PRD、用户旅程、MVP、指标、Demo 叙事 | [topics/topic12/README.md](topics/topic12/README.md) |

Topic 7（Docker）与 Topic 8（MCP）在路线图中为 **可选加分**；与 Topic 9 的 MCP 集成说明见各主题 README。

---

## 免责声明

本项目仅供学习与演示；不构成任何投资建议。请勿将 API 密钥提交到版本库。

---

## 目录结构（概要）

与路线图一致的约定：**文档说明在 `docs/`，按主题动手材料在 `topics/topicN/`**，核心业务代码在 `src/`、`api/`、`app/`。

```text
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── docs/
│   ├── coding_study_roadmap.md   # 完整学习路线与进度表（主入口）
│   ├── topic1_coding_basics.md
│   ├── topic2_software_architecture.md
│   ├── topic2_fastapi_tutorial.md
│   ├── topic3_llm_prompts.md
│   ├── topic4_rag_notes.md
│   └── security_notes.md
├── topics/
│   ├── topic1/        # 编程基础与公司风险分析练习
│   ├── topic2/        # FastAPI 与架构（含 fastapi_basics 子项目）
│   ├── topic3/        # LLM 与提示词
│   ├── topic4/        # RAG 与文档问答原型
│   ├── topic5/        # Git / GitHub 与协作
│   ├── topic6/        # 隐私与安全（密钥、鉴权、扫描等）
│   ├── topic7/        # 容器化（可选）：Docker / Compose / CI 示例
│   ├── topic8/        # MCP（可选）：服务端与客户端示例
│   ├── topic9/        # Agent 工作流：策略、记忆、HITL、失败恢复
│   ├── topic10/       # Agent 评测与可观测性
│   ├── topic11/       # 护栏与负责任 AI
│   └── topic12/       # AI 产品管理（PRD、旅程、MVP、指标）
├── data/raw/ · data/processed/
├── notebooks/
├── src/               # 分析、RAG、LLM 客户端等共享模块
├── api/               # FastAPI 应用入口（占位/演示）
├── app/               # Streamlit 等前端 Demo
├── tests/
└── .github/workflows/ # 例如 basic-check.yml
```

各 `topics/topicN/README.md` 内有该主题的目录清单与运行方式；不必在根 README 重复罗列每个脚本文件名。

---

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # 填入真实密钥（勿提交 .env）
```

- **API（占位）**：`uvicorn api.main:app --reload`
- **Streamlit（占位）**：`streamlit run app/streamlit_app.py`
- **测试**：`pytest`

如需容器化运行，参见 `Dockerfile`、`docker-compose.yml` 及 [topics/topic7/README.md](topics/topic7/README.md) 中的示例文件。

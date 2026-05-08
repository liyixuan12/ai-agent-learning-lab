# FinSight AI（金融 AI Demo）学习与项目仓库

本仓库用于「金融 AI Demo / FinSight AI」的学习路线与代码骨架。完整的学习目标、主题 checklist、技术栈与进度表见：

**[docs/coding_study_roadmap.md](docs/coding_study_roadmap.md)**

## 免责声明

本项目仅供学习与演示；不构成任何投资建议。请勿将 API 密钥提交到版本库。

## 目录结构（与路线图一致）

```text
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── docs/
│   ├── coding_study_roadmap.md    # 完整学习路线（原根目录 README 内容）
│   ├── topic1_coding_basics.md
│   ├── topic2_software_architecture.md
│   ├── security_notes.md
│   ├── python_basics_notes.md
│   └── architecture_diagram.png   # 可自行添加架构示意图
├── topics/topic1/                 # 主题 1：练习脚本、小作业与公司风险分析器
│   ├── topic1_exercises.py
│   ├── topic1_final_project.py
│   ├── exercises/                 # 分章节练习占位
│   └── company_risk_analyzer/     # 小项目
├── topics/topic3/                 # 主题 3：LLM 与提示词（可与 docs/topic3_llm_prompts.md 对照）
├── topics/topic4/                 # 主题 4：RAG 练习与文档问答原型
├── data/raw/
├── data/processed/
├── notebooks/
├── src/
├── api/
├── app/
├── tests/
└── Dockerfile
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # 填入真实密钥（勿提交 .env）
```

- API（占位）：`uvicorn api.main:app --reload`
- Streamlit（占位）：`streamlit run app/streamlit_app.py`
- 测试：`pytest`

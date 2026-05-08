# Topic 4 — RAG 基础完整教学

> 范围：本目录是 Topic 4 的实操区。你将完成「文档加载 → 切分 → 向量化 → 检索 → 拼接 Prompt → LLM 回答」一个最小可运行的 RAG 闭环，并用同一份样本文档做「固定窗口 vs 按章节切块」的对比实验。
>
> 配套笔记（概念为主）：`docs/topic4_rag_notes.md`。本文件聚焦「**这一份代码**到底是怎么实现的、怎么跑、怎么看输出、怎么避坑」。

---

## 1. 学完这一节你应具备的能力

- 用 Python 读入并清洗一份金融文档；理解为什么不能整篇直接喂给 LLM。
- 会两种切块策略：**固定字符窗口** 与 **按章节标题** + 章节内二次切；能解释各自的优缺点与适用场景。
- 用相似度（余弦）从一组 chunks 中检索 Top-K；能读懂「分数」、判断哪些命中是噪声。
- 把检索内容拼成 grounded prompt，让模型只基于上下文回答（防止幻觉）。
- 能用 `--dry-run` 在不调用 LLM 的情况下做检索/切块对比实验。
- 能描述当前方案的局限，并知道下一阶段要升级到「真正的 embedding 模型 + 向量库」。

---

## 2. 本目录结构

```text
topics/topic4/
├── README.md            # 本文件，完整教学
├── load_docs.py         # 文档加载 + 文本规范化
├── chunk_embed.py       # 切块 + 词袋向量 + 余弦检索（含 chunk_by_section）
└── rag_qa_demo.py       # 端到端 Demo（含 --strategy / --top-k / --dry-run）

# 配套数据与文档
data/raw/sample_10k.txt           # 样本财报文本（教学用）
docs/topic4_rag_notes.md          # 概念笔记
```

---

## 3. 先决条件与环境

- 仓库已合并为根目录单一 `.venv` 与 `.env`（详见仓库根 `README` 与 `.env.example`）。
- `.env` 至少包含：

  ```env
  GEMINI_API_KEY=...
  GEMINI_MODEL=gemini-2.5-flash
  ```

- 不安装 `google-genai` 也能运行：脚本会自动用 Gemini REST API 兜底。

---

## 4. RAG 的最小心智模型（一图）

```text
原始文档
   │
   ▼
[1] 加载/规范化  ─────────► load_docs.load_text_file()
   │
   ▼
[2] 切块 (Chunking) ─────► chunk_embed.chunk_text() 或 chunk_by_section()
   │
   ▼
[3] 向量化 (Embedding) ──► chunk_embed.embed_text() (词袋演示)
   │
   ▼
[4] 检索 (Retrieval) ────► chunk_embed.rank_chunks()    # 取 Top-K
   │
   ▼
[5] 拼 Prompt + 调用 LLM ► rag_qa_demo.build_prompt() / answer_with_llm()
   │
   ▼
最终答案（grounded）
```

记住一句话：**RAG 的天花板由「检索」决定，不是模型。**

---

## 5. 代码导读（与你将运行的脚本对应）

### 5.1 `load_docs.py` — 加载与规范化

- `normalize_text()`：统一换行、压缩多余空白；保留段落分隔。
- `load_text_file()`：只接受 `.txt` / `.md`（PDF 等留给后续课）。

> 注意事项
> - 真实财报常有页眉页脚、表格、脚注，**规范化是第一步而不是装饰**。
> - 不要在加载阶段去掉换行；很多切块逻辑依赖段落边界。

---

### 5.2 `chunk_embed.py` — 切块 + 检索

**两个切块函数：**

| 函数 | 策略 | 适合 |
|---|---|---|
| `chunk_text(text, chunk_size, overlap)` | 固定字符窗口 + 重叠 | 无结构纯文本、Demo |
| `chunk_by_section(text, max_chunk_size, overlap, section_titles)` | 按已知小标题切；长章节再 `chunk_text` 二次切 | 财报 / 招股书 / 合同 |

**`Chunk` 数据结构：**

```python
@dataclass
class Chunk:
    chunk_id: str          # e.g. "section_profitability__0"
    text: str
    start_char: int        # 在原文中的起点（按章节切时也保持全局偏移）
    end_char: int
    section: str | None    # 仅按章节切时有：来自哪一节
```

**词袋向量与余弦相似度：**

- `tokenize()` 同时支持中文/英文/数字字符；
- `embed_text()` 生成「**归一化的稀疏词频向量**」；
- `cosine_sim()` 在稀疏字典上做点积；
- `rank_chunks()` 给所有 chunk 算分并排序，取 Top-K。

> 注意事项
> - 这里的「embedding」是**演示版**：纯按词形匹配，**不会理解语义近义**（margin ≈ gross margin ≈ profitability）。
> - 真实生产请替换成 OpenAI / Gemini / BGE / E5 等 embedding 模型，并把向量持久化到 Chroma/FAISS。

---

### 5.3 `rag_qa_demo.py` — 端到端 Demo

关键函数：

- `build_chunks(document, strategy)`：根据 `--strategy` 决定调 `chunk_text` 还是 `chunk_by_section`。
- `build_prompt(question, contexts)`：拼装 grounded prompt。**这里是防止幻觉的关键**——明确告诉模型「只基于上下文 / 缺信息要说『资料不足』 / 中文 + 免责声明」。
- `answer_with_llm(prompt)`：优先用 `google-genai` SDK；没有则走 Gemini REST。
- `load_environment()`：自动尝试以下 `.env` 路径：

  ```text
  ./.env
  ./topics/topic3/llm_prompt_basics/.env
  ./topics/topic4/.env
  ```

CLI 参数：

```text
--strategy    fixed | section | both    （默认 fixed）
--question    "..."                     （默认是 revenue/margin 那一题）
--top-k       N                         （默认 5）
--dry-run                               （跳过 LLM，仅做检索与 Prompt 预览）
```

---

## 6. 快速开始

> 在仓库根目录执行（统一 venv）。

### 6.1 单策略，正常调用 LLM

```bash
.venv/bin/python topics/topic4/rag_qa_demo.py --strategy section --top-k 5
```

### 6.2 离线对比实验（推荐，第一次跑用这个）

```bash
.venv/bin/python topics/topic4/rag_qa_demo.py --strategy both --top-k 5 --dry-run
```

输出会包含两段「EXPERIMENT RUN」，分别打印两种切块策略的 Top-K chunks 与 Prompt 预览。

### 6.3 自定义问题

```bash
.venv/bin/python topics/topic4/rag_qa_demo.py \
  --strategy both \
  --top-k 5 \
  --question "What drove gross margin improvement in FY2025?"
```

---

## 7. 怎么读输出（重点）

每条命中行长这样：

```text
1. section_profitability__0 | score=0.1425 | section=Profitability
Profitability Gross margin improved from 58.2% to 61.5%, primarily driven by ...
```

读法：

- `chunk_id`：固定窗口下是 `chunk_<n>`；按章节切下是 `section_<slug>__<i>`，能让你**一眼看出来自哪一节**。
- `score`：词袋余弦相似度；当前是 0–1 之间。**它是相对值**，不要拿不同问题的分数互相比较。
- `section`：只有按章节策略才会有；对调试和可追溯性极有价值。

---

## 8. 实验：为什么要「按章节」切？

固定窗口下你可能看到这种 chunk：

```text
chunk_2  →  ...Professional services revenue remained flat...
            Profitability
            Gross margin improved from 58.2% to 61.5%, ...
```

一个块里**同时**含有 Revenue 段尾巴和 Profitability 开头——它对「营收问题」和「毛利率问题」**都不够纯粹**，分数会被稀释。

按章节切之后：

```text
section_revenue_and_growth__0  →  整段 Revenue and Growth
section_profitability__0       →  整段 Profitability
```

每块语义集中，召回质量直接提升，并且**可以告诉用户「答案来自 Profitability 这一节」**——溯源价值很大。

实操建议（按收益排序）：

1. **用 `chunk_by_section`**（结构清晰的财报第一选项）。
2. 长章节用 `max_chunk_size` 兜底，避免单块超长。
3. 短章节直接成块，**不要再切**。
4. 给检索结果带上 `section` 元数据，用于展示与排错。

---

## 9. 注意事项 / 常见坑

### 9.1 切块（最容易踩）
- chunk 太大 → 一块里啥都有，检索糊掉。
- chunk 太小 → 上下文残缺，LLM 看不懂。
- 没有 overlap → 一句话被切成两半，跨块语义丢失。
- 不识别小标题 → 跨章节内容拼一起，主题混杂。

### 9.2 检索（词袋方案的局限）
- 词袋不懂同义词：问 “margin” 不会匹配 “profitability”。
- 一个长 chunk 里高频词会主导分数（“revenue”出现多次会压过更精确的命中）。
- `top_k` 太小容易漏；太大噪声多——通常 **3–8** 之间试。

### 9.3 Prompt（防幻觉）
- 必须显式写：「**只基于上下文回答**」「**信息不足时说『资料不足』**」。
- 控制输出形式（中文 / 要点 / 字数），否则模型容易自由发挥。
- 给 chunks 编号（`[Context 1]` / `[Context 2]`）能让模型在回答里更稳定地引用。

### 9.4 数据与合规
- `data/raw/sample_10k.txt` 是教学用文本；放真实文档前确认版权与用途。
- `.env` 永远不要提交（仓库 `.gitignore` 已忽略 `.env`）。
- 答案务必带免责声明——这是「**金融研究助手**」的硬性 UI 约束，不是花絮。

### 9.5 网络与依赖
- 没装 `google-genai` 也能跑：脚本会切到 Gemini REST API。
- 偶发 503 / 429：先用 `--dry-run` 验证检索逻辑，再重试 LLM 调用。
- API Key 出现在 URL 时只走 HTTPS，不要把请求日志贴到公共渠道。

---

## 10. 推荐练习（按顺序做）

1. **基线对比**  
   ```bash
   .venv/bin/python topics/topic4/rag_qa_demo.py --strategy both --top-k 5 --dry-run
   ```
   写下「fixed 与 section 各自的 Top5 是什么」「哪些是噪声」。

2. **缩小 top_k**  
   把 `--top-k 5` 改成 `--top-k 3`，再对比；体会「召回 vs 精度」的权衡。

3. **换一个问题**  
   - `What were the key risks for FY2026?`  
   - `What is the company's leverage and liquidity position?`  
   观察哪种切块策略更稳定。

4. **加章节标题**  
   在 `chunk_embed.py` 的 `DEFAULT_FINANCIAL_SECTION_TITLES` 中加你自己文档的小标题（例：`Forward-Looking Statements`），再跑一遍。

5. **错例归档**  
   建一个 `topics/topic4/error_log.md`，写 2 个「检索错了 / 模型说资料不足但其实有」的案例，并附上你打算怎么修。

---

## 11. 升级路线（Topic 4 → Topic 4+）

- 把 `embed_text()` 替换为真实 embedding 模型（OpenAI / Gemini / BGE / E5）。
- 用 **Chroma** 或 **FAISS** 持久化向量，启动时不用每次重新计算。
- 引入 **reranker**（如 `bge-reranker`）做二次精排。
- 加入「**不可回答识别**」评估：构造一些原文里**没有**的问题，检查模型是否会乖乖说「资料不足」。
- 多文档检索：把 `chunk` metadata 中的 `source` 字段也带上，回答时引用 `[来源: filename / section]`。

---

## 12. 自测检查表

- [ ] 我能解释 RAG 的 5 步流程，并指出「天花板在检索」是什么意思。
- [ ] 我能跑通 `--strategy both --dry-run`，并讲出两种切块的差异。
- [ ] 我能在 `chunk_by_section()` 中加新的小标题。
- [ ] 我能写出一段「让 LLM 不乱编」的 grounded prompt。
- [ ] 我能列出当前方案的 3 个局限，以及对应的升级方向。

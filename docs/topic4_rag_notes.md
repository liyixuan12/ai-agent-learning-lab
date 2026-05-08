# Topic 4: RAG Basics 实战笔记

这份文档用于带你完成 Topic 4 的最小可运行闭环：

`文档加载 -> 文本切分 -> 向量化 -> 检索 -> 拼接 Prompt -> LLM 回答`

---

## 1. 学完 Topic 4 你应具备的能力

- 能把一份金融文档加载并清洗成可处理文本。
- 能为财报类内容设置合理 `chunk_size` 与 `overlap`。
- 能做相似度检索，并挑出与问题最相关的片段。
- 能把检索到的片段放进 Prompt，让回答可追溯（grounded）。
- 能识别并记录 RAG 局限：命中偏差、表格丢失、数据时效问题。

---

## 2. 本主题目录

```text
docs/topic4_rag_notes.md
topics/topic4/
    load_docs.py
    chunk_embed.py
    rag_qa_demo.py
data/raw/sample_10k.txt
```

---

## 3. 快速开始（直接跑）

在项目根目录执行：

```bash
python topics/topic4/rag_qa_demo.py
```

你将看到：

1. 检索到的 Top chunks 及相似度分数。  
2. 拼装后的 Prompt 预览。  
3. 最终答案（若未配置 API Key，会给出本地提示）。  

---

## 4. 代码结构说明

### 4.1 `load_docs.py`

- 负责加载 `.txt/.md` 文档。
- 做基础规范化（空白、换行）。

### 4.2 `chunk_embed.py`

- `chunk_text()`：按固定窗口 + 重叠切分文本。
- `embed_text()`：用轻量词袋向量做演示（便于本地零依赖跑通）。
- `rank_chunks()`：计算 query 与 chunk 的余弦相似度并排序。

### 4.3 `rag_qa_demo.py`

- 读取样本文档。
- 执行切分和检索。
- 将检索内容拼入 grounded prompt。
- 若有 `GEMINI_API_KEY`，调用模型回答；否则给出本地 fallback。

---

## 5. 推荐练习（按顺序）

1. 修改问题并观察检索变化  
   - 例如：`FY2026 的主要风险是什么？`
2. 调整切分参数  
   - 比较 `chunk_size=300/450/700` 对检索结果的影响。
3. 增加真实文档样本  
   - 复制一份新的 `data/raw/*.txt`，替换 `rag_qa_demo.py` 的输入路径。
4. 写一段“错误分析”  
   - 记录 2 个检索失误案例和改进思路。

---

## 6. 常见问题排查

- 没命中（score 接近 0）  
  - 问题写得太泛；先加入实体名（公司名、年份、指标）。
- 命中片段不完整  
  - 增大 `chunk_size` 或 `overlap`。
- 回答和文档不一致  
  - 检查 Prompt 是否限制“仅基于上下文”。
- 输出太啰嗦  
  - 在 Prompt 增加回答格式约束（要点式、字数上限）。

---

## 7. 下一步升级（Topic 4 -> Topic 4+）

- 将 `embed_text()` 替换为真实 embedding 模型（如 OpenAI/Gemini embedding）。
- 接入 Chroma/FAISS 做持久化向量检索。
- 加 reranking（可选）提高相关性。
- 

### Document Chunking Strategy

In this project, the financial report is split into smaller text chunks before retrieval.  
The chunking strategy combines section-based splitting and fixed-length splitting:

1. The document is first split by financial section headings, such as Business Overview, Revenue and Growth, Profitability, and Risk Factors.
2. If a section is too long, it is further split into smaller chunks with overlap.
3. Each chunk is embedded and stored for similarity-based retrieval.
4. During question answering, the top-k most relevant chunks are retrieved and passed to the LLM as context.

This design improves retrieval quality and reduces the risk that the model answers without seeing the relevant information.


### 文档切分策略

本项目在进行 RAG 检索前，会先将金融文本切分为多个较小的 chunk。  
切分方式采用“章节标题切分 + 固定长度切分”的混合策略：

1. 首先根据 Business Overview、Revenue and Growth、Profitability、Risk Factors 等金融章节标题进行切分；
2. 如果某一章节内容过长，则继续按照固定长度进行二次切分，并保留一定 overlap；
3. 每个 chunk 会被转换为 embedding 并存入向量库；
4. 用户提问时，系统会检索相似度最高的 top-k chunks，并作为上下文传入 LLM。

这种方式可以提升检索质量，减少模型在没有看到相关资料时产生不完整或不准确回答的风险。
---

## 8. 完成检查（自测）

- [ ] 我能加载并切分至少一份金融文档  
- [ ] 我能完成相似度检索并解释命中原因  
- [ ] 我能把检索上下文接入 Prompt 并得到 grounded 回答  
- [ ] 我能说清当前方案的 3 个局限  
- [ ] 我有一条明确的升级路线（向量库 + 评估）  

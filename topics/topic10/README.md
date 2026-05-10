# Topic 10 — Agent 评测与可观测性

> **衔接 Topic 9**：你已经有了 Router、Planner、Executor、HITL、`safe_call` 和 **jsonl 友好** 的 `_log()`。Topic 10 回答三件事：**（1）质量是否下降可以自动发现？（2）慢在哪、贵在哪能否量化？（3）面试里如何讲「你可控地迭代 Agent」？**

---

## 1. 学完本节你应具备的能力

- 维护一份 **`golden_set.jsonl`**：每条包含用户问题、期望路由（或期望工具序列）、标签。
- 用 **一条命令** 跑回归（本目录 `eval_runner.py`），对比修改 Router/Planner **前后** 的准确率。
- 说出至少三种 **Agent/RAG 质量指标**（路由准确率、工具序列正确率、检索 Hit@k、忠实度等）。
- 根据 Topic 9 的 trace 字段，解释如何聚合 **P95 延迟、失败率、HITL 拒绝率、token 成本**。
- 在作品集/README 里写一小段 **「Eval + Observability」** 叙述（可与 Topic 7 Docker / Topic 8 MCP 并列）。

---

## 2. 本目录结构

```text
topics/topic10/
├── README.md                 # 本文件
├── golden_set.jsonl          # 黄金测试集（路由期望 + tags）
├── eval_runner.py            # 跑 golden 集、生成 markdown 报告
├── rag_eval.md               # RAG 侧指标备忘
└── observability_metrics.md  # 从 trace 派生指标备忘
```

复用：`topics/topic9/workflow_policy.py`（被 `eval_runner` 动态加载）。

---

## 3. 为什么「能跑」不等于「可上线」

| 只有 Demo | 加上 Topic 10 |
|-----------|----------------|
| 改 prompt 靠感觉 | **黄金集**告诉你是否回归 |
| 用户说「变慢了」 | **P95 延迟**按步骤拆解 |
| 不知道钱花在哪儿 | **按 route / 按调用** 粗算 token |
| 出错靠猜 | **trace_id** 串起全链路 |

---

## 4. 立即动手（约 10 分钟）

在仓库根目录执行：

```bash
python topics/topic10/eval_runner.py
```

应看到 **Route accuracy: 100%**（与当前 `workflow_policy.route` 一致）。  
改 `REFUSE_KEYWORDS` 或 `SINGLE_TOOL_KEYWORDS` 故意破坏一行逻辑，再运行——你会在报告里看到 **Route mismatches**。

导出报告（可选）：

```bash
python topics/topic10/eval_runner.py --label baseline --out topics/topic10/eval_report_baseline.md
```

对比实验：

```bash
# 修改 workflow_policy 后
python topics/topic10/eval_runner.py --label experiment --out topics/topic10/eval_report_experiment.md
diff topics/topic10/eval_report_baseline.md topics/topic10/eval_report_experiment.md
```

---

## 5. 黄金集怎么写

每行一个 JSON（jsonl）：

| 字段 | 必填 | 含义 |
|------|------|------|
| `id` | 建议 | 稳定编号，方便 diff |
| `query` | 是 | 用户自然语言 |
| `expected_route` | 是 | `DIRECT` / `SINGLE` / `PLAN` / `COMPARE_COMPANIES` / `REFUSE`（与 Topic 9 `route()` 返回值一致） |
| `tags` | 否 | 分组统计用，如 `policy`、`rag`、`compare` |
| `expected_tools` | 否 | 若要与 `make_plan` 对齐，列出工具名序列；运行 `eval_runner.py --check-tools` 时校验 |

**原则**：覆盖每条路由至少 2 条；覆盖拒绝类问题；覆盖边界（如「Compare ROE vs ROI」无公司名 → 落到 `PLAN`）。

---

## 6. RAG 与工具评测的分工

- **路由 / 计划结构**：`eval_runner.py` + `golden_set.jsonl`。
- **检索是否找对文档**：需带 **gold chunk id** 的数据集，算 Hit@k / MRR——见 `rag_eval.md`。
- **生成是否胡说**：忠实度、citation 覆盖率——可用规则 + 抽检或 LLM-as-judge（注意偏差）。

不要把「路由对了」当成「RAG 对了」；二者叠加才是端到端质量。

---

## 7. 可观测性：从 `_log` 到指标

Topic 9 每条日志是一行 JSON，含 `trace_id`、`event`、`elapsed_ms` 等。  
按 `trace_id` 聚合即可得到步骤序列与总耗时。详见 `observability_metrics.md`。

**最小落地**：把 `print(json.dumps(...))` 改成追加写入 `logs/agent.jsonl`，用小型脚本按天统计 `step.error` 比例。

---

## 8. 完成检查表（对照路线图）

- [ ] 能用一条命令复现评测结果（`eval_runner.py`）。
- [ ] 能解释至少三个与你 Demo 相关的质量指标。
- [ ] 能从 trace 或自建指标里指出 **一个** 性能或失败瓶颈。
- [ ] 能对固定黄金集描述 **成本 / 延迟** 的对比思路（哪怕先用粗估 token）。

---

## 9. 学习反思（可复制）

```text
优化后哪些指标发生了变化：

黄金测试集发现了哪些回归问题：

最有价值的可观测数据是什么：

下一步改进：
```

---

## 10. 延伸阅读顺序建议

1. 跑通 `eval_runner.py`，故意改坏路由再跑一次。  
2. 读 `rag_eval.md`、`observability_metrics.md`。  
3. 打开 `topics/topic9/workflow_policy.py` 搜索 `_log`，对照每条 `event` 想「若写入 BI，该画什么图」。  
4. 准备 Topic 11（护栏）时，把「注入攻击拦截率」也当作一类 golden 标签。

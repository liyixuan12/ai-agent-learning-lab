# Topic 11 — Guardrails & Responsible AI

> **衔接 Topic 9/10**：你已经有了基础 Agent 工作流与评测框架。Topic 11 解决的是「系统能做」和「系统该不该做」之间的边界问题：如何防提示词注入、如何拒绝越界投资建议、如何在返回前做输出安全校验。

---

## 1. 学完本节你应具备的能力

- 识别常见提示词注入模式，并在执行前拦截高风险请求。
- 明确教育性金融解释与个性化投资建议的边界，并给出一致的拒答策略。
- 对输出做结构化校验（免责声明、引用、禁止语句）。
- 能写出风险台账，并把风险映射到负责人和缓解动作。
- 能把护栏纳入 Topic 10 的评测闭环，而不是只靠人工感觉。

---

## 2. 本目录结构

```text
topics/topic11/
├── README.md               # 本文件
├── guardrails_policy.md    # 护栏策略与判定规则
├── injection_tests.jsonl   # 注入/越界测试集（可回归）
├── output_validator.py     # 输出安全校验脚本
└── risk_register.md        # 风险登记册（风险、影响、缓解、owner）
```

---

## 3. 快速开始（5 分钟）

在仓库根目录执行：

```bash
python topics/topic11/output_validator.py --sample safe
python topics/topic11/output_validator.py --sample unsafe
```

你应看到：

- `safe` 用例通过校验（包含免责声明与引用）。
- `unsafe` 用例失败，并提示触发了哪些规则。

---

## 4. 你要重点掌握的三层护栏

1. **输入护栏（Input Guardrails）**  
   拦截注入、越权、恶意指令；在进入 planner/tool 前先做判定。
2. **过程护栏（Execution Guardrails）**  
   工具调用遵循最小权限；高风险动作必须 HITL。
3. **输出护栏（Output Guardrails）**  
   最终返回前强制校验免责声明、引用、禁用建议语句。

---

## 5. 如何与 Topic 10 结合

- 把 `injection_tests.jsonl` 当作一类 golden set，统计「注入拦截率」。
- 新增指标：`guardrail_block_rate`、`unsafe_output_rate`、`false_refusal_rate`。
- 每次改路由策略都要跑一次护栏回归，避免「优化回答质量时放松安全边界」。

---

## 6. 完成检查表

- [ ] 我能演示一次注入请求被拦截并给出安全降级回复。
- [ ] 我能用一段话解释教育性分析与投资建议的边界。
- [ ] 我能在返回前对关键字段做自动校验，而不是人工目测。
- [ ] 我能维护一份最小风险登记册，并写出下一个改进动作。

---

## 7. 学习反思（可复制）

```text
护栏哪里过严（误拒）：

护栏哪里过松（漏拦）：

最有价值的一条规则是：

下一步改进：
```


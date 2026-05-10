# 可观测性指标（Topic 10）

Topic 9 的 `workflow_policy._log()` 已输出 **jsonl 友好** 的单行 JSON。Topic 10 要把这些行当成**事件的事实来源**，再聚合出指标。

## 1. 必备字段（每条 trace）

| 字段 | 作用 |
|------|------|
| `trace_id` | 把一次用户请求下的所有步骤串起来 |
| `event` | 事件类型：`plan.start`、`step.ok`、`step.error`、`plan.done` 等 |
| `elapsed_ms` | 该步骤耗时（若记录） |

生产环境通常还会加：`service`、`env`、`user_id`（脱敏）、`model`、`prompt_version`。

## 2. 从 trace 派生的核心指标

| 指标 | 计算方式 | 用途 |
|------|----------|------|
| **P95 延迟** | 同 trace_id 下 `plan.start` → 最后 `plan.done` 或失败事件 | 发现慢路径 |
| **步骤失败率** | `step.error` + `plan.failed` / 总 step 数 | 工具稳定性 |
| **空检索率** | `step.empty` / `retrieve_docs` 调用次数 | RAG 质量预警 |
| **HITL 拒绝率** | `hitl` 且 `approved=false` / 高风险工具调用次数 | Router/Planner 是否乱触发副作用 |
| **重试率** | `attempt>1` 的 step 占比 | 超时与抖动 |

## 3. 成本与 token

Demo 可用 **粗估**：`sum(每步 token 估算)` 或按 `route` 类型给固定成本系数。  
上线应对每次 LLM 调用记录 **input_tokens / output_tokens**，按模型单价算钱。

## 4. 与 OpenTelemetry 的关系

jsonl 适合本地与 CI；上云可把同样字段打成 **span**：每个 `step` 一个 span，`trace_id` 映射为 trace。思路一致：**先统一字段，再换导出后端**。

# Topic 11 Risk Register

## 1. 使用说明

此表用于持续维护护栏风险，不是一次性文档。每次出现误拒、漏拦或异常调用都应更新。

---

## 2. 风险清单（最小版）

| 风险ID | 风险描述 | 概率 | 影响 | 当前控制 | 待办动作 | Owner | 状态 |
|---|---|---|---|---|---|---|---|
| R-001 | 提示词注入导致策略被绕过 | 中 | 高 | 输入黑名单 + 拒答模板 | 增加模式归一化（大小写/空格变体）测试 | Agent Eng | Open |
| R-002 | 输出出现个性化买卖建议 | 低 | 高 | 输出规则校验 + 免责声明 | 扩充禁用语句库并做周回归 | AI Safety | Open |
| R-003 | 引用缺失导致事实不可追溯 | 中 | 中 | `missing_source_citation` 校验 | 引入 citation 覆盖率指标到 Topic 10 报告 | Data Eng | Open |
| R-004 | 误拒率过高影响可用性 | 中 | 中 | 手工抽样复盘 | 增加 `false_refusal_rate` 指标并按标签分析 | PM/Eng | Open |
| R-005 | 高风险工具越权调用 | 低 | 高 | 最小权限 + HITL | 增加工具白名单审计日志 | Platform | Planned |

---

## 3. 事件响应（简化）

1. 发现问题后 24 小时内登记风险与样本。
2. 判断是误拒还是漏拦，标注优先级（P0-P3）。
3. 指定 owner 与截止日期，提交规则或代码修复。
4. 用 `injection_tests.jsonl` 补回归样本，防止回归。

---

## 4. 指标建议

- `guardrail_block_rate`：被护栏阻断的请求比例
- `unsafe_output_rate`：输出校验失败比例
- `false_refusal_rate`：本应可答却被拒绝的比例
- `citation_coverage`：应引用场景下的引用覆盖率


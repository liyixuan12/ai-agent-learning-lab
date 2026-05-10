# HITL 规则手册（Human-in-the-Loop）

> Topic 9 配套文档。和 `workflow_policy.py` 里的 `hitl_gate()` 配合使用。
>
> 一句话原则：**只要这一步出错会让用户损失（钱、数据、声誉、合规），就必须让人按一下「Approve」。**

---

## 1. 工具风险等级

| 等级 | 含义 | 是否需要 HITL | 例子（金融 Demo 场景） |
|---|---|---|---|
| **L0：只读** | 不改变任何外部状态 | ❌ 不需要 | `retrieve_docs`, `analyze_company`, `direct_answer` |
| **L1：本地写入** | 只在本地（沙箱内）写文件 | ⚠️ 默认免审，但要进 trace | 写入 `./.topic9/`、生成 PDF 报告 |
| **L2：内部副作用** | 修改本仓库的持久存储 | ⚠️ 配置开关 | 写入向量库、写入项目 SQLite |
| **L3：外部副作用** | 调用第三方 API 但不可逆 / 收费 | ✅ **必须** | 发邮件、推 Slack、调付费 API、下单 |
| **L4：不可恢复** | 删除 / 改写已有数据 | ✅ **必须 + 二次确认** | 清空向量库、删除用户文件、撤回已发邮件 |

> `workflow_policy.py` 的 `TOOLS` 字典里第二个布尔值就是 `is_risky`：默认对应 ≥L3。
> L1/L2 的「轻确认」可以用别的机制（如 dry-run 默认值），不一定走全套 HITL。

---

## 2. 触发 HITL 的条件（任一满足即触发）

1. 工具风险等级 ≥ L3。
2. 单次工具调用预估成本 ≥ $0.10（`gpt-4o` 一次重 query 即可达到这个量级）。
3. 单次调用涉及 **跨用户 / 跨账户** 数据。
4. 调用参数被检测到注入痕迹（详见 Topic 11，例：args 里出现 `\n\nIgnore previous instructions`）。
5. 当前 plan 累计已重试 ≥ 2 次仍未成功——继续重试前要让人介入。
6. 用户 query 命中「投资建议」红线（参见 `route()` 中的 `REFUSE_KEYWORDS`）——在最终回复前让人审核话术。

---

## 3. 标准化的 HITL 提示词模板

> 给用户的提示语必须包含：**做什么 / 用什么参数 / 为什么 / 拒绝后会怎样**。

```text
[需要确认]

我准备执行：    {tool_name}
参数：          {args_json}
预计影响：      {impact}        ← 例如 "向 watchlist 中所有人发送本周报告"
预计成本：      ${cost_usd:.2f} ← 可选，能估就估
拒绝后会：      {fallback}      ← 例如 "改为只生成 PDF 不发送"

是否继续？(y / n / edit)
```

三个动作的设计要点：
- `y`：批准当前**这次**调用，不批准未来。
- `n`：拒绝并执行 `fallback`；如果没有 fallback，整条 plan 终止。
- `edit`：让用户修改 args 后重提交（**强烈推荐**——比"批/拒"二元更人性化）。

---

## 4. 批准时效与作用域

| 维度 | 推荐值 | 反例（不要这样做） |
|---|---|---|
| 时效 | **60 秒** | "本会话内永久批准" → 等于关掉 HITL |
| 作用域 | **`tool_name + args` 哈希** 唯一匹配 | 仅按 `tool_name` 批准 → LLM 改个参数就绕开 |
| 重提交 | 用户 edit 后**重新走一遍** HITL | 直接用旧批准记录 → 失去 edit 的意义 |
| 并发 | **每个 trace_id 单独一份批准缓存** | 全局批准缓存 → 一个会话的批准被另一个会话复用，越权 |

---

## 5. CI / 自动化模式下的默认行为

**强制默认拒绝（fail-closed）**。理由：

- CI 跑回归测试时，如果默认批准，一个失控的脚本就能把生产数据删光。
- 自动化任务通常不该需要 L3+ 工具——如果需要，应当事先用**带签名的 token** 显式 opt-in，而不是依赖运行时 HITL。

`workflow_policy.py` 里的 `hitl_gate(..., auto_decision=None)` 就是这个语义。如果你想在 CI 里跑一个**真的能调发送的**集成测试，必须显式传 `HitlDecision(approve=True, reason="ci-integration-test")`，并且这个测试只对**沙箱账户**生效。

---

## 6. 一个完整的示例对话

> 场景：用户让 Agent 把上周的财报分析推送给 `watchlist` 里所有公司联系人。

```text
User:
    把我 watchlist 里 5 家公司的本周风险摘要发给他们的 IR 联系人邮箱。

Agent (内部 plan):
    1. retrieve_docs(...)         L0
    2. retrieve_docs(...) x4      L0
    3. llm_summarize(...)         L0
    4. send_email(to=[...], subject="...", body="<<step3>>")   L3 ⚠️

Agent (在 step 4 之前停下):
    [需要确认]
    我准备执行：    send_email
    参数：          {"to": ["ir@apple.com","ir@msft.com",...], "subject":"FinSight 风险周报", "body":"…1.2KB…"}
    预计影响：      向 5 个外部邮箱发送邮件，无法撤回
    预计成本：      $0.00（邮件本身），但生成 body 已花费 $0.04
    拒绝后会：      只生成本地 PDF，不发送
    是否继续？(y / n / edit)

User:
    edit  把 to 改成只剩 ir@apple.com 我先试一封

Agent:
    [需要确认]
    我准备执行：    send_email
    参数：          {"to": ["ir@apple.com"], "subject":"FinSight 风险周报", "body":"…1.2KB…"}
    预计影响：      向 1 个外部邮箱发送邮件
    预计成本：      $0.00
    拒绝后会：      只生成本地 PDF
    是否继续？(y / n / edit)

User:
    y

Agent (执行 + trace):
    {"event":"hitl","step":4,"approved":true,"reason":"manual","approved_args_hash":"…"}
    {"event":"step.ok","step":4,"tool":"send_email","attempt":1}
    [DONE] 已发送给 ir@apple.com，请在收件箱确认。
```

---

## 7. 反模式（在面试 / 评审里被质疑的常见做法）

| 反模式 | 为什么差 | 正确做法 |
|---|---|---|
| 「批准一次，整个 session 都不再问」 | 等于没有 HITL | 单次批准，60 秒过期 |
| 「先调用，再问要不要继续」 | 已经造成的副作用收不回来 | 永远在调用**之前**确认 |
| 仅按 `tool_name` 匹配批准 | LLM 改参数就绕过 | 按 `tool_name + args_hash` |
| HITL 只显示工具名，不展开参数 | 用户不知道自己批准了什么 | 必须 pretty-print args |
| 把 HITL 决策写进 LLM prompt 让模型评估 | LLM 是被审核者，不能当审核员 | HITL 必须是确定性代码或真人 |
| 拒绝后直接 fail，没有 fallback | 用户体验差，且鼓励他们粗暴批准 | 每个 L3+ 工具都给一个 L≤ 的降级路径 |

---

## 8. 与本仓库其他 Topic 的衔接

- **Topic 6（Privacy & Security）**：HITL 是身份认证的「前一公里」——你确认了"是这个用户"，HITL 确认"这个用户真的想做这件事"。
- **Topic 10（Evaluation）**：HITL 拒绝率应作为指标。如果 ≥30% 的工具调用被人工拒绝，说明你的 Router/Planner 有问题。
- **Topic 11（Guardrails）**：HITL 只是防误用的最后一道；护栏（如 args 注入检测）应该在 HITL 之前过滤掉**明显恶意**的调用，让人工审 review 的真的是「合理但有风险」的请求，而不是垃圾。

---

## 9. 自测题

- [ ] 我能说出本仓库里至少 2 个 L3+ 工具，并解释为什么是 L3+。
- [ ] 我的 HITL 提示词包含了「做什么 / 参数 / 影响 / 拒绝后会」四要素。
- [ ] 我在 CI 模式下默认拒绝，且能给出一个例外开关的设计。
- [ ] 我能解释「按 args_hash 而不是按 tool_name 批准」的原因。
- [ ] 我没有让任何 L3+ 工具走「永久批准」路径。

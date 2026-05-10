# 失败处理 Playbook（Failure Recovery）

> Topic 9 配套文档。和 `workflow_policy.py` 里的 `safe_call()` 配合使用。
>
> 一句话原则：**任何工具调用都假设会失败；失败的处理路径要写在代码里，而不是事后再说。**

---

## 1. 失败的四大类（必须先分类，再讨论怎么处理）

| 类别 | 信号 | 例子 |
|---|---|---|
| **Timeout** | 超过预算时间没返回 | 网络慢、API 限流被排队、模型推理 >30 s |
| **Exception** | 抛错 | 401 鉴权 / 4xx 参数错 / 5xx 服务端 / 解析错 |
| **Empty** | 调用成功但结果为空 | 检索 0 命中、LLM 返回空字符串 |
| **Hallucinated** | 调用成功且非空，但内容错 | LLM 凭空编了不存在的来源、检索结果完全不相关 |

> **重要**：把「失败」=「抛异常」是初学者最大的误区。**Empty 和 Hallucinated 才是金融 Demo 里最常见、最危险的失败**——它们看起来"成功"，但答案是错的。

---

## 2. 重试 / 回退 / 降级 / 放弃 决策表

| 失败类型 | 重试 | 回退到另一工具 | 降级回答 | 放弃并告知 |
|---|---|---|---|---|
| 单次 Timeout | ✅ ≤2 次（带 jitter） | ❌ | ❌ | ❌ |
| 连续 Timeout | ❌ | ✅ 缓存 / 备用 API | ✅ "暂时无法获取最新数据，仅基于公开信息回答" | ❌ |
| 401 / 403 鉴权错 | ❌ | ❌ | ❌ | ✅ 让用户检查 API key |
| 4xx 参数错 | ❌（除非重写 args） | ❌ | ❌ | ✅ 让 LLM 改 plan |
| 5xx 服务端错 | ✅ ≤2 次 | ✅ | ✅ | ❌ |
| 检索为空 | ✅ ≤1 次（改 query） | ❌ | ✅ "未找到相关原文，仅基于通用知识" | ❌ |
| 检索结果不相关 | ❌ | ❌ | ✅ | ❌ |
| 输出疑似幻觉 | ❌ | ✅ 加引用校验工具 | ✅ "以下内容可能不准确" | ❌ |
| HITL 被拒绝 | ❌ | 走 fallback step | ✅ 仅本地预览 / 不发送 | ❌ |

> 这张表不是死的——业务变化时要更新。但**一定要有一张表**。"出错了模型自己看着办"不是工程。

---

## 3. 四种处理动作的具体写法

### 3.1 重试（Retry）

```python
for attempt in range(1, max_retries + 2):
    try:
        return tool(**args)
    except TimeoutError:
        time.sleep(0.05 * attempt + random.random() * 0.05)  # backoff + jitter
```

要点：
- **带 jitter**：避免上下游同时重试雪崩。
- **有上限**：通常 `max_retries = 2`；超过就走降级或放弃。
- **不是所有错都该重试**：4xx 参数错、401 鉴权错重试只会浪费 quota。

### 3.2 回退到另一工具（Fallback）

例：`retrieve_docs` 用 ChromaDB 失败时，回退到本地 grep。

```python
def retrieve_with_fallback(query, top_k):
    try:
        return chroma_retrieve(query, top_k)
    except Exception:
        # local fallback: just grep the raw corpus
        return grep_retrieve(query, top_k)
```

**铁律**：**回退路径的安全等级不能高于原路径**。
反例：`retrieve_docs` 失败 → 回退到「让 LLM 凭记忆瞎答」。这等于把"找不到"伪装成"找到了"，比直接报错更糟。

### 3.3 降级（Graceful Degradation）

输出依然给用户，但**显式告知不完整 / 不准确**。

```text
我没能从最新文档中检索到相关原文，以下回答基于截至 2024 年初的通用知识：
...
（此回答可能不反映最新披露，请以官方公告为准。）
```

**铁律**：降级回答必须**显式声明已降级**——不要假装一切正常。这条在金融场景比一切都重要。

### 3.4 放弃（Give Up Cleanly）

明确告诉用户做不到、原因是什么、下一步建议。

```text
我无法完成这次分析：检索 API 返回 401（鉴权失败）。
请检查 .env 中的 OPENAI_API_KEY 是否过期。
（trace_id: 7060ecc5）
```

**铁律**：放弃信息要包含 **trace_id**，方便排障。Topic 10 会教怎么把 trace_id 串起来。

---

## 4. Empty 和 Hallucination 的特别处理

### 4.1 Empty 检测

```python
if step.tool == "retrieve_docs" and not result:
    # 触发软失败：扩大 top_k 再试一次
    if attempt <= 1:
        step.args["top_k"] += 2
        continue
    return StepResult(ok=False, error="empty")
```

`workflow_policy.py` 里就是这个逻辑。注意它**不退化为"瞎答"**——空结果直接终止 plan。

### 4.2 Hallucination 检测（产品级）

幻觉无法 100% 杜绝，但可以**降低概率 + 让用户能识别**：

| 措施 | 实现 | 成本 |
|---|---|---|
| 强制引用 | LLM 输出必须含 `[来源]` 字段，否则 reject 重写 | 低 |
| Citation 校验 | 把回答里出现的引用 id 反查向量库，不存在就 reject | 中 |
| Cross-check | 用第二个模型对答案打 fact-consistency 分 | 高 |
| Confidence cap | 检索 score < 阈值 → 降级回答 | 低 |

> **建议优先级**：先做「强制引用 + 检索 score 阈值」（成本低、收益大），再考虑 cross-check。

---

## 5. 三个不要踩的坑

- ❌ **无限重试**：永远要有 `max_retries`。
- ❌ **静默吞错**：每次失败都必须进 trace（jsonl）。否则 Topic 10 评测时根本看不到「Agent 其实坏了」。
- ❌ **回退到更危险的工具**：见 §3.2 铁律。失败回退路径必须 **安全等级 ≤ 原工具**。

---

## 6. 完整示例：4 种失败的端到端处理

### 6.1 Timeout → 重试 → 成功

```jsonc
{"trace_id":"abc","event":"step.timeout","step":1,"attempt":1}
{"trace_id":"abc","event":"step.timeout","step":1,"attempt":2}
{"trace_id":"abc","event":"step.ok","step":1,"tool":"retrieve_docs","attempt":3}
```

用户视角：稍慢一点，但回答正常。

### 6.2 Empty → 改 query 重试一次 → 仍空 → 降级

```jsonc
{"trace_id":"def","event":"step.ok","step":1,"tool":"retrieve_docs","attempt":1}
{"trace_id":"def","event":"step.empty","step":1,"attempt":1}
{"trace_id":"def","event":"step.ok","step":1,"tool":"retrieve_docs","attempt":2}
{"trace_id":"def","event":"step.empty","step":1,"attempt":2}
{"trace_id":"def","event":"plan.failed","step":1,"error":"empty"}
```

用户视角：「未找到相关原文，以下基于通用知识：……（带降级声明）」。

### 6.3 401 鉴权错 → 直接放弃

```jsonc
{"trace_id":"ghi","event":"step.error","step":1,"attempt":1,"error":"AuthError: 401"}
{"trace_id":"ghi","event":"plan.failed","step":1,"error":"AuthError: 401"}
```

用户视角：「**API key 失效，请检查 .env**（trace_id: ghi）」。

### 6.4 看似成功但是幻觉 → cross-check 拦下

```jsonc
{"trace_id":"jkl","event":"step.ok","step":2,"tool":"llm_summarize","attempt":1}
{"trace_id":"jkl","event":"validation.failed","step":2,"reason":"citation-not-found:src=fake_10k.txt"}
{"trace_id":"jkl","event":"step.retry-with-stricter-prompt","step":2}
{"trace_id":"jkl","event":"step.ok","step":2,"tool":"llm_summarize","attempt":2}
```

用户视角：完全无感（多花 200 ms 和一点点 token）。这就是幻觉防护的理想效果。

---

## 7. 与其他 Topic 的衔接

- **Topic 10（Evaluation & Observability）**：`safe_call` 输出的 jsonl 就是评测系统的输入。失败率、平均重试次数、降级率都是核心指标。
- **Topic 11（Guardrails）**：很多「失败」其实是被护栏拦下的越界请求——它们应当走 **REFUSE** 路径而不是 retry。
- **Topic 6（Security）**：错误信息绝不能泄露内部细节（堆栈、文件路径、API key 片段）——给用户看的 message 要脱敏，trace 才记完整。

---

## 8. 自测题

- [ ] 我能说出 4 类失败（timeout / exception / empty / hallucinated）。
- [ ] 我能针对每类至少给 1 种处理动作。
- [ ] 我的所有重试都有上限和 jitter。
- [ ] 我没有让任何「失败回退」走到比原步骤更危险的路径上去。
- [ ] 我的降级回答**显式声明**自己在降级。
- [ ] 我的失败信息里有 trace_id，便于排障。
- [ ] 我对 hallucination 至少做了引用强制 / 检索 score 阈值之一。

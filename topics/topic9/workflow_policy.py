"""Topic 9 - Minimal Agent Workflow Demo.

This file is intentionally dependency-free (only stdlib) so you can run it
without installing anything new. It glues together:

  * Router         (rule-based; see route())
  * Planner        (template-based; see make_plan())
  * Executor       (sequential + concurrent; see execute_plan())
  * HITL hook      (only triggers for risky tools; see hitl_gate())
  * Failure guard  (retry / fallback / degrade; see safe_call())
  * Trace          (jsonl-style step log; see _log())

It deliberately uses STUB tools so that the workflow itself is the lesson.
Replace the stubs in TOOLS dict with your real implementations from:

  - src/financial_analyzer.py  (Topic 1)
  - src/rag_pipeline.py        (Topic 4)
  - src/llm_client.py          (Topic 3)

Run from the repository root:

    python topics/topic9/workflow_policy.py

The script prints traces for four representative queries that exercise each
of the four router branches (DIRECT / SINGLE_TOOL / PLAN / REFUSE).
"""

from __future__ import annotations

import json
import random
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable

# ---------------------------------------------------------------------------
# 0. Trace helper - every step in the agent must be observable.
# ---------------------------------------------------------------------------


def _log(trace_id: str, event: str, **fields: Any) -> None:
    """Print a single trace event as one JSON line.

    In production you'd send this to a file / OTel / Logfire. The format is
    intentionally jsonl-friendly so Topic 10 can parse it later.
    """
    payload = {"trace_id": trace_id, "event": event, **fields}
    print(json.dumps(payload, ensure_ascii=False))


# ---------------------------------------------------------------------------
# 1. Tool registry. In a real project these would import from src/.
# ---------------------------------------------------------------------------


def _tool_direct_answer(query: str) -> str:
    """Return a canned educational answer. Replace with src.llm_client."""
    return f"[stub direct answer for] {query}"


def _tool_retrieve_docs(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Pretend to do RAG. Replace with topics/topic4 retriever."""
    if "fail-empty" in query:
        return []
    if "fail-timeout" in query:
        time.sleep(2)
        raise TimeoutError("retrieve_docs took too long")
    return [
        {
            "text": f"[chunk {i}] excerpt about: {query}",
            "source": f"sample_10k_{i}.txt",
            "score": round(0.9 - i * 0.1, 2),
        }
        for i in range(top_k)
    ]


def _tool_analyze_company(name: str) -> dict[str, Any]:
    """Rule-based analysis stub (mirrors src.financial_analyzer)."""
    return {"company": name, "status": "stub", "growth": "unknown"}


def _tool_llm_summarize(inputs: list[Any], template: str) -> str:
    """Pretend to call an LLM. Replace with src.llm_client."""
    return f"[summary using template={template!r} over {len(inputs)} inputs]"


def _tool_append_disclaimer(answer: str) -> str:
    """Append the financial disclaimer (Topic 6)."""
    return (
        f"{answer}\n\n"
        "---\n"
        "本回答仅用于学习与研究目的，不构成任何投资建议。"
    )


# Registry: name -> (callable, is_risky).
# `is_risky=True` will trigger the HITL gate (see §6 of README.md).
TOOLS: dict[str, tuple[Callable[..., Any], bool]] = {
    "direct_answer": (_tool_direct_answer, False),
    "retrieve_docs": (_tool_retrieve_docs, False),
    "analyze_company": (_tool_analyze_company, False),
    "llm_summarize": (_tool_llm_summarize, False),
    "append_disclaimer": (_tool_append_disclaimer, False),
    # Example of a risky tool. We don't actually wire it up to real I/O here,
    # but the HITL path is illustrated in the demo runs at the bottom.
    "send_email": (lambda **_: "email-sent", True),
}


# ---------------------------------------------------------------------------
# 2. Router - rule based, intentionally simple. Add LLM router only if rule
#    misclassification rate exceeds ~10% over a labelled set (see Topic 10).
# ---------------------------------------------------------------------------


REFUSE_KEYWORDS = (
    "should i buy",
    "should i sell",
    "我该买",
    "我该卖",
    "predict price",
    "预测股价",
    "推荐股票",
)
COMPARE_KEYWORDS = ("compare", "vs", "versus", "对比", "比较", "差异")
PLAN_KEYWORDS = ("compare", "vs", "对比", "trend", "演变", "近 3 年", "过去几年")
SINGLE_TOOL_KEYWORDS = (
    "10-k",
    "10-q",
    "财报",
    "risk factor",
    "风险因子",
    "retrieve",
    "查文档",
)

# Tiny company catalog used by COMPARE_COMPANIES route. In production this
# would come from L3 durable memory (a SQLite / Chroma table of company
# profiles). Aliases include English, Chinese and ticker variants so the
# router stays robust to natural phrasing.
KNOWN_COMPANIES: dict[str, str] = {
    "apple": "AAPL", "aapl": "AAPL", "苹果": "AAPL",
    "microsoft": "MSFT", "msft": "MSFT", "微软": "MSFT",
    "google": "GOOG", "alphabet": "GOOG", "goog": "GOOG", "googl": "GOOG", "谷歌": "GOOG",
    "meta": "META", "facebook": "META",
    "tesla": "TSLA", "tsla": "TSLA", "特斯拉": "TSLA",
    "byd": "BYD", "比亚迪": "BYD",
    "nvidia": "NVDA", "nvda": "NVDA", "英伟达": "NVDA",
    "amd": "AMD",
    "amazon": "AMZN", "amzn": "AMZN", "亚马逊": "AMZN",
}


def extract_companies(query: str) -> list[str]:
    """Return canonical tickers mentioned in the query.

    Dedup'd in first-seen order. The lookup is intentionally a dumb substring
    match — replace with a tokenised / fuzzy matcher once you have an eval
    set (Topic 10). For now it's good enough to demonstrate the routing logic.
    """
    q = query.lower()
    seen: list[str] = []
    for alias, ticker in KNOWN_COMPANIES.items():
        if alias in q and ticker not in seen:
            seen.append(ticker)
    return seen


def route(query: str) -> str:
    """Decide one of {DIRECT, SINGLE, PLAN, COMPARE_COMPANIES, REFUSE}."""
    q = query.lower()
    if any(k in q for k in REFUSE_KEYWORDS):
        return "REFUSE"
    # COMPARE_COMPANIES is more specific than PLAN — check it first, and only
    # accept when ≥2 KNOWN companies are present so that "compare ROE vs ROI"
    # (no companies) still falls through to the generic PLAN route.
    if any(k in q for k in COMPARE_KEYWORDS) and len(extract_companies(query)) >= 2:
        return "COMPARE_COMPANIES"
    if any(k in q for k in PLAN_KEYWORDS):
        return "PLAN"
    if any(k in q for k in SINGLE_TOOL_KEYWORDS):
        return "SINGLE"
    return "DIRECT"


# ---------------------------------------------------------------------------
# 3. Planner - template-based plans. In Topic 10 you'd evaluate plan quality
#    on a golden set; once stable you can swap to an LLM planner.
# ---------------------------------------------------------------------------


@dataclass
class Step:
    step: int
    intent: str
    tool: str
    args: dict[str, Any]
    expects: str
    fallback_step: int | None = None
    parallel_group: int | None = None  # steps in the same group can run together


@dataclass
class Plan:
    route: str
    steps: list[Step] = field(default_factory=list)
    max_retries_per_step: int = 2
    max_replans: int = 2


def make_plan(route_label: str, query: str) -> Plan:
    """Produce a Plan based on the route. Pure function, easy to unit test."""
    if route_label == "DIRECT":
        return Plan(
            route="DIRECT",
            steps=[
                Step(1, "answer directly", "direct_answer", {"query": query},
                     expects="non-empty string"),
                Step(2, "attach disclaimer", "append_disclaimer",
                     {"answer": "<<step1>>"}, expects="answer + disclaimer"),
            ],
        )

    if route_label == "SINGLE":
        return Plan(
            route="SINGLE",
            steps=[
                Step(1, "retrieve relevant chunks", "retrieve_docs",
                     {"query": query, "top_k": 5},
                     expects=">=1 chunk with source"),
                Step(2, "summarise grounded answer", "llm_summarize",
                     {"inputs": "<<step1>>", "template": "grounded-qa"},
                     expects="non-empty summary"),
                Step(3, "attach disclaimer", "append_disclaimer",
                     {"answer": "<<step2>>"}, expects="final text"),
            ],
        )

    if route_label == "COMPARE_COMPANIES":
        # Dynamic plan: N parallel retrievals (one per company) + summary + disclaimer.
        # Steps are numbered 1..N for retrievals, N+1 for summary, N+2 for disclaimer.
        companies = extract_companies(query)
        steps: list[Step] = []
        for i, ticker in enumerate(companies, start=1):
            steps.append(Step(
                i,
                f"retrieve latest disclosures for {ticker}",
                "retrieve_docs",
                {"query": f"{ticker} latest risk factors and strategy", "top_k": 3},
                expects=">=1 chunk",
                parallel_group=1,
            ))
        summary_idx = len(companies) + 1
        steps.append(Step(
            summary_idx,
            f"compare {len(companies)} companies side-by-side",
            "llm_summarize",
            {
                "inputs": f"<<step1..{len(companies)}>>",
                "template": f"compare-{len(companies)}-companies",
            },
            expects="comparison text",
        ))
        steps.append(Step(
            summary_idx + 1,
            "attach disclaimer",
            "append_disclaimer",
            {"answer": f"<<step{summary_idx}>>"},
            expects="final text",
        ))
        return Plan(route="COMPARE_COMPANIES", steps=steps)

    if route_label == "PLAN":
        # A toy multi-step plan illustrating parallelism (single-company trend).
        return Plan(
            route="PLAN",
            steps=[
                Step(1, "Apple 2022 risks", "retrieve_docs",
                     {"query": "Apple 2022 risk factors", "top_k": 3},
                     expects=">=1 chunk", parallel_group=1),
                Step(2, "Apple 2023 risks", "retrieve_docs",
                     {"query": "Apple 2023 risk factors", "top_k": 3},
                     expects=">=1 chunk", parallel_group=1),
                Step(3, "Apple 2024 risks", "retrieve_docs",
                     {"query": "Apple 2024 risk factors", "top_k": 3},
                     expects=">=1 chunk", parallel_group=1),
                Step(4, "summarise trend", "llm_summarize",
                     {"inputs": "<<step1..3>>", "template": "trend-3y"},
                     expects="trend summary"),
                Step(5, "attach disclaimer", "append_disclaimer",
                     {"answer": "<<step4>>"}, expects="final text"),
            ],
        )

    # REFUSE
    return Plan(
        route="REFUSE",
        steps=[
            Step(1, "polite refusal", "direct_answer",
                 {"query": "投资建议拒绝模板"},
                 expects="refusal string"),
            Step(2, "attach disclaimer", "append_disclaimer",
                 {"answer": "<<step1>>"}, expects="final text"),
        ],
    )


# ---------------------------------------------------------------------------
# 4. HITL gate - blocks risky tools until a human confirms.
#    For automated demo / CI we read from `auto_decision`. In production this
#    becomes an interactive prompt (input()) or a UI confirmation event.
# ---------------------------------------------------------------------------


@dataclass
class HitlDecision:
    approve: bool
    reason: str = ""


def hitl_gate(
    trace_id: str, step: Step, auto_decision: HitlDecision | None = None
) -> bool:
    """Return True if the step is allowed to proceed, False otherwise.

    By default (auto_decision=None) **denies** risky steps. This is the safe
    default for CI / automated runs. UIs should swap in an interactive prompt.
    """
    fn, is_risky = TOOLS[step.tool]
    if not is_risky:
        return True

    decision = auto_decision or HitlDecision(approve=False,
                                             reason="default-deny in demo mode")
    _log(
        trace_id,
        "hitl",
        step=step.step,
        tool=step.tool,
        approved=decision.approve,
        reason=decision.reason,
    )
    return decision.approve


# ---------------------------------------------------------------------------
# 5. Failure guard - retry / fallback / degrade.
# ---------------------------------------------------------------------------


@dataclass
class StepResult:
    ok: bool
    step: Step
    result: Any = None
    error: str | None = None
    attempts: int = 0
    elapsed_ms: int = 0


def safe_call(trace_id: str, step: Step, max_retries: int) -> StepResult:
    """Execute a step with bounded retries and tagged error categories."""
    fn, _ = TOOLS[step.tool]
    started = time.time()
    last_err: str | None = None

    for attempt in range(1, max_retries + 2):  # initial + retries
        try:
            result = fn(**step.args)
            elapsed = int((time.time() - started) * 1000)
            _log(trace_id, "step.ok", step=step.step, tool=step.tool,
                 attempt=attempt, elapsed_ms=elapsed)
            # Empty-result detection - treated as soft failure for retrieve_docs.
            if step.tool == "retrieve_docs" and not result:
                last_err = "empty"
                _log(trace_id, "step.empty", step=step.step, attempt=attempt)
                # one retry with a relaxed query, then give up
                if attempt <= 1:
                    step.args = {**step.args, "top_k": int(step.args.get("top_k", 3)) + 2}
                    continue
                return StepResult(ok=False, step=step, error="empty",
                                  attempts=attempt, elapsed_ms=elapsed)
            return StepResult(ok=True, step=step, result=result,
                              attempts=attempt, elapsed_ms=elapsed)
        except TimeoutError as e:
            last_err = f"timeout: {e}"
            _log(trace_id, "step.timeout", step=step.step, attempt=attempt)
            time.sleep(0.05 * attempt + random.random() * 0.05)  # backoff + jitter
        except Exception as e:  # noqa: BLE001 - we want to log & categorize
            last_err = f"{type(e).__name__}: {e}"
            _log(trace_id, "step.error", step=step.step, attempt=attempt,
                 error=last_err)
            # 4xx-like errors should not be blindly retried; for the demo we
            # break on any non-timeout exception.
            break

    elapsed = int((time.time() - started) * 1000)
    return StepResult(ok=False, step=step, error=last_err or "unknown",
                      attempts=attempt, elapsed_ms=elapsed)


# ---------------------------------------------------------------------------
# 6. Executor - resolves <<stepN>> placeholders, runs sequential or grouped.
# ---------------------------------------------------------------------------


def _resolve_args(args: dict[str, Any], outputs: dict[int, Any]) -> dict[str, Any]:
    """Replace `<<stepN>>` placeholders with actual prior outputs.

    Supports a tiny mini-syntax:
      - "<<step3>>"        → outputs[3]
      - "<<step1..4>>"     → [outputs[1], outputs[2], outputs[3], outputs[4]]
    """
    resolved: dict[str, Any] = {}
    for key, value in args.items():
        if isinstance(value, str) and value.startswith("<<step") and value.endswith(">>"):
            inner = value[2:-2].removeprefix("step")
            if ".." in inner:
                lo, hi = (int(x) for x in inner.split(".."))
                resolved[key] = [outputs[i] for i in range(lo, hi + 1)
                                 if i in outputs]
            else:
                resolved[key] = outputs.get(int(inner))
        else:
            resolved[key] = value
    return resolved


def execute_plan(plan: Plan, hitl_auto: HitlDecision | None = None) -> dict[int, Any]:
    """Run a Plan and return {step_number: result}. Stops on first hard failure."""
    trace_id = uuid.uuid4().hex[:8]
    _log(trace_id, "plan.start", route=plan.route, n_steps=len(plan.steps))

    outputs: dict[int, Any] = {}

    # Group steps that can run in parallel together; the rest run serially.
    grouped: list[list[Step]] = []
    current: list[Step] = []
    last_group: int | None = -1
    for step in plan.steps:
        if step.parallel_group is not None and step.parallel_group == last_group:
            current.append(step)
        else:
            if current:
                grouped.append(current)
            current = [step]
            last_group = step.parallel_group
    if current:
        grouped.append(current)

    for batch in grouped:
        if len(batch) == 1:
            step = batch[0]
            step.args = _resolve_args(step.args, outputs)
            if not hitl_gate(trace_id, step, hitl_auto):
                _log(trace_id, "plan.aborted", reason="hitl_denied",
                     step=step.step)
                return outputs
            res = safe_call(trace_id, step, plan.max_retries_per_step)
            if not res.ok:
                _log(trace_id, "plan.failed", step=step.step, error=res.error)
                return outputs
            outputs[step.step] = res.result
        else:
            # Run a parallel group concurrently. Args are resolved against the
            # outputs available *before* the group started.
            with ThreadPoolExecutor(max_workers=min(4, len(batch))) as pool:
                futures = []
                for step in batch:
                    step.args = _resolve_args(step.args, outputs)
                    if not hitl_gate(trace_id, step, hitl_auto):
                        _log(trace_id, "plan.aborted", reason="hitl_denied",
                             step=step.step)
                        return outputs
                    futures.append(
                        (step, pool.submit(safe_call, trace_id, step,
                                           plan.max_retries_per_step))
                    )
                for step, fut in futures:
                    res = fut.result()
                    if not res.ok:
                        _log(trace_id, "plan.failed", step=step.step,
                             error=res.error)
                        return outputs
                    outputs[step.step] = res.result

    _log(trace_id, "plan.done", produced_steps=list(outputs.keys()))
    return outputs


# ---------------------------------------------------------------------------
# 7. Top-level entry: take a query, route, plan, execute.
# ---------------------------------------------------------------------------


def handle_query(query: str) -> Any:
    print(f"\n=== Q: {query} ===")
    route_label = route(query)
    print(f"[ROUTE={route_label}]")
    plan = make_plan(route_label, query)
    outputs = execute_plan(plan)
    final = outputs.get(max(outputs.keys())) if outputs else None
    print(f"[FINAL] {final}\n")
    return final


# ---------------------------------------------------------------------------
# 8. Demo. Each query exercises a different router branch and a different
#    failure mode (so you can see the recovery story end to end).
# ---------------------------------------------------------------------------


def main() -> None:
    handle_query("什么是 ROE")  # DIRECT
    handle_query("帮我查 Apple 10-K 的 risk factors")  # SINGLE
    handle_query("Apple 近 3 年的风险因子演变趋势")  # PLAN (single-company trend)
    handle_query("我该买 Apple 吗")  # REFUSE
    print("--- failure scenarios ---")
    handle_query("查文档 fail-empty")     # empty-result recovery
    # NOTE: timeout demo is commented to keep CI fast. Uncomment to see the
    # retry + give-up path:
    # handle_query("查文档 fail-timeout")

    print("\n--- compare-companies route (practice #2) ---")
    # 1. en + 2 companies: classic comparison
    handle_query("Compare Apple and Microsoft on AI strategy")
    # 2. zh + 2 companies, mixed-script aliases
    handle_query("对比 Tesla 和 BYD 的最新风险因子")
    # 3. zh + 3 companies, mix of Chinese aliases and English brand
    handle_query("对比 苹果、谷歌、Meta 三家公司")
    # 4. mixed + 4 companies (stress test for parallel group sizing)
    handle_query("对比 NVDA、AMD、Apple、Microsoft 在 AI 上的战略差异")
    # 5. compare keyword but 0 known companies → falls back to PLAN
    handle_query("Compare ROE vs ROI")


if __name__ == "__main__":
    main()

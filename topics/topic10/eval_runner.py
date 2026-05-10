"""Topic 10 — 黄金集路由回归评测（stdlib only）。

从仓库根目录运行::

    python topics/topic10/eval_runner.py

可选::

    python topics/topic10/eval_runner.py --golden topics/topic10/golden_set.jsonl --out topics/topic10/eval_report.md

评测对象：Topic 9 ``workflow_policy.route()``；若黄金集中含 ``expected_tools``，可用 ``--check-tools`` 校验 ``make_plan`` 工具序列。

替换 Router 关键词或 Planner 模板后重新运行，即可对比两版「工作流」的准确率。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def _load_workflow_policy(repo_root: Path):
    path = repo_root / "topics" / "topic9" / "workflow_policy.py"
    # Stable unique name + sys.modules registration avoids dataclass errors on
    # exec_module (Python 3.9–3.11).
    mod_name = "_topic9_workflow_policy_eval"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_golden(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def plan_tool_sequence(wp, route_label: str, query: str) -> list[str]:
    plan = wp.make_plan(route_label, query)
    return [s.tool for s in plan.steps]


def main() -> int:
    parser = argparse.ArgumentParser(description="Golden-set route evaluation for Topic 10.")
    parser.add_argument(
        "--golden",
        type=Path,
        default=None,
        help="Path to golden_set.jsonl (default: sibling golden_set.jsonl)",
    )
    parser.add_argument("--out", type=Path, default=None, help="Write markdown report to this path.")
    parser.add_argument("--label", default="default", help="Run label for the report header.")
    parser.add_argument(
        "--check-tools",
        action="store_true",
        help="If golden rows include expected_tools, verify full tool sequence.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    golden_path = args.golden or (Path(__file__).resolve().parent / "golden_set.jsonl")

    wp = _load_workflow_policy(repo_root)
    cases = load_golden(golden_path)

    tag_pass: Counter[str] = Counter()
    tag_total: Counter[str] = Counter()
    route_mismatches: list[dict] = []
    tool_mismatches: list[dict] = []

    for row in cases:
        q = row["query"]
        exp_route = row["expected_route"]
        actual_route = wp.route(q)

        for t in row.get("tags") or []:
            tag_total[t] += 1
            if actual_route == exp_route:
                tag_pass[t] += 1

        if actual_route != exp_route:
            route_mismatches.append(row)
            continue

        if args.check_tools and "expected_tools" in row:
            tools = plan_tool_sequence(wp, actual_route, q)
            exp_tools = row["expected_tools"]
            if tools != exp_tools:
                tool_mismatches.append(
                    {
                        "id": row.get("id", ""),
                        "query": q,
                        "expected_tools": exp_tools,
                        "actual_tools": tools,
                    }
                )

    n = len(cases)
    route_ok = n - len(route_mismatches)
    route_acc = route_ok / n if n else 0.0

    lines = [
        f"# Eval Report — `{args.label}`",
        "",
        f"- Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"- Golden file: `{golden_path}`",
        f"- Cases: **{n}**",
        f"- Route accuracy: **{route_acc:.1%}** ({route_ok}/{n})",
        "",
    ]

    if route_mismatches:
        lines.extend(["## Route mismatches", ""])
        for row in route_mismatches:
            q = row["query"]
            ar = wp.route(q)
            lines.append(
                f"- **{row.get('id', '')}** expected `{row['expected_route']}` "
                f"got `{ar}` — {q[:120]}"
            )
        lines.append("")
    else:
        lines.extend(["## Route mismatches", "", "*None.*", ""])

    if args.check_tools:
        lines.append("## Tool sequence mismatches")
        lines.append("")
        if tool_mismatches:
            for tm in tool_mismatches:
                lines.append(f"- **{tm['id']}** {tm['query'][:80]}")
                lines.append(f"  - expected: `{tm['expected_tools']}`")
                lines.append(f"  - actual: `{tm['actual_tools']}`")
            lines.append("")
        else:
            lines.extend(["*None (or no expected_tools in golden set).*", ""])

    if tag_total:
        lines.extend(["## Tags", "", "| tag | pass / total |", "|-----|--------------|"])
        for tag in sorted(tag_total.keys()):
            lines.append(f"| {tag} | {tag_pass[tag]} / {tag_total[tag]} |")
        lines.append("")

    lines.extend(
        [
            "## Next steps",
            "",
            "- 改 Router 后重新运行，对比两次报告。",
            "- 把 `workflow_policy` 的 jsonl trace 接到日志文件，按 `observability_metrics.md` 聚合。",
            "- RAG 命中类指标见 `rag_eval.md`，需单独准备带 chunk 标注的数据集。",
            "",
        ]
    )
    report = "\n".join(lines)

    print(report)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"\n[written] {args.out}", file=sys.stderr)

    failed = bool(route_mismatches or (args.check_tools and tool_mismatches))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

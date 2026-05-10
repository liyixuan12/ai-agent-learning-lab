"""Topic 9 - Three-layer memory store for the FinSight agent.

This file shows the minimum mental model:

    L1 Session  →  in-memory dict     (cleared every new conversation)
    L2 Project  →  JSON file on disk  (per-project preferences / cache)
    L3 Durable  →  pluggable backend  (vector DB / SQLite / Postgres)

It is dependency-free and runs as a self-contained demo:

    python topics/topic9/memory_store.py

It deliberately does NOT use any cloud / vendor SDK so you can read every
line and decide later which row goes into which layer when wiring it into
the final FinSight demo.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# L1: Session memory  -- lives in process, cleared by `reset()`.
# ---------------------------------------------------------------------------


@dataclass
class SessionMemory:
    """Per-conversation scratchpad.

    Holds:
      * recent turns (capped to keep prompts cheap)
      * intermediate results between Plan steps (resolved by Executor)

    Never put: passwords, durable preferences, anything that should outlive
    the current chat tab.
    """

    max_turns: int = 10
    turns: list[dict[str, str]] = field(default_factory=list)
    scratchpad: dict[str, Any] = field(default_factory=dict)

    def add_turn(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content,
                           "ts": int(time.time())})
        if len(self.turns) > self.max_turns:
            # drop the oldest turn first
            self.turns = self.turns[-self.max_turns:]

    def remember(self, key: str, value: Any) -> None:
        self.scratchpad[key] = value

    def recall(self, key: str, default: Any = None) -> Any:
        return self.scratchpad.get(key, default)

    def reset(self) -> None:
        self.turns.clear()
        self.scratchpad.clear()


# ---------------------------------------------------------------------------
# L2: Project memory  -- persisted as JSON on disk per project root.
# ---------------------------------------------------------------------------


class ProjectMemory:
    """User / project preferences that should outlive a single chat session.

    Stored as a single JSON file (default: `./.topic9/project_memory.json`).
    Use `set/get` for arbitrary preferences; `add_to_list/list_get` for
    accumulating items like a watchlist.
    """

    def __init__(self, path: str | os.PathLike[str] = ".topic9/project_memory.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def _load(self) -> dict[str, Any]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # Self-heal: if the file got corrupted (e.g. interrupted write),
            # reset to empty rather than crash the whole agent.
            self.path.write_text("{}", encoding="utf-8")
            return {}

    def _save(self, data: dict[str, Any]) -> None:
        # Write atomically: write to a tmp file then rename, so a crash mid-
        # write can't leave a partial JSON behind.
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        tmp.replace(self.path)

    def set(self, key: str, value: Any) -> None:
        data = self._load()
        data[key] = value
        self._save(data)

    def get(self, key: str, default: Any = None) -> Any:
        return self._load().get(key, default)

    def add_to_list(self, key: str, item: Any) -> list[Any]:
        data = self._load()
        items = list(data.get(key, []))
        if item not in items:
            items.append(item)
        data[key] = items
        self._save(data)
        return items

    def list_get(self, key: str) -> list[Any]:
        return list(self._load().get(key, []))

    def all(self) -> dict[str, Any]:
        return self._load()


# ---------------------------------------------------------------------------
# L3: Durable memory -- abstract base, plug in Chroma / SQLite / Postgres.
# ---------------------------------------------------------------------------


class DurableMemory:
    """Abstract long-term memory.

    Subclass this with your real backend in Topic 10+. The default impl is
    an in-memory dict so the demo runs without external services.
    """

    def __init__(self) -> None:
        self._kv: dict[str, Any] = {}

    def write(self, key: str, value: Any, *, source: str | None = None) -> None:
        # Audit fields encourage callers to think about provenance early.
        self._kv[key] = {
            "value": value,
            "source": source,
            "ts": int(time.time()),
        }

    def read(self, key: str) -> Any | None:
        record = self._kv.get(key)
        return record["value"] if record else None

    def search(self, query: str, *, top_k: int = 3) -> list[dict[str, Any]]:
        """Stub semantic search - replace with Chroma / FAISS in real life."""
        results = []
        for key, record in self._kv.items():
            if query.lower() in str(record["value"]).lower() or query.lower() in key.lower():
                results.append({"key": key, **record})
        return results[:top_k]

    def keys(self) -> Iterable[str]:
        return self._kv.keys()


# ---------------------------------------------------------------------------
# Convenience: bundled memory used by the agent.
# ---------------------------------------------------------------------------


@dataclass
class AgentMemory:
    session: SessionMemory = field(default_factory=SessionMemory)
    project: ProjectMemory = field(default_factory=ProjectMemory)
    durable: DurableMemory = field(default_factory=DurableMemory)


# ---------------------------------------------------------------------------
# Demo: shows what belongs in each layer.
# ---------------------------------------------------------------------------


def main() -> None:
    mem = AgentMemory()

    print("--- L1 session ---")
    mem.session.add_turn("user", "我重点关注 Apple 和 Microsoft")
    mem.session.add_turn("agent", "明白，我会重点跟进这两家")
    mem.session.remember("last_retrieved_chunks",
                         [{"text": "Apple risk factors..."}])
    print("turns:", mem.session.turns)
    print("scratchpad keys:", list(mem.session.scratchpad.keys()))

    print("\n--- L2 project (persisted to ./.topic9/project_memory.json) ---")
    mem.project.add_to_list("watchlist", "AAPL")
    mem.project.add_to_list("watchlist", "MSFT")
    mem.project.set("preferred_lang", "zh-CN")
    print("watchlist:", mem.project.list_get("watchlist"))
    print("preferred_lang:", mem.project.get("preferred_lang"))

    print("\n--- L3 durable (in-memory stub - swap for Chroma in real demo) ---")
    mem.durable.write("company:AAPL:profile",
                      {"name": "Apple Inc.", "ticker": "AAPL"},
                      source="seed-data")
    mem.durable.write("company:MSFT:profile",
                      {"name": "Microsoft", "ticker": "MSFT"},
                      source="seed-data")
    print("read AAPL:", mem.durable.read("company:AAPL:profile"))
    print("search 'apple':", mem.durable.search("apple"))

    print("\n--- session reset ---")
    mem.session.reset()
    print("turns after reset:", mem.session.turns)
    print("project still has watchlist:", mem.project.list_get("watchlist"))


if __name__ == "__main__":
    main()

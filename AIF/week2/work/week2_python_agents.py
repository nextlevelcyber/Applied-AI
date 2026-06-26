from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)


def python_basics_demo() -> dict:
    a, b = 12, 5
    words = ["agent", "percept", "action", "environment"]
    return {
        "arithmetic": {"a": a, "b": b, "sum": a + b, "product": a * b, "power": a**b},
        "string_slice": "Artificial Intelligence"[:10],
        "list_first_last": [words[0], words[-1]],
        "dictionary": {"agent": "entity that perceives and acts"},
    }


@dataclass
class VacuumWorld:
    location: str = "A"
    dirt: dict[str, bool] | None = None

    def __post_init__(self) -> None:
        if self.dirt is None:
            self.dirt = {"A": True, "B": True}

    def percept(self) -> tuple[str, str]:
        return self.location, "Dirty" if self.dirt[self.location] else "Clean"

    def act(self, action: str) -> int:
        if action == "Suck" and self.dirt[self.location]:
            self.dirt[self.location] = False
            return 10
        if action == "Right":
            self.location = "B"
            return -1
        if action == "Left":
            self.location = "A"
            return -1
        return -1


def reflex_vacuum_agent(percept: tuple[str, str]) -> str:
    location, status = percept
    if status == "Dirty":
        return "Suck"
    return "Right" if location == "A" else "Left"


def run_vacuum_world(steps: int = 6) -> dict:
    env = VacuumWorld()
    trace = []
    total_reward = 0
    for step in range(steps):
        percept = env.percept()
        action = reflex_vacuum_agent(percept)
        reward = env.act(action)
        total_reward += reward
        trace.append({"step": step + 1, "percept": percept, "action": action, "reward": reward})
    return {"trace": trace, "total_reward": total_reward, "final_dirt": env.dirt}


def main() -> None:
    results = {
        "python_basics": python_basics_demo(),
        "reflex_agent_simulation": run_vacuum_world(),
    }
    (RESULTS / "week2_python_agents_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

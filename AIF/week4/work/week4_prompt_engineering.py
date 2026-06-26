from __future__ import annotations

import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)


def build_prompt(task: str, context: str, constraints: list[str]) -> str:
    constraint_text = "\n".join(f"- {item}" for item in constraints)
    return f"""Task:
{task}

Context:
{context}

Constraints:
{constraint_text}

Respond with:
1. A concise answer.
2. Your reasoning steps.
3. Any assumptions or limitations.
"""


def classify_prompt(prompt: str) -> str:
    text = prompt.lower()
    if "step by step" in text or "reasoning" in text:
        return "chain-of-thought style prompt"
    if "example" in text:
        return "few-shot prompt"
    return "zero-shot prompt"


def main() -> None:
    prompts = [
        {
            "name": "zero_shot_summary",
            "prompt": build_prompt(
                "Summarise the commercial risks of deploying a chatbot in customer support.",
                "A retail company wants to use an LLM chatbot for first-line support.",
                ["Use plain language", "Mention privacy, accuracy, and escalation"],
            ),
        },
        {
            "name": "cot_planning",
            "prompt": build_prompt(
                "Plan step by step how to evaluate a simple AI agent.",
                "The agent receives observations and chooses actions in a small environment.",
                ["Include metrics", "Include failure cases", "Keep the plan testable"],
            ),
        },
        {
            "name": "few_shot_classification",
            "prompt": (
                "Classify each request as factual, creative, or planning.\n"
                "Example: 'Write a poem' -> creative\n"
                "Example: 'What is reinforcement learning?' -> factual\n"
                "Request: 'Design an AI coursework plan' ->"
            ),
        },
    ]
    for item in prompts:
        item["type"] = classify_prompt(item["prompt"])

    (RESULTS / "week4_prompt_engineering_results.json").write_text(
        json.dumps(prompts, indent=2), encoding="utf-8"
    )
    (RESULTS / "week4_prompt_examples.md").write_text(
        "\n\n".join(f"## {p['name']}\n\nType: {p['type']}\n\n```text\n{p['prompt']}\n```" for p in prompts),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

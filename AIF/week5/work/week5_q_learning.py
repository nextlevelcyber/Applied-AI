from __future__ import annotations

import json
import random
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)


STATES = ["start", "middle", "goal"]
ACTIONS = ["left", "right"]


def transition(state: str, action: str) -> tuple[str, int, bool]:
    if state == "goal":
        return "goal", 0, True
    if state == "start":
        return ("middle", -1, False) if action == "right" else ("start", -2, False)
    if state == "middle":
        return ("goal", 10, True) if action == "right" else ("start", -1, False)
    raise ValueError(state)


def choose_action(q: dict[str, dict[str, float]], state: str, epsilon: float) -> str:
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    values = q[state]
    return max(values, key=values.get)


def train(episodes: int = 300, alpha: float = 0.2, gamma: float = 0.9, epsilon: float = 0.15) -> dict:
    random.seed(42)
    q = {state: {action: 0.0 for action in ACTIONS} for state in STATES}
    episode_rewards = []
    for _ in range(episodes):
        state = "start"
        total_reward = 0
        for _step in range(10):
            action = choose_action(q, state, epsilon)
            next_state, reward, done = transition(state, action)
            total_reward += reward
            best_next = max(q[next_state].values())
            q[state][action] += alpha * (reward + gamma * best_next - q[state][action])
            state = next_state
            if done:
                break
        episode_rewards.append(total_reward)
    policy = {state: max(q[state], key=q[state].get) for state in STATES}
    return {
        "q_table": {s: {a: round(v, 3) for a, v in actions.items()} for s, actions in q.items()},
        "policy": policy,
        "average_reward_last_25": round(sum(episode_rewards[-25:]) / 25, 3),
        "episodes": episodes,
    }


def main() -> None:
    result = train()
    (RESULTS / "week5_q_learning_results.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

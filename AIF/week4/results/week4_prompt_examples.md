## zero_shot_summary

Type: chain-of-thought style prompt

```text
Task:
Summarise the commercial risks of deploying a chatbot in customer support.

Context:
A retail company wants to use an LLM chatbot for first-line support.

Constraints:
- Use plain language
- Mention privacy, accuracy, and escalation

Respond with:
1. A concise answer.
2. Your reasoning steps.
3. Any assumptions or limitations.

```

## cot_planning

Type: chain-of-thought style prompt

```text
Task:
Plan step by step how to evaluate a simple AI agent.

Context:
The agent receives observations and chooses actions in a small environment.

Constraints:
- Include metrics
- Include failure cases
- Keep the plan testable

Respond with:
1. A concise answer.
2. Your reasoning steps.
3. Any assumptions or limitations.

```

## few_shot_classification

Type: few-shot prompt

```text
Classify each request as factual, creative, or planning.
Example: 'Write a poem' -> creative
Example: 'What is reinforcement learning?' -> factual
Request: 'Design an AI coursework plan' ->
```
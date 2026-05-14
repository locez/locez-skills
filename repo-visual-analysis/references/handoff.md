# Optional Handoff

This skill must not require external brainstorming, design, or planning skills. A repository analysis report is complete when it provides useful visual maps, evidence-backed observations, and next-step opportunities.

Use a handoff only when the user selects an opportunity and wants to develop it into a concrete design.

## Handoff Package

Pass only relevant context:

- Repository summary.
- Selected opportunity.
- Relevant diagrams or visual model excerpts.
- Supporting evidence.
- Risks, constraints, and confidence level.
- Open questions.
- Suggested small/medium/large directions if already identified.

Do not pass the entire report unless needed.

## If A Brainstorming/Design Skill Exists

Invoke it only after the user asks to develop or design an opportunity. Tell it:

```text
Use this repository evidence as context. Do not re-summarize the whole repo unless needed.
Develop the selected opportunity into a design. Preserve uncertainty and ask for clarification where repository evidence is incomplete.
```

## If No Brainstorming/Design Skill Exists

Continue manually:

1. Ask what outcome the user wants from the selected opportunity.
2. Offer 2-3 implementation/design directions.
3. Recommend one based on repository evidence.
4. Stop before implementation unless the user asks to proceed.

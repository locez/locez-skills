# Workflow Skill Architect Repository Integration

## Context

`workflow-skill-architect` was created locally under `~/.codex/skills/workflow-skill-architect/` and is now tracked in this repository so it can be reused across machines and evolved alongside the other local skills.

## Skill Purpose

The skill helps convert complex tasks or overloaded skills into structured workflow skills. It is intended for cases where the main prompt has absorbed too much responsibility, worker agents lack contracts, human confirmation points are scattered, artifacts are unclear, validation is weak, or independent stages are needlessly serialized.

## Repository Placement

The copied skill lives at:

```text
workflow-skill-architect/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── agent-contracts.md
    ├── agent-set-activation.md
    ├── concurrency.md
    ├── data-cleaning-template.md
    ├── refactor-levels.md
    └── workflow-refactoring.md
```

No README or changelog is added inside the skill directory. The skill directory stays focused on files the agent should use at runtime; repository-level explanation belongs in the root `README.md` and this spec.

## Design Notes

- `SKILL.md` remains the orchestrator entry point.
- `references/agent-contracts.md` defines worker contract templates and boundary tests.
- `references/agent-set-activation.md` defines when to stay single-agent and when to use a review agent set.
- `references/concurrency.md` defines dependency labels, safe parallelism, barriers, and shared-write rules.
- `references/workflow-refactoring.md` covers converting overloaded skills into orchestrated workflows.
- `references/data-cleaning-template.md` provides a domain template for data-cleaning workflow skills.
- `references/refactor-levels.md` defines recommendation levels from `no-op` through `template-extract`.
- `agents/openai.yaml` supplies UI metadata for Codex skill listing and invocation.

## Validation Expectations

When this skill changes, verify:

- frontmatter includes `name` and trigger-focused `description`;
- `SKILL.md` directly references each file in `references/`;
- no competing workflow entry point exists outside `SKILL.md`;
- artifact, concurrency, and sub-agent guidance remain traceable through the references;
- recommendation levels and agent set activation rules are represented in both `SKILL.md` and references;
- repository docs list the skill and show an invocation example.

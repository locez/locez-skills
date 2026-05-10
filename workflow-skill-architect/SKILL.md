---
name: workflow-skill-architect
description: Use when creating or refactoring a skill for a complex multi-step task, especially when an existing skill has an overloaded main prompt, unclear sub-agent responsibilities, repeated human confirmations, missing intermediate artifacts, weak validation, or a need to turn domain-specific work such as data cleaning into a structured workflow skill.
---

# Workflow Skill Architect

## Overview

Use this skill to turn complex tasks or poorly structured skills into workflow skills with clear orchestration, sub-agent contracts, structured artifacts, review gates, concurrency boundaries, and validation. Treat a skill as a workflow entry point, not as a long prompt that does all work itself.

## Core Rule

Do not make the main `SKILL.md` carry the whole task. Keep it responsible for activation, orchestration rules, resource navigation, and stop conditions. Move domain knowledge, detailed procedures, templates, examples, and reusable prompts into `references/`; move deterministic repeated work into `scripts/` when scripts are available.

## Workflow

### 1. Intake

Identify whether the input is:

- An existing skill to refactor.
- A new complex task that should become a skill.
- A domain-specific template request, such as data cleaning.

For an existing skill, extract its current goal, user-facing trigger, inputs, outputs, workflow steps, tools, confirmation points, and failure modes. For a new skill, infer those from the user's task description and ask only for missing information that changes the architecture.

### 2. Diagnose Architecture Smells

Look for these problems:

- Main prompt performs analysis, planning, execution, validation, and reporting.
- Business rules are mixed with execution steps.
- Confirmation questions interrupt the workflow instead of batching uncertainty.
- No explicit intermediate artifacts.
- Sub-agents are absent, duplicated, or only named without input/output contracts.
- Independent work is forced through a serial main flow even though it could run concurrently.
- Deterministic work is done by model reasoning instead of scripts or structured procedures.
- Final output is not traceable back to rules, inputs, and decisions.

### 3. Split Responsibilities

Separate the workflow into an orchestrator and focused workers. The orchestrator owns sequencing, state, artifact routing, user review gates, and final synthesis. Worker agents own bounded transformations, such as profiling, domain analysis, rule design, execution, validation, exception triage, or querying.

Use `references/agent-contracts.md` when defining sub-agents.

### 4. Define Dependency And Concurrency Map

Mark each stage as serial, parallelizable, or barrier. Parallelizable stages have independent inputs and do not write the same artifact. Barrier stages wait for upstream artifacts before continuing. Use `references/concurrency.md` when deciding what can safely run concurrently.

### 5. Decide Whether To Activate Agent Set

Default to single-agent analysis. Activate an agent set only for large, high-risk, actual-refactor, batch, or multi-dimensional reviews where parallel reviewers add real signal. If activated, include an anti-overengineering reviewer. Use `references/agent-set-activation.md`.

### 6. Assign Recommendation Level

Before recommending structure, assign the smallest useful change level: `no-op`, `small-polish`, `protocolize`, `split`, `rebuild`, or `template-extract`. Use `references/refactor-levels.md`.

### 7. Define Artifact Protocols

Every major stage must produce an artifact that the next stage can consume. Prefer structured files or tightly specified Markdown sections. Examples:

- `intake-summary.md`
- `domain-model.md`
- `workflow-plan.md`
- `agent-contracts.md`
- `rules.yaml`
- `validation-report.md`
- `exceptions.csv`
- `handoff-summary.md`

If an artifact does not change downstream behavior, remove it.

For read-only architecture analysis, do not force artifact files. The final answer can be the artifact. Add artifact protocols only when the task involves actual refactoring, persistent outputs, batch migration, or repeatable execution.

### 8. Compress Human Review

Replace scattered confirmation prompts with review gates. Each gate should present grouped decisions, defaults, impact, and unresolved risk. Confirmations should update rules or references so the same issue is not asked again on the next run.

### 9. Build the New Skill Structure

Recommended target skill structure:

These are example files for generated or refactored skills, not required files for this skill itself.

```text
target-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── agent-contracts.md
│   ├── agent-set-activation.md
│   ├── concurrency.md
│   ├── domain-model.md
│   ├── rules.md
│   ├── validation.md
│   └── query-guide.md
└── scripts/
    └── optional deterministic helpers
```

`agents/openai.yaml` is UI metadata for skill listings and default prompts. Worker or sub-agent contracts belong in `references/agent-contracts.md`.

Only create directories and files that the target skill needs. Do not add README, installation guides, changelogs, or narrative docs.

### 10. Validate

Validate both structure and behavior:

- Run the platform skill validator when available, such as `quick_validate.py <skill-folder>` in Codex skill-creator environments. If no validator exists, do a manual structural check.
- Check that frontmatter describes triggering conditions.
- Confirm `SKILL.md` can be understood without loading every reference.
- Confirm each referenced file is directly linked from `SKILL.md`.
- Confirm legacy workflow files are either integrated or explicitly demoted to cookbook/reference status.
- Confirm independent stages are marked for concurrent execution and shared-write hazards are blocked.
- Confirm the final recommendation includes a change level from `references/refactor-levels.md`.
- Confirm agent set and artifact protocols were not added where a smaller change would solve the problem.
- Forward-test with a realistic bad input skill or task request when possible.

## Domain Templates

For data cleaning workflow skills, read `references/data-cleaning-template.md`.

For general workflow refactoring details, read `references/workflow-refactoring.md`.

For sub-agent contract templates, read `references/agent-contracts.md`.

For deciding whether to use a review agent set, read `references/agent-set-activation.md`.

For concurrency and dependency design, read `references/concurrency.md`.

For recommendation levels and anti-overengineering triage, read `references/refactor-levels.md`.

## Output Quality Bar

A good workflow skill makes the complex path boring: it has a short main entry point, bounded worker responsibilities when needed, explicit artifacts when they change behavior, parallel execution where safe, fewer interruptions, review gates at high-risk decisions, and validation that can catch regressions. If the result is merely a rewritten long prompt, a needlessly serial pipeline, or unnecessary architecture around a simple stable skill, the architecture work failed.

---
name: project-continuity
description: Use when initializing or continuing a long-running project across Codex sessions with durable state, session-scoped goals, handoffs, optional roadmap or backlog extraction, protected planning boundaries, commit-on-lease-completion, and a fixed next command such as /goal $project-continuity.
---

# Project Continuity

## Overview

Use this skill to keep a project moving across fresh Codex sessions without relying on long chat history. The unit of work is one lease that advances one session milestone: a bounded objective for this `/goal` invocation with an explicit task queue, done condition, and drift boundary.

When invoked without extra instructions, especially as `/goal $project-continuity`, treat the current goal as **one session milestone**, not the whole project. Complete as many tasks inside that milestone as safely possible before stopping.

## Modes

1. **Initialize** if the project has no continuity state yet.
2. **Continue** if `SESSION_RUNBOOK.md`, `AGENT_ROLES.md`, `EXECUTION_STATE.md`, and `HANDOFF.md` exist and define an active or derivable session milestone.
3. **Repair** if continuity artifacts are partial, conflicting, or incomplete; repair the state files first, then stop with a handoff.

Do not invent a structured roadmap when project evidence is weak. Use `BACKLOG.md` or `DISCOVERY_NOTES.md` instead.

## Resources

Read only the reference needed for the current mode:

- Initialization and continuation workflow: `references/workflow.md`
- Planning maturity and roadmap/backlog choice: `references/planning-maturity.md`
- File schemas and update rules: `references/artifact-contracts.md`
- Session language continuity: `references/session-language.md`
- Sub-agent dispatch contract: `references/subagent-dispatch.md`
- Fixed prompts and completion wording: `references/continuation-prompts.md`

Use the templates in `assets/continuity/` when creating missing artifacts. Copy only the files needed for the selected planning maturity.

If the target project has no `AGENTS.md`, create one from `assets/continuity/AGENTS.md`. If it already exists, add the continuity routing guidance only when it is missing and the current lease allows editing it.

## Required Artifacts

Core artifacts:

- `AGENTS.md`
- `SESSION_RUNBOOK.md`
- `AGENT_ROLES.md`
- `EXECUTION_STATE.md`
- `HANDOFF.md`

Optional artifacts:

- `ROADMAP.md` when there are clear milestones
- `BACKLOG.md` when there are known tasks but no stable roadmap
- `DISCOVERY_NOTES.md` when the project is still exploratory
- `DECISIONS.md` when a non-trivial decision is made
- `CHANGE_REQUESTS.md` when planning, scope, or protected sources need material change

## Lease Rules

- Advance the current session milestone declared in `EXECUTION_STATE.md`; treat individual tasks as queue items inside that milestone.
- Do not stop only because one task finished. Continue through the milestone task queue while the next task remains inside the milestone goal, included task types, allowed edits, validation plan, and drift boundary.
- Use `AGENT_ROLES.md` for role boundaries and output contracts.
- Preserve the communication language recorded in `EXECUTION_STATE.md`; if missing, infer it from the latest user request and project docs, then record it.
- When delegating to sub-agents, the Continuity Lead must pass the role, task, required excerpts, allowed actions, forbidden actions, output schema, communication language, and write ownership if edits are allowed.
- Use research only when `SESSION_RUNBOOK.md` research triggers apply.
- End the lease on complete, rollover, or blocked.
- Do not start a second session milestone in the same lease.
- A lease is not complete until `HANDOFF.md` is written and changes are committed, unless a no-commit reason is recorded.
- The next session command is always `/goal $project-continuity`.

## Stop Conditions

Stop and write a handoff if:

- state files conflict and cannot be reconciled confidently
- protected files or planning artifacts need material change
- allowed scope is insufficient
- the same blocker remains after two serious attempts
- validation cannot run and the risk is non-trivial
- the session starts expanding beyond the current session milestone

## Final Response

Keep the final response short. Include lease status, validation result, commit status, and the next command:

```text
/goal $project-continuity
```

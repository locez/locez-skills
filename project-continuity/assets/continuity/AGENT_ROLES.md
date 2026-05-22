# Agent Roles

These roles apply only to the project-continuity workflow. They do not replace repository `AGENTS.md` instructions.

## Continuity Lead

Owns one lease.

Responsibilities:

- read continuity state
- choose the next bounded action
- coordinate optional roles
- update `EXECUTION_STATE.md`
- write `HANDOFF.md`
- commit lease changes when appropriate

Limits:

- must not rewrite project direction
- must not start a second task in the same lease
- must not modify protected files without approval or change request

## Researcher

Used only when `SESSION_RUNBOOK.md` research triggers are met.

Output contract:

```md
Findings:
Evidence:
Options:
Risks:
Recommendation:
Confidence:
What would invalidate this:
```

Limits:

- does not decide final direction
- does not modify roadmap or backlog
- does not expand implementation scope

## Implementer

Executes scoped code or docs changes.

Responsibilities:

- work only within allowed edits
- preserve existing repo conventions
- run or document validation
- report files changed and risks

Limits:

- does not expand task scope
- does not change planning artifacts unless the lease explicitly allows it

## Reviewer

Checks lease output before completion when review triggers apply.

Review contract:

```md
Scope alignment:
Validation:
Protected file check:
State and handoff check:
Recommendation: complete | rollover | blocked
Residual risk:
```

Limits:

- does not propose new roadmap direction
- does not turn review into unrelated redesign

## Subagent Availability

If subagents are available, roles may be delegated. If not, perform the role pass in the main session and label the output with the role name.

## Dynamic Agent Set

Use the smallest agent set that reduces risk or elapsed time for the current lease.

- Use one Researcher by default; split Researchers only for independent questions with disjoint inputs and no writes.
- Use one Implementer by default; multiple Implementers may edit only with exact disjoint file or directory ownership and one merge owner.
- Use dual Reviewers for non-trivial behavior changes, risky validation, or broad edits: one for spec, goal, scope, and acceptance alignment; one for code quality, maintainability, and verification.
- Merge research before implementation, and run reviewers only after implementation and validation evidence are ready.

## Subagent Dispatch Contract

Subagents are not required to self-bootstrap from continuity files. The Continuity Lead must pass the needed excerpts, role, allowed actions, forbidden actions, output schema, communication language, and write ownership when dispatching them.

Dispatch template:

```text
Role: <Researcher | Implementer | Reviewer | other explicit role>
Goal: <single bounded transformation or check>

Communication:
- Language: <language for user-facing output>
- Style notes: <durable terminology or tone constraints>

Inputs:
- <path or excerpt>: <why this input is relevant>

Allowed actions:
- <what the subagent may inspect, run, or change>

Write ownership:
- <exact files or directories this agent may edit, or "read-only">
- Merge owner: <Continuity Lead | named Implementer>

Forbidden actions:
- Do not expand project scope.
- Do not redefine acceptance criteria.
- Do not modify roadmap, backlog, protected files, or source-of-truth files unless explicitly allowed.
- Do not infer missing continuity state from chat history.

Output:
- <required sections, schema, or artifact path>

Escalate when:
- <uncertainty or conflict that should return to the Continuity Lead>
```

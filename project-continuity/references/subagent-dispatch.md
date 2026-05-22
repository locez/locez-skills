# Sub-Agent Dispatch

Use this contract when the Continuity Lead delegates a bounded part of a lease to a sub-agent.

Sub-agents are not required to self-bootstrap from continuity files. The Continuity Lead must pass the needed excerpts, role, allowed actions, forbidden actions, output schema, communication language, and write ownership when dispatching them.

## Dynamic Agent Set

Use the smallest agent set that reduces risk or elapsed time for the current lease.

Default to a single main-session role pass. Add sub-agents only when the task has independent work streams, high-risk behavior changes, unclear implementation paths, or review triggers that benefit from separate perspectives.

Common patterns:

- **Single Researcher**: one uncertainty dimension.
- **Split Researchers**: two independent research questions with disjoint inputs and no writes, such as runtime policy versus runner or test feasibility.
- **Single Implementer**: default writer for code or docs changes.
- **Multiple Implementers**: allowed only when each writer owns a disjoint file or directory set, no file is shared, and the Continuity Lead names one merge owner. If write ownership cannot be made disjoint, use one Implementer.
- **Dual Reviewers**: use for non-trivial behavior changes, risky validation, or broad edits. Reviewer 1 checks spec, goal, scope, and acceptance alignment. Reviewer 2 checks code quality, maintainability, and verification.

Barriers:

- Merge researcher outputs before implementation starts.
- Start implementation only after writable scopes are explicit.
- Run reviewers after implementation and validation evidence are ready.
- Research and review agents are read-only unless the dispatch explicitly grants a narrow write scope.

## Dispatch Template

```text
Role: <Researcher | Implementer | Reviewer | other explicit role>
Goal: <single bounded transformation or check>

Communication:
- Language: <language for user-facing output>
- Style notes: <durable terminology or tone constraints>

Inputs:
- <path or excerpt>: <why this input is relevant>

Allowed actions:
- <what the sub-agent may inspect, run, or change>

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

## Required Fields

Every sub-agent dispatch must include:

- role
- goal
- communication language
- inputs or excerpts
- allowed actions
- forbidden actions
- output schema
- escalation conditions
- write ownership for any agent allowed to edit
- merge owner and barrier when multiple sub-agents run

## Write Ownership

Only one actor may own each writable artifact in a lease. If a sub-agent can write files, the dispatch contract must name the exact files or directories it may touch.

Review and research agents should usually return structured text instead of editing files.

Multiple editing agents may run in the same lease only when the Continuity Lead can prove disjoint write ownership before dispatch. Do not allow concurrent edits to the same file, planning artifact, generated output, lockfile, or shared configuration.

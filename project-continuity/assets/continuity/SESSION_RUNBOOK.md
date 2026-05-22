# Session Runbook

## Startup

Read in order:

1. `SESSION_RUNBOOK.md`
2. `AGENT_ROLES.md`
3. `EXECUTION_STATE.md`
4. `HANDOFF.md` if present
5. source-of-truth files listed in `EXECUTION_STATE.md`

Before any user-facing status update, apply the communication language recorded in `EXECUTION_STATE.md`. If it is missing, infer it from the latest user request and project docs, then record it before ending the lease.

If files disagree, follow this priority:

1. `SESSION_RUNBOOK.md`
2. `EXECUTION_STATE.md`
3. source-of-truth files
4. `HANDOFF.md`
5. chat context

## Lease

Execute exactly one bounded lease. A lease advances one session milestone, then writes `HANDOFF.md`, commits or records a no-commit reason, reports status, and stops.

A session milestone should be large enough to reduce context switching and produce a meaningful handoff and commit. It may include multiple related tasks when they share one goal, task queue, allowed expansion, drift boundary, allowed edit scope, and validation plan.

Avoid micro-leases. If a task completes and the next task is in the milestone task queue or allowed expansion, continue within the same lease instead of ending immediately.

A lease ends when:

- session milestone is complete
- rollover is triggered
- blocked state is reached

Do not start another session milestone in the same lease.

## Required Inspection

Every session must inspect:

- session milestone
- task queue
- done condition
- drift boundary
- communication language
- allowed edits
- forbidden edits
- protected files
- acceptance criteria
- validation command
- relevant repo files

## Research Triggers

Use the Researcher role only if one or more is true:

- acceptance criteria are unclear
- repo evidence conflicts
- task affects architecture, public API, data model, security, migration, compatibility, or performance envelope
- multiple implementation options have meaningful tradeoffs
- session milestone depends on unknown external behavior
- planning maturity is unclear during initialization

If no trigger applies, do not perform dedicated research.

Use one Researcher by default. Use split Researchers only when there are independent questions with disjoint inputs and a required merge decision before implementation.

## Lease Ending Triggers

Stop and write `HANDOFF.md` if:

- session milestone reaches its done condition; use lease status `complete`
- protected file change is needed
- allowed scope is insufficient
- same blocker remains after two serious attempts
- validation cannot be run and risk is non-trivial
- state files conflict and cannot be reconciled
- milestone needs roadmap, backlog, or runbook changes
- the session starts expanding beyond the session milestone

## Change Request Triggers

Append `CHANGE_REQUESTS.md` and stop if:

- `ROADMAP.md` or `BACKLOG.md` needs a material change
- task priority should change materially
- source-of-truth files need modification
- acceptance criteria should be redefined
- protected planning files need modification without explicit approval

## Review Triggers

Use the Reviewer role before ending if:

- code or project behavior changed
- a non-trivial decision was made
- validation failed or was skipped
- allowed scope was close to being exceeded
- protected files were touched

Use dual Reviewers for non-trivial behavior changes, risky validation, or broad edits. Reviewer 1 checks spec, goal, scope, and acceptance alignment. Reviewer 2 checks code quality, maintainability, and verification. Reviewers are read-only unless explicitly dispatched otherwise.

## Implementation Concurrency

Use one Implementer by default.

Multiple Implementers may edit in the same lease only if:

- each owns an exact disjoint file or directory set
- no shared file, planning artifact, generated output, lockfile, or shared configuration is edited by more than one actor
- the Continuity Lead names one merge owner
- implementation starts after research outputs are merged

If ownership cannot be made disjoint, use one Implementer.

## Completion Requirements

Before ending:

- update `EXECUTION_STATE.md`
- write `HANDOFF.md`
- record `DECISIONS.md` if a non-trivial decision was made
- append `CHANGE_REQUESTS.md` if planning change is needed
- run validation or document why validation was not run
- create a git commit unless a no-commit reason is recorded

The next session command is always:

```text
/goal $project-continuity
```

## Commit Policy

At the end of every lease, create a git commit if:

- lease status is `complete`, or
- lease status is `rollover` with meaningful state, code, or docs changes, or
- lease status is `blocked` but handoff, state, or decisions changed

Do not commit if:

- no files changed
- the user explicitly says not to commit
- changes are experimental and explicitly marked not ready
- validation found a serious issue that makes the diff unsafe
- unrelated user changes cannot be separated from lease changes

Before committing:

- inspect git status
- inspect changed files
- ensure protected files were not modified without approval
- commit only lease-related files

Commit message format:

```text
project-continuity: <status> <task id or short task name>
```

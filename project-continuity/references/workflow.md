# Workflow

## Recommendation Level

This skill is intentionally `template-extract + protocolize`. It provides reusable artifacts and a fixed session protocol. It is not a supervisor, project manager, or automatic planner.

## Repo Inspection

Every invocation starts by inspecting the repository:

- identify the repo root
- list existing top-level docs and planning files
- inspect `README*`, `AGENTS.md`, docs, package metadata, tests, and existing roadmap/backlog files when present
- inspect git status before editing
- determine communication language from user instructions, state files, and project docs

Respect user changes. Do not overwrite existing continuity artifacts without reading them first. Patch minimally when possible.

## Session Milestone Sizing

One lease advances one session milestone. The session milestone is the objective boundary for this `/goal` invocation, not a single small task.

Choose a session milestone that is large enough to reduce context switching but small enough to prevent goal drift.

A good session milestone defines:

- **Goal**: the concrete state this `/goal` should reach.
- **Task queue**: multiple tasks or task types that may be completed under this milestone.
- **Allowed expansion**: adjacent tasks that may be added without asking.
- **Done condition**: the milestone state that justifies stopping with `complete`.
- **Drift boundary**: changes that mean the session is no longer pursuing this milestone.
- **Validation plan**: how to check the completed milestone.

Size guidance:

- Too small: reading a few files, making one trivial edit, or running one isolated check when follow-up work is already clear and inside the same milestone.
- Good: a coherent outcome that may include research, implementation, tests, review, and state updates under one validation plan.
- Too large: a milestone that spans unrelated objectives, requires redefining roadmap/backlog, or cannot name a concrete done condition.

Continue within the same lease while the next task:

- advances the same milestone goal
- matches the included task queue or allowed expansion
- stays within allowed edits and forbidden edits
- can be covered by the same validation plan
- does not cross the drift boundary

Stop when the next task would cross the drift boundary by changing the milestone goal, acceptance criteria, protected files, planning, allowed edits, or validation risk.

## Initialize Mode

Use initialize mode when the project has no continuity state yet:

1. Inspect the repo and existing docs.
2. Read `references/planning-maturity.md`.
3. Read `references/session-language.md`.
4. Create or patch project `AGENTS.md`:
   - if missing, create it from `assets/continuity/AGENTS.md`
   - if present, add the continuity routing guidance only when missing and allowed by the lease
5. Create core artifacts from `assets/continuity/`.
6. Choose at most one planning artifact to create initially:
   - `ROADMAP.md` only when milestones are already clear from user intent or repo evidence.
   - `BACKLOG.md` when tasks are known but sequence is not stable.
   - `DISCOVERY_NOTES.md` when the next work is exploratory.
7. Fill `EXECUTION_STATE.md` with the first session milestone, task queue, done condition, drift boundary, and communication language.
8. Write `HANDOFF.md` with status `rollover` unless a concrete first task was completed during initialization.
9. Commit the continuity setup if changes are safe to commit.
10. Stop and report `/goal $project-continuity`.

If the first milestone cannot be inferred, create a bounded discovery milestone instead of asking immediately. Ask the user only when durable project evidence is too thin to define even a safe discovery milestone.

## Continue Mode

Use continue mode when all core artifacts exist:

1. Read `SESSION_RUNBOOK.md`.
2. Read `AGENT_ROLES.md`.
3. Read `EXECUTION_STATE.md`.
4. Read `HANDOFF.md`.
5. Read source-of-truth files listed in `EXECUTION_STATE.md`.
6. Apply `references/session-language.md` before user-facing updates.
7. Confirm the current session milestone, task queue, done condition, drift boundary, allowed edits, forbidden edits, protected files, and validation commands.
   - If the previous lease completed and no active milestone remains, derive one coherent session milestone from `ROADMAP.md`, `BACKLOG.md`, or `DISCOVERY_NOTES.md` when the evidence is clear.
   - Prefer roadmap order when a reliable roadmap exists, backlog priority when there is no stable roadmap, and a bounded discovery milestone when direction is still exploratory.
   - Include adjacent tightly related tasks when they fit the milestone goal, task queue, allowed expansion, allowed edits, and validation plan.
   - Do not ask solely because `ROADMAP.md` is absent. Ask only when the durable state and repo evidence do not support a safe session milestone or discovery milestone.
8. Apply runbook triggers:
   - research trigger
   - change request trigger
   - rollover trigger
   - review trigger
9. Execute one bounded session milestone:
   - inspect/research
   - implement
   - validate
   - review if triggered
   - if delegating, read `references/subagent-dispatch.md`, choose the smallest useful agent set, and pass explicit dispatch contracts
10. When one task in the milestone completes, continue to the next queued or allowed-expansion task if it remains inside the same milestone and no stop condition is triggered.
11. Update state files, including communication language.
12. Commit lease changes or record a no-commit reason.
13. Stop.

## Repair Mode

Use repair mode when continuity artifacts are partial, conflicting, or incomplete:

- reconcile obvious drift against `SESSION_RUNBOOK.md` and `EXECUTION_STATE.md`
- do not change roadmap/backlog meaningfully
- write `HANDOFF.md` with the conflict and next exact action
- commit repair-only changes if safe
- stop

Examples of repair triggers:

- some but not all core continuity artifacts exist
- `HANDOFF.md` says one session milestone but `EXECUTION_STATE.md` says another
- required fields are blank after a previous lease
- protected file policy is missing
- validation status is unknown after code changes

## Commit Policy

At the end of every lease, create a git commit if there are meaningful state, code, or docs changes and the diff is safe to preserve.

Do not commit if:

- no files changed
- the user explicitly says not to commit
- changes are experimental and marked not ready
- validation found a serious issue that makes the diff unsafe
- unrelated user changes cannot be separated from lease changes

Before committing:

- inspect git status
- inspect changed files
- ensure protected files were not modified without approval
- run relevant validation or document why not
- update `EXECUTION_STATE.md`
- write `HANDOFF.md`

Commit only files changed for this lease. Do not stage unrelated user changes.

Commit message format:

```text
project-continuity: <status> <task id or short task name>
```

Examples:

```text
project-continuity: complete M2-T3 auth flow
project-continuity: rollover validation setup
project-continuity: blocked package manager decision
```

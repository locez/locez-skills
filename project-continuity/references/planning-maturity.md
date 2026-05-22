# Planning Maturity

Classify planning maturity before creating `ROADMAP.md`, `BACKLOG.md`, or `DISCOVERY_NOTES.md`.

## Levels

### No Roadmap

Use when:

- project direction is exploratory
- repo evidence does not show stable milestones
- the user has not provided a durable plan
- the next useful step is discovery or narrowing

Create:

- `DISCOVERY_NOTES.md`
- `EXECUTION_STATE.md` with a bounded discovery task

Do not create `ROADMAP.md`.

### Backlog Only

Use when:

- there are known tasks or issues
- ordering is partial or unstable
- there are no reliable milestones

Create:

- `BACKLOG.md`
- `EXECUTION_STATE.md` with a session milestone derived from the top backlog priority

Do not create `ROADMAP.md`.

### Lightweight Roadmap

Use when:

- there are clear phases or milestones
- details are incomplete but direction is stable enough
- repo docs or user intent support the sequence

Create:

- `ROADMAP.md`
- optional `BACKLOG.md` for unsequenced tasks

Keep roadmap items brief and mark assumptions.

### Structured Roadmap

Use when:

- milestones, tasks, acceptance criteria, and dependencies are explicit
- project direction is stable
- roadmap items are traceable to docs, code, or user-provided intent

Create:

- `ROADMAP.md`
- `DECISIONS.md` if decisions are already known

## Evidence Rules

- Every roadmap milestone should trace to repo evidence or user-provided intent.
- If evidence is weak, choose backlog or discovery.
- Do not turn guesses into roadmap commitments.
- Put uncertainty in `DISCOVERY_NOTES.md`, not `ROADMAP.md`.
- Put proposed planning changes in `CHANGE_REQUESTS.md`, not directly in roadmap.

# Artifact Contracts

## Core Files

### AGENTS.md

Purpose: target-project ambient agent guidance.

Owns:

- project-level safety and language defaults
- routing hint for `$project-continuity`
- sub-agent dispatcher-contract reminder

Do not put lease-specific tasks, acceptance criteria, or workflow internals here.

### SESSION_RUNBOOK.md

Purpose: durable execution protocol.

Owns:

- startup order
- authority order
- research triggers
- rollover triggers
- change request triggers
- review triggers
- completion requirements
- commit policy

Update only when improving the workflow protocol itself.

### AGENT_ROLES.md

Purpose: role boundaries and output contracts.

Owns:

- Continuity Lead behavior
- Researcher contract
- Implementer contract
- Reviewer contract

Do not use it as project organization design.

### EXECUTION_STATE.md

Purpose: current lease state.

Owns:

- source-of-truth files
- planning maturity
- current milestone or track
- session milestone
- task queue
- allowed expansion
- done condition
- drift boundary
- communication language and style constraints
- acceptance criteria
- allowed edits
- forbidden edits
- protected files
- validation command
- next exact action
- lease status

Update every lease.

### HANDOFF.md

Purpose: next-session startup state.

Owns:

- lease status
- session milestone
- task queue status
- done condition
- drift boundary
- what changed
- validation
- decisions
- blockers
- commit status
- next exact action
- next command
- communication language for the next session

Write every lease, even when blocked.

## Optional Files

### ROADMAP.md

Use only when milestone evidence is strong. Keep it stable. Material changes require `CHANGE_REQUESTS.md`.

### BACKLOG.md

Use for known but not fully sequenced work. It may be edited as tasks are completed or reprioritized, but material priority shifts should be recorded.

### DISCOVERY_NOTES.md

Use for uncertain project direction, findings, hypotheses, and unresolved questions.

### DECISIONS.md

Append when a non-trivial technical, product, or workflow decision is made.

Decision entry:

```md
## YYYY-MM-DD - Short Decision

Decision:
Reason:
Evidence:
Tradeoff:
Reversible:
Follow-up:
```

### CHANGE_REQUESTS.md

Append when planning, priority, scope, protected files, or acceptance criteria need material change.

Change request entry:

```md
## CR-N - Short Title

Status: proposed
Reason:
Affected files:
Impact:
Recommendation:
Next action:
```

## Protection Rules

Protected files are listed in `EXECUTION_STATE.md`. By default, treat these as protected once created:

- `SESSION_RUNBOOK.md`
- `AGENT_ROLES.md`
- `ROADMAP.md`
- `CHANGE_REQUESTS.md`

Protected does not mean immutable. It means changes require explicit approval or a change request.

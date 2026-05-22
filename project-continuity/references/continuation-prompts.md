# Continuation Prompts

## Fixed Entry

Use this in a fresh session:

```text
/goal $project-continuity
```

The skill must derive the next session milestone from durable repo state, not from chat history.

The skill must also derive the user-facing communication language from `EXECUTION_STATE.md`, `HANDOFF.md`, and the latest user request. Do not default to English when the stored or current user language indicates otherwise.

## Goal Semantics

When invoked through `/goal`, the goal is complete when one lease ends.

Valid lease endings:

- `complete`
- `rollover`
- `blocked`

Project completion is not required.

## Final Response Shape

Use this concise shape:

```md
Lease status: complete | rollover | blocked
Validation: <command/result or documented gap>
Commit: <hash/message or no-commit reason>
Next: /goal $project-continuity
```

If initialization occurred, include created artifacts.

If blocked, include the blocker and the file where it was recorded.

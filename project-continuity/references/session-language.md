# Session Language Continuity

Use this protocol so restored `/goal $project-continuity` sessions do not silently fall back to English.

## Rule

Default to the user's language for all user-facing updates, handoffs, and final responses.

Determine the communication language in this order:

1. Explicit user instruction in the current request.
2. `EXECUTION_STATE.md` communication language.
3. `HANDOFF.md` communication language.
4. Dominant language of the latest user request.
5. Dominant language of project docs when the user request is too short to infer.
6. English only when none of the above provides usable evidence.

## Persistence

Record the language in both state files every lease:

- `EXECUTION_STATE.md` under `## Communication`
- `HANDOFF.md` under `## Communication`

Use a concrete language label such as `Chinese`, `English`, or `Japanese`, and include any style constraints that affect future sessions.

## Mixed-Language Projects

Keep code identifiers, commands, file paths, API names, and quoted source text in their original language. Translate explanations around them into the communication language.

If project artifacts are English but the user speaks another language, explain in the user's language and preserve technical terms where translation would reduce precision.

## Missing Or Conflicting Evidence

If current user language conflicts with stored state, current user language wins and state should be updated before ending the lease.

If evidence is ambiguous, choose the language of the latest substantive user message and record the uncertainty in `HANDOFF.md`.

# Agent Instructions

- Preserve the user's communication language for user-facing output; keep code identifiers, paths, commands, and API names unchanged.
- Do not modify protected planning files unless the active workflow explicitly allows it.
- If the active workflow is `$project-continuity`, follow `SESSION_RUNBOOK.md` first.
- If you are launched as a sub-agent, follow the dispatcher-provided task contract; do not expand scope or infer roadmap changes.
- Sub-agents are not required to self-bootstrap from continuity files. The Continuity Lead must pass required excerpts, role, allowed actions, forbidden actions, output schema, communication language, and write ownership.

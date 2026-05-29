# Project Continuity Unavailable Decision

Status: Accepted
Date: 2026-05-29

Chinese version: [2026-05-29-project-continuity-unavailable.zh-CN.md](2026-05-29-project-continuity-unavailable.zh-CN.md)

## Decision

`project-continuity` is marked unavailable, but the skill directory is not deleted. The repository keeps its `SKILL.md`, `references/`, `assets/`, and `agents/` files as historical material for review, postmortem analysis, and possible migration work. It must no longer be used to initialize, continue, repair, or manage long-running project state across sessions.

## Rationale

Experiments showed that this working model depends too heavily on state. It requires the agent to maintain durable state, handoffs, lease boundaries, and next commands continuously and correctly across sessions. In real collaboration, user instructions naturally interrupt the planned flow, change priorities, skip steps, or ask the agent to handle a new issue immediately. Those normal interactions interfere with state updates and make the state files drift away from actual project progress.

Once continuity breaks, the damage compounds. A fresh session may treat the saved state as reliable context even when it is incomplete, stale, contradictory, or describing the wrong project situation. At that point the state is not merely less helpful; it can actively mislead the next agent into planning or delivering from false premises, making the overall project condition disastrous.

The skill also depends too heavily on model intelligence. It expects the model to consistently understand project boundaries, decide whether a user interruption changes the lease, repair state conflicts, know which files can be edited, and record the right handoff details. If model reasoning quality drops, delivery quality drops sharply: boundaries drift, state repair becomes guesswork, handoffs create false certainty, and long-running project management becomes less reliable instead of more reliable.

## Impact

- `$project-continuity` is no longer recommended as the entry point for long-running projects.
- `/goal $project-continuity` is no longer emitted as a next-session command.
- Continuity templates from this skill should no longer be copied into target projects.
- Historical files remain available for auditing the failure mode, identifying reusable ideas, and evaluating whether smaller replacements are worth building.

## Future Direction

Any future attempt at similar capability should avoid tying project correctness to a large durable state system. Safer alternatives include smaller, local, and more verifiable mechanisms: single-task handoffs, explicit human confirmation points, read-only project summaries, or deterministic script-generated snapshots. A replacement should remain recoverable when users frequently change instructions, model capability varies, or parts of the state are missing, instead of passing bad state into the next session.

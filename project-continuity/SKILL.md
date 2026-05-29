---
name: project-continuity
description: "Unavailable archived skill. Do not use to initialize, continue, repair, or manage long-running projects across sessions; retained only for historical reference and postmortem analysis."
---

# Project Continuity (Unavailable)

## Status

This skill is unavailable and must not be used for active work.

Do not use it to initialize, continue, repair, or manage project state across sessions. Do not emit `/goal $project-continuity` as a next command. Do not create or update continuity artifacts from this skill.

The skill directory is retained only as an archive for historical review, migration analysis, or postmortem work. Its former references, templates, and workflow assets remain on disk, but they are inactive.

## Why It Is Disabled

Experiments showed that this workflow depends too heavily on durable state and strict state updates. User instructions naturally interrupt and redirect sessions, which can prevent the state files from staying coherent. Once continuity breaks, the stored project picture can become seriously misleading for a fresh session.

The workflow also depends too much on model capability. If the model's reasoning quality drops, the lease boundaries, state repair, and handoff discipline degrade quickly, producing poor delivery quality and compounding bad state.

See the repository decision records:

- English: `docs/specs/2026-05-29-project-continuity-unavailable.md`
- Chinese: `docs/specs/2026-05-29-project-continuity-unavailable.zh-CN.md`

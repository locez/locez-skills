# Project Continuity Repository Integration (Historical)

> Historical note: this integration record is superseded by
> [Project Continuity Unavailable Decision](2026-05-29-project-continuity-unavailable.md).
> The skill remains in the repository as an archive, but it is no longer available for active use.

## Context

`project-continuity` was designed by Locez as a reusable workflow skill for keeping long-running projects moving across fresh Codex sessions. It is now tracked in this repository so it can be reused across machines and evolved alongside the other Locez-designed skills.

## Skill Purpose

The skill initializes, continues, or repairs durable continuity state for a target project. It treats one invocation as one bounded session lease: the agent advances one session milestone, updates state files, writes a handoff, and commits safe lease changes unless there is a recorded no-commit reason.

## Repository Placement

The copied skill lives at:

```text
project-continuity/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── continuity/
│       ├── AGENTS.md
│       ├── AGENT_ROLES.md
│       ├── BACKLOG.md
│       ├── CHANGE_REQUESTS.md
│       ├── DECISIONS.md
│       ├── DISCOVERY_NOTES.md
│       ├── EXECUTION_STATE.md
│       ├── HANDOFF.md
│       ├── ROADMAP.md
│       └── SESSION_RUNBOOK.md
└── references/
    ├── artifact-contracts.md
    ├── continuation-prompts.md
    ├── planning-maturity.md
    ├── session-language.md
    ├── subagent-dispatch.md
    └── workflow.md
```

No README or changelog is added inside the skill directory. The skill directory stays focused on runtime resources; repository-level explanation belongs in the root README files and this spec.

## Design Notes

- `SKILL.md` remains the lean entry point and links to mode-specific references.
- `references/workflow.md` owns initialize, continue, repair, and commit policy flow.
- `references/planning-maturity.md` prevents the agent from inventing a roadmap when evidence only supports backlog or discovery notes.
- `references/artifact-contracts.md` defines which continuity file owns each class of state.
- `references/session-language.md` preserves the user's durable communication language across sessions.
- `references/subagent-dispatch.md` defines the dispatch contract when the Continuity Lead uses worker agents.
- `assets/continuity/` contains templates copied into target projects during initialization or repair.
- `agents/openai.yaml` supplies UI metadata for skill listing and invocation.

## Historical Validation Expectations

These expectations applied while the skill was active. They are kept only to explain the original integration criteria and are superseded by the unavailable decision above. Do not use them as current validation rules.

When this skill was active, changes were expected to verify:

- frontmatter includes `name: project-continuity` and a trigger-focused `description`;
- `SKILL.md` directly references every file in `references/`;
- every required continuity artifact named in `SKILL.md` has a matching template in `assets/continuity/`;
- the next-session command remained `/goal $project-continuity`;
- repository README files list the skill, installation examples, and invocation examples;
- repository wording states that these skills are Locez-designed, not a collected third-party catalog.

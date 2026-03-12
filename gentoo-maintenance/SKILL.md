---
name: gentoo-maintenance
description: Use when handling Portage conflicts, @world upgrades, /etc/portage cleanup, binpkg tradeoffs, or deciding where Gentoo maintenance rules and local host preferences should live
---

# Gentoo Maintenance

## Overview

Use this skill to classify Gentoo maintenance work before changing anything. The job is to determine host role, task type, risk level, local preference state, and file placement, then stage reviewable candidates instead of mutating `/etc/portage` directly.

Core rule: read-only inspection and `/tmp` staging may proceed, but any other write must stop for user review first.

## When To Use

Use this skill when the user is:

- debugging Portage conflicts, blocks, slot conflicts, or autounmask fallout
- running or preparing a meaningful `@world` upgrade
- cleaning up `/etc/portage` structure or old autounmask residue
- deciding whether a rule belongs in `custom`, `zz-autounmask`, `package.use/<topic>`, `package.mask`, or the local `gm-*` files
- optimizing a VPS or binpkg host by trimming non-core features
- changing package policy, ebuild behavior, or long-term package pins

Do not use this skill for:

- basic Gentoo explanations with no maintenance decision
- package build failures that are clearly code defects inside an ebuild or patch
- one-off shell usage unrelated to Portage state

## Workflow

Follow this sequence every time:

1. Read `/etc/portage/gm-agent-preferences.yaml` if present.
2. Read `/etc/portage/gm-host-profile.yaml` if present.
3. Identify host role.
4. Identify task type.
5. Determine whether task-critical profile fields are missing.
6. Ask one question at a time for any missing field that materially affects the answer.
7. Assign risk level.
8. Gather only the evidence needed for that task.
9. Classify each proposed change.
10. Choose the target file class.
11. Stage candidates under `/tmp/gentoo-maintenance/` if changes are needed.
12. Stop at the review gate before any system write.

If profile data is incomplete, continue only with read-only analysis and mark any affected recommendations as temporary.

## Safety Rules

- Do not edit `/etc/portage` directly without explicit review.
- Do not run `emerge` without `-p` unless the user has reviewed the plan and approved the write.
- Do not let auto mode bypass the review gate.
- Treat kernel, boot, ZFS, GPU driver, and repo configuration changes as high-risk by default.
- Treat writes to `/etc/portage/gm-host-profile.yaml` and `/etc/portage/gm-agent-preferences.yaml` as reviewed system writes.
- If host role or profile-dependent strategy is still unclear after reading available evidence, ask instead of guessing.

## Reference Map

Load only the references you need.

- Host role detection: `references/host-roles.md`
- Task classification: `references/task-types.md`
- Portage file placement rules: `references/portage-file-placement.md`
- Combined decision routing: `references/decision-matrix.md`
- Command strength and risk selection: `references/command-strategy.md`
- Safety gates and stop conditions: `references/safety-gates.md`
- VPS and builder tradeoffs: `references/binpkg-policy.md`
- Host profile schema: `references/host-profile-schema.md`
- Agent workflow preference schema: `references/agent-preferences-schema.md`

## Required Output Shape

Default response structure:

- `Context`
- `Findings`
- `Decision`
- `Next write candidates`

If profile data is incomplete, `Context` should also include:

- `missing_profile_fields`
- `temporary_assumptions`
- `questions_needed`
- `final_decision_blocked_by_profile`

If candidate files are generated, place them under:

```text
/tmp/gentoo-maintenance/
```

Use the templates in `assets/tmp-layout/` as the starting point for staged outputs.

## Quick Routing Rules

- Direct long-term package intent usually goes to `custom` or a topic file.
- Dependency-only exceptions usually go to `zz-autounmask` with short provenance comments.
- Long-term "do not select this" policy goes to `package.mask`.
- Machine-wide strategy belongs in `/etc/portage/gm-host-profile.yaml`.
- Durable user workflow overrides belong in `/etc/portage/gm-agent-preferences.yaml`.
- Temporary conflict fixes should remain staged until they prove they deserve a permanent home.
- Missing profile data is never permission to silently apply default desktop or VPS assumptions.

## Common Mistakes

- Dumping all keyword exceptions into `custom`
- Keeping provenance-free entries in `zz-autounmask`
- Using the heaviest `emerge` solver mode for every command
- Applying desktop full-feature logic to VPS or builder hosts
- Repeating generic cleanup advice after the user has already given a durable override
- Turning one-off solver output into permanent policy without review

## Final Gate

Before any non-`/tmp` write, state:

- what will be changed
- why it is a write
- what files or system state it affects
- whether missing profile data still blocks a final recommendation
- that user review is required first

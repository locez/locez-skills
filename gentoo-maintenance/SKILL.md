---
name: gentoo-maintenance
description: Use when handling Portage conflicts, @world upgrades, /etc/portage cleanup, binpkg tradeoffs, or deciding where Gentoo maintenance rules should live
---

# Gentoo Maintenance

## Overview

Use this skill to classify Gentoo maintenance work before changing anything. The job is to determine host role, task type, risk level, and file placement, then stage reviewable candidates instead of mutating `/etc/portage` directly.

Core rule: read-only inspection and `/tmp` staging may proceed, but any other write must stop for user review first.

## When To Use

Use this skill when the user is:

- debugging Portage conflicts, blocks, slot conflicts, or autounmask fallout
- running or preparing a meaningful `@world` upgrade
- cleaning up `/etc/portage` structure or old autounmask residue
- deciding whether a rule belongs in `custom`, `zz-autounmask`, `package.use/<topic>`, or `package.mask`
- optimizing a VPS or binpkg host by trimming non-core features
- changing package policy, ebuild behavior, or long-term package pins

Do not use this skill for:

- basic Gentoo explanations with no maintenance decision
- package build failures that are clearly code defects inside an ebuild or patch
- one-off shell usage unrelated to Portage state

## Workflow

Follow this sequence every time:

1. Identify host role.
2. Identify task type.
3. Assign risk level.
4. Gather only the evidence needed for that task.
5. Classify each proposed change.
6. Choose the target file class.
7. Stage candidates under `/tmp/gentoo-maintenance/` if changes are needed.
8. Stop at the review gate before any system write.

Do not skip classification. File placement is the whole point of this skill.

## Safety Rules

- Do not edit `/etc/portage` directly without explicit review.
- Do not run `emerge` without `-p` unless the user has reviewed the plan and approved the write.
- Do not let auto mode bypass the review gate.
- Treat kernel, boot, ZFS, GPU driver, and repo configuration changes as high-risk by default.
- If host role is unclear after reading available evidence, stop and ask instead of guessing.

## Reference Map

Load only the references you need.

- Host role detection: `references/host-roles.md`
- Task classification: `references/task-types.md`
- Portage file placement rules: `references/portage-file-placement.md`
- Combined decision routing: `references/decision-matrix.md`
- Command strength and risk selection: `references/command-strategy.md`
- Safety gates and stop conditions: `references/safety-gates.md`
- VPS and builder tradeoffs: `references/binpkg-policy.md`
- Local host policy input format: `references/host-profile-schema.md`

## Required Output Shape

Default response structure:

- `Context`
- `Findings`
- `Decision`
- `Next write candidates`

If candidate files are generated, place them under:

```text
/tmp/gentoo-maintenance/
```

Use the templates in `assets/tmp-layout/` as the starting point for staged outputs.

## Quick Routing Rules

- Direct long-term package intent usually goes to `custom` or a topic file.
- Dependency-only exceptions usually go to `zz-autounmask` with short provenance comments.
- Long-term "do not select this" policy goes to `package.mask`.
- Machine-wide preferences belong in the local host profile, not in public skill files.
- Temporary conflict fixes should remain staged until they prove they deserve a permanent home.

## Common Mistakes

- Dumping all keyword exceptions into `custom`
- Keeping provenance-free entries in `zz-autounmask`
- Using the heaviest `emerge` solver mode for every command
- Applying desktop full-feature logic to VPS or builder hosts
- Turning one-off solver output into permanent policy without review

## Final Gate

Before any non-`/tmp` write, state:

- what will be changed
- why it is a write
- what files or system state it affects
- that user review is required first

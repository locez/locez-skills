# Gentoo Maintenance Skill Design

Date: 2026-03-12
Status: Draft
Scope: Open-source skill design for reusable Gentoo and Portage maintenance workflows

## Purpose

`gentoo-maintenance` is a decision-oriented skill for Portage maintenance. It is not a Gentoo tutorial and not a bag of one-off commands. Its job is to:

- classify the current host context
- classify the current maintenance task
- decide where configuration changes belong
- stage candidate changes safely for review

The skill must support both desktop and VPS-oriented workflows, while remaining useful for binpkg-focused hosts and mixed-purpose machines.

## Goals

- reduce repeated human effort during Portage maintenance
- keep `/etc/portage` more consistent over time
- distinguish direct user intent from dependency fallout
- support aggressive analysis with conservative write behavior
- keep the skill repository open-source and free of sensitive host data

## Non-Goals

- teaching basic Gentoo usage
- storing private host facts in the public repository
- automatically mutating system state without review
- encoding large package-specific compatibility tables into the skill

## Core Principles

- Prefer correct classification over fast action.
- Keep permanent rules small and explainable.
- Use `/tmp` as the normal staging area for unreviewed changes.
- Treat direct user intent differently from indirect dependency exceptions.
- Keep host policy outside the public skill body and inject it locally.
- Escalate dependency solving only when evidence justifies it.

## Safety Model

The skill must enforce these hard constraints:

- Any action that writes outside `/tmp` requires explicit user review first.
- Any system-changing action requires explicit user review first.
- Auto mode must not bypass the review gate.
- Read-only inspection and `/tmp` candidate generation are allowed without confirmation.

Write actions include:

- editing `/etc/portage`
- running `emerge` without `-p`
- changing kernel, boot, ZFS, GPU driver, or overlay state
- running `etc-update` or `dispatch-conf`
- modifying package sets, world files, or repo config

## Repository Layout

The repository root is:

`~/locez-skills`

The skill layout should be:

```text
gentoo-maintenance/
  SKILL.md
  references/
    host-roles.md
    task-types.md
    portage-file-placement.md
    decision-matrix.md
    command-strategy.md
    safety-gates.md
    binpkg-policy.md
    host-profile-schema.md
  assets/
    tmp-layout/
      review-summary.txt
      package.accept_keywords.custom
      package.accept_keywords.zz-autounmask
      package.use.topic
      package.mask.pins
  agents/
    openai.yaml
```

The repository should also contain spec history under:

```text
docs/specs/
```

## SKILL.md Responsibilities

`SKILL.md` should stay lean and contain:

- when to use the skill
- the fixed workflow entry sequence
- hard safety boundaries
- links to the specific reference files to load as needed

It should not duplicate long reference material already stored in `references/`.

## Host Role Model

The skill supports four host roles:

- `desktop`
- `vps`
- `binpkg-builder`
- `mixed`

Role resolution priority:

1. explicit user instruction
2. local host profile file
3. hostname mapping
4. heuristics
5. stop and ask if still unclear

Heuristics may assist but must not be treated as durable truth.

## Local Host Profile

The public repository defines a schema, not the actual private profile.

Recommended local path:

`~/.config/locez-skills/gentoo-host-profile.yaml`

Suggested schema:

```yaml
role: desktop
optimize_for:
  - stability
  - convenience

allow_non_core_feature_loss: false
prefer_binpkg_when_possible: false
prefer_tmp_candidates: true
require_manual_review_for_writes: true

high_risk_areas:
  - kernel
  - boot
  - zfs
  - gpu-driver

topic_policies:
  steam_32bit_stack: keep
  qt_kde_stack: full-featured
  vps_feature_trimming: disallow

package_pins:
  - "=sys-kernel/xanmod-sources-6.15.8::gentoo-zh"

notes:
  - "Interactive desktop"
  - "Preserve KDE and Steam usability"
```

The profile should express strategy, not mirror `/etc/portage`.

## Task Types

The skill recognizes these task types:

- `world-upgrade`
- `conflict-debug`
- `portage-hygiene`
- `package-intent-change`
- `binpkg-optimization`
- `build-or-ebuild-adjustment`

The skill must always identify host role first, then task type.

## Change Categories

Every proposed change should be classified as one of:

- `direct-long-term-intent`
- `dependency-exception`
- `topic-policy`
- `host-policy`
- `temporary-fix`

Classification is required before deciding file placement.

## Portage File Placement Rules

### `package.accept_keywords/custom`

Use for direct, long-term user intent:

- intentionally tracked `~amd64` packages
- intentionally tracked live packages
- deliberate version-pinned keyword rules

Do not place indirect dependency exceptions here.

### `package.accept_keywords/zz-autounmask`

Use for dependency-driven keyword exceptions:

- indirect dependencies
- helper packages not directly chosen by the user

Requirements:

- keep short provenance comments
- do not keep naked entries
- summarize provenance by package or scenario, not by long autounmask history

### `package.use/<topic>`

Use for long-term topic policies such as:

- `steam`
- `kernel`
- `sunshine`
- `cross-*`
- `system`
- `app-custom`

These files should encode durable topic-level decisions, not one-off conflict fixes.

### `package.use/zz-autounmask`

Use for dependency-driven USE exceptions that are not direct intent. Treat it as a regenerable buffer, not a source of truth.

### `package.mask`

Use for long-term "do not select this" policy:

- known-bad versions
- temporarily unacceptable major upgrades
- intentionally excluded versions

### Host Profile

Use the local host profile for machine-wide policy, not for package-level clutter.

### `/tmp`

Use `/tmp/gentoo-maintenance/` as the staging area for all unreviewed candidates.

## Command Strategy

The skill should use progressive dependency-solving strength based on risk.

### Risk Levels

- `low`
- `medium`
- `high`
- `critical`

High-risk areas such as kernel, boot, ZFS, or GPU driver should increase the risk level.

### Command Levels

#### Level 1: Light Check

For low-risk tasks:

```bash
emerge -pv <pkg>
```

or:

```bash
emerge -pvuD @world
```

#### Level 2: Standard World Validation

For medium-risk validation:

```bash
emerge -pvuDN --complete-graph=y @world
```

This is the default recommendation for `@world` on desktop and VPS hosts.

#### Level 3: Heavy Conflict Resolution

For high-risk conflict solving:

```bash
emerge -pvuDN --complete-graph=y --autounmask-backtrack=y @world
```

Use this when:

- autounmask requirements cause early solver stop
- slot or subslot conflicts appear
- large desktop or toolchain stacks are moving together

#### Level 4: Execution

For reviewed write actions:

```bash
emerge -avuDN --complete-graph=y [--autounmask-backtrack=y] @world
```

This always requires explicit review.

### Command Policy Rules

- `@world` on desktop or VPS should default to `--complete-graph=y`.
- `--autounmask-backtrack=y` should not be enabled by default for all runs.
- It should be added only when the solver stops early or complex conflicts justify it.
- `--with-bdeps` should be documented as reference behavior, not emphasized as a core rule.

## Interaction Protocol

Each run of the skill should follow a stable five-phase protocol.

### Phase 1: Identify

Report:

- host role
- task type
- risk level
- write scope

### Phase 2: Findings

Summarize the critical evidence:

- root cause chain
- top-level packages or policies involved
- matching Portage files
- historical residue that affects the result

### Phase 3: Decision

For each proposed change, record:

- change category
- target file or target class
- short reason for placement

### Phase 4: Candidate Output

Generate only into:

`/tmp/gentoo-maintenance/`

Candidate output should explicitly state:

- what files were generated
- where each file should be copied
- whether the application mode is overwrite, append, or manual merge

### Phase 5: Review Gate

Before any system write, stop and state:

- what action would be taken
- why it counts as a write
- what it affects
- that user review is required

## Output Format

Default response structure:

- `Context`
- `Findings`
- `Decision`
- `Next write candidates`

This format should remain consistent unless the user explicitly asks for a different structure.

## Automation Reduction Triggers

The skill should become more conservative when:

- host role evidence conflicts
- deletions significantly exceed additions
- multiple Portage topic files are affected at once
- kernel, boot, ZFS, or GPU driver are involved
- system upgrade and config restructuring are happening together
- multiple materially different valid solutions exist

## Best Practices

- Keep `custom` small and intentional.
- Keep `zz-autounmask` commented and disposable.
- Prefer moving stable policy into topic files over piling up generic files.
- Prefer feature trimming over patching in binpkg-focused VPS workflows.
- Prefer patching only after USE and package-level strategy are exhausted.
- Keep private host facts out of the public skill repository.

## Anti-Patterns

- using `custom` as a dump for all keyword exceptions
- keeping provenance-free entries in `zz-autounmask`
- preserving long raw autounmask comment chains forever
- turning one-off conflict workarounds into permanent policy without review
- applying VPS feature-cutting logic to desktop hosts
- applying desktop full-feature expectations to builder hosts
- letting the skill mutate `/etc/portage` directly

## Open Questions For Implementation

- whether to generate `agents/openai.yaml` immediately or after `SKILL.md` is stable
- whether to include helper scripts for staging candidate files in `/tmp`
- whether hostname-to-role mapping belongs in the public repo or only in local private config

## Expected Next Step

After this spec is reviewed and accepted, the next workflow should be:

1. create an implementation plan for the skill structure and reference files
2. implement the skill in the repository
3. validate that the skill remains concise and follows the stated safety model

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
- stop guessing when host policy or user workflow preferences materially affect the answer

The skill must support desktop, VPS, binpkg-focused, and mixed-purpose hosts without forcing one policy style onto every machine.

## Goals

- reduce repeated human effort during Portage maintenance
- keep `/etc/portage` more consistent over time
- distinguish direct user intent from dependency fallout
- support aggressive analysis with conservative write behavior
- remember durable host and workflow preferences so the skill stops re-guessing
- keep the public repository free of private host data

## Non-Goals

- teaching basic Gentoo usage
- storing private host facts in the public repository
- automatically mutating system state without review
- encoding large package-specific compatibility tables into the skill
- turning one-off conversation details into permanent profile state by default

## Core Principles

- Prefer correct classification over fast action.
- Keep permanent rules small and explainable.
- Use `/tmp` as the normal staging area for unreviewed changes.
- Treat direct user intent differently from indirect dependency exceptions.
- Separate machine facts from agent workflow overrides.
- Escalate dependency solving only when evidence justifies it.
- If key profile data is missing, ask instead of silently substituting skill defaults.

## Safety Model

The skill must enforce these hard constraints:

- Any action that writes outside `/tmp` requires explicit user review first.
- Any system-changing action requires explicit user review first.
- Auto mode must not bypass the review gate.
- Read-only inspection and `/tmp` candidate generation are allowed without confirmation.
- Missing profile fields may block final recommendations, but they must not block read-only evidence gathering.

Write actions include:

- editing `/etc/portage`
- writing or updating the local profile files under `/etc/portage`
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
    agent-preferences-schema.md
  assets/
    tmp-layout/
      review-summary.txt
      package.accept_keywords.custom
      package.accept_keywords.zz-autounmask
      package.use.topic
      package.mask.pins
      gm-host-profile.yaml
      gm-agent-preferences.yaml
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
- the requirement to read local profile sources before relying on heuristics
- links to the specific reference files to load as needed

It should not duplicate long reference material already stored in `references/`.

## Configuration Model

The skill should use two system-level local files under `/etc/portage`:

- `/etc/portage/gm-host-profile.yaml`
- `/etc/portage/gm-agent-preferences.yaml`

These are the durable local inputs for host classification and workflow behavior.

### `gm-host-profile.yaml`

This file stores machine facts and machine-level strategy, such as:

- `role`
- `optimize_for`
- `prefer_binpkg_when_possible`
- `prefer_tmp_candidates`
- `require_manual_review_for_writes`
- `allow_non_core_feature_loss`
- `high_risk_areas`
- `notes`

This file answers: "What kind of machine is this, and what system-level tradeoffs are normal here?"

### `gm-agent-preferences.yaml`

This file stores durable user overrides for how the skill should behave on this host, such as:

- treat-this-host-as overrides when the user wants policy to differ from heuristics
- default review posture preferences
- rules about when to avoid certain cleanup or normalization advice
- durable workflow guidance like preferring staged candidates first
- explicit "follow this habit even if the generic skill would suggest otherwise" rules

This file answers: "How should the agent behave here when the user has already stated a durable preference?"

### Why Two Files

Host facts and agent workflow overrides must remain distinct:

- host facts describe the machine
- agent preferences describe how to interpret and present maintenance decisions

Keeping them separate avoids turning one-off tool behavior into fake machine facts.

## Decision Precedence

The skill should resolve strategy in this order:

1. explicit instruction in the current conversation
2. `/etc/portage/gm-agent-preferences.yaml`
3. `/etc/portage/gm-host-profile.yaml`
4. read-only system evidence and heuristics
5. ask the user if a missing field still materially affects the decision

Heuristics are advisory only. They must not override explicit user direction or durable local profile data.

## Host Role Model

The skill supports four host roles:

- `desktop`
- `vps`
- `binpkg-builder`
- `mixed`

Role resolution priority:

1. explicit user instruction in the current task
2. `gm-agent-preferences.yaml` override
3. `gm-host-profile.yaml`
4. hostname mapping if later introduced
5. heuristics
6. ask if still materially ambiguous

Heuristics may assist but must not be treated as durable truth.

## Profile Discovery And Completion

The skill should not only ask when a profile file is missing. It should ask whenever the current task lacks key profile data that changes the recommended strategy.

### Discovery Flow

At the start of every run:

1. read `gm-agent-preferences.yaml` if present
2. read `gm-host-profile.yaml` if present
3. identify the task type
4. determine which fields are required for this task
5. ask follow-up questions only for missing fields that materially affect the outcome

### Questioning Rule

- Ask one question at a time.
- Explain which field is missing and why it matters.
- After the user answers, classify the answer as:
  - current-turn only
  - `gm-host-profile.yaml`
  - `gm-agent-preferences.yaml`
- If the answer is durable, stage a candidate update under `/tmp/gentoo-maintenance/` and stop at the normal review gate before any system write.

### Continuation Rule

If profile data is incomplete, the skill may continue with read-only analysis. It may:

- inspect files
- trace dependency chains
- summarize likely causes
- prepare staged candidates

It must not present profile-sensitive conclusions as final. Those must be marked as temporary until the missing fields are confirmed.

## Required Fields

### Common Required Fields

These fields are the baseline for most tasks:

- `role`
- `prefer_binpkg_when_possible`
- `prefer_tmp_candidates`
- `require_manual_review_for_writes`

### Conditional Fields

These should be requested only when relevant:

- `allow_non_core_feature_loss`
  - required for VPS, builder, or binpkg-optimization tradeoffs
- topic-specific feature preservation preferences
  - required when desktop feature completeness materially affects the answer
- durable workflow overrides
  - required when the user says the generic recommendation style is wrong for this machine

### Example `gm-host-profile.yaml`

```yaml
role: vps
prefer_binpkg_when_possible: true
prefer_tmp_candidates: true
require_manual_review_for_writes: true
allow_non_core_feature_loss: true
optimize_for:
  - stability
  - low-maintenance
high_risk_areas:
  - kernel
  - boot
  - zfs
notes:
  - service-oriented host
```

### Example `gm-agent-preferences.yaml`

```yaml
prefer_question_when_profile_incomplete: true
allow_readonly_analysis_without_full_profile: true

host_overrides:
  treat_this_host_as: vps

workflow:
  prefer_staged_candidates: true
  avoid_recommending_autounmask_cleanup_by_default: true

rules_to_follow:
  - when: portage-hygiene
    rule: respect existing user layout unless explicitly asked to normalize it
    reason: durable user preference
  - when: binpkg-optimization
    rule: ask before trading feature completeness for easier binpkg resolution
    reason: durable user preference
```

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

### Host Profile Files

Use `/etc/portage/gm-host-profile.yaml` for machine-level policy and `/etc/portage/gm-agent-preferences.yaml` for durable workflow overrides. Do not use either file as a dump for package-level clutter.

### `/tmp`

Use `/tmp/gentoo-maintenance/` as the staging area for all unreviewed candidates, including candidate updates to the two local profile files.

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

Each run of the skill should follow a stable six-phase protocol.

### Phase 1: Load Context

Report:

- which local profile files were found
- which profile fields were loaded
- which required fields are missing for the current task

### Phase 2: Identify

Report:

- host role
- evidence quality
- task type
- risk level
- write scope
- whether any conclusions are temporary because profile data is incomplete

### Phase 3: Findings

Summarize the critical evidence:

- root cause chain
- top-level packages or policies involved
- matching Portage files
- historical residue that affects the result

### Phase 4: Decision

For each proposed change, record:

- change category
- target file or target class
- short reason for placement
- which profile field or user preference affected the choice

### Phase 5: Candidate Output

Generate only into:

`/tmp/gentoo-maintenance/`

Candidate output should explicitly state:

- what files were generated
- where each file should be copied
- whether the application mode is overwrite, append, or manual merge

### Phase 6: Review Gate

Before any system write, stop and state:

- what action would be taken
- why it counts as a write
- what it affects
- whether any missing profile fields still block final application
- that user review is required

## Output Format

Default response structure:

- `Context`
- `Findings`
- `Decision`
- `Next write candidates`

When profile data is incomplete, `Context` should also include:

- `missing_profile_fields`
- `temporary_assumptions`
- `questions_needed`
- `final_decision_blocked_by_profile`

This format should remain consistent unless the user explicitly asks for a different structure.

## Automation Reduction Triggers

The skill should become more conservative when:

- host role evidence conflicts
- explicit user instruction conflicts with stored agent preferences
- deletions significantly exceed additions
- multiple Portage topic files are affected at once
- kernel, boot, ZFS, or GPU driver are involved
- system upgrade and config restructuring are happening together
- multiple materially different valid solutions exist
- final recommendations depend on currently missing profile data

## Best Practices

- Keep `custom` small and intentional.
- Keep `zz-autounmask` commented and disposable.
- Prefer moving stable policy into topic files over piling up generic files.
- Prefer feature trimming over patching in binpkg-focused VPS workflows.
- Prefer patching only after USE and package-level strategy are exhausted.
- Keep private host facts out of the public skill repository.
- Store durable user workflow overrides explicitly so the skill stops repeating unwanted generic advice.

## Anti-Patterns

- using `custom` as a dump for all keyword exceptions
- keeping provenance-free entries in `zz-autounmask`
- preserving long raw autounmask comment chains forever
- turning one-off conflict workarounds into permanent policy without review
- applying VPS feature-cutting logic to desktop hosts
- applying desktop full-feature expectations to builder hosts
- letting the skill mutate `/etc/portage` directly
- treating missing profile data as permission to silently guess
- mixing machine facts with agent workflow rules in the same local file

## Open Questions For Implementation

- whether to add migration guidance from the earlier `~/.config/locez-skills/...` prototype path or simply replace it
- whether to provide example staged templates for both `gm-*.yaml` files in `assets/tmp-layout/`
- whether hostname-to-role mapping belongs in the public repo or only in local private config

## Expected Next Step

After this spec is reviewed and accepted, the next workflow should be:

1. create an implementation plan for the skill structure and reference files
2. implement the skill in the repository
3. validate that the skill remains concise and follows the stated safety model

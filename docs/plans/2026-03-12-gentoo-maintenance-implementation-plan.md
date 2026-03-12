# Gentoo Maintenance Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the `gentoo-maintenance` skill so it discovers, asks for, and stages durable host and agent preferences using the approved `/etc/portage/gm-*.yaml` model.

**Architecture:** The implementation stays documentation-first. `SKILL.md` remains the short entrypoint, while reference files define routing, schema, and safety behavior for the new two-file profile model. Template assets under `assets/tmp-layout/` provide reviewable staged candidates for both Portage rules and local profile updates.

**Tech Stack:** Markdown, YAML, Git, local filesystem structure under `~/locez-skills`

---

## File Structure

### Repository Documentation

- Existing: `/home/locez/locez-skills/docs/specs/2026-03-12-gentoo-maintenance-skill-design.md`
- Modify: `/home/locez/locez-skills/docs/plans/2026-03-12-gentoo-maintenance-implementation-plan.md`

### Skill Entry And Metadata

- Modify: `/home/locez/locez-skills/gentoo-maintenance/SKILL.md`
- Existing: `/home/locez/locez-skills/gentoo-maintenance/agents/openai.yaml`

### Reference Files

- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/host-roles.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/task-types.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/portage-file-placement.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/decision-matrix.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/command-strategy.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/safety-gates.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/binpkg-policy.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/host-profile-schema.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/agent-preferences-schema.md`

### Asset Templates

- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/review-summary.txt`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.custom`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.zz-autounmask`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.use.topic`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.mask.pins`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/gm-host-profile.yaml`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/gm-agent-preferences.yaml`

## Chunk 1: Entry Workflow And Local Profile Model

### Task 1: Rewrite The Core `SKILL.md`

**Files:**
- Modify: `/home/locez/locez-skills/gentoo-maintenance/SKILL.md`
- Reference: `/home/locez/locez-skills/docs/specs/2026-03-12-gentoo-maintenance-skill-design.md`

- [ ] **Step 1: Open the approved spec and current skill together**

Run:
```bash
sed -n '1,260p' /home/locez/locez-skills/docs/specs/2026-03-12-gentoo-maintenance-skill-design.md
sed -n '1,220p' /home/locez/locez-skills/gentoo-maintenance/SKILL.md
```
Expected: the spec mentions `/etc/portage/gm-host-profile.yaml` and `/etc/portage/gm-agent-preferences.yaml`, while the current skill still needs to be updated to match it

- [ ] **Step 2: Rewrite the workflow entry so it loads local profile sources before heuristics**

Add these requirements:
- read `gm-agent-preferences.yaml` and `gm-host-profile.yaml` first
- determine missing task-critical fields
- ask one question at a time when a missing field materially affects the answer
- allow read-only analysis to continue with temporary conclusions only
- stage any durable profile update under `/tmp/gentoo-maintenance/`

- [ ] **Step 3: Update the quick-routing and safety language**

Ensure `SKILL.md` explicitly states:
- machine-wide preferences belong in `gm-host-profile.yaml`
- durable user workflow overrides belong in `gm-agent-preferences.yaml`
- missing profile data is not permission to guess silently
- writing either `gm-*.yaml` file is a reviewed system write

- [ ] **Step 4: Link the new schema reference**

Reference all required files:
- `references/host-roles.md`
- `references/task-types.md`
- `references/portage-file-placement.md`
- `references/decision-matrix.md`
- `references/command-strategy.md`
- `references/safety-gates.md`
- `references/binpkg-policy.md`
- `references/host-profile-schema.md`
- `references/agent-preferences-schema.md`

- [ ] **Step 5: Verify the entrypoint stays concise**

Run:
```bash
wc -l /home/locez/locez-skills/gentoo-maintenance/SKILL.md
```
Expected: `SKILL.md` remains comfortably below 500 lines

### Task 2: Define The Two Local Schema References

**Files:**
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/host-profile-schema.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/agent-preferences-schema.md`

- [ ] **Step 1: Rewrite `host-profile-schema.md` around the approved system path**

Document:
- recommended path `/etc/portage/gm-host-profile.yaml`
- common required fields
- conditional fields such as `allow_non_core_feature_loss`
- a small YAML example
- guidance to keep the file strategic rather than package-level

- [ ] **Step 2: Create `agent-preferences-schema.md` for durable user overrides**

Document:
- recommended path `/etc/portage/gm-agent-preferences.yaml`
- override categories such as host treatment, workflow, and rules to follow
- examples for “respect current layout” and “ask before trading feature completeness for binpkg convenience”
- guidance on what should remain current-turn-only instead of being persisted

- [ ] **Step 3: Run a schema consistency check**

Run:
```bash
rg -n "gm-host-profile.yaml|gm-agent-preferences.yaml|prefer_binpkg_when_possible|allow_non_core_feature_loss|rules_to_follow" /home/locez/locez-skills/gentoo-maintenance
```
Expected: the two schema docs and `SKILL.md` use the same field names and file paths

- [ ] **Step 4: Commit chunk 1**

```bash
git -C /home/locez/locez-skills add gentoo-maintenance/SKILL.md gentoo-maintenance/references/host-profile-schema.md gentoo-maintenance/references/agent-preferences-schema.md
git -C /home/locez/locez-skills commit -m "docs: add gentoo maintenance local profile model"
```

## Chunk 2: Decision Routing And Safety Rules

### Task 3: Update Role And Task Classification References

**Files:**
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/host-roles.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/task-types.md`

- [ ] **Step 1: Rewrite `host-roles.md` to include precedence and ambiguity handling**

Cover:
- explicit current-turn instruction
- `gm-agent-preferences.yaml` override
- `gm-host-profile.yaml`
- heuristics as last resort
- stop-and-ask behavior when missing fields still affect role choice

- [ ] **Step 2: Update `task-types.md` to mention task-driven field requirements**

For each task type, add:
- what profile fields are commonly needed
- when binpkg preference affects the recommendation
- when layout preferences affect hygiene advice
- when the task should continue read-only with temporary conclusions

- [ ] **Step 3: Verify the boundaries between role and task docs**

Run:
```bash
sed -n '1,240p' /home/locez/locez-skills/gentoo-maintenance/references/host-roles.md
sed -n '1,260p' /home/locez/locez-skills/gentoo-maintenance/references/task-types.md
```
Expected: `host-roles.md` focuses on precedence and ambiguity, while `task-types.md` focuses on evidence and field needs per task

### Task 4: Update Placement, Decision, Safety, And Binpkg References

**Files:**
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/portage-file-placement.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/decision-matrix.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/safety-gates.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/binpkg-policy.md`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/references/command-strategy.md`

- [ ] **Step 1: Update `portage-file-placement.md` for the two-file local model**

Make sure it says:
- `gm-host-profile.yaml` is for machine-level strategy
- `gm-agent-preferences.yaml` is for durable workflow overrides
- neither file is a package-rule dumping ground
- staged profile updates belong under `/tmp/gentoo-maintenance/`

- [ ] **Step 2: Update `decision-matrix.md` to include profile-sensitive recommendation style**

Add language showing that:
- `gm-agent-preferences.yaml` can change recommendation style without changing package placement
- `gm-host-profile.yaml` can change strategy selection such as binpkg preference and acceptable feature trimming
- temporary conclusions must be marked when critical fields are missing

- [ ] **Step 3: Update `safety-gates.md` and `command-strategy.md`**

Document:
- writes to `gm-*.yaml` files are reviewed system writes
- read-only analysis may continue with incomplete profile data
- final recommendations must stop short when missing fields still affect execution
- `--complete-graph=y` and `--autounmask-backtrack=y` guidance remains unchanged unless profile-sensitive strategy calls for additional caution

- [ ] **Step 4: Update `binpkg-policy.md`**

Document:
- `prefer_binpkg_when_possible`
- `allow_non_core_feature_loss`
- the rule that binpkg tradeoffs should be asked about when absent instead of guessed

- [ ] **Step 5: Run cross-reference checks for old and new model terms**

Run:
```bash
rg -n "~/.config/locez-skills|gentoo-host-profile|gm-host-profile.yaml|gm-agent-preferences.yaml|temporary_assumptions|final_decision_blocked_by_profile" /home/locez/locez-skills/gentoo-maintenance /home/locez/locez-skills/docs/specs
```
Expected: no active documentation still routes to the old `~/.config/locez-skills` path, and the new `gm-*` terms appear where routing and safety are defined

- [ ] **Step 6: Commit chunk 2**

```bash
git -C /home/locez/locez-skills add gentoo-maintenance/references/host-roles.md gentoo-maintenance/references/task-types.md gentoo-maintenance/references/portage-file-placement.md gentoo-maintenance/references/decision-matrix.md gentoo-maintenance/references/safety-gates.md gentoo-maintenance/references/binpkg-policy.md gentoo-maintenance/references/command-strategy.md
git -C /home/locez/locez-skills commit -m "docs: refine gentoo maintenance decision routing"
```

## Chunk 3: Templates, Metadata, And Validation

### Task 5: Add Staged Templates For Local Profile Updates

**Files:**
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/review-summary.txt`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/gm-host-profile.yaml`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/gm-agent-preferences.yaml`

- [ ] **Step 1: Expand `review-summary.txt` for profile-sensitive runs**

Include placeholders for:
- loaded profile sources
- missing profile fields
- temporary assumptions
- whether `final_decision_blocked_by_profile` is true
- copy target and merge mode for any `gm-*.yaml` candidate

- [ ] **Step 2: Create `gm-host-profile.yaml` staged example**

Include placeholder keys for:
- `role`
- `prefer_binpkg_when_possible`
- `prefer_tmp_candidates`
- `require_manual_review_for_writes`
- `allow_non_core_feature_loss`
- `optimize_for`
- `high_risk_areas`
- `notes`

- [ ] **Step 3: Create `gm-agent-preferences.yaml` staged example**

Include placeholder keys for:
- `prefer_question_when_profile_incomplete`
- `allow_readonly_analysis_without_full_profile`
- `host_overrides`
- `workflow`
- `rules_to_follow`

- [ ] **Step 4: Verify the new templates are obviously examples**

Run:
```bash
sed -n '1,220p' /home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/review-summary.txt
sed -n '1,220p' /home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/gm-host-profile.yaml
sed -n '1,220p' /home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/gm-agent-preferences.yaml
```
Expected: the files are generic templates with placeholders and no private or host-specific data

### Task 6: Refresh Existing Portage Candidate Templates And Metadata

**Files:**
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.custom`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.zz-autounmask`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.use.topic`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.mask.pins`
- Modify: `/home/locez/locez-skills/gentoo-maintenance/agents/openai.yaml`

- [ ] **Step 1: Refresh the existing Portage templates**

Ensure the placeholder comments demonstrate:
- direct long-term intent
- dependency provenance comments
- topic ownership
- temporary staging language
- compatibility with the new review summary terminology

- [ ] **Step 2: Update `agents/openai.yaml`**

Ensure metadata mentions:
- Portage conflicts
- `@world` upgrades
- `/etc/portage` cleanup
- binpkg and VPS tradeoffs
- local profile and workflow preference handling

- [ ] **Step 3: Run a structure and trigger audit**

Run:
```bash
find /home/locez/locez-skills/gentoo-maintenance -maxdepth 3 -type f | sort
wc -l /home/locez/locez-skills/gentoo-maintenance/SKILL.md
rg -n "gm-host-profile.yaml|gm-agent-preferences.yaml|prefer_binpkg_when_possible|rules_to_follow" /home/locez/locez-skills/gentoo-maintenance
```
Expected: only intended files exist, `SKILL.md` stays lean, and the new profile model is visible in the right files

- [ ] **Step 4: Run manual pressure-scenario checks**

Check whether the updated skill would route these correctly:
- KDE or Qt world-upgrade conflict on a desktop host with no stored binpkg preference
- VPS request to avoid local compilation when `allow_non_core_feature_loss` is missing
- hygiene request where the user previously said to preserve their current layout
- mixed host where heuristics say desktop but `gm-agent-preferences.yaml` says to treat it as VPS

Expected: each scenario points to the right references, asks for missing critical fields one at a time, and preserves the review gate before any system write

- [ ] **Step 5: Commit chunk 3**

```bash
git -C /home/locez/locez-skills add gentoo-maintenance/assets/tmp-layout gentoo-maintenance/agents/openai.yaml
git -C /home/locez/locez-skills commit -m "docs: add gentoo maintenance profile templates"
```

- [ ] **Step 6: Final repository status check**

Run:
```bash
git -C /home/locez/locez-skills status --short
```
Expected: clean working tree

## Execution Notes

- Use `@writing-skills` when implementing this documentation-heavy skill change.
- Use `@verification-before-completion` before claiming the skill is finished.
- Do not add repo-wide documents or migration tooling unless implementation proves they are necessary.
- Keep private host facts out of the repository and inside staged examples only as placeholders.
- If plan execution uncovers a need for backward compatibility with the old `~/.config/locez-skills` path, document that as an explicit follow-up instead of silently expanding scope.

## Ready State

After this plan is saved, the next execution step is to implement it using `@writing-skills`.

# Gentoo Maintenance Skill Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable open-source `gentoo-maintenance` skill in `~/locez-skills`, with a concise `SKILL.md`, focused reference files, staging templates, and validation rules aligned with the approved spec.

**Architecture:** The implementation is documentation-first. `SKILL.md` stays lean and acts as the workflow entrypoint, while detailed policy lives in `references/`. Reusable candidate file layouts live in `assets/tmp-layout/`, and validation focuses on discoverability, safety gates, and keeping the skill concise enough to load reliably.

**Tech Stack:** Markdown, YAML, Git, local filesystem structure under `~/locez-skills`

---

## File Structure

### Repository Documentation

- Existing: `/home/locez/locez-skills/docs/specs/2026-03-12-gentoo-maintenance-skill-design.md`
- Create: `/home/locez/locez-skills/docs/plans/2026-03-12-gentoo-maintenance-implementation-plan.md`

### Skill Entry And Metadata

- Create: `/home/locez/locez-skills/gentoo-maintenance/SKILL.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/agents/openai.yaml`

### Reference Files

- Create: `/home/locez/locez-skills/gentoo-maintenance/references/host-roles.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/task-types.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/portage-file-placement.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/decision-matrix.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/command-strategy.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/safety-gates.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/binpkg-policy.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/host-profile-schema.md`

### Asset Templates

- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/review-summary.txt`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.custom`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.zz-autounmask`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.use.topic`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.mask.pins`

## Chunk 1: Skill Skeleton And Entry Workflow

### Task 1: Create The Plan Path And Save This Plan

**Files:**
- Create: `/home/locez/locez-skills/docs/plans/2026-03-12-gentoo-maintenance-implementation-plan.md`

- [ ] **Step 1: Create the plans directory**

Run: `mkdir -p /home/locez/locez-skills/docs/plans`
Expected: directory exists with no error output

- [ ] **Step 2: Copy this plan into the repository**

Run: `cp /tmp/2026-03-12-gentoo-maintenance-implementation-plan.md /home/locez/locez-skills/docs/plans/2026-03-12-gentoo-maintenance-implementation-plan.md`
Expected: plan file exists in `docs/plans`

- [ ] **Step 3: Verify the saved plan**

Run: `sed -n '1,80p' /home/locez/locez-skills/docs/plans/2026-03-12-gentoo-maintenance-implementation-plan.md`
Expected: header matches this plan

### Task 2: Write The Core SKILL.md

**Files:**
- Create: `/home/locez/locez-skills/gentoo-maintenance/SKILL.md`
- Reference: `/home/locez/locez-skills/docs/specs/2026-03-12-gentoo-maintenance-skill-design.md`

- [ ] **Step 1: Draft the frontmatter with strong trigger wording**

Include:
- `name: gentoo-maintenance`
- `description: Use when ...`

The description should trigger on:
- Portage conflicts
- `@world` upgrades
- `/etc/portage` cleanup
- binpkg and VPS tradeoff decisions
- ebuild and USE policy placement decisions

- [ ] **Step 2: Write the skill overview and hard safety rules**

Include:
- purpose of the skill
- requirement to identify host role first
- requirement to identify task type second
- hard rule that only `/tmp` and read-only work may proceed without review

- [ ] **Step 3: Write the core workflow**

Document this fixed flow:
1. identify host role
2. identify task type
3. assign risk level
4. gather only the needed evidence
5. classify change category
6. decide target file class
7. generate `/tmp/gentoo-maintenance/` candidates if needed
8. stop at review gate before any write

- [ ] **Step 4: Link to reference files instead of embedding detail**

Reference:
- `references/host-roles.md`
- `references/task-types.md`
- `references/portage-file-placement.md`
- `references/decision-matrix.md`
- `references/command-strategy.md`
- `references/safety-gates.md`
- `references/binpkg-policy.md`
- `references/host-profile-schema.md`

- [ ] **Step 5: Verify `SKILL.md` stays lean**

Run: `wc -l /home/locez/locez-skills/gentoo-maintenance/SKILL.md`
Expected: comfortably below 500 lines

- [ ] **Step 6: Commit the skeleton and skill entrypoint**

```bash
git -C /home/locez/locez-skills add docs/plans/2026-03-12-gentoo-maintenance-implementation-plan.md gentoo-maintenance/SKILL.md
git -C /home/locez/locez-skills commit -m "docs: add gentoo maintenance implementation plan and skill entrypoint"
```

## Chunk 2: Reference Set

### Task 3: Write Host Role And Task Type References

**Files:**
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/host-roles.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/task-types.md`

- [ ] **Step 1: Write `host-roles.md`**

Cover:
- `desktop`, `vps`, `binpkg-builder`, `mixed`
- role resolution priority
- when heuristics are allowed
- when to stop and ask

- [ ] **Step 2: Write `task-types.md`**

Cover:
- all six task types
- their goals
- what evidence each task type should gather
- when one task type should hand off to another

- [ ] **Step 3: Verify both references are concise and not duplicative**

Run:
```bash
sed -n '1,220p' /home/locez/locez-skills/gentoo-maintenance/references/host-roles.md
sed -n '1,260p' /home/locez/locez-skills/gentoo-maintenance/references/task-types.md
```
Expected: responsibilities are distinct and non-overlapping

### Task 4: Write Placement And Decision References

**Files:**
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/portage-file-placement.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/decision-matrix.md`

- [ ] **Step 1: Write `portage-file-placement.md`**

Cover:
- `package.accept_keywords/custom`
- `package.accept_keywords/zz-autounmask`
- `package.use/<topic>`
- `package.use/zz-autounmask`
- `package.mask`
- host profile
- `/tmp` staging

- [ ] **Step 2: Write `decision-matrix.md`**

Map:
- host role
- task type
- change category

To:
- target file class
- preferred behavior
- expected review posture

- [ ] **Step 3: Add one short example per change category**

Examples should show:
- direct intent
- dependency exception
- topic policy
- host policy
- temporary fix

- [ ] **Step 4: Commit the role, task, placement, and decision references**

```bash
git -C /home/locez/locez-skills add gentoo-maintenance/references/host-roles.md gentoo-maintenance/references/task-types.md gentoo-maintenance/references/portage-file-placement.md gentoo-maintenance/references/decision-matrix.md
git -C /home/locez/locez-skills commit -m "docs: add gentoo maintenance role and decision references"
```

## Chunk 3: Risk, Safety, Binpkg, And Profile Policy

### Task 5: Write Command, Safety, Binpkg, And Host Profile References

**Files:**
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/command-strategy.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/safety-gates.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/binpkg-policy.md`
- Create: `/home/locez/locez-skills/gentoo-maintenance/references/host-profile-schema.md`

- [ ] **Step 1: Write `command-strategy.md`**

Cover:
- risk levels `low`, `medium`, `high`, `critical`
- Level 1 to Level 4 command strength
- when `--complete-graph=y` is default
- when `--autounmask-backtrack=y` is justified

- [ ] **Step 2: Write `safety-gates.md`**

Cover:
- what counts as a write
- what actions require stopping
- what conditions require reduced automation
- requirement that auto mode cannot bypass the review gate

- [ ] **Step 3: Write `binpkg-policy.md`**

Cover:
- VPS and builder feature-trimming policy
- preference order: USE strategy, package strategy, then patching
- preserving core function while allowing non-core feature loss

- [ ] **Step 4: Write `host-profile-schema.md`**

Cover:
- recommended local path
- field meanings
- small example schema
- warning against duplicating `/etc/portage`

- [ ] **Step 5: Verify cross-reference consistency**

Run:
```bash
rg -n "complete-graph|autounmask-backtrack|review gate|host profile|non-core feature" /home/locez/locez-skills/gentoo-maintenance
```
Expected: terms appear in the right files with consistent wording

- [ ] **Step 6: Commit the policy references**

```bash
git -C /home/locez/locez-skills add gentoo-maintenance/references/command-strategy.md gentoo-maintenance/references/safety-gates.md gentoo-maintenance/references/binpkg-policy.md gentoo-maintenance/references/host-profile-schema.md
git -C /home/locez/locez-skills commit -m "docs: add gentoo maintenance policy references"
```

## Chunk 4: Assets, Metadata, And Validation

### Task 6: Create Template Assets For `/tmp` Candidate Output

**Files:**
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/review-summary.txt`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.custom`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.accept_keywords.zz-autounmask`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.use.topic`
- Create: `/home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/package.mask.pins`

- [ ] **Step 1: Write `review-summary.txt` template**

Include placeholders for:
- context
- findings
- decisions
- copy targets
- merge mode

- [ ] **Step 2: Write the keyword and USE templates**

Include short placeholder comments demonstrating:
- direct intent layout
- dependency provenance comments
- topic file structure
- mask note format

- [ ] **Step 3: Verify templates are clearly examples, not live policy**

Run: `sed -n '1,200p' /home/locez/locez-skills/gentoo-maintenance/assets/tmp-layout/*`
Expected: placeholder content is generic and open-source safe

### Task 7: Create UI Metadata And Validate The Skill

**Files:**
- Create: `/home/locez/locez-skills/gentoo-maintenance/agents/openai.yaml`
- Verify: `/home/locez/locez-skills/gentoo-maintenance/SKILL.md`
- Verify: `/home/locez/locez-skills/gentoo-maintenance/references/*.md`

- [ ] **Step 1: Write `agents/openai.yaml`**

Ensure metadata matches `SKILL.md`:
- display name fits the skill purpose
- short description reflects triggers, not workflow
- default prompt fits Portage maintenance use

- [ ] **Step 2: Run a concise structure audit**

Run:
```bash
find /home/locez/locez-skills/gentoo-maintenance -maxdepth 3 -type f | sort
wc -l /home/locez/locez-skills/gentoo-maintenance/SKILL.md
```
Expected: only intended files exist and `SKILL.md` remains lean

- [ ] **Step 3: Run manual pressure-scenario checks**

Check whether the skill would route these correctly:
- Qt/KDE world upgrade conflict on desktop
- Steam-induced multilib dependency exception
- VPS request to avoid local compilation by trimming non-core features
- `/etc/portage` cleanup request with mixed direct intent and autounmask residue

Expected: each scenario points to the right references and preserves the write-review rule

- [ ] **Step 4: Commit the assets and metadata**

```bash
git -C /home/locez/locez-skills add gentoo-maintenance/assets/tmp-layout gentoo-maintenance/agents/openai.yaml
git -C /home/locez/locez-skills commit -m "docs: add gentoo maintenance assets and metadata"
```

- [ ] **Step 5: Final repository status check**

Run: `git -C /home/locez/locez-skills status --short`
Expected: clean working tree

## Execution Notes

- Keep `SKILL.md` concise and push details into references.
- Do not add extra repo documents such as `README.md` or `CHANGELOG.md` for this skill unless explicitly requested.
- Do not place private host data into the public repository.
- If implementation reveals the scope is still too large, split the plan by chunk rather than bloating `SKILL.md`.

## Ready State

After this plan is saved, the next execution step is to implement it using `writing-skills` for the actual skill authoring work.

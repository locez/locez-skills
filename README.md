# locez-skills

Reusable AI skills for agentic engineering work.

[中文说明](README.zh-CN.md)

This repository collects workflow, maintenance, analysis, and judgment-calibration skills that can be reused across agents, machines, and projects without embedding private host state. A skill is not just a prompt. It is a small, versioned working protocol that tells the agent when to use it, how to reason about the task, what artifacts or checks matter, and when the work is ready to hand back.

For a longer beginner guide, see [docs/skill-primer.md](docs/skill-primer.md).

Deep dives from that guide:

- [Locez Lens: why scope calibration matters](docs/skill-primer.md#locez-lens-deep-dive)
- [workflow-skill-architect: turning long prompts into workflows](docs/skill-primer.md#workflow-skill-architect-deep-dive)
- [How Locez Lens and workflow-skill-architect work together](docs/skill-primer.md#lens-and-workflow-skill-architect)

## Skill Catalog

| Skill | Repository Path | Use When | What It Helps With |
| --- | --- | --- | --- |
| `$gentoo-maintenance` | `gentoo-maintenance/` | Handling Portage conflicts, `@world` upgrades, `/etc/portage` cleanup, binpkg tradeoffs, or local Gentoo policy placement. | Classifies host role and task type, separates local preferences from generated rules, stages candidate Portage changes under `/tmp`, and stops before non-`/tmp` writes. |
| `$locez-overlay-bump-workflow` | `locez-overlay-bump-workflow/` | Maintaining packages in `/home/locez/locez-overlay`, especially bumping, removing, or reconciling nvchecker-tracked packages. | Distinguishes release-managed, live-only, and removed packages; keeps nvchecker automation aligned with package state; requires local ebuild verification for meaningful changes. |
| `$repo-visual-analysis` | `repo-visual-analysis/` | Understanding a repository, generating visual architecture or flow maps, producing a clickable visual report, or finding evidence-backed improvement opportunities. | Builds quick scans, focused maps, Mermaid or rendered visual reports, claim/evidence traces, and repository-informed opportunity lists without pretending weak evidence is certain. |
| `$workflow-skill-architect` | `workflow-skill-architect/` | Creating or refactoring complex workflow skills, especially overloaded `SKILL.md` files, unclear sub-agent roles, repeated confirmations, or weak validation. | Turns long prompts into structured workflow skills with orchestration rules, references, artifact protocols, optional agent contracts, concurrency boundaries, and validation gates. |
| `$locez-lens` | `lens/` | Any bug, review, writing, architecture, product, research, or code-change task where the visible issue may be too narrow. | Adds a lightweight scope check before acting so the agent can decide whether the request is an instance, symptom, boundary failure, repeated pattern, or wrong framing. |

## Which Skill Should I Start With?

- For Gentoo system maintenance, start with `$gentoo-maintenance`.
- For `locez-overlay` package bump or nvchecker work, start with `$locez-overlay-bump-workflow`.
- For codebase understanding, visual maps, or architecture reports, start with `$repo-visual-analysis`.
- For designing or repairing another skill, start with `$workflow-skill-architect`.
- For ambiguous fixes, reviews, decisions, or writing where the framing may be too narrow, start with `$locez-lens`.

Typical requests:

```text
$gentoo-maintenance analyze this @world slot conflict
$gentoo-maintenance help me clean package.accept_keywords
$locez-overlay-bump-workflow bump app-misc/example
$repo-visual-analysis create a visual report for this repository
$workflow-skill-architect refactor this data-cleaning prompt into a workflow skill
$locez-lens check whether this fix is scoped too narrowly
```

## Installing Into Agents

These skills follow the `SKILL.md` package shape, so the same repository checkout can be symlinked into several agent runtimes.

| Runtime | Personal Skill Directory | Project Skill Directory | Notes |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` | Personal skills apply across projects; project skills stay with one repository. |
| Codex / Agent Skills compatible tools | `~/.agents/skills/<skill-name>/` | Tool-dependent | Useful as a shared directory for tools that read the Agent Skills convention. Some Codex setups may also read `~/.codex/skills/`. |
| OpenCode | `~/.config/opencode/skills/<skill-name>/` | `.opencode/skills/<skill-name>/` | OpenCode also discovers Claude-compatible `.claude/skills/` and agent-compatible `.agents/skills/` locations. |
| Hermes Agent | `~/.hermes/skills/<skill-name>/` | `skills/` or configured external directories | Hermes can also scan shared external directories such as `~/.agents/skills` via `skills.external_dirs`. |

Most skills use the same repository directory and skill name. For example, install globally for Claude Code:

```bash
mkdir -p ~/.claude/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.claude/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.claude/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.claude/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.claude/skills/workflow-skill-architect
```

Install into the shared Agent Skills directory used by Codex-style runtimes:

```bash
mkdir -p ~/.agents/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.agents/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.agents/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.agents/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.agents/skills/workflow-skill-architect
```

`locez-lens` is stored in the shorter `lens/` directory:

```bash
ln -s ~/locez-skills/lens ~/.claude/skills/locez-lens
ln -s ~/locez-skills/lens ~/.agents/skills/locez-lens
```

For OpenCode:

```bash
mkdir -p ~/.config/opencode/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.config/opencode/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.config/opencode/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.config/opencode/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.config/opencode/skills/workflow-skill-architect
ln -s ~/locez-skills/lens ~/.config/opencode/skills/locez-lens
```

For Hermes Agent, either symlink directly:

```bash
mkdir -p ~/.hermes/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.hermes/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.hermes/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.hermes/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.hermes/skills/workflow-skill-architect
ln -s ~/locez-skills/lens ~/.hermes/skills/locez-lens
```

Or keep shared skills in `~/.agents/skills` and add that directory to `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
```

If a link already exists and you want to recreate it:

```bash
RUNTIME_SKILL_DIR=~/.agents/skills
rm "$RUNTIME_SKILL_DIR/<skill-name>"
ln -s ~/locez-skills/<repo-directory> "$RUNTIME_SKILL_DIR/<skill-name>"
```

After installing or updating a skill, restart the agent or start a new session if your runtime does not hot-reload skill directories.

## Repository Map

```text
<skill-name>/
  SKILL.md       # trigger, core rules, and navigation
  references/    # detailed workflow rules, templates, contracts, validation
  scripts/       # deterministic helpers used by the skill
  agents/        # UI metadata for skill listings
  assets/        # optional runtime assets

docs/
  specs/         # design history and decisions
  plans/         # implementation plans
```

Not every skill has every optional directory. Keep skill directories focused on runtime resources; put repository-level documentation in `README.md`, `README.zh-CN.md`, or `docs/`.

## Repository Rules

- Keep private machine state out of this repository.
- Keep `SKILL.md` lean and move detailed procedures into `references/`.
- Prefer deterministic helpers in `scripts/` when repeated work should not depend on model memory.
- Prefer templates in `assets/` over copying live system configuration into the repo.
- Record design history in `docs/specs/`.
- Record implementation plans in `docs/plans/`.
- Validate skills after meaningful changes.

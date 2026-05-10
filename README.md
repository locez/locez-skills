# locez-skills

Open-source repository for reusable AI skills.

This repository is meant to hold workflow and maintenance skills that can be reused across machines and projects without embedding private host state.

## Layout

```text
docs/
  specs/   # design docs and decisions
  plans/   # implementation plans

gentoo-maintenance/
  SKILL.md
  references/
  assets/
  agents/

locez-overlay-bump-workflow/
  SKILL.md
  agents/

workflow-skill-architect/
  SKILL.md
  references/
  agents/
```

## Current Skills

### `gentoo-maintenance`

Use this skill for:

- Portage conflicts
- `@world` upgrade analysis
- `/etc/portage` cleanup and rule placement
- VPS and binpkg feature-trimming tradeoffs
- deciding whether a rule belongs in `custom`, `zz-autounmask`, a topic file, or `package.mask`

The skill is designed to:

- identify host role first
- identify task type second
- classify changes before choosing file placement
- stage candidate files under `/tmp/gentoo-maintenance/`
- stop for review before any non-`/tmp` write

### `locez-overlay-bump-workflow`

Use this skill for package maintenance in `/home/locez/locez-overlay` when:

- bumping nvchecker-tracked packages
- removing packages from the overlay
- reconciling live-only or removed packages with `[nvchecker]` issues
- deciding whether a package belongs in `.github/workflows/nvchecker.toml`

The skill is designed to:

- classify packages as `release-managed`, `live-only`, or `removed`
- keep release-bump automation aligned with package state
- centralize issue handling in `.github/workflows/nvchecker.yml`
- require local manifest, pkgcheck, and ebuild verification for meaningful ebuild changes

### `workflow-skill-architect`

Use this skill when creating or refactoring complex workflow skills, especially when an existing skill has:

- an overloaded main `SKILL.md`
- unclear sub-agent responsibilities
- scattered human confirmations
- missing intermediate artifacts
- weak validation or traceability
- needless serialization of independent work

The skill is designed to:

- keep `SKILL.md` as a compact orchestrator
- move detailed procedures into `references/`
- define sub-agent contracts and artifact protocols only when they change behavior
- choose the smallest useful refactor level before recommending structure
- default to single-agent review unless an agent set adds real signal
- mark serial, parallelizable, barrier, and merge stages when concurrency is useful
- compress repeated questions into review gates

## Installing Into Codex

For local development, install a skill from this repository with a symlink:

```bash
ln -s ~/locez-skills/<skill-name> ~/.codex/skills/<skill-name>
```

If the link already exists and you want to recreate it:

```bash
rm ~/.codex/skills/<skill-name>
ln -s ~/locez-skills/<skill-name> ~/.codex/skills/<skill-name>
```

After installing or updating a skill, restart Codex so it picks up the new files.

## Using The Skill

In a new Codex session, invoke a skill explicitly:

```text
$gentoo-maintenance 帮我分析这次 @world 冲突
```

Typical requests:

- `$gentoo-maintenance 这次 slot conflict 的根因是什么`
- `$gentoo-maintenance 帮我整理 package.accept_keywords`
- `$gentoo-maintenance 这个 USE 应该进 steam 还是 system`
- `$locez-overlay-bump-workflow 帮我 bump app-misc/example`
- `$workflow-skill-architect 帮我把这个数据清洗 prompt 改成 workflow skill`

## Repository Rules

- Keep private machine state out of this repository.
- Keep `SKILL.md` lean and move details into `references/`.
- Prefer templates in `assets/` over copying live system config into the repo.
- Record design history in `docs/specs/`.
- Record implementation plans in `docs/plans/`.
- Keep skill directories focused on runtime resources; put repository documentation in `README.md` or `docs/`.

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
```

## Current Skill

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

## Installing Into Codex

For local development, install the current worktree copy with a symlink:

```bash
ln -s ~/locez-skills/.worktrees/gentoo-maintenance-skill/gentoo-maintenance ~/.codex/skills/gentoo-maintenance
```

If the link already exists and you want to recreate it:

```bash
rm ~/.codex/skills/gentoo-maintenance
ln -s ~/locez-skills/.worktrees/gentoo-maintenance-skill/gentoo-maintenance ~/.codex/skills/gentoo-maintenance
```

After installing or updating a skill, restart Codex so it picks up the new files.

## Using The Skill

In a new Codex session, invoke it explicitly:

```text
$gentoo-maintenance 帮我分析这次 @world 冲突
```

Typical requests:

- `$gentoo-maintenance 这次 slot conflict 的根因是什么`
- `$gentoo-maintenance 帮我整理 package.accept_keywords`
- `$gentoo-maintenance 这个 USE 应该进 steam 还是 system`

## Repository Rules

- Keep private machine state out of this repository.
- Keep `SKILL.md` lean and move details into `references/`.
- Prefer templates in `assets/` over copying live system config into the repo.
- Record design history in `docs/specs/`.
- Record implementation plans in `docs/plans/`.

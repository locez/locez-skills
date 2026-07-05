---
name: gentoo-ebuild
description: Use when working on Gentoo ebuilds, overlays, eclasses, Manifest files, metadata.xml, pkgdev, pkgcheck, ebuild QA, version bumps, new packages, package reviews, or Gentoo package pull requests.
---

# Gentoo Ebuild

## Purpose

Use this as the entry point for Gentoo package maintenance. Classify the task, load only the needed reference files, work from repository/local/official evidence, and validate with native Gentoo tools. This skill is not a replacement for target repository policy.

## Activation Protocol

1. Read local policy first: `AGENTS.md`, `README*`, `CONTRIBUTING*`, PR templates, and CI config.
2. Classify the request before editing: new package, version bump, revision update, QA/review fix, eclass decision, commit/PR prep, or mixed task.
3. For any non-trivial package edit, read `references/workflow.md` before task-specific references.
4. Keep workflow notes lightweight. Do not create persistent planning artifacts unless the repository or user asks for them.

## Core Rules

- Target repository policy overrides generic guidance here.
- Prefer existing package style and nearby precedent over generic templates.
- Use native tools directly: `pkgdev`, `pkgcheck`, `ebuild`, `emerge`, `git`, `gh`, `nvchecker` when relevant.
- Use bundled scripts only for narrow deterministic lint/fix work they explicitly own.
- Never choose eclasses from memory alone; verify from local Gentoo tree or official Gentoo sources.
- Do not add wrappers, queue systems, custom commit automation, or project-specific helper tools as part of this skill.
- Batch unresolved maintainer decisions into a single review gate when possible.
- Report what was tested, what was skipped, and why.

## Task Routing

- Mixed tasks or non-trivial package edits: read `references/workflow.md` first.
- New package: read `references/new-package.md`.
- Version bump or revision update: read `references/version-bump.md`.
- Eclass choice, phase behavior, or helper question: read `references/eclass-discovery.md`.
- QA failure, review, or test issue: read `references/qa.md`.
- Commit or PR preparation: read `references/commit-pr.md`.

## Evidence Order

1. Target repository policy and current package directory.
2. Similar packages in the same overlay.
3. Local main Gentoo tree, usually `/var/db/repos/gentoo`.
4. Local eclass files, usually `/var/db/repos/gentoo/eclass/*.eclass`.
5. Official Gentoo devmanual, eclass docs, and gentoo.git examples.
6. Upstream project documentation and release artifacts.

If evidence conflicts, state the conflict and prefer the current, local, package-specific source unless official Gentoo guidance clearly overrides it.

## Native Tool Baseline

Use these directly unless repository policy says otherwise. Resolve the bundled helper path from this skill directory; do not assume the target repository contains a copy of the script.

```bash
python3 <gentoo-ebuild-skill>/scripts/ensure_copyright_year.py --fix path/to/package-version.ebuild
pkgdev manifest category/package
pkgcheck scan category/package
ebuild category/package/package-version.ebuild clean compile install
pkgcheck scan --commits --net
pkgdev commit
```

Adjust commands to repository policy and local permissions.

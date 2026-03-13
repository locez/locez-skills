---
name: locez-overlay-bump-workflow
description: Use when bumping, removing, or reconciling nvchecker-tracked packages in locez-overlay, especially when deciding whether a package is release-managed, live-only, or no longer maintained
---

# locez-overlay Bump Workflow

## Overview

Use this skill for package maintenance in `/home/locez/locez-overlay`.

The core rule is simple: only packages with at least one non-`9999` ebuild are bump-managed. `9999`-only packages may still exist, but they should not create or keep open `nvchecker` bump issues.

## When To Use

Use this skill when the user asks to:

- bump a package in `locez-overlay`
- remove a package from the overlay
- reconcile GitHub `nvchecker` issues with the current repo state
- decide whether a package should stay in `.github/workflows/nvchecker.toml`
- adjust the bump automation in `.github/workflows/nvchecker.yml`

Do not use this skill for:

- generic Gentoo maintenance outside `locez-overlay`
- live-only `9999` package development that does not affect bump tracking
- merge or release management

## Package Classification

Classify the target package before changing anything:

- `release-managed`: the package directory exists and has at least one non-`9999` ebuild
- `live-only`: the package exists, but every ebuild is `9999`
- `removed`: the package directory or maintained release ebuilds are gone by intent

This classification drives both package edits and issue handling.

## Workflow

1. Work in `/home/locez/locez-overlay` or its active worktree, not in the skill repository.
2. Inspect:
   - the package directory
   - `.github/workflows/nvchecker.toml`
   - `.github/workflows/nvchecker.yml`
   - existing `[nvchecker]` issue state
3. Classify the package as `release-managed`, `live-only`, or `removed`.
4. Apply the matching action:
   - `release-managed`: bump the release ebuild, regenerate `Manifest`, keep `nvchecker` tracking
   - `live-only`: allow functional ebuild edits, but do not create or keep bump issues
   - `removed`: delete package files, remove the `nvchecker.toml` entry, and close stale bump issues
5. Keep issue logic centralized in `.github/workflows/nvchecker.yml`.

## Repository Rules

- `nvchecker.toml` may track maintained release packages and, only if intentionally useful, live-only packages for visibility.
- Removed packages must be deleted from `nvchecker.toml`.
- Open issues for removed or live-only packages should be commented and closed.
- Do not write process notes or skill drafts into the overlay repository.
- Do not perform merge actions as part of this workflow.

## Verification

For every meaningful ebuild change, run:

1. `pkgdev manifest`
2. `pkgcheck scan`

For each new or bumped release ebuild, also run:

`ebuild <target.ebuild> clean fetch unpack compile install clean`

If the ebuild supports useful tests and the cost is justified, run:

`ebuild <target.ebuild> test clean`

The final `clean` is required. Do not leave build residue behind after local verification.

## Required Output Shape

Default response structure:

- `Classification`
- `Changes`
- `Verification`
- `Open issue follow-up`
- `Risks`

## Common Mistakes

- treating `9999` packages as normal bump targets
- forgetting to remove deleted packages from `nvchecker.toml`
- leaving old `[nvchecker]` issues open after a package is dropped
- relying on GitHub CI instead of local verification
- writing skill or process docs into the overlay repository

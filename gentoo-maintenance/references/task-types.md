# Task Types

Use one task type per main request. Switch only when the evidence shows the work has changed.

## `world-upgrade`

Use for:

- `@world` dry-runs and execution planning
- large package refreshes
- desktop stack, toolchain, or broad dependency upgrades

Gather:

- current `emerge` output
- whether the solver stops early
- whether global consistency is at risk

Hand off to `conflict-debug` if blocks, slot conflicts, or autounmask fallout become the main issue.

## `conflict-debug`

Use for:

- block, slot, subslot, keyword, USE, mask, or binpkg mismatch analysis
- tracing one reported conflict back to top-level causes

Gather:

- exact error output
- root dependency chain
- relevant `/etc/portage` hits
- whether the rule is direct intent or dependency fallout

## `portage-hygiene`

Use for:

- reorganizing `/etc/portage`
- cleaning old autounmask files
- moving rules to more maintainable locations

Gather:

- current file list
- rule origin and age signals
- whether each rule is stable policy or residue

## `package-intent-change`

Use for:

- adding or removing a package from long-term policy
- deciding that a package should be tracked, pinned, or demoted

Gather:

- whether the package is direct user intent
- whether the change is short-term or long-term

## `binpkg-optimization`

Use for:

- VPS or builder cases where local compilation should be reduced
- deciding whether non-core features can be trimmed

Gather:

- package purpose
- core vs non-core features
- whether USE trimming solves the problem before patching

## `build-or-ebuild-adjustment`

Use for:

- ebuild behavior changes
- local patches or overlay adjustments
- package-level build strategy changes

Gather:

- why the build is happening
- whether the issue can be solved by USE, package selection, or binpkg policy first

## Output Expectation

Every run should report:

- chosen task type
- why that task type fits better than nearby alternatives

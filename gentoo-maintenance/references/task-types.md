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
- whether `prefer_binpkg_when_possible` changes the recommended path

Continue read-only with temporary conclusions if the missing binpkg preference would affect strategy.

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
- whether missing host policy changes the preferred fix

## `portage-hygiene`

Use for:

- reorganizing `/etc/portage`
- cleaning old autounmask files
- moving rules to more maintainable locations

Gather:

- current file list
- rule origin and age signals
- whether each rule is stable policy or residue
- whether `gm-agent-preferences.yaml` says to preserve the user's current layout

Continue read-only if layout preference is missing, but stage moves as temporary.

## `package-intent-change`

Use for:

- adding or removing a package from long-term policy
- deciding that a package should be tracked, pinned, or demoted

Gather:

- whether the package is direct user intent
- whether the change is short-term or long-term
- whether the rule belongs in a Portage file or a local profile file

## `binpkg-optimization`

Use for:

- VPS or builder cases where local compilation should be reduced
- deciding whether non-core features can be trimmed

Gather:

- package purpose
- core vs non-core features
- whether USE trimming solves the problem before patching
- `prefer_binpkg_when_possible`
- `allow_non_core_feature_loss`

Ask when either binpkg field is missing. Continue read-only only if the final recommendation would otherwise be guessed.

## `build-or-ebuild-adjustment`

Use for:

- ebuild behavior changes
- local patches or overlay adjustments
- package-level build strategy changes

Gather:

- why the build is happening
- whether the issue can be solved by USE, package selection, or binpkg policy first
- whether missing host policy changes the need for patching

## Output Expectation

Every run should report:

- chosen task type
- why that task type fits better than nearby alternatives
- which profile fields are required for this task

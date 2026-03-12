# Portage File Placement

Choose placement by intent, not by convenience.

## `package.accept_keywords/custom`

Use for direct, long-term user intent:

- packages the user intentionally tracks on `~arch`
- live packages the user deliberately wants
- exact-version keyword exceptions the user means to keep

Bad fit:

- helper packages pulled only by dependencies
- one-off solver fallout

## `package.accept_keywords/zz-autounmask`

Use for indirect dependency exceptions:

- helper packages not selected directly by the user
- temporary or regenerable keyword fallout

Rules:

- always include short provenance comments
- keep comments short and scenario-based
- do not preserve raw, version-heavy autounmask chains

## `package.use/<topic>`

Use for durable topic policy:

- `steam`
- `kernel`
- `system`
- `sunshine`
- `cross-*`
- another clearly named topical file

This is where long-term themed policy belongs.

## `package.use/zz-autounmask`

Use for indirect USE exceptions that are not direct intent. Treat it as disposable and regenerable.

## `package.mask`

Use for durable "do not take this" policy:

- known-bad versions
- intentionally delayed major upgrades
- versions excluded for compatibility reasons

## Local Host Profile

Use the local profile for machine-wide preference:

- host role
- optimization goals
- tolerance for non-core feature loss
- high-risk areas

Do not mirror `/etc/portage` here.

## `/tmp/gentoo-maintenance/`

Use as the staging area for all unreviewed candidates. Default to staging first unless the user has already reviewed the final placement.

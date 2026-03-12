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

## `gm-host-profile.yaml`

Use `/etc/portage/gm-host-profile.yaml` for machine-level strategy:

- host role
- optimization goals
- binpkg preference
- tolerance for non-core feature loss
- high-risk areas

Do not mirror `/etc/portage` here.

## `gm-agent-preferences.yaml`

Use `/etc/portage/gm-agent-preferences.yaml` for durable workflow overrides:

- treat-this-host-as overrides
- review posture preferences
- layout-preservation rules
- other reusable agent behavior instructions

Do not store package-level rules here.

## `/tmp/gentoo-maintenance/`

Use as the staging area for all unreviewed candidates, including staged updates for `gm-host-profile.yaml` and `gm-agent-preferences.yaml`.

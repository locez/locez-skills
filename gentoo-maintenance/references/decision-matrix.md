# Decision Matrix

This matrix maps change category to preferred landing zone and review posture.

## Change Categories

| Category | Meaning |
|---|---|
| `direct-long-term-intent` | the user explicitly wants the package, version, or policy long-term |
| `dependency-exception` | the rule exists because another package pulls it in |
| `topic-policy` | the rule is part of a broader themed policy such as Steam, kernel, or crossdev |
| `host-policy` | the rule reflects machine-wide strategy or durable workflow guidance |
| `temporary-fix` | the rule only exists to test or unblock the current solve |

## Primary Routing

| Category | Preferred target | Review posture |
|---|---|---|
| `direct-long-term-intent` | `package.accept_keywords/custom` or `package.use/<topic>` | usually keep after review |
| `dependency-exception` | `zz-autounmask` file with provenance comments | keep disposable and easy to prune |
| `topic-policy` | `package.use/<topic>` or `package.mask` | keep with explicit topic ownership |
| `host-policy` | `gm-host-profile.yaml` or `gm-agent-preferences.yaml`, then derived Portage candidates if needed | review for host-wide impact |
| `temporary-fix` | `/tmp/gentoo-maintenance/` only | do not promote until proven stable |

## Profile-Sensitive Routing

- `gm-host-profile.yaml` changes strategy selection such as binpkg preference or acceptable feature trimming.
- `gm-agent-preferences.yaml` changes recommendation style, review posture, and host interpretation without changing package placement by itself.
- If a critical profile field is missing, keep the routing temporary and ask before promoting it.

## Task-Type Influence

### `world-upgrade`

- prefer stable routing
- do not mix temporary fixes into permanent files unless repeated evidence supports them
- if binpkg preference is missing, mark execution strategy as temporary

### `conflict-debug`

- prioritize root-cause tracing before placement
- dependency exceptions are common; avoid misclassifying them as user intent

### `portage-hygiene`

- default to staging proposed moves in `/tmp`
- preserve comments that explain why indirect rules exist
- respect durable layout-preservation rules from `gm-agent-preferences.yaml`

### `package-intent-change`

- direct intent should dominate
- if intent is unclear, stage first and ask

### `binpkg-optimization`

- treat feature trimming as policy, not as accidental residue
- record durable tradeoffs in topic files or `gm-host-profile.yaml`
- ask when binpkg tolerance is not explicitly known

### `build-or-ebuild-adjustment`

- prefer package strategy before patching
- if patching remains necessary, explain whether it is host-local or overlay policy

## Short Examples

- `direct-long-term-intent`: user tracks `app-editors/foo` on `~amd64` for daily use
- `dependency-exception`: `dev-python/bar` becomes `~amd64` only because another package requires it
- `topic-policy`: Steam needs 32-bit graphics stack rules grouped under `package.use/steam`
- `host-policy`: a VPS prefers binpkg and allows trimmed non-core features, while the user also wants layout-preserving hygiene advice
- `temporary-fix`: a one-off mask or USE toggle is staged in `/tmp` until the next world dry-run confirms it is still needed

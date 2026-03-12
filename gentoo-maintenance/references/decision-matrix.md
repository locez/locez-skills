# Decision Matrix

This matrix maps change category to preferred landing zone and review posture.

## Change Categories

| Category | Meaning |
|---|---|
| `direct-long-term-intent` | the user explicitly wants the package, version, or policy long-term |
| `dependency-exception` | the rule exists because another package pulls it in |
| `topic-policy` | the rule is part of a broader themed policy such as Steam, kernel, or crossdev |
| `host-policy` | the rule reflects machine-wide strategy, not a package-specific decision |
| `temporary-fix` | the rule only exists to test or unblock the current solve |

## Primary Routing

| Category | Preferred target | Review posture |
|---|---|---|
| `direct-long-term-intent` | `package.accept_keywords/custom` or `package.use/<topic>` | usually keep after review |
| `dependency-exception` | `zz-autounmask` file with provenance comments | keep disposable and easy to prune |
| `topic-policy` | `package.use/<topic>` or `package.mask` | keep with explicit topic ownership |
| `host-policy` | local host profile, then derived Portage candidates if needed | review for machine-wide impact |
| `temporary-fix` | `/tmp/gentoo-maintenance/` only | do not promote until proven stable |

## Task-Type Influence

### `world-upgrade`

- prefer stable routing
- do not mix temporary fixes into permanent files unless repeated evidence supports them

### `conflict-debug`

- prioritize root-cause tracing before placement
- dependency exceptions are common; avoid misclassifying them as user intent

### `portage-hygiene`

- default to staging proposed moves in `/tmp`
- preserve comments that explain why indirect rules exist

### `package-intent-change`

- direct intent should dominate
- if intent is unclear, stage first and ask

### `binpkg-optimization`

- treat feature trimming as policy, not as accidental residue
- record durable tradeoffs in topic files or local host profile

### `build-or-ebuild-adjustment`

- prefer package strategy before patching
- if patching remains necessary, explain whether it is host-local or overlay policy

## Short Examples

- `direct-long-term-intent`: user tracks `app-editors/foo` on `~amd64` for daily use
- `dependency-exception`: `dev-python/bar` becomes `~amd64` only because another package requires it
- `topic-policy`: Steam needs 32-bit graphics stack rules grouped under `package.use/steam`
- `host-policy`: a VPS allows trimming docs and optional GUI helpers to keep binpkg usage high
- `temporary-fix`: a one-off mask or USE toggle is staged in `/tmp` until the next world dry-run confirms it is still needed

# Command Strategy

Choose solver strength based on risk. Do not default to the heaviest mode.

## Risk Levels

| Risk | Typical cases |
|---|---|
| `low` | simple single-package queries, low-impact checks |
| `medium` | normal `@world` validation, moderate package policy changes |
| `high` | slot/subslot conflicts, autounmask early stop, desktop stack transitions |
| `critical` | kernel, boot, ZFS, GPU driver, or combined upgrade-plus-restructure work |

High-risk areas should raise the risk level by at least one step.

## Command Levels

### Level 1: Light Check

Use for low-risk or quick inspection:

```bash
emerge -pv <pkg>
```

or:

```bash
emerge -pvuD @world
```

### Level 2: Standard World Validation

Use for normal `@world` safety checks:

```bash
emerge -pvuDN --complete-graph=y @world
```

Desktop and VPS hosts should usually start here for meaningful `@world` work.

### Level 3: Heavy Conflict Resolution

Use when the solver stops too early or stack transitions are clearly complex:

```bash
emerge -pvuDN --complete-graph=y --autounmask-backtrack=y @world
```

Good triggers:

- autounmask suggestions cause early exit
- slot or subslot transitions need full rebuild planning
- Qt/KDE, Mesa, LLVM, or large Python stack upgrades are moving together

### Level 4: Execution

Use only after review:

```bash
emerge -avuDN --complete-graph=y [--autounmask-backtrack=y] @world
```

This is a write operation and must stop at the review gate first.

## Profile-Sensitive Notes

- Missing binpkg preference does not change the dry-run commands, but it may block the final recommendation for what to do next.
- Missing feature-loss tolerance should reduce confidence in any recommendation that trims optional features.
- `--complete-graph=y` and `--autounmask-backtrack=y` guidance should stay stable unless the user asks for a different safety posture.

## Policy Notes

- `--complete-graph=y` is the default recommendation for desktop and VPS `@world` work.
- `--autounmask-backtrack=y` is not a universal default.
- `--with-bdeps` usually does not need to be emphasized for normal install actions; document it only when relevant to the user's confusion.

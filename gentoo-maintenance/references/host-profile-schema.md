# Host Profile Schema

The public skill defines the schema only. Keep the actual local profile out of the repository.

## Recommended Local Path

```text
/etc/portage/gm-host-profile.yaml
```

## Common Required Fields

```yaml
role: vps
prefer_binpkg_when_possible: true
prefer_tmp_candidates: true
require_manual_review_for_writes: true
```

These fields are the baseline for most tasks:

- `role`: default host role
- `prefer_binpkg_when_possible`: whether binpkg availability should influence strategy early
- `prefer_tmp_candidates`: whether staged candidates should be the default
- `require_manual_review_for_writes`: hard gate for non-`/tmp` writes

## Conditional Fields

Add these only when they materially affect decisions:

- `allow_non_core_feature_loss`: whether optional feature trimming is acceptable
- `optimize_for`: ordered goals such as `stability` or `low-maintenance`
- `high_risk_areas`: topics that should raise risk level
- `notes`: short host reminders

## Suggested Example

```yaml
role: vps
prefer_binpkg_when_possible: true
prefer_tmp_candidates: true
require_manual_review_for_writes: true
allow_non_core_feature_loss: true
optimize_for:
  - stability
  - low-maintenance
high_risk_areas:
  - kernel
  - boot
  - zfs
notes:
  - service-oriented host
```

## Guidance

- Keep this file small.
- Use it for machine strategy, not for mirroring `/etc/portage`.
- Do not store package-rule clutter here.
- If the task only needs a current-turn preference, do not persist it.

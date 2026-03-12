# Host Profile Schema

The public skill should define the schema only. Keep the actual local profile out of the repository.

## Recommended Local Path

```text
~/.config/locez-skills/gentoo-host-profile.yaml
```

## Suggested Fields

```yaml
role: desktop
optimize_for:
  - stability
  - convenience

allow_non_core_feature_loss: false
prefer_binpkg_when_possible: false
prefer_tmp_candidates: true
require_manual_review_for_writes: true

high_risk_areas:
  - kernel
  - boot
  - zfs
  - gpu-driver

topic_policies:
  steam_32bit_stack: keep
  desktop_stack: full-featured
  vps_feature_trimming: disallow

package_pins:
  - "=sys-kernel/example-kernel-6.12.0"

notes:
  - "Interactive host"
```

## Field Meanings

- `role`: the default host role
- `optimize_for`: ordered strategy goals
- `allow_non_core_feature_loss`: whether trimmed optional features are acceptable
- `prefer_binpkg_when_possible`: whether binpkg availability should influence decisions early
- `prefer_tmp_candidates`: whether staged candidates should be the default
- `require_manual_review_for_writes`: hard gate for non-`/tmp` writes
- `high_risk_areas`: topics that should raise risk level
- `topic_policies`: durable machine-level preferences
- `package_pins`: long-term version constraints
- `notes`: free-form reminders for local policy

## Guidance

- Keep this file small.
- Use it for strategy, not for mirroring `/etc/portage`.
- Prefer topic files or normal Portage files for package-level rules that must exist on the system.

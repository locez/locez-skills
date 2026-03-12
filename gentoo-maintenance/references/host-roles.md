# Host Roles

## Roles

Use one of these roles:

| Role | Meaning | Default bias |
|---|---|---|
| `desktop` | Interactive machine where feature completeness matters | preserve full functionality |
| `vps` | Service-oriented host where low maintenance and lower local build cost matter | prefer reliability and smaller change surface |
| `binpkg-builder` | Host mainly used to produce binary packages | prefer buildability and package output |
| `mixed` | Host with meaningful overlap between roles | require explicit tradeoff checks |

## Resolution Order

Choose role in this order:

1. Explicit current-turn user statement
2. `gm-agent-preferences.yaml` host override
3. `gm-host-profile.yaml`
4. Hostname mapping if one is introduced later
5. Heuristics from installed stack and current task
6. Ask if still materially ambiguous

Heuristics are only a fallback.

## Heuristic Hints

Desktop signals:

- full Plasma, GNOME, or similar desktop stack
- gaming, multimedia, or heavy GUI world set
- user cares about feature completeness

VPS signals:

- service packages dominate
- user wants less local compilation or a smaller package surface
- GUI and desktop integration are absent or optional

Binpkg builder signals:

- the main purpose is producing packages for other machines
- the user accepts trimmed non-core features to keep builds flowing
- dependency breadth matters more than local UX

Mixed signals:

- the machine is both a daily driver and a build source
- desktop and builder requirements conflict regularly

## When To Stop

Stop and ask when:

- explicit instruction conflicts with stored overrides
- `gm-host-profile.yaml` and `gm-agent-preferences.yaml` point in different directions
- heuristics point to two roles with materially different outcomes
- required role-sensitive fields are still missing

## Output Expectation

Every run should report:

- selected host role
- evidence quality: explicit, preference, profile, heuristic, or uncertain
- whether the role is temporary pending profile confirmation

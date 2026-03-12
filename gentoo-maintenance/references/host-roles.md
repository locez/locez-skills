# Host Roles

## Roles

Use one of these roles:

| Role | Meaning | Default bias |
|---|---|---|
| `desktop` | Interactive machine where user experience and feature completeness matter | preserve full functionality |
| `vps` | Service-oriented host where low maintenance and minimal local build cost matter | prefer reliability and smaller change surface |
| `binpkg-builder` | Host mainly used to produce binary packages | prefer buildability and package output |
| `mixed` | Host with meaningful overlap between roles | require explicit tradeoff checks |

## Resolution Order

Choose role in this order:

1. Explicit user statement
2. Local host profile file
3. Hostname mapping if available
4. Heuristics from installed stack and current task
5. Ask the user if still ambiguous

## Heuristic Hints

Heuristics are only a fallback.

Desktop signals:

- full Plasma, GNOME, or similar desktop stack
- gaming stack, multimedia stack, or heavy GUI world set
- user explicitly cares about feature completeness

VPS signals:

- service packages dominate
- user asks to avoid local compilation or reduce package surface
- GUI and desktop integration are optional or absent

Binpkg builder signals:

- focus is on producing packages for other machines
- user is willing to trim non-core features to keep builds flowing
- packaging and dependency breadth matters more than local UX

Mixed signals:

- the machine is both a daily driver and a build source
- desktop and builder requirements conflict regularly

## When To Stop

Stop and ask when:

- explicit user intent conflicts with the local profile
- heuristics point to two roles with materially different outcomes
- the task touches both desktop-critical and builder-critical policies

## Output Expectation

Every run should report:

- selected host role
- evidence quality: explicit, profile, heuristic, or uncertain

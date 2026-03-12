# Agent Preferences Schema

The public skill defines the schema only. Keep the actual local preferences out of the repository.

## Recommended Local Path

```text
/etc/portage/gm-agent-preferences.yaml
```

## What Belongs Here

Use this file for durable user instructions that should override the generic skill behavior on this host.

Examples:

- treat the host as `vps` even when heuristics look desktop-like
- preserve the user's current `/etc/portage` layout unless explicitly asked to normalize it
- ask before trading feature completeness for easier binpkg resolution
- prefer staged candidates before recommending direct system edits

## Suggested Structure

```yaml
prefer_question_when_profile_incomplete: true
allow_readonly_analysis_without_full_profile: true

host_overrides:
  treat_this_host_as: vps

workflow:
  prefer_staged_candidates: true
  avoid_recommending_autounmask_cleanup_by_default: true

rules_to_follow:
  - when: portage-hygiene
    rule: respect existing user layout unless explicitly asked to normalize it
    reason: durable user preference
  - when: binpkg-optimization
    rule: ask before trading feature completeness for easier binpkg resolution
    reason: durable user preference
```

## Field Guidance

- `prefer_question_when_profile_incomplete`: ask when a missing field changes the answer
- `allow_readonly_analysis_without_full_profile`: keep read-only investigation moving while final decisions stay temporary
- `host_overrides`: durable instruction that changes how the host should be treated
- `workflow`: stable presentation and review preferences
- `rules_to_follow`: reusable user instructions scoped by task or scenario

## Do Not Persist

Keep these current-turn-only unless the user clearly says they should be remembered:

- one-off emergency workarounds
- temporary frustration with a single package or solver result
- package-level rules that belong in normal Portage files
- guesses inferred only from heuristics

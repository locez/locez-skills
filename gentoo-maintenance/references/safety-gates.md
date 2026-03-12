# Safety Gates

The skill may inspect and stage, but it must not silently change system state.

## Always Allowed Without Review

- read-only inspection
- `emerge -p...` dry-runs
- generating candidates under `/tmp/gentoo-maintenance/`
- comparing current Portage files to staged candidates
- continuing read-only analysis while profile-sensitive conclusions remain temporary

## Actions That Require Review First

- editing `/etc/portage`
- writing `/etc/portage/gm-host-profile.yaml`
- writing `/etc/portage/gm-agent-preferences.yaml`
- running `emerge` without `-p`
- changing kernel, boot, ZFS, or GPU driver state
- changing repo config, overlays, package sets, or world files
- writing outside `/tmp` in response to the maintenance decision

## Mandatory Stop Conditions

Stop and ask when:

- host role is still ambiguous after available evidence
- a required profile field is still missing and changes the final recommendation
- two materially different placements both look valid
- deletion volume is high enough that rollback risk is non-trivial
- the request mixes large system upgrade work with config restructuring
- the action crosses into kernel, boot, ZFS, or GPU driver policy

## Automation Reduction Triggers

Become more conservative when:

- the user wants understanding before action
- multiple topic files would change at once
- heuristics conflict with explicit user preference
- stored agent preferences conflict with current-turn instructions
- the proposed write affects long-lived policy files
- final execution depends on still-missing profile data

## Review Message Requirements

Before any write, state:

- what will change
- why it counts as a write
- what files or system state it affects
- whether the change is overwrite, append, merge, install, or another write class
- whether missing profile data still blocks final application

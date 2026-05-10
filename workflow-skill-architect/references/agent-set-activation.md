# Agent Set Activation

Use this reference to decide whether workflow-skill-architect should stay as a single-agent analysis or activate a multi-agent review set.

## Default

Default to single-agent analysis. Most skill reviews should produce a concise architecture assessment without spawning workers, writing artifacts, or forcing a large workflow structure.

## Activate Agent Set When

Use an agent set only when at least one trigger is present:

- The user asks for actual refactoring or file changes.
- The skill has large scope: multiple domains, many references, long scripts, or more content than one agent can inspect reliably.
- The target is high-risk infrastructure, such as a system skill, security-sensitive workflow, package manager policy, production data pipeline, or live business process.
- The review has independent dimensions that can be assessed in parallel: resources, prompts, validation, concurrency, safety, metadata, and domain templates.
- The user asks for a deep audit, batch migration, or comparison across multiple skills.
- Prior analysis produced conflicting recommendations and needs an independent anti-overengineering pass.

Do not activate an agent set only because sub-agents are available.

## Anti-Overengineering Gate

Before activating, answer:

- Would the final answer improve materially over a single-agent review?
- Is there enough independent work to justify parallelism?
- Are there disjoint outputs or review dimensions?
- Would artifact protocols, agent contracts, or concurrency maps make the skill clearer rather than heavier?
- Is the target skill production-stable and only needs small protocol polish?

If the answer is mostly no, keep the review single-agent and explicitly recommend the smallest useful change.

## Standard Review Set

When activated, use only the roles needed:

### Smell Detector

Finds overloaded prompts, mixed responsibilities, repeated confirmations, missing validation, competing workflows, and hidden state changes.

### Resource Mapper

Maps existing `scripts/`, `references/`, `assets/`, `agents/openai.yaml`, and duplicated knowledge. Recommends what should move or stay.

### Agent Contract Designer

Defines worker roles only if the target workflow benefits from sub-agent boundaries.

### Concurrency Reviewer

Identifies safe parallel work, barriers, shared-write hazards, and merge owners.

### Validation Reviewer

Checks structural validation, behavioral validation, forward-testing, output quality gates, and residual risk.

### Anti-Overengineering Reviewer

Challenges the proposed architecture. Looks for unnecessary references, needless sub-agents, fake artifacts, premature generalization, and changes that make a stable skill harder to use.

## Merge Rules

The orchestrator merges worker outputs. Workers should not edit the target skill directly unless the user requested implementation and write scopes are disjoint.

Merge order:

1. Collect findings by review dimension.
2. Apply the anti-overengineering pass.
3. Classify recommendation level using `refactor-levels.md`.
4. Present only the highest-signal recommendations.

## Worker Prompt Pattern

```text
You are the <review role> for a workflow skill architecture review.

Target: <skill path or pasted skill>
Scope: read-only review unless explicitly assigned a write scope.
Focus: <one review dimension>
Output: concise findings with severity and concrete recommended change.
Forbidden: do not redesign the whole skill, do not edit files, do not assume other reviewers' findings.
```

## Output Shape

For read-only analysis:

```markdown
## Architecture Assessment

Change level:

Verdict:

Highest-value changes:

What not to change:

Agent set needed next time:
```

For implementation:

```markdown
## Refactor Plan

Change level:
Files:
Review gates:
Validation:
Anti-overengineering notes:
```

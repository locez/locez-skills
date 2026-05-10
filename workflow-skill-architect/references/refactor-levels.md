# Refactor Levels

Use a change level before recommending structure. The level prevents overengineering and makes the final recommendation easier to act on.

## Levels

### `no-op`

Use when the target skill is already clear, stable, and proportionate. Recommend no structural change.

### `small-polish`

Use for wording, reference-map clarity, metadata clarification, validation wording, or other small edits that do not change the workflow.

### `protocolize`

Use when the skill is basically sound but needs explicit protocols, such as validation, artifact ownership, concurrency, agent contracts, review gates, or manifest schemas.

### `split`

Use when `SKILL.md` is carrying too much detail and should move stable domain knowledge, templates, examples, or long procedures into references.

### `rebuild`

Use when the skill's main workflow is structurally wrong: mixed responsibilities, competing workflows, hidden state changes, repeated interruptions, missing outputs, or no validation path.

### `template-extract`

Use when the target contains a reusable domain or workflow pattern that should become a template for future generated skills.

## Selection Rules

- Prefer the smallest level that solves the real problem.
- Do not promote a stable production skill beyond `small-polish` or `protocolize` without strong evidence.
- `protocolize` is not permission to add every protocol. Add only the protocol that changes behavior.
- `rebuild` requires evidence that smaller changes would leave the skill fragile.
- `template-extract` should not be used for one-off domain knowledge.

## Output Requirement

Every architecture assessment should include:

```markdown
Change level: <level>
Reason: <one sentence>
Recommended action: <smallest useful change>
```

# Workflow Refactoring

Use this reference when converting an existing overloaded skill or task description into a structured workflow skill.

## Refactoring Pass

1. **Extract intent**: user goal, trigger phrases, accepted inputs, final outputs, and success criteria.
2. **Flatten the old flow**: list every action the current skill asks the model or user to perform.
3. **Classify each action**:
   - Orchestration
   - Domain analysis
   - Rule design
   - Deterministic execution
   - Validation
   - Human review
   - Final synthesis or query
4. **Move knowledge**:
   - Stable domain rules go to `references/`.
   - Repeated deterministic operations go to `scripts/`.
   - Workflow routing stays in `SKILL.md`.
5. **Demote legacy workflow files**: if the old skill has `execution-workflow.md`, `runbook.md`, or similar files, decide whether each becomes the new orchestration workflow or a lower-level command cookbook. Do not leave two competing workflow entry points.
6. **Define dependencies and concurrency**: mark stages as serial, parallelizable, or barrier. Independent workers should run concurrently when the platform allows it.
7. **Define artifacts**: each stage produces one named artifact consumed by a later stage.
8. **Batch uncertainty**: replace repeated confirmation questions with exception lists and review gates.
9. **Rebuild the skill**: create a short `SKILL.md`, focused references, optional scripts, and UI metadata.
10. **Validate**: structure check, trigger check, artifact check, concurrency check, and a realistic forward test.

## Orchestrator Responsibilities

The orchestrator should:

- Maintain the workflow state.
- Decide which reference files to load.
- Dispatch work to specialized agents when the platform allows it.
- Start independent workers concurrently when their inputs are ready and write sets do not overlap.
- Keep sub-agent prompts narrow and self-contained.
- Route artifacts between stages.
- Wait at explicit barrier stages before synthesis, execution, or validation.
- Stop for human review only at defined gates.
- Synthesize final output and residual risk.

The orchestrator should not:

- Perform detailed domain analysis itself.
- Rewrite large datasets or documents by freehand.
- Hide uncertainty.
- Ask one-off confirmation questions that should become rules.
- Serialize independent analysis work just because it is simpler to describe.

## Worker Responsibilities

Each worker should own one transformation. If a worker needs to both discover rules and execute them, split it. If two workers produce the same kind of judgment, merge them or define a priority rule.

Good worker scope:

- Profile input data and produce a report.
- Extract business rules from a legacy skill.
- Compile rules into a structured rulebook.
- Execute a deterministic transformation.
- Validate outputs against rules.
- Prepare an exception review packet.

Bad worker scope:

- "Clean the data."
- "Understand the business and fix everything."
- "Review the whole skill and improve it."

## Concurrency Design

Good workflow skills describe both order and parallelism. A pipeline is not automatically serial. Identify which work can begin from the same upstream artifact and which work must wait for a barrier.

Use `concurrency.md` for the target skill when:

- multiple source files or domains can be profiled independently;
- different worker agents can extract domain rules, existing artifacts, and script inventory in parallel;
- validators can check independent output surfaces at the same time;
- query/documentation generation can run after stable references exist while implementation details are still being checked.

Do not parallelize stages that write the same artifact, depend on unresolved business decisions, or need a deterministic global order.

## Artifact Design

Artifacts are the workflow's interface. Use them to avoid context soup.

Each artifact needs:

- Name and path.
- Owner stage.
- Required fields or sections.
- Consumer stage.
- Pass/fail criteria.
- Write owner and merge rule when concurrent workers feed a shared synthesis artifact.

Prefer machine-readable formats for execution-facing artifacts and Markdown for human-facing review:

- Use YAML or JSON for rules, plans, mappings, and validation criteria.
- Use CSV for row-level exception queues.
- Use Markdown for summaries, review packets, and final reports.

## Human Review Gates

Use review gates for decisions that are risky, irreversible, or dependent on business judgment. A review gate should include:

- Grouped decisions.
- Recommended defaults.
- Impact estimate.
- Rows, files, or entities affected.
- What happens if the user does not decide.
- How the decision is persisted into rules.

Avoid stopping the user for low-risk or reversible choices.

## Validation Checklist

Before calling the refactor complete:

- The main `SKILL.md` is short enough to act as an entry point.
- Every sub-agent has a contract.
- Every nontrivial stage has an artifact.
- Every artifact has a downstream consumer.
- Each stage is marked serial, parallelizable, or barrier.
- Parallel stages have disjoint write ownership or an explicit merge artifact.
- Legacy workflow/runbook files cannot compete with the new main workflow.
- Human confirmations are batched.
- Deterministic work is not left to model improvisation when a script or structured operation is practical.
- The final skill can explain what changed, what was skipped, and what still needs review.

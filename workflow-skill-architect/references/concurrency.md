# Concurrency

Use this reference when designing workflow skills that can run independent work in parallel. A good workflow defines order, barriers, and safe parallelism.

## Core Principle

Parallelize independent discovery, profiling, extraction, and validation. Serialize decisions, shared writes, irreversible execution, and final synthesis.

Do not use concurrency as a status symbol. For small read-only assessments, single-agent review is usually better unless independent dimensions are large enough to justify merge overhead.

## Stage Labels

Use these labels in `workflow.md`:

- `serial`: must run after a specific upstream stage and before downstream work.
- `parallelizable`: can run alongside named stages once inputs are ready.
- `barrier`: waits for multiple upstream artifacts before continuing.
- `merge`: combines outputs from parallel workers into one artifact.

## Concurrency Map Template

```markdown
## Concurrency Map

| Stage | Label | Inputs Ready When | May Run With | Writes | Barrier Before |
| --- | --- | --- | --- | --- | --- |
| Intake | serial | user request exists | none | intake-summary.md | profiling, domain analysis |
| Source profiling | parallelizable | files listed | domain analysis, script inventory | profile reports | rule design |
| Domain analysis | parallelizable | request and references available | source profiling | domain-model.md | rule design |
| Rule design | barrier | profile + domain model ready | none | rules.yaml | execution |
| Validation | parallelizable | outputs ready | report drafting | validation-report.md | final synthesis |
| Final synthesis | barrier | validation + exceptions ready | none | final-response.md | delivery |
```

## Safe To Parallelize

- Read-only analysis over different files, references, source categories, or output sheets.
- Workers with disjoint output artifacts.
- Independent validators whose results feed a merge stage.
- Documentation/query-guide generation after its required inputs are stable.

## Keep Serial

- User intake decisions that determine scope.
- Rule approval gates.
- Registry, database, or stateful memory updates.
- Destructive transforms, overwrites, deletes, merges, or imputations.
- Final report synthesis.

## Write Ownership

Every artifact must have one write owner. When multiple parallel workers contribute to a shared result, require a merge owner and an intermediate artifact per worker.

Bad:

- Three workers append directly to `rules.md`.

Good:

- `water-rules.md`, `pathogen-rules.md`, and `feeding-rules.md` are written independently.
- Rule Compiler merges them into `rules.yaml`.

## Sub-Agent Dispatch Guidance

When sub-agents are available, dispatch parallel workers only after defining:

- exact input artifacts;
- exact output path or response schema;
- forbidden writes;
- merge owner;
- barrier that waits for completion.

Do not dispatch a worker if the orchestrator immediately needs its result for the next step. Do that blocking work locally.

## Validation

Before accepting the workflow:

- Each parallel stage has disjoint write ownership.
- Each barrier lists the artifacts it waits for.
- Each merge stage has deterministic conflict handling.
- No worker needs hidden context from another worker's private reasoning.
- The final response reports unfinished parallel branches or failed worker outputs.
- The concurrency map does not make a simple stable skill harder to use.

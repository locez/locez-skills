# Agent Contracts

Use this reference when defining sub-agents for a workflow skill.

## Contract Template

```markdown
## <Agent Name>

**Purpose:** One sentence describing the transformation this agent owns.

**Use When:** Conditions that trigger this agent.

**Inputs:**
- `<artifact-or-user-input>`: required shape and path

**Outputs:**
- `<artifact-path>`: required sections or schema

**Concurrency:**
- Whether this agent can run in parallel, what it can run alongside, and which artifacts it must not write.

**Allowed Actions:**
- Actions this agent may perform.

**Forbidden Actions:**
- Actions reserved for other agents or the orchestrator.

**Quality Bar:**
- Concrete checks the output must satisfy.

**Escalation:**
- Conditions that require returning uncertainty instead of guessing.
```

## Prompt Pattern

When dispatching a worker, include only the local task, relevant artifacts, output contract, and forbidden actions. Do not pass the whole workflow unless the worker needs it.

```text
You are the <Agent Name> for this workflow.

Goal: <single transformation>
Inputs: <paths or pasted excerpts>
Output: write/return <artifact> following this schema
Concurrency: <parallelizable or serial; write ownership>
Forbidden: <things this agent must not do>
Escalate when: <uncertainty conditions>
```

## Common Agent Types

### Intake Analyst

Extracts the user's goal, inputs, outputs, constraints, and success criteria. Does not design the final workflow.

### Domain Analyst

Maps domain concepts, business entities, terms, and semantics. Does not execute transformations.

### Rule Designer

Turns domain requirements into explicit rules. Does not apply rules to production data or documents.

### Rule Compiler

Converts natural-language rules into structured artifacts such as YAML, JSON, schemas, or checklists. Does not invent business meaning.

### Executor

Applies approved rules. Prefers scripts or deterministic operations. Does not reinterpret rules.

### Validator

Checks output against rules, input/output deltas, invariants, and risk criteria. Does not fix issues directly unless the workflow explicitly allows a repair loop.

### Exception Triage

Groups ambiguous cases for human review. Does not ask one-off questions during discovery.

### Query Agent

Answers questions over approved outputs and reference material. Does not re-clean or reinterpret raw inputs.

## Boundary Tests

Use these tests when reviewing agent contracts:

- Can this agent be replaced without changing other agents?
- Can a downstream agent consume its output without reading its private reasoning?
- Does it have exactly one owner for each artifact it writes?
- Can it run concurrently without racing another worker for the same artifact?
- Are forbidden actions explicit enough to prevent scope creep?
- Does it return uncertainty instead of making hidden business decisions?

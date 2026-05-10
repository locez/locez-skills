# Data Cleaning Workflow Template

Use this template when generating or refactoring a data-cleaning skill for business users who understand the domain but do not want to manage pipeline architecture.

## Principle

Data cleaning is a stable pipeline with variable business rules. Keep the pipeline generic and make business semantics, rules, thresholds, output formats, and query language domain-specific references.

## Recommended Skill Structure

```text
data-cleaning-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── agent-contracts.md
│   ├── concurrency.md
│   ├── data-dictionary.md
│   ├── cleaning-rules.md
│   ├── validation-rules.md
│   ├── exception-policy.md
│   └── query-guide.md
└── scripts/
    ├── profile_data.py
    ├── clean_data.py
    └── validate_cleaning.py
```

Create scripts only when the environment and data formats make them useful. For one-off or unknown environments, specify the script contracts first and add scripts later.

## Pipeline

1. **Intake**: collect file paths, source systems, target users, downstream use, output format, and risk constraints.
2. **Profiling**: compute schema, row count, null rates, unique counts, duplicate candidates, value distributions, date spans, numeric ranges, and suspicious values.
3. **Semantic Mapping**: map columns to business concepts, entities, keys, status fields, money fields, dates, and relationships.
4. **Rule Design**: define type conversions, normalization, deduplication, missing-value handling, validation rules, exception policies, and non-editable fields.
5. **Cleaning Plan**: estimate affected rows and risks before changing data.
6. **Execution**: apply approved rules with deterministic code or tightly specified transformations.
7. **Validation**: compare before/after row counts, key uniqueness, totals, null rates, category distributions, and known invariants.
8. **Exception Review**: produce a batch review packet for ambiguous or high-risk records.
9. **Reporting**: produce cleaned data, audit report, unresolved exceptions, and rule changes.
10. **Query Support**: answer questions only against cleaned data, data dictionary, and query guide.

## Concurrency Pattern

Data cleaning should not be fully serial when source categories are independent.

Usually parallelizable:

- Profiling multiple input files or sheets.
- Normalizing independent source categories into separate CSVs.
- Extracting business semantics from field lists while profiling runs.
- Validating independent output sheets or metric groups.
- Preparing query guide and data dictionary after semantic mapping stabilizes.

Usually serial or barrier:

- Intake before dispatch.
- Registry refresh before final batch mapping.
- Cleaning plan approval before destructive or irreversible execution.
- Workbook build after required normalized data and registry are ready.
- Final synthesis after validation and exception triage.

Never parallelize two workers that write the same registry, rulebook, output workbook, or final report unless the workflow defines a merge owner.

## Sub-Agent Set

### Data Profiler

Produces `profile_report.json` or `profile_report.md`. Uses tools or scripts whenever possible. Does not infer business meaning beyond obvious type and distribution clues.

### Business Schema Analyst

Produces `data-dictionary.md` and `schema-map.yaml`. Identifies business meaning, key fields, entity relationships, and terms that need user confirmation.

### Cleaning Rule Designer

Produces `cleaning-rules.md` or `cleaning-rules.yaml`. Separates automatic rules, suggested rules, manual-review rules, and forbidden transformations.

### Cleaning Plan Agent

Produces `cleaning-plan.md`. Estimates impact and identifies review gates before execution.

### Cleaning Executor

Produces cleaned output and `execution-log.md`. Applies approved rules only. Does not invent new rules during execution.

### Validation Agent

Produces `validation-report.md`. Checks invariants and before/after deltas. Flags suspicious changes.

### Exception Triage Agent

Produces `exceptions.csv` and `exception-review.md`. Groups uncertain records and proposes batch decisions.

### Query Agent

Produces answers based on cleaned data, `data-dictionary.md`, and `query-guide.md`. Does not query raw dirty data unless explicitly asked for diagnostics.

## Business Review Gates

Use review gates at these points:

- After semantic mapping, when field meanings or keys are uncertain.
- Before execution, when cleaning rules can delete, merge, overwrite, or impute data.
- After validation, when totals, row counts, or key uniqueness changed unexpectedly.

Do not interrupt for every uncertain row. Batch ambiguous records into `exceptions.csv`.

## Cleaning Rule Categories

Use these categories in rule artifacts:

- `automatic`: safe, deterministic, reversible or low-risk.
- `suggested`: likely correct but requires review before first use.
- `manual_review`: cannot be resolved without business judgment.
- `report_only`: should be detected but not changed.
- `forbidden`: must not be changed by the workflow.

## Query Layer

The query layer should expose business-friendly semantics:

- approved field names and aliases
- metric definitions
- date and status interpretations
- known exclusions
- unresolved exception caveats

The query agent must cite the cleaned-data artifact and the relevant rule or dictionary entry when answering nontrivial questions.

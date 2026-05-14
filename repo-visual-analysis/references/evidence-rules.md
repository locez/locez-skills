# Evidence Rules

Use these rules to prevent repository analysis from becoming structured hallucination.

## Evidence Levels

Label important statements:

- **Observed**: Directly visible in a file, manifest, config, test, command output, or git metadata.
- **Derived**: Supported by multiple observed facts, such as an import edge plus a route registration.
- **Inferred**: Reasonable but incomplete; useful for navigation but not final truth.
- **Unsupported**: Not enough evidence. Keep as an open question, not a conclusion.

## Evidence Upgrade Ladder

Increase proof requirements as claim strength increases:

| Statement type | Minimum support |
| --- | --- |
| Navigation observation | Snapshot, tree, manifest, or search result |
| Candidate component | Directory/manifest evidence or repeated references |
| Key component responsibility | Reopen and inspect relevant source files |
| Diagram node | Evidence or explicit `candidate` label |
| Diagram edge | Import/config/call/runtime evidence or explicit `candidate` label |
| Opportunity | At least one observation or evidence-backed claim |
| Global claim | Reproducible search, command, or broad source inspection |

Do not use strong wording for weak evidence.

## Verify Before Reuse

Before reusing a prior summary for any final report, diagram, opportunity, or global statement:

1. Locate the source evidence or prior claim.
2. Reopen the original file or rerun the relevant search when practical.
3. Inspect any new file that references the same component, symbol, route, config, or data object.
4. Decide whether the earlier claim is confirmed, narrowed, expanded, contradicted, or still uncertain.
5. Update the report or artifact before relying on it.

This rule applies to final outputs and high-value conclusions. Ordinary navigation can use summaries, as long as the summary is not treated as proof.

## Claim Registry

Use a claim registry only when producing a Full Visual Report or when a Focused Map has important conclusions that will be reused.

Keep it small. Record claims that affect:

- Final architecture diagrams.
- Cross-component relationships.
- Critical runtime or data-flow paths.
- Hotspot or risk judgments.
- Opportunity recommendations.

Suggested JSONL shape:

```json
{
  "id": "claim-api-001",
  "level": "Derived",
  "claim": "接口层解析请求并委托 service 层处理主要业务逻辑。",
  "scope": "src/api and src/services",
  "evidence": [
    {"file": "src/api/routes.py", "lines": "20-76"},
    {"file": "src/services/user_service.py", "lines": "8-64"}
  ],
  "confidence": "medium",
  "status": "verified",
  "limits": "admin routes not checked"
}
```

Do not claim precision that was not verified. If line numbers are unavailable, cite file paths and symbol names.

## Dangerous Words

Avoid these unless strongly verified:

- all
- only
- always
- never
- entire
- the core
- no tests
- unused
- dead code

Prefer:

- "in the inspected paths"
- "the primary observed path"
- "candidate"
- "likely"
- "not found by the searches run"
- "needs verification"

## Contradictions

If new evidence contradicts a prior claim, do not patch around it. Surface the contradiction:

```md
Conflict: Earlier scan suggested all writes go through `StorageService`, but `src/jobs/export.py` writes files directly.
Impact: The data-flow diagram should show a secondary write path or mark storage ownership as inconsistent.
Next verification: Search for other direct file writes.
```

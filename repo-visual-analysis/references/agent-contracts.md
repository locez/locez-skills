# Agent Contracts

Use these contracts only when subagents/workers are available and the repository is large enough to justify parallel Focused Maps. Single-agent analysis remains the default.

## Focused Map Worker

**Purpose:** Verify one component, path, or theme from the focus queue.

**Use When:** Quick Scan has produced multiple independent focus items and parallel review would materially reduce time without shared-write risk.

**Inputs:**
- Quick Scan or focus queue excerpt.
- Snapshot path or relevant inventory excerpt.
- Assigned focus id and scope.
- Any explicit paths that are in scope.

**Outputs:**
- `module-cards/<focus-id>.md` following the Module Card schema in [artifact-protocols.md](artifact-protocols.md).
- `visual-models/<focus-id>.yaml` when a diagram is produced.

**Concurrency:**
- May run alongside other Focused Map Workers with disjoint focus ids and write paths.
- Must not write shared report, claim, or quick-scan artifacts.

**Allowed Actions:**
- Read assigned files and nearby dependencies.
- Run read-only searches and inspection commands.
- Create local visual model and local Mermaid diagram.
- Mark uncertainty and open questions.

**Forbidden Actions:**
- Do not edit `report.md`, `claims.jsonl`, `quick-scan.md`, or another worker's artifacts.
- Do not make repository-wide claims unless explicitly assigned to verify them.
- Do not implement code changes.
- Do not smooth over contradictions with Quick Scan or other Focused Maps.

**Quality Bar:**
- List files and searches inspected.
- Cite evidence for responsibilities, diagram edges, risks, and opportunities.
- Preserve uncertainty instead of filling gaps.
- Return focused output that the Integration Pass can consume without reading private reasoning.

**Escalation:**
- Return `needs integration review` when a finding depends on another component, crosses scope boundaries, or contradicts Quick Scan.

## Integration Owner

**Purpose:** Merge Quick Scan and Focused Maps into a Full Visual Report.

**Use When:** The user requests a Full Visual Report or enough Focused Maps exist to justify integration.

**Inputs:**
- `quick-scan.md` or Quick Scan answer.
- Selected `module-cards/*.md`.
- Selected `visual-models/*.yaml`.
- Optional `snapshot.json`.

**Outputs:**
- `report.md` when persistence matters.
- `claims.jsonl` when report-level claims will be reused.

**Concurrency:**
- Serial merge stage. It must not run concurrently with workers still writing selected artifacts.

**Allowed Actions:**
- Reconcile names, boundaries, and edges.
- Reopen evidence for final diagrams and global claims.
- Surface conflicts and confidence gaps.

**Forbidden Actions:**
- Do not invent missing component relationships to make the report look complete.
- Do not silently upgrade candidate worker findings into verified report facts.

**Quality Bar:**
- Names all input Focused Maps.
- Marks candidate and conflicted relationships clearly.
- Ties opportunities to evidence or Focused Map observations.

# Concurrency

Default to single-agent analysis. Parallelism is optional and only helps when multiple Focused Maps are independent enough to inspect separately and merge later.

## Activation

Use parallel Focused Maps only when:

- Quick Scan has produced a focus queue.
- At least two focus items have mostly disjoint file scopes or concerns.
- The repository is large enough that parallel review saves meaningful time.
- Each worker can produce its own module card and visual model.
- A single Integration Pass will merge outputs.

Do not parallelize Quick Scan, final report synthesis, shared claim registry updates, or Mermaid/report finalization.

## Stage Map

| Stage | Label | Inputs Ready When | May Run With | Writes | Barrier Before |
| --- | --- | --- | --- | --- | --- |
| Intake | serial | User request exists | none | none or intake note | Snapshot |
| Snapshot | serial | Repo path known | none | `snapshot.json` if persistent | Quick Scan |
| Quick Scan | serial | Snapshot/inventory ready | none | `quick-scan.md` if persistent | Focused Maps |
| Focused Map | parallelizable | Focus queue exists | Other Focused Maps with disjoint scopes | `module-cards/<id>.md`, `visual-models/<id>.yaml` | Integration |
| Integration Pass | barrier/merge | Selected Focused Maps ready | none | `claims.jsonl`, `report.md` | Delivery |
| HTML Render | serial | Markdown report artifacts ready | none | `index.html` | Delivery |
| Validation | serial or parallelizable | Output draft exists | Independent diagram/artifact checks | validation notes or final edits | Delivery |

## Integration Owner

The Integration Pass is the only owner of:

- Cross-component architecture.
- Final report-level diagrams.
- `claims.jsonl`.
- Conflict resolution and confidence/gaps.

When worker outputs disagree, keep both claims visible until evidence resolves the conflict.

For worker/subagent contracts, read [agent-contracts.md](agent-contracts.md).

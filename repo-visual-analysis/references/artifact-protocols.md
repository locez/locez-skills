# Artifact Protocols

Use artifacts only when they improve downstream behavior: repeated analysis, multi-step Focused Maps, Full Visual Report integration, or handoff to another design/planning workflow. For small read-only answers, the final response can be the artifact.

## Naming

Use stable paths for the latest analysis:

```text
.repo-visual-analysis/snapshot.json
.repo-visual-analysis/quick-scan.md
.repo-visual-analysis/report.md
.repo-visual-analysis/index.html
```

Use timestamped snapshots only for history, comparison, or avoiding overwrite:

```text
.repo-visual-analysis/snapshots/snapshot-YYYYMMDDTHHMMSSZ.json
```

Do not use `/tmp` paths as conventions.

## Write Ownership

Every artifact has one write owner:

| Artifact | Owner | Purpose |
| --- | --- | --- |
| `snapshot.json` | Snapshot stage | Route analysis and record inventory facts |
| `quick-scan.md` | Quick Scan stage | Provide overview diagrams and focus queue |
| `module-cards/<focus-id>.md` | One Focused Map | Capture verified local understanding |
| `visual-models/<focus-id>.yaml` | Same Focused Map | Source model for local Mermaid diagrams |
| `claims.jsonl` | Integration Pass | Store only report-level reusable claims |
| `report.md` | Integration Pass | Deliver Full Visual Report |
| `index.html` | HTML Render stage | Present Quick Scan, Focused Maps, and Full Report with rendered Mermaid |

Parallel Focused Maps must not append to shared files. The Integration Pass merges their outputs.

The HTML Render stage must not rewrite source artifacts. It reads Markdown and produces only presentation HTML.

## Quick Scan Artifact

`quick-scan.md` should include:

- Snapshot summary.
- 1-2 candidate diagrams.
- Component candidates table.
- Focus queue.
- Open questions and confidence notes.

Do not include a claim registry. Quick Scan candidates are not final facts.

## Module Card Schema

Use this shape for persistent Focused Map cards:

```md
# Focused Map: <focus-id>

## Scope
- Goal:
- Included paths:
- Excluded paths:

## Evidence Read
- Files:
- Searches/commands:

## Local Map
- Visual model: `../visual-models/<focus-id>.yaml`
- Mermaid:

## Verified Responsibilities
| Responsibility | Evidence | Confidence |
| --- | --- | --- |

## Boundaries
- Owns:
- Depends on:
- Exposes:
- Unverified:

## Risks And Opportunities
| Item | Evidence | Impact | Next verification |
| --- | --- | --- | --- |

## Open Questions
- ...
```

## Visual Model Schema

Use YAML as the editable source for important diagrams:

```yaml
diagram:
  id: "<focus-id>-architecture"
  title: "组件架构图"
  level: "L1 Architecture"
  status: "candidate|verified|mixed"
nodes:
  - id: "api"
    label: "接口层"
    kind: "component"
    status: "observed|derived|candidate"
    evidence:
      - file: "src/api/routes.py"
        lines: "20-76"
edges:
  - from: "api"
    to: "service"
    label: "调用"
    status: "derived|candidate"
    evidence:
      - file: "src/api/routes.py"
        lines: "42-51"
notes:
  - "admin routes not inspected"
```

If a node or edge has no evidence, mark it `candidate` or remove it.

## Claim Registry

Use `claims.jsonl` only for Full Visual Report or reusable high-value Focused Map conclusions. Keep it small and report-level.

Each claim should include:

```json
{
  "id": "claim-001",
  "level": "Observed|Derived|Inferred",
  "claim": "short claim text",
  "scope": "paths or subsystem covered",
  "evidence": [{"file": "path", "lines": "optional"}],
  "confidence": "low|medium|high",
  "status": "verified|candidate|conflicted",
  "limits": "what was not checked"
}
```

Do not create claim ids for routine observations that will not be reused.

## HTML Visual Report

Use `.repo-visual-analysis/index.html` as the stable browser-openable report. Generate it with:

```bash
/path/to/repo-visual-analysis/scripts/render_report_html.py --analysis-dir .repo-visual-analysis --language <zh|en|auto>
```

The bundled scripts prefer `python3` and fall back to `python` when executed directly. If executable permissions are unavailable, run the same script with `python3` or `python`.

Default input discovery:

```text
.repo-visual-analysis/quick-scan.md
.repo-visual-analysis/module-cards/*.md
.repo-visual-analysis/report.md
```

Use explicit inputs only when assembling a custom report:

```bash
/path/to/repo-visual-analysis/scripts/render_report_html.py \
  --input .repo-visual-analysis/quick-scan.md \
  --input .repo-visual-analysis/module-cards/api.md \
  --language zh \
  --out .repo-visual-analysis/index.html
```

The HTML report is a rendered view, not the evidence source. If HTML and Markdown disagree, fix the source Markdown or visual model and regenerate HTML.

When delivering the report to the user, provide the absolute full path printed by `render_report_html.py`, not the relative `.repo-visual-analysis/index.html` path. If the script output was not captured, resolve it before the final response:

```bash
realpath .repo-visual-analysis/index.html
```

Delivery rule: the final user-facing HTML report line must contain the resolved absolute `index.html` path. Do not make `.repo-visual-analysis/index.html` the primary link or only link.

## Layer Map Blocks

The HTML renderer supports `rva-layer-map` fenced blocks for broad layered capability architecture maps:

````md
```rva-layer-map
{
  "title": "分层架构图",
  "status": "candidate",
  "layers": [
    {"id": "layer_app", "label": "应用层", "items": ["管理后台", "API", "CLI"]},
    {"id": "layer_service", "label": "服务层", "items": ["编排服务", "检索服务"]},
    {"id": "layer_storage", "label": "存储层", "items": ["数据库", "对象存储"]}
  ]
}
```
````

Use this instead of Mermaid when the intended output is a compact human-facing layered architecture canvas.

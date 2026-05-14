# Workflow

Use this workflow to keep repository analysis useful under context limits. Prefer small verified maps over one large confident report.

## 1. Intake

Identify the user's actual goal:

- Understand an unfamiliar repository.
- Generate architecture or flow diagrams.
- Find improvement opportunities.
- Analyze one component, feature, risk, or execution path.
- Build a full visual report for human or LLM handoff.

If the user did not specify a goal, default to Quick Scan.

Stage label: `serial`.

Output when persistence matters: an implicit or written intake note with goal, mode, target path, requested depth, output expectation, and report language. Do not ask repeated clarification questions; choose conservative defaults and surface assumptions in the report.

Set report language from the user's current interaction language. Read [language-policy.md](language-policy.md) when the language is unclear or when rendering HTML.

## 2. Snapshot

Create a lightweight repository inventory before reading deeply. Prefer `scripts/repo_snapshot.py` if available:

```bash
/path/to/repo-visual-analysis/scripts/repo_snapshot.py --repo . --out .repo-visual-analysis/snapshot.json
```

The bundled scripts prefer `python3` and fall back to `python` when executed directly. If executable permissions are unavailable, run the same script with `python3` or `python`.

Use stable artifact names by default so later steps can find and refresh the latest analysis:

```text
.repo-visual-analysis/snapshot.json
.repo-visual-analysis/quick-scan.md
.repo-visual-analysis/report.md
.repo-visual-analysis/index.html
```

Use timestamped artifacts only when preserving history, comparing runs, or avoiding overwrite matters:

```bash
/path/to/repo-visual-analysis/scripts/repo_snapshot.py --repo . --out-dir .repo-visual-analysis/snapshots --timestamped
```

Do not use `/tmp` paths as skill conventions. Temporary files are acceptable for one-off validation only.

The snapshot should capture:

- Git head and status summary when available.
- Top-level directories and important manifests.
- Language/file extension distribution.
- Scripts, test configuration, CI files, docs, and likely entry files.
- Largest files and high-level file counts.

Do not treat the snapshot as final understanding. It is a routing layer.

Stage label: `serial`.

Output when persistence matters: `.repo-visual-analysis/snapshot.json`.

## 3. Quick Scan

Quick Scan is the default and the most important mode. It creates the navigation map for all later work.

Produce:

- Repository identity: likely project type, languages, package/build/test tools.
- Entry candidates: CLI, app server, UI entry, worker, library exports, scripts.
- Component candidates: 5-9 top-level conceptual components.
- 1-2 diagrams:
  - Layered Architecture Sketch when recognizable layers exist; otherwise Repo Architecture Sketch.
  - Primary Flow Sketch, only when a likely main flow is visible.
- Focus queue: the next components or paths worth analyzing.
- Open questions and confidence labels.

Use wording such as `candidate`, `likely`, `observed`, and `needs verification`. Do not claim complete architecture truth.

Quick Scan should not:

- Build a full claim registry.
- Draw every directory or file.
- Assert "only", "all", "always", or "the core" without verification.
- Produce more than two diagrams unless the user explicitly asks.

Stage label: `serial`.

Output: final answer or `.repo-visual-analysis/quick-scan.md`. If later Focused Maps will be run, Quick Scan owns the focus queue.

## 4. Focused Map

Focused Map verifies one component, path, or theme. Use it after Quick Scan or when the user names a target.

Examples:

- "Focus on the plugin system."
- "Map the request flow."
- "Analyze testing risk."
- "Explain how data moves from ingestion to output."

Produce:

- Scope and reason this focus was selected.
- Files read and searches run.
- Verified responsibilities and entry points.
- Local architecture, runtime, or data-flow diagram.
- Boundary notes: what this component owns, depends on, and exposes.
- Risks, hotspots, and Evidence-Backed Opportunities.
- Open questions and what would verify them.

Focused Map is where candidate components become confirmed, narrowed, or rejected.

Stage label: `parallelizable` after Quick Scan, when multiple selected components or flows are independent.

Output when persistence matters:

```text
.repo-visual-analysis/module-cards/<focus-id>.md
.repo-visual-analysis/visual-models/<focus-id>.yaml
```

Each Focused Map owns only its own module card and visual model. It must not edit `report.md`, `claims.jsonl`, or other Focused Map artifacts.

## 5. Full Visual Report

Full Visual Report is an Integration Pass over multiple Focused Maps. Do not generate it by reading many files once and summarizing from memory.

Produce:

- Executive repo map.
- System context map.
- Architecture map.
- Critical runtime flow.
- Data flow map when data movement matters.
- Hotspot map or hotspot table.
- Evidence-Backed Opportunities matrix.
- Confidence and gaps section.

During integration:

- Reconcile component names and boundaries across Focused Maps.
- Check cross-component edges before drawing them as confirmed.
- Mark unresolved conflicts instead of smoothing them over.
- Reopen evidence for final diagrams, global claims, and opportunities.

Stage label: `barrier` and `merge`.

Inputs: Quick Scan plus selected Focused Maps. Output: `.repo-visual-analysis/report.md` when persistence matters. Integration owns final cross-component claims and report-level diagrams.

## 6. HTML Render

When the user requests a clickable visual report or when persistent report artifacts are written, render the Markdown artifacts into a browser-openable HTML report:

```bash
/path/to/repo-visual-analysis/scripts/render_report_html.py --analysis-dir .repo-visual-analysis --language <zh|en|auto>
```

The default output is `.repo-visual-analysis/index.html`. It should include, when present:

- `quick-scan.md`
- `module-cards/*.md`
- `report.md`

Stage label: `serial`.

Inputs: existing Markdown report artifacts. Output: `.repo-visual-analysis/index.html`. HTML render owns only the presentation artifact. It must not rewrite evidence, claims, module cards, or visual models.

Before delivery, capture the absolute path printed by `render_report_html.py`. If the output was not captured, resolve the default output with:

```bash
realpath .repo-visual-analysis/index.html
```

The final response must use the absolute `index.html` path as the primary browser-openable report link. Do not leave the user with only `.repo-visual-analysis/index.html`.

## 7. Artifact Strategy

Keep artifacts proportional to the mode.

Quick Scan may produce only the final answer. If persistence is useful, write:

```text
.repo-visual-analysis/
  snapshot.json
  quick-scan.md
```

Focused Map may write:

```text
.repo-visual-analysis/
  module-cards/<component>.md
  visual-models/<component>.yaml
```

Full Visual Report may write:

```text
.repo-visual-analysis/
  snapshot.json
  module-cards/*.md
  visual-models/*.yaml
  claims.jsonl
  report.md
  index.html
```

Do not create heavy artifacts unless they change downstream behavior.

## 8. Parallelism

This skill must work with a single agent. If subagents are available and the repository is large, use them only for independent Focused Maps with disjoint read scopes. Merge their outputs through the Integration Pass. Do not let parallel workers write the same artifact.

For detailed parallel execution rules, read [concurrency.md](concurrency.md). For persistent output shapes, read [artifact-protocols.md](artifact-protocols.md). For delivery checks, read [validation.md](validation.md).

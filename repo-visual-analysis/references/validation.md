# Validation

Use these gates before delivering reports or writing reusable artifacts. Validation should catch unsupported certainty, sprawling diagrams, and stale summaries.

## Quick Scan Gate

Before delivering Quick Scan:

- Snapshot or equivalent inventory was created.
- Project type, tools, tests, docs, and entry candidates are labeled as observed or candidate.
- A Layered Architecture Sketch is included when recognizable layers exist.
- Broad layered capability maps use `rva-layer-map` when HTML output is available, rather than forcing Mermaid auto-layout.
- Mermaid node, edge, and `subgraph` labels follow the report language; ids remain ASCII.
- 1-2 diagrams are included unless the repository has too little structure to justify them.
- Diagrams are explicitly marked candidate when based on top-level structure.
- Focus queue lists why each item matters and the next verification step.
- No global claim uses "all", "only", "always", "never", or "the core" without proof.
- Report language follows the user's current interaction language unless the user requested another language.

## Focused Map Gate

Before delivering a Focused Map:

- Scope is explicit: included and excluded paths are named.
- Files read and searches/commands run are listed.
- At least one local diagram is included when it improves understanding.
- Responsibilities and boundaries cite evidence or are marked unverified.
- Risks/opportunities cite evidence and include next verification.
- New findings are checked against relevant Quick Scan candidates.

## Full Visual Report Gate

Before delivering a Full Visual Report:

- Inputs are named: Quick Scan and Focused Maps used.
- Component names and boundaries are reconciled.
- Cross-component edges are verified or marked candidate.
- Conflicts are surfaced in `Confidence And Gaps`.
- Report-level diagrams are based on visual models or clearly described evidence.
- Evidence-Backed Opportunities are tied to observations, claims, or Focused Maps.

## HTML Report Gate

Before delivering an HTML visual report:

- `.repo-visual-analysis/index.html` exists or the chosen `--out` path exists.
- The generated HTML path has been captured from `render_report_html.py` output or resolved with `realpath`.
- The final response includes the generated HTML path as an absolute full path.
- The final response does not present `.repo-visual-analysis/index.html` as the primary report link or only report link.
- The HTML includes Quick Scan, Focused Map, and Full Visual Report sections when their source Markdown files exist.
- Mermaid code fences become renderable Mermaid blocks in the HTML.
- The page can still show Mermaid source if the CDN renderer fails.
- HTML is treated as a presentation artifact; source Markdown and visual models remain authoritative.

## Diagram Gate

Every Mermaid diagram must pass:

- One question per diagram.
- 5-9 nodes preferred; 12 node hard limit unless justified.
- ASCII ids and quoted Chinese labels when using Chinese text.
- Node ids, subgraph ids, class ids, and edge ids do not use Mermaid keywords or unsafe ids such as `graph`, `flowchart`, `subgraph`, `end`, `class`, `default`, `node`, or direction tokens.
- Nodes and edges have evidence, or the diagram/element is marked candidate.
- No mixed abstraction levels unless explicitly described as a sketch.
- If `architecture-beta` fails in the target renderer, convert the same visual model to `flowchart`.

## Reuse Gate

Before reusing prior summaries in final outputs:

- Reopen evidence or rerun searches for final claims, diagrams, global statements, and opportunities.
- If evidence was not reopened, phrase the result as candidate or needs verification.
- If new evidence contradicts prior summary, update the report and expose the conflict.

## Tool Validation

When modifying this skill:

- Run the platform skill validator.
- Run `repo_snapshot.py` in stable output mode.
- Run `repo_snapshot.py` in timestamped output mode when that path changed.
- Run `render_report_html.py` against a sample analysis directory containing at least one Mermaid diagram.

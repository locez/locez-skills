---
name: repo-visual-analysis
description: "Evidence-backed visual repository analysis for understanding codebases, creating concise Mermaid architecture/flow diagrams, mapping components and runtime/data paths, identifying hotspots, and producing repository-informed improvement opportunities. Use when the user asks to analyze a repository, understand a codebase, generate architecture diagrams, create a visual repo report, find high-value improvement directions, or prepare context for later design/planning work."
---

# Repo Visual Analysis

Create concise, evidence-backed visual maps of a repository. The goal is not to read every file or produce confident-sounding summaries; it is to build a useful navigation map, verify important claims, and preserve uncertainty where evidence is weak.

## Operating Principle

Never convert uncertainty into structure. If evidence is weak, label the result as a candidate, likely path, or open question instead of hiding it behind a diagram, claim id, or confident wording.

Summaries are navigation aids, not evidence. Final judgments, diagram nodes/edges, global claims, and improvement opportunities must trace back to source files, configuration, tests, commands, or reproducible searches.

## Mode Selection

Choose the smallest mode that satisfies the user request:

- **Quick Scan**: Default. Use for first-pass repository understanding, onboarding, or "look at this repo and tell me what matters." Produces 1-2 concise diagrams, component candidates, and a focus queue.
- **Focused Map**: Use when the user names a subsystem, component, feature, flow, risk, or goal. Verifies one slice deeply and produces a local architecture/flow map with evidence.
- **Full Visual Report**: Use only when the user explicitly asks for a full report, visual report, architecture report, opportunity analysis, or enough Focused Maps have been completed to integrate. Build it by composing Focused Maps, not by one-shot summarization.

If the request is broad and the repository is large, start with Quick Scan and offer the focus queue instead of attempting a full report immediately.

## Workflow

Read [references/workflow.md](references/workflow.md) for the full procedure.

Core flow:

1. Run or manually create a lightweight repository snapshot.
2. Produce a Quick Scan with 1-2 candidate diagrams and a focus queue.
3. For each selected component or theme, run a Focused Map.
4. If requested, run an Integration Pass to combine Focused Maps into a Full Visual Report.
5. Generate Evidence-Backed Opportunities from verified observations, not free-form inspiration.

Use `scripts/repo_snapshot.py` when a deterministic first-pass inventory is useful.

## Artifact Protocol

Read [references/artifact-protocols.md](references/artifact-protocols.md) before writing persistent analysis files.

Minimum rules:

- Do not write artifacts for every run. Quick Scan can be a final answer unless persistence helps downstream work.
- Use stable names for latest artifacts and timestamped names only for history or comparison.
- Every persistent artifact must have one owner and one downstream purpose.
- Full Visual Report artifacts are composed from Focused Maps; they are not a separate one-shot summary.

## HTML Visual Report

When the user asks for a visual report, clickable report, rendered Mermaid, or an artifact they can open in a browser, generate `.repo-visual-analysis/index.html` with `scripts/render_report_html.py`.

Minimum rules:

- Include Quick Scan, Focused Maps, and Full Visual Report sections when their Markdown artifacts exist.
- Render Mermaid diagrams in the browser; keep the Mermaid source visible if rendering fails.
- Treat HTML as a presentation artifact. The evidence-backed Markdown, module cards, and visual models remain the source artifacts.
- Do not start a web server unless the user asks; the generated HTML is designed to open directly in a browser.
- Capture or resolve the final `index.html` path after rendering. `render_report_html.py` prints the resolved absolute path; if that output is unavailable, run `realpath .repo-visual-analysis/index.html` or `pwd` plus the relative path.
- In the final response, give the generated HTML path as an absolute full path. Do not present `.repo-visual-analysis/index.html` as the primary report link; relative paths may appear only as secondary source-artifact context.

## Evidence Discipline

Read [references/evidence-rules.md](references/evidence-rules.md) before making final claims, diagrams, or opportunity recommendations.

Minimum rules:

- Use `Observed`, `Derived`, `Inferred`, and `Unsupported` labels.
- Use summaries to navigate; reopen evidence before using a claim in a final report, diagram, opportunity, or global statement.
- Require stronger proof for stronger wording. Avoid "all", "only", "always", "never", and "the core" unless backed by reproducible searches or direct verification.
- Record only high-value claims. Do not build a heavy claim registry for every minor observation.

## Diagram Discipline

Read [references/diagram-rules.md](references/diagram-rules.md) before producing Mermaid diagrams.

Minimum rules:

- Quick Scan should include 1-2 diagrams: preferably a Layered Architecture Sketch plus a Primary Flow Sketch when a likely flow is discoverable.
- For layered capability maps like application/service/governance/storage/resource layers, prefer `rva-layer-map` rendered by the HTML report instead of Mermaid.
- Use ASCII ids and quoted Chinese labels, for example `api["接口层"]`.
- Do not use Mermaid keywords or unsafe ids as node ids. Use prefixed ids like `svc_graph`, `data_store`, `layer_app` instead.
- Pick diagram syntax by concept. `architecture-beta` is allowed when it best expresses component topology, even though Mermaid may evolve.
- Keep diagrams tight: one diagram answers one question, usually 5-9 nodes, hard limit 12 nodes unless justified.
- Build important diagrams from a small visual model first; Mermaid is the rendered view, not the source of truth.

## Language Policy

Read [references/language-policy.md](references/language-policy.md) before writing reports or rendering HTML.

Default to the user's current interaction language for report headings, labels, diagram text, status text, and HTML chrome. Do not default to English unless the user is interacting in English or explicitly asks for English.

## Validation Gates

Read [references/validation.md](references/validation.md) before delivering a report or writing reusable artifacts.

Minimum gates:

- Quick Scan must separate observed facts from candidates and include a focus queue.
- Focused Map must list inspected files/searches and mark unverified boundaries.
- Full Visual Report must reconcile Focused Maps and surface conflicts instead of smoothing them over.
- Diagrams must pass the compactness gate and cite evidence or carry candidate status.

## Optional Parallelism

Read [references/concurrency.md](references/concurrency.md) only for large repositories or multiple independent Focused Maps.

Default to single-agent analysis. Use parallel workers only when they own disjoint Focused Map outputs and a single merge owner performs the Integration Pass. If workers/subagents are used, read [references/agent-contracts.md](references/agent-contracts.md).

## Report Templates

Use [references/report-template.md](references/report-template.md) for Quick Scan, Focused Map, and Full Visual Report sections.

Every report should make its confidence level visible. A useful report can say "this is probably the main path, but these files need verification."

## Optional Handoff

This skill must not depend on external brainstorming, design, or planning skills. It should work on its own.

If the user wants to develop one Evidence-Backed Opportunity into a concrete design and a brainstorming/design skill is available, use [references/handoff.md](references/handoff.md) to pass only the relevant repository summary, diagrams, evidence, risks, and open questions. If no such skill exists, continue with a lightweight manual design discussion.

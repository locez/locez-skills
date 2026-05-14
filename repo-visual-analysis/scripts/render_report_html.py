#!/bin/sh
"exec" "$(command -v python3 || command -v python)" "$0" "$@"

from __future__ import annotations

__doc__ = "Render repo-visual-analysis Markdown artifacts into a browser-openable HTML report."

import argparse
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path


MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"

MERMAID_UNSAFE_IDS = {
    "graph",
    "flowchart",
    "subgraph",
    "end",
    "class",
    "classDef",
    "click",
    "style",
    "linkStyle",
    "default",
    "interpolate",
    "direction",
    "TB",
    "TD",
    "BT",
    "LR",
    "RL",
    "node",
    "edge",
}


@dataclass
class Document:
    path: Path
    title: str
    kind: str
    html: str


LABELS = {
    "en": {
        "title": "Repository Visual Analysis",
        "tagline": "Rendered repository analysis with Mermaid diagrams.",
        "source_artifacts": "source artifact(s)",
        "loading": "Loading Mermaid renderer...",
        "rendered": "Mermaid diagrams rendered",
        "failed": "Mermaid renderer unavailable; diagram source is still visible",
        "nav_label": "Report sections",
        "quick_scan": "Quick Scan",
        "focused_map": "Focused Map",
        "full_report": "Full Report",
        "custom": "Custom",
        "warnings": "Diagram warnings",
    },
    "zh": {
        "title": "仓库可视化分析报告",
        "tagline": "包含 Mermaid 架构图与流程图的仓库分析报告。",
        "source_artifacts": "个来源文档",
        "loading": "正在加载 Mermaid 渲染器...",
        "rendered": "Mermaid 图已渲染",
        "failed": "Mermaid 渲染器不可用；图源码仍可阅读",
        "nav_label": "报告章节",
        "quick_scan": "快速扫描",
        "focused_map": "聚焦分析",
        "full_report": "完整报告",
        "custom": "自定义",
        "warnings": "图表警告",
    },
}


def slugify(text: str, fallback: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", text.strip().lower()).strip("-")
    return slug or fallback


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def inline_markdown(text: str) -> str:
    parts = text.split("`")
    rendered: list[str] = []
    for index, part in enumerate(parts):
        if index % 2:
            rendered.append(f"<code>{html.escape(part)}</code>")
        else:
            escaped = html.escape(part)
            escaped = re.sub(
                r"\[([^\]]+)\]\(([^)]+)\)",
                lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
                escaped,
            )
            rendered.append(escaped)
    return "".join(rendered)


def render_layer_map(raw: str) -> str:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return (
            '<pre class="code-block layer-map-error"><code>'
            + html.escape(f"Invalid rva-layer-map JSON: {exc}\n\n{raw}")
            + "</code></pre>"
        )

    title = str(data.get("title", "Layered Architecture Map"))
    status = str(data.get("status", "candidate"))
    layers = data.get("layers", [])
    if not isinstance(layers, list):
        layers = []

    out = [
        '<figure class="layer-map">',
        f"<figcaption>{html.escape(title)} <span>{html.escape(status)}</span></figcaption>",
        '<div class="layer-map-grid">',
    ]
    for layer in layers:
        if not isinstance(layer, dict):
            continue
        label = str(layer.get("label", "Layer"))
        items = layer.get("items", [])
        if not isinstance(items, list):
            items = []
        out.append('<section class="layer-row">')
        out.append(f'<div class="layer-label">{html.escape(label)}</div>')
        out.append('<div class="layer-items">')
        for item in items:
            if isinstance(item, dict):
                item_label = str(item.get("label", ""))
                item_status = str(item.get("status", ""))
            else:
                item_label = str(item)
                item_status = ""
            status_attr = f' data-status="{html.escape(item_status, quote=True)}"' if item_status else ""
            out.append(f'<div class="layer-item"{status_attr}>{html.escape(item_label)}</div>')
        out.append("</div></section>")
    out.append("</div></figure>")
    return "\n".join(out)


def parse_table(lines: list[str], start: int) -> tuple[str, int] | None:
    if start + 1 >= len(lines):
        return None
    header = lines[start]
    separator = lines[start + 1]
    if "|" not in header or not re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", separator):
        return None

    table_lines = [header]
    index = start + 2
    while index < len(lines) and "|" in lines[index] and lines[index].strip():
        table_lines.append(lines[index])
        index += 1

    def cells(row: str) -> list[str]:
        stripped = row.strip().strip("|")
        return [cell.strip() for cell in stripped.split("|")]

    headers = cells(table_lines[0])
    body = [cells(row) for row in table_lines[1:]]
    out = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    for cell in headers:
        out.append(f"<th>{inline_markdown(cell)}</th>")
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        for cell in row:
            out.append(f"<td>{inline_markdown(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out), index


def close_lists(out: list[str], list_stack: list[str]) -> None:
    while list_stack:
        out.append(f"</{list_stack.pop()}>")


def flush_paragraph(out: list[str], paragraph: list[str]) -> None:
    if paragraph:
        out.append(f"<p>{inline_markdown(' '.join(part.strip() for part in paragraph))}</p>")
        paragraph.clear()


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_stack: list[str] = []
    index = 0
    in_code = False
    code_lang = ""
    code_lines: list[str] = []

    while index < len(lines):
        line = lines[index]

        fence = re.match(r"^\s*(```+)\s*([A-Za-z0-9_-]+)?\s*$", line)
        if fence:
            if in_code:
                code = "\n".join(code_lines)
                if code_lang.lower() == "mermaid":
                    out.append(f'<pre class="mermaid">{html.escape(code)}</pre>')
                elif code_lang.lower() == "rva-layer-map":
                    out.append(render_layer_map(code))
                else:
                    out.append(
                        f'<pre class="code-block"><code>{html.escape(code)}</code></pre>'
                    )
                code_lines = []
                code_lang = ""
                in_code = False
            else:
                flush_paragraph(out, paragraph)
                close_lists(out, list_stack)
                in_code = True
                code_lang = fence.group(2) or ""
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if not line.strip():
            flush_paragraph(out, paragraph)
            close_lists(out, list_stack)
            index += 1
            continue

        table = parse_table(lines, index)
        if table:
            flush_paragraph(out, paragraph)
            close_lists(out, list_stack)
            table_html, index = table
            out.append(table_html)
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            flush_paragraph(out, paragraph)
            close_lists(out, list_stack)
            level = min(len(heading.group(1)) + 1, 6)
            text = heading.group(2).strip()
            out.append(f'<h{level} id="{slugify(text, f"section-{index}")}">{inline_markdown(text)}</h{level}>')
            index += 1
            continue

        unordered = re.match(r"^\s*[-*]\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+[.]\s+(.+)$", line)
        if unordered or ordered:
            flush_paragraph(out, paragraph)
            tag = "ul" if unordered else "ol"
            if not list_stack or list_stack[-1] != tag:
                close_lists(out, list_stack)
                out.append(f"<{tag}>")
                list_stack.append(tag)
            item = (unordered or ordered).group(1)
            out.append(f"<li>{inline_markdown(item)}</li>")
            index += 1
            continue

        paragraph.append(line)
        index += 1

    if in_code:
        code = "\n".join(code_lines)
        out.append(f'<pre class="code-block"><code>{html.escape(code)}</code></pre>')
    flush_paragraph(out, paragraph)
    close_lists(out, list_stack)
    return "\n".join(out)


def mermaid_blocks(markdown: str) -> list[str]:
    return re.findall(r"```mermaid\s*\n(.*?)\n```", markdown, flags=re.DOTALL | re.IGNORECASE)


def find_mermaid_warnings(markdown: str, source: Path) -> list[str]:
    warnings: list[str] = []
    for block_index, block in enumerate(mermaid_blocks(markdown), start=1):
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("%%"):
                continue
            node_match = re.match(
                r"^(?:subgraph\s+)?([A-Za-z][A-Za-z0-9_]*)\s*(?:\[|\(|\{|\>|@|:::|-->|---|==>|-.->|:)",
                stripped,
            )
            if node_match and node_match.group(1) in MERMAID_UNSAFE_IDS:
                warnings.append(
                    f"{source.as_posix()} mermaid block {block_index}: unsafe id/keyword `{node_match.group(1)}`"
                )
    return warnings


def infer_language(markdown: str) -> str:
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", markdown))
    latin_words = len(re.findall(r"\b[A-Za-z]{3,}\b", markdown))
    return "zh" if cjk_chars >= 8 and cjk_chars >= latin_words // 3 else "en"


def normalize_language(value: str, markdown: str) -> str:
    if value in {"zh", "en"}:
        return value
    return infer_language(markdown)


def discover_inputs(analysis_dir: Path) -> list[Path]:
    inputs: list[Path] = []
    quick_scan = analysis_dir / "quick-scan.md"
    if quick_scan.exists():
        inputs.append(quick_scan)

    module_dir = analysis_dir / "module-cards"
    if module_dir.exists():
        inputs.extend(sorted(module_dir.glob("*.md")))

    report = analysis_dir / "report.md"
    if report.exists():
        inputs.append(report)

    return inputs


def doc_kind(path: Path, analysis_dir: Path, labels: dict[str, str]) -> str:
    try:
        rel = path.resolve().relative_to(analysis_dir.resolve())
    except ValueError:
        return labels["custom"]
    if rel.as_posix() == "quick-scan.md":
        return labels["quick_scan"]
    if rel.parts and rel.parts[0] == "module-cards":
        return labels["focused_map"]
    if rel.as_posix() == "report.md":
        return labels["full_report"]
    return labels["custom"]


def load_documents(paths: list[Path], analysis_dir: Path, labels: dict[str, str]) -> tuple[list[Document], list[str]]:
    docs: list[Document] = []
    warnings: list[str] = []
    for path in paths:
        markdown = path.read_text(encoding="utf-8")
        warnings.extend(find_mermaid_warnings(markdown, path))
        fallback = path.stem.replace("-", " ").title()
        docs.append(
            Document(
                path=path,
                title=first_heading(markdown, fallback),
                kind=doc_kind(path, analysis_dir, labels),
                html=markdown_to_html(markdown),
            )
        )
    return docs, warnings


def build_html(docs: list[Document], title: str, analysis_dir: Path, language: str, labels: dict[str, str], warnings: list[str]) -> str:
    nav_items = []
    sections = []
    for index, doc in enumerate(docs, start=1):
        section_id = f"doc-{index}-{slugify(doc.title, str(index))}"
        nav_items.append(
            f'<a href="#{section_id}"><span>{html.escape(doc.kind)}</span>{html.escape(doc.title)}</a>'
        )
        try:
            rel_path = doc.path.resolve().relative_to(analysis_dir.resolve()).as_posix()
        except ValueError:
            rel_path = doc.path.as_posix()
        sections.append(
            f"""
            <section id="{section_id}" class="report-section">
              <div class="section-kicker">{html.escape(doc.kind)} · {html.escape(rel_path)}</div>
              {doc.html}
            </section>
            """
        )

    artifact_count = f"{len(docs)} {labels['source_artifacts']}" if language == "en" else f"{len(docs)}{labels['source_artifacts']}"
    warning_html = ""
    if warnings:
        warning_items = "".join(f"<li>{inline_markdown(item)}</li>" for item in warnings)
        warning_html = f"""
        <section class="warnings" aria-label="{html.escape(labels['warnings'])}">
          <h2>{html.escape(labels['warnings'])}</h2>
          <ul>{warning_items}</ul>
        </section>
        """

    return f"""<!doctype html>
<html lang="{html.escape(language)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f5f1;
      --ink: #22211d;
      --muted: #6a665d;
      --line: #d9d4c8;
      --panel: #fffdf8;
      --accent: #0d6b63;
      --accent-2: #a94724;
      --code: #ede8dd;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 15px/1.55 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    a {{ color: inherit; }}
    .shell {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
    }}
    aside {{
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
      padding: 22px 18px;
      border-right: 1px solid var(--line);
      background: #eeeadf;
    }}
    .brand {{
      margin-bottom: 22px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--line);
    }}
    .brand h1 {{
      margin: 0 0 6px;
      font-size: 18px;
      line-height: 1.2;
      letter-spacing: 0;
    }}
    .brand p {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
    }}
    nav {{
      display: grid;
      gap: 8px;
    }}
    nav a {{
      display: grid;
      gap: 2px;
      padding: 9px 10px;
      border: 1px solid transparent;
      text-decoration: none;
    }}
    nav a:hover, nav a:focus {{
      border-color: var(--line);
      background: rgba(255,255,255,.45);
      outline: none;
    }}
    nav span {{
      color: var(--accent);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    main {{
      min-width: 0;
      padding: 28px clamp(18px, 4vw, 54px) 60px;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--line);
    }}
    .toolbar strong {{ font-size: 14px; }}
    #render-status {{
      color: var(--muted);
      font-size: 13px;
    }}
    .report-section {{
      max-width: 1120px;
      margin: 0 0 28px;
      padding: 24px 0 30px;
      border-bottom: 1px solid var(--line);
    }}
    .warnings {{
      max-width: 1120px;
      margin: 0 0 22px;
      padding: 14px 16px;
      border: 1px solid #d29b7d;
      background: #fff7ef;
    }}
    .warnings h2 {{
      margin: 0 0 8px;
      font-size: 16px;
      color: var(--accent-2);
    }}
    .warnings ul {{
      margin: 0;
      padding-left: 20px;
    }}
    .section-kicker {{
      color: var(--accent-2);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .05em;
      margin-bottom: 12px;
    }}
    h2, h3, h4, h5, h6 {{
      margin: 22px 0 10px;
      line-height: 1.2;
      letter-spacing: 0;
    }}
    h2 {{ font-size: clamp(26px, 4vw, 44px); margin-top: 0; }}
    h3 {{ font-size: 22px; }}
    h4 {{ font-size: 17px; }}
    p, ul, ol {{ max-width: 860px; }}
    li {{ margin: 4px 0; }}
    code {{
      padding: 1px 5px;
      background: var(--code);
      border-radius: 3px;
      font-size: .92em;
    }}
    pre {{
      overflow: auto;
      border: 1px solid var(--line);
      background: var(--panel);
    }}
    .code-block {{
      padding: 14px;
    }}
    pre.mermaid {{
      padding: 18px;
      min-height: 80px;
      text-align: center;
    }}
    .layer-map {{
      margin: 18px 0 24px;
      padding: 0;
      max-width: 1120px;
    }}
    .layer-map figcaption {{
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      margin: 0 0 10px;
      color: var(--ink);
      font-weight: 700;
    }}
    .layer-map figcaption span {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    .layer-map-grid {{
      display: grid;
      gap: 8px;
      border: 1px solid #a8a755;
      background: #fffde8;
      padding: 10px;
    }}
    .layer-row {{
      display: grid;
      grid-template-columns: minmax(92px, 128px) minmax(0, 1fr);
      gap: 8px;
      min-height: 64px;
    }}
    .layer-label {{
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 8px;
      background: #b85ae5;
      color: #fff;
      font-weight: 800;
      text-align: center;
      border: 1px solid #9d43c8;
    }}
    .layer-items {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 8px;
      align-content: center;
      padding: 8px;
      border: 1px dashed #bd78e5;
      background: #fffafc;
    }}
    .layer-item {{
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 42px;
      padding: 8px 10px;
      border: 1px solid #b56af0;
      background: #f0eaff;
      color: #2d2638;
      font-weight: 650;
      text-align: center;
      overflow-wrap: anywhere;
    }}
    .layer-item[data-status="candidate"] {{
      border-style: dashed;
    }}
    .layer-map-error {{
      border-color: #d29b7d;
      background: #fff7ef;
    }}
    .table-wrap {{
      max-width: 100%;
      overflow: auto;
      margin: 14px 0 18px;
      border: 1px solid var(--line);
      background: var(--panel);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 680px;
    }}
    th, td {{
      padding: 9px 10px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
      text-align: left;
    }}
    th {{
      color: var(--accent);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .04em;
      background: #f4f0e7;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    @media (max-width: 820px) {{
      .shell {{ grid-template-columns: 1fr; }}
      aside {{
        position: static;
        height: auto;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }}
      nav {{
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      }}
      main {{ padding: 22px 16px 44px; }}
      .layer-row {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside>
      <div class="brand">
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(labels['tagline'])}</p>
      </div>
      <nav aria-label="{html.escape(labels['nav_label'])}">
        {"".join(nav_items)}
      </nav>
    </aside>
    <main>
      <div class="toolbar">
        <strong>{html.escape(artifact_count)}</strong>
        <span id="render-status">{html.escape(labels['loading'])}</span>
      </div>
      {warning_html}
      {"".join(sections)}
    </main>
  </div>
  <script type="module">
    const status = document.getElementById('render-status');
    try {{
      const mermaidModule = await import('{MERMAID_CDN}');
      const mermaid = mermaidModule.default;
      mermaid.initialize({{
        startOnLoad: false,
        securityLevel: 'strict',
        theme: 'default',
        flowchart: {{ htmlLabels: true, useMaxWidth: true }},
        sequence: {{ useMaxWidth: true }}
      }});
      await mermaid.run({{ querySelector: '.mermaid', suppressErrors: true }});
      status.textContent = {labels['rendered']!r};
    }} catch (error) {{
      console.error(error);
      status.textContent = {labels['failed']!r};
      status.style.color = '#a94724';
    }}
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-dir", default=".repo-visual-analysis", help="Analysis artifact directory.")
    parser.add_argument("--input", action="append", help="Markdown file to include. May be repeated.")
    parser.add_argument("--out", help="Output HTML path. Defaults to <analysis-dir>/index.html.")
    parser.add_argument("--title", help="HTML report title.")
    parser.add_argument("--language", choices=["auto", "en", "zh"], default="auto", help="Report chrome language.")
    args = parser.parse_args()

    analysis_dir = Path(args.analysis_dir).resolve()
    inputs = [Path(item).resolve() for item in args.input] if args.input else discover_inputs(analysis_dir)
    if not inputs:
        parser.error(
            "no Markdown artifacts found; expected quick-scan.md, module-cards/*.md, or report.md"
        )

    combined_markdown = "\n\n".join(path.read_text(encoding="utf-8") for path in inputs)
    language = normalize_language(args.language, combined_markdown)
    labels = LABELS[language]
    title = args.title or labels["title"]
    docs, warnings = load_documents(inputs, analysis_dir, labels)
    out = Path(args.out).resolve() if args.out else (analysis_dir / "index.html").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_html(docs, title, analysis_dir, language, labels, warnings), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

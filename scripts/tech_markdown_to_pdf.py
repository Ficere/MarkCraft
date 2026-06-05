#!/usr/bin/env python3
"""
Convert Markdown to a polished technology-style PDF or HTML document.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
from pathlib import Path


STYLE_PRESETS = {
    "tech": {
        "primary": "#00AEEF",
        "secondary": "#7C3AED",
        "accent_bg": "#0B1220",
        "text": "#111827",
        "muted": "#64748B",
        "soft": "#E0F2FE",
        "code_bg": "#0F172A",
        "code_text": "#E5E7EB",
    },
    "deep-blue": {
        "primary": "#2563EB",
        "secondary": "#06B6D4",
        "accent_bg": "#08111F",
        "text": "#0F172A",
        "muted": "#64748B",
        "soft": "#DBEAFE",
        "code_bg": "#0B1220",
        "code_text": "#E2E8F0",
    },
    "cyan-violet": {
        "primary": "#00D4FF",
        "secondary": "#8B5CF6",
        "accent_bg": "#0F1028",
        "text": "#111827",
        "muted": "#6B7280",
        "soft": "#EEF2FF",
        "code_bg": "#111827",
        "code_text": "#F3F4F6",
    },
    "slate-minimal": {
        "primary": "#334155",
        "secondary": "#0EA5E9",
        "accent_bg": "#F8FAFC",
        "text": "#0F172A",
        "muted": "#64748B",
        "soft": "#F1F5F9",
        "code_bg": "#F8FAFC",
        "code_text": "#0F172A",
    },
    "bio-ai": {
        "primary": "#00C2A8",
        "secondary": "#3B82F6",
        "accent_bg": "#071A23",
        "text": "#102027",
        "muted": "#607D8B",
        "soft": "#DDFCF6",
        "code_bg": "#06252D",
        "code_text": "#E6FFFA",
    },
}


DENSITY = {
    "compact": {"body": "10.2pt", "line": "1.50", "margin": "16mm 17mm 18mm 17mm"},
    "normal": {"body": "11pt", "line": "1.62", "margin": "18mm 19mm 20mm 19mm"},
    "spacious": {"body": "11.4pt", "line": "1.72", "margin": "20mm 22mm 22mm 22mm"},
}


def require_markdown():
    try:
        import markdown  # noqa: F401
        import pygments  # noqa: F401
    except ImportError:
        print("Installing missing Python packages: markdown pygments", file=sys.stderr)
        import importlib
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "pygments"])
        importlib.invalidate_caches()


def extract_title(md_text: str, input_path: Path) -> str:
    for line in md_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return re.sub(r"[#*_`]+", "", match.group(1)).strip()
    return input_path.stem.replace("-", " ").replace("_", " ").title()


def build_toc(md_text: str) -> str:
    items = []
    for line in md_text.splitlines():
        match = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        title = re.sub(r"[#*_`]+", "", match.group(2)).strip()
        if not title:
            continue
        items.append(f'<li class="toc-level-{level}">{html.escape(title)}</li>')
    if len(items) < 3:
        return ""
    return '<section class="toc-page"><h1>目录 / Contents</h1><ol class="toc-list">' + "\n".join(items) + "</ol></section>"


def markdown_to_html(md_text: str) -> str:
    require_markdown()
    import markdown

    md_text = clean_invisible_characters(md_text)
    md_text = normalize_citation_markers(md_text)

    renderer = markdown.Markdown(
        extensions=[
            "extra",
            "fenced_code",
            "tables",
            "footnotes",
            "toc",
            "codehilite",
            "sane_lists",
            "nl2br",
            "attr_list",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "codehilite",
                "guess_lang": False,
                "linenums": False,
            }
        },
        output_format="html5",
    )
    return enhance_wide_tables(renderer.convert(md_text))


# Tables with at least this many columns are rendered on a wide landscape page so
# that content-sized columns have room to breathe instead of being squeezed into
# uniform narrow columns that shred CJK text and English tokens alike.
WIDE_TABLE_MIN_COLUMNS = 5


def enhance_wide_tables(body_html: str) -> str:
    """Wrap wide tables so they render on landscape pages with content-sized columns.

    The default fixed equal-width layout works for 2-4 column tables but forces
    severe wrapping on 5+ column tables (model names break mid-word, parentheses and
    English tokens fragment). Detect those tables and tag them for landscape layout.
    """

    def column_count(table_html: str) -> int:
        header = re.search(r"<thead\b[^>]*>(.*?)</thead>", table_html, re.IGNORECASE | re.DOTALL)
        scope = header.group(1) if header else table_html
        first_row = re.search(r"<tr\b[^>]*>(.*?)</tr>", scope, re.IGNORECASE | re.DOTALL)
        if not first_row:
            return 0
        return len(re.findall(r"<t[hd]\b", first_row.group(1), re.IGNORECASE))

    def wrap(match: re.Match) -> str:
        table_html = match.group(0)
        if column_count(table_html) < WIDE_TABLE_MIN_COLUMNS:
            return table_html
        return f'<div class="wide-table-page">{table_html}</div>'

    return re.sub(r"<table\b.*?</table>", wrap, body_html, flags=re.IGNORECASE | re.DOTALL)


def clean_invisible_characters(md_text: str) -> str:
    """Remove or normalize invisible characters that commonly damage PDF layout."""
    replacements = {
        "\ufeff": "",
        "\u200b": "",
        "\u200c": "",
        "\u200d": "",
        "\u2060": "",
        "\u00ad": "",
        "\u00a0": " ",
        "\u3000": " ",
    }
    for src, dst in replacements.items():
        md_text = md_text.replace(src, dst)
    md_text = md_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in md_text.split("\n")]
    return "\n".join(lines)


def normalize_citation_markers(md_text: str) -> str:
    """Render [^1]-style citation markers as superscripts when no footnote definitions exist."""
    has_footnote_defs = re.search(r"(?m)^\[\^[^\]]+\]:", md_text) is not None
    if has_footnote_defs:
        return md_text
    return re.sub(r"\[\^([A-Za-z0-9_-]+)\]", r'<sup class="ref-marker">[\1]</sup>', md_text)


def css(palette: dict[str, str], density: dict[str, str], title: str, team_name: str, slogan: str) -> str:
    escaped_team = team_name.replace("\\", "\\\\").replace('"', '\\"')
    escaped_slogan = slogan.replace("\\", "\\\\").replace('"', '\\"')
    escaped_title = title.replace("\\", "\\\\").replace('"', '\\"')
    return f"""
    @page {{
      size: A4;
      margin: {density["margin"]};
      @top-left {{
        content: "{escaped_team}";
        font-size: 8.5pt;
        color: {palette["muted"]};
      }}
      @top-right {{
        content: "{escaped_title}";
        font-size: 8.5pt;
        color: {palette["muted"]};
      }}
      @bottom-left {{
        content: "{escaped_slogan}";
        font-size: 8pt;
        color: {palette["muted"]};
      }}
      @bottom-right {{
        content: counter(page);
        font-size: 8.5pt;
        color: {palette["muted"]};
      }}
    }}

    @page wide {{
      size: A4 landscape;
      margin: 14mm 15mm 15mm 15mm;
      @top-left {{ content: "{escaped_team}"; font-size: 8.5pt; color: {palette["muted"]}; }}
      @top-right {{ content: "{escaped_title}"; font-size: 8.5pt; color: {palette["muted"]}; }}
      @bottom-left {{ content: "{escaped_slogan}"; font-size: 8pt; color: {palette["muted"]}; }}
      @bottom-right {{ content: counter(page); font-size: 8.5pt; color: {palette["muted"]}; }}
    }}

    * {{ box-sizing: border-box; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", "PingFang SC",
        "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC",
        "WenQuanYi Micro Hei", Arial, sans-serif;
      color: {palette["text"]};
      font-size: {density["body"]};
      line-height: {density["line"]};
      letter-spacing: 0.01em;
      margin: 0;
      background: white;
    }}

    .cover {{
      min-height: 238mm;
      padding: 18mm 14mm;
      margin: -4mm -2mm 12mm -2mm;
      color: white;
      background:
        linear-gradient(135deg, {palette["accent_bg"]} 0%, #111827 52%, {palette["secondary"]} 155%),
        radial-gradient(circle at 88% 12%, {palette["primary"]}55, transparent 28%),
        radial-gradient(circle at 12% 88%, {palette["secondary"]}44, transparent 25%);
      position: relative;
      page-break-after: always;
      overflow: hidden;
    }}

    .cover:before {{
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
      background-size: 18px 18px;
      mask-image: linear-gradient(135deg, black 0%, transparent 86%);
    }}

    .cover-inner {{
      position: relative;
      z-index: 1;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .brand-badge {{
      display: inline-block;
      width: fit-content;
      padding: 7px 12px;
      border: 1px solid rgba(255,255,255,0.22);
      border-radius: 999px;
      background: rgba(255,255,255,0.08);
      color: #E0F7FF;
      font-size: 10pt;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}

    .cover-title {{
      margin-top: 58mm;
      max-width: 164mm;
    }}

    .cover h1 {{
      color: white;
      font-size: 31pt;
      line-height: 1.18;
      margin: 0 0 8mm 0;
      border: none;
      padding: 0;
      letter-spacing: -0.03em;
    }}

    .cover .slogan {{
      color: #D8F8FF;
      font-size: 14pt;
      max-width: 140mm;
      border-left: 4px solid {palette["primary"]};
      padding-left: 5mm;
    }}

    .cover-meta {{
      color: rgba(255,255,255,0.70);
      font-size: 9.5pt;
      display: flex;
      justify-content: space-between;
      border-top: 1px solid rgba(255,255,255,0.18);
      padding-top: 6mm;
    }}

    .tech-rule {{
      height: 4px;
      width: 48mm;
      border-radius: 99px;
      background: linear-gradient(90deg, {palette["primary"]}, {palette["secondary"]});
      margin: 0 0 8mm 0;
    }}

    main {{
      counter-reset: h2;
    }}

    h1, h2, h3, h4 {{
      font-weight: 750;
      line-height: 1.26;
      page-break-after: avoid;
      break-after: avoid;
      color: {palette["text"]};
    }}

    h1 {{
      font-size: 22pt;
      margin: 0 0 7mm 0;
      padding-bottom: 3mm;
      border-bottom: 2px solid {palette["primary"]};
    }}

    h2 {{
      font-size: 17pt;
      margin: 10mm 0 4mm 0;
      padding-left: 4mm;
      border-left: 4px solid {palette["primary"]};
    }}

    h3 {{
      font-size: 13.5pt;
      margin: 7mm 0 2.5mm 0;
      color: {palette["secondary"]};
    }}

    h4 {{
      font-size: 11.5pt;
      margin: 5mm 0 1.8mm 0;
      color: {palette["text"]};
    }}

    p {{ margin: 0 0 3.5mm 0; }}
    strong {{ font-weight: 750; }}
    em {{ color: {palette["muted"]}; }}

    sup.ref-marker {{
      color: {palette["secondary"]};
      font-weight: 700;
      font-size: 0.70em;
      line-height: 0;
      margin-left: 0.06em;
    }}

    a {{
      color: {palette["secondary"]};
      text-decoration: none;
      overflow-wrap: anywhere;
    }}

    ul, ol {{
      margin: 2mm 0 4mm 0;
      padding-left: 7mm;
    }}

    li {{ margin: 1.2mm 0; }}

    blockquote {{
      margin: 5mm 0;
      padding: 3.5mm 5mm;
      border-left: 4px solid {palette["primary"]};
      background: {palette["soft"]};
      border-radius: 0 8px 8px 0;
      color: {palette["text"]};
      page-break-inside: avoid;
    }}

    table {{
      width: 100%;
      table-layout: fixed;
      border-collapse: collapse;
      margin: 5mm 0 6mm 0;
      font-size: 9.6pt;
      text-align: left;
    }}

    th {{
      background: linear-gradient(90deg, {palette["accent_bg"]}, {palette["secondary"]});
      color: white;
      font-weight: 700;
      text-align: left !important;
    }}

    th, td {{
      border: 1px solid #CBD5E1;
      padding: 2.4mm 2.8mm;
      vertical-align: top;
      overflow-wrap: anywhere;
      word-break: normal;
      hyphens: auto;
      text-align: left !important;
    }}

    tr:nth-child(even) td {{ background: #F8FAFC; }}

    tr {{
      page-break-inside: avoid;
      break-inside: avoid;
    }}

    /* Wide tables (5+ columns) render on a landscape page with content-sized
       columns so model names, parentheses, and English tokens stay intact while
       Chinese prose still wraps naturally. */
    .wide-table-page {{
      page: wide;
      page-break-before: always;
      page-break-after: always;
    }}

    .wide-table-page table {{
      table-layout: auto;
      font-size: 8.6pt;
    }}

    .wide-table-page th,
    .wide-table-page td {{
      padding: 1.8mm 2.2mm;
      word-break: keep-all;
      overflow-wrap: normal;
      hyphens: manual;
    }}

    .wide-table-page a {{ overflow-wrap: normal; word-break: keep-all; }}

    code {{
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 0.92em;
      color: {palette["secondary"]};
      background: {palette["soft"]};
      padding: 0.15em 0.38em;
      border-radius: 4px;
    }}

    pre, .codehilite {{
      background: {palette["code_bg"]};
      color: {palette["code_text"]};
      border-radius: 10px;
      padding: 4mm 4.5mm;
      margin: 5mm 0;
      overflow-wrap: break-word;
      white-space: pre-wrap;
      page-break-inside: avoid;
      break-inside: avoid;
      border: 1px solid rgba(148, 163, 184, 0.35);
    }}

    pre code, .codehilite code {{
      color: inherit;
      background: transparent;
      padding: 0;
      font-size: 8.8pt;
      line-height: 1.5;
    }}

    img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 5mm auto;
      page-break-inside: avoid;
    }}

    hr {{
      border: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, {palette["primary"]}, transparent);
      margin: 9mm 0;
    }}

    .toc-page {{
      page-break-after: always;
      padding-top: 8mm;
    }}

    .toc-list {{
      list-style: none;
      padding-left: 0;
      border-left: 3px solid {palette["primary"]};
      margin-left: 2mm;
    }}

    .toc-list li {{
      padding: 1.7mm 0 1.7mm 5mm;
      border-bottom: 1px solid #E2E8F0;
    }}

    .toc-level-2 {{ padding-left: 10mm !important; color: {palette["text"]}; }}
    .toc-level-3 {{ padding-left: 16mm !important; color: {palette["muted"]}; font-size: 9.5pt; }}
    """


def build_document(md_text: str, args: argparse.Namespace, input_path: Path) -> str:
    title = args.title or extract_title(md_text, input_path)
    generated_date = args.date or dt.date.today().isoformat()
    palette = STYLE_PRESETS[args.style]
    density = DENSITY[args.density]
    body_html = markdown_to_html(md_text)
    toc_html = build_toc(md_text) if args.toc else ""
    doc_css = css(palette, density, title, args.team_name, args.slogan)

    return f"""<!doctype html>
<html lang="{html.escape(args.language)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="author" content="Perplexity Computer">
  <style>{doc_css}</style>
</head>
<body>
  <section class="cover">
    <div class="cover-inner">
      <div>
        <div class="brand-badge">{html.escape(args.team_name)}</div>
        <div class="cover-title">
          <div class="tech-rule"></div>
          <h1>{html.escape(title)}</h1>
          <div class="slogan">{html.escape(args.slogan)}</div>
        </div>
      </div>
      <div class="cover-meta">
        <span>{html.escape(args.team_name)}</span>
        <span>{html.escape(generated_date)}</span>
      </div>
    </div>
  </section>
  {toc_html}
  <main>
    {body_html}
  </main>
</body>
</html>
"""


def write_pdf(html_text: str, output_pdf: Path, base_url: Path) -> bool:
    try:
        from weasyprint import HTML
    except Exception as exc:
        print(f"WeasyPrint unavailable, attempting install: {exc}", file=sys.stderr)
        try:
            import importlib
            import subprocess

            subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint"])
            importlib.invalidate_caches()
            from weasyprint import HTML
        except Exception as install_exc:
            print(f"WeasyPrint unavailable, skipping PDF render: {install_exc}", file=sys.stderr)
            return False

    HTML(string=html_text, base_url=str(base_url)).write_pdf(str(output_pdf))
    set_pdf_metadata(output_pdf)
    return True


def set_pdf_metadata(output_pdf: Path) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except Exception:
        try:
            import importlib
            import subprocess

            subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
            importlib.invalidate_caches()
            from pypdf import PdfReader, PdfWriter
        except Exception as exc:
            print(f"Could not set PDF metadata: {exc}", file=sys.stderr)
            return

    reader = PdfReader(str(output_pdf))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    existing = reader.metadata or {}
    title = existing.get("/Title") or output_pdf.stem
    writer.add_metadata({
        "/Title": str(title),
        "/Author": "Perplexity Computer",
        "/Producer": "WeasyPrint + pypdf",
    })
    with output_pdf.open("wb") as f:
        writer.write(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to a branded technology-style PDF.")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("--output", "-o", help="Output PDF path")
    parser.add_argument("--team-name", default="AI Science Team", help="Team, lab, department, or project name")
    parser.add_argument("--slogan", default="From Markdown to Knowledge", help="Short slogan shown on cover/footer")
    parser.add_argument("--title", help="Override document title")
    parser.add_argument("--date", help="Override cover date, default today")
    parser.add_argument("--language", default="mixed", choices=["zh", "en", "mixed"], help="Document language hint")
    parser.add_argument("--style", default="tech", choices=sorted(STYLE_PRESETS), help="Visual style preset")
    parser.add_argument("--density", default="normal", choices=sorted(DENSITY), help="Typography density")
    parser.add_argument("--toc", action="store_true", default=True, help="Include generated table of contents")
    parser.add_argument("--no-toc", action="store_false", dest="toc", help="Disable generated table of contents")
    parser.add_argument("--html-only", action="store_true", help="Only generate HTML")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    output_pdf = Path(args.output).expanduser().resolve() if args.output else input_path.with_suffix(".pdf")
    output_html = output_pdf.with_suffix(".html")
    md_text = input_path.read_text(encoding="utf-8")
    html_text = build_document(md_text, args, input_path)
    output_html.write_text(html_text, encoding="utf-8")
    print(f"HTML written: {output_html}")

    if args.html_only:
        return 0

    ok = write_pdf(html_text, output_pdf, input_path.parent)
    if not ok:
        print(f"PDF not generated. Use the HTML fallback: {output_html}", file=sys.stderr)
        return 1

    if output_pdf.exists() and output_pdf.stat().st_size > 0:
        print(f"PDF written: {output_pdf}")
        return 0

    print(f"PDF generation failed: {output_pdf}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

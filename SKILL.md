---
name: markcraft
description: "MarkCraft converts Markdown documents into polished, readable PDF reports with a technology-style visual theme. Use when the user asks to turn .md, Markdown, README, technical notes, product docs, research briefs, proposals, or long-form documentation into a PDF with readable typography, code blocks, left-aligned tables, citations, Chinese/CJK support, and professional layout. Optional team name and slogan can be added as decorative branding on the cover, header, and footer."
license: MIT
compatibility: "Python 3.10+. Optional dependencies: markdown, pygments, weasyprint. Falls back to HTML output if PDF rendering dependencies are unavailable."
metadata:
  version: "1.0.0"
  author: "Perplexity Computer"
---

# MarkCraft

## When to Use This Skill

Use this skill when the user wants to:

- Convert Markdown files into polished PDF reports, technical documents, whitepapers, SOPs, README exports, product specs, research briefs, meeting notes, or proposals.
- Produce a PDF in any of 9 visual styles: `tech`, `deep-blue`, `cyan-violet`, `slate-minimal`, `bio-ai`, `business` (gold/charcoal), `academic` (navy/crimson), `warm-earth` (terracotta/brown), `forest` (forest green/teal).
- Optionally add a custom team name and slogan as visual decoration in the cover, header, footer, or watermark.
- Improve readability through better typography, spacing, section hierarchy, tables, code blocks, callouts, and page breaks.
- Preserve Chinese/CJK text quality and mixed Chinese-English technical writing.

Do not use this skill for slide-deck-first outputs unless the user explicitly asks for Marp/PPT-style presentation PDFs. For slide decks, use a PPT/Marp workflow instead.

## Core Behavior

When invoked, create a production-ready PDF from the provided Markdown while preserving the Markdown's meaning and improving document readability. Readability and clean layout are the core deliverable; team name and slogan are optional decoration, not requirements.

Team name and slogan are optional. Do not ask for them — if the user wants branding they will say so. When the user provides neither and asks for none, the script applies neutral defaults (team name `AI Science Team`, slogan `From Markdown to Knowledge`) so the cover and header still look finished. If a user wants a clean, unbranded look, pass empty values to suppress the badge and slogan.

Prefer a clean, restrained technology style over decorative clutter. The document should feel like a professional technical report, not a poster.

## Inputs to Collect

Collect or infer these inputs:

- `input_md`: Markdown file path or Markdown text. **Required** — this is the only input you actually need.
- `output_pdf`: desired PDF filename. Default to the input filename with `.pdf`.
- `team_name` *(optional)*: custom team, lab, department, company, or project name. Decorative only.
- `slogan` *(optional)*: short slogan, mission line, or document tagline. Decorative only.
- `author` *(optional)*: document author written to PDF `/Author` metadata and the HTML `<meta name="author">`. Resolved in order: `--author`, `MARKCRAFT_AUTHOR` env, the `author` key in the config file (`~/.config/markcraft/config`, override path with `MARKCRAFT_CONFIG`), then the default `Perplexity Computer`. `team_name` is decorative and is never used as the author.
- `language`: `zh`, `en`, or `mixed`. Default to `mixed`.
- `style`: default `tech`. Optional variants: `deep-blue`, `cyan-violet`, `slate-minimal`, `bio-ai`, `business`, `academic`, `warm-earth`, `forest`.
- `density`: default `normal`. Optional variants: `compact` for long documents and `spacious` for executive-facing reports.
- `toc`: default true for documents longer than 4 pages.

## Recommended Workflow

1. Inspect the Markdown source.
   - Identify title, subtitle, author/date, heading depth, tables, code blocks, images, citations, and long sections.
   - If the Markdown lacks a clear title, derive one from the filename or first heading.

2. Normalize the document.
   - Keep user content intact unless asked to edit.
   - The script strips invisible characters (BOM, zero-width spaces, non-breaking spaces) that otherwise damage layout; no manual cleanup needed.
   - Add a title block only if the document has no cover/title.
   - Preserve citation URLs and links.
   - Avoid changing technical terms, formulas, gene/protein names, chemical names, or code.

3. Apply readability improvements.
   - Use clear heading hierarchy.
   - Keep line length readable.
   - Add page-break control around headings, tables, images, and code blocks.
   - Render tables left-aligned with zebra striping and sufficient padding.
   - Wide tables (5+ columns) automatically render on a landscape page with content-sized columns so CJK text, parentheses, and English/model tokens stay intact.
   - Render code blocks with monospaced fonts and syntax highlighting.
   - Use callout styling for blockquotes and important notes.

4. Apply optional brand decoration (only when the user wants branding).
   - Put the team name and slogan on the cover.
   - Put the team name in the running header.
   - Put the slogan or document title in the footer when space allows.
   - Add subtle geometric accents, gradient lines, or grid backgrounds.
   - Do not let decoration reduce readability. When no branding is requested, a clean unbranded layout is a perfectly valid result.

5. Generate PDF.
   - Prefer the bundled script: `scripts/markcraft.py`.
   - If PDF dependencies fail, produce an HTML file with the same styling and explain that it can be printed to PDF.

6. QA before sharing.
   - Confirm the PDF exists and has nonzero size.
   - Open or inspect the first pages if possible.
   - Check CJK characters, headings, tables, code blocks, page numbers, links, and any brand text that was requested.
   - If the PDF is a formal deliverable, share the final file with the user.

## Bundled Script Usage

Use the bundled script from the skill directory. The only required argument is the input file:

```bash
python scripts/markcraft.py input.md --output report.pdf
```

Useful options (team name and slogan are optional decoration):

```bash
python scripts/markcraft.py input.md --style cyan-violet --density spacious --no-toc
python scripts/markcraft.py input.md --team-name "Platform Team" --slogan "Build, Measure, Learn"
python scripts/markcraft.py input.md --author "Jane Doe"
MARKCRAFT_AUTHOR="Jane Doe" python scripts/markcraft.py input.md
python scripts/markcraft.py input.md \
  --team-name "Deep Potential" \
  --slogan "AI for Science" \
  --style bio-ai \
  --density normal \
  --toc
python scripts/markcraft.py input.md --html-only
```

## Visual System

Default style rules:

- Page: A4, generous margins, readable body text.
- Fonts: system sans stack with strong Chinese support; monospaced stack for code.
- Colors: deep navy background accents, cyan primary accent, violet secondary accent, slate text.
- Cover: gradient top bar, team badge, slogan, document title, date.
- Headers/footers: unobtrusive, with team name, slogan/title, page numbers.
- Tables: high contrast, zebra rows, no cramped cells.
- Code: dark readable block or light technical block depending on style; never shrink below legible size.
- Callouts: left accent border and soft tinted background.

Read `references/style-guide.md` when the user asks for customization, brand consistency, or style variants.

## Markdown Support

The workflow should support:

- Headings H1-H4
- Paragraphs and emphasis
- Ordered/unordered lists and nested lists
- Fenced code blocks with language labels
- Inline code
- Tables
- Images with relative paths
- Links and URLs
- Blockquotes
- Horizontal rules
- Chinese/CJK characters
- Basic HTML embedded in Markdown
- Table of contents when requested

## Output Expectations

A successful output should:

- Produce a PDF that can be opened without errors.
- Display the team name and slogan correctly when branding was requested.
- Maintain readable typography and spacing across the whole document.
- Preserve Markdown structure and links.
- Avoid awkward page breaks after headings or inside tables/code when possible.
- Render Chinese and English text cleanly.
- Use a cohesive technology-style color palette without overwhelming the content.

## Troubleshooting

- If `weasyprint` is missing, install Python dependencies or use `--html-only`.
- If system libraries for PDF rendering are unavailable, generate HTML and print it to PDF from a browser.
- If Chinese text appears as tofu boxes, install or select a CJK-capable font such as PingFang SC, Microsoft YaHei, Noto Sans CJK, Source Han Sans, or WenQuanYi Micro Hei.
- Tables with 5+ columns are detected automatically and rendered on a landscape page with content-sized columns; for tables with extremely long cell text that still feels cramped, retry with `--density compact` or simplify the content.
- If code blocks overflow, keep horizontal scrolling in HTML or reduce font size slightly in PDF.

## Example User Prompts

- “把这份 Markdown 技术方案排成可读性更好的 PDF。”
- “Convert this README to a clean, readable PDF.”
- “Convert this Markdown research brief to a polished tech-style PDF, deep-blue theme.”
- “把这个 README 转成 PDF，团队名用 Deep Potential，slogan 用 AI for Science，科技风。”
- “生成一份带团队名称和口号页眉页脚的 PDF 报告。”

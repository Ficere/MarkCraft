---
name: markdown-to-pdf-tech
description: "Convert Markdown documents into polished, readable PDF reports with a technology-style visual theme. Use when the user asks to turn .md, Markdown, README, technical notes, product docs, research briefs, proposals, or long-form documentation into a PDF with custom team name, slogan, brand accents, Chinese/CJK support, readable typography, code blocks, tables, citations, and professional layout."
license: MIT
compatibility: "Python 3.10+. Optional dependencies: markdown, pygments, weasyprint. Falls back to HTML output if PDF rendering dependencies are unavailable."
metadata:
  version: "1.0.0"
  author: "Perplexity Computer"
---

# Markdown to PDF Tech

## When to Use This Skill

Use this skill when the user wants to:

- Convert Markdown files into polished PDF reports, technical documents, whitepapers, SOPs, README exports, product specs, research briefs, meeting notes, or proposals.
- Add a custom team name and slogan as visual decoration in the cover, header, footer, or watermark.
- Produce a technology-style PDF with dark blue, cyan, violet, slate, grid, glow, or gradient accents.
- Improve readability through better typography, spacing, section hierarchy, tables, code blocks, callouts, and page breaks.
- Preserve Chinese/CJK text quality and mixed Chinese-English technical writing.

Do not use this skill for slide-deck-first outputs unless the user explicitly asks for Marp/PPT-style presentation PDFs. For slide decks, use a PPT/Marp workflow instead.

## Core Behavior

When invoked, create a production-ready PDF from the provided Markdown while preserving the Markdown's meaning and improving document readability. Ask for missing brand details only if they materially affect the output. If the user does not provide team name or slogan, use neutral defaults:

- Team name: `AI Science Team`
- Slogan: `From Markdown to Knowledge`

Prefer a clean, restrained technology style over decorative clutter. The document should feel like a professional technical report, not a poster.

## Inputs to Collect

Collect or infer these inputs:

- `input_md`: Markdown file path or Markdown text.
- `output_pdf`: desired PDF filename. Default to the input filename with `.pdf`.
- `team_name`: custom team, lab, department, company, or project name.
- `slogan`: short slogan, mission line, or document tagline.
- `language`: `zh`, `en`, or `mixed`. Default to `mixed`.
- `style`: default `tech`. Optional variants: `deep-blue`, `cyan-violet`, `slate-minimal`, `bio-ai`.
- `density`: default `normal`. Optional variants: `compact` for long documents and `spacious` for executive-facing reports.
- `toc`: default true for documents longer than 4 pages.

## Recommended Workflow

1. Inspect the Markdown source.
   - Identify title, subtitle, author/date, heading depth, tables, code blocks, images, citations, and long sections.
   - If the Markdown lacks a clear title, derive one from the filename or first heading.

2. Normalize the document.
   - Keep user content intact unless asked to edit.
   - Add a title block only if the document has no cover/title.
   - Preserve citation URLs and links.
   - Avoid changing technical terms, formulas, gene/protein names, chemical names, or code.

3. Apply readability improvements.
   - Use clear heading hierarchy.
   - Keep line length readable.
   - Add page-break control around headings, tables, images, and code blocks.
   - Render tables with zebra striping and sufficient padding.
   - Render code blocks with monospaced fonts and syntax highlighting.
   - Use callout styling for blockquotes and important notes.

4. Apply brand decoration.
   - Put the team name and slogan on the cover.
   - Put the team name in the running header.
   - Put the slogan or document title in the footer when space allows.
   - Add subtle geometric accents, gradient lines, or grid backgrounds.
   - Do not let decoration reduce readability.

5. Generate PDF.
   - Prefer the bundled script: `scripts/tech_markdown_to_pdf.py`.
   - If PDF dependencies fail, produce an HTML file with the same styling and explain that it can be printed to PDF.

6. QA before sharing.
   - Confirm the PDF exists and has nonzero size.
   - Open or inspect the first pages if possible.
   - Check CJK characters, headings, tables, code blocks, page numbers, links, and brand text.
   - If the PDF is a formal deliverable, share the final file with the user.

## Bundled Script Usage

Use the bundled script from the skill directory:

```bash
python scripts/tech_markdown_to_pdf.py input.md \
  --output output.pdf \
  --team-name "Deep Potential" \
  --slogan "AI for Science" \
  --style bio-ai \
  --density normal \
  --toc
```

Useful options:

```bash
python scripts/tech_markdown_to_pdf.py input.md --output report.pdf
python scripts/tech_markdown_to_pdf.py input.md --team-name "Platform Team" --slogan "Build, Measure, Learn"
python scripts/tech_markdown_to_pdf.py input.md --style cyan-violet --density spacious --no-toc
python scripts/tech_markdown_to_pdf.py input.md --html-only
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
- Display the team name and slogan correctly.
- Maintain readable typography and spacing across the whole document.
- Preserve Markdown structure and links.
- Avoid awkward page breaks after headings or inside tables/code when possible.
- Render Chinese and English text cleanly.
- Use a cohesive technology-style color palette without overwhelming the content.

## Troubleshooting

- If `weasyprint` is missing, install Python dependencies or use `--html-only`.
- If system libraries for PDF rendering are unavailable, generate HTML and print it to PDF from a browser.
- If Chinese text appears as tofu boxes, install or select a CJK-capable font such as PingFang SC, Microsoft YaHei, Noto Sans CJK, Source Han Sans, or WenQuanYi Micro Hei.
- If tables overflow, retry with `--density compact` or manually simplify very wide tables.
- If code blocks overflow, keep horizontal scrolling in HTML or reduce font size slightly in PDF.

## Example User Prompts

- “把这个 README 转成 PDF，团队名用 Deep Potential，slogan 用 AI for Science，科技风。”
- “把这份 Markdown 技术方案排成可读性更好的 PDF。”
- “生成一份带团队名称和口号页眉页脚的 PDF 报告。”
- “Convert this Markdown research brief to a polished tech-style PDF.”

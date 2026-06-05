# 🛠 MarkCraft

Turn Markdown, README files, and technical notes into polished, readable PDF reports — with a clean technology-style theme and optional team branding. Crafted for clarity.

把 Markdown 文档、README、技术笔记转换成高可读性、带科技风视觉的 PDF 报告，团队名称和 slogan 等品牌装点完全可选。

It works two ways: as an **Agent Skill** that any compatible AI agent can load and trigger with plain language, and as a **standalone CLI script** you can run on its own. Built to the [Agent Skills open standard](https://agentskills.io), so it works across Claude Code, Cursor, GitHub Copilot, Codex, Windsurf, Gemini CLI, Perplexity Computer, and 30+ other agent platforms.

## Install

```bash
npx skills add Ficere/MarkCraft
```

> Requires Node.js. Once installed, your agent auto-discovers the skill and loads it when it's relevant — no command to memorize.
>
> 需要 Node.js。安装后 Agent 会自动发现并按需加载该技能。

<details>
<summary>Other ways to install / 其他安装方式</summary>

**Manual install / 手动安装** — clone and drop the directory into your agent's skills folder:

```bash
git clone https://github.com/Ficere/MarkCraft.git markcraft
#   Claude Code:  ~/.claude/skills/
#   Cursor:       .cursor/skills/
#   Copilot:      .github/skills/
#   Codex:        ~/.codex/skills/
#   Gemini CLI:   .gemini/skills/
```

**Perplexity Computer** — download this repo as a zip and upload it on the [Skills management page](https://www.perplexity.ai/computer/skills).

</details>

## Usage

Once installed, just describe what you want in natural language. A bare "turn this into a PDF" is enough — everything else is optional refinement.

```text
Convert this README into a clean, readable PDF.
```

```text
把这份 Markdown 技术方案转成 PDF，目录清晰、表格可读、代码块不要挤在一起。
```

You can layer on style and optional branding when you want it:

```text
Convert this research brief to a polished tech-style PDF, deep-blue theme.
```

```text
把这份方案排成 PDF，团队名用 Platform Engineering，slogan 用 Build reliable AI systems。
```

Team name and slogan are decorative. Leave them out and the PDF still looks finished; add them when you want a branded cover, header, or footer.

## Features

| What | Details |
|------|---------|
| **Markdown → PDF** | Convert `.md`, README files, technical docs, product specs, and research briefs into clean A4 PDFs |
| **Readable typography** | Tuned heading hierarchy, line spacing, margins, left-aligned tables, code blocks, callouts, and page breaks |
| **Tech-style themes** | Five built-in looks: `tech`, `deep-blue`, `cyan-violet`, `slate-minimal`, `bio-ai` |
| **Optional branding** | Add a team name and slogan to the cover, header, and footer — entirely optional decoration |
| **Bilingual layout** | Solid Chinese/CJK font stacks and mixed Chinese-English technical writing |
| **Clean input** | Strips invisible characters (zero-width spaces, BOM, non-breaking spaces) that quietly break layout |
| **Citation markers** | Standard Markdown footnotes, plus `[^N]`-style markers rendered as superscripts |
| **HTML fallback** | If PDF rendering libraries are missing, emit the same styling as HTML you can print to PDF from a browser |

<details>
<summary>Style options / 样式参数</summary>

| Option | Values | Notes |
|--------|--------|-------|
| `--style` | `tech` | Default tech blue/violet |
| `--style` | `deep-blue` | More formal engineering blue |
| `--style` | `cyan-violet` | Suits AI, data, and model-platform docs |
| `--style` | `slate-minimal` | Restrained, low-decoration internal docs |
| `--style` | `bio-ai` | Fits AI for Science, computational biology, drug discovery |
| `--density` | `compact` | Long documents — tighter but still readable |
| `--density` | `normal` | Default |
| `--density` | `spacious` | Roomier layout for executive or client-facing reports |

</details>

## Examples

Two real case studies, each generated with this skill from a Markdown source — see the source and the rendered PDF side by side in [`examples/`](examples/):

| Document | Markdown | PDF |
|----------|----------|-----|
| AI Coding Agents in Software Engineering Workflows (2026, English) | [`.md`](examples/ai-coding-agents-workflows-2026.md) | [`.pdf`](examples/ai-coding-agents-workflows-2026.pdf) |
| AI for Science: 蛋白设计基础模型与工作流 (2026, 中文) | [`.md`](examples/ai-for-science-protein-design-2026.md) | [`.pdf`](examples/ai-for-science-protein-design-2026.pdf) |

## Standalone Script

`scripts/markcraft.py` runs without any agent platform. The only required argument is the input file:

```bash
python scripts/markcraft.py report.md --output report.pdf
```

Common variations:

```bash
# Pick a theme and density
python scripts/markcraft.py report.md --style cyan-violet --density compact

# Add optional branding
python scripts/markcraft.py report.md --team-name "Research Ops" --slogan "Readable by design"

# Emit HTML only (no PDF dependencies needed)
python scripts/markcraft.py report.md --html-only
```

Dependencies:

- Python 3.10+
- `markdown`, `pygments`, `weasyprint`, `pypdf`

The script auto-installs missing Python packages where it can; if the system lacks WeasyPrint's native libraries, it keeps the HTML output as a fallback.

## Structure

```text
markcraft/
├── SKILL.md                         # Skill entry point, read automatically by agents
├── scripts/
│   └── markcraft.py                 # Standalone Markdown → tech-style PDF/HTML script
├── references/
│   └── style-guide.md               # Visual style, palette, and typography guide
├── examples/                        # Sample Markdown sources and rendered PDFs
├── requirements.txt                 # Python dependencies
├── LICENSE
└── README.md
```

## Scope

**Good fit:**

- Technical proposals, product docs, research briefs, SOPs, READMEs, and internal reports
- Mixed Chinese-English engineering documents with lots of tables and code blocks
- PDFs that benefit from consistent styling — with or without team branding

**Not a fit:**

- Slide-deck-style presentation PDFs
- Material needing rich interactivity or web animation
- Final book or journal output requiring strict publishing typography

## License

MIT

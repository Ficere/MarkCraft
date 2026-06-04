# 📄 Markdown to PDF Tech

把 Markdown 文档转换成带团队名称、slogan 和科技风视觉装点的高可读性 PDF 报告。

Convert Markdown into polished, readable technology-style PDF reports with custom team branding.

遵循 [Agent Skills 开放标准](https://agentskills.io)，兼容 Claude Code、Cursor、GitHub Copilot、Codex、Windsurf、Gemini CLI、Perplexity Computer 等 30+ AI Agent 平台。

## 安装 / Install

```bash
npx skills add Ficere/markdown-to-pdf-tech
```

> 需要 Node.js。安装后 Agent 会自动发现并按需加载该技能。
>
> Requires Node.js. Once installed, your agent will auto-discover and load this skill when relevant.

<details>
<summary>其他安装方式 / Alternative methods</summary>

**手动安装 / Manual install：**

```bash
git clone https://github.com/Ficere/markdown-to-pdf-tech.git
# 将整个目录复制到你的 Agent 的 skills 目录下即可
# Copy the directory to your agent's skills folder:
#   Claude Code:  ~/.claude/skills/
#   Cursor:       .cursor/skills/
#   Copilot:      .github/skills/
#   Codex:        ~/.codex/skills/
#   Gemini CLI:   .gemini/skills/
```

**Perplexity Computer：**

下载本仓库 zip → 在 [Skills 管理页面](https://www.perplexity.ai/computer/skills) 上传。

</details>

## 使用 / Usage

安装后直接用自然语言触发，无需记命令：

```text
把这份 Markdown 技术方案转成 PDF，团队名用 Platform Engineering，slogan 用 Build reliable AI systems，科技风。
```

```text
Convert this README into a polished PDF report with the team name Research Ops and a clean deep-blue style.
```

```text
把这份产品文档排成适合内部评审的 PDF，要求目录清晰、表格可读、代码块不要挤在一起。
```

```text
生成一份带团队名称和口号页眉页脚的 PDF 报告，整体偏 AI / engineering 风格。
```

## 功能 / Features

| 模块 | 说明 |
|------|------|
| **Markdown → PDF** | 将 `.md`、README、技术文档、产品文档、研究简报转换为 A4 PDF |
| **品牌装点** | 在封面、页眉、页脚中加入团队名称、slogan、标题和日期 |
| **科技风样式** | 内置 `tech`、`deep-blue`、`cyan-violet`、`slate-minimal`、`bio-ai` 五套风格 |
| **可读性排版** | 优化标题层级、行距、页边距、表格、代码块、引用块和分页 |
| **中英文混排** | 支持中文/CJK 字体栈和中英文技术文档 |
| **引用标记** | 支持标准 Markdown 脚注，也能将 `[^\d]` 风格引用标记渲染为上标 |
| **HTML fallback** | PDF 依赖不可用时生成同样样式的 HTML，可用浏览器打印成 PDF |

<details>
<summary>样式参数 / Style options</summary>

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `--style` | `tech` | 默认科技蓝紫风 |
| `--style` | `deep-blue` | 更正式的深蓝工程风 |
| `--style` | `cyan-violet` | 更适合 AI、数据、模型平台文档 |
| `--style` | `slate-minimal` | 克制、低装饰的内部文档风 |
| `--style` | `bio-ai` | 适合 AI for Science、生物计算、药物研发等主题 |
| `--density` | `compact` | 长文档，压缩但保持可读 |
| `--density` | `normal` | 默认密度 |
| `--density` | `spacious` | 面向管理层或客户的宽松排版 |

</details>

## 独立脚本 / Standalone Script

`scripts/tech_markdown_to_pdf.py` 可以脱离 Agent 平台独立运行：

```bash
python scripts/tech_markdown_to_pdf.py input.md \
  --output output.pdf \
  --team-name "AI Science Team" \
  --slogan "From Markdown to Knowledge" \
  --style bio-ai \
  --density normal
```

常用命令：

```bash
python scripts/tech_markdown_to_pdf.py report.md --output report.pdf
python scripts/tech_markdown_to_pdf.py report.md --team-name "Research Ops" --slogan "Readable by design"
python scripts/tech_markdown_to_pdf.py report.md --style cyan-violet --density compact
python scripts/tech_markdown_to_pdf.py report.md --html-only
```

依赖说明：

- Python 3.10+
- `markdown`
- `pygments`
- `weasyprint`
- `pypdf`

脚本会在缺少 Python 包时尝试自动安装；如果系统缺少 WeasyPrint 运行库，则会保留 HTML 输出作为 fallback。

## 目录结构 / Structure

```text
markdown-to-pdf-tech/
├── SKILL.md                         # 技能入口，Agent 自动读取
├── scripts/
│   └── tech_markdown_to_pdf.py      # Markdown 转科技风 PDF/HTML 的独立脚本
├── references/
│   └── style-guide.md               # 视觉风格、配色和排版规范
├── requirements.txt                 # Python 依赖
├── LICENSE
└── README.md
```

## 适用边界 / Scope

适合：

- 技术方案、产品说明、研究简报、SOP、README、内部汇报材料
- 需要团队名称、slogan、页眉页脚和统一视觉风格的 PDF
- 中英文混排、表格较多、代码块较多的工程文档

不适合：

- 以幻灯片为主的演示稿 PDF
- 需要复杂交互或网页级动画的材料
- 需要严格出版社排版规范的书籍或论文终稿

## License

MIT

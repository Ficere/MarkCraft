# Bundled Icon Fonts

These font files are bundled so that status/symbol glyphs (✅ ❌ ⚠️ ⭐ ✓ ✗ ✔ ✘ etc.)
render as real icons in the generated PDF instead of missing-glyph "tofu" boxes.
WeasyPrint cannot rely on whatever fonts happen to be installed on the host, so the
glyphs are bound to these bundled fonts via `@font-face` in the generated HTML.

## Why these two fonts

- **Noto Sans Symbols 2** covers the line-art symbols: `✓ ✗ ✔ ✘ ⚠ ⭐ ☑ ☒ ►` and many
  geometric shapes. Its monochrome outlines blend cleanly with body text.
- **Noto Emoji** (the monochrome, *outline* emoji font — not the color bitmap
  `NotoColorEmoji`) covers the emoji-style status marks `✅` (U+2705) and `❌`
  (U+274C) that Symbols 2 does not. A monochrome outline font is used on purpose:
  WeasyPrint has no color-emoji (CBDT/COLR) rasterization pipeline, so a color
  emoji font would not render reliably in the PDF.

Together they give full coverage of the status icons this skill cares about, with
the symbol font preferred first and the emoji font as the fallback.

## Files & licenses

Both fonts are licensed under the **SIL Open Font License, Version 1.1 (OFL-1.1)**,
which explicitly permits bundling/redistribution (including alongside other
software) as long as the license text travels with the font and the fonts are not
sold on their own.

| File | Family | Source | License |
|------|--------|--------|---------|
| `NotoSansSymbols2-Regular.ttf` | Noto Sans Symbols 2 | google/fonts `ofl/notosanssymbols2` | OFL-1.1 (`OFL-NotoSansSymbols2.txt`) |
| `NotoEmoji-Regular.ttf` | Noto Emoji (monochrome, static Regular instance) | google/fonts `ofl/notoemoji` | OFL-1.1 (`OFL-NotoEmoji.txt`) |

`NotoEmoji-Regular.ttf` is a static `wght=400` instance produced from the upstream
variable font `NotoEmoji[wght].ttf` (via fontTools `instancer`) so it loads
predictably in WeasyPrint. The instancing does not change the license.

The full, unmodified OFL text for each font is included in this directory
(`OFL-NotoEmoji.txt`, `OFL-NotoSansSymbols2.txt`). The reserved font names and
copyright notices in those files are retained as required by the license.

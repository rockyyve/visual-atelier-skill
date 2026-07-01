# Static Style Presets

Use these six built-in styles for style selection and final generation. The style examples already exist in `assets/style-examples/`; show those static PNGs instead of generating per-request demos.

Each selected style must become a concrete `style-lock.md` and `visual-system.md` before final images are generated. Keep final in-image text short so the selected provider can produce polished native cards.

## 1. clean-lifestyle-guide

Best for: productivity, learning, creator workflow, light tutorial, broad save-worthy content.

- Mood: bright, breathable, practical, friendly.
- Palette: warm white `#fffdf8`, ink `#171717`, soft coral `#ff6b6b`, mint `#7ed9b5`, light yellow `#ffe8a3`.
- Layout: large title at top, central workflow/checklist illustration, 3-5 rounded blocks, soft footer note.
- Cover recipe: benefit-led title + "收藏向 / 新手友好" label + clean visual object + tiny preview chips.
- Final page inheritance: keep the friendly guide feel through rounded practical modules, soft highlight labels, a central explanatory object/flow, and a warm footer takeaway. Do not turn it into a sparse pastel report.
- Avoid: empty pastel backgrounds, decorative-only doodles, tiny body text.

## 2. signal-playbook

Best for: mistake correction, launch/deployment workflows, technical checklists, before/after decisions, actionable playbooks.

- Mood: decisive, modern, sharp, premium, high-signal.
- Palette: off-white `#f8f7f2`, ink `#111111`, signal red `#ef233c`, cobalt `#2563eb`, acid green `#b7f000`, graphite `#2f3437`.
- Layout: bold editorial headline slab, numbered command ribbons, diagnostic split panels, verification stamps, precise callout arrows, compact playbook modules, strong bottom action bar.
- Cover recipe: sharp benefit-led headline + one clear diagnostic contrast + 4-6 command steps + verification stamp.
- Final page inheritance: preserve the operation-playbook identity through headline slabs, numbered ribbons, diagnostic panels, stamps, arrows, and bottom action bars. Body pages should feel like high-signal field cards, not comic posters or neutral reports.
- Avoid: comic stickers, explosive bursts, childish doodles, generic dashboard panels, decorative code.

## 3. editorial-magazine

Best for: deep thinking, product analysis, brand-aware notes, course summaries, premium explainers.

- Mood: refined, calm, magazine-like, thoughtful.
- Palette: ivory `#f7f0e6`, charcoal `#222222`, wine red `#8a1538`, muted gold `#c6a15b`, pale gray `#ded8cf`.
- Layout: masthead, elegant large title, still-life or document composition, pull quote, two-column blocks.
- Cover recipe: title as primary subject + refined source objects such as notebook, spec sheet, UI wireframe, code page.
- Final page inheritance: preserve magazine identity with masthead/issue labels, editorial typography feel, source-object still life, pull quotes/captions, and refined two-column or framed modules. Do not turn it into a generic slide.
- Avoid: stock-photo atmosphere, overdecorated frames, unsupported luxury cues.

## 4. tech-dashboard

Best for: AI tools, coding tutorials, technical systems, workflow diagrams, data-heavy knowledge.

- Mood: precise, modern, structured, credible.
- Palette: near black `#080a0f`, cyan `#22d3ee`, violet `#8b5cf6`, lime `#a3e635`, soft white `#f8fafc`.
- Layout: top status bar, large title, module grid, code/spec panel, UI preview panel, bottom insight bar.
- Cover recipe: five-step workflow dashboard with readable nodes and controlled glow.
- Final page inheritance: preserve dashboard identity with status bars, code/build/preview/QA panels, system chips, connected workflow nodes, and bottom insight/status bars. Do not use plain white checklist cards unless styled as dashboard panels.
- Avoid: fake app screenshots, excessive glow, tiny code, visual clutter.

## 5. handdrawn-notebook

Best for: beginner-friendly explainers, learning notes, mental models, practical checklists.

- Mood: warm, approachable, handmade, clear.
- Palette: notebook cream `#fff7df`, pencil gray `#4b5563`, soft blue `#93c5fd`, grass green `#86efac`, red pen `#ef4444`.
- Layout: notebook paper, taped diagram, margin notes, numbered sticky notes, summary stamp.
- Cover recipe: handwritten-feeling big title + simple flow diagram + 4-8 practical questions/checkpoints.
- Final page inheritance: preserve notebook identity with paper lines, taped notes, numbered sticky checkpoints, hand-marked arrows/circles, margin notes, and stamp-like conclusions. Do not turn it into clean digital UI cards.
- Avoid: illegible handwriting, childish doodles, dense long paragraphs.

## 6. ai-tool-lab

Best for: Codex, Claude Code, AI Agent, MCP, Skills, AI workflows, automation, productized tool notes.

- Mood: clean technical magazine, Swiss grid, lab record, software product note.
- Palette: cold white `#f8fafc`, deep charcoal `#111827`, signal green `#16c653`, cyan `#38bdf8`, light gray `#e5e7eb`.
- Layout: lab label, huge title, central workflow cards, small experiment tags, qualitative benefit chips.
- Cover recipe: "AI TOOL LAB" header + big black/green title + five lab modules + bottom qualitative benefits.
- Final page inheritance: preserve lab identity with experiment labels, objective/evidence/insight sections, central workflow cards, verification chips, tool/model tags, and crisp Swiss-grid lab panels. Do not turn it into a generic SaaS dashboard.
- Avoid: fake percentages, KPI arrows, official-ad tone, large blank white areas.

## Style Selection Guidance

Recommend styles based on content:

- Broad how-to or productivity: `clean-lifestyle-guide`, `handdrawn-notebook`.
- Strong mistake correction or actionable workflow: `signal-playbook`.
- Reflective course or product design notes: `editorial-magazine`.
- Technical workflow: `tech-dashboard`, `ai-tool-lab`.
- AI tools, agents, plugins, skills: `ai-tool-lab` first, `tech-dashboard` second.

## Static Style Example Output

When the user has not specified a style, show the existing style examples and summarize them like this:

```markdown
1. clean-lifestyle-guide：适合...
2. signal-playbook：适合...
3. editorial-magazine：适合...
4. tech-dashboard：适合...
5. handdrawn-notebook：适合...
6. ai-tool-lab：适合...

请选择 1-6，我再按选定风格生成完整轮播。
```

Use Markdown image tags with absolute local paths to the corresponding files under `assets/style-examples/`. Do not call an image provider during this step.

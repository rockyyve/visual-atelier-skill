# Style Lock

Use this reference after the user chooses one of the static style examples or provides a custom style, and before creating `visual-system.md` or generating final images. The goal is to preserve the selected style identity and prevent the final image set from drifting into a generic exact-text template.

## Required Output

Create `style-lock.md` in the selected-style output folder before creating `visual-system.md` or generating final images.

It must include:

- Selected style slug and selected static style example path, or custom style brief.
- Output image set path.
- Visual promise: one sentence describing why this style fits the user's request.
- Locked traits: 6-10 concrete style features to preserve.
- Page inheritance rule: what every final page must repeat.
- Visual-system handoff: what `visual-system.md` must convert into executable page rules.
- Allowed simplifications for exact Chinese text.
- Forbidden drift: what would make the final cards fail.

## Style Lock Template

```markdown
# Style Lock

Selected style: {style slug}
Style reference: {assets/style-examples/style-0N-*.png or custom style brief}
Output image set: {selected-style}/

## Visual Promise

{What the selected style visually promises the user}

## Locked Traits

1. {composition trait}
2. {title/typography trait}
3. {graphic device trait}
4. {content module trait}
5. {texture/depth trait}
6. {CTA/footer trait}

## Page Inheritance Rule

Every final image must use at least 3 locked traits. A cover or first image should use at least 4 when the format includes one.

## Visual-System Handoff

`visual-system.md` must convert these locked traits into typography, layout, color-ratio, component, background, decoration, and footer/label rules before final images are generated.

## Allowed Simplifications

- Simplify tiny decorative details when needed for exact Chinese text.
- Replace unreadable imagegen text with controlled typography.
- Adapt module count to the source content.

## Forbidden Drift

- Palette-only inheritance.
- Generic report, dashboard, card, or checklist layout when the selected style promised a stronger visual language.
- Replacing the selected style's typography feel with neutral UI/system text.
- Letting final images look less refined than the selected style reference in typography, layout, color richness, or component craft.
- Removing the selected style's main graphic devices from final images.
- Huge blank lower areas or thin content modules.
```

## Style-Specific Locked Traits

Use these as a starting point, then refine them from the selected static example or custom style brief.

### clean-lifestyle-guide

- Bright warm-white field with soft coral/mint/yellow accents.
- Friendly large title with highlight marks, not corporate UI type.
- Rounded practical blocks, checklist flow, soft object illustration.
- Airy but not empty; content blocks occupy most of the canvas.
- Small friendly labels such as "收藏向" or "新手友好".
- Gentle footer note or save-worthy takeaway.

Forbidden drift: sterile SaaS dashboard, beige blank page, thin pastel cards without a central visual object.

### signal-playbook

- Bold editorial headline slab or heavy title block with clear command language.
- Off-white/ink foundation with signal red, cobalt, acid green, and graphite accents.
- Numbered command ribbons, step rails, diagnostic split panels, verification stamps, and precise callout arrows.
- Before/after, risk/fix, fail/pass, or decision/playbook structure.
- Compact high-signal modules that feel like field cards or operating instructions.
- Strong bottom action bar that states the next step or takeaway.

Forbidden drift: comic pop posters, explosive sticker clutter, neutral report/checklist layout, generic SaaS dashboard, or palette-only command cards without playbook devices.

### editorial-magazine

- Refined magazine masthead, issue label, section marker, or editorial grid.
- Elegant large title, serif/editorial feel, controlled spacing.
- Still-life/source objects: document stack, spec sheet, notebook, UI wireframe, code page.
- Pull quote, caption, two-column text, or framed editorial modules.
- Ivory/charcoal/wine/gold palette with tactile paper feel.
- Calm premium rhythm; fewer but better-composed modules.

Forbidden drift: generic business slide, dashboard panel, stock-photo mood with no article object.

### tech-dashboard

- Dark or near-dark technical canvas with status bars and system labels.
- Modular dashboard grid: code panel, build log, deployment status, preview window, QA checklist.
- Cyan/violet/lime highlights with controlled glow.
- Data/system hierarchy, terminal snippets, route/status chips, node connections.
- Dense but readable operational interface feel.
- Bottom insight/status bar.

Forbidden drift: simple white checklist page, fake decorative code, excessive neon blur, unsupported metrics.

### handdrawn-notebook

- Notebook paper, margin lines, taped cards, sticky notes, red-pen marks.
- Handwritten-feeling title and numbered learning checkpoints.
- Doodles or simple diagrams that explain the concept, not random decoration.
- Pencil/marker texture, stamps, circles, arrows, underlines.
- Warm beginner-friendly density with visible note-taking structure.
- Final takeaway written like a margin note or stamped conclusion.

Forbidden drift: clean digital cards, corporate checklist, illegible handwriting, childish unrelated doodles.

### ai-tool-lab

- Lab record / Swiss grid / software product note structure.
- Header label such as "AI TOOL LAB", experiment ID, objective, evidence, insight.
- Central workflow cards, model/tool labels, result states, verification chips.
- Cold white/deep charcoal/signal green/cyan palette.
- Crisp technical-magazine typography and modular lab panels.
- Evidence/experiment/checklist blocks tied to the current source.

Forbidden drift: generic dashboard, KPI marketing sheet, large blank white areas, fake percentages or official-ad tone.

## Final QA Questions

Before delivery, compare the selected style reference and final images:

- If colors were removed, would each final image still look like the selected style?
- Does each final image repeat at least 3 locked traits?
- Does the cover or first image repeat at least 4 locked traits when the format includes one?
- Were final images generated provider-native rather than flattened into deterministic templates?
- Would the user reasonably say the final images came from the selected style family?

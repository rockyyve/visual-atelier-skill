# Visual System

Use this reference after `style-lock.md` exists and before final images are generated. The goal is to keep the image set as refined as the selected static style example or generated cover instead of letting it collapse into generic report, dashboard, or checklist cards.

## Required Output

Create `visual-system.md` in the selected-style output folder before generating final images.

It must include:

- Style reference path or custom style brief.
- Generated cover / first image path, when one exists.
- Visual quality promise: one sentence describing the level of craft the final images must preserve.
- Typography system: title mood, title scale, body scale, emphasis treatment, and forbidden fallback fonts.
- Color system: background color or texture, dominant/accent/support ratios, contrast rules, and forbidden palette drift.
- Layout system: grid, title zone, content zone, evidence zone, bottom zone, margins, and spacing rhythm.
- Component vocabulary: allowed modules, cards, chips, dividers, callouts, arrows, stamps, labels, diagrams, or object frames.
- Background and texture rules.
- Footer or bottom-anchor rule.
- Image recipes: 3-6 reusable image patterns derived from the selected style.
- Provider prompt notes for turning the style system into final-image prompts.
- Visual downgrade traps.

## Template

```markdown
# Visual System

Style reference: {assets/style-examples/style-0N-*.png or custom style brief}
Generated cover / first image: {path if one exists}
Selected style: {style slug}

## Visual Quality Promise

Final images must look like the same designed series as the selected style reference, with no obvious drop in typography care, color richness, layout craft, or graphic detail.

## Typography System

- Main title: {font mood, weight, scale, line-height, decoration}
- Section title: {scale, weight, treatment}
- Body text: {scale, line-height, density}
- Emphasis: {highlight, underline, chip, stamp, bracket, cursor mark, etc.}
- Forbidden: {neutral system UI fallback / tiny report text / mismatched serif-sans mix}

## Color System

- Background: {color/texture}
- Dominant color: {rough percentage}
- Accent colors: {rough percentage and where used}
- Support neutrals: {rough percentage}
- Contrast rule: {how text remains readable}
- Forbidden drift: {washed-out palette / single-hue monotony / weak accents}

## Layout System

- Grid: {columns, alignment, rhythm}
- Title zone: {position and size}
- Content zone: {module pattern}
- Evidence/visual zone: {diagram/object/panel pattern}
- Bottom zone: {CTA/status/takeaway pattern}
- Margins and spacing: {outer margin, gap rhythm}

## Component Vocabulary

- {component 1}: {shape, border, fill, shadow/texture}
- {component 2}: {shape, border, fill, shadow/texture}
- {component 3}: {shape, border, fill, shadow/texture}
- Decorative devices: {arrows, stamps, stickers, marks, nodes, frames}

## Image Recipes

1. {recipe for framework page}
2. {recipe for step/process page}
3. {recipe for comparison/risk page}
4. {recipe for checklist/CTA page}

## Provider Prompt Notes

- Generate final images directly with the selected image provider.
- Reuse the same title treatments, module shapes, accent colors, texture, visual metaphor, and footer/label system on every image.
- Keep in-image Chinese text short: one title, one subtitle, and 2-4 short labels or bullets.
- Put exact long copy in `note-package.md`, `post-copy.md`, or `image-set-package.md`, not in the image.
- Do not translate this visual system into an HTML/CSS renderer unless the user explicitly requests exact-text screenshots.

## Visual Downgrade Traps

- Final images use only the style palette while switching to generic cards.
- Font becomes neutral UI text with no title treatment.
- Accent colors become timid or disappear from final images.
- Modules become evenly spaced report boxes instead of style-specific components.
- Background texture, object metaphor, decorative marks, or footer rhythm disappear.
- Final images have less visual density or weaker hierarchy than the style reference.
```

## Final Image Standard

Each final image must use at least 5 concrete rules from `visual-system.md`:

- 1 typography rule.
- 1 color ratio or accent-placement rule.
- 1 layout/grid rule.
- 1 component vocabulary rule.
- 1 background, decorative, or footer rule.

If the page would still look generic after removing colors, it fails.

## Text Handling Rule

Exact Chinese text is important, but it is not permission to downgrade the visual design.

- Keep in-image text short enough for the selected image provider to render cleanly.
- Use concise labels, title phrases, checklist nouns, status chips, and 2-4 short bullets.
- Put exact full wording in the Markdown companion document.
- If generated text is slightly imperfect but the visual card is strong, regenerate with shorter text.
- Do not switch to HTML/CSS/canvas just to repair small text errors.

## Final QA Question

Before delivery, compare every image with the selected style reference and generated cover when one exists:

```text
如果这张图和选定风格样张放在同一组作品里，用户会觉得它们是同一个设计师做的吗？
```

If the honest answer is no, regenerate the image with the selected provider.

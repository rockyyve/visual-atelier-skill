# Rendering And QA

Use this reference before exporting final images or declaring an image package complete.

## Style Selection Rules

- Use the static examples in `assets/style-examples/` as the selection surface.
- Do not generate demo images, contact sheets, `demo-overview.png`, or per-request style previews by default.
- Do not present cached style examples as if they are content-specific demos. They are reusable style samples.
- If the user asks for fresh visual exploration, treat it as an explicit exception and record it in `generation-record.md`.

## Generation Strategy

- Generate final images with the selected provider by default.
- Do not create `render-final.js`, `render.html`, Playwright screenshots, canvas exports, or template-rendered final cards unless the user explicitly asks for exact-text screenshots.
- If exact Chinese text matters, shorten the text shown in the image and put precise long wording in the companion Markdown document.
- If using ZenMux, pass the selected static style example as a reference image when useful for preserving style.
- Record provider, model, dimensions, selected style, reference images, and exceptions in `generation-record.md`.

## Canvas Rules

- Use the user's requested dimensions. For Xiaohongshu notes, default to `1080 x 1350`.
- Do not solve off-ratio output by letterboxing, pillarboxing, blur-fill, decorative frames, or padding.
- If a provider output is off-ratio, regenerate or crop only when the crop preserves the whole designed card without letterboxing or padding.

## Layout Density

- Use a top title/identity zone, middle content zone, and bottom information anchor on every image unless the user's format calls for another structure.
- Real content should occupy roughly 70%-86% of the canvas height.
- Do not leave a continuous blank lower area larger than 160px on vertical social cards.
- If content is thin, add one of: why it matters, how to judge, next step, common mistake, example, applicable scenario.

## Style Inheritance

- Palette is not enough. Final images must reuse the selected style's composition logic, typography feel, graphic devices, component shapes, and content density.
- Each final image must show at least 3 locked traits from `style-lock.md` and at least 5 concrete rules from `visual-system.md`.
- Use `style-lock.md` to decide whether the image should be poster-like, magazine-like, dashboard-like, notebook-like, lab-like, or lifestyle-guide-like.
- Use `visual-system.md` to implement typography, color ratio, module shape, background treatment, decorative density, and footer/label rhythm.
- If an image looks publishable but no longer looks like the selected style family, it fails QA.

## Typography

For 1080 x 1350 social cards, use these floors:

| Element | Recommended | Absolute floor |
| --- | ---: | ---: |
| Cover title | 82-104px | 76px |
| Content page title | 60-76px | 56px |
| Subtitle / lede | 34-44px | 32px |
| Card title | 38-48px | 36px |
| Card body | 32-40px | 32px |
| Code / directory | 28-34px | 28px |
| Table body | 30-36px | 30px |
| Bottom takeaway | 32-40px | 32px |
| Pill / tag | 24-30px | 22px |

Scale proportionally for other dimensions. Never use tiny UI text for real card content.

## QA Checklist

- Static style examples contain exactly six PNG files named `style-01-...png` through `style-06-...png`.
- Final PNG count matches the user's requested count.
- Final PNG dimensions match the user's requested dimensions, or `1080 x 1350` for default Xiaohongshu notes.
- Final package contains `style-lock.md`.
- Final package contains `visual-system.md`.
- Xiaohongshu note packages contain `note-package.md`; general image sets contain `image-set-package.md`.
- `generation-record.md` names the image provider (`imagegen` or `zenmux`) and model when available.
- Final images are provider-native outputs unless `generation-record.md` records an explicit user request for exact-text screenshots.
- Every image has one visual focus.
- The selected style is consistent across all final images.
- No unsupported metrics, fake logos, fake official branding, watermarks, celebrity likenesses, or ungrounded claims.
- Technical content is believable and not decorative filler.
- Text is large enough for mobile reading when the output is a social card.
- No important content is clipped, occluded, or too close to edges.
- Final response reports validation results.

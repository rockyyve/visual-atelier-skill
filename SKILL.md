---
name: visual-atelier
description: "Use when the user asks for style-based image generation, image sets, social cards, carousels, posters, covers, or a specified number of generated images from given content, style, and dimensions. Supports 指定风格, 指定尺寸, 指定数量, 封面图, 轮播图, 海报卡片, 小红书图片笔记, and provider-native image generation with ZenMux or imagegen."
---

# Visual Atelier

Turn source material or direct image requirements into a refined provider-native PNG image set. The skill supports general requests such as "use this style, this size, this content, make N images"; Xiaohongshu notes are one supported social-card use case, not the skill boundary.

## Core Contract

- Do not generate style demo images by default. Use the static high-fidelity style examples in `assets/style-examples/` as the style selection surface.
- Show the static style examples first when the user has not already specified a style. Ask the user to choose by number or slug before generating final images.
- If the user already specifies a style, skip the style menu and proceed with that style.
- If the user gives a custom style not covered by the examples, write a concise style brief and ask only if the style is ambiguous.
- Support arbitrary final image dimensions and counts. For Xiaohongshu image notes, default to `1080 x 1350` and 4:5 vertical when the user does not specify size.
- Support image provider selection. Use `zenmux` only when `ZENMUX_API_KEY` is present and `scripts/zenmux_generate_image.py --check` passes; otherwise use built-in `imagegen`, unless the user explicitly chooses a provider.
- Never paste or store API keys in output files. Read keys from environment variables only.
- For ZenMux, default to OpenAI SDK-compatible base URL `https://zenmux.ai/api/v1` and model `openai/gpt-image-2`, unless `ZENMUX_BASE_URL`, `ZENMUX_IMAGE_MODEL`, or `ZENMUX_IMAGE_SIZE` override the defaults. ZenMux requires the local OpenAI SDK path; do not fall back to raw HTTP.
- Generate final images with the selected image provider by default. Do not use local HTML/CSS/Playwright rendering unless the user explicitly requests exact-text screenshots and accepts the possible visual downgrade.
- Keep one visual system across the final image set. Do not mix multiple built-in styles in one set unless the user explicitly asks for mixed styles.
- Create `style-lock.md` and `visual-system.md` before final generation. They should be based on the selected static style example or the user's custom style brief.
- For Xiaohongshu notes, create `note-package.md` and usually `post-copy.md`. For general image sets, create `image-set-package.md` instead.

## Workflow

1. **Load references only as needed.**
   - Read `references/style-presets.md` before showing style options or applying a selected style.
   - Read `references/image-providers.md` before generating final images, especially when ZenMux is configured or requested.
   - Read `references/article-parsing.md` when the source is long, messy, multi-format, or not already split into image roles.
   - Read `references/style-lock.md` and `references/visual-system.md` after style selection and before final generation.
   - Read `references/cover-design.md` for Xiaohongshu covers or any request that needs a first/cover image.
   - Read `references/publishing-copy.md` only when the output includes Xiaohongshu publishing copy.
   - Read `references/rendering-and-qa.md` before validating final assets.

2. **Parse the user's image request.**
   - Extract: purpose/platform, source content, target audience, image count, dimensions, aspect ratio, style, provider, output folder, and whether publishing copy is needed.
   - If the request is a Xiaohongshu note and count is unspecified, choose 5-8 pages for most knowledge/tutorial notes, 3-5 for quick tips, and 8-12 for full guides.
   - If the request is a general image set and count or dimensions are missing, infer only when the intent is obvious; otherwise ask a short clarifying question.
   - Preserve claims. Do not invent metrics, testimonials, product facts, logos, screenshots, or official endorsements.

3. **Show static style examples instead of generating demos.**
   - Use the six files in `assets/style-examples/`:
     - `style-01-clean-lifestyle-guide.png`
     - `style-02-signal-playbook.png`
     - `style-03-editorial-magazine.png`
     - `style-04-tech-dashboard.png`
     - `style-05-handdrawn-notebook.png`
     - `style-06-ai-tool-lab.png`
   - Present them as existing high-fidelity examples. Do not call any image provider during style selection.
   - Do not create `demo-overview.png`, contact sheets, generated demo covers, or per-request style previews unless the user explicitly asks for new explorations.
   - After showing the examples, stop and ask the user to choose a style if no style was specified.

4. **Lock the selected style.**
   - Create `style-lock.md` in the output folder or selected-style subfolder.
   - Record selected style slug, selected style example path or custom style brief, visual promise, locked traits, page/image inheritance rules, and forbidden drift.
   - Create `visual-system.md` from the style lock. Translate the selected style into typography mood, color ratios, layout rhythm, component shapes, background treatment, graphic devices, and footer/label rules.

5. **Plan the final image set.**
   - For Xiaohongshu notes: plan cover, body pages, and CTA/summary page; write short in-image text and exact companion copy.
   - For general image sets: plan one role per image, exact dimensions, required text, subject matter, composition, and any sequence logic.
   - Use short in-image text. Put exact long copy in `note-package.md`, `post-copy.md`, or `image-set-package.md`.

6. **Generate final images with the selected provider.**
   - Use the selected provider for every final image.
   - Before choosing ZenMux, run `python3 scripts/zenmux_generate_image.py --check`. If it fails because the OpenAI SDK is missing, use `imagegen` unless the user explicitly requires ZenMux.
   - If ZenMux returns `403 Forbidden`, record the failure in `generation-record.md` and fall back to `imagegen` unless the user explicitly requires ZenMux. Do not retry the same ZenMux request repeatedly.
   - If using ZenMux, prefer `scripts/zenmux_generate_image.py --image assets/style-examples/style-0N-*.png ...` when the static style example can help preserve style. Add user-provided reference images with additional `--image` arguments when relevant.
   - If using imagegen, carry the selected style example's visual traits into the prompt.
   - For Xiaohongshu notes, export as `01-cover.png`, `02-{role}.png`, etc.
   - For general image sets, export as `01-{role}.png`, `02-{role}.png`, etc.
   - Regenerate images that fail dimensions, major content requirements, style consistency, readability, or claim safety.

7. **Write the companion document.**
   - Xiaohongshu note: save `note-package.md`; create `post-copy.md` when publication copy should be separate.
   - General image set: save `image-set-package.md` with original request, selected style, dimensions, count, per-image role, prompt summary, text used, output list, and provider/model.
   - Always create `generation-record.md` with provider, model, dimensions, selected style, reference images used, and any fallback or regeneration notes. Never include secrets.

8. **Validate before delivery.**
   - Validate static style examples after skill changes:
     ```bash
     python3 scripts/validate_package.py assets/style-examples --style-examples-set
     ```
   - Validate Xiaohongshu final packages:
     ```bash
     python3 scripts/validate_package.py <output-dir> --width 1080 --height 1350
     ```
   - Validate general image sets:
     ```bash
     python3 scripts/validate_package.py <output-dir> --general-image-set --width {width} --height {height}
     ```
   - Inspect final images for text overflow, blank lower halves, style drift, unsupported claims, fake logos, watermarks, template sameness, and incorrect dimensions.

## Default Output Structures

For Xiaohongshu notes:

```text
outputs/xhs-note-{YYYY-MM-DD}-{slug}/
  {selected-style}/
    style-lock.md
    visual-system.md
    01-cover.png
    02-{role}.png
    ...
  note-package.md
  post-copy.md
  generation-record.md
```

For general image sets:

```text
outputs/image-set-{YYYY-MM-DD}-{slug}/
  {selected-style}/
    style-lock.md
    visual-system.md
    01-{role}.png
    02-{role}.png
    ...
  image-set-package.md
  generation-record.md
```

If the user specifies an output folder, use it.

## Style Selection Response

When the user has not chosen a style, show the six static examples with image links and short guidance:

```markdown
下面是内置高保真风格样张，请选 1-6：

1. clean-lifestyle-guide：适合效率、学习、清单、轻教程。
   ![clean-lifestyle-guide](/absolute/path/assets/style-examples/style-01-clean-lifestyle-guide.png)
2. signal-playbook：适合技术流程、排错、部署、行动手册。
   ![signal-playbook](/absolute/path/assets/style-examples/style-02-signal-playbook.png)
3. editorial-magazine：适合深度思考、产品分析、高级感内容。
   ![editorial-magazine](/absolute/path/assets/style-examples/style-03-editorial-magazine.png)
4. tech-dashboard：适合 AI 工具、代码教程、系统流程、数据面板。
   ![tech-dashboard](/absolute/path/assets/style-examples/style-04-tech-dashboard.png)
5. handdrawn-notebook：适合新手科普、学习笔记、心智模型。
   ![handdrawn-notebook](/absolute/path/assets/style-examples/style-05-handdrawn-notebook.png)
6. ai-tool-lab：适合 Codex、Agent、MCP、Skills、AI 工作流。
   ![ai-tool-lab](/absolute/path/assets/style-examples/style-06-ai-tool-lab.png)

请选择风格编号或 slug，我再按你的内容、尺寸和数量生成最终图片。
```

Use absolute local paths in Markdown image tags so the app can render them.

## Final Image Prompt Shape

Use this prompt shape for each final image:

```text
Use case: {social-card / infographic-diagram / poster / product-card / custom}
Asset type: provider-native PNG image {N} of {total}
Provider: {imagegen / zenmux}
Dimensions: {width} x {height}
Selected style: {style slug or custom style name}
Style reference: {static example path or custom style brief}
Style lock: {3-6 required visual traits from style-lock.md}
Visual system: {5-8 executable rules from visual-system.md}
Image role: {cover / framework / steps / comparison / checklist / CTA / custom role}
Content source: {short factual summary}
Short in-image text:
Title: "{title}"
Subtitle: "{subtitle}"
Bullets or labels: "{item 1}" / "{item 2}" / "{item 3}"
Composition: {specific layout instructions from selected style, not a generic template}
Craft requirement: preserve style-level typography care, color richness, component shapes, decoration density, and readable hierarchy.
Text handling: use short phrases only; exact long wording goes in the companion Markdown document.
Constraints: provider-native final image, no watermark, no fake data, no unsupported claims, no fake logos, no palette-only style inheritance, no HTML/CSS template look.
```

If the provider does not preserve exact text, shorten the in-image wording and regenerate. Do not switch to HTML/CSS just to repair small text errors unless the user explicitly requested exact-text screenshots.

## Handoff

Final responses should list:

- Selected style.
- Image provider and model.
- Output folder.
- Final dimensions and image count.
- Final PNG paths.
- `style-lock.md` path.
- `visual-system.md` path.
- Companion Markdown path.
- Recommended title and publishing hook when it is a Xiaohongshu note.
- Validation result.

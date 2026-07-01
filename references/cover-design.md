# Cover Design

Use this reference after the user chooses a style and before generating a Xiaohongshu cover or any first image that functions as a cover.

This guidance adapts the useful parts of `oil-cover`: one-glance subject, content attribution, clean evidence, strong title hierarchy, and no local post-generation repair.

## Required Output

- Generate the cover or first image as a final provider-native image after style selection.
- Do not promote a static style example to `01-cover.png`; style examples are only references.
- Do not generate pages `02+` until the cover exists and passes QA when the request is a Xiaohongshu note or cover-led carousel.
- Use the cover's actual generated visual system, plus `style-lock.md`, as the source of truth for remaining pages.

## Cover Goal

Before generating the cover, answer:

```text
这张封面 0.5 秒内要让读者看到什么结果？
```

That answer is the one-glance subject. The cover title, visual evidence, and decorative chips must serve it.

## Source Attribution

Decide these before generation:

- Main topic.
- Main product/tool/workflow, if any.
- Host interface or evidence source, if any.
- Supporting brands, only if the source explicitly discusses them.

Do not bring in historical product names, previous labels, old color schemes, unrelated logos, or stale keywords.

## Title Rules

- Make the title the first visual anchor.
- Use a short benefit-led title, not a generic topic label.
- Prefer 4-10 Chinese characters for the strongest title phrase when possible.
- Add intentional line breaks. Avoid single-character orphan lines.
- Use one restrained emphasis treatment for the key word: soft highlight, underline, small status chip, bracket, cursor mark, or serif/English accent.
- Do not use hashtags, clickbait punctuation, fake urgency, or unsupported claims.

## Visual Evidence

Use source-specific evidence or a source-specific metaphor:

- Product/workflow screenshot, if available and relevant.
- Code/terminal/spec/worktree/browser verification objects for technical tutorials.
- Checklist, flow diagram, result gallery, comparison card, or document stack when there is no screenshot.
- For AI-tool content, show the real workflow concept: prompt, spec, UI concept, build, browser verification, model/tool labels, or result state.

Distill evidence. Do not paste a raw full screenshot full of sidebars, long text, timestamps, paths, notifications, avatars, or irrelevant UI.

## Composition

- Use the user's requested canvas. For Xiaohongshu, default to `1080 x 1350`.
- The cover should feel like a complete first card, not a title slide.
- Title is the first anchor; source evidence or metaphor is the second anchor.
- Use the selected style's palette, typography, layout rhythm, and visual metaphor.
- Add 1-2 content-related decorations only when they help comprehension.
- Keep phone-feed readability for social cards: big title, clear hierarchy, no tiny dense paragraphs.

## No Local Repair

The cover should be generated as one complete provider-native image. Do not fix a weak cover by locally pasting text, logo, stickers, or frames afterward.

If exact Chinese text is too long for the provider, shorten the in-image wording and put the precise long copy in `note-package.md` or `image-set-package.md`. Do not switch to HTML/CSS just to repair a cover unless the user explicitly requests an exact-text rebuilt variant.

## Cover Prompt Checklist

Prompt must include:

- `Use case: ads-marketing` or `infographic-diagram`, depending on cover style.
- Asset type: `{platform or purpose} cover / first image`.
- Requested dimensions.
- Selected style slug and static style example path or custom style brief.
- One-glance subject.
- Exact short title and intended line breaks.
- Optional subtitle.
- Source-specific evidence/metaphor.
- Composition plan.
- Title decoration plan.
- Avoid list.

## Cover QA

Reject and regenerate a cover if:

- It looks like a generic template unrelated to the source.
- The title is not the strongest visual element.
- The title has awkward orphan-character line breaks.
- The visual evidence is tiny, decorative, or unrelated.
- It invents metrics, badges, logos, screenshots, or claims.
- It contains people, avatars, watermarks, hashtags, or unrelated brand marks.
- It ignores the selected style.
- It requires local patching to look complete.

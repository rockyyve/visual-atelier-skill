# Article Parsing

Use this reference when the source is not already a clean page-by-page carousel plan.

## Supported Source Shapes

- Markdown articles with headings, lists, tables, frontmatter, or code blocks.
- Plain text essays, messy notes, chat transcripts, outlines, or pasted fragments.
- Technical tutorials, tool reviews, workflow notes, product docs, course notes, and personal experience posts.
- Mixed Chinese/English content.

## Extraction Order

1. Topic: infer from title, frontmatter, first paragraph, repeated nouns, or final takeaway.
2. Reader: infer who benefits from the material.
3. Core value: what the reader can do better after saving the post.
4. Hook: strongest Xiaohongshu cover angle, preferably a concrete pain point or outcome.
5. Must-keep facts: names, claims, code details, dates, product constraints, warnings.
6. Image roles: map source sections into a carousel, social-card sequence, or general image set.

## Page Count Heuristics

| Source type | Pages | Structure |
| --- | ---: | --- |
| Quick tip | 3-5 | Cover, tip list, example, CTA |
| Knowledge card | 3-6 | Cover, concept, comparison/checklist, summary |
| Tool recommendation | 5-8 | Cover, pain point, feature, scenario, workflow, CTA |
| Technical tutorial | 6-10 | Cover, context, steps, example, pitfall, checklist |
| Full guide | 8-12 | Cover, overview, chapter breakdown, examples, checklist, CTA |

## Format Handling Rules

- Headings become candidate page titles, not mandatory pages.
- Lists become step cards, checklist cards, comparison rows, or module grids.
- Tables become comparison pages or decision guides.
- Code blocks become short code excerpts, command cards, directory panels, or "what this code does" summaries. Do not paste long code into a card.
- Quotes become pull quotes only if they are central to the argument.
- Frontmatter and metadata can inform topic, tags, and source, but should not appear verbatim in cards unless useful to readers.
- If the source is too long, summarize into 5-8 core page roles before drafting page text.
- If the source is scattered, first group it into: problem, method, example, checklist, conclusion.

## Rewrite Rules

- Make cover titles benefit-led, not topic labels.
- Use short Chinese lines designed for mobile scanning.
- Keep one idea per page.
- Prefer concrete nouns and verbs over broad abstractions.
- Do not invent numbers or guarantee outcomes.
- If a source contains unsupported metrics, either cite them as source claims or remove them.

## Content Plan Output

Before style selection or final generation, produce this internal plan:

```markdown
主题：
目标读者：
核心价值：
内容类型：
推荐页数：
封面 hook：
必须保留：
页面大纲：
1. 封面：...
2. ...
```

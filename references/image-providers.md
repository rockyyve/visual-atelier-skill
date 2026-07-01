# Image Providers

Use this reference before generating final images.

## Provider Selection

- First honor explicit user choice: use `imagegen` when the user asks for it, and use `zenmux` when the user asks for it.
- If no provider is specified, check whether ZenMux is usable before defaulting to `imagegen`.
- Treat ZenMux as usable only when `ZENMUX_API_KEY` is present in the process environment and `scripts/zenmux_generate_image.py --check` passes.
- Use `zenmux` when it is usable. Use `imagegen` when ZenMux is not usable, when the user explicitly asks for built-in image generation, or when ZenMux fails with an account/model permission error.
- Do not switch providers inside one final image set unless the user asks or the provider fails.
- If ZenMux fails with missing SDK or `403 Forbidden`, record the failure and fall back to `imagegen` unless the user explicitly required ZenMux.

## Secrets

- Never paste API keys into prompts, Markdown outputs, logs, screenshots, or `generation-record.md`.
- Read API keys from environment variables only.
- For ZenMux, use:
  - `ZENMUX_API_KEY`: required.
  - `ZENMUX_BASE_URL`: optional; defaults to `https://zenmux.ai/api/v1`.
  - `ZENMUX_IMAGE_MODEL`: optional; defaults to `openai/gpt-image-2`.
  - `ZENMUX_IMAGE_SIZE`: optional; defaults to `1024x1024` because this is the documented example size.
  - `ZENMUX_PROVIDER_CLIENT`: optional; `auto` by default. `auto` uses ZenMux REST endpoints, matching the proven `oil-cover` skill path. Set `openai` only when you explicitly want the OpenAI SDK-compatible client.
  - `ZENMUX_PROXY`: optional; proxy override for the OpenAI SDK-compatible client.

ZenMux can be called through REST endpoints or the OpenAI SDK-compatible client. This skill defaults to the REST path because it matches the working `oil-cover` implementation:

- generation maps to `POST /images/generations`
- reference-image editing maps to multipart `POST /images/edits`
- if `/images/edits` returns `403 access_denied`, the script falls back to `/images/generations` without uploading reference images, unless `--no-generation-fallback` is used

## ZenMux Checklist

Before calling ZenMux:

- Confirm `ZENMUX_API_KEY` is available in the environment.
- If using `scripts/zenmux_generate_image.py`, make sure `ZENMUX_API_KEY` is already exported in the shell or process environment.
- Run `python3 scripts/zenmux_generate_image.py --check` before selecting ZenMux. This checks the local key and selected local client without making a network request.
- Use the default REST client unless there is a specific reason to test the OpenAI SDK-compatible client with `--provider-client openai`.
- Use model `openai/gpt-image-2` unless `ZENMUX_IMAGE_MODEL` is set.
- Use size from `ZENMUX_IMAGE_SIZE` when set, otherwise request the closest provider-supported size. If the target size is not directly supported, prompt for a center-safe composition so the image can be cropped/resized without cutting important text.
- Use the same prompt structure as the built-in image provider.
- Keep image text short and put exact long copy in the companion Markdown document.
- For final images, pass the selected static style example, generated cover, or user-provided reference image with `--image` when available. This helps preserve typography mood, layout language, color richness, and graphic devices across the set.
- Use multiple `--image` arguments when combining a selected cover with additional source/reference pictures.
- If reference-image editing fails with `403 access_denied`, let the script fall back to generation-only mode before falling back to `imagegen`.

## ZenMux Script Usage

Prefer `scripts/zenmux_generate_image.py` when available so the response is saved consistently and secrets are not printed.

Environment check:

```bash
python3 scripts/zenmux_generate_image.py --check
```

Generation:

```bash
python3 scripts/zenmux_generate_image.py \
  --prompt-file prompts/page-02.md \
  --out selected-style/02-framework.png
```

Reference-image editing or style carryover:

```bash
python3 scripts/zenmux_generate_image.py \
  --image assets/style-examples/style-06-ai-tool-lab.png \
  --prompt-file prompts/page-02.md \
  --out selected-style/02-framework.png
```

Multiple references:

```bash
python3 scripts/zenmux_generate_image.py \
  --image assets/style-examples/style-06-ai-tool-lab.png \
  --image references/product-shot.png \
  --prompt-file prompts/page-03.md \
  --out selected-style/03-example.png
```

Force generation-only mode when the account or model cannot access `/images/edits`:

```bash
python3 scripts/zenmux_generate_image.py \
  --generation-only \
  --prompt-file prompts/page-03.md \
  --out selected-style/page-03.png
```

The script supports:

- `/images/generations` when no `--image` is provided or `--generation-only` is used.
- `/images/edits` when one or more `--image` references are provided.
- automatic `/images/edits` 403 fallback to `/images/generations`.
- `--provider-client auto|rest|openai`.
- `--size`; passed to both generation and editing.

## Raw ZenMux Request Shape

The normal workflow uses REST calls through the bundled Python script. This mirrors `oil-cover` and avoids depending on the OpenAI SDK for the default path.

Generation shape:

```bash
curl https://zenmux.ai/api/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZENMUX_API_KEY" \
  -d '{
    "model": "openai/gpt-image-2",
    "prompt": "...",
    "n": 1,
    "size": "1024x1024"
  }'
```

OpenAI SDK-compatible generation, optional debugging path only:

```python
import base64
from openai import OpenAI

client = OpenAI(base_url="https://zenmux.ai/api/v1", api_key="<ZENMUX_API_KEY>")
img = client.images.generate(
    model="openai/gpt-image-2",
    prompt="...",
    n=1,
    size="1024x1024",
)

image_bytes = base64.b64decode(img.data[0].b64_json)
```

OpenAI SDK-compatible editing, optional debugging path only:

```python
result = client.images.edit(
    model="openai/gpt-image-2",
    image=[open("cover.png", "rb"), open("reference.png", "rb")],
    prompt="...",
    size="1024x1024",
)

image_bytes = base64.b64decode(result.data[0].b64_json)
```

## Generation Record

Record provider details without secrets:

```markdown
## Image Provider

- Provider: zenmux
- Base URL: `https://zenmux.ai/api/v1`
- Operation: `images.generate` or `images.edit`
- Model: {ZENMUX_IMAGE_MODEL or `openai/gpt-image-2`}
- Requested size: {ZENMUX_IMAGE_SIZE or `1024x1024`}
- API key: read from `ZENMUX_API_KEY`, not stored
- Reference images: {none / selected cover / source images}
- Output size: {requested width}x{requested height}
- Final images: generated with zenmux
```

If ZenMux fails:

```markdown
## Image Provider Failure

- Provider attempted: zenmux
- Failure: {missing OpenAI SDK / HTTP 403 Forbidden / model permission / other}
- Action: fell back to imagegen
- Secrets: not logged
```

For built-in generation:

```markdown
## Image Provider

- Provider: imagegen
- Output size: {requested width}x{requested height}
- Final images: generated with imagegen
```

## Provider-Native Final Rule

Final images should come directly from the selected image provider. Do not create HTML/CSS/Playwright-rendered final images unless the user explicitly requests an exact-text screenshot variant.

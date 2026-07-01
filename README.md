# Visual Atelier Skill

Visual Atelier is a Codex skill for creating refined, style-led image sets from source material or direct image requirements.

It supports:

- static high-fidelity style selection before generation
- provider-native image generation with `imagegen` or ZenMux
- arbitrary image counts and dimensions
- social cards, posters, covers, carousels, and Xiaohongshu image notes
- companion package documents for generated image sets

## What Makes It Different

Visual Atelier does not generate fresh demo images for every request. Instead, it ships with six reusable high-fidelity style examples in `assets/style-examples/`. A user chooses a style first, then the skill generates the final image set with a consistent visual system.

## Included Styles

1. `clean-lifestyle-guide`
2. `signal-playbook`
3. `editorial-magazine`
4. `tech-dashboard`
5. `handdrawn-notebook`
6. `ai-tool-lab`

## Structure

```text
visual-atelier-skill/
  SKILL.md
  agents/openai.yaml
  assets/style-examples/
  references/
  scripts/
```

## Installation

Copy this repository folder into your Codex skills directory:

```bash
cp -R visual-atelier-skill ~/.agents/skills/visual-atelier
```

Then invoke it as:

```text
$visual-atelier
```

## ZenMux

ZenMux support is optional. If used, configure the API key as an environment variable:

```bash
export ZENMUX_API_KEY="..."
```

The key must not be committed to the repository.

Check local ZenMux readiness without a network request:

```bash
python3 scripts/zenmux_generate_image.py --check
```

If the check says `OpenAI SDK is required for ZenMux`, install the OpenAI Python SDK into the same Python environment that runs the script:

```bash
python3 -m pip install openai
```

Then verify that the active `python3` can import it:

```bash
python3 -c "import openai; print(openai.__version__)"
python3 scripts/zenmux_generate_image.py --check
```

If you use `pyenv`, Conda, or another Python manager, first confirm which interpreter Codex is using:

```bash
which python3
python3 -c "import sys; print(sys.executable)"
```

Install `openai` with that same interpreter. Installing the package into a different Python environment will not fix the ZenMux readiness check.

## Validation

Validate the bundled style examples:

```bash
python3 scripts/validate_package.py assets/style-examples --style-examples-set
```

Validate a general image set:

```bash
python3 scripts/validate_package.py <output-dir> --general-image-set --width 1080 --height 1350
```

## License

MIT

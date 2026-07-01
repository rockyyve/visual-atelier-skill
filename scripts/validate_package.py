#!/usr/bin/env python3
"""Validate a styled image-set output package."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1350
OVERVIEW_NAME = "demo-overview.png"
REQUIRED_STYLE_EXAMPLE_PREFIXES = (
    "style-01-",
    "style-02-",
    "style-03-",
    "style-04-",
    "style-05-",
    "style-06-",
    "style-07-",
    "style-08-",
)


def read_size(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width = height = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("pixelWidth:"):
            width = int(line.split(":", 1)[1].strip())
        elif line.startswith("pixelHeight:"):
            height = int(line.split(":", 1)[1].strip())
    if width is None or height is None:
        raise ValueError(f"Could not read dimensions for {path}")
    return width, height


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--allow-demos-only", action="store_true")
    parser.add_argument("--demo-set", action="store_true")
    parser.add_argument("--style-examples-set", action="store_true")
    parser.add_argument("--general-image-set", action="store_true")
    parser.add_argument(
        "--allow-controlled-renderer",
        action="store_true",
        help="Allow exact-text HTML/CSS/canvas renderer artifacts when the user explicitly requested them.",
    )
    parser.add_argument(
        "--require-imagegen-record",
        action="store_true",
        help="Require generation-record.md to mention a supported image provider.",
    )
    args = parser.parse_args()
    examples_only = args.allow_demos_only or args.style_examples_set

    output_dir = args.output_dir
    if not output_dir.exists() or not output_dir.is_dir():
        print(f"Output directory not found: {output_dir}", file=sys.stderr)
        return 2

    pngs = sorted(output_dir.rglob("*.png"))
    if not pngs:
        print("No PNG files found.", file=sys.stderr)
        return 2

    failures: list[str] = []
    overview_path = output_dir / OVERVIEW_NAME

    if args.demo_set:
        demo_pngs = sorted(
            path
            for path in output_dir.glob("demo-[0-9][0-9]-*.png")
            if path.name != OVERVIEW_NAME
        )
        if len(demo_pngs) != 6:
            failures.append(f"Demo set must contain exactly 6 demo-*.png files, found {len(demo_pngs)}")
        for index in range(1, 7):
            prefix = f"demo-{index:02d}-"
            if not any(path.name.startswith(prefix) for path in demo_pngs):
                failures.append(f"Missing demo file with prefix {prefix}")
        suspicious_scripts = [
            "render-demos.js",
            "generate-demos.js",
            "demo-render.js",
            "render-demo.js",
        ]
        script_search_roots = [output_dir, output_dir.parent]
        for root in script_search_roots:
            for script_name in suspicious_scripts:
                if (root / script_name).exists():
                    failures.append(
                        f"Demo set appears to use local template rendering: found {root / script_name}"
                    )

        record_candidates = [
            output_dir / "generation-record.md",
            output_dir.parent / "generation-record.md",
        ]
        record_text = ""
        for record in record_candidates:
            if record.exists():
                record_text += record.read_text(encoding="utf-8", errors="ignore").lower()
        if args.require_imagegen_record:
            if not record_text:
                failures.append("Missing generation-record.md for demo origin check")
            elif not any(provider in record_text for provider in ("imagegen", "image_gen", "zenmux")):
                failures.append("generation-record.md does not mention imagegen/image_gen/zenmux demo generation")

    if args.style_examples_set:
        style_pngs = sorted(output_dir.glob("style-[0-9][0-9]-*.png"))
        if len(style_pngs) < len(REQUIRED_STYLE_EXAMPLE_PREFIXES):
            failures.append(
                f"Style examples set must contain at least {len(REQUIRED_STYLE_EXAMPLE_PREFIXES)} style-*.png files, found {len(style_pngs)}"
            )
        for prefix in REQUIRED_STYLE_EXAMPLE_PREFIXES:
            if not any(path.name.startswith(prefix) for path in style_pngs):
                failures.append(f"Missing style example file with prefix {prefix}")

    checked_card_count = 0
    for png in pngs:
        if args.demo_set and png == overview_path:
            continue
        checked_card_count += 1
        try:
            width, height = read_size(png)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{png}: failed to read dimensions: {exc}")
            continue
        if (width, height) != (args.width, args.height):
            failures.append(f"{png}: expected {args.width}x{args.height}, got {width}x{height}")

    markdowns = {p.name for p in output_dir.glob("*.md")}
    has_note_package = "note-package.md" in markdowns
    has_image_set_package = "image-set-package.md" in markdowns
    has_post_copy = "post-copy.md" in markdowns
    if not examples_only and args.general_image_set and not has_image_set_package:
        failures.append("Missing image-set-package.md")
    if not examples_only and not args.general_image_set and not has_note_package:
        failures.append("Missing note-package.md")
    if not examples_only:
        style_lock_files = [p for p in output_dir.rglob("style-lock.md") if p.is_file()]
        if not style_lock_files:
            failures.append("Missing required style-lock.md")
        visual_system_files = [p for p in output_dir.rglob("visual-system.md") if p.is_file()]
        if not visual_system_files:
            failures.append("Missing required visual-system.md")
        if not args.general_image_set:
            cover_files = [p for p in output_dir.rglob("01-cover.png") if p.is_file()]
            if not cover_files:
                failures.append("Missing required 01-cover.png")

        renderer_names = {
            "render-final.js",
            "render.html",
            "rendered.html",
            "render-cards.js",
            "render-note.js",
            "playwright-render.js",
        }
        renderer_files = [p for p in output_dir.rglob("*") if p.is_file() and p.name in renderer_names]
        if renderer_files and not args.allow_controlled_renderer:
            failures.append(
                "Final package contains local renderer artifacts; provider-native final cards are required by default: "
                + ", ".join(str(p.relative_to(output_dir)) for p in renderer_files)
            )

        record_path = output_dir / "generation-record.md"
        if not record_path.exists():
            failures.append("Missing generation-record.md")
        else:
            record_text = record_path.read_text(encoding="utf-8", errors="ignore").lower()
            mentions_provider = any(provider in record_text for provider in ("imagegen", "image_gen", "zenmux"))
            if args.general_image_set:
                mentions_final_body = (
                    "final image" in record_text
                    or "image set" in record_text
                    or "generated images" in record_text
                    or "最终图片" in record_text
                    or "图片集" in record_text
                )
            else:
                mentions_final_body = (
                    "final body" in record_text
                    or "body page" in record_text
                    or "body cards" in record_text
                    or "正文" in record_text
                    or "pages 02" in record_text
                )
            if not mentions_provider or not mentions_final_body:
                if args.general_image_set:
                    failures.append(
                        "generation-record.md must state that final images were generated with imagegen/image_gen/zenmux"
                    )
                else:
                    failures.append(
                        "generation-record.md must state that final body cards were generated with imagegen/image_gen/zenmux"
                    )

    if failures:
        print("Validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Validated {checked_card_count} PNG file(s) at {args.width}x{args.height}.")
    if args.demo_set:
        print("Validated demo set structure.")
        if overview_path.exists():
            print(f"Ignored optional legacy {OVERVIEW_NAME}.")
    if args.style_examples_set:
        print("Validated static style examples set structure.")
    if has_note_package:
        print("Found note-package.md.")
    if has_image_set_package:
        print("Found image-set-package.md.")
    if has_post_copy:
        print("Found post-copy.md.")
    if not examples_only:
        print("Found style-lock.md.")
        print("Found visual-system.md.")
        if args.general_image_set:
            print("Final image set provider record check passed.")
        else:
            print("Final body imagegen record check passed.")
    if examples_only and not has_note_package and not has_image_set_package:
        print("Examples-only package accepted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

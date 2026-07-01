#!/usr/bin/env python3
"""Create a 2x3 overview image from six style example PNGs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


THUMB_WIDTH = 600
THUMB_HEIGHT = 750
PADDING = 56
GAP_X = 44
GAP_Y = 54
LABEL_HEIGHT = 62
HEADER_HEIGHT = 118
BACKGROUND = "#f8fafc"
INK = "#111827"
MUTED = "#6b7280"
BORDER = "#d1d5db"
ACCENT = "#16c653"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size, index=0)
            except Exception:
                continue
    return ImageFont.load_default()


def style_label(path: Path) -> str:
    match = re.match(r"(?:demo|style)-(\d{2})-(.+)\.png$", path.name)
    if not match:
        return path.stem
    number, slug = match.groups()
    return f"{number}  {slug}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("examples_dir", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    examples_dir = args.examples_dir
    examples = sorted(examples_dir.glob("style-[0-9][0-9]-*.png"))
    if not examples:
        examples = sorted(examples_dir.glob("demo-[0-9][0-9]-*.png"))
    if len(examples) != 6:
        raise SystemExit(f"Expected exactly 6 style example images, found {len(examples)}")

    out_path = args.out or examples_dir / "style-overview.png"
    width = PADDING * 2 + THUMB_WIDTH * 2 + GAP_X
    height = PADDING * 2 + HEADER_HEIGHT + (LABEL_HEIGHT + THUMB_HEIGHT) * 3 + GAP_Y * 2

    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(44, bold=True)
    subtitle_font = load_font(24)
    label_font = load_font(27, bold=True)

    draw.text((PADDING, PADDING), "Visual Atelier Style Overview", fill=INK, font=title_font)
    draw.text(
        (PADDING, PADDING + 58),
        "Choose 1-6. Each thumbnail is a reusable style example; overview is only for comparison.",
        fill=MUTED,
        font=subtitle_font,
    )

    start_y = PADDING + HEADER_HEIGHT
    for index, path in enumerate(examples):
        col = index % 2
        row = index // 2
        x = PADDING + col * (THUMB_WIDTH + GAP_X)
        y = start_y + row * (THUMB_HEIGHT + LABEL_HEIGHT + GAP_Y)

        draw.rounded_rectangle(
            (x - 8, y - 8, x + THUMB_WIDTH + 8, y + LABEL_HEIGHT + THUMB_HEIGHT + 8),
            radius=22,
            fill="#ffffff",
            outline=BORDER,
            width=2,
        )
        draw.rounded_rectangle((x, y, x + THUMB_WIDTH, y + LABEL_HEIGHT - 10), radius=16, fill="#ecfdf5")
        draw.text((x + 20, y + 15), style_label(path), fill=INK, font=label_font)

        with Image.open(path) as img:
            img = img.convert("RGB")
            thumb = img.resize((THUMB_WIDTH, THUMB_HEIGHT), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y + LABEL_HEIGHT))
        draw.rectangle((x, y + LABEL_HEIGHT, x + THUMB_WIDTH, y + LABEL_HEIGHT + THUMB_HEIGHT), outline=BORDER, width=1)

    draw.rounded_rectangle((width - PADDING - 170, PADDING + 8, width - PADDING, PADDING + 50), radius=21, fill=ACCENT)
    draw.text((width - PADDING - 145, PADDING + 16), "6 OPTIONS", fill="#ffffff", font=subtitle_font)
    sheet.save(out_path)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

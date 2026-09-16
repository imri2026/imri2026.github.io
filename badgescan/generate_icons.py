#!/usr/bin/env python3
"""Generate app icons for the iMRI 2026 Scan PWA from the conference logo.

Requires the `rsvg-convert` CLI (e.g. `brew install librsvg`) to rasterize
assets/imri-logo.svg. That file is a local copy of the site's
images/imri-logo.svg, kept here so this script doesn't depend on the
badgescan/ folder's location relative to the rest of the Jekyll site.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).parent
LOGO_SVG = HERE / "assets" / "imri-logo.svg"
ICONS_DIR = HERE / "icons"

BLUE = (31, 78, 121, 255)  # site brand "dark navy" #1F4E79


def rasterize_logo(target_width_px):
    if not shutil.which("rsvg-convert"):
        sys.exit(
            "rsvg-convert not found. Install it (e.g. `brew install librsvg`) "
            "and re-run, or rasterize assets/imri-logo.svg to a transparent "
            "PNG yourself and adapt this script."
        )
    proc = subprocess.run(
        ["rsvg-convert", "-w", str(target_width_px), str(LOGO_SVG)],
        capture_output=True,
        check=True,
    )
    from io import BytesIO

    img = Image.open(BytesIO(proc.stdout)).convert("RGBA")
    return img.crop(img.getbbox())


def compose_icon(logo, size, logo_width_ratio, rounded_ratio=None):
    """Center the logo on a brand-navy square. rounded_ratio=None -> square
    (edge-to-edge, for maskable icons); otherwise a rounded-rect radius ratio."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    if rounded_ratio is not None:
        draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * rounded_ratio), fill=BLUE)
    else:
        draw.rectangle([0, 0, size - 1, size - 1], fill=BLUE)

    target_w = int(size * logo_width_ratio)
    scale = target_w / logo.width
    target_h = int(logo.height * scale)
    resized = logo.resize((target_w, target_h), Image.LANCZOS)

    x = (size - target_w) // 2
    y = (size - target_h) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def save(img, path):
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    ICONS_DIR.mkdir(exist_ok=True)
    logo = rasterize_logo(1600)  # rasterize once at high res, reuse for all sizes

    # Standard icons: rounded-rect tile, logo at ~84% width, modest padding.
    save(compose_icon(logo, 192, 0.84, rounded_ratio=0.18), ICONS_DIR / "icon-192.png")
    save(compose_icon(logo, 512, 0.84, rounded_ratio=0.18), ICONS_DIR / "icon-512.png")

    # Maskable: edge-to-edge background (OS applies its own mask shape), logo
    # kept narrower (~68%) so it survives a circular crop within the
    # standard ~80%-diameter safe zone.
    save(compose_icon(logo, 512, 0.68, rounded_ratio=None), ICONS_DIR / "icon-maskable-512.png")

#!/usr/bin/env python3
"""Generate simple app icons for the iMRI 2026 Check-In PWA."""
from PIL import Image, ImageDraw

BLUE = (31, 78, 121, 255)  # site brand "dark navy" #1F4E79
ORANGE = (244, 161, 29, 255)  # site brand "amber gold" #F4A11D
WHITE = (255, 255, 255, 255)


def draw_scan_icon(size, corner_radius_ratio, bracket_inset_ratio, rounded=True):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if rounded:
        radius = int(size * corner_radius_ratio)
        draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BLUE)
    else:
        draw.rectangle([0, 0, size - 1, size - 1], fill=BLUE)

    inset = int(size * bracket_inset_ratio)
    bracket_len = int(size * 0.16)
    stroke = max(int(size * 0.035), 3)

    corners = [
        (inset, inset, 1, 1),  # top-left: (x, y, dx, dy) direction of arms
        (size - inset, inset, -1, 1),  # top-right
        (inset, size - inset, 1, -1),  # bottom-left
        (size - inset, size - inset, -1, -1),  # bottom-right
    ]
    for x, y, dx, dy in corners:
        draw.line([(x, y), (x + dx * bracket_len, y)], fill=WHITE, width=stroke)
        draw.line([(x, y), (x, y + dy * bracket_len)], fill=WHITE, width=stroke)

    # Center checkmark in orange, denoting "checked in".
    cx, cy = size / 2, size / 2
    s = size * 0.11
    check = [
        (cx - s, cy + s * 0.1),
        (cx - s * 0.25, cy + s * 0.85),
        (cx + s * 1.1, cy - s * 0.75),
    ]
    draw.line(check, fill=ORANGE, width=max(int(size * 0.045), 4), joint="curve")

    return img


def save(img, path):
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    save(draw_scan_icon(192, 0.18, 0.14), "icons/icon-192.png")
    save(draw_scan_icon(512, 0.18, 0.14), "icons/icon-512.png")
    # Maskable: background fills edge-to-edge (OS applies its own mask), and
    # icon content stays within the ~80% "safe zone".
    save(draw_scan_icon(512, 0.0, 0.20, rounded=False), "icons/icon-maskable-512.png")

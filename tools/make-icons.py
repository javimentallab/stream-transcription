#!/usr/bin/env python3
"""Draws the extension icon (16/32/48/96/128 px) into extension/shared/icons/.

A rounded purple square with two subtitle bars and a red "live" dot.
Drawn at 8x and downsampled, so the small sizes stay crisp.
Run:  python tools/make-icons.py
"""
import os

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "extension", "shared", "icons")
SIZES = (16, 32, 48, 96, 128)


def draw(px):
    s = px * 8
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # background with a vertical gradient
    top, bottom = (128, 96, 255), (90, 56, 240)
    grad = Image.new("RGBA", (s, s))
    gd = ImageDraw.Draw(grad)
    for y in range(s):
        k = y / (s - 1)
        gd.line([(0, y), (s, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)) + (255,))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=255)
    img.paste(grad, (0, 0), mask)

    # subtitle bars
    white = (255, 255, 255, 255)
    soft = (255, 255, 255, 170)
    h = s * 0.12
    r = h / 2
    d.rounded_rectangle([s * 0.17, s * 0.52, s * 0.83, s * 0.52 + h], radius=r, fill=white)
    d.rounded_rectangle([s * 0.27, s * 0.70, s * 0.73, s * 0.70 + h], radius=r, fill=soft)

    # live dot
    c, rad = (s * 0.29, s * 0.29), s * 0.105
    d.ellipse([c[0] - rad * 1.45, c[1] - rad * 1.45, c[0] + rad * 1.45, c[1] + rad * 1.45], fill=(255, 255, 255, 60))
    d.ellipse([c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad], fill=(255, 77, 125, 255))
    return img.resize((px, px), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    for px in SIZES:
        draw(px).save(os.path.join(OUT, f"icon{px}.png"))
    print("icons:", ", ".join(str(p) for p in SIZES))


if __name__ == "__main__":
    main()

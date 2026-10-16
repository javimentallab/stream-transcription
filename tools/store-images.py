#!/usr/bin/env python3
"""Composes the 1280x800 store / README images from raw screenshots.

    python tools/store-images.py <folder with raw screenshots>

Raw inputs (taken with the extension in English): subtitles-en.png, vram-en.png (1280x800
pages), popup-real-en.png, popup-mock-en.png (popup) and models-en.png (settings panel).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "store")
W, H = 1280, 800
FONT = "C:/Windows/Fonts/segoeui.ttf"
FONT_B = "C:/Windows/Fonts/segoeuib.ttf"


def background():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, bottom = (38, 28, 74), (15, 15, 26)
    for y in range(H):
        k = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([700, -200, 1500, 500], fill=90)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(Image.new("RGB", (W, H), (120, 90, 255)), (0, 0), glow)
    return img


def shadowed(base, shot, pos, radius=14):
    x, y = pos
    sh = Image.new("L", (shot.width + 80, shot.height + 80), 0)
    ImageDraw.Draw(sh).rounded_rectangle([40, 48, shot.width + 40, shot.height + 48], radius=radius, fill=160)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    base.paste(Image.new("RGB", sh.size, (0, 0, 0)), (x - 40, y - 40), sh)
    mask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width - 1, shot.height - 1], radius=radius, fill=255)
    base.paste(shot.convert("RGB"), (x, y), mask)


def text_block(img, x, y, title, lines, width=470):
    d = ImageDraw.Draw(img)
    ft = ImageFont.truetype(FONT_B, 46)
    fb = ImageFont.truetype(FONT, 25)
    for part in title.split("\n"):
        d.text((x, y), part, font=ft, fill=(255, 255, 255))
        y += 58
    y += 18
    for line in lines:
        words, cur = line.split(), ""
        for w in words:
            test = (cur + " " + w).strip()
            if d.textlength(test, font=fb) > width:
                d.text((x, y), cur, font=fb, fill=(205, 200, 230))
                y += 36
                cur = w
            else:
                cur = test
        d.text((x, y), cur, font=fb, fill=(205, 200, 230))
        y += 50


def scaled(path, factor):
    im = Image.open(path)
    return im.resize((int(im.width * factor), int(im.height * factor)), Image.LANCZOS)


def main(raw):
    os.makedirs(OUT, exist_ok=True)

    # 1 - subtitles over a stream: the raw page as it is
    Image.open(os.path.join(raw, "subtitles-en.png")).convert("RGB").save(os.path.join(OUT, "screenshot-1-subtitles.png"))

    # 2 - popup
    img = background()
    pop = scaled(os.path.join(raw, "popup-real-en.png"), 1.45)
    shadowed(img, pop, (W - pop.width - 120, (H - pop.height) // 2))
    text_block(img, 90, 200, "Subtitles in\nyour language",
               ["One click on any tab: Twitch, YouTube, Kick…",
                "Pick the model, the spoken language and the language you want to read."])
    img.save(os.path.join(OUT, "screenshot-2-popup.png"))

    # 3 - models
    img = background()
    mod = scaled(os.path.join(raw, "models-en.png"), 1.12)
    shadowed(img, mod, (W - mod.width - 70, (H - mod.height) // 2))
    text_block(img, 70, 190, "Any Whisper\nmodel", [
        "Paste a Hugging Face name or link and your server downloads it.",
        "Normal models are converted automatically. No paths, no terminal."], width=380)
    img.save(os.path.join(OUT, "screenshot-3-models.png"))

    # 4 - VRAM warning: page + popup
    img = Image.open(os.path.join(raw, "vram-en.png")).convert("RGB")
    pop = scaled(os.path.join(raw, "popup-mock-en.png"), 1.0)
    shadowed(img, pop, (W - pop.width - 40, 40))
    img.save(os.path.join(OUT, "screenshot-4-vram.png"))

    # icon for the listing
    from importlib import util
    spec = util.spec_from_file_location("mk", os.path.join(ROOT, "tools", "make-icons.py"))
    mk = util.module_from_spec(spec)
    spec.loader.exec_module(mk)
    mk.draw(512).save(os.path.join(OUT, "icon-512.png"))
    print("store images written to", OUT)


if __name__ == "__main__":
    main(sys.argv[1])

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(r"C:\Users\Lenovo\Documents\ChatGPT\images_for_media")
SOURCES = Path(r"C:\Users\Lenovo\.codex\generated_images\01a080a6-b560-7c12-bf98-2c1f9a33703e")
OUT = ROOT / "outputs" / "obuchenie-sverhsposobnostyam"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350
FONT = Path(r"C:\Windows\Fonts\DejaVuSans.ttf")
BOLD = Path(r"C:\Windows\Fonts\DejaVuSans-Bold.ttf")

SPECS = [
    ("exec-b0fe1202-6a0a-4b4c-a168-3592ebb45305.png", "01-sovremennaya.png", (10, 20, 38, 185), (255, 255, 255)),
    ("exec-816a7f0f-210b-401b-987d-5f3de609e816.png", "02-praktikum.png", (21, 34, 26, 178), (255, 255, 250)),
    ("exec-40b0a840-50a1-4b71-89fb-ff5d382ffede.png", "03-simvolicheskaya.png", (7, 16, 38, 188), (250, 234, 190)),
]
GIF_SOURCE = "exec-530cd1a1-b74e-456a-96ca-9d8029f86fbe.png"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def base_image(source: str) -> Image.Image:
    image = Image.open(SOURCES / source).convert("RGB")
    return ImageOps.fit(image, (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, fnt, fill, spacing: int = 0) -> int:
    box = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=spacing, align="center")
    x = (W - (box[2] - box[0])) // 2
    draw.multiline_text((x, y), text, font=fnt, fill=fill, spacing=spacing, align="center")
    return y + box[3] - box[1]


def add_copy(image: Image.Image, panel_color, text_color) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle((42, 36, W - 42, 486), radius=28, fill=panel_color)
    draw.rounded_rectangle((42, H - 142, W - 42, H - 42), radius=24, fill=panel_color)

    y = draw_centered(draw, "ОБУЧЕНИЕ\nСВЕРХСПОСОБНОСТЯМ", 63, font(BOLD, 57), text_color, 0)
    y += 7
    y = draw_centered(draw, "1 СТУПЕНЬ", y, font(BOLD, 23), text_color)
    y += 15
    y = draw_centered(draw, "СТАТЬ ЭКСТРАСЕНСОМ\nЗА 2 ДНЯ!", y, font(BOLD, 31), text_color, 2)
    y += 18
    y = draw_centered(draw, "26–27 СЕНТЯБРЯ · 10:00–19:00\nЕКАТЕРИНБУРГ", y, font(BOLD, 25), text_color, 6)
    y += 16
    draw_centered(draw, "ВЕДУЩАЯ: ТАТЬЯНА НОВОСЕЛОВА\nМАСТЕР АКАДЕМИИ РАЗВИТИЯ ЧЕЛОВЕКА", y, font(BOLD, 21), text_color, 5)
    draw_centered(draw, "ул. 8 Марта, 194Б · код 7#777", H - 108, font(BOLD, 22), text_color)
    return Image.alpha_composite(image.convert("RGBA"), layer)


def build_pngs() -> None:
    for source, destination, panel_color, text_color in SPECS:
        final = add_copy(base_image(source), panel_color, text_color).convert("RGB")
        final.save(OUT / destination, quality=95)


def build_gif() -> None:
    original = base_image(GIF_SOURCE)
    random.seed(260927)
    particles = [(random.randint(250, 840), random.randint(440, 1030), random.randint(2, 5), random.random() * math.tau) for _ in range(80)]
    frames = []
    for index in range(18):
        phase = index / 18 * math.tau
        frame = original.convert("RGBA")
        effects = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(effects)

        glow = int(18 + 26 * (0.5 + 0.5 * math.sin(phase)))
        draw.ellipse((382, 507, 698, 823), fill=(255, 197, 83, glow))
        for x, y, radius, offset in particles:
            alpha = int(35 + 150 * (0.5 + 0.5 * math.sin(phase * 1.7 + offset)))
            drift = int(15 * math.sin(phase + offset))
            draw.ellipse((x + drift - radius, y - radius, x + drift + radius, y + radius), fill=(255, 207, 107, alpha))

        mist = Image.new("RGBA", (W, 250), (0, 0, 0, 0))
        mist_draw = ImageDraw.Draw(mist)
        for wave in range(8):
            yy = 25 + wave * 30 + int(12 * math.sin(phase + wave))
            mist_draw.ellipse((-180 + int(80 * math.sin(phase + wave)), yy, 650, yy + 84), fill=(225, 235, 255, 18))
            mist_draw.ellipse((430 + int(70 * math.sin(phase + wave + 1)), yy + 10, 1250, yy + 100), fill=(225, 235, 255, 16))
        effects.alpha_composite(mist.filter(ImageFilter.GaussianBlur(20)), (0, 1010))

        # Restrained moving highlights on the two translucent curtains.
        for side in (0, 1):
            base_x = 130 if side == 0 else 820
            shift = int(30 * math.sin(phase + side * math.pi))
            draw.polygon([(base_x + shift, 400), (base_x + 55 + shift, 430), (base_x + 175 + shift, 930), (base_x + 105 + shift, 905)], fill=(255, 233, 188, 24))

        animated = Image.alpha_composite(frame, effects)
        final = add_copy(animated, (7, 16, 38, 190), (250, 234, 190)).convert("P", palette=Image.Palette.ADAPTIVE)
        frames.append(final)
    frames[0].save(OUT / "04-3d-animaciya.gif", save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=False, disposal=2)


if __name__ == "__main__":
    build_pngs()
    build_gif()
    print(OUT)

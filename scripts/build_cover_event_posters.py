from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageSequence

from build_event_posters import GIF_SOURCE, OUT, W, H, base_image, font, BOLD


def cover_gradient(color: tuple[int, int, int]) -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = overlay.load()
    for x in range(W):
        progress = min(x / 720, 1.0)
        alpha = int(218 * (1 - progress) ** 1.7)
        for y in range(H):
            pixels[x, y] = (*color, alpha)
    return overlay


def text(draw, xy, value, size, color, stroke):
    draw.multiline_text(xy, value, font=font(BOLD, size), fill=color, spacing=3, stroke_width=2, stroke_fill=stroke)


def cover_copy(image: Image.Image, accent, main, shade) -> Image.Image:
    image = Image.alpha_composite(image.convert("RGBA"), cover_gradient(shade))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    stroke = (*shade, 235)
    text(draw, (64, 88), "ОБУЧЕНИЕ\nСВЕРХСПОСОБНОСТЯМ", 45, main, stroke)
    draw.rounded_rectangle((66, 212, 330, 218), radius=3, fill=accent)
    text(draw, (66, 243), "1 СТУПЕНЬ", 24, accent, stroke)
    text(draw, (66, 340), "СТАТЬ ЭКСТРАСЕНСОМ\nЗА 2 ДНЯ!", 34, main, stroke)
    draw.rounded_rectangle((66, 438, 276, 444), radius=3, fill=accent)
    text(draw, (66, 474), "26–27 СЕНТЯБРЯ\n10:00–19:00\nЕКАТЕРИНБУРГ", 25, main, stroke)
    text(draw, (66, 680), "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии\nРазвития Человека", 20, main, stroke)
    text(draw, (66, 1265), "ул. 8 Марта, 194Б · код 7#777", 19, main, stroke)
    return Image.alpha_composite(image, layer)


def build_pngs():
    specs = [
        ("exec-b0fe1202-6a0a-4b4c-a168-3592ebb45305.png", "09-sovremennaya-cover.png", (235, 182, 94, 255), (255, 251, 240, 255), (7, 20, 40)),
        ("exec-816a7f0f-210b-401b-987d-5f3de609e816.png", "10-praktikum-cover.png", (241, 219, 151, 255), (255, 253, 243, 255), (28, 50, 33)),
        ("exec-40b0a840-50a1-4b71-89fb-ff5d382ffede.png", "11-simvolicheskaya-cover.png", (247, 220, 156, 255), (252, 245, 222, 255), (5, 13, 33)),
    ]
    for source, name, accent, main, shade in specs:
        cover_copy(base_image(source), accent, main, shade).convert("RGB").save(OUT / name, quality=95)


def build_gif():
    original = base_image(GIF_SOURCE)
    random.seed(260927)
    particles = [(random.randint(250, 840), random.randint(440, 1030), random.randint(2, 5), random.random() * math.tau) for _ in range(80)]
    frames = []
    for index in range(18):
        phase = index / 18 * math.tau
        effects = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(effects)
        draw.ellipse((382, 507, 698, 823), fill=(255, 197, 83, int(20 + 32 * (0.5 + 0.5 * math.sin(phase)))))
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
        for side in (0, 1):
            base_x = 130 if side == 0 else 820
            shift = int(30 * math.sin(phase + side * math.pi))
            draw.polygon([(base_x + shift, 400), (base_x + 55 + shift, 430), (base_x + 175 + shift, 930), (base_x + 105 + shift, 905)], fill=(255, 233, 188, 24))
        animated = Image.alpha_composite(original.convert("RGBA"), effects)
        frames.append(cover_copy(animated, (247, 220, 156, 255), (252, 245, 222, 255), (5, 13, 33)).convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(OUT / "12-3d-animaciya-cover.gif", save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=False, disposal=2)


if __name__ == "__main__":
    build_pngs()
    build_gif()
    print(OUT)

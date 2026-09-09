from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageSequence

from build_event_posters import GIF_SOURCE, OUT, W, H, base_image, font, BOLD


def block(draw, xy, text, size, color, align="left", spacing=3, stroke=(7, 13, 28, 190)):
    draw.multiline_text(
        xy,
        text,
        font=font(BOLD, size),
        fill=color,
        spacing=spacing,
        align=align,
        stroke_width=2,
        stroke_fill=stroke,
    )


def line(draw, x, y, width, color):
    draw.rounded_rectangle((x, y, x + width, y + 5), radius=3, fill=color)


def integrated_copy(image: Image.Image, style: int) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    if style == 1:
        white, accent, dark = (250, 248, 242, 255), (237, 181, 97, 255), (7, 18, 38, 210)
        block(draw, (68, 66), "ОБУЧЕНИЕ\nСВЕРХСПОСОБНОСТЯМ", 49, white, spacing=-2, stroke=dark)
        line(draw, 70, 192, 208, accent)
        block(draw, (70, 218), "1 СТУПЕНЬ", 22, accent, stroke=dark)
        block(draw, (70, 274), "СТАТЬ ЭКСТРАСЕНСОМ\nЗА 2 ДНЯ!", 31, white, spacing=0, stroke=dark)
        block(draw, (698, 456), "26–27 СЕНТЯБРЯ\n10:00–19:00 · ЕКАТЕРИНБУРГ", 20, white, spacing=4, stroke=dark)
        line(draw, 700, 540, 184, accent)
        block(draw, (618, 585), "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии\nРазвития Человека", 18, white, spacing=2, stroke=dark)
        block(draw, (70, 1270), "ул. 8 Марта, 194Б · код 7#777", 20, white, stroke=dark)
    elif style == 2:
        white, accent, dark = (254, 251, 239, 255), (65, 100, 73, 255), (250, 248, 235, 205)
        block(draw, (546, 66), "ОБУЧЕНИЕ\nСВЕРХСПОСОБНОСТЯМ", 38, accent, spacing=-2, stroke=dark)
        line(draw, 550, 166, 188, accent)
        block(draw, (550, 193), "1 СТУПЕНЬ", 20, accent, stroke=dark)
        block(draw, (70, 484), "СТАТЬ ЭКСТРАСЕНСОМ\nЗА 2 ДНЯ!", 31, white, spacing=0, stroke=(24, 44, 28, 210))
        line(draw, 72, 567, 170, (238, 222, 154, 255))
        block(draw, (70, 602), "26–27 СЕНТЯБРЯ · 10:00–19:00\nЕКАТЕРИНБУРГ", 20, white, spacing=4, stroke=(24, 44, 28, 210))
        block(draw, (610, 1025), "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии\nРазвития Человека", 18, accent, spacing=2, stroke=dark)
        block(draw, (70, 1270), "ул. 8 Марта, 194Б · код 7#777", 20, accent, stroke=dark)
    elif style == 3:
        gold, pearl, dark = (247, 222, 160, 255), (241, 242, 246, 255), (4, 10, 28, 220)
        block(draw, (126, 68), "ОБУЧЕНИЕ\nСВЕРХСПОСОБНОСТЯМ", 50, gold, spacing=-2, stroke=dark)
        line(draw, 126, 195, 258, gold)
        block(draw, (126, 222), "1 СТУПЕНЬ", 21, pearl, stroke=dark)
        block(draw, (230, 482), "СТАТЬ ЭКСТРАСЕНСОМ\nЗА 2 ДНЯ!", 30, gold, spacing=0, stroke=dark)
        block(draw, (76, 730), "26–27 СЕНТЯБРЯ\n10:00–19:00\nЕКАТЕРИНБУРГ", 19, pearl, spacing=4, stroke=dark)
        block(draw, (642, 1058), "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии\nРазвития Человека", 17, gold, spacing=2, stroke=dark)
        block(draw, (70, 1270), "ул. 8 Марта, 194Б · код 7#777", 20, pearl, stroke=dark)
    else:
        gold, pearl, dark = (247, 222, 160, 255), (241, 242, 246, 255), (4, 10, 28, 220)
        block(draw, (128, 66), "ОБУЧЕНИЕ\nСВЕРХСПОСОБНОСТЯМ", 50, gold, spacing=-2, stroke=dark)
        line(draw, 128, 194, 260, gold)
        block(draw, (128, 222), "1 СТУПЕНЬ", 21, pearl, stroke=dark)
        block(draw, (686, 420), "СТАТЬ\nЭКСТРАСЕНСОМ\nЗА 2 ДНЯ!", 27, gold, spacing=1, stroke=dark)
        block(draw, (74, 778), "26–27 СЕНТЯБРЯ\n10:00–19:00\nЕКАТЕРИНБУРГ", 19, pearl, spacing=4, stroke=dark)
        block(draw, (610, 1056), "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии\nРазвития Человека", 17, gold, spacing=2, stroke=dark)
        block(draw, (70, 1270), "ул. 8 Марта, 194Б · код 7#777", 20, pearl, stroke=dark)
    return Image.alpha_composite(image.convert("RGBA"), layer)


def build_pngs():
    sources = [
        "exec-b0fe1202-6a0a-4b4c-a168-3592ebb45305.png",
        "exec-816a7f0f-210b-401b-987d-5f3de609e816.png",
        "exec-40b0a840-50a1-4b71-89fb-ff5d382ffede.png",
    ]
    names = ["05-sovremennaya-integrated.png", "06-praktikum-integrated.png", "07-simvolicheskaya-integrated.png"]
    for index, (source, name) in enumerate(zip(sources, names), start=1):
        integrated_copy(base_image(source), index).convert("RGB").save(OUT / name, quality=95)


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
        frames.append(integrated_copy(animated, 4).convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(OUT / "08-3d-animaciya-integrated.gif", save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=False, disposal=2)


if __name__ == "__main__":
    build_pngs()
    build_gif()
    print(OUT)

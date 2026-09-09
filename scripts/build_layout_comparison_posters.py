from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from build_event_posters import BOLD, FONT, H, OUT, SOURCES, W, base_image, font


TITLE = "ОБУЧЕНИЕ\nСВЕРХСПОСОБНОСТЯМ"
OFFER = "СТАТЬ ЭКСТРАСЕНСОМ\nЗА 2 ДНЯ!"
DATE = "26–27 СЕНТЯБРЯ · 10:00–19:00\nЕКАТЕРИНБУРГ"
HOST = "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии Развития Человека"
ADDRESS = "ул. 8 Марта, 194Б · код 7#777"
CURRENCY_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


def text(draw: ImageDraw.ImageDraw, xy, value: str, size: int, color, *, anchor=None, align="left", stroke=(0, 0, 0, 0), width=0, spacing=4, typeface=BOLD):
    draw.multiline_text(xy, value, font=font(typeface, size), fill=color, anchor=anchor, align=align, spacing=spacing, stroke_width=width, stroke_fill=stroke)


def text_in_column(draw: ImageDraw.ImageDraw, xy, value: str, size: int, color, max_right: int, *, stroke=(0, 0, 0, 0), width=0, spacing=4, typeface=BOLD):
    bounds = draw.multiline_textbbox(xy, value, font=font(typeface, size), spacing=spacing, stroke_width=width)
    if bounds[2] > max_right:
        raise ValueError(f"Text exceeds column: {value!r}")
    text(draw, xy, value, size, color, stroke=stroke, width=width, spacing=spacing, typeface=typeface)


def left_gradient(color: tuple[int, int, int]) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = layer.load()
    for x in range(620):
        alpha = int(242 * (1 - x / 620) ** 1.25)
        for y in range(H):
            pixels[x, y] = (*color, alpha)
    return layer


def vertical_fade(color: tuple[int, int, int], top: int, bottom: int) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = layer.load()
    for y in range(top, bottom):
        alpha = int(225 * (1 - (y - top) / max(1, bottom - top)))
        for x in range(W):
            pixels[x, y] = (*color, alpha)
    return layer


def save(image: Image.Image, name: str) -> None:
    image.convert("RGB").save(OUT / name, quality=95)


def editorial_column() -> None:
    image = Image.alpha_composite(base_image("exec-b0fe1202-6a0a-4b4c-a168-3592ebb45305.png").convert("RGBA"), left_gradient((7, 19, 37)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cream, amber, dark = (255, 250, 237, 255), (239, 185, 90, 255), (7, 19, 37, 255)
    text(draw, (62, 80), TITLE, 49, cream, stroke=dark, width=2)
    draw.rounded_rectangle((64, 222, 330, 228), radius=3, fill=amber)
    text(draw, (64, 255), "1 СТУПЕНЬ", 27, amber, stroke=dark, width=2)
    text(draw, (64, 360), OFFER, 37, cream, stroke=dark, width=2)
    draw.rounded_rectangle((64, 472, 320, 478), radius=3, fill=amber)
    text(draw, (64, 510), DATE, 28, cream, stroke=dark, width=2)
    text(draw, (64, 756), HOST, 25, cream, stroke=dark, width=2)
    text(draw, (64, 1260), ADDRESS, 27, cream, stroke=dark, width=2)
    save(Image.alpha_composite(image, layer), "17-layout-editorial-column.png")


def cinematic_poster() -> None:
    image = base_image("exec-816a7f0f-210b-401b-987d-5f3de609e816.png").convert("RGBA")
    image = Image.alpha_composite(image, vertical_fade((12, 28, 23), 0, 440))
    image = Image.alpha_composite(image, vertical_fade((12, 28, 23), 1010, H))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cream, lime, dark = (255, 253, 240, 255), (203, 222, 154, 255), (12, 28, 23, 255)
    text(draw, (W // 2, 73), TITLE, 57, cream, anchor="ma", align="center", stroke=dark, width=3)
    text(draw, (W // 2, 230), "1 СТУПЕНЬ", 27, lime, anchor="ma", align="center", stroke=dark, width=2)
    text(draw, (W // 2, 318), OFFER, 35, cream, anchor="ma", align="center", stroke=dark, width=3)
    draw.rounded_rectangle((116, 1085, 964, 1091), radius=3, fill=lime)
    text(draw, (W // 2, 1125), DATE, 28, cream, anchor="ma", align="center", stroke=dark, width=2)
    text(draw, (W // 2, 1205), HOST, 25, cream, anchor="ma", align="center", stroke=dark, width=2)
    text(draw, (W // 2, 1300), ADDRESS, 27, cream, anchor="ms", align="center", stroke=dark, width=2)
    save(Image.alpha_composite(image, layer), "18-layout-cinematic-poster.png")


def scene_integrated() -> None:
    image = base_image("exec-40b0a840-50a1-4b71-89fb-ff5d382ffede.png").convert("RGBA")
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.ellipse((48, 44, 1032, 414), fill=(4, 12, 31, 172))
    draw_shadow.rounded_rectangle((64, 1040, 1016, 1328), radius=34, fill=(4, 12, 31, 188))
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(16)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    gold, cream, navy = (242, 204, 125, 255), (255, 248, 229, 255), (4, 12, 31, 255)
    text(draw, (W // 2, 68), TITLE, 54, gold, anchor="ma", align="center", stroke=navy, width=3)
    text(draw, (W // 2, 226), "1 СТУПЕНЬ", 27, cream, anchor="ma", align="center", stroke=navy, width=2)
    text(draw, (W // 2, 310), OFFER, 36, cream, anchor="ma", align="center", stroke=navy, width=3)
    draw.arc((110, 378, 970, 1240), 202, 338, fill=gold, width=5)
    text(draw, (W // 2, 1068), DATE, 29, cream, anchor="ma", align="center", stroke=navy, width=2)
    text(draw, (W // 2, 1158), HOST, 25, cream, anchor="ma", align="center", stroke=navy, width=2)
    text(draw, (W // 2, 1302), ADDRESS, 27, gold, anchor="ms", align="center", stroke=navy, width=2)
    save(Image.alpha_composite(image, layer), "19-layout-scene-integrated.png")


def diptych() -> None:
    source = base_image("exec-530cd1a1-b74e-456a-96ca-9d8029f86fbe.png").convert("RGBA")
    image = Image.new("RGBA", (W, H), (8, 18, 39, 255))
    right = ImageOps.fit(source, (540, H), method=Image.Resampling.LANCZOS, centering=(0.58, 0.5))
    image.alpha_composite(right, (540, 0))
    seam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_seam = ImageDraw.Draw(seam)
    draw_seam.rectangle((520, 0, 560, H), fill=(8, 18, 39, 150))
    draw_seam.line((540, 92, 540, 1258), fill=(238, 193, 100, 210), width=3)
    image = Image.alpha_composite(image, seam)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cream, amber, navy = (255, 250, 236, 255), (238, 193, 100, 255), (8, 18, 39, 255)
    text(draw, (54, 92), TITLE, 45, cream, stroke=navy, width=2)
    draw.rounded_rectangle((56, 235, 338, 241), radius=3, fill=amber)
    text(draw, (56, 272), "1 СТУПЕНЬ", 27, amber, stroke=navy, width=2)
    text(draw, (56, 375), OFFER, 34, cream, stroke=navy, width=2)
    text(draw, (56, 646), DATE, 28, cream, stroke=navy, width=2)
    text(draw, (56, 865), HOST, 25, cream, stroke=navy, width=2)
    text(draw, (56, 1260), "ул. 8 Марта,\n194Б · код 7#777", 27, cream, stroke=navy, width=2)
    save(Image.alpha_composite(image, layer), "20-layout-diptych.png")


def orbital() -> None:
    image = base_image("exec-0fe38914-fb4a-42b9-b111-f31859d4d985.png").convert("RGBA")
    haze = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_haze = ImageDraw.Draw(haze)
    draw_haze.ellipse((82, 78, 998, 990), outline=(12, 28, 58, 178), width=72)
    draw_haze.rounded_rectangle((62, 1060, 1018, 1328), radius=38, fill=(7, 18, 39, 180))
    image = Image.alpha_composite(image, haze.filter(ImageFilter.GaussianBlur(7)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cream, amber, navy = (255, 248, 228, 255), (240, 194, 104, 255), (7, 18, 39, 255)
    draw.arc((116, 92, 964, 940), 198, 342, fill=amber, width=5)
    text(draw, (W // 2, 90), TITLE, 48, cream, anchor="ma", align="center", stroke=navy, width=3)
    text(draw, (W // 2, 244), "1 СТУПЕНЬ", 27, amber, anchor="ma", align="center", stroke=navy, width=2)
    text(draw, (W // 2, 895), OFFER, 36, cream, anchor="ma", align="center", stroke=navy, width=3)
    text(draw, (W // 2, 1087), DATE, 29, cream, anchor="ma", align="center", stroke=navy, width=2)
    text(draw, (W // 2, 1179), HOST, 25, cream, anchor="ma", align="center", stroke=navy, width=2)
    text(draw, (W // 2, 1305), ADDRESS, 27, amber, anchor="ms", align="center", stroke=navy, width=2)
    save(Image.alpha_composite(image, layer), "21-layout-orbital.png")


def diptych_strict() -> None:
    split = 640
    image = Image.new("RGBA", (W, H), (8, 18, 39, 255))
    source = base_image("exec-530cd1a1-b74e-456a-96ca-9d8029f86fbe.png").convert("RGBA")
    visual = ImageOps.fit(source, (W - split, H), method=Image.Resampling.LANCZOS, centering=(0.58, 0.5))
    image.alpha_composite(visual, (split, 0))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cream, amber, navy = (255, 250, 236, 255), (238, 193, 100, 255), (8, 18, 39, 255)
    draw.line((split, 92, split, 1258), fill=amber, width=3)
    text(draw, (54, 92), TITLE, 38, cream, stroke=navy, width=2)
    draw.rounded_rectangle((56, 220, 330, 226), radius=3, fill=amber)
    text(draw, (56, 258), "1 СТУПЕНЬ", 27, amber, stroke=navy, width=2)
    text(draw, (56, 374), OFFER, 34, cream, stroke=navy, width=2)
    text(draw, (56, 648), DATE, 28, cream, stroke=navy, width=2)
    text(draw, (56, 868), HOST, 25, cream, stroke=navy, width=2)
    text(draw, (56, 1260), "ул. 8 Марта,\n194Б · код 7#777", 27, cream, stroke=navy, width=2)
    save(Image.alpha_composite(image, layer), "22-layout-diptych-strict.png")


def diptych_headline_bleed() -> None:
    split = 518
    source = base_image("exec-0fe38914-fb4a-42b9-b111-f31859d4d985.png").convert("RGBA")
    image = Image.new("RGBA", (W, H), (7, 18, 39, 255))
    visual = ImageOps.fit(source, (W - split, H), method=Image.Resampling.LANCZOS, centering=(0.58, 0.5))
    image.alpha_composite(visual, (split, 0))
    header = Image.new("RGBA", (W, 390), (0, 0, 0, 0))
    header_pixels = header.load()
    for x in range(780):
        alpha = int(230 * (1 - x / 780) ** 1.45)
        for y in range(390):
            header_pixels[x, y] = (7, 18, 39, alpha)
    image.alpha_composite(header)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cream, amber, navy = (255, 250, 236, 255), (238, 193, 100, 255), (7, 18, 39, 255)
    draw.line((split, 430, split, 1258), fill=amber, width=3)
    text(draw, (54, 94), TITLE, 47, cream, stroke=navy, width=3)
    text_in_column(draw, (56, 250), "1 СТУПЕНЬ", 27, amber, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 330), "ТОНКО ЧУВСТВОВАТЬ\nЯСНО ВИДЕТЬ\nЯСНО ЗНАТЬ", 27, amber, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 445), OFFER, 30, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 560), "26–27 СЕНТЯБРЯ\n10:00–19:00\nЕКАТЕРИНБУРГ", 27, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 700), "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии\nРазвития Человека", 27, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 855), "СТОИМОСТЬ\nдо 10.09 — 25 000 ₽\nпосле — 27 000 ₽\nв день — 30 000 ₽", 27, amber, split - 18, stroke=navy, width=2, typeface=CURRENCY_BOLD)
    text_in_column(draw, (56, 1035), "ЗАПИСЬ: +7 (912)\n633-11-18", 27, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 1185), "ул. 8 Марта,\n194Б · код 7#777", 27, cream, split - 18, stroke=navy, width=2)
    save(Image.alpha_composite(image, layer), "23-layout-diptych-headline-bleed.png")


def diptych_headline_bleed_offer_readable() -> None:
    split = 518
    source = base_image("exec-0fe38914-fb4a-42b9-b111-f31859d4d985.png").convert("RGBA")
    image = Image.new("RGBA", (W, H), (7, 18, 39, 255))
    visual = ImageOps.fit(source, (W - split, H), method=Image.Resampling.LANCZOS, centering=(0.58, 0.5))
    image.alpha_composite(visual, (split, 0))
    header = Image.new("RGBA", (W, 390), (0, 0, 0, 0))
    header_pixels = header.load()
    for x in range(780):
        alpha = int(230 * (1 - x / 780) ** 1.45)
        for y in range(390):
            header_pixels[x, y] = (7, 18, 39, alpha)
    image.alpha_composite(header)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cream, amber, navy = (255, 250, 236, 255), (238, 193, 100, 255), (7, 18, 39, 255)
    draw.line((split, 430, split, 1258), fill=amber, width=3)
    text(draw, (54, 94), TITLE, 47, cream, stroke=navy, width=3)
    text_in_column(draw, (56, 250), "1 СТУПЕНЬ", 27, amber, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 330), "ТОНКО ЧУВСТВОВАТЬ\nЯСНО ВИДЕТЬ\nЯСНО ЗНАТЬ", 32, amber, split - 18, stroke=navy, width=2, spacing=8, typeface=CURRENCY_BOLD)
    text_in_column(draw, (56, 480), OFFER, 30, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 605), "26–27 СЕНТЯБРЯ\n10:00–19:00\nЕКАТЕРИНБУРГ", 27, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 745), "ТАТЬЯНА НОВОСЕЛОВА\nМастер Академии\nРазвития Человека", 27, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 900), "СТОИМОСТЬ\nдо 10.09 — 25 000 ₽\nпосле — 27 000 ₽\nв день — 30 000 ₽", 27, amber, split - 18, stroke=navy, width=2, typeface=CURRENCY_BOLD)
    text_in_column(draw, (56, 1080), "ЗАПИСЬ: +7 (912)\n633-11-18", 27, cream, split - 18, stroke=navy, width=2)
    text_in_column(draw, (56, 1210), "ул. 8 Марта,\n194Б · код 7#777", 27, cream, split - 18, stroke=navy, width=2)
    save(Image.alpha_composite(image, layer), "24-layout-diptych-headline-bleed-offer-readable.png")


if __name__ == "__main__":
    editorial_column()
    cinematic_poster()
    scene_integrated()
    diptych()
    orbital()
    diptych_strict()
    diptych_headline_bleed()
    diptych_headline_bleed_offer_readable()
    print(OUT)

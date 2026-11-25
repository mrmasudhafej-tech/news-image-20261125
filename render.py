"""Render a one-page newspaper front page for 25 November 2026.

Draws everything with Pillow shapes and DejaVu fonts and saves
entry.png beside this file. No external images are used.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 36
LEFT = MARGIN
RIGHT = W - MARGIN
CONTENT_W = RIGHT - LEFT

PAPER = (253, 251, 243)
INK = (17, 17, 17)
GREY = (85, 85, 85)
RULE = (17, 17, 17)
ACCENT = (153, 27, 30)
NAVY = (18, 42, 76)
SKY_TOP = (16, 38, 84)
SKY_MID = (52, 102, 168)
SKY_LOW = (150, 188, 224)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def load(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


FONTS = {
    "kicker": load("DejaVuSans-Bold.ttf", 17),
    "masthead": load("DejaVuSerif-Bold.ttf", 104),
    "dateline": load("DejaVuSans-Bold.ttf", 18),
    "headline": load("DejaVuSerif-Bold.ttf", 44),
    "standfirst": load("DejaVuSerif.ttf", 21),
    "label": load("DejaVuSans-Bold.ttf", 14),
    "story_head": load("DejaVuSerif-Bold.ttf", 23),
    "story_body": load("DejaVuSans.ttf", 17),
    "caption": load("DejaVuSans-Bold.ttf", 15),
    "footer_bold": load("DejaVuSans-Bold.ttf", 15),
    "footer": load("DejaVuSans.ttf", 15),
    "source": load("DejaVuSans.ttf", 13),
}


def wrap(draw, text, font, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, y, text, font, fill=INK):
    draw.text((W // 2, y), text, font=font, fill=fill, anchor="ma")


def draw_header(draw):
    draw.rectangle([LEFT, 22, RIGHT, 26], fill=RULE)
    draw.rectangle([LEFT, 30, RIGHT, 31], fill=RULE)
    centred(draw, 40, "ONE DAY  \u2022  ONE PAGE  \u2022  THE WORLD'S NEWS",
            FONTS["kicker"])
    centred(draw, 66, "WORLD NEWS", FONTS["masthead"])
    draw.rectangle([LEFT, 182, RIGHT, 186], fill=RULE)
    draw.rectangle([LEFT, 190, RIGHT, 191], fill=RULE)
    centred(draw, 198, "WEDNESDAY 25 NOVEMBER 2026", FONTS["dateline"])


def draw_lead(draw):
    headline = "First Pakistani in orbit as China's Shenzhou-24 lifts off"
    lines = wrap(draw, headline, FONTS["headline"], CONTENT_W)
    y = 226
    for line in lines:
        draw.text((LEFT, y), line, font=FONTS["headline"], fill=INK)
        y += 52
    standfirst = (
        "Zeeshan Ali, 40, a Pakistan Air Force pilot, is set to become "
        "the first foreign astronaut aboard China's Tiangong station. "
        "The crew launched at 08:18 from Jiuquan for 5 to 10 days "
        "of experiments."
    )
    body_lines = wrap(draw, standfirst, FONTS["standfirst"], CONTENT_W)
    y = 340
    for line in body_lines:
        draw.text((LEFT, y), line, font=FONTS["standfirst"], fill=GREY)
        y += 29


def draw_illustration(draw):
    top, bottom = 440, 640
    # Sky gradient in horizontal bands.
    bands = 40
    for i in range(bands):
        t = i / max(1, bands - 1)
        r = int(SKY_TOP[0] + (SKY_LOW[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_LOW[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_LOW[2] - SKY_TOP[2]) * t)
        y0 = top + int(i * (bottom - top) / bands)
        y1 = top + int((i + 1) * (bottom - top) / bands)
        draw.rectangle([LEFT, y0, RIGHT, y1], fill=(r, g, b))
    # Stars in the upper sky.
    for sx, sy, sr in [(90, 462, 2), (180, 478, 2), (300, 458, 3),
                       (430, 472, 2), (760, 460, 2), (880, 476, 3),
                       (940, 458, 2), (250, 492, 2), (830, 492, 2)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))
    # Pale sun glow, top left.
    draw.ellipse([70, 452, 150, 532], fill=(255, 236, 170))
    draw.ellipse([88, 470, 132, 514], fill=(255, 248, 210))
    # Distant hills.
    draw.polygon([(LEFT, 600), (300, 556), (560, 600), (760, 568),
                  (RIGHT, 600), (RIGHT, bottom), (LEFT, bottom)],
                 fill=(96, 122, 150))
    # Launch tower on the left of the rocket.
    draw.rectangle([512, 478, 522, 612], fill=(70, 70, 70))
    draw.rectangle([500, 478, 560, 486], fill=(70, 70, 70))
    for ty in (508, 538, 568):
        draw.rectangle([500, ty, 560, ty + 5], fill=(70, 70, 70))
    draw.line([(560, 500), (596, 516)], fill=(70, 70, 70), width=4)
    # Rocket body, centred near x=620.
    cx = 620
    draw.polygon([(cx - 20, 492), (cx + 20, 492), (cx, 452)],
                 fill=(220, 38, 38), outline=(120, 10, 10))
    draw.rectangle([cx - 20, 492, cx + 20, 578], fill=(245, 245, 245),
                   outline=(120, 10, 10))
    draw.rectangle([cx - 20, 540, cx + 20, 552], fill=(220, 38, 38))
    draw.ellipse([cx - 9, 506, cx + 9, 524], fill=(120, 190, 230),
                 outline=(17, 17, 17))
    # Fins.
    draw.polygon([(cx - 20, 548), (cx - 44, 584), (cx - 20, 584)],
                 fill=(220, 38, 38))
    draw.polygon([(cx + 20, 548), (cx + 44, 584), (cx + 20, 584)],
                 fill=(220, 38, 38))
    # Flame.
    draw.polygon([(cx - 12, 578), (cx + 12, 578), (cx, 612)],
                 fill=(255, 140, 0))
    draw.polygon([(cx - 6, 578), (cx + 6, 578), (cx, 600)],
                 fill=(255, 220, 60))
    # Smoke clouds at the base.
    for sx, sy, sr in [(560, 600, 26), (600, 610, 32), (650, 610, 32),
                       (690, 600, 26), (580, 590, 20), (665, 590, 20)]:
        draw.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2],
                     fill=(235, 235, 235))
    # Ground.
    draw.rectangle([LEFT, 612, RIGHT, bottom], fill=(88, 84, 78))
    draw.rectangle([LEFT, 612, RIGHT, 614], fill=(60, 58, 54))
    # Caption bar across the foot of the panel.
    draw.rectangle([LEFT, 614, RIGHT, bottom], fill=NAVY)
    draw.text((LEFT + 14, 619), "SHENZHOU-24  \u2022  JIUQUAN, CHINA",
              font=FONTS["caption"], fill=(255, 255, 255))
    draw.text((RIGHT - 14, 619), "ILLUSTRATION", font=FONTS["caption"],
              fill=(200, 215, 235), anchor="ra")


def draw_stories(draw):
    stories = [
        ("MIDDLE EAST",
         "Houthis threaten Jeddah and Saudi Red Sea ports",
         "Warning came if Riyadh attacks Hodeidah; coalition struck "
         "targets there on Wednesday."),
        ("MARKETS",
         "Asian stocks fall as new US tariff threat looms",
         "Chip shares led falls after reports of new US tariff "
         "findings; Nvidia fell 5.9%."),
        ("COURTS",
         "US jury convicts Huawei on 10 of 12 counts",
         "Brooklyn jury found fraud and trade-secret theft over Iran "
         "business; Huawei was cleared of racketeering."),
        ("UNITED NATIONS",
         "UN: five women killed every hour by partner or relative",
         "47,000 women and girls were killed in 2025, UN Women and "
         "UNODC said, as 16 Days of Activism begins."),
    ]
    col_w = (CONTENT_W - 28) // 2
    xs = [LEFT, LEFT + col_w + 28]
    ys = [652, 776]
    for idx, (label, head, body) in enumerate(stories):
        x = xs[idx % 2]
        y = ys[idx // 2]
        draw.text((x, y), label, font=FONTS["label"], fill=ACCENT)
        head_lines = wrap(draw, head, FONTS["story_head"], col_w)
        hy = y + 22
        for line in head_lines[:2]:
            draw.text((x, hy), line, font=FONTS["story_head"], fill=INK)
            hy += 27
        body_lines = wrap(draw, body, FONTS["story_body"], col_w)
        by = y + 76
        for line in body_lines[:3]:
            draw.text((x, by), line, font=FONTS["story_body"], fill=GREY)
            by += 21
    mid_x = LEFT + col_w + 14
    draw.line([(mid_x, 652), (mid_x, 906)], fill=(180, 180, 180), width=1)
    draw.line([(LEFT, 768), (RIGHT, 768)], fill=(180, 180, 180), width=1)


def draw_footer(draw):
    draw.rectangle([LEFT, 918, RIGHT, 920], fill=RULE)
    centred(draw, 930,
            "ALSO: Chess Game 2 today in Geneva \u2014 Gukesh has White "
            "after Game 1 draw", FONTS["footer_bold"])
    centred(draw, 954,
            "Shanghai pledges loyalty as party chief Chen is probed "
            "\u2022  Russian strike kills two in Odesa, governor says",
            FONTS["footer"])
    centred(draw, 978,
            "Stories reported on 25 November 2026  \u2022  Sources: "
            "Reuters, UN Women, FIDE", FONTS["source"], fill=GREY)


def main():
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw_header(draw)
    draw_lead(draw)
    draw_illustration(draw)
    draw_stories(draw)
    draw_footer(draw)
    out = Path(__file__).resolve().parent / "entry.png"
    image.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()

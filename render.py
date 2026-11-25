#!/usr/bin/env python3
"""Draw the 25 November 2026 front page and save it as entry.png.

Original artwork drawn with Pillow for this competition day only.
Run:  python3 render.py   (writes entry.png next to this file, 1024x1024)
The shipped entry program (main.py) only copies entry.png to the output
directory, so grading runs are byte-identical.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 246, 236)
INK = (22, 22, 22)
NAVY = (22, 41, 77)
RED = (176, 30, 36)
GREY = (90, 90, 84)
SKY_TOP = (13, 27, 58)
SKY_BOTTOM = (58, 104, 160)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, spacing=4):
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def headline_block(draw, x, y, text, fnt, max_width, fill, spacing=2):
    return draw_wrapped(draw, x, y, text, fnt, max_width, fill, spacing)


def draw_rocket_panel(d, x0, y0, x1, y1):
    """Original rocket-launch illustration inside the given panel."""
    # Night-sky gradient in horizontal bands.
    steps = 24
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(
            int(SKY_TOP[c] + (SKY_BOTTOM[c] - SKY_TOP[c]) * t)
            for c in range(3)
        )
        yy0 = y0 + (y1 - y0) * i // steps
        yy1 = y0 + (y1 - y0) * (i + 1) // steps
        d.rectangle([x0, yy0, x1, yy1], fill=col)
    # Stars.
    for sx, sy in [(x0 + 28, y0 + 24), (x0 + 88, y0 + 14),
                   (x0 + 210, y0 + 34), (x0 + 268, y0 + 18),
                   (x0 + 52, y0 + 72), (x0 + 250, y0 + 84),
                   (x0 + 150, y0 + 52), (x0 + 308, y0 + 64)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # Full moon.
    mx, my = x0 + 278, y0 + 30
    d.ellipse([mx - 18, my - 18, mx + 18, my + 18], fill=(240, 236, 200))
    # Ground and launch smoke.
    ground = y1 - 26
    d.rectangle([x0, ground, x1, y1], fill=(52, 58, 52))
    for cx, cy, rx, ry in [(x0 + 70, ground - 8, 62, 16),
                           (x0 + 250, ground - 4, 72, 18),
                           (x0 + 160, ground - 16, 54, 13)]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                  fill=(226, 226, 226))
    # Rocket, centred in the panel.
    cx = (x0 + x1) // 2
    nose_y = y0 + 34
    body_top = y0 + 78
    body_bottom = ground - 44
    half = 26
    # Fins.
    d.polygon([(cx - half, body_bottom - 34), (cx - half, body_bottom),
               (cx - 62, body_bottom)], fill=RED)
    d.polygon([(cx + half, body_bottom - 34), (cx + half, body_bottom),
               (cx + 62, body_bottom)], fill=RED)
    # Body and nose.
    d.rectangle([cx - half, body_top, cx + half, body_bottom],
                fill=(245, 245, 245), outline=NAVY, width=2)
    d.polygon([(cx - half, body_top), (cx + half, body_top),
               (cx, nose_y)], fill=RED)
    # Red band and window.
    d.rectangle([cx - half, body_top + 62, cx + half, body_top + 78],
                fill=RED)
    d.ellipse([cx - 11, body_top + 22, cx + 11, body_top + 44],
              fill=(120, 180, 220), outline=NAVY, width=2)
    # Flame.
    fy = body_bottom
    d.polygon([(cx - 14, fy), (cx + 14, fy), (cx, fy + 34)],
              fill=(240, 120, 20))
    d.polygon([(cx - 7, fy), (cx + 7, fy), (cx, fy + 20)],
              fill=(250, 210, 60))
    # Thin exhaust trail curving up to the left.
    for i in range(9):
        t = i / 8
        ex = cx - 58 - int(46 * t)
        ey = nose_y + int((body_bottom - nose_y) * t * 0.55)
        r = 3 + int(3 * t)
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 34
    right = W - mx
    cw = right - mx

    # ---- Masthead ----
    d.text((W // 2, 28), "ONE DAY  \u2022  ONE PAGE  \u2022  THE WORLD'S NEWS",
           font=font(SANS_BOLD, 19), fill=GREY, anchor="ma")
    d.text((W // 2, 54), "WORLD NEWS",
           font=font(SERIF_BOLD, 88), fill=NAVY, anchor="ma")
    d.text((W // 2, 150), "WEDNESDAY  25  NOVEMBER  2026",
           font=font(SANS_BOLD, 30), fill=RED, anchor="ma")
    d.line([(mx, 194), (right, 194)], fill=INK, width=4)
    d.line([(mx, 200), (right, 200)], fill=INK, width=1)

    # ---- Lead story: full-width panel ----
    top, bottom = 212, 500
    d.rectangle([mx, top, right, bottom], outline=NAVY, width=3)
    art_x0, art_y0 = right - 358, top + 14
    art_x1, art_y1 = right - 14, bottom - 40
    draw_rocket_panel(d, art_x0, art_y0, art_x1, art_y1)
    d.rectangle([art_x0, art_y0, art_x1, art_y1], outline=NAVY, width=2)
    d.text(((art_x0 + art_x1) // 2, bottom - 32),
           "SHENZHOU-24  \u2022  JIUQUAN, CHINA",
           font=font(SANS_BOLD, 14), fill=NAVY, anchor="ma")

    tx = mx + 16
    tw = art_x0 - tx - 18
    d.text((tx, top + 14), "SPACE  \u2022  CHINA",
           font=font(SANS_BOLD, 20), fill=RED)
    y = headline_block(d, tx, top + 46,
                       "First Pakistani in orbit as China's Shenzhou-24 lifts off",
                       font(SERIF_BOLD, 35), tw, INK)
    y += 8
    draw_wrapped(d, tx, y,
                 "Zeeshan Ali, 40, a Pakistan Air Force pilot, is "
                 "set to become the first foreign astronaut aboard "
                 "China's Tiangong station. The crew launched at "
                 "08:18 from Jiuquan for 5 to 10 days of experiments.",
                 font(SANS, 20), tw, INK, spacing=3)

    # ---- Middle row: two stories ----
    d.line([(mx, 512), (right, 512)], fill=INK, width=2)
    mid_y = 524
    col_w = (cw - 28) // 2
    lx, rx = mx, mx + col_w + 28
    d.line([(mx + col_w + 14, mid_y), (mx + col_w + 14, 700)],
           fill=GREY, width=1)

    # Left: Red Sea
    d.text((lx, mid_y), "MIDDLE EAST  \u2022  RED SEA",
           font=font(SANS_BOLD, 19), fill=RED)
    y = headline_block(d, lx, mid_y + 28,
                       "Houthis threaten Jeddah and Saudi Red Sea ports",
                       font(SERIF_BOLD, 28), col_w, INK)
    draw_wrapped(d, lx, y + 6,
                 "Warning came if Riyadh attacks Hodeidah; "
                 "coalition struck targets there on Wednesday.",
                 font(SANS, 19), col_w, INK, spacing=4)

    # Right: markets
    d.text((rx, mid_y), "MARKETS  \u2022  ASIA",
           font=font(SANS_BOLD, 19), fill=RED)
    y = headline_block(d, rx, mid_y + 28,
                       "Asian stocks fall as new US tariff threat looms",
                       font(SERIF_BOLD, 28), col_w, INK)
    draw_wrapped(d, rx, y + 6,
                 "Chip shares led falls after reports of new US "
                 "tariff findings; Nvidia fell 5.9%.",
                 font(SANS, 19), col_w, INK, spacing=4)

    # ---- Bottom row: two boxed stories ----
    d.line([(mx, 712), (right, 712)], fill=INK, width=2)
    box_y, box_h = 724, 204
    for bx, header in [(lx, "TECH & LAW  \u2022  UNITED STATES"),
                       (rx, "SOCIETY  \u2022  UNITED NATIONS")]:
        d.rectangle([bx, box_y, bx + col_w, box_y + box_h], outline=INK,
                    width=2)
        d.rectangle([bx, box_y, bx + col_w, box_y + 34], fill=NAVY)
        d.text((bx + 12, box_y + 6), header,
               font=font(SANS_BOLD, 18), fill=(255, 255, 255))
    # Huawei story
    y = headline_block(d, lx + 12, box_y + 44,
                       "US jury convicts Huawei on 10 of 12 counts",
                       font(SERIF_BOLD, 25), col_w - 24, INK)
    draw_wrapped(d, lx + 12, y + 6,
                 "Brooklyn jury found fraud and trade-secret theft "
                 "over Iran business; Huawei was cleared of "
                 "racketeering.",
                 font(SANS, 19), col_w - 24, INK, spacing=4)
    # UN femicide story
    y = headline_block(d, rx + 12, box_y + 44,
                       "UN: five women killed every hour by partner or relative",
                       font(SERIF_BOLD, 25), col_w - 24, INK)
    draw_wrapped(d, rx + 12, y + 6,
                 "47,000 women and girls were killed in 2025, UN "
                 "Women and UNODC said, as 16 Days of Activism begins.",
                 font(SANS, 19), col_w - 24, INK, spacing=4)

    # ---- Footer strip ----
    d.line([(mx, 938), (right, 938)], fill=INK, width=1)
    d.text((W // 2, 946),
           "ALSO: Chess Game 2 today in Geneva \u2014 Gukesh has White after Game 1 draw",
           font=font(SANS_BOLD, 19), fill=NAVY, anchor="ma")
    d.text((W // 2, 972),
           "Shanghai pledges loyalty as party chief Chen is probed  \u2022  Russian strike kills two in Odesa, governor says",
           font=font(SANS, 16), fill=GREY, anchor="ma")
    d.text((W // 2, 994),
           "Stories reported on 25 November 2026  \u2022  Sources: Reuters, UN Women, FIDE",
           font=font(SANS, 14), fill=GREY, anchor="ma")

    out = "entry.png"
    img.save(out, optimize=True)
    print(f"saved {out} {img.size}")


if __name__ == "__main__":
    main()

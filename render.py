"""Render the November 17, 2026 world front page as entry.png.

Draws a newspaper front page with Pillow: masthead, six verified stories
from Tuesday, November 17, 2026, a ticker of the day's other headlines,
and simple vector-style icons drawn with PIL primitives (no photos, no
AI-generated art, so every word stays crisp and legible).

Run:  python3 render.py
Writes: entry.png  (1024 x 1024, under 1 MiB)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 234, 255)
CARD = (255, 255, 255, 255)
INK = (20, 20, 20, 255)
MUTED = (74, 74, 74, 255)
NAVY = (14, 42, 71, 255)
NAVY_LIGHT = (27, 68, 105, 255)
RED = (176, 30, 36, 255)
GOLD = (200, 162, 74, 255)
GOLD_LIGHT = (232, 203, 124, 255)
TEAL = (18, 110, 105, 255)
STEEL = (58, 96, 128, 255)
RULE = (196, 188, 172, 255)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


# ---------------------------------------------------------------- icons

def icon_buildings(draw, box, bg):
    """City skyline with a red prohibition slash: sanctions."""
    x0, y0, x1, y1 = box
    rounded(draw, box, 14, bg)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    # buildings, white silhouettes
    bw = (x1 - x0) // 5
    heights = [0.42, 0.62, 0.5, 0.72, 0.55]
    base = y1 - 26
    for i, h in enumerate(heights):
        bx = x0 + 14 + i * (bw - 2)
        bh = int((y1 - y0 - 52) * h)
        draw.rectangle([bx, base - bh, bx + bw - 8, base], fill=(255, 255, 255, 255))
    # windows
    for i in range(5):
        bx = x0 + 14 + i * (bw - 2)
        draw.rectangle([bx + 4, base - 26, bx + bw - 12, base - 18], fill=bg)
    # red prohibition ring + slash over the skyline
    r = int((x1 - x0) * 0.34)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=9)
    draw.line([cx - r + 8, cy + r - 8, cx + r - 8, cy - r + 8], fill=RED, width=9)


def icon_bridge(draw, box, bg):
    """Suspension bridge: deck, towers, cables."""
    x0, y0, x1, y1 = box
    rounded(draw, box, 12, bg)
    w, h = x1 - x0, y1 - y0
    deck_y = y0 + int(h * 0.72)
    draw.line([x0 + 8, deck_y, x1 - 8, deck_y], fill=(255, 255, 255, 255), width=6)
    # towers
    for tx in (x0 + int(w * 0.26), x0 + int(w * 0.72)):
        draw.line([tx, y0 + int(h * 0.22), tx, deck_y], fill=(255, 255, 255, 255), width=6)
        draw.line([tx - 12, y0 + int(h * 0.22), tx + 12, y0 + int(h * 0.22)],
                  fill=(255, 255, 255, 255), width=5)
    # main cable arc
    pts = []
    for i in range(41):
        t = i / 40.0
        x = x0 + 8 + t * (w - 16)
        y = y0 + int(h * 0.22) + int(math.sin(t * math.pi) * h * 0.34)
        pts.append((x, y))
    draw.line(pts, fill=GOLD_LIGHT, width=4)
    # hangers
    for t in (0.2, 0.35, 0.5, 0.65, 0.8):
        x = x0 + 8 + t * (w - 16)
        y = y0 + int(h * 0.22) + int(math.sin(t * math.pi) * h * 0.34)
        draw.line([x, y, x, deck_y], fill=(255, 255, 255, 255), width=2)
    # sun
    draw.ellipse([x1 - 34, y0 + 10, x1 - 14, y0 + 30], fill=GOLD_LIGHT)


def icon_jet(draw, box, bg):
    """Fighter jet, nose up-right."""
    x0, y0, x1, y1 = box
    rounded(draw, box, 12, bg)
    w, h = x1 - x0, y1 - y0
    # fuselage delta
    draw.polygon([
        (x0 + int(w * 0.82), y0 + int(h * 0.18)),
        (x0 + int(w * 0.30), y0 + int(h * 0.55)),
        (x0 + int(w * 0.42), y0 + int(h * 0.66)),
        (x0 + int(w * 0.62), y0 + int(h * 0.80)),
        (x0 + int(w * 0.72), y0 + int(h * 0.72)),
    ], fill=(255, 255, 255, 255))
    # main wing
    draw.polygon([
        (x0 + int(w * 0.48), y0 + int(h * 0.48)),
        (x0 + int(w * 0.16), y0 + int(h * 0.86)),
        (x0 + int(w * 0.30), y0 + int(h * 0.88)),
        (x0 + int(w * 0.60), y0 + int(h * 0.62)),
    ], fill=GOLD_LIGHT)
    # tail fin
    draw.polygon([
        (x0 + int(w * 0.52), y0 + int(h * 0.55)),
        (x0 + int(w * 0.38), y0 + int(h * 0.34)),
        (x0 + int(w * 0.48), y0 + int(h * 0.30)),
        (x0 + int(w * 0.62), y0 + int(h * 0.52)),
    ], fill=(255, 255, 255, 255))
    # motion lines
    for i, yy in enumerate((0.30, 0.44, 0.58)):
        draw.line([x0 + 10, y0 + int(h * yy), x0 + int(w * (0.30 - i * 0.05)),
                   y0 + int(h * yy)], fill=(255, 255, 255, 255), width=3)


def icon_flame(draw, box, bg):
    """Oil flame over a drop: energy / Hormuz tanker."""
    x0, y0, x1, y1 = box
    rounded(draw, box, 12, bg)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    # outer flame
    draw.polygon([
        (cx, y0 + 14),
        (cx + 26, cy - 6),
        (cx + 18, cy + 22),
        (cx, y1 - 16),
        (cx - 18, cy + 22),
        (cx - 26, cy - 6),
    ], fill=(255, 176, 32, 255))
    # inner flame
    draw.polygon([
        (cx, cy - 2),
        (cx + 13, cy + 12),
        (cx + 8, cy + 30),
        (cx, y1 - 24),
        (cx - 8, cy + 30),
        (cx - 13, cy + 12),
    ], fill=(255, 255, 255, 255))
    # waves below
    for yy in (y1 - 14, y1 - 8):
        draw.arc([x0 + 14, yy - 6, x1 - 14, yy + 6], 0, 180, fill=(255, 255, 255, 255), width=3)


def icon_gavel(draw, box, bg):
    """Judge's gavel, diagonal."""
    x0, y0, x1, y1 = box
    rounded(draw, box, 12, bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    ang = math.radians(-38)
    ca, sa = math.cos(ang), math.sin(ang)

    def rot(px, py):
        return (cx + px * ca - py * sa, cy + px * sa + py * ca)

    # handle
    hx0, hy0 = rot(-34, 3)
    hx1, hy1 = rot(34, -3)
    draw.line([hx0, hy0, hx1, hy1], fill=(255, 255, 255, 255), width=7)
    # head
    head = [rot(-16, -26), rot(16, -26), rot(16, -12), rot(-16, -12)]
    draw.polygon(head, fill=GOLD_LIGHT)
    # sound block
    draw.line([rot(-26, 22), rot(26, 22)], fill=(255, 255, 255, 255), width=6)
    draw.line([rot(-20, 30), rot(20, 30)], fill=(255, 255, 255, 255), width=4)


def icon_globe(draw, box, bg):
    """Globe with meridians: climate summit."""
    x0, y0, x1, y1 = box
    rounded(draw, box, 12, bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = int(min(x1 - x0, y1 - y0) * 0.36)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 255), width=4)
    draw.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
                 outline=(255, 255, 255, 255), width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255, 255), width=3)
    draw.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)], 0, 180,
             fill=(255, 255, 255, 255), width=3)
    draw.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)], 180, 360,
             fill=(255, 255, 255, 255), width=3)
    # leaf
    lx, ly = x1 - 26, y1 - 26
    draw.pieslice([lx - 14, ly - 14, lx + 14, ly + 14], 200, 20, fill=GOLD_LIGHT)


# ---------------------------------------------------------------- page

def story_panel(draw, box, kicker, headline, deck, icon, bg,
                head_size, deck_size, kick_size=17):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CARD)
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    pad = 16
    if icon is None:
        # slim accent bar on top; headline gets the full width
        draw.rectangle([x0, y0, x1, y0 + 6], fill=bg)
        text_w = (x1 - x0) - pad * 2
        kx, ky = x0 + pad, y0 + pad + 2
    else:
        ix0 = x1 - pad - 92
        iy0 = y0 + pad
        icon_box = (ix0, iy0, ix0 + 92, iy0 + 92)
        icon(draw, icon_box, bg)
        text_w = (x1 - x0) - pad * 2 - 92 - 14
        kx, ky = x0 + pad, y0 + pad
    draw.text((kx, ky), kicker, font=font(SANS_BLACK, kick_size), fill=RED)
    hy = ky + kick_size + 10
    head_f = font(SERIF, head_size)
    lines = wrap(draw, headline, head_f, text_w)
    hy = draw_lines(draw, lines, kx, hy, head_f, INK, head_size + 7)
    dy = hy + 8
    deck_f = font(SANS, deck_size)
    deck_lines = wrap(draw, deck, deck_f, (x1 - x0) - pad * 2)
    draw_lines(draw, deck_lines, kx, dy, deck_f, MUTED, deck_size + 7)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- top red rule + navy masthead
    draw.rectangle([0, 0, W, 10], fill=RED)
    draw.rectangle([0, 10, W, 158], fill=NAVY)
    name_f = font(SERIF, 58)
    name = "THE DAILY GLOBE"
    draw.text(((W - draw.textlength(name, font=name_f)) / 2, 24),
              name, font=name_f, fill=(255, 255, 255, 255))
    draw.line([90, 100, W - 90, 100], fill=GOLD, width=2)
    date_f = font(SANS_BOLD, 30)
    date = "TUESDAY, NOVEMBER 17, 2026"
    draw.text(((W - draw.textlength(date, font=date_f)) / 2, 110),
              date, font=date_f, fill=GOLD_LIGHT)
    side_f = font(SANS_BOLD, 15)
    draw.text((30, 122), "WORLD EDITION", font=side_f, fill=(255, 255, 255, 255))
    right = "SIX STORIES  •  ONE DAY"
    draw.text((W - 30 - draw.textlength(right, font=side_f), 122),
              right, font=side_f, fill=(255, 255, 255, 255))

    # ---- lead story: UK sanctions
    lx0, ly0, lx1, ly1 = 28, 170, W - 28, 444
    draw.rectangle([lx0, ly0, lx1, ly1], fill=CARD)
    draw.rectangle([lx0, ly0, lx1, ly1], outline=RULE, width=1)
    draw.rectangle([lx0, ly0, lx0 + 10, ly1], fill=RED)
    pad = 22
    icon_buildings(draw, (lx1 - pad - 190, ly0 + 30, lx1 - pad, ly0 + 220), NAVY_LIGHT)
    kx, ky = lx0 + pad + 10, ly0 + 18
    draw.text((kx, ky), "MIDDLE EAST  —  LEAD STORY", font=font(SANS_BLACK, 19), fill=RED)
    head_f = font(SERIF, 42)
    head = "Britain sanctions Israeli settlement firms over the West Bank"
    lines = wrap(draw, head, head_f, (lx1 - lx0) - pad * 2 - 10 - 190 - 18)
    hy = draw_lines(draw, lines, kx, ky + 34, head_f, INK, 50)
    deck_f = font(SANS, 22)
    deck = ("London blacklists eight construction companies and an activist group "
            "accused of blocking aid to Gaza. Israel calls the move a \u201chostile act\u201d.")
    deck_lines = wrap(draw, deck, deck_f, (lx1 - lx0) - pad * 2 - 10)
    draw_lines(draw, deck_lines, kx, hy + 12, deck_f, MUTED, 29)

    # ---- row 2: two stories
    y2, h2 = 456, 226
    w2 = (W - 28 * 2 - 14) // 2
    story_panel(draw, (28, y2, 28 + w2, y2 + h2),
                "WAR IN UKRAINE",
                "Ukraine strikes Kerch Bridge; Russia hits Kyiv bridges",
                "The Crimean link is closed after an overnight strike; Moscow "
                "answers with strikes on Kyiv bridges.",
                icon_bridge, STEEL, 28, 17)
    story_panel(draw, (28 + w2 + 14, y2, W - 28, y2 + h2),
                "ASIA  —  SECURITY",
                "Japan scrambles jets as Russian planes enter its airspace",
                "Tokyo protests strongly after two suspected Russian aircraft "
                "enter Japanese airspace.",
                icon_jet, NAVY_LIGHT, 28, 17)

    # ---- row 3: three stories
    y3, h3 = 694, 196
    w3 = (W - 28 * 2 - 14 * 2) // 3
    story_panel(draw, (28, y3, 28 + w3, y3 + h3),
                "U.S.  —  IRAN",
                "Fourth tanker hits mine in Hormuz",
                "Iran reports the blast; Guards say a U.S. drone was seized.",
                None, (146, 44, 32, 255), 26, 17, kick_size=15)
    story_panel(draw, (28 + w3 + 14, y3, 28 + w3 * 2 + 14, y3 + h3),
                "FRANCE  —  COURTS",
                "Depardieu admits assault charge",
                "The French star drops his appeal in Paris and pleads guilty.",
                None, (96, 74, 42, 255), 26, 17, kick_size=15)
    story_panel(draw, (28 + w3 * 2 + 28, y3, W - 28, y3 + h3),
                "CLIMATE  —  COP31",
                "COP31: faster fossil exit, $120bn",
                "Antalya deal text raises climate aid for developing nations.",
                None, TEAL, 26, 17, kick_size=15)

    # ---- ticker strip
    ty0, ty1 = 902, 964
    draw.rectangle([28, ty0, W - 28, ty1], fill=NAVY)
    tick_f = font(SANS_BOLD, 16)
    tick = ("ALSO TODAY:   FAA halts router rollout   •   Ex-Nvidia chief Huang: "
            "\u201cI'd return if asked\u201d   •   AI stocks lead Wall Street slide   •   "
            "JPMorgan blames bug for outage   •   Mongolia's president resigns   •   "
            "Trump heads to Asia for Xi\u2013Putin summit")
    tick_lines = wrap(draw, tick, tick_f, (W - 28 * 2) - 24)
    ty = ty0 + 8
    for line in tick_lines[:2]:
        draw.text((40, ty), line, font=tick_f, fill=(255, 255, 255, 255))
        ty += 24

    # ---- footer
    foot_f = font(SANS, 17)
    foot = "All events happened or were first reported on Tuesday, November 17, 2026."
    draw.text(((W - draw.textlength(foot, font=foot_f)) / 2, 974),
              foot, font=foot_f, fill=MUTED)
    foot2_f = font(SANS_BOLD, 14)
    foot2 = "THE DAILY GLOBE  •  WORLD FRONT PAGE"
    draw.text(((W - draw.textlength(foot2, font=foot2_f)) / 2, 998),
              foot2, font=foot2_f, fill=(140, 132, 116, 255))

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

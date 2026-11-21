#!/usr/bin/env python3
"""Draw the 21 November 2026 one-day world-news infographic with PIL.

Cream newspaper layout at 1024x1024: masthead naming the day, four big
illustrated stories, twelve medium stories, an "Also on Saturday" column of
one-liners, a UTC timeline strip and a DATE CHECK footer. Everything is drawn
programmatically (no external images, no network), so the output bytes are
deterministic. Writes entry.png next to this script.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 240, 221)
INK = (26, 24, 20)
MUTED = (96, 90, 78)
RULE = (150, 142, 122)
RED = (163, 22, 33)
NAVY = (29, 53, 87)
GOLD = (184, 134, 11)
PANEL = (238, 231, 210)
PANEL_DARK = (32, 40, 58)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_MAST = font(SERIF_B, 56)
F_DATE = font(SERIF_B, 27)
F_SUB = font(SANS, 12)
F_SECT = font(SANS_B, 13)
F_BIG_H = font(SERIF_B, 17)
F_MED_H = font(SERIF_B, 14)
F_BODY = font(SERIF, 11)
F_BODY_S = font(SERIF, 10)
F_TAG = font(SANS_B, 8)
F_LINE = font(SERIF, 11)
F_LINE_B = font(SERIF_B, 11)
F_TIME = font(SANS_B, 10)
F_TIME_S = font(SANS, 9)
F_FOOT_H = font(SANS_B, 11)
F_FOOT = font(SERIF, 10)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def tag(draw, x, y, text, fill=RED):
    draw.text((x, y), text.upper(), font=F_TAG, fill=fill)


def section_head(draw, x, y, text, x2):
    draw.line([(x, y + 8), (x2, y + 8)], fill=RULE, width=1)
    spaced = " ".join(text.upper())
    tw = draw.textlength(spaced, font=F_SECT)
    draw.rectangle([x, y, x + tw + 10, y + 17], fill=PAPER)
    draw.text((x, y + 1), spaced, font=F_SECT, fill=NAVY)


# ---------------------------------------------------------------- illustrations
def ill_poland(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_DARK)
    # rough Poland outline
    pts = [(x + 60, y + 12), (x + 120, y + 8), (x + 175, y + 18), (x + 195, y + 42),
           (x + 180, y + 66), (x + 130, y + 74), (x + 80, y + 70), (x + 55, y + 45)]
    draw.polygon(pts, outline=(240, 240, 230), width=2)
    draw.text((x + 100, y + 34), "POLAND", font=F_TAG, fill=(240, 240, 230))
    # missile arcs from the east
    for i, (sx, sy) in enumerate([(x + 232, y + 10), (x + 236, y + 30), (x + 230, y + 50)]):
        ex, ey = x + 150 - i * 18, y + 30 + i * 10
        draw.arc([min(sx, ex), min(sy, ey) - 14, max(sx, ex), max(sy, ey) + 14],
                 start=180, end=330, fill=RED, width=2)
        draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 180, 60))
    draw.text((x + 196, y + 62), "RU", font=F_TAG, fill=(255, 120, 120))


def ill_summit(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL)
    # table
    draw.rectangle([x + 30, y + h - 20, x + w - 30, y + h - 13], fill=(110, 80, 50))
    draw.rectangle([x + 42, y + h - 13, x + 50, y + h - 4], fill=(110, 80, 50))
    draw.rectangle([x + w - 50, y + h - 13, x + w - 42, y + h - 4], fill=(110, 80, 50))
    flags = [("US", (60, 60, 140)), ("CN", (200, 30, 30)), ("RU", (240, 240, 240))]
    for i, (label, col) in enumerate(flags):
        fx = x + 48 + i * 72
        draw.line([(fx, y + 8), (fx, y + h - 20)], fill=INK, width=2)
        draw.rectangle([fx, y + 8, fx + 34, y + 26], fill=col, outline=INK)
        if label == "RU":
            draw.rectangle([fx, y + 14, fx + 34, y + 20], fill=(40, 80, 180))
            draw.rectangle([fx, y + 20, fx + 34, y + 26], fill=(200, 30, 30))
        if label == "US":
            for r in range(3):
                draw.line([(fx, y + 11 + r * 5), (fx + 34, y + 11 + r * 5)], fill=(255, 255, 255), width=2)
        draw.text((fx + 8, y + 29), label, font=F_TAG, fill=INK)


def ill_market(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 248, 240), outline=RULE)
    for gy in range(y + 14, y + h - 6, 16):
        draw.line([(x + 10, gy), (x + w - 10, gy)], fill=(225, 220, 200), width=1)
    pts = [(x + 14, y + 18), (x + 50, y + 26), (x + 84, y + 22), (x + 118, y + 38),
           (x + 150, y + 34), (x + 182, y + 52), (x + 216, y + 66)]
    draw.line(pts, fill=RED, width=3)
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    draw.polygon([(x + 216, y + 66), (x + 206, y + 58), (x + 208, y + 70)], fill=RED)
    draw.text((x + 150, y + 10), "-3.7%", font=font(SANS_B, 15), fill=RED)
    draw.text((x + 12, y + h - 16), "S&P 500 · DOW", font=F_TAG, fill=MUTED)


def ill_riyadh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_DARK)
    # skyline
    base = y + h - 8
    towers = [(14, 26), (34, 40), (58, 30), (82, 52), (108, 34), (132, 44), (158, 28), (182, 38), (206, 30)]
    for tx, th in towers:
        draw.rectangle([x + tx, base - th, x + tx + 16, base], fill=(90, 100, 130))
        for wy in range(base - th + 5, base - 4, 8):
            draw.rectangle([x + tx + 4, wy, x + tx + 7, wy + 3], fill=(255, 220, 120))
    # shield arc + intercepted bursts
    draw.arc([x + 20, y + 4, x + w - 20, y + h + 30], start=200, end=340, fill=(120, 200, 255), width=3)
    for bx, by in [(x + 70, y + 18), (x + 130, y + 10), (x + 185, y + 20)]:
        for dx, dy in [(-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)]:
            draw.line([(bx, by), (bx + dx, by + dy)], fill=(255, 180, 60), width=2)
        draw.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(255, 230, 150))


# ---------------------------------------------------------------- content
BIG = [
    (ill_poland, "Russian missiles come down in Poland",
     "Two Russian missiles and a suspected drone fell on Polish soil. Warsaw called it a deliberate provocation; NATO called it a grave violation of its airspace, and Poland asked for more NATO support.",
     "OneTurn · Warsaw"),
    (ill_summit, "Trump, Xi and Putin meet — few results",
     "The first Trump–Xi–Putin trilateral summit in Shenzhen ended with a symbolic declaration against nuclear war and few concrete deals. Trump called Putin “a friend of mine”.",
     "OneTurn · Shenzhen"),
    (ill_market, "Wall Street slumps into correction",
     "US stocks fell about 3.7% on Friday as AI and chip shares sold off, pushing the S&P 500 and the Dow into correction territory.",
     "OneTurn · New York"),
    (ill_riyadh, "Houthi missiles intercepted over Riyadh",
     "The Saudi-led coalition said it destroyed three Houthi ballistic missiles fired at Riyadh and struck Hodeidah. Debris caused material damage in the capital.",
     "Arab Coalition · Riyadh"),
]

MEDIUM = [
    ("Tanker ablaze in Strait of Hormuz",
     "A tanker was hit by an unknown projectile and caught fire 8 nautical miles north of Khasab, near Oman.", "UKMTO"),
    ("Denmark foils 'Russian' assassination plot",
     "Danish intelligence said it thwarted a plot to kill Ukrainian rapper Kyivstoner; two Danes were charged with recruitment by Russia.", "PET · Denmark"),
    ("BepiColombo reaches Mercury",
     "After 8 years and 6 billion miles, the ESA–JAXA probe fires its engine today to enter Mercury orbit — the first mission with two orbiters there.", "NPR · ESA/JAXA"),
    ("Pancreatic-cancer pill hailed as breakthrough",
     "Daraxonrasib made tumours undetectable in some patients in a trial, a rare response for the deadly cancer.", "Mogaz"),
    ("Man convicted of starting Palisades Fire",
     "A Los Angeles jury convicted Jonathan Rinderknecht of starting the fire that became the Palisades Fire.", "OneTurn · Los Angeles"),
    ("US approved ~900,000 AI chips for China",
     "The Trump administration approved the sale of nearly 900,000 advanced Nvidia and AMD chips to Chinese firms in six months, a House committee disclosed.", "House Foreign Affairs Cmte"),
    ("Nvidia probes CEO's alleged China link",
     "Nvidia hired a top law firm over claims linking CEO Jensen Huang to an alleged Chinese spy; California's attorney general subpoenaed the firm.", "Munich Eye"),
    ("Russian transport plane crashes in Siberia",
     "All 19 aboard a Russian military transport aircraft died when it crashed in an unpopulated area of western Siberia.", "Russian Defence Ministry"),
    ("Kryvyi Rih strike kills 2, injures 42",
     "Two people were killed and 42 injured, four of them children, in a strike on the Ukrainian city, its military administration said.", "Vilkul · Ukraine"),
    ("New Zealand election too close to call",
     "Preliminary results show a razor-thin lead for PM Luxon's right-wing coalition; special votes are counted on 27 November.", "WH News"),
    ("Fiona the hippo dies at Cincinnati Zoo",
     "Fiona, the famous 9-year-old hippo, died after failing to pass a hat she had ingested more than a week earlier.", "Cincinnati Zoo"),
    ("Muslims to be largest faith by 2035",
     "A Pew Research report projects Muslims will become the world's largest religious group by 2035 and outnumber Christians by 2070.", "Pew Research"),
]

LINES = [
    ("Virginia", "first measles-linked death of 2026, a child under 5.", "VA Health Dept"),
    ("Washington", "four Iranians added to OFAC sanctions over oil revenues.", "US Treasury"),
    ("Brussels", "EU Council adopts €1bn military aid package for Ukraine.", "EU Council"),
    ("London", "UK pledges 1,000+ drones for Ukraine in £260m package.", "UK govt"),
    ("Washington", "US sanctions Comancheros gang and 'Ndrangheta syndicate.", "US Treasury"),
    ("Washington", "Trump announces posthumous pardon for Pete Rose.", "White House"),
    ("Lima", "magnitude 4.0 earthquake shakes region near Ancón.", "Mogaz"),
    ("New York", "JPMorgan: cyberattack on vendors exposed email data.", "Mogaz"),
    ("San Francisco", "Scott Wiener tops primary to succeed Pelosi; Connie Chan second.", "Mogaz"),
    ("Tokyo", "Honda recalls 810,592 vehicles over Takata airbag risk.", "EditUSA"),
    ("Khartoum", "army says RSF strongholds dismantled in 10 West Kordofan areas.", "Binder"),
    ("Mexico", "fresh caravan of ~300 migrants crosses into the south.", "Binder"),
    ("Caracas", "Venezuela rejects ICJ role in Essequibo dispute, seeks talks.", "Binder"),
    ("Baghdad", "Iraq ends Kata'ib Hezbollah's 12-year grip on Jurf al-Sakhar.", "Kspears"),
    ("Kuala Lumpur", "Malaysia–Turkey deal to relocate 10,000 Rohingya.", "Binder"),
    ("Berlin", "SkyFall and Auterion to build drones in Germany for Ukraine.", "Binder"),
    ("Abu Dhabi", "UAE Bulls beat Yas Lions by 24 runs in T10 final.", "Gyan Higyan"),
    ("Kuala Lumpur", "India U17 draw Malaysia 0-0, reach AFC U17 Asian Cup.", "IANS"),
    ("Turin", "Medvedev beats Tiafoe 6-3 6-4 at ATP Finals.", "ScoreZaap"),
    ("Munich", "Bayern held 1-1 by Köln; Espanyol win 1-0 at Athletic.", "ScoreZaap"),
    ("Vandenberg", "SpaceX Falcon 9 USSF-317 rescheduled to 02:32 UTC.", "KeepTrack"),
    ("Washington", "DIA: Russia developing nuclear-armed satellite.", "DIA"),
    ("Houston", "Pegasus lunar rover clears NASA review, eyes 2028 Moon.", "Lunar Outpost"),
    ("Jakarta", "Prabowo and Xi discuss South China Sea cooperation.", "Gruber"),
    ("Kathmandu", "Indian tourist killed as helicopters collide near Everest.", "BBC"),
    ("Hong Kong", "activist Joshua Wong jailed 10 years for foreign collusion.", "WH News"),
]

TIMELINE = [
    ("00:21", "Riyadh debris\nconfirmed"),
    ("02:27", "Kryvyi Rih toll:\n2 dead, 42 hurt"),
    ("02:32", "Falcon 9\nUSSF-317 window"),
    ("03:22", "Prabowo–Xi\ntalks reported"),
    ("03:34", "OFAC Iran\nsanctions out"),
    ("03:50", "Long March 6C\nscheduled"),
    ("Daytime", "BepiColombo\nMercury burn"),
    ("Evening", "NZ results\ntrickle in"),
]

EXCLUDED = [
    "ICJ Myanmar verdict 19 Nov",
    "Voyager 1 light-day 18 Nov",
    "Senate Iran vote 19 Nov",
    "Gibran resigns 19 Nov",
    "Pulsar paper 19 Nov",
    "Genie 4 opens 18 Nov",
]
NOT_YET = [
    "NZ special votes counted — 27 Nov",
    "Cygnus XL ISS resupply launch — 29 Nov",
    "US Congress funding deadline — 11 Dec",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    right = W - M

    # masthead
    d.line([(M, 16), (right, 16)], fill=INK, width=3)
    centered(d, W // 2, 24, "THE DAILY WIRE", F_MAST)
    centered(d, W // 2, 88, "Saturday 21 November 2026", F_DATE, fill=NAVY)
    centered(d, W // 2, 122,
             "42 verified stories from one day of world news · a source on every story",
             F_SUB, fill=MUTED)
    d.line([(M, 142), (right, 142)], fill=INK, width=1)
    d.line([(M, 145), (right, 145)], fill=INK, width=3)

    # big four
    section_head(d, M, 156, "The big four", right)
    col_w = (right - M - 3 * 12) // 4
    y0 = 180
    for i, (ill, head, body, src) in enumerate(BIG):
        x = M + i * (col_w + 12)
        ill(d, x, y0, col_w, 70)
        y = draw_wrapped(d, x, y0 + 76, head, F_BIG_H, col_w, 19, max_lines=2)
        y = draw_wrapped(d, x, y + 2, body, F_BODY, col_w, 13, max_lines=5)
        tag(d, x, y + 3, src)
        if i:
            d.line([(x - 6, y0), (x - 6, y0 + 182)], fill=RULE, width=1)

    # medium twelve
    section_head(d, M, 380, "Also making news", right)
    med_w = (right - M - 2 * 16) // 3
    y0 = 406
    row_h = 72
    for i, (head, body, src) in enumerate(MEDIUM):
        col, row = i % 3, i // 3
        x = M + col * (med_w + 16)
        y = y0 + row * row_h
        y = draw_wrapped(d, x, y, head, F_MED_H, med_w, 16, max_lines=2)
        y = draw_wrapped(d, x, y + 1, body, F_BODY_S, med_w, 12, max_lines=3)
        tag(d, x, y + 2, src)

    # one-liners
    section_head(d, M, 702, "Also on Saturday", right)
    line_w = (right - M - 16) // 2
    y0 = 726
    half = (len(LINES) + 1) // 2
    for col in range(2):
        x = M + col * (line_w + 16)
        y = y0
        for place, text, src in LINES[col * half:(col + 1) * half]:
            lead = place + " — "
            d.text((x, y), lead, font=F_LINE_B, fill=INK)
            lw = d.textlength(lead, font=F_LINE_B)
            rest = text + "  (" + src + ")"
            d.text((x + lw, y), rest, font=F_LINE, fill=INK)
            y += 13

    # UTC timeline
    section_head(d, M, 900, "The day in UTC (as reported)", right)
    ty = 926
    d.line([(M + 6, ty + 6), (right - 6, ty + 6)], fill=NAVY, width=2)
    step = (right - M - 12) / (len(TIMELINE) - 1)
    for i, (t, label) in enumerate(TIMELINE):
        cx = M + 6 + i * step
        d.ellipse([cx - 4, ty + 2, cx + 4, ty + 10], fill=RED)
        centered(d, cx, ty + 13, t, F_TIME, fill=NAVY)
        for j, part in enumerate(label.split("\n")):
            centered(d, cx, ty + 26 + j * 10, part, F_TIME_S, fill=INK)

    # date check footer
    fy = 980
    d.rectangle([M, fy, right, fy + 38], outline=NAVY, width=1)
    d.text((M + 8, fy + 3), "DATE CHECK — deliberately left out (happened before 21 Nov):",
           font=F_FOOT_H, fill=NAVY)
    ex = " · ".join(EXCLUDED)
    draw_wrapped(d, M + 8, fy + 16, ex, F_FOOT, right - M - 16, 11, max_lines=1)
    ny = "Not yet news: " + " · ".join(NOT_YET)
    draw_wrapped(d, M + 8, fy + 27, ny, F_FOOT, right - M - 16, 11, max_lines=1)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()

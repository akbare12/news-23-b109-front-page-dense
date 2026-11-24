#!/usr/bin/env python3
"""news-23 b109 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def f(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = f(FL + "LiberationSerif-Bold.ttf", 44)
SANS_B = lambda s: f(FD + "DejaVuSans-Bold.ttf", s)
SANS = lambda s: f(FD + "DejaVuSans.ttf", s)

BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
RED = (176, 0, 32)
DARKRED = (140, 20, 20)
NAVY = (31, 56, 100)
GREEN = (30, 132, 73)
TEAL = (14, 98, 98)
GRAY = (97, 106, 107)
LGRAY = (234, 234, 234)
BLUE = (26, 82, 118)
MAPGREEN = (200, 230, 160)
CREAM = (250, 243, 224)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, font, fill=BLACK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def center(x0, x1, y, s, font, fill=BLACK):
    text((x0 + x1) / 2, y, s, font, fill, anchor="ma")


# ---------- masthead ----------
d.rectangle([0, 0, W, 56], fill=BLACK)
text(16, 6, "THE WORLD TODAY", SERIF_B, WHITE)
text(W - 16, 20, "MONDAY 23 NOVEMBER 2026", SANS_B(15), GOLD, anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 56, W, 76], fill=RED)
center(0, W, 60, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       SANS_B(13), WHITE)

# ---------- number strip: 2 rows x 5 cols, pitch 28 ----------
strip = [
    [("\u22123.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", BLACK),
     ("11,762", "EBOLA CASES, DRC", BLACK), ("10T won", "SEOUL STABILISATION FUND", BLACK),
     ("2%", "BILLIONAIRE TAX IN PARIS", BLACK)],
    [("$450M", "SKUBAL DEAL", BLACK), ("165", "RUSSIAN MISSILES/WEEK", BLACK),
     ("12,000", "CLEARED IN MANCHESTER", BLACK), ("264 kg", "EXPLOSIVES SEIZED", BLACK),
     ("$107.3B", "ANTHROPIC IPO", BLACK)],
]
cw = W // 5
for r, row in enumerate(strip):
    y0 = 76 + r * 27
    for c, (val, lab, col) in enumerate(row):
        x0 = c * cw
        text(x0 + 10, y0 + 1, val, SANS_B(15), col)
        text(x0 + 10, y0 + 17, lab, SANS(8), GRAY)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", 7, (176, 58, 46)), ("AMERICAS 8", 8, (146, 43, 33)),
           ("MIDDLE EAST 6", 6, (183, 149, 11)), ("EUROPE 5", 5, NAVY),
           ("AFRICA 3", 3, GREEN), ("WORLD 2", 2, GRAY)]
x = 0
for name, n, col in regions:
    w = round(n / 31 * W)
    d.rectangle([x, 132, x + w, 150], fill=col)
    center(x, x + w, 136, name, SANS_B(11), WHITE)
    x += w

# ---------- UTC strip ----------
d.rectangle([0, 150, W, 166], fill=LGRAY)
text(10, 153, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     SANS(10), BLACK)
text(W - 10, 153, "~ APPROX", SANS(10), GRAY, anchor="ra")

# ---------- hero scenes ----------
HX = [8, 348, 688]
HW = 328


def kospi_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 32, 64))
    # skyline
    import random
    rnd = random.Random(23)
    bx = x0 + 8
    while bx < x0 + w - 30:
        bw = rnd.randint(18, 30)
        bh = rnd.randint(35, 80)
        d.rectangle([bx, y0 + h - bh, bx + bw, y0 + h], fill=(24, 48, 90),
                    outline=(60, 90, 140))
        for wy in range(y0 + h - bh + 6, y0 + h - 4, 9):
            for wx in range(bx + 4, bx + bw - 3, 7):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # descending chart line
    pts = []
    for i in range(7):
        px = x0 + 14 + i * (w - 28) / 6
        py = y0 + 34 + i * (h - 60) / 6 + rnd.randint(-4, 4)
        pts.append((px, py))
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE, outline=(255, 140, 40))
    text(x0 + 12, y0 + 6, "\u22123.3%", SANS_B(26), WHITE)


def guterres_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(20, 70, 45))
    lines = ["150", "DELEGATES", "BACK A RISK", "FRAMEWORK"]
    for i, ln in enumerate(lines):
        col = GOLD if i > 0 else (255, 214, 90)
        sz = 30 if i == 0 else 20
        text(x0 + 12, y0 + 8 + i * 26, ln, SANS_B(sz), col)
    # globe
    cx, cy, r = x0 + w - 62, y0 + h // 2 + 6, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 240, 200), outline=(150, 210, 150), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(140, 190, 140))
    d.line([cx - r, cy, cx + r, cy], fill=(140, 190, 140))
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(140, 190, 140))


def power_scene(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    text(x0 + 10, y0 + 6, "NARROWEST SINCE 2018", SANS_B(11), BLACK)
    text(x0 + w - 10, y0 + 6, "GAP 5.3", SANS_B(12), RED, anchor="ra")
    bars = [("78.9", "US", NAVY, 0.789), ("73.6", "CHINA", RED, 0.736), ("40.5", "INDIA", (183, 149, 11), 0.405)]
    bw = 62
    gap = (w - 3 * bw - 20) / 2
    base = y0 + h - 8
    for i, (val, lab, col, frac) in enumerate(bars):
        bx = x0 + 10 + i * (bw + gap)
        bh = int((h - 52) * frac)
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
        text(bx + bw / 2, base - bh - 20, val, SANS_B(15), BLACK, anchor="ma")
        text(bx + bw / 2, base - 16, lab, SANS_B(10), WHITE, anchor="ma")


heroes = [
    (kospi_scene, "KOSPI 4,708.54  \u00b7  \u2212161 PTS", "AI ROUT HITS ASIA",
     "Kospi closes \u22123.3% to 4,708.54, sheds 161 pts; intraday \u22125.8%. Samsung \u22123.1%, SK Hynix \u22122.5%.",
     "KOREA EXCHANGE"),
    (guterres_scene, "UN  \u00b7  BRIDGETOWN", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    (power_scene, "ASIA POWER INDEX 2026", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]

for i, (scene, strip_txt, head, body, src) in enumerate(heroes):
    x0 = HX[i]
    scene(x0, 166, HW, 122)
    d.rectangle([x0, 288, x0 + HW, 306], fill=BLACK)
    text(x0 + 8, 291, strip_txt, SANS_B(10), WHITE)
    lines = wrap(head, SANS_B(20), HW - 8)
    for j, ln in enumerate(lines):
        text(x0 + 2, 312 + j * 22, ln, SANS_B(20), BLACK)
    blines = wrap(body, SANS(11), HW - 4)
    for j, ln in enumerate(blines[:2]):
        text(x0 + 2, 402 + j * 14, ln, SANS(11), BLACK)
    text(x0 + 2, 434, src, SANS(9), GRAY)
    d.rectangle([x0 + HW - 74, 430, x0 + HW - 2, 446], fill=BLUE)
    center(x0 + HW - 74, x0 + HW - 2, 433, "REPORTED", SANS_B(9), WHITE)

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 450, W, 470], fill=BLACK)
text(10, 454, "MORE OF THE DAY  \u2014  10 STORIES", SANS_B(12), WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", (176, 58, 46), "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", NAVY, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", TEAL, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", GREEN, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", (202, 108, 20), "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", (202, 108, 20), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", (108, 52, 131), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", (14, 98, 98), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", NAVY, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (74, 60, 140), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
for idx, (cat, col, head, body, src, chip) in enumerate(cards):
    r, c = divmod(idx, 5)
    x0 = 8 + c * 204
    y0 = 470 + r * 90
    d.rectangle([x0, y0, x0 + 198, y0 + 88], outline=(200, 200, 200))
    d.rectangle([x0, y0, x0 + 198, y0 + 14], fill=col)
    text(x0 + 5, y0 + 2, cat, SANS_B(9), WHITE)
    text(x0 + 198 - 5, y0 + 2, str(idx + 1), SANS_B(9), WHITE, anchor="ra")
    hlines = wrap(head, SANS_B(11), 190)
    for j, ln in enumerate(hlines[:2]):
        text(x0 + 5, y0 + 18 + j * 13, ln, SANS_B(11), BLACK)
    text(x0 + 5, y0 + 48, body, SANS(9), BLACK)
    text(x0 + 5, y0 + 72, src, SANS(8), GRAY)
    chipcol = BLUE if chip == "REPORTED" else RED
    d.rectangle([x0 + 198 - 72, y0 + 68, x0 + 198 - 3, y0 + 84], fill=chipcol)
    center(x0 + 198 - 72, x0 + 198 - 3, y0 + 71, chip, SANS_B(9), WHITE)

# ---------- bottom strips ----------
d.rectangle([8, 652, 336, 670], fill=BLACK)
text(14, 655, "WHERE IT HAPPENED", SANS_B(11), WHITE)
d.rectangle([344, 652, 1016, 670], fill=BLACK)
text(350, 655, "ALSO ON MONDAY", SANS_B(11), WHITE)

# ---------- map ----------
d.rectangle([8, 670, 336, 918], fill=(248, 248, 240))
# Americas blob
d.polygon([(30, 700), (70, 680), (120, 690), (140, 720), (120, 770), (95, 830), (70, 870),
           (45, 850), (25, 800), (20, 740)], fill=MAPGREEN)
# Europe / Africa blob
d.polygon([(185, 695), (230, 685), (255, 710), (250, 760), (235, 820), (210, 860),
           (190, 830), (180, 770), (175, 720)], fill=MAPGREEN)
# Asia blob
d.polygon([(265, 690), (320, 685), (332, 720), (325, 770), (300, 800), (270, 780), (260, 730)],
          fill=MAPGREEN)
# Australia blob
d.polygon([(285, 840), (320, 835), (330, 860), (300, 875), (280, 860)], fill=MAPGREEN)

pins = [
    (1, "Seoul", 305, 735), (2, "Bridgetown", 60, 850), (3, "Beijing", 290, 715),
    (4, "Washington", 105, 790), (5, "New York", 112, 762), (6, "Kyiv", 232, 740),
    (7, "Chicago", 78, 762), (8, "SF", 45, 792), (9, "Denver", 72, 806),
    (10, "Austin", 88, 830), (11, "Warsaw", 214, 726), (12, "London", 192, 708),
    (13, "Moscow", 246, 706),
]
for n, _name, px, py in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    center(px - 8, px + 8, py - 6, str(n), SANS_B(9), WHITE)

legend = ["Pins 1\u201313:  1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
          "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF",
          "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow"]
for j, ln in enumerate(legend):
    text(12, 884 + j * 11, ln, SANS(8), BLACK)

# ---------- ALSO list ----------
also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: the day after Antalya pact rejected", False),
    ("18. Israel unity talks resume", False),
    ("19. Gaza: two killed in Israeli strike", False),
    ("20. West Bank settler attacks", False),
    ("21. Iran war: no deal in sight", False),
    ("22. Lebanon seizes 264 kg explosives", False),
    ("23. Bahrain: strike hits plant, 2 hurt", False),
    ("24. Benghazi: UN demands probe [CLAIM]", True),
    ("25. Sudan: defences down drones [CLAIM]", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if she returns", False),
    ("28. Seoul minister quits in exam row", False),
    ("29. SK Telecom \u22127.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
for i, (item, claim) in enumerate(also):
    col = 0 if i < 9 else 1
    row = i % 9
    x0 = 350 + col * 336
    y = 676 + row * 27
    text(x0, y, item, SANS_B(10) if claim else SANS(10), RED if claim else BLACK)

# ---------- DATE CHECK ----------
d.rectangle([8, 922, 1016, 970], outline=RED, width=2)
text(14, 926, "DATE CHECK", SANS_B(11), RED)
text(1010, 926, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", SANS_B(9), RED, anchor="ra")
text(14, 940, "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
     SANS(9), BLACK)
text(14, 954, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
     SANS(9), BLACK)

# ---------- footer ----------
text(10, 976, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     SANS(8), GRAY)
text(10, 990, "CHIPS: REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim, not independently confirmed  \u00b7  ONGOING = still developing.",
     SANS(8), GRAY)
center(0, W, 1006, "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
       SANS_B(11), GOLD)

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT))

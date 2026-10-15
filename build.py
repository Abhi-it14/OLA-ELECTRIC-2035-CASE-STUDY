import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.fonts import addMapping

GF = '/usr/share/fonts/truetype/google-fonts/'
LF = '/usr/share/fonts/truetype/liberation/'
for n, f in [('HeadR', GF + 'Poppins-Regular.ttf'), ('HeadM', GF + 'Poppins-Medium.ttf'),
             ('HeadB', GF + 'Poppins-Bold.ttf'),
             ('Body', LF + 'LiberationSans-Regular.ttf'), ('Body-B', LF + 'LiberationSans-Bold.ttf'),
             ('Body-I', LF + 'LiberationSans-Italic.ttf'), ('Body-BI', LF + 'LiberationSans-BoldItalic.ttf')]:
    pdfmetrics.registerFont(TTFont(n, f))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Body-B', italic='Body-I', boldItalic='Body-BI')
pdfmetrics.registerFontFamily('HeadM', normal='HeadM', bold='HeadB', italic='HeadM', boldItalic='HeadB')
pdfmetrics.registerFontFamily('HeadB', normal='HeadB', bold='HeadB', italic='HeadB', boldItalic='HeadB')

NAVY = HexColor('#0B1F3A'); NAVY_T = HexColor('#1B3355'); LIME = HexColor('#C6F432'); LIME_T = HexColor('#EAFAB8')
AMBER = HexColor('#F2A20C'); AMBER_T = HexColor('#FCE7BD'); GREY_L = HexColor('#F1F4F8'); GREY_M = HexColor('#C5CCD6')
GREY_T = HexColor('#4A5568'); LINE = HexColor('#D5DBE3'); MUTED_ON_NAVY = HexColor('#AEBBD0')

W, H = landscape(A4)
M = 36
CW = W - 2 * M


def Y(t): return H - t


def rect(c, x, t, w, h, fill=None, stroke=None, r=0, sw=0.6):
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(sw)
    if r: c.roundRect(x, Y(t + h), w, h, r, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
    else: c.rect(x, Y(t + h), w, h, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
    c.restoreState()


def text(c, s, x, t, font, size, color, al='l'):
    c.setFont(font, size); c.setFillColor(color)
    {'l': c.drawString, 'c': c.drawCentredString, 'r': c.drawRightString}[al](x, Y(t), s)


def para(c, s, x, t, w, font='Body', size=9, color=GREY_T, lead=None, align=0, draw=True):
    st = ParagraphStyle('p', fontName=font, fontSize=size, leading=lead or size * 1.32, textColor=color, alignment=align)
    p = Paragraph(s, st)
    pw, ph = p.wrap(w, 1000)
    if draw: p.drawOn(c, x, Y(t) - ph)
    return ph


def hline(c, x1, x2, t, color=LINE, lw=0.6):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(lw); c.line(x1, Y(t), x2, Y(t)); c.restoreState()


def arrow(c, x1, y1, x2, y2, col, lw=1, hs=3.5):
    c.saveState(); c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(lw)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2 - y1, x2 - x1)
    p = c.beginPath(); p.moveTo(x2, y2)
    p.lineTo(x2 - hs * math.cos(a - 0.45), y2 - hs * math.sin(a - 0.45))
    p.lineTo(x2 - hs * math.cos(a + 0.45), y2 - hs * math.sin(a + 0.45)); p.close()
    c.drawPath(p, stroke=0, fill=1); c.restoreState()


def pill(c, s, x, t, fill, color, size=7, font='HeadB', padx=6, h=13):
    w = pdfmetrics.stringWidth(s, font, size) + 2 * padx
    rect(c, x, t, w, h, fill=fill, r=h / 2)
    text(c, s, x + padx, t + h / 2 + size * 0.35, font, size, color)
    return w


def icon(c, name, cx, t, s, col, lw=1.2):
    cy = Y(t)
    c.saveState(); c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(lw); c.setLineCap(1); c.setLineJoin(1)
    if name == 'home':
        p = c.beginPath(); p.moveTo(cx - s, cy); p.lineTo(cx, cy + s); p.lineTo(cx + s, cy); c.drawPath(p, stroke=1, fill=0)
        c.rect(cx - .7 * s, cy - s, 1.4 * s, s, stroke=1, fill=0); c.rect(cx - .2 * s, cy - s, .4 * s, .6 * s, stroke=1, fill=0)
    elif name == 'building':
        c.rect(cx - .6 * s, cy - s, 1.2 * s, 2 * s, stroke=1, fill=0)
        for dx in (-.25, .25):
            for dy in (.5, 0, -.5):
                c.circle(cx + dx * s, cy + dy * s, .06 * s + .3, stroke=0, fill=1)
    elif name == 'bus':
        c.roundRect(cx - s, cy - .6 * s, 2 * s, 1.5 * s, 2, stroke=1, fill=0)
        c.line(cx - s, cy + .2 * s, cx + s, cy + .2 * s)
        for dx in (-.5, .5): c.circle(cx + dx * s, cy - .6 * s, .22 * s, stroke=1, fill=0)
    elif name == 'train':
        c.roundRect(cx - .65 * s, cy - .8 * s, 1.3 * s, 1.8 * s, 2, stroke=1, fill=0)
        c.rect(cx - .4 * s, cy + .25 * s, .8 * s, .45 * s, stroke=1, fill=0)
        for dx in (-.3, .3): c.circle(cx + dx * s, cy - .45 * s, .12 * s + .3, stroke=0, fill=1)
        c.line(cx - .6 * s, cy - s, cx - .8 * s, cy - 1.15 * s); c.line(cx + .6 * s, cy - s, cx + .8 * s, cy - 1.15 * s)
    elif name == 'car':
        c.roundRect(cx - s, cy - .45 * s, 2 * s, .75 * s, 2, stroke=1, fill=0)
        p = c.beginPath(); p.moveTo(cx - .6 * s, cy + .3 * s); p.lineTo(cx - .35 * s, cy + .75 * s); p.lineTo(cx + .35 * s, cy + .75 * s); p.lineTo(cx + .6 * s, cy + .3 * s)
        c.drawPath(p, stroke=1, fill=0)
        for dx in (-.55, .55): c.circle(cx + dx * s, cy - .5 * s, .2 * s, stroke=1, fill=0)
    elif name == 'pin':
        c.circle(cx, cy + .25 * s, .55 * s, stroke=1, fill=0)
        c.line(cx - .5 * s, cy - .05 * s, cx, cy - s); c.line(cx + .5 * s, cy - .05 * s, cx, cy - s)
        c.circle(cx, cy + .25 * s, .18 * s, stroke=0, fill=1)
    elif name == 'repeat':
        c.arc(cx - .8 * s, cy - .8 * s, cx + .8 * s, cy + .8 * s, 40, 270)
        a = math.radians(310); px, py = cx + .8 * s * math.cos(a), cy + .8 * s * math.sin(a)
        arrow(c, px - .3 * s, py - .15 * s, px + .05 * s, py + .1 * s, col, lw, hs=4)
    elif name == 'clock':
        c.circle(cx, cy, s, stroke=1, fill=0); c.line(cx, cy, cx, cy + .6 * s); c.line(cx, cy, cx + .45 * s, cy - .2 * s)
    elif name == 'ticket':
        c.roundRect(cx - s, cy - .6 * s, 2 * s, 1.2 * s, 2, stroke=1, fill=0)
        c.setDash(1.5, 1.5); c.line(cx + .3 * s, cy - .6 * s, cx + .3 * s, cy + .6 * s); c.setDash()
    elif name == 'swap':
        arrow(c, cx - s, cy + .4 * s, cx + s, cy + .4 * s, col, lw, hs=4); arrow(c, cx + s, cy - .4 * s, cx - s, cy - .4 * s, col, lw, hs=4)
    elif name == 'shield':
        p = c.beginPath(); p.moveTo(cx, cy + s); p.lineTo(cx + .8 * s, cy + .55 * s); p.lineTo(cx + .8 * s, cy - .1 * s)
        p.curveTo(cx + .8 * s, cy - .6 * s, cx + .3 * s, cy - .85 * s, cx, cy - s)
        p.curveTo(cx - .3 * s, cy - .85 * s, cx - .8 * s, cy - .6 * s, cx - .8 * s, cy - .1 * s)
        p.lineTo(cx - .8 * s, cy + .55 * s); p.close(); c.drawPath(p, stroke=1, fill=0)
        p = c.beginPath(); p.moveTo(cx - .3 * s, cy); p.lineTo(cx - .05 * s, cy - .3 * s); p.lineTo(cx + .4 * s, cy + .3 * s); c.drawPath(p, stroke=1, fill=0)
    elif name == 'gear':
        c.circle(cx, cy, .45 * s, stroke=1, fill=0); c.circle(cx, cy, .72 * s, stroke=1, fill=0)
        for k in range(8):
            a = k * math.pi / 4; c.line(cx + .72 * s * math.cos(a), cy + .72 * s * math.sin(a), cx + s * math.cos(a), cy + s * math.sin(a))
    elif name == 'code':
        for sg in (-1, 1):
            p = c.beginPath(); p.moveTo(cx + sg * .35 * s, cy + .6 * s); p.lineTo(cx + sg * .95 * s, cy); p.lineTo(cx + sg * .35 * s, cy - .6 * s); c.drawPath(p, stroke=1, fill=0)
        c.line(cx + .2 * s, cy + .7 * s, cx - .2 * s, cy - .7 * s)
    elif name == 'store':
        p = c.beginPath(); p.moveTo(cx - s, cy + .1 * s); p.lineTo(cx - .75 * s, cy + .8 * s); p.lineTo(cx + .75 * s, cy + .8 * s); p.lineTo(cx + s, cy + .1 * s); p.close(); c.drawPath(p, stroke=1, fill=0)
        c.rect(cx - .8 * s, cy - .8 * s, 1.6 * s, .9 * s, stroke=1, fill=0); c.rect(cx - .2 * s, cy - .8 * s, .4 * s, .55 * s, stroke=1, fill=0)
    elif name == 'star':
        p = c.beginPath()
        for k in range(10):
            r = s if k % 2 == 0 else .45 * s; a = math.pi / 2 + k * math.pi / 5
            (p.moveTo if k == 0 else p.lineTo)(cx + r * math.cos(a), cy + r * math.sin(a))
        p.close(); c.drawPath(p, stroke=1, fill=0)
    elif name == 'user':
        c.circle(cx, cy + .4 * s, .4 * s, stroke=1, fill=0); c.arc(cx - .8 * s, cy - 1.1 * s, cx + .8 * s, cy + .3 * s, 0, 180)
    elif name == 'target':
        c.circle(cx, cy, s, stroke=1, fill=0); c.circle(cx, cy, .55 * s, stroke=1, fill=0); c.circle(cx, cy, .15 * s + .3, stroke=0, fill=1)
    elif name == 'coin':
        c.circle(cx, cy, s, stroke=1, fill=0); c.line(cx - .35 * s, cy + .35 * s, cx + .35 * s, cy + .35 * s)
        c.line(cx - .35 * s, cy, cx + .35 * s, cy); c.line(cx - .1 * s, cy + .35 * s, cx - .1 * s, cy - .5 * s)
    elif name == 'check':
        p = c.beginPath(); p.moveTo(cx - .6 * s, cy); p.lineTo(cx - .1 * s, cy - .5 * s); p.lineTo(cx + .65 * s, cy + .5 * s); c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def icon_badge(c, name, cx, t, r, bg, fg, s=None):
    c.saveState(); c.setFillColor(bg); c.circle(cx, Y(t), r, stroke=0, fill=1); c.restoreState()
    icon(c, name, cx, t, s or r * 0.52, fg)


def frame(c, n, section, title, source, cover=False):
    rect(c, 0, 232 if cover else 34, 7, H - (232 if cover else 34), fill=LIME)
    if not cover:
        rect(c, 0, 0, W, 34, fill=NAVY)
        text(c, '0%d  %s' % (n, section.upper()), M, 21.5, 'HeadM', 9, white)
        text(c, 'OLA COMMUTE  |  2035 CASE STUDY', W - M - 60, 21, 'HeadM', 6.8, MUTED_ON_NAVY, 'r')
        text(c, '%d / 5' % n, W - M, 22, 'HeadB', 10, LIME, 'r')
        size = 20
        while pdfmetrics.stringWidth(title, 'HeadB', size) > CW and size > 15: size -= .5
        text(c, title, M, 66, 'HeadB', size, NAVY)
        rect(c, M, 74, 44, 3, fill=LIME); hline(c, M + 44, W - M, 75.5)
    hline(c, M, W - M, 558)
    para(c, source, M, 562, CW, size=7.2, color=GREY_T, lead=9)


def card(c, x, t, w, h, fill=GREY_L, stroke=LINE, r=8):
    rect(c, x, t, w, h, fill=fill, stroke=stroke, r=r)


def tag(c, s, x, t, color=GREY_T):
    text(c, s, x, t, 'HeadB', 6.8, color)


# ----------------------------------------------------------------- PAGE 1
def page1(c):
    frame(c, 1, '', '', 'Sources: [1] World Bank, Financing India\u2019s Urban Infrastructure Needs (600M urban residents by 2036). [2] PIB/MoHUA, 2025 Metro Rail review (1,095 km, 26 cities). '
          '[3] TomTom Traffic Index 2025. [4] NITI Aayog, Scenarios Towards Viksit Bharat and Net Zero: Transport. [6] MoHUA, PM-eBus Sewa.', cover=True)
    rect(c, 0, 0, W, 232, fill=NAVY)
    text(c, 'OLA ELECTRIC  |  PRODUCT STRATEGY ASSIGNMENT  |  CASE STUDY: 2035', M, 36, 'HeadM', 7.5, LIME)
    text(c, '1 / 5', W - M, 36, 'HeadB', 9, LIME, 'r')
    text(c, 'India doesn\u2019t need another vehicle.', M, 78, 'HeadB', 28, white)
    text(c, 'It needs a better commute.', M, 113, 'HeadB', 28, LIME)
    para(c, '<font color="#C6F432"><b>The answer:</b></font> We build <b>Ola Commute</b> for metro-city weekday commuters, a recurring, multimodal '
              'commute service that keeps mass transit as the backbone and <b>guarantees the missing first and last mile</b> with pooled electric feeders and a reliable fallback ride.',
         M, 138, 440, size=11, color=white, lead=15.5)
    # route illustration
    px = 530
    xs = [px + 15, px + 90, px + 170, px + 250]
    ty = 168
    c.saveState(); c.setStrokeColor(LIME); c.setLineWidth(1.2); c.setDash(3, 3); c.line(xs[0], Y(ty), xs[3], Y(ty)); c.restoreState()
    labs = ['Home', 'Feeder EV', 'Metro / bus', 'Office']; icons = ['home', 'bus', 'train', 'building']
    for x, l, ic in zip(xs, labs, icons):
        icon_badge(c, ic, x, ty, 17, NAVY_T, LIME)
        c.saveState(); c.setStrokeColor(LIME); c.setLineWidth(1); c.circle(x, Y(ty), 17, stroke=1, fill=0); c.restoreState()
        text(c, l, x, ty + 31, 'Body', 8, white, 'c')
    c.saveState(); c.setStrokeColor(AMBER); c.setLineWidth(1.2); c.setDash(2, 2)
    p = c.beginPath(); p.moveTo(xs[1] + 14, Y(ty - 14)); p.curveTo(xs[1] + 40, Y(ty - 48), xs[2] - 40, Y(ty - 48), xs[2] - 14, Y(ty - 14)); c.drawPath(p, stroke=1, fill=0); c.restoreState()
    text(c, 'Auto fallback if a leg misses its SLA', (xs[1] + xs[2]) / 2, ty - 50, 'Body', 8, AMBER, 'c')
    # KPI tiles
    kp = [('100M', 'daily users targeted by 2035, about 1 in 6 of 600M urban Indians', True),
          ('600M', 'urban residents expected in India by 2036', False),
          ('1,095 km', 'operational metro network in India, 2025', False),
          ('74.4%', 'congestion level in Bengaluru, 2025', False)]
    tw = (CW - 3 * 14) / 4
    for i, (v, l, hl) in enumerate(kp):
        x = M + i * (tw + 14)
        rect(c, x, 246, tw, 72, fill=LIME if hl else GREY_L, stroke=None if hl else LINE, r=8)
        text(c, v, x + 12, 278, 'HeadB', 25, NAVY)
        para(c, l, x + 12, 284, tw - 24, size=8.5, color=NAVY if hl else GREY_T, lead=10.5)
    # seven answers
    text(c, 'The case in seven answers', M, 344, 'HeadB', 11.5, NAVY)
    rect(c, M, 349, 30, 2.5, fill=LIME)
    rows = [('Target user & problem', 'Metro-city weekday commuters living 3\u20138 km from transit; their pain is unreliable, high-friction connections between modes.', 'p.2'),
            ('Why it matters in 2035', '600M urban residents by 2036 and 1,095 km of metro are in place; NITI Aayog flags weak integration and recommends electric feeders.', 'p.2'),
            ('Product & experience', 'One booking, one promise: Ola plans the full chain (pooled EV feeder, metro/bus, last mile) with an automatic auto fallback.', 'p.3'),
            ('Alternatives & trade-offs', 'Five concepts and five commute modes scored; the multimodal commute layer ranks first (4.95 / 5).', 'p.4'),
            ('Why Ola', 'MoveOS + OTA software, integrated EV manufacturing, retail/service/charging footprint and an established mobility brand.', 'p.4'),
            ('Path to 100M (what must be true)', 'Density first: one corridor, then a city, then 60\u201380 cities, with 100M daily users by 2035.', 'p.5'),
            ('Success metrics', 'North Star: weekly completed commutes per active rider, with explicit kill criteria after a 12-month pilot.', 'p.5')]
    rh = 27; t0 = 358
    for i, (q, a, pg) in enumerate(rows):
        t = t0 + i * rh
        if i: hline(c, M, 560 - 0 if False else 548 + 0 if False else M + 524, t)
        c.saveState(); c.setFillColor(NAVY); c.circle(M + 8, Y(t + rh / 2), 7.5, stroke=0, fill=1); c.restoreState()
        text(c, str(i + 1), M + 8, t + rh / 2 + 3, 'HeadB', 7.5, LIME, 'c')
        para(c, q, M + 22, t + 4, 112, font='HeadM', size=8, color=NAVY, lead=10)
        para(c, a, M + 140, t + 3.5, 345, size=8.5, color=GREY_T, lead=10.5)
        text(c, pg, M + 524, t + rh / 2 + 3, 'HeadM', 7.5, GREY_T, 'r')
    # assumptions
    ax = M + 548; aw = W - M - ax
    card(c, ax, 340, aw, 212, fill=GREY_L)
    rect(c, ax, 340, 4, 212, fill=AMBER)
    pill(c, 'ASSUMPTIONS FOR 2035', ax + 16, 350, AMBER, NAVY, size=6.8)
    para(c, 'This thesis holds only if:', ax + 16, 372, aw - 28, font='Body-B', size=9, color=NAVY)
    items = ['Urban populations continue to rise', 'Metro and bus coverage expands', 'EV operating costs decline',
             'Public transit remains the backbone', 'Cities increasingly prioritize integrated, demand-responsive feeders']
    t = 392
    for it in items:
        c.saveState(); c.setFillColor(NAVY); c.circle(ax + 20, Y(t + 5.5), 2.2, stroke=0, fill=1); c.restoreState()
        h = para(c, it, ax + 30, t, aw - 42, size=9, color=NAVY, lead=11.5)
        t += h + 7


# ----------------------------------------------------------------- PAGE 2
def hbars(c, x, t, labels, vals, maxv, wbar, hl, fmt, rowh=24, lab_w=64, barh=14):
    for i, (l, v) in enumerate(zip(labels, vals)):
        tt = t + i * rowh
        text(c, l, x, tt + barh / 2 + 3, 'Body-B' if i == hl else 'Body', 8.5, NAVY)
        bw = max(wbar * v / maxv, 2)
        rect(c, x + lab_w, tt, bw, barh, fill=LIME if i == hl else GREY_M, r=2)
        text(c, fmt(v), x + lab_w + bw + 5, tt + barh / 2 + 3, 'HeadB' if i == hl else 'HeadM', 8.5, NAVY)


def page2(c):
    frame(c, 2, 'Who & why', 'The pain is the connection between modes, not a lack of transport',
          'Sources: [3] TomTom Traffic Index 2025 (congestion level by city). [1] World Bank, Financing India\u2019s Urban Infrastructure Needs. [2] PIB/MoHUA, 2025 Metro Rail review. '
          '[4] NITI Aayog, Transport scenarios. [5] World Bank, Designing Public Transport in India That Works for All. Total-population figure (1.5B): [NEEDS SOURCE: year and publisher].')
    top = 92
    # Persona card
    ax, aw = M, 228
    card(c, ax, top, aw, 458)
    pill(c, 'BEACHHEAD USER', ax + 14, top + 14, LIME, NAVY)
    icon_badge(c, 'user', ax + 30, top + 56, 18, NAVY, LIME)
    para(c, 'Metro-city weekday commuter', ax + 56, top + 41, aw - 66, font='HeadB', size=11.5, color=NAVY, lead=14)
    t = top + 86
    for b in ['Predictable weekday travel pattern', 'Lives 3\u20138 km from a mass-transit station',
              'Already willing to use shared transport', 'Stitches together 2\u20133 modes every day',
              'Loses time and reliability at every switch']:
        c.saveState(); c.setFillColor(NAVY); c.circle(ax + 18, Y(t + 5.5), 2, stroke=0, fill=1); c.restoreState()
        h = para(c, b, ax + 27, t, aw - 40, size=9, color=NAVY, lead=11.5); t += h + 6
    text(c, 'A typical daily chain', ax + 14, t + 12, 'Body-B', 8, GREY_T)
    t += 22
    chips = ['Walk', 'Auto', 'Metro', 'Walk']; cw = 40; gap = (aw - 28 - 4 * cw) / 3
    for i, ch in enumerate(chips):
        x = ax + 14 + i * (cw + gap)
        rect(c, x, t, cw, 18, fill=white, stroke=GREY_M, r=9); text(c, ch, x + cw / 2, t + 12, 'Body-B', 8, NAVY, 'c')
        if i < 3: arrow(c, x + cw + 2, Y(t + 9), x + cw + gap - 2, Y(t + 9), GREY_T, .9, hs=3)
    t += 34
    text(c, 'Segment size: [NEEDS SOURCE]', ax + 14, t + 4, 'Body-I', 7.5, GREY_T)
    # key insight
    kt = t + 18
    rect(c, ax + 10, kt, aw - 20, 550 - kt - 10, fill=NAVY, r=8)
    tag(c, 'KEY INSIGHT', ax + 24, kt + 20, LIME)
    para(c, 'The core pain point is <b>not an absolute lack of transport</b>. It is the <font color="#C6F432"><b>friction, anxiety and unreliability</b></font> of the connections between modes.',
         ax + 24, kt + 28, aw - 48, size=11.5, color=white, lead=15.5)
    # chart 1
    bx = M + aw + 16; bw = 256
    card(c, bx, top, bw, 214, fill=white)
    para(c, 'Bengaluru leads congestion among major Indian cities, at 74.4%', bx + 14, top + 12, bw - 28, font='HeadB', size=10, color=NAVY, lead=13)
    text(c, 'Average congestion level, %, 2025', bx + 14, top + 50, 'Body', 8, GREY_T)
    hbars(c, bx + 14, top + 66, ['Bengaluru', 'Pune', 'Mumbai', 'Delhi', 'Kolkata'], [74.4, 71.1, 63.2, 60.2, 58.9], 100, 140, 0, lambda v: '%.1f%%' % v, rowh=25, lab_w=62)
    text(c, 'Source: TomTom Traffic Index 2025 [3]', bx + 14, top + 204, 'Body', 7.2, GREY_T)
    # women
    wt = top + 228
    card(c, bx, wt, bw, 230, fill=GREY_L)
    rect(c, bx, wt, 4, 230, fill=AMBER)
    pill(c, 'SAFETY IMPERATIVE', bx + 16, wt + 14, AMBER, NAVY)
    cx, cyt, R = bx + 52, wt + 80, 30
    c.saveState()
    c.setFillColor(AMBER); c.wedge(cx - R, Y(cyt) - R, cx + R, Y(cyt) + R, 90, -302.4, stroke=0, fill=1)
    c.setFillColor(GREY_M); c.wedge(cx - R, Y(cyt) - R, cx + R, Y(cyt) + R, 90 - 302.4, -57.6, stroke=0, fill=1)
    c.setFillColor(GREY_L); c.circle(cx, Y(cyt), R * .62, stroke=0, fill=1); c.restoreState()
    text(c, '84%', cx, cyt + 4.5, 'HeadB', 11, NAVY, 'c')
    para(c, 'of work trips by women rely on public, intermediate or non-motorised transport',
         bx + 98, wt + 56, bw - 112, font='Body-B', size=9, color=NAVY, lead=11.5)
    para(c, 'Chart: share of women\u2019s work trips, %. Source: World Bank [5]', bx + 14, wt + 122, bw - 28, size=7.2, color=GREY_T)
    hline(c, bx + 14, bx + bw - 14, wt + 138)
    para(c, 'Safety concerns and long waits restrict access to jobs and education. <b>Safety must be engineered as a core product requirement</b>, not run as a marketing campaign.',
         bx + 14, wt + 148, bw - 28, size=9, color=NAVY, lead=12)
    # chart 2
    cx0 = bx + bw + 16; cwid = W - M - cx0
    card(c, cx0, top, cwid, 214, fill=white)
    para(c, '100M daily users is about 1 in 6 of India\u2019s 600M urban residents', cx0 + 14, top + 12, cwid - 28, font='HeadB', size=10, color=NAVY, lead=13)
    text(c, 'Population, millions', cx0 + 14, top + 50, 'Body', 8, GREY_T)
    for i, (l, v, hl) in enumerate([('Total population', 1500, False), ('Urban pop. (2036)', 600, False), ('Ola Commute target', 100, True)]):
        tt = top + 70 + i * 32
        text(c, l, cx0 + 14, tt - 3, 'Body-B' if hl else 'Body', 8.5, NAVY)
        bwid = max(150 * v / 1500, 3)
        rect(c, cx0 + 14, tt + 1, bwid, 13, fill=LIME if hl else GREY_M, r=2)
        text(c, ('%s' % ('1,500M' if v == 1500 else '%dM' % v)) + ('*' if v == 1500 else ''), cx0 + 14 + bwid + 5, tt + 11, 'HeadB' if hl else 'HeadM', 8.5, NAVY)
    text(c, 'Source: World Bank [1]. *Year/source needed [NEEDS SOURCE]', cx0 + 14, top + 204, 'Body', 7.2, GREY_T)
    # why now
    nt = top + 228
    rect(c, cx0, nt, cwid, 230, fill=NAVY, r=8)
    tag(c, 'WHY NOW', cx0 + 16, nt + 22, LIME)
    t = nt + 32
    for big, small in [('600M', 'urban residents projected by 2036'), ('1,095 km', 'metro network operational in 2025')]:
        text(c, big, cx0 + 16, t + 17, 'HeadB', 16, LIME)
        para(c, small, cx0 + 112, t + 5, cwid - 126, size=8.5, color=white, lead=10.5)
        t += 32
    hline(c, cx0 + 16, cx0 + cwid - 16, t + 2, color=NAVY_T)
    h = para(c, 'NITI Aayog: poor service quality and inadequate integration remain major roadblocks; it recommends <b>electric feeders and shared mobility around mass transit</b>.',
             cx0 + 16, t + 10, cwid - 32, size=8.5, color=white, lead=11)
    t += h + 22
    para(c, '<font color="#C6F432"><b>100M is a realistic denominator</b></font> only because Ola Commute is a <b>layer over existing mobility</b>, not an owned fleet carrying 100M people.',
         cx0 + 16, t, cwid - 32, size=8.5, color=white, lead=11)


# ----------------------------------------------------------------- PAGE 3
def page3(c):
    frame(c, 3, 'The product', 'Ola Commute: one booking, one promise, multiple modes',
          'Sources: [4] NITI Aayog, Transport scenarios (feeders and integrated shared mobility). App screens are illustrative concept mock-ups, not live product. '
          '"Where API integration permits": transit-operator integration is a dependency (see p.5).')
    top = 92
    nodes = [('Set once', 'Home to office', 'home', NAVY, white), ('Ola plans', 'Optimum chain', 'code', NAVY, white),
             ('Feeder EV', 'First-mile pickup', 'bus', LIME, NAVY), ('Metro / bus', 'High-capacity backbone', 'train', GREY_M, NAVY),
             ('Last mile', '+ Auto fallback', 'car', LIME, NAVY)]
    nw = (CW - 4 * 18) / 5
    for i, (a, b, ic, bg, fg) in enumerate(nodes):
        x = M + i * (nw + 18)
        rect(c, x, top, nw, 52, fill=bg, r=8)
        icon(c, ic, x + 22, top + 26, 9, fg, 1.3)
        text(c, a, x + 42, top + 23, 'HeadB', 9.5, fg)
        text(c, b, x + 42, top + 37, 'Body', 8.2, fg)
        if i < 4: arrow(c, x + nw + 3, Y(top + 26), x + nw + 15, Y(top + 26), GREY_T, 1.2, hs=4)
    # legend
    lx = M
    for col, lab in [(NAVY, 'Ola intelligence'), (LIME, 'Ola-controlled legs'), (GREY_M, 'City / operator infrastructure')]:
        rect(c, lx, top + 63, 8, 8, fill=col, r=2); text(c, lab, lx + 12, top + 70.5, 'Body', 7.5, GREY_T)
        lx += 18 + pdfmetrics.stringWidth(lab, 'Body', 7.5) + 10
    # UI cards
    t2 = top + 88
    text(c, 'Core user experience (illustrative screens)', M, t2, 'HeadB', 10, NAVY)
    ct = t2 + 10; ch = 262; cwd = 150; g = 15
    # card1
    x = M
    card(c, x, ct, cwd, ch, fill=GREY_L); tag(c, 'STEP 1 · SET & FORGET', x + 12, ct + 20, GREY_T); hline(c, x + 12, x + cwd - 12, ct + 27)
    text(c, 'Ola Commute', x + 12, ct + 46, 'HeadB', 11, NAVY)
    para(c, 'Tomorrow \u00b7 Home \u2192 Tech Park', x + 12, ct + 54, cwd - 24, size=8.5)
    para(c, 'Leave 8:20 AM', x + 12, ct + 76, cwd - 24, font='Body-B', size=10, color=NAVY)
    t = ct + 100
    for b in ['Feeder pickup: 8:20', 'Metro departs: 8:34']:
        c.saveState(); c.setFillColor(NAVY); c.circle(x + 16, Y(t + 4.5), 2, stroke=0, fill=1); c.restoreState()
        para(c, b, x + 25, t, cwd - 40, size=8.5, color=NAVY); t += 16
    rect(c, x + 12, ct + ch - 44, cwd - 24, 28, fill=NAVY, r=6); text(c, 'Confirm Commute', x + cwd / 2, ct + ch - 26, 'HeadM', 8.5, white, 'c')
    # card2
    x = M + cwd + g
    card(c, x, ct, cwd, ch, fill=GREY_L); tag(c, 'STEP 2 · ON THE WAY', x + 12, ct + 20, GREY_T); hline(c, x + 12, x + cwd - 12, ct + 27)
    text(c, 'Commute Promise', x + 12, ct + 46, 'HeadB', 11, NAVY)
    pill(c, 'ON TIME', x + 12, ct + 54, LIME, NAVY, size=6.8)
    para(c, 'Arriving by 9:02 AM', x + 12, ct + 78, cwd - 24, font='Body-B', size=10, color=NAVY)
    t = ct + 104
    for a, b in [('Feeder (9/12 seats)', '6 min away'), ('Metro (Blue Line)', 'On time')]:
        para(c, a, x + 12, t, 80, size=8.5, color=GREY_T); text(c, b, x + cwd - 12, t + 9, 'Body-B', 8.5, NAVY, 'r')
        hline(c, x + 12, x + cwd - 12, t + 25); t += 32
    rect(c, x + 12, ct + ch - 44, cwd - 24, 28, fill=white, stroke=GREY_M, r=6); text(c, 'View Live Track', x + cwd / 2, ct + ch - 26, 'HeadM', 8.5, NAVY, 'c')
    # card3
    x = M + 2 * (cwd + g)
    card(c, x, ct, cwd, ch, fill=white, stroke=AMBER); rect(c, x, ct, cwd, 3, fill=AMBER)
    tag(c, 'STEP 3 · EXCEPTION', x + 12, ct + 20, GREY_T); hline(c, x + 12, x + cwd - 12, ct + 27)
    text(c, 'Fallback Ready', x + 12, ct + 46, 'HeadB', 11, NAVY)
    pill(c, 'AUTO FALLBACK', x + 12, ct + 54, AMBER, NAVY, size=6.8)
    para(c, 'Feeder delayed by 7 mins due to traffic.', x + 12, ct + 78, cwd - 24, size=8.5)
    para(c, 'Switching you to an Auto.', x + 12, ct + 104, cwd - 24, font='Body-B', size=9.5, color=NAVY)
    rect(c, x + 12, ct + 124, cwd - 24, 22, fill=LIME_T, r=5); text(c, 'No extra charge.', x + 20, ct + 139, 'Body-B', 9, NAVY)
    para(c, 'Revised arrival: <b>9:05 AM</b>', x + 12, ct + 160, cwd - 24, size=9, color=NAVY)
    # features
    fx = M + 3 * cwd + 2 * g + 20; fw = (W - M - fx - 14) / 2
    text(c, 'Six features that deliver the promise', fx, t2, 'HeadB', 10, NAVY)
    feats = [('repeat', 'Recurring Commute', 'Save home and work once; Ola proposes the best departure time for every weekday.'),
             ('clock', 'Commute Promise', 'Optimizes end-to-end arrival reliability, favouring predictability over the cheapest single ride.'),
             ('bus', 'Shared EV Feeder', 'Pools 6\u201312 riders on high-density routes linking homes to transit stations.'),
             ('ticket', 'One Fare', 'One pass covers feeder + transit (where API integration permits), removing search and payment friction.'),
             ('swap', 'Smart Fallback', 'If an Ola-controlled leg misses its SLA, the rider is upgraded to a direct auto/cab at a capped cost.'),
             ('shield', 'Safety Layer', 'Verified drivers, live trip sharing, pickup lighting guidelines and a frictionless SOS path.')]
    for i, (ic, nm, ds) in enumerate(feats):
        col, row = i % 2, i // 2
        x = fx + col * (fw + 14); tt = ct + row * 88
        icon_badge(c, ic, x + 11, tt + 11, 11, NAVY, LIME, s=6)
        text(c, '0%d' % (i + 1), x + 28, tt + 8, 'HeadB', 6.5, GREY_T)
        text(c, nm, x + 28, tt + 19, 'HeadB', 8.5, NAVY)
        para(c, ds, x, tt + 28, fw, size=8, color=GREY_T, lead=10)
    # boundary
    bt = ct + ch + 14
    bh = 550 - bt
    rect(c, M, bt, 560, bh, fill=NAVY, r=8)
    tag(c, 'STRATEGIC BOUNDARY', M + 16, bt + 17, LIME)
    para(c, 'We deliberately do <b>not</b> build a new metro system, a robotaxi fleet or a nationwide bus operation. <font color="#C6F432"><b>Ola owns the customer promise, the routing logic and the orchestration;</b></font> cities and fleet partners own the heavy infrastructure.',
         M + 16, bt + 24, 528, size=9, color=white, lead=12)
    ox = M + 576; ow = (W - M - ox - 12) / 2
    for i, (hd, bg, fgc, items) in enumerate([('Ola owns', LIME, NAVY, 'Promise \u00b7 Routing \u00b7 Orchestration'), ('Partners own', GREY_L, NAVY, 'Heavy infrastructure \u00b7 Fleet')]):
        x = ox + i * (ow + 12)
        rect(c, x, bt, ow, bh, fill=bg, stroke=None if i == 0 else LINE, r=8)
        text(c, hd, x + 10, bt + 18, 'HeadB', 8.5, fgc)
        para(c, items, x + 10, bt + 24, ow - 20, size=8, color=fgc, lead=10)


# ----------------------------------------------------------------- PAGE 4
def dots(c, x, t, n, col=NAVY):
    for k in range(5):
        c.saveState(); c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(.7)
        c.circle(x + k * 8, Y(t), 2.6, stroke=1, fill=1 if k < n else 0); c.restoreState()


def page4(c):
    frame(c, 4, 'Why this solution, why Ola', 'The moat is coordination and density, not the vehicle itself',
          'Sources: [7] Ola Electric, MoveOS 5 announcement. [8] Ola Electric business / DRHP materials. [9] Ola Electric investor relations (retail, service and charging footprint). '
          'Scores: author\u2019s assessment, weighted per header (scale 1\u20135); weighted totals recalculated from the weights shown.')
    top = 92
    lw = 520
    text(c, 'Five concepts scored: the multimodal commute layer ranks first', M, top + 8, 'HeadB', 10.5, NAVY)
    text(c, 'Score 1\u20135 per criterion; weight in brackets; weighted total out of 5', M, top + 21, 'Body', 8, GREY_T)
    crit = [('Problem', .20), ('Frequency', .15), ('Users', .15), ('Ola edge', .15), ('2035 fit', .10), ('Scale', .10), ('Econ.', .10), ('Diff.', .05)]
    data = {'Multimodal Commute': [5, 5, 5, 5, 5, 5, 5, 4], 'Dynamic mini-bus': [5, 5, 5, 4, 5, 4, 4, 4],
            'Women-first mobility': [5, 4, 3, 4, 5, 4, 3, 4], 'Employer shuttles': [4, 5, 2, 4, 5, 3, 3, 3],
            'Autonomous pods': [4, 3, 3, 4, 2, 2, 2, 5]}
    scores = {k: sum(v * w for v, (_, w) in zip(vs, crit)) for k, vs in data.items()}
    order = sorted(data, key=lambda k: -scores[k])
    t0 = top + 30; c0 = 108; cwc = 41; sc = lw - c0 - 8 * cwc
    rect(c, M, t0, lw, 32, fill=NAVY, r=4)
    text(c, 'Concept', M + 8, t0 + 19, 'HeadB', 7.5, white)
    for i, (n_, w_) in enumerate(crit):
        x = M + c0 + i * cwc + cwc / 2
        text(c, n_, x, t0 + 14, 'HeadB', 6.8, white, 'c'); text(c, '(%d%%)' % round(w_ * 100), x, t0 + 25, 'Body', 6.8, LIME, 'c')
    text(c, 'Total', M + lw - sc / 2, t0 + 19, 'HeadB', 7.5, LIME, 'c')
    rh = 21
    for r_, k in enumerate(order):
        tt = t0 + 34 + r_ * rh
        win = r_ == 0
        if win: rect(c, M - 2, tt - 1, lw + 4, rh, fill=None, stroke=NAVY, r=4, sw=1.2)
        text(c, k, M + 8, tt + 13, 'HeadB' if win else 'HeadM', 7.8, NAVY)
        for i, v in enumerate(data[k]):
            bg = LIME if v == 5 else LIME_T if v == 4 else GREY_L if v == 3 else AMBER_T
            rect(c, M + c0 + i * cwc + 2, tt + 1, cwc - 4, rh - 4, fill=bg, r=3)
            text(c, str(v), M + c0 + i * cwc + cwc / 2, tt + 13, 'HeadM', 8, NAVY, 'c')
        text(c, '%.2f' % scores[k], M + lw - sc / 2, tt + 14, 'HeadB', 10 if win else 9, NAVY, 'c')
    lt = t0 + 34 + 5 * rh + 6
    lx = M
    for col, lab in [(LIME, '5'), (LIME_T, '4'), (GREY_L, '3'), (AMBER_T, '1\u20132 (weak spot)')]:
        rect(c, lx, lt, 8, 8, fill=col, stroke=LINE, r=2); text(c, lab, lx + 12, lt + 7, 'Body', 7.5, GREY_T)
        lx += 20 + pdfmetrics.stringWidth(lab, 'Body', 7.5) + 8
    # mode table
    t1 = lt + 26
    text(c, 'Against today\u2019s commute modes, only Ola Commute pairs transit economics with reliability', M, t1, 'HeadB', 10.5, NAVY)
    text(c, 'Cost: $ low to $$$ high. Dots: 1\u20135, 5 is best', M, t1 + 13, 'Body', 8, GREY_T)
    th = t1 + 20
    cols = [('Mode', 78), ('Cost', 40), ('Reliability', 54), ('Flexibility', 54), ('Scale', 54), ('Why it wins or loses', 0)]
    cols[-1] = (cols[-1][0], lw - sum(w for _, w in cols[:-1]))
    rect(c, M, th, lw, 20, fill=NAVY, r=4)
    x = M
    xs = []
    for nme, w_ in cols:
        xs.append(x); text(c, nme, x + 8, th + 13, 'HeadB', 7.5, white); x += w_
    modes = [('Own bike', '$$', 4, 5, 2, 'Fast, but adds ownership cost, parking friction and congestion.'),
             ('Cab / Auto', '$$$', 3, 5, 3, 'Flexible, but prohibitively expensive for daily commuting.'),
             ('Metro + Auto', '$', 3, 3, 5, 'Cheap backbone, but transfer friction and waits stay high.'),
             ('Fixed bus', '$', 3, 2, 5, 'Great economics, but weak flexibility for fragmented suburban demand.'),
             ('Ola Commute', '$$', 4, 4, 5, 'Mass-transit efficiency, plus it solves the critical connection problem.')]
    mr = 26
    for i, (m_, cost, a, b, s_, why) in enumerate(modes):
        tt = th + 24 + i * mr
        ola = m_ == 'Ola Commute'
        if ola: rect(c, M, tt - 2, lw, mr - 1, fill=LIME_T, stroke=NAVY, r=4, sw=1.1)
        elif i % 2 == 0: rect(c, M, tt - 2, lw, mr - 1, fill=GREY_L, r=4)
        text(c, m_, xs[0] + 8, tt + 13, 'HeadB' if ola else 'HeadM', 8, NAVY)
        text(c, cost, xs[1] + 8, tt + 13, 'HeadB', 8.5, NAVY)
        for j, v in enumerate((a, b, s_)): dots(c, xs[2 + j] + 12, tt + 9.5, v)
        para(c, why, xs[5] + 8, tt, cols[5][1] - 14, size=8, color=NAVY if ola else GREY_T, lead=9.6)
    kt = th + 24 + 5 * mr + 6
    rect(c, M, kt, lw, 550 - kt, fill=NAVY, r=8)
    tag(c, 'KEY INSIGHT', M + 14, kt + 16, LIME)
    para(c, 'The hardest part is <b>not building the AI</b>. It is getting enough people on the same corridors at the same time, and earning the right to coordinate with cities and operators. '
            '<font color="#C6F432"><b>If Ola solves that, the vehicle becomes a commodity and the commute promise becomes the product.</b></font>',
         M + 14, kt + 22, lw - 28, size=8.6, color=white, lead=11)
    # right: why Ola
    rx = M + lw + 20; rw = W - M - rx
    text(c, 'Why Ola: four assets, one mobility layer', rx, top + 8, 'HeadB', 10.5, NAVY)
    text(c, 'Ola Electric today  \u2192  what it becomes', rx, top + 21, 'Body', 8, GREY_T)
    assets = [('code', 'MoveOS + OTA software capability', 'A mobility layer that continuously optimizes routes, charging, vehicle health and rider experience.'),
              ('gear', 'Integrated EV manufacturing & supply chain', 'Standardized feeder vehicles with lower operating costs and highly predictable service uptime.'),
              ('store', 'Large retail, service & charging footprint', 'The physical operating backbone for rapid city launches, fleet maintenance and partner support.'),
              ('star', 'Existing mobility brand & consumer behavior', 'Much lower friction to introduce a daily-use mobility habit than a new market entrant.')]
    ah = 100
    for i, (ic, nm, ds) in enumerate(assets):
        tt = top + 30 + i * (ah + 6)
        card(c, rx, tt, rw, ah, fill=GREY_L)
        icon_badge(c, ic, rx + 22, tt + 24, 14, NAVY, LIME, s=8)
        para(c, nm, rx + 44, tt + 12, rw - 54, font='HeadB', size=8.5, color=NAVY, lead=11)
        pill(c, 'IN 2035', rx + 12, tt + 46, LIME, NAVY, size=6.5, h=12)
        para(c, ds, rx + 12, tt + 63, rw - 24, size=8.5, color=NAVY, lead=10.8)


# ----------------------------------------------------------------- PAGE 5
def page5(c):
    frame(c, 5, 'Path to 100M & metrics', 'Density first: win one corridor, then a city, then 60\u201380 cities',
          'All sources: [1] World Bank, Financing India\u2019s Urban Infrastructure Needs \u00b7 [2] PIB/MoHUA, Metro Rail review 2025 \u00b7 [3] TomTom Traffic Index 2025 \u00b7 [4] NITI Aayog, Transport scenarios \u00b7 '
          '[5] World Bank, Designing Public Transport in India \u00b7 [6] MoHUA, PM-eBus Sewa \u00b7 [7] Ola Electric, MoveOS 5 \u00b7 [8] Ola Electric, DRHP \u00b7 [9] Ola Electric investor relations. '
          'Growth path and economics are illustrative target-state figures from the case; currency unit of the economics: [NEEDS SOURCE].')
    top = 92
    lw = 470
    text(c, 'MVP roadmap: prove the habit before scaling', M, top + 8, 'HeadB', 10.5, NAVY)
    steps = [('0\u20133 MONTHS', '1 corridor', ['500\u20131,000 riders', 'Manual ops', '3\u20135 feeder routes']),
             ('3\u20136 MONTHS', '3 corridors', ['Recurring bookings live', 'Initial transit / operator API integration']),
             ('6\u201312 MONTHS', '1 city', ['10k+ active riders', 'Commute Promise + automated fallback']),
             ('12\u201324 MONTHS', '3 cities', ['100k+ active riders', 'Expand only after unit economics proven'])]
    sw = (lw - 3 * 14) / 4
    rect(c, M + 6, top + 33, lw - 12, 2, fill=GREY_M)
    for i, (mo, hd, bl) in enumerate(steps):
        x = M + i * (sw + 14)
        c.saveState(); c.setFillColor(LIME if i == 3 else NAVY); c.circle(x + 10, Y(top + 34), 5, stroke=0, fill=1); c.restoreState()
        card(c, x, top + 44, sw, 92, fill=GREY_L)
        text(c, mo, x + 10, top + 60, 'HeadB', 6.8, GREY_T)
        text(c, hd, x + 10, top + 77, 'HeadB', 11, NAVY)
        t = top + 84
        for b in bl:
            c.saveState(); c.setFillColor(NAVY); c.circle(x + 13, Y(t + 4.5), 1.6, stroke=0, fill=1); c.restoreState()
            h = para(c, b, x + 19, t, sw - 28, size=8, color=NAVY, lead=9.6); t += h + 2.5
    # chart
    ct = top + 148
    para(c, 'Scale is back-loaded: 45M daily users in 2033 must become 100M by 2035', M, ct, 250, font='HeadB', size=9.5, color=NAVY, lead=12)
    text(c, 'Ola Commute daily users, millions (target path)', M, ct + 36, 'Body', 8, GREY_T)
    base = ct + 158; maxh = 80
    vals = [('2027', .3), ('2029', 3), ('2031', 15), ('2033', 45), ('2035', 100)]
    bw_ = 36; gp = (250 - 5 * bw_) / 4
    hline(c, M, M + 250, base, color=GREY_M, lw=.8)
    for i, (yr, v) in enumerate(vals):
        x = M + i * (bw_ + gp); h = max(maxh * v / 100, 2)
        rect(c, x, base - h, bw_, h, fill=LIME if i == 4 else GREY_M, r=2)
        text(c, ('%gM' % v), x + bw_ / 2, base - h - 5, 'HeadB' if i == 4 else 'HeadM', 8.5, NAVY, 'c')
        text(c, yr, x + bw_ / 2, base + 12, 'Body-B' if i == 4 else 'Body', 8, NAVY, 'c')
    # expansion order
    ex = M + 276; ew = lw - 276
    text(c, 'Expansion order', ex, ct + 8, 'HeadB', 9.5, NAVY)
    order = ['Bengaluru', 'Delhi NCR', 'Mumbai', 'Pune / Hyderabad', 'Chennai / Ahmedabad', 'Next 40\u201360 cities']
    for i, o in enumerate(order):
        tt = ct + 20 + i * 17
        c.saveState(); c.setFillColor(LIME if i == 5 else NAVY); c.circle(ex + 7, Y(tt + 7), 7, stroke=0, fill=1); c.restoreState()
        text(c, str(i + 1), ex + 7, tt + 10, 'HeadB', 7, NAVY if i == 5 else LIME, 'c')
        text(c, o, ex + 20, tt + 10.5, 'Body-B' if i == 5 else 'Body', 8.8, NAVY)
    para(c, 'Launch one dense corridor, then a full city; later cities need transit density and operator supply.', ex, ct + 126, ew, size=7.6, color=GREY_T, lead=9.4)
    # 100M math tile
    rect(c, ex, ct + 168 - 6 + 0, 0, 0)
    mt = ct + 176
    rect(c, M, mt, lw, 38, fill=LIME, r=8)
    text(c, '100M math', M + 12, mt + 15, 'HeadB', 8, NAVY)
    para(c, '100M daily users, not 100M owned vehicles, spread across <b>60\u201380 cities</b>: at 60 cities that averages <b>1.67M daily users per city</b>.',
         M + 80, mt + 7, lw - 92, size=8.5, color=NAVY, lead=11)
    # flywheel
    ft = mt + 54
    fl = ['More commuters', 'Higher feeder utilization', 'Lower cost, better frequency', 'More commuters']
    fw_ = (lw - 3 * 14) / 4
    text(c, 'Growth engine: density flywheel', M, ft - 2, 'HeadB', 8, NAVY)
    ec = 0
    for i, f in enumerate(fl):
        x = M + i * (fw_ + 14)
        rect(c, x, ft + 4, fw_, 24, fill=white, stroke=NAVY if i in (0, 3) else GREY_M, r=12)
        para(c, f, x + 6, ft + 9, fw_ - 12, font='HeadM', size=6.6, color=NAVY, lead=8, align=1)
        if i < 3: arrow(c, x + fw_ + 2, Y(ft + 16), x + fw_ + 12, Y(ft + 16), GREY_T, 1, hs=3)
    # economics bar
    et = ft + 40
    text(c, 'Illustrative target economics per completed commute (currency unit to confirm)', M, et + 4, 'HeadB', 7.4, NAVY)
    text(c, 'Revenue 40', M + lw, et + 4, 'HeadB', 7.4, NAVY, 'r')
    cw1 = lw * 31 / 40
    rect(c, M, et + 10, cw1, 17, fill=GREY_M, r=3); rect(c, M + cw1, et + 10, lw - cw1, 17, fill=LIME, r=3)
    text(c, 'Direct mobility + operator cost: 31', M + 8, et + 22, 'Body-B', 8, NAVY)
    text(c, 'Contribution: 9', M + cw1 + 8, et + 22, 'Body-B', 8, NAVY)

    # right column
    rx = M + lw + 20; rw = W - M - rx
    nh = 258
    rect(c, rx, top, rw, nh, fill=NAVY, r=8)
    pill(c, 'WHAT MUST BE TRUE', rx + 14, top + 12, LIME, NAVY, size=6.8)
    conds = [('Enough riders share the same corridors at the same time',
              'Empty seats destroy pooled-vehicle economics.', 'Launch corridor by corridor; require pre-booking by recurring commuters before adding vehicles.'),
             ('Cities and operators open data, fares and pickup access',
              'Without them the \u201cone product\u201d illusion breaks.', 'Start with one progressive transit agency; open APIs / contracts; keep fallback under tight Ola control.'),
             ('The commute promise holds',
              'A missed transfer destroys trust faster than a cab delay.', 'Guarantee only Ola-controlled legs at first; cap fallback exposure.'),
             ('Unit economics work at scale',
              'Target: 9 contribution on 40 revenue per commute.', 'Drivers: vehicle utilization, routing efficiency, procurement scale, repeat rate.')]
    t = top + 34
    for i, (cond, risk, mit) in enumerate(conds):
        icon_badge(c, 'check', rx + 24, t + 10, 8, LIME, NAVY, s=4.5)
        h = para(c, cond, rx + 38, t + 1, rw - 52, font='HeadB', size=8.3, color=white, lead=10.2)
        h2 = para(c, '<font color="#F2A20C"><b>Risk:</b></font> ' + risk, rx + 38, t + h + 3, rw - 52, size=7.6, color=MUTED_ON_NAVY, lead=9.2)
        h3 = para(c, '<font color="#C6F432"><b>How:</b></font> ' + mit, rx + 38, t + h + h2 + 5, rw - 52, size=7.6, color=white, lead=9.2)
        t += h + h2 + h3 + 12
        if i < 3: hline(c, rx + 14, rx + rw - 14, t - 5, color=NAVY_T)
    # metrics
    mt2 = top + nh + 10
    mh = 550 - mt2
    card(c, rx, mt2, rw, mh, fill=GREY_L)
    text(c, 'Success metrics and kill criteria', rx + 12, mt2 + 17, 'HeadB', 9, NAVY)
    nw_ = 104
    rect(c, rx + 12, mt2 + 26, nw_, 106, fill=LIME, r=7)
    icon(c, 'target', rx + 26, mt2 + 41, 7, NAVY, 1.1)
    text(c, 'NORTH STAR', rx + 38, mt2 + 44, 'HeadB', 6.5, NAVY)
    h = para(c, 'Weekly completed commutes per active rider', rx + 22, mt2 + 52, nw_ - 20, font='HeadB', size=8, color=NAVY, lead=9.6)
    para(c, 'Tests whether Ola is a daily habit, not an occasional fallback ride.', rx + 22, mt2 + 52 + h + 3, nw_ - 20, size=7.2, color=NAVY, lead=8.6)
    sm = [('30-day cohort repeat rate', '\u2265 35% floor'), ('Feeder capacity utilization', '\u2265 55% floor'),
          ('On-time arrival %', '[NEEDS SOURCE] target'), ('Fallback trigger rate', '[NEEDS SOURCE] target'),
          ('Contribution / commute', '9 of 40 target')]
    sx = rx + 12 + nw_ + 10; swd = rw - 12 - nw_ - 10 - 12
    for i, (a, b) in enumerate(sm):
        tt = mt2 + 28 + i * 21
        text(c, a, sx, tt + 7, 'Body', 7.6, GREY_T)
        text(c, b, sx, tt + 17, 'HeadB' if 'NEEDS' not in b else 'Body-I', 7.4, NAVY if 'NEEDS' not in b else GREY_T)
        hline(c, sx, sx + swd, tt + 21)
    kt2 = mt2 + 140
    rect(c, rx + 12, kt2, rw - 24, mh - 140 - 8, fill=white, stroke=AMBER, r=6, sw=1)
    rect(c, rx + 12, kt2, 4, mh - 140 - 8, fill=AMBER, r=1)
    para(c, '<b>KILL / PIVOT:</b> after 12 months in 3 pilot cities, if repeat usage is below 35% <b>and</b> feeder utilization below 55% despite adequate corridor density, halt expansion and redesign the operating model.',
         rx + 24, kt2 + 5, rw - 48, size=7.4, color=NAVY, lead=9)


c = canvas.Canvas('Ola_Commute_Case_Study_2035.pdf', pagesize=(W, H))
c.setTitle('Ola Commute: India does not need another vehicle. It needs a better commute.')
c.setAuthor('Ola Electric Product Strategy Assignment')
for fn in (page1, page2, page3, page4, page5):
    fn(c); c.showPage()
c.save()
print('ok')

"""
deck_kit.py
-----------
Reusable design system + helpers for the Databricks training deck.

Everything renders with native PowerPoint vector shapes (no external images,
no emoji) so the deck looks identical in Microsoft PowerPoint, Google Slides,
Keynote and LibreOffice.  Colours follow the Databricks brand palette.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

# --------------------------------------------------------------------------- #
#  Brand palette (Databricks-inspired)                                        #
# --------------------------------------------------------------------------- #
LAVA      = RGBColor(0xFF, 0x36, 0x21)   # Databricks signature "Lava" red
LAVA_DK   = RGBColor(0xC4, 0x26, 0x18)
LAVA_LT   = RGBColor(0xFF, 0x6B, 0x57)
NAVY      = RGBColor(0x1B, 0x31, 0x39)   # Databricks "Navy 800"
NAVY_2    = RGBColor(0x27, 0x44, 0x4F)
NAVY_3    = RGBColor(0x35, 0x59, 0x66)
INK       = RGBColor(0x0E, 0x1C, 0x21)
OAT       = RGBColor(0xF9, 0xF7, 0xF4)   # Databricks "Oat Light"
OAT_2     = RGBColor(0xEF, 0xEC, 0xE6)
OAT_3     = RGBColor(0xE4, 0xDF, 0xD6)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GREEN     = RGBColor(0x00, 0xA9, 0x72)
GREEN_DK  = RGBColor(0x05, 0x7A, 0x55)
BLUE      = RGBColor(0x22, 0x72, 0xB4)
BLUE_LT   = RGBColor(0x4A, 0x9F, 0xE0)
TEAL      = RGBColor(0x0E, 0x8C, 0x9C)
YELLOW    = RGBColor(0xF5, 0x9E, 0x0B)
PURPLE    = RGBColor(0x7C, 0x5C, 0xCF)
GRAY      = RGBColor(0x46, 0x52, 0x57)   # body text on light
GRAY_2    = RGBColor(0x6B, 0x77, 0x7C)
GRAY_LT   = RGBColor(0x9A, 0xA6, 0xAB)
LINE      = RGBColor(0xDD, 0xD8, 0xCF)   # card borders on light
LINE_DK   = RGBColor(0x3A, 0x53, 0x5C)   # borders on dark

# medal tones for the medallion architecture
BRONZE    = RGBColor(0xB0, 0x6A, 0x3B)
SILVER    = RGBColor(0x8D, 0x9A, 0xA3)
GOLD      = RGBColor(0xD8, 0xA3, 0x2B)

FONT      = "Segoe UI"            # modern, ships on virtually all Office installs
FONT_LT   = "Segoe UI Light"
FONT_SB   = "Segoe UI Semibold"

# 16:9 widescreen canvas
SW, SH    = 13.333, 7.5
MX        = 0.62                  # page side margin
CW        = SW - 2 * MX          # content width
EMU       = 914400

# running page number (set by footer())
_PAGE = {"n": 0}


# --------------------------------------------------------------------------- #
#  Low-level helpers                                                           #
# --------------------------------------------------------------------------- #
def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    cp = prs.core_properties
    cp.title = "Big Data & Databricks — From Fundamentals to the Lakehouse"
    cp.author = "Enterprise Data Platform Training Series"
    cp.subject = "Big Data Fundamentals · Introduction to Databricks · Databricks Architecture"
    cp.category = "Technical Training"
    cp.keywords = "Databricks, Lakehouse, Delta Lake, Apache Spark, Big Data, Unity Catalog"
    return prs


def slide(prs, bg=OAT):
    s = prs.slides.add_slide(prs.slide_layouts[6])   # blank layout
    band(s, 0, 0, SW, SH, bg)                         # full-bleed background
    return s


def _noshadow(sp):
    try:
        sp.shadow.inherit = False
    except Exception:
        pass
    return sp


def soft_shadow(sp, blur=0.10, dist=0.045, direction=5400000, alpha=24, color="1B3139"):
    """Subtle drop shadow via raw XML (blur/dist in inches)."""
    spPr = sp._element.spPr
    for el in spPr.findall(qn('a:effectLst')):
        spPr.remove(el)
    eff = spPr.makeelement(qn('a:effectLst'), {})
    sh = eff.makeelement(qn('a:outerShdw'), {
        'blurRad': str(int(blur * EMU)),
        'dist': str(int(dist * EMU)),
        'dir': str(direction),
        'rotWithShape': '0',
    })
    clr = sh.makeelement(qn('a:srgbClr'), {'val': color})
    clr.append(clr.makeelement(qn('a:alpha'), {'val': str(int(alpha * 1000))}))
    sh.append(clr)
    eff.append(sh)
    spPr.append(eff)
    return sp


def _fill(sp, color):
    if color is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = color


def _line(sp, color, w=1.0):
    if color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = color
        sp.line.width = Pt(w)


def shape(s, kind, x, y, w, h, fill=None, line=None, line_w=1.0, shadow=False, adj=None):
    sp = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    _noshadow(sp)
    if adj is not None:
        try:
            for i, v in enumerate(adj if isinstance(adj, (list, tuple)) else [adj]):
                sp.adjustments[i] = v
        except Exception:
            pass
    _fill(sp, fill)
    _line(sp, line, line_w)
    if shadow:
        soft_shadow(sp)
    sp.text_frame.word_wrap = True
    return sp


def band(s, x, y, w, h, fill, line=None, line_w=1.0):
    return shape(s, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=fill, line=line, line_w=line_w)


def card(s, x, y, w, h, fill=WHITE, line=LINE, line_w=1.0, radius=0.055, shadow=True):
    sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=line,
               line_w=line_w, shadow=shadow, adj=radius)
    return sp


def circle(s, cx, cy, d, fill, line=None, line_w=1.0, shadow=False):
    return shape(s, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d,
                 fill=fill, line=line, line_w=line_w, shadow=shadow)


def grad(sp, c1, c2, angle=90):
    """Two-stop linear gradient with a solid fallback."""
    try:
        f = sp.fill
        f.gradient()
        f.gradient_stops[0].color.rgb = c1
        f.gradient_stops[0].position = 0.0
        f.gradient_stops[1].color.rgb = c2
        f.gradient_stops[1].position = 1.0
        try:
            f.gradient_angle = angle
        except Exception:
            pass
    except Exception:
        _fill(sp, c1)
    return sp


# --------------------------------------------------------------------------- #
#  Text                                                                        #
# --------------------------------------------------------------------------- #
def text(s, x, y, w, h, runs, size=16, color=NAVY, bold=False, italic=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=FONT, spacing=1.0,
         space_after=2, wrap=True):
    """`runs` may be a string (single run) or a list of paragraphs.
    Each paragraph is a string, or a list of run-dicts:
        {"t": str, "size":, "color":, "bold":, "italic":, "font":}
    or a dict with paragraph props + "runs":[...]."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    if isinstance(runs, str):
        runs = [runs]

    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)

        if isinstance(para, dict) and "runs" in para:
            p.alignment = para.get("align", align)
            p.space_after = Pt(para.get("space_after", space_after))
            p.space_before = Pt(para.get("space_before", 0))
            p.line_spacing = para.get("spacing", spacing)
            rlist = para["runs"]
        elif isinstance(para, str):
            rlist = [{"t": para}]
        else:
            rlist = para

        for rd in rlist:
            r = p.add_run()
            r.text = rd["t"]
            r.font.size = Pt(rd.get("size", size))
            r.font.bold = rd.get("bold", bold)
            r.font.italic = rd.get("italic", italic)
            r.font.color.rgb = rd.get("color", color)
            r.font.name = rd.get("font", font)
    return tb


def _hang(p, marL=0.32):
    pPr = p._p.get_or_add_pPr()
    pPr.set('marL', str(int(marL * EMU)))
    pPr.set('indent', str(int(-marL * EMU)))


def bullets(s, x, y, w, h, items, size=15, color=GRAY, marker=LAVA,
            spacing=1.12, gap=7, font=FONT, glyph="▪",
            anchor=MSO_ANCHOR.TOP, bold_lead=False):
    """`items`: list of strings, or (text, level) tuples, or (text, level, color)."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    for i, it in enumerate(items):
        if isinstance(it, str):
            txt, lvl, mk = it, 0, marker
        elif len(it) == 2:
            txt, lvl, mk = it[0], it[1], marker
        else:
            txt, lvl, mk = it[0], it[1], it[2]

        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = spacing
        p.space_after = Pt(gap)
        p.space_before = Pt(0)
        _hang(p, marL=0.30 + lvl * 0.26)

        g = "▪" if lvl == 0 else "–"
        b = p.add_run()
        b.text = g + "   "
        b.font.size = Pt(size)
        b.font.bold = True
        b.font.name = font
        b.font.color.rgb = mk if lvl == 0 else GRAY_LT

        # allow simple "Lead — rest" bolding of the lead phrase
        if bold_lead and ("—" in txt or " – " in txt):
            sep = "—" if "—" in txt else " – "
            lead, rest = txt.split(sep, 1)
            r1 = p.add_run(); r1.text = lead + sep
            r1.font.size = Pt(size); r1.font.bold = True; r1.font.name = font
            r1.font.color.rgb = NAVY
            r2 = p.add_run(); r2.text = rest
            r2.font.size = Pt(size); r2.font.name = font; r2.font.color.rgb = color
        else:
            r = p.add_run(); r.text = txt
            r.font.size = Pt(size); r.font.name = font; r.font.color.rgb = color
    return tb


# --------------------------------------------------------------------------- #
#  Page furniture                                                              #
# --------------------------------------------------------------------------- #
def header(s, kicker, title, accent=LAVA, title_color=NAVY, sub=None):
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 0.60, 0.085, 0.74,
          fill=accent, line=None, adj=0.5)
    text(s, MX + 0.24, 0.50, CW - 0.24, 0.30, kicker.upper(),
         size=11.5, color=accent, bold=True, font=FONT_SB)
    text(s, MX + 0.23, 0.76, CW - 0.24, 0.62, title,
         size=27, color=title_color, bold=True)
    if sub:
        text(s, MX + 0.24, 1.30, CW - 0.24, 0.30, sub, size=13, color=GRAY_2, italic=True)
    band(s, MX, 1.62 if not sub else 1.66, CW, 0.014, OAT_3)


def footer(s, dark=False):
    _PAGE["n"] += 1
    c = GRAY_LT if not dark else RGBColor(0x7E, 0x91, 0x99)
    text(s, MX, 7.06, 7.0, 0.26,
         "Big Data & Databricks  ·  Enterprise Training Series",
         size=8.5, color=c, font=FONT)
    text(s, SW - MX - 1.6, 7.06, 1.6, 0.26, f"{_PAGE['n']:02d}",
         size=8.5, color=c, align=PP_ALIGN.RIGHT, bold=True)


def chip(s, x, y, w, h, label, fill, txt_color=WHITE, size=10.5, bold=True,
         radius=0.5, line=None):
    sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=line, adj=radius)
    tf = sp.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = txt_color; r.font.name = FONT_SB
    return sp


def notes(s, body):
    s.notes_slide.notes_text_frame.text = body


# --------------------------------------------------------------------------- #
#  Connectors / arrows                                                         #
# --------------------------------------------------------------------------- #
def arrow_h(s, x, y, w, color=GRAY_LT, h=0.16):
    """Small horizontal block arrow used between flow steps."""
    sp = shape(s, MSO_SHAPE.RIGHT_ARROW, x, y - h / 2, w, h, fill=color, line=None)
    try:
        sp.adjustments[0] = 0.55
        sp.adjustments[1] = 0.55
    except Exception:
        pass
    return sp


def chevron_step(s, x, y, w, h, fill, label, sub=None, txt=WHITE, sub_txt=None,
                 lbl_size=14, first=False):
    kind = MSO_SHAPE.PENTAGON if not first else MSO_SHAPE.PENTAGON
    sp = shape(s, MSO_SHAPE.CHEVRON, x, y, w, h, fill=fill, line=None)
    try:
        sp.adjustments[0] = 0.45
    except Exception:
        pass
    return sp


# --------------------------------------------------------------------------- #
#  Vector mini-icons (drawn inside a coloured tile)                            #
# --------------------------------------------------------------------------- #
def _ico_shape(s, kind, cx, cy, w, h, color=None):
    return shape(s, kind, cx - w / 2, cy - h / 2, w, h, fill=color, line=None)


def icon(s, kind, cx, cy, size, color=WHITE):
    """Draw a small white (or coloured) vector glyph centred at (cx, cy)."""
    u = size
    k = kind
    try:
        if k == "database":
            sp = _ico_shape(s, MSO_SHAPE.CAN, cx, cy, u * 0.82, u)
            _fill(sp, color)
        elif k == "bolt":
            _fill(_ico_shape(s, MSO_SHAPE.LIGHTNING_BOLT, cx, cy, u * 0.7, u), color)
        elif k == "variety":
            # 2x2 mixed tiles
            g = u * 0.42
            offs = [(-g/2, -g/2), (g/2, -g/2), (-g/2, g/2), (g/2, g/2)]
            shp = [MSO_SHAPE.OVAL, MSO_SHAPE.RECTANGLE, MSO_SHAPE.DIAMOND, MSO_SHAPE.RECTANGLE]
            for (dx, dy), sk in zip(offs, shp):
                _fill(_ico_shape(s, sk, cx + dx, cy + dy, g * 0.74, g * 0.74), color)
        elif k == "check":
            check(s, cx, cy, u, color, weight=u * 0.16)
        elif k == "diamond":
            _fill(_ico_shape(s, MSO_SHAPE.DIAMOND, cx, cy, u * 0.92, u), color)
        elif k == "down":
            _fill(_ico_shape(s, MSO_SHAPE.DOWN_ARROW, cx, cy, u * 0.62, u), color)
        elif k == "gear":
            _fill(_ico_shape(s, MSO_SHAPE.GEAR_6, cx, cy, u, u), color)
        elif k == "chart":
            bars(s, cx, cy, u, color)
        elif k == "people":
            people(s, cx, cy, u, color)
        elif k == "delta":
            _fill(_ico_shape(s, MSO_SHAPE.ISOSCELES_TRIANGLE, cx, cy, u, u * 0.9), color)
        elif k == "ml":
            ml_icon(s, cx, cy, u, color)
        elif k == "lock":
            lock(s, cx, cy, u, color)
        elif k == "cloud":
            _fill(_ico_shape(s, MSO_SHAPE.CLOUD, cx, cy, u * 1.15, u * 0.85), color)
        elif k == "cube":
            _fill(_ico_shape(s, MSO_SHAPE.CUBE, cx, cy, u * 0.85, u * 0.85), color)
        elif k == "cluster":
            cluster_icon(s, cx, cy, u, color)
        elif k == "shield":
            shield(s, cx, cy, u, color)
        elif k == "star":
            _fill(_ico_shape(s, MSO_SHAPE.STAR_5_POINT, cx, cy, u, u), color)
        elif k == "hex":
            _fill(_ico_shape(s, MSO_SHAPE.HEXAGON, cx, cy, u, u * 0.9), color)
        elif k == "flow":
            _fill(_ico_shape(s, MSO_SHAPE.RIGHT_ARROW, cx, cy, u, u * 0.6), color)
        elif k == "warehouse":
            warehouse(s, cx, cy, u, color)
        elif k == "lake":
            _fill(_ico_shape(s, MSO_SHAPE.CLOUD, cx, cy, u * 1.1, u * 0.8), color)
        elif k == "link":
            link_icon(s, cx, cy, u, color)
        elif k == "globe":
            globe(s, cx, cy, u, color)
        elif k == "doc":
            doc_icon(s, cx, cy, u, color)
        else:
            _fill(_ico_shape(s, MSO_SHAPE.OVAL, cx, cy, u * 0.6, u * 0.6), color)
    except Exception:
        _fill(_ico_shape(s, MSO_SHAPE.OVAL, cx, cy, u * 0.6, u * 0.6), color)


def check(s, cx, cy, size, color=WHITE, weight=0.05):
    """A tick mark built from two rotated rounded bars."""
    short = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - size*0.28, cy + size*0.02,
                  size*0.30, weight, fill=color, line=None, adj=0.5)
    short.rotation = 45
    long = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - size*0.06, cy - size*0.20,
                 size*0.58, weight, fill=color, line=None, adj=0.5)
    long.rotation = -52


def bars(s, cx, cy, size, color=WHITE):
    n = 3
    bw = size * 0.20
    gap = size * 0.12
    heights = [size*0.5, size*0.78, size*1.0]
    total = n*bw + (n-1)*gap
    x0 = cx - total/2
    base = cy + size*0.5
    for i, hh in enumerate(heights):
        x = x0 + i*(bw+gap)
        _fill(shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, base-hh, bw, hh,
                    fill=color, line=None, adj=0.25), color)


def people(s, cx, cy, size, color=WHITE):
    head = circle(s, cx, cy - size*0.22, size*0.40, color)
    body = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - size*0.34, cy + size*0.04,
                 size*0.68, size*0.42, fill=color, line=None, adj=0.5)


def ml_icon(s, cx, cy, size, color=WHITE):
    # central node + 3 satellites (neural feel)
    circle(s, cx, cy, size*0.34, color)
    for dx, dy in [(-size*0.42, -size*0.30), (size*0.42, -size*0.30), (0, size*0.44)]:
        # connector
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                    Inches(cx), Inches(cy),
                                    Inches(cx+dx), Inches(cy+dy))
        ln.line.color.rgb = color; ln.line.width = Pt(1.4)
        circle(s, cx+dx, cy+dy, size*0.22, color)


def lock(s, cx, cy, size, color=WHITE):
    body = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx - size*0.34, cy - size*0.05,
                 size*0.68, size*0.5, fill=color, line=None, adj=0.18)
    shackle = shape(s, MSO_SHAPE.BLOCK_ARC, cx - size*0.24, cy - size*0.5,
                    size*0.48, size*0.5, fill=color, line=None)
    try:
        shackle.adjustments[0] = 3.14159 * 1.0
    except Exception:
        pass


def cluster_icon(s, cx, cy, size, color=WHITE):
    g = size*0.40
    for dx, dy in [(-g/2, -g/2), (g/2, -g/2), (-g/2, g/2), (g/2, g/2)]:
        _fill(shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx+dx-g*0.34, cy+dy-g*0.34,
                    g*0.68, g*0.68, fill=color, line=None, adj=0.2), color)


def shield(s, cx, cy, size, color=WHITE):
    sp = shape(s, MSO_SHAPE.PENTAGON, cx - size*0.42, cy - size*0.48,
               size*0.84, size*0.92, fill=color, line=None)
    sp.rotation = 90


def warehouse(s, cx, cy, size, color=WHITE):
    # structured "table" grid (3 cols x 2 rows of equal cells)
    cols, rows = 3, 2
    cw, ch = size*0.26, size*0.30
    gap = size*0.07
    tw = cols*cw + (cols-1)*gap
    th = rows*ch + (rows-1)*gap
    x0, y0 = cx - tw/2, cy - th/2
    for r in range(rows):
        for c in range(cols):
            x = x0 + c*(cw+gap)
            y = y0 + r*(ch+gap)
            _fill(shape(s, MSO_SHAPE.RECTANGLE, x, y, cw, ch, fill=color, line=None), color)


def link_icon(s, cx, cy, size, color=WHITE):
    for dx in (-size*0.18, size*0.18):
        r = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx+dx-size*0.22, cy-size*0.18,
                  size*0.44, size*0.36, fill=None, line=color, line_w=size*9)
        try:
            r.adjustments[0] = 0.5
        except Exception:
            pass


def globe(s, cx, cy, size, color=WHITE):
    ring = shape(s, MSO_SHAPE.OVAL, cx-size*0.46, cy-size*0.46, size*0.92, size*0.92,
                 fill=None, line=color, line_w=size*8)
    v = shape(s, MSO_SHAPE.OVAL, cx-size*0.18, cy-size*0.46, size*0.36, size*0.92,
              fill=None, line=color, line_w=size*6)
    hbar = shape(s, MSO_SHAPE.RECTANGLE, cx-size*0.46, cy-size*0.03, size*0.92, size*0.06,
                 fill=color, line=None)


def doc_icon(s, cx, cy, size, color=WHITE):
    sp = shape(s, MSO_SHAPE.FOLDED_CORNER, cx-size*0.32, cy-size*0.42,
               size*0.64, size*0.84, fill=color, line=None)


# --------------------------------------------------------------------------- #
#  Composite building blocks                                                   #
# --------------------------------------------------------------------------- #
def icon_tile(s, cx, cy, d, ic, tile_color, glyph_color=WHITE, shadow=True, line=None):
    t = circle(s, cx, cy, d, tile_color, line=line, line_w=1.2, shadow=shadow)
    icon(s, ic, cx, cy, d*0.46, glyph_color)
    return t


def number_badge(s, cx, cy, d, n, fill=LAVA, txt=WHITE, size=15):
    c = circle(s, cx, cy, d, fill)
    tf = c.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(n)
    r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = txt; r.font.name = FONT_SB
    return c

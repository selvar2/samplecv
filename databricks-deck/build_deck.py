#!/usr/bin/env python3
"""
build_deck.py
-------------
Generates "Big Data & Databricks — From Fundamentals to the Lakehouse",
a 32-slide, training-ready presentation rendered entirely with native
PowerPoint vector shapes.

Run:  python3 build_deck.py
Out:  Big-Data-and-Databricks-Training.pptx
"""

from math import ceil
from deck_kit import *
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


# ===========================================================================
#  COMPOSITE BUILDING BLOCKS
# ===========================================================================
def dark_bg(s, decorate=True):
    """Premium navy gradient background with subtle geometry."""
    bgrect = s.shapes[0]                       # the full-bleed band added by slide()
    grad(bgrect, NAVY, INK, angle=120)
    if decorate:
        # faint oversized rings / hexagons on the right
        r1 = shape(s, MSO_SHAPE.OVAL, 9.7, -1.6, 5.4, 5.4, fill=None, line=NAVY_3, line_w=1.2)
        r2 = shape(s, MSO_SHAPE.OVAL, 10.9, 0.2, 3.2, 3.2, fill=None, line=NAVY_3, line_w=1.0)
        hx = shape(s, MSO_SHAPE.HEXAGON, 10.55, 4.7, 2.0, 1.8, fill=None, line=LINE_DK, line_w=1.0)
        hx.rotation = 12
        # a couple of solid lava accents
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 12.55, 2.7, 0.5, 0.5, fill=LAVA, line=None, adj=0.25).rotation = 18
        shape(s, MSO_SHAPE.DIAMOND, 9.5, 5.9, 0.34, 0.34, fill=GREEN, line=None)


def flow_steps(s, steps, y_top, card_h=1.95, icon_d=0.96, arrow=True,
               title_size=14.5, desc_size=10.8, x0=None, total_w=None,
               arrow_color=GRAY_LT, card_fill=WHITE):
    """Horizontal sequence of icon cards with connecting arrows.
    steps: list of dict(title, desc, color, icon, badge?)"""
    n = len(steps)
    x0 = MX if x0 is None else x0
    total_w = CW if total_w is None else total_w
    aw = 0.40 if arrow and n > 1 else 0.0
    cw = (total_w - (n - 1) * aw) / n
    for i, st in enumerate(steps):
        x = x0 + i * (cw + aw)
        card(s, x, y_top, cw, card_h, fill=card_fill, line=LINE, shadow=True)
        # color accent bar on top of card
        top = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y_top, cw, 0.12,
                    fill=st["color"], line=None, adj=0.5)
        cx = x + cw / 2
        icon_tile(s, cx, y_top + 0.72, icon_d, st["icon"], st["color"], shadow=True)
        if st.get("badge"):
            number_badge(s, x + cw - 0.34, y_top + 0.34, 0.40, st["badge"],
                         fill=NAVY, txt=WHITE, size=12)
        text(s, x + 0.12, y_top + 1.24, cw - 0.24, 0.34, st["title"],
             size=title_size, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
        text(s, x + 0.16, y_top + 1.58, cw - 0.32, card_h - 1.6, st["desc"],
             size=desc_size, color=GRAY_2, align=PP_ALIGN.CENTER, spacing=1.05)
        if arrow and i < n - 1:
            arrow_h(s, x + cw + 0.04, y_top + card_h / 2, aw - 0.08, arrow_color, h=0.18)


def grid_cards(s, items, cols, x, y, w, h, gx=0.28, gy=0.28,
               icon_d=0.74, title_size=14, desc_size=11, desc_color=GRAY_2):
    """Generic grid of feature cards. item: dict(icon,color,title,desc)."""
    n = len(items)
    rows = ceil(n / cols)
    cw = (w - (cols - 1) * gx) / cols
    ch = (h - (rows - 1) * gy) / rows
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        cx = x + c * (cw + gx)
        cy = y + r * (ch + gy)
        card(s, cx, cy, cw, ch, fill=WHITE, line=LINE, shadow=True)
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, 0.10, ch, fill=it["color"],
              line=None, adj=0.5)
        icon_tile(s, cx + 0.55, cy + 0.52, icon_d, it["icon"], it["color"], shadow=False)
        text(s, cx + 1.02, cy + 0.18, cw - 1.18, 0.7, it["title"],
             size=title_size, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
        text(s, cx + 0.30, cy + 0.95, cw - 0.56, ch - 1.05, it["desc"],
             size=desc_size, color=desc_color, spacing=1.08)


def pipeline(s, stages, y_top, box_h=0.92, ex_h=1.15, label_size=11.5,
             ex_size=10, arrow_color=LAVA):
    """Labelled stage boxes with example chips beneath. stage: dict(title,examples,color,icon)."""
    n = len(stages)
    aw = 0.34
    bw = (CW - (n - 1) * aw) / n
    for i, stg in enumerate(stages):
        x = MX + i * (bw + aw)
        # stage header box
        b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y_top, bw, box_h,
                  fill=stg["color"], line=None, adj=0.14, shadow=True)
        soft_shadow(b)
        icon(s, stg["icon"], x + 0.32, y_top + box_h / 2, 0.38, WHITE)
        text(s, x + 0.52, y_top, bw - 0.62, box_h, stg["title"],
             size=label_size, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE,
             align=PP_ALIGN.CENTER, spacing=0.92)
        # examples card
        card(s, x, y_top + box_h + 0.18, bw, ex_h, fill=WHITE, line=LINE, shadow=True)
        ex = [f"{e}" for e in stg["examples"]]
        bullets(s, x + 0.18, y_top + box_h + 0.34, bw - 0.34, ex_h - 0.3, ex,
                size=ex_size, marker=stg["color"], gap=4, spacing=1.05)
        if i < n - 1:
            arrow_h(s, x + bw + 0.02, y_top + box_h / 2, aw - 0.06, arrow_color, h=0.17)


def timeline(s, events, y_center, accent=LAVA):
    """Horizontal timeline, captions alternating above/below the spine."""
    n = len(events)
    band(s, MX + 0.2, y_center - 0.018, CW - 0.4, 0.036, OAT_3)
    step = (CW - 0.4) / n
    for i, ev in enumerate(events):
        cx = MX + 0.2 + step * (i + 0.5)
        col = ev.get("color", accent)
        above = (i % 2 == 0)
        ty = y_center - 1.62 if above else y_center + 0.34
        # connector stick
        band(s, cx - 0.006, min(y_center, ty + (1.28 if above else 0)),
             0.012, 1.28 if above else 0.30, OAT_3)
        # year chip
        chy = ty if above else ty
        chip(s, cx - 0.55, chy, 1.10, 0.34, ev["year"], col, WHITE, size=12, radius=0.5)
        # title + desc
        if above:
            text(s, cx - 1.15, ty + 0.40, 2.30, 0.34, ev["title"], size=11.5,
                 color=NAVY, bold=True, align=PP_ALIGN.CENTER, spacing=1.0)
            text(s, cx - 1.2, ty + 0.74, 2.40, 0.5, ev["desc"], size=9.3,
                 color=GRAY_2, align=PP_ALIGN.CENTER, spacing=1.0)
        else:
            text(s, cx - 1.15, ty + 0.42, 2.30, 0.34, ev["title"], size=11.5,
                 color=NAVY, bold=True, align=PP_ALIGN.CENTER, spacing=1.0)
            text(s, cx - 1.2, ty + 0.76, 2.40, 0.5, ev["desc"], size=9.3,
                 color=GRAY_2, align=PP_ALIGN.CENTER, spacing=1.0)
        circle(s, cx, y_center, 0.22, col, line=WHITE, line_w=2.2, shadow=True)


def vs_table(s, x, y, w, headers, rows, hcolors):
    """3-column comparison. headers: (aspect, left, right). rows: list of (aspect,left,right)."""
    aspect_w = w * 0.24
    col_w = (w - aspect_w) / 2
    hh = 0.56
    rh = (6.78 - (y + hh)) / len(rows)
    rh = min(rh, 0.66)
    # header chips
    chip(s, x, y, aspect_w - 0.1, hh, headers[0], NAVY, WHITE, size=12.5, radius=0.16)
    chip(s, x + aspect_w, y, col_w - 0.1, hh, headers[1], hcolors[0], WHITE, size=12.5, radius=0.16)
    chip(s, x + aspect_w + col_w, y, col_w - 0.1, hh, headers[2], hcolors[1], WHITE, size=12.5, radius=0.16)
    yy = y + hh + 0.10
    for i, (asp, lt, rt) in enumerate(rows):
        if i % 2 == 0:
            band(s, x, yy, w, rh, OAT_2)
        text(s, x + 0.12, yy, aspect_w - 0.24, rh, asp, size=11.5, color=NAVY,
             bold=True, anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
        text(s, x + aspect_w + 0.14, yy, col_w - 0.28, rh, lt, size=11, color=GRAY,
             anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
        text(s, x + aspect_w + col_w + 0.14, yy, col_w - 0.28, rh, rt, size=11,
             color=GRAY, anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
        yy += rh


def hub_spoke(s, cx, cy, hub_label, spokes):
    """Central hub with labelled spokes around it. spoke: dict(title,desc,color,icon,pos)."""
    # connectors first (so they sit beneath nodes)
    for sp in spokes:
        x, y = sp["pos"]
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(cx), Inches(cy),
                                    Inches(x), Inches(y))
        ln.line.color.rgb = OAT_3
        ln.line.width = Pt(1.6)
    # spokes
    for sp in spokes:
        x, y = sp["pos"]
        w, h = 2.55, 0.92
        card(s, x - w / 2, y - h / 2, w, h, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x - w / 2 + 0.5, y, 0.62, sp["icon"], sp["color"], shadow=False)
        text(s, x - w / 2 + 0.92, y - h / 2 + 0.10, w - 1.0, 0.34, sp["title"],
             size=11.8, color=NAVY, bold=True, spacing=1.0)
        text(s, x - w / 2 + 0.92, y - h / 2 + 0.45, w - 1.0, 0.42, sp["desc"],
             size=8.8, color=GRAY_2, spacing=0.98)
    # hub on top
    d = 1.9
    circle(s, cx, cy, d, LAVA, line=WHITE, line_w=3, shadow=True)
    circle(s, cx, cy, d - 0.26, None, line=RGBColor(0xFF, 0x8A, 0x78), line_w=1.4)
    text(s, cx - d / 2, cy - 0.42, d, 0.9, hub_label, size=15, color=WHITE,
         bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=0.95)


def takeaway(s, x, y, w, txt, color=GREEN, icon_kind="check", h=0.82):
    card(s, x, y, w, h, fill=WHITE, line=LINE, shadow=True)
    icon_tile(s, x + 0.5, y + h / 2, 0.58, icon_kind, color, shadow=False)
    text(s, x + 0.95, y, w - 1.1, h, txt, size=11.5, color=GRAY,
         anchor=MSO_ANCHOR.MIDDLE, spacing=1.05)


# ===========================================================================
#  SLIDES
# ===========================================================================
def s_cover(prs):
    s = slide(prs, bg=NAVY)
    dark_bg(s)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 1.35, 0.09, 2.0, fill=LAVA, line=None, adj=0.5)
    text(s, MX + 0.30, 1.30, 9, 0.3, "ENTERPRISE DATA PLATFORM  ·  TRAINING SERIES",
         size=12.5, color=LAVA_LT, bold=True, font=FONT_SB)
    text(s, MX + 0.27, 1.72, 11.4, 1.5,
         [[{"t": "Big Data ", "color": WHITE, "size": 53, "bold": True},
           {"t": "& Databricks", "color": WHITE, "size": 53, "bold": True}]],
         spacing=1.0)
    text(s, MX + 0.27, 2.74, 11.4, 0.8, "From Fundamentals to the Lakehouse",
         size=29, color=LAVA, bold=True, font=FONT_LT)
    text(s, MX + 0.30, 3.66, 9.6, 0.7,
         "A consulting-grade journey through modern data architecture — why Big Data "
         "matters, what the Databricks Lakehouse is, and how it is engineered end to end.",
         size=14, color=RGBColor(0xC4, 0xD0, 0xD4), spacing=1.25)
    # section chips
    chips = [("01", "Big Data Fundamentals"), ("02", "Introduction to Databricks"),
             ("03", "Databricks Architecture")]
    cx = MX + 0.30
    for no, label in chips:
        w = 3.62
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx, 4.85, w, 0.62,
              fill=None, line=LINE_DK, line_w=1.3, adj=0.5)
        text(s, cx + 0.30, 4.85, w - 0.45, 0.62,
             [[{"t": no + "    ", "color": LAVA, "size": 13, "bold": True},
               {"t": label, "color": WHITE, "size": 12, "bold": True}]],
             anchor=MSO_ANCHOR.MIDDLE)
        cx += w + 0.26
    band(s, MX + 0.30, 6.05, 6.5, 0.02, LINE_DK)
    text(s, MX + 0.30, 6.22, 11, 0.4,
         "Audience:  Data Engineers · Analysts · Data Scientists · Cloud Architects · Technical Leaders",
         size=11.5, color=GRAY_LT)
    text(s, MX + 0.30, 6.62, 11, 0.4,
         "Powered by the Databricks Lakehouse Platform  ·  Apache Spark · Delta Lake · Unity Catalog",
         size=11.5, color=GRAY_LT, italic=True)
    notes(s,
          "Welcome the audience and frame the session. This is a foundational-to-architecture "
          "training arc in three parts: (1) Big Data fundamentals and why the field exists, "
          "(2) what Databricks is and the Lakehouse paradigm, and (3) how the platform is "
          "architected end to end. Set expectations: by the end, attendees will understand the "
          "control vs. compute plane split, Delta Lake, the medallion architecture, and how data "
          "flows from source to dashboard. Ask the room about their roles to calibrate depth.")


def s_agenda(prs):
    s = slide(prs)
    header(s, "Course Roadmap", "Your Learning Journey")
    secs = [
        dict(no="01", color=BLUE, icon="database", title="Big Data Fundamentals",
             items=["Why Big Data matters", "The 5 V's & challenges",
                    "Technologies & ecosystem", "Real-world use cases"],
             outcome="Speak the language of Big Data with confidence."),
        dict(no="02", color=LAVA, icon="bolt", title="Introduction to Databricks",
             items=["What & why Databricks", "The Lakehouse concept",
                    "Unified analytics platform", "Core components & benefits"],
             outcome="Explain the Lakehouse and what Databricks unifies."),
        dict(no="03", color=GREEN, icon="cluster", title="Databricks Architecture",
             items=["Control & compute planes", "Spark, Delta & Medallion",
                    "Clusters, security, data flow", "Integration architecture"],
             outcome="Describe how Databricks runs end to end."),
    ]
    cw = (CW - 2 * 0.4) / 3
    for i, sec in enumerate(secs):
        x = MX + i * (cw + 0.4)
        card(s, x, 2.05, cw, 4.5, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.05, cw, 0.14, sec["color"])
        # remove square corners overlap by rounding handled visually; add header zone
        icon_tile(s, x + 0.78, 2.95, 1.0, sec["icon"], sec["color"], shadow=True)
        text(s, x + 1.5, 2.62, cw - 1.6, 0.4, "SECTION " + sec["no"], size=11,
             color=sec["color"], bold=True, font=FONT_SB)
        text(s, x + 1.5, 2.92, cw - 1.6, 0.7, sec["title"], size=15.5, color=NAVY,
             bold=True, spacing=0.98)
        band(s, x + 0.42, 3.66, cw - 0.84, 0.014, OAT_3)
        bullets(s, x + 0.46, 3.84, cw - 0.8, 2.0,
                [(it, 0) for it in sec["items"]], size=12.5, marker=sec["color"],
                gap=12, spacing=1.05)
        band(s, x + 0.42, 5.72, cw - 0.84, 0.014, OAT_3)
        text(s, x + 0.46, 5.86, cw - 0.86, 0.6,
             [[{"t": "OUTCOME   ", "color": sec["color"], "bold": True, "size": 9.5,
                "font": FONT_SB},
               {"t": sec["outcome"], "color": GRAY_2, "size": 10.5, "italic": True}]],
             spacing=1.12)
    text(s, MX, 6.74, CW, 0.3,
         "Twelve concepts · three sections · one continuous narrative — from raw data to a governed, AI-ready Lakehouse.",
         size=11.5, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "Walk the audience through the three sections and the logical build-up. Emphasise that "
          "each section answers a question: Section 1 — why does Big Data need new tools? Section 2 "
          "— what is Databricks' answer (the Lakehouse)? Section 3 — how is it built? Tell learners "
          "they don't need prior Spark experience; concepts are layered. Mention timing/breaks if relevant.")


def s_divider(prs, no, kicker, title, items, icon_kind, color=LAVA):
    s = slide(prs, bg=NAVY)
    dark_bg(s, decorate=True)
    text(s, MX, 1.6, 6, 2.4, no, size=200, color=NAVY_2, bold=True, font=FONT_LT)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.05, 3.62, 0.85, 0.10, fill=color, line=None, adj=0.5)
    text(s, MX + 0.05, 3.0, 8, 0.4, kicker.upper(), size=13.5, color=color, bold=True, font=FONT_SB)
    text(s, MX, 3.78, 8.4, 1.2, title, size=40, color=WHITE, bold=True, spacing=0.98)
    bullets(s, MX + 0.05, 5.2, 7.6, 1.6, [(it, 0) for it in items],
            size=14.5, color=RGBColor(0xCC, 0xD6, 0xDA), marker=color, gap=9, spacing=1.1)
    icon_tile(s, 10.7, 3.9, 2.5, icon_kind, color, glyph_color=WHITE, shadow=True,
              line=RGBColor(0xFF, 0x8A, 0x78) if color == LAVA else None)
    footer(s, dark=True)
    notes(s, f"Section {no}: {title}. Transition slide — pause, then preview the four ideas listed. "
             "Use it to re-anchor the narrative and tell the audience what they'll be able to do by the "
             "end of this section.")


# ---------- SECTION 1 : BIG DATA FUNDAMENTALS ----------
def s_what_bigdata(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "What Is Big Data?")
    # definition card
    card(s, MX, 2.0, 6.55, 2.55, fill=NAVY, line=None, shadow=True)
    text(s, MX + 0.4, 2.28, 5.8, 0.3, "DEFINITION", size=11, color=LAVA_LT, bold=True, font=FONT_SB)
    text(s, MX + 0.4, 2.62, 5.85, 1.8,
         "Big Data refers to datasets so large, fast-moving, and varied that traditional "
         "databases and single-server tools can no longer capture, store, or process them — "
         "requiring distributed, horizontally-scalable systems to turn raw signals into value.",
         size=14.5, color=WHITE, spacing=1.28)
    # key points
    bullets(s, MX + 0.05, 4.85, 6.5, 1.8, [
        "Not just size — it is volume, speed, and diversity combined",
        "Powered by distributed computing across clusters of machines",
        "80%+ of new data is unstructured: text, images, logs, video, IoT",
    ], size=12.8, marker=LAVA, gap=10)
    # stat tiles
    stats = [("402M+", "terabytes of data\ncreated every day", BLUE),
             ("181 ZB", "global data volume\nby 2025", LAVA),
             ("80%+", "of enterprise data\nis unstructured", GREEN),
             ("5G · IoT", "billions of connected\nsensors & devices", PURPLE)]
    gx, gy = 0.3, 0.3
    tw, th = (4.55 - gx) / 2, (4.55 - gy) / 2
    x0 = 7.55
    for i, (big, lab, col) in enumerate(stats):
        r, c = divmod(i, 2)
        x = x0 + c * (tw + gx); y = 2.0 + r * (th + gy)
        card(s, x, y, tw, th, fill=WHITE, line=LINE, shadow=True)
        band(s, x, y, 0.10, th, col)
        text(s, x + 0.28, y + 0.18, tw - 0.4, 0.6, big, size=26, color=col, bold=True)
        text(s, x + 0.30, y + 0.78, tw - 0.45, 0.9, lab.replace("\n", " "),
             size=11, color=GRAY, spacing=1.05)
    footer(s)
    notes(s,
          "Define Big Data beyond 'a lot of data'. The key shift is that the data outgrew the machine: "
          "you can no longer scale up a single server, so you scale OUT across a cluster. Use the stats "
          "to make it visceral — hundreds of millions of terabytes daily, most of it unstructured. "
          "Real examples: a jet engine emits ~10TB per 30 minutes of flight; a single autonomous car "
          "generates terabytes per day. These numbers motivate everything that follows. (Figures are "
          "widely-cited industry estimates — present as orders of magnitude, not precise values.)")


def s_history(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "The Evolution of Big Data")
    events = [
        dict(year="1990s", title="Relational Era", desc="RDBMS & data warehouses; structured, vertical scaling", color=NAVY_2),
        dict(year="2003-04", title="Google Papers", desc="GFS & MapReduce define web-scale computing", color=BLUE),
        dict(year="2006", title="Apache Hadoop", desc="Open-source HDFS + MapReduce go mainstream", color=TEAL),
        dict(year="2010s", title="NoSQL & Cloud", desc="Elastic storage, streaming, data lakes emerge", color=GREEN),
        dict(year="2013", title="Apache Spark", desc="In-memory engine, 100x faster than MapReduce", color=YELLOW),
        dict(year="2020", title="The Lakehouse", desc="Delta Lake unifies lake + warehouse", color=LAVA),
        dict(year="2023+", title="Data + AI", desc="GenAI & LLMs on governed enterprise data", color=PURPLE),
    ]
    timeline(s, events, y_center=4.1)
    text(s, MX, 6.5, CW, 0.4,
         "Each wave solved the prior era's bottleneck — scale, then speed, then unification, and now intelligence.",
         size=12, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "Tell the story as a series of bottlenecks being broken. Warehouses handled structured data but "
          "couldn't scale to the web. Google's 2003-04 GFS/MapReduce papers inspired Hadoop (2006), which "
          "made distributed batch processing accessible but was slow and hard to use. Spark (2013, from UC "
          "Berkeley's AMPLab — the founders of Databricks) brought in-memory speed. Data lakes gave cheap "
          "storage but became 'swamps' with no reliability. The Lakehouse (2020) merged lake economics with "
          "warehouse reliability — and is now the foundation for enterprise AI.")


def s_5vs(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "The 5 V's of Big Data")
    steps = [
        dict(title="Volume", icon="database", color=BLUE, badge=1,
             desc="Terabytes to petabytes. Scale-out storage across clusters."),
        dict(title="Velocity", icon="bolt", color=LAVA, badge=2,
             desc="Speed of arrival — batch, micro-batch and real-time streams."),
        dict(title="Variety", icon="variety", color=GREEN, badge=3,
             desc="Structured, semi-structured & unstructured formats together."),
        dict(title="Veracity", icon="check", color=YELLOW, badge=4,
             desc="Trust & quality — accuracy, completeness, consistency."),
        dict(title="Value", icon="diamond", color=PURPLE, badge=5,
             desc="The goal — turning raw data into decisions & outcomes."),
    ]
    flow_steps(s, steps, y_top=2.35, card_h=2.45, icon_d=1.02, arrow=True)
    text(s, MX, 5.25, CW, 0.4,
         "Volume · Velocity · Variety describe the data;  Veracity · Value describe whether it can be trusted and what it returns.",
         size=12.3, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    # mini examples strip
    card(s, MX, 5.75, CW, 0.95, fill=OAT_2, line=LINE, shadow=False)
    text(s, MX + 0.35, 5.86, CW - 0.7, 0.8,
         [[{"t": "Enterprise lens  ", "bold": True, "color": NAVY, "size": 12},
           {"t": "Volume: ", "bold": True, "color": BLUE, "size": 11.5},
           {"t": "years of transactions   ", "color": GRAY, "size": 11.5},
           {"t": "Velocity: ", "bold": True, "color": LAVA, "size": 11.5},
           {"t": "card swipes per second   ", "color": GRAY, "size": 11.5},
           {"t": "Variety: ", "bold": True, "color": GREEN, "size": 11.5},
           {"t": "JSON, images, clickstream   ", "color": GRAY, "size": 11.5},
           {"t": "Veracity: ", "bold": True, "color": YELLOW, "size": 11.5},
           {"t": "duplicate / missing fields   ", "color": GRAY, "size": 11.5},
           {"t": "Value: ", "bold": True, "color": PURPLE, "size": 11.5},
           {"t": "real-time fraud blocked", "color": GRAY, "size": 11.5}]],
         anchor=MSO_ANCHOR.MIDDLE, spacing=1.3)
    footer(s)
    notes(s,
          "The 5 V's are the canonical definition of Big Data. Explain each with a fraud-detection example: "
          "Volume = years of card transactions; Velocity = thousands of swipes per second that must be scored "
          "in milliseconds; Variety = transaction records + device fingerprints + geolocation; Veracity = "
          "messy, duplicated, missing data that must be cleansed; Value = the business outcome (a blocked "
          "fraudulent charge). Note some frameworks cite 3 V's (the original Gartner set) or more; 5 is the "
          "common training standard. Veracity and Value are what make a project succeed or fail.")


def s_trad_vs_big(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "Traditional Data vs. Big Data")
    rows = [
        ("Volume", "Gigabytes to terabytes", "Terabytes to petabytes & beyond"),
        ("Data Types", "Structured rows & columns", "Structured + semi + unstructured"),
        ("Schema", "Schema-on-write (rigid)", "Schema-on-read (flexible)"),
        ("Processing", "Centralized, single server", "Distributed across clusters"),
        ("Scaling", "Scale up — bigger machine", "Scale out — more machines"),
        ("Architecture", "Monolithic RDBMS / warehouse", "Data lake / Lakehouse, decoupled"),
        ("Cost Model", "Costly proprietary hardware", "Commodity & elastic cloud"),
    ]
    vs_table(s, MX, 2.0, CW, ("Aspect", "Traditional Data", "Big Data"),
             rows, hcolors=(NAVY_2, LAVA))
    footer(s)
    notes(s,
          "This contrast is the heart of the 'why'. The single most important row is Scaling: traditional "
          "systems scale UP (a bigger, pricier server with a hard ceiling), while Big Data scales OUT "
          "(add commodity nodes, near-limitless). Schema-on-write vs schema-on-read is the second key idea: "
          "warehouses force structure before you store; lakes let you store first and apply structure when "
          "you read. Big Data isn't 'better' — it's a different toolset for a different problem. Many "
          "enterprises run both, which is exactly the tension the Lakehouse resolves.")


def s_challenges(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "Big Data Challenges")
    items = [
        dict(icon="database", color=BLUE, title="Storage & Scale",
             desc="Cost-effectively storing petabytes across distributed, fault-tolerant systems."),
        dict(icon="check", color=YELLOW, title="Data Quality",
             desc="Duplicates, missing values and inconsistency erode trust (the Veracity problem)."),
        dict(icon="link", color=TEAL, title="Integration & Silos",
             desc="Hundreds of sources and formats fragmented across disconnected systems."),
        dict(icon="bolt", color=LAVA, title="Real-Time Processing",
             desc="Acting on streaming events in milliseconds, not overnight batch windows."),
        dict(icon="people", color=GREEN, title="Skills & Complexity",
             desc="Scarce talent and brittle, hand-stitched toolchains slow delivery."),
        dict(icon="lock", color=PURPLE, title="Governance & Security",
             desc="Privacy, access control, lineage and regulatory compliance (GDPR, HIPAA)."),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=14, desc_size=11)
    footer(s)
    notes(s,
          "Frame these as the problems any Big Data platform must solve — and a preview of why Databricks "
          "exists. Storage is largely solved by cheap cloud object stores. Quality and Governance are where "
          "most projects fail: a 'data lake' with no reliability or access control becomes a 'data swamp'. "
          "Real-time and Skills/Complexity are about operational maturity. As you cover Databricks later, "
          "call back to this slide — Delta Lake addresses quality, Unity Catalog addresses governance, the "
          "unified workspace addresses skills/complexity.")


def s_technologies(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "The Big Data Technology Landscape")
    items = [
        dict(icon="down", color=TEAL, title="Ingestion",
             desc="Kafka · Spark Structured Streaming · Fivetran · NiFi · Auto Loader"),
        dict(icon="cube", color=BLUE, title="Storage",
             desc="HDFS · Amazon S3 · ADLS · Google Cloud Storage · Delta Lake"),
        dict(icon="gear", color=LAVA, title="Processing",
             desc="Apache Spark · Flink · MapReduce · Photon · dbt"),
        dict(icon="flow", color=GREEN, title="Orchestration",
             desc="Apache Airflow · Databricks Workflows · Dagster"),
        dict(icon="chart", color=PURPLE, title="Query & Analytics",
             desc="Hive · Trino / Presto · Databricks SQL · Snowflake"),
        dict(icon="ml", color=YELLOW, title="ML & AI",
             desc="MLflow · TensorFlow · PyTorch · scikit-learn · Mosaic AI"),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=14.5, desc_size=10.8)
    footer(s)
    notes(s,
          "Map the ecosystem by function, not by vendor. Every Big Data stack has these layers: ingest, "
          "store, process, orchestrate, query, and ML/AI. The key takeaway: traditionally each layer was a "
          "separate tool to integrate, secure, and operate — enormous complexity. This sets up the Databricks "
          "value proposition: one platform that spans processing, query, ML and orchestration on open storage, "
          "collapsing this landscape. Note Spark appears in both processing and ML — it's the common engine.")


def s_ecosystem(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "The Big Data Ecosystem — End to End")
    stages = [
        dict(title="Data\nSources", icon="globe", color=NAVY_2,
             examples=["Apps & databases", "IoT / sensors", "Logs & clickstream", "APIs & files"]),
        dict(title="Ingestion", icon="down", color=TEAL,
             examples=["Kafka", "Auto Loader", "Fivetran", "Batch + stream"]),
        dict(title="Storage", icon="cube", color=BLUE,
             examples=["S3 / ADLS / GCS", "Delta Lake", "Data lake", "Open formats"]),
        dict(title="Processing", icon="gear", color=LAVA,
             examples=["Apache Spark", "Photon", "ETL / ELT", "Transform & clean"]),
        dict(title="Analytics", icon="ml", color=GREEN,
             examples=["SQL analytics", "Machine learning", "Data science", "AI / GenAI"]),
        dict(title="BI & Viz", icon="chart", color=PURPLE,
             examples=["Dashboards", "Power BI", "Tableau", "Reports & alerts"]),
    ]
    pipeline(s, stages, y_top=2.45, box_h=1.0, ex_h=1.5, label_size=11, ex_size=9.8)
    text(s, MX, 5.95, CW, 0.6,
         [[{"t": "Raw signals flow left-to-right, gaining structure and value at each stage — "
                 "the same backbone the Databricks Lakehouse implements as ", "color": GRAY_2, "size": 12, "italic": True},
           {"t": "one unified platform.", "color": LAVA, "size": 12, "bold": True, "italic": True}]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.2)
    footer(s)
    notes(s,
          "This is the reference pipeline for the entire field — memorise the six stages: Sources → Ingestion "
          "→ Storage → Processing → Analytics → Visualization. Data enters raw and noisy on the left and exits "
          "as trusted insight on the right. Traditionally each stage is a different product. The punchline, "
          "which you'll return to in Section 3: Databricks implements this whole backbone as one platform on "
          "open storage, which is what 'unified analytics' means. Foreshadow the medallion architecture here.")


def s_usecases(prs):
    s = slide(prs)
    header(s, "Big Data Fundamentals", "Big Data in the Real World")
    items = [
        dict(icon="diamond", color=BLUE, title="Financial Services",
             desc="Real-time fraud detection, risk modelling & algorithmic trading on streaming transactions."),
        dict(icon="ml", color=GREEN, title="Healthcare & Life Sciences",
             desc="Genomics at scale, medical imaging AI and predictive patient diagnostics."),
        dict(icon="chart", color=LAVA, title="Retail & E-Commerce",
             desc="Personalized recommendations, demand forecasting & dynamic pricing."),
        dict(icon="gear", color=TEAL, title="Manufacturing",
             desc="Predictive maintenance and IoT sensor analytics across the factory floor."),
        dict(icon="globe", color=PURPLE, title="Telecom & Media",
             desc="Network optimization, churn prediction and content recommendation."),
        dict(icon="bolt", color=YELLOW, title="Energy & Mobility",
             desc="Smart-grid balancing, fleet telematics and autonomous-vehicle data."),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=14, desc_size=10.8)
    footer(s)
    notes(s,
          "Make it concrete and industry-relevant to your audience. Pick the two verticals closest to the "
          "room and go deep. Strong story: a global bank scoring every card transaction for fraud in under "
          "50ms across billions of events — that single use case needs all 5 V's and the full ecosystem. "
          "Healthcare genomics is another vivid one: a single human genome is ~200GB raw. These examples "
          "prove Big Data is a business capability, not an IT science project.")


# ---------- SECTION 2 : INTRODUCTION TO DATABRICKS ----------
def s_what_databricks(prs):
    s = slide(prs)
    header(s, "Introduction to Databricks", "What Is Databricks?")
    card(s, MX, 2.0, 7.1, 2.5, fill=NAVY, line=None, shadow=True)
    text(s, MX + 0.4, 2.26, 6.4, 0.3, "DEFINITION", size=11, color=LAVA_LT, bold=True, font=FONT_SB)
    text(s, MX + 0.4, 2.60, 6.4, 1.9,
         [[{"t": "Databricks is a unified ", "color": WHITE, "size": 15},
           {"t": "Lakehouse platform", "color": LAVA_LT, "size": 15, "bold": True},
           {"t": " that combines data engineering, data warehousing, data science, "
                 "analytics, AI and machine learning in a single collaborative "
                 "environment — built on open standards and powered by ", "color": WHITE, "size": 15},
           {"t": "Apache Spark and Delta Lake.", "color": LAVA_LT, "size": 15, "bold": True}]],
         spacing=1.32)
    facts = [
        dict(icon="bolt", color=LAVA, title="Born from Spark",
             desc="Founded 2013 by the creators of Apache Spark."),
        dict(icon="cloud", color=BLUE, title="Multi-Cloud",
             desc="Runs natively on AWS, Azure and Google Cloud."),
        dict(icon="hex", color=GREEN, title="Open-Source Roots",
             desc="Created Spark, Delta Lake, MLflow & Unity Catalog."),
        dict(icon="people", color=PURPLE, title="One Platform",
             desc="Every data persona in one governed workspace."),
    ]
    x0 = MX + 7.1 + 0.4
    rw = CW + MX - x0
    gy = 0.10
    th = (2.5 - 3 * gy) / 4
    for i, it in enumerate(facts):
        y = 2.0 + i * (th + gy)
        card(s, x0, y, rw, th, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x0 + 0.42, y + th / 2, 0.5, it["icon"], it["color"], shadow=False)
        text(s, x0 + 0.80, y + 0.07, rw - 0.95, 0.26, it["title"], size=12,
             color=NAVY, bold=True)
        text(s, x0 + 0.80, y + 0.31, rw - 0.95, 0.24, it["desc"], size=9.3,
             color=GRAY_2, spacing=1.0)
    # bottom band: the GOOD example contrast
    card(s, MX, 4.75, CW, 1.85, fill=OAT_2, line=LINE, shadow=False)
    text(s, MX + 0.4, 4.92, CW - 0.8, 0.3, "WHY THE WORDING MATTERS", size=11, color=LAVA, bold=True, font=FONT_SB)
    text(s, MX + 0.4, 5.26, 5.5, 1.2,
         [[{"t": "Vague:  ", "color": LAVA, "size": 12.5, "bold": True},
           {"t": "“Databricks is a cloud platform used for analytics.”",
            "color": GRAY, "size": 12.5, "italic": True}]], spacing=1.2)
    band(s, MX + 6.2, 5.0, 0.014, 1.4, OAT_3)
    text(s, MX + 6.55, 5.16, 5.0, 1.3,
         [[{"t": "Precise:  ", "color": GREEN_DK, "size": 12.5, "bold": True},
           {"t": "“A unified Lakehouse uniting engineering, warehousing, "
                 "science, AI & ML on one collaborative, Spark-powered platform.”",
            "color": NAVY, "size": 12.5, "italic": True}]], spacing=1.22)
    footer(s)
    notes(s,
          "Anchor on the precise definition — Databricks unifies the full data + AI lifecycle on open "
          "standards. History matters for credibility: the founders wrote Apache Spark, then open-sourced "
          "Delta Lake, MLflow and Unity Catalog, so Databricks is the commercial home of the modern data "
          "stack's core technologies. Stress 'open' and 'multi-cloud' — customers avoid lock-in and keep "
          "data in their own cloud account. The bottom band teaches precision: avoid the vague one-liner.")


def s_why_databricks(prs):
    s = slide(prs)
    header(s, "Introduction to Databricks", "Why Databricks? The Problem It Solves")
    # problem card
    card(s, MX, 2.05, 5.35, 4.4, fill=WHITE, line=LINE, shadow=True)
    band(s, MX, 2.05, 5.35, 0.7, RGBColor(0x9C, 0x2A, 0x1E))
    text(s, MX + 0.35, 2.05, 4.7, 0.7, "THE TRADITIONAL TWO-SYSTEM WORLD", size=12.5,
         color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    bullets(s, MX + 0.35, 2.95, 4.7, 3.4, [
        "Separate data lake AND data warehouse to maintain",
        "Constant, brittle copying of data between systems",
        "Duplicated storage, stale copies, drifting definitions",
        "Governance & security bolted on per system",
        "ML on the lake, BI on the warehouse — never together",
        "High cost, high complexity, slow time-to-insight",
    ], size=12.5, marker=LAVA_DK, gap=11.5)
    # arrow
    sp = shape(s, MSO_SHAPE.RIGHT_ARROW, 6.0, 3.95, 1.0, 0.7, fill=LAVA, line=None)
    try:
        sp.adjustments[0] = 0.5; sp.adjustments[1] = 0.6
    except Exception:
        pass
    # solution card
    card(s, 7.35, 2.05, 5.35, 4.4, fill=NAVY, line=None, shadow=True)
    band(s, 7.35, 2.05, 5.35, 0.7, GREEN_DK)
    text(s, 7.7, 2.05, 4.7, 0.7, "THE DATABRICKS LAKEHOUSE ANSWER", size=12.5,
         color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    bullets(s, 7.7, 2.95, 4.7, 3.4, [
        "One platform for ALL data, analytics & AI",
        "Open Delta Lake storage — single copy, no silos",
        "ACID reliability directly on cheap cloud storage",
        "Unity Catalog: one governance & security model",
        "BI, SQL, streaming & ML on the same data",
        "Lower cost, less complexity, faster insight",
    ], size=12.5, marker=GREEN, color=RGBColor(0xD6, 0xDE, 0xE1), gap=11.5)
    footer(s)
    notes(s,
          "This is the core sales/architecture narrative. For two decades enterprises ran two stacks: a "
          "data lake (cheap, flexible, but unreliable — good for data science) and a data warehouse "
          "(reliable, fast SQL, but rigid and expensive — good for BI). Teams endlessly copied data between "
          "them, creating cost, staleness, and governance gaps, and ML teams and BI teams never shared a "
          "source of truth. Databricks' answer is the Lakehouse: one open copy of data with warehouse "
          "reliability and lake flexibility, one governance model, serving every workload. Everything else "
          "in the platform follows from this single idea.")


def s_evolution(prs):
    s = slide(prs)
    header(s, "Introduction to Databricks", "The Databricks Evolution")
    events = [
        dict(year="2013", title="Founded", desc="Creators of Spark commercialize the engine", color=NAVY_2),
        dict(year="2015", title="Cloud Platform", desc="Managed Spark + collaborative notebooks", color=BLUE),
        dict(year="2019", title="Delta Lake", desc="ACID reliability on the lake, open-sourced", color=TEAL),
        dict(year="2020", title="Lakehouse", desc="Lake + warehouse unified into one paradigm", color=GREEN),
        dict(year="2021", title="Unity Catalog", desc="Unified governance & lineage across clouds", color=YELLOW),
        dict(year="2023", title="Generative AI", desc="MosaicML; LLMs on governed enterprise data", color=LAVA),
        dict(year="2024+", title="Data Intelligence", desc="Mosaic AI · Lakeflow · AI/BI Genie", color=PURPLE),
    ]
    timeline(s, events, y_center=4.1)
    text(s, MX, 6.5, CW, 0.4,
         "From a faster engine, to reliable storage, to a unified platform, to a Data Intelligence Platform for the AI era.",
         size=12, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "Databricks' product history mirrors the industry's: it began by commercializing Spark (speed), "
          "then added Delta Lake (reliability) and named the Lakehouse paradigm (unification), then Unity "
          "Catalog (governance), and most recently leaned into AI — acquiring MosaicML and building Mosaic AI "
          "so customers can build and serve LLMs on their own governed data. The current positioning is the "
          "'Data Intelligence Platform'. The throughline: each release removed a reason customers needed a "
          "second system.")


def s_lakehouse(prs):
    s = slide(prs)
    header(s, "Introduction to Databricks", "The Lakehouse — Best of Both Worlds")
    # warehouse + lake = lakehouse
    cards_def = [
        dict(x=MX, color=BLUE, icon="warehouse", title="Data Warehouse",
             pros=["Reliable & structured", "Fast SQL & BI", "ACID transactions"],
             cons=["Rigid schema", "Costly to scale", "No ML / unstructured"]),
        dict(x=4.85, color=TEAL, icon="lake", title="Data Lake",
             pros=["Cheap & scalable", "Any data type", "Great for ML / AI"],
             cons=["No reliability", "Becomes a 'swamp'", "Weak governance"]),
    ]
    cw = 3.85
    for cd in cards_def:
        x = cd["x"]
        card(s, x, 2.05, cw, 3.9, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.05, cw, 0.62, cd["color"])
        icon(s, cd["icon"], x + 0.55, 2.36, 0.42, WHITE)
        text(s, x + 0.95, 2.05, cw - 1.0, 0.62, cd["title"], size=14.5, color=WHITE,
             bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + 0.3, 2.82, cw - 0.6, 0.3, "STRENGTHS", size=9.5, color=GREEN_DK, bold=True, font=FONT_SB)
        bullets(s, x + 0.3, 3.12, cw - 0.55, 1.3, cd["pros"], size=11, marker=GREEN, gap=6)
        text(s, x + 0.3, 4.42, cw - 0.6, 0.3, "LIMITATIONS", size=9.5, color=LAVA, bold=True, font=FONT_SB)
        bullets(s, x + 0.3, 4.72, cw - 0.55, 1.3, cd["cons"], size=11, marker=LAVA, gap=6)
    # plus / equals
    text(s, 4.45, 3.55, 0.5, 0.8, "+", size=40, color=GRAY_LT, bold=True, align=PP_ALIGN.CENTER)
    text(s, 8.55, 3.55, 0.6, 0.8, "=", size=40, color=LAVA, bold=True, align=PP_ALIGN.CENTER)
    # lakehouse card
    x = 9.2
    cw2 = CW + MX - x
    card(s, x, 2.05, cw2, 3.9, fill=NAVY, line=None, shadow=True)
    band(s, x, 2.05, cw2, 0.62, LAVA)
    icon(s, "delta", x + 0.5, 2.36, 0.42, WHITE)
    text(s, x + 0.88, 2.05, cw2 - 0.95, 0.62, "Lakehouse", size=15, color=WHITE,
         bold=True, anchor=MSO_ANCHOR.MIDDLE)
    bullets(s, x + 0.3, 2.85, cw2 - 0.55, 3.0, [
        "One open platform for all data",
        "ACID reliability on cheap storage",
        "BI + SQL + streaming + ML together",
        "Unified governance & security",
        "No data duplication or silos",
        "Open formats — zero lock-in",
    ], size=11.3, marker=LAVA_LT, color=RGBColor(0xD6, 0xDE, 0xE1), gap=8.5)
    text(s, MX, 6.18, CW, 0.5,
         [[{"t": "Lakehouse  =  the reliability & performance of a warehouse  ", "color": GRAY_2, "size": 12.3, "italic": True},
           {"t": "+", "color": LAVA, "size": 13, "bold": True},
           {"t": "  the scale, openness & flexibility of a lake", "color": GRAY_2, "size": 12.3, "italic": True}]],
         align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "The Lakehouse is THE defining concept of the course — make sure everyone leaves understanding it. "
          "Warehouses are reliable but rigid and expensive; lakes are cheap and flexible but unreliable and "
          "ungoverned. Historically you had to choose, or run both. The Lakehouse adds a transactional "
          "metadata layer (Delta Lake) directly on top of cheap cloud object storage, giving you warehouse-"
          "grade ACID reliability and performance WITH lake-grade scale, openness and ML support — one copy "
          "of data, one governance model, every workload. This is what Delta Lake makes technically possible.")


def s_platform(prs):
    s = slide(prs)
    header(s, "Introduction to Databricks", "One Unified Platform, Every Persona")
    # personas row
    personas = [("Data Engineers", "bolt", LAVA), ("Data Analysts", "chart", BLUE),
                ("Data Scientists", "ml", GREEN), ("ML Engineers", "gear", PURPLE),
                ("Business / BI", "people", TEAL)]
    pw = (CW - 4 * 0.3) / 5
    for i, (name, ic, col) in enumerate(personas):
        x = MX + i * (pw + 0.3)
        card(s, x, 2.0, pw, 1.05, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x + pw / 2, 2.36, 0.56, ic, col, shadow=False)
        text(s, x + 0.06, 2.66, pw - 0.12, 0.35, name, size=10.8, color=NAVY,
             bold=True, align=PP_ALIGN.CENTER, spacing=0.95)
        # down arrow into platform
        a = shape(s, MSO_SHAPE.DOWN_ARROW, x + pw / 2 - 0.07, 3.12, 0.14, 0.22, fill=GRAY_LT, line=None)
    # platform band
    card(s, MX, 3.5, CW, 1.55, fill=NAVY, line=None, shadow=True)
    text(s, MX, 3.62, CW, 0.34, "DATABRICKS DATA INTELLIGENCE PLATFORM", size=12.5,
         color=LAVA_LT, bold=True, align=PP_ALIGN.CENTER, font=FONT_SB)
    caps = ["Delta Lake\nETL & Streaming", "Databricks SQL\nWarehousing & BI",
            "Mosaic AI\nML & GenAI", "Workflows\nOrchestration", "Unity Catalog\nGovernance"]
    capcols = [TEAL, BLUE, GREEN, YELLOW, PURPLE]
    cwp = (CW - 0.7 - 4 * 0.2) / 5
    for i, (cap, col) in enumerate(zip(caps, capcols)):
        x = MX + 0.35 + i * (cwp + 0.2)
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 4.06, cwp, 0.84, fill=NAVY_2, line=col, line_w=1.4, adj=0.14)
        title, sub = cap.split("\n")
        text(s, x + 0.05, 4.12, cwp - 0.1, 0.36, title, size=11, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, spacing=0.9)
        text(s, x + 0.05, 4.5, cwp - 0.1, 0.36, sub, size=8.8, color=RGBColor(0xB6, 0xC2, 0xC6),
             align=PP_ALIGN.CENTER, spacing=0.9)
    # open storage foundation
    card(s, MX, 5.25, CW, 1.0, fill=OAT_2, line=LINE, shadow=False)
    text(s, MX, 5.34, CW, 0.32, "OPEN DATA LAKE  ·  YOUR CLOUD STORAGE", size=11,
         color=GRAY, bold=True, align=PP_ALIGN.CENTER, font=FONT_SB)
    found = ["Amazon S3", "Azure ADLS", "Google Cloud Storage", "Open Delta / Parquet / Iceberg"]
    fw = (CW - 0.7 - 3 * 0.25) / 4
    for i, f in enumerate(found):
        x = MX + 0.35 + i * (fw + 0.25)
        chip(s, x, 5.72, fw, 0.42, f, WHITE, NAVY, size=10.5, radius=0.4, line=LINE)
    footer(s)
    notes(s,
          "The 'unified' claim made visual: every persona — engineers, analysts, scientists, ML engineers, "
          "and business users — works on ONE platform sitting on ONE open copy of data in the customer's "
          "cloud storage. Each capability (ETL/streaming, SQL warehousing, ML/GenAI, orchestration, "
          "governance) is a first-class part of the platform rather than a separate product to integrate. "
          "The foundation row reinforces openness: data lives in the customer's own object storage in open "
          "formats. This collapses the tool sprawl from the ecosystem slide into a single collaborative "
          "environment.")


def s_components(prs):
    s = slide(prs)
    header(s, "Introduction to Databricks", "Databricks Core Components")
    steps = [
        dict(title="Workspace", icon="people", color=BLUE, badge=1,
             desc="Collaborative notebooks, repos & dashboards for every team."),
        dict(title="Spark + Photon", icon="bolt", color=LAVA, badge=2,
             desc="Distributed engine with a vectorized C++ query accelerator."),
        dict(title="Delta Lake", icon="delta", color=TEAL, badge=3,
             desc="Open storage layer bringing ACID reliability to the lake."),
        dict(title="Mosaic AI", icon="ml", color=GREEN, badge=4,
             desc="MLflow & GenAI lifecycle — track, tune, serve & govern."),
        dict(title="Unity Catalog", icon="lock", color=PURPLE, badge=5,
             desc="One governance layer: access, lineage, discovery & sharing."),
    ]
    flow_steps(s, steps, y_top=2.3, card_h=2.5, icon_d=1.02, arrow=True)
    card(s, MX, 5.2, CW, 1.1, fill=OAT_2, line=LINE, shadow=False)
    text(s, MX + 0.4, 5.34, CW - 0.8, 0.85,
         [[{"t": "Together these form the Lakehouse:  ", "color": NAVY, "size": 12.5, "bold": True},
           {"t": "the Workspace is where people work, Spark + Photon is the engine, "
                 "Delta Lake is the reliable storage, Mosaic AI delivers intelligence, "
                 "and Unity Catalog governs it all — one secure, open, collaborative system.",
            "color": GRAY, "size": 12.5}]],
         anchor=MSO_ANCHOR.MIDDLE, spacing=1.25)
    footer(s)
    notes(s,
          "These five components map cleanly to the platform: Workspace (where humans collaborate), Spark + "
          "Photon (compute engine — Photon is Databricks' vectorized C++ rewrite of Spark's execution, much "
          "faster for SQL), Delta Lake (reliable open storage), Mosaic AI/MLflow (the ML & GenAI lifecycle — "
          "MLflow is the open experiment-tracking and model-registry standard), and Unity Catalog (unified "
          "governance). In Section 3 we'll open up Spark, Delta and Unity Catalog individually. For now, "
          "learners just need the mental model of what each piece does.")


def s_db_benefits(prs):
    s = slide(prs)
    header(s, "Introduction to Databricks", "Why Enterprises Choose Databricks")
    items = [
        dict(icon="hex", color=LAVA, title="Unified",
             desc="Engineering, analytics, ML & AI on one platform — no tool sprawl."),
        dict(icon="cube", color=BLUE, title="Open & Standard",
             desc="Delta, Spark, MLflow, Iceberg — open formats, zero vendor lock-in."),
        dict(icon="bolt", color=YELLOW, title="High Performance",
             desc="Photon engine & optimized runtime deliver record price/performance."),
        dict(icon="cluster", color=GREEN, title="Elastic Scale",
             desc="Serverless & autoscaling compute from gigabytes to petabytes."),
        dict(icon="people", color=TEAL, title="Collaborative",
             desc="Shared notebooks, Git integration and reproducible workflows."),
        dict(icon="lock", color=PURPLE, title="Governed & Secure",
             desc="Unity Catalog, fine-grained access, lineage and compliance built in."),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=14.5, desc_size=11)
    footer(s)
    notes(s,
          "Summarize the value proposition in six words leaders care about. Tie each back to a problem from "
          "the Challenges slide: Unified solves complexity/silos; Open solves lock-in; Performance and Elastic "
          "Scale solve cost and real-time needs; Collaborative solves the skills/velocity gap; Governed solves "
          "security & compliance. If asked about ROI, the headline is consolidation — replacing many "
          "point tools with one platform — plus faster time-to-insight and a single governed copy of data.")


# ---------- SECTION 3 : DATABRICKS ARCHITECTURE ----------
def s_arch_overview(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "Architecture Overview — Two Planes")
    # control plane band
    card(s, MX, 2.0, CW, 1.85, fill=NAVY, line=None, shadow=True)
    chip(s, MX + 0.3, 2.22, 2.7, 0.5, "CONTROL PLANE", LAVA, WHITE, size=12, radius=0.16)
    text(s, MX + 3.2, 2.22, CW - 3.5, 0.5, "Managed by Databricks  ·  no customer data at rest",
         size=11.5, color=RGBColor(0xB6, 0xC2, 0xC6), anchor=MSO_ANCHOR.MIDDLE, italic=True)
    cp = ["Web App & UI", "Notebooks & Repos", "Job Scheduler", "Cluster Manager", "Unity Catalog", "REST APIs"]
    cwp = (CW - 0.6 - 5 * 0.18) / 6
    for i, c in enumerate(cp):
        x = MX + 0.3 + i * (cwp + 0.18)
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 2.85, cwp, 0.78, fill=NAVY_2, line=LINE_DK, line_w=1, adj=0.12)
        text(s, x + 0.04, 2.85, cwp - 0.08, 0.78, c, size=10.2, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=0.92)
    # double arrow
    a = shape(s, MSO_SHAPE.LEFT_RIGHT_ARROW, 6.25, 4.0, 0.8, 0.34, fill=GRAY_LT, line=None)
    a.rotation = 90
    text(s, 7.1, 3.96, 5.5, 0.4, "secure, encrypted control channel", size=9.5, color=GRAY_LT, italic=True)
    # compute plane band
    card(s, MX, 4.55, CW, 1.95, fill=WHITE, line=LINE, shadow=True)
    chip(s, MX + 0.3, 4.77, 3.0, 0.5, "COMPUTE PLANE", GREEN_DK, WHITE, size=12, radius=0.16)
    text(s, MX + 3.5, 4.77, CW - 3.8, 0.5, "Runs in YOUR cloud account  ·  your data never leaves",
         size=11.5, color=GRAY_2, anchor=MSO_ANCHOR.MIDDLE, italic=True)
    dp = [("Clusters & Spark", LAVA), ("Photon Engine", YELLOW), ("Serverless Compute", GREEN),
          ("Delta Lake Tables", TEAL), ("Cloud Object Storage", BLUE)]
    cwp2 = (CW - 0.6 - 4 * 0.2) / 5
    for i, (c, col) in enumerate(dp):
        x = MX + 0.3 + i * (cwp2 + 0.2)
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 5.42, cwp2, 0.85, fill=OAT_2, line=col, line_w=1.5, adj=0.12)
        band(s, x, 5.42, 0.09, 0.85, col)
        text(s, x + 0.16, 5.42, cwp2 - 0.22, 0.85, c, size=10.5, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=0.95)
    footer(s)
    notes(s,
          "The single most important architecture concept: Databricks splits into a CONTROL PLANE and a "
          "COMPUTE PLANE (formerly called the data plane). The control plane is the managed backend Databricks "
          "operates — the web UI, notebooks, job scheduler, cluster manager and Unity Catalog metadata. "
          "Crucially it holds NO customer data at rest. The compute plane is where clusters spin up and data "
          "is processed; in the classic model it runs inside the CUSTOMER'S own cloud account, so your data "
          "and compute stay in your tenancy. This separation is why Databricks is enterprise-secure: "
          "Databricks manages the experience, you keep control of your data.")


def s_planes(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "Control Plane & Compute Plane in Detail")
    # control plane
    card(s, MX, 2.05, 5.9, 4.45, fill=WHITE, line=LINE, shadow=True)
    band(s, MX, 2.05, 5.9, 0.66, NAVY)
    text(s, MX + 0.35, 2.05, 5.2, 0.66, "CONTROL PLANE  ·  Databricks-Managed", size=12.5,
         color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    text(s, MX + 0.35, 2.86, 5.2, 0.3, "Hosts the experience & metadata", size=10.5, color=LAVA, bold=True, italic=True)
    bullets(s, MX + 0.35, 3.2, 5.2, 3.2, [
        "Web application, UI & collaborative notebooks",
        "Jobs scheduler & workflow orchestration",
        "Cluster lifecycle manager & autoscaling logic",
        "Unity Catalog metastore — permissions & lineage",
        "REST APIs, Git integration & connectors",
        "No customer data stored at rest",
    ], size=11.8, marker=LAVA, gap=10)
    # compute plane
    card(s, 6.8, 2.05, 5.9, 4.45, fill=WHITE, line=LINE, shadow=True)
    band(s, 6.8, 2.05, 5.9, 0.66, GREEN_DK)
    text(s, 7.15, 2.05, 5.2, 0.66, "COMPUTE PLANE  ·  Your Cloud Account", size=12.5,
         color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    text(s, 7.15, 2.86, 5.2, 0.3, "Where data is actually processed", size=10.5, color=GREEN_DK, bold=True, italic=True)
    bullets(s, 7.15, 3.2, 5.2, 3.2, [
        "Clusters of VMs running Apache Spark + Photon",
        "Reads & writes Delta tables in your object storage",
        ("Classic compute — in your own cloud VPC/VNet", 1),
        ("Serverless compute — instant, Databricks-hosted pool", 1),
        "Your data & credentials never leave your tenancy",
        "Encrypted, network-isolated, compliance-ready",
    ], size=11.8, marker=GREEN, gap=9)
    footer(s)
    notes(s,
          "Go one level deeper on the two planes. Control plane = the brains and the UI, run by Databricks, "
          "metadata-only. Compute plane = the muscle, where VMs run Spark and touch your data. Highlight the "
          "two compute models: CLASSIC compute provisions VMs inside the customer's own cloud account/VPC "
          "(maximum control & isolation), while SERVERLESS compute uses a pre-warmed pool managed by "
          "Databricks for instant startup (convenience & speed). In both cases governance and credentials "
          "are controlled by the customer. This answers the #1 enterprise security question: 'where does my "
          "data live?' — in your own cloud storage, always.")


def s_spark(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "Apache Spark — Distributed Execution")
    # driver
    card(s, MX, 2.15, 3.2, 2.0, fill=NAVY, line=None, shadow=True)
    icon_tile(s, MX + 0.55, 2.62, 0.66, "gear", LAVA, shadow=False)
    text(s, MX + 1.0, 2.32, 2.1, 0.5, "Driver", size=15, color=WHITE, bold=True)
    text(s, MX + 0.3, 3.0, 2.7, 1.0,
         "SparkContext · builds the DAG, plans & schedules tasks across the cluster.",
         size=10.5, color=RGBColor(0xC4, 0xD0, 0xD4), spacing=1.1)
    # cluster manager
    chip(s, MX + 0.2, 4.45, 2.8, 0.6, "Cluster Manager", TEAL, WHITE, size=12, radius=0.16)
    text(s, MX, 5.2, 3.3, 1.0, "Allocates worker resources & autoscales the cluster up or down.",
         size=10.5, color=GRAY_2, spacing=1.1)
    # arrows to executors
    for ty in (2.45, 3.55, 4.65):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(MX + 3.2), Inches(3.15),
                                    Inches(4.9), Inches(ty + 0.45))
        ln.line.color.rgb = GRAY_LT; ln.line.width = Pt(1.6)
    # executors
    exs = [("Executor 1", LAVA), ("Executor 2", BLUE), ("Executor 3", GREEN)]
    for i, (name, col) in enumerate(exs):
        y = 2.3 + i * 1.4
        card(s, 4.9, y, 4.4, 1.2, fill=WHITE, line=LINE, shadow=True)
        band(s, 4.9, y, 0.1, 1.2, col)
        text(s, 5.15, y + 0.12, 2.0, 0.4, name, size=12.5, color=NAVY, bold=True)
        text(s, 5.15, y + 0.5, 2.1, 0.6, "JVM · cache · tasks", size=9.5, color=GRAY_2)
        # task partitions
        for t in range(4):
            tx = 7.05 + t * 0.55
            sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, tx, y + 0.32, 0.45, 0.56, fill=OAT_2, line=col, line_w=1.2, adj=0.18)
            text(s, tx, y + 0.32, 0.45, 0.56, "P" + str(t + 1), size=9, color=col, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 7.05, 1.95, 2.3, 0.3, "Parallel tasks on partitions", size=9, color=GRAY_LT, italic=True)
    # photon callout
    card(s, 9.55, 2.3, 3.15, 3.7, fill=NAVY, line=None, shadow=True)
    icon_tile(s, 9.55 + 0.6, 2.85, 0.7, "bolt", YELLOW, shadow=False)
    text(s, 9.55 + 1.05, 2.55, 2.0, 0.55, "Photon", size=15, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.55 + 1.05, 3.05, 2.0, 0.3, "Vectorized engine", size=9.5, color=YELLOW, italic=True)
    bullets(s, 9.8, 3.55, 2.7, 2.3, [
        "Native C++ rewrite of Spark execution",
        "Vectorized, SIMD-optimized processing",
        "Drop-in — no code changes",
        "Up to 2-3x faster SQL & DataFrames",
        "Lower cost per query",
    ], size=10.3, marker=YELLOW, color=RGBColor(0xCC, 0xD6, 0xDA), gap=7)
    footer(s)
    notes(s,
          "Explain Spark's master/worker model. The DRIVER runs your program, holds the SparkContext, builds "
          "a DAG of the computation and breaks it into TASKS. The CLUSTER MANAGER allocates resources. "
          "EXECUTORS are JVM processes on worker nodes that actually run tasks in parallel, each task "
          "processing one PARTITION of the data — this parallelism is the whole point. Key teaching analogy: "
          "the driver is the head chef writing the plan; executors are line cooks each working a portion "
          "simultaneously. PHOTON is Databricks' native C++ vectorized engine that transparently accelerates "
          "Spark SQL/DataFrame workloads 2-3x with no code change. Mention lazy evaluation: nothing runs "
          "until an action triggers the DAG.")


def s_delta(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "Delta Lake — Reliability on the Lake")
    # left: how it works
    card(s, MX, 2.1, 6.2, 4.3, fill=WHITE, line=LINE, shadow=True)
    text(s, MX + 0.35, 2.3, 5.6, 0.34, "HOW IT WORKS", size=11, color=LAVA, bold=True, font=FONT_SB)
    # object storage layer
    band2 = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.35, 2.74, 5.5, 1.0, fill=OAT_2, line=LINE, adj=0.1)
    text(s, MX + 0.5, 2.82, 5.2, 0.3, "Cloud Object Storage", size=10.5, color=GRAY, bold=True)
    for i in range(5):
        px = MX + 0.55 + i * 1.04
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, px, 3.18, 0.92, 0.46, fill=BLUE, line=None, adj=0.16)
        text(s, px, 3.18, 0.92, 0.46, ".parquet", size=8.3, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # delta log layer
    log = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.35, 3.95, 5.5, 0.62, fill=NAVY, line=None, adj=0.14)
    text(s, MX + 0.5, 3.95, 5.2, 0.62,
         [[{"t": "_delta_log/", "color": LAVA_LT, "size": 11, "bold": True},
           {"t": "   transaction log  →  ACID, versions, schema", "color": WHITE, "size": 10.5}]],
         anchor=MSO_ANCHOR.MIDDLE)
    a = shape(s, MSO_SHAPE.UP_ARROW, MX + 3.0, 3.66, 0.3, 0.32, fill=LAVA, line=None)
    # delta table abstraction
    tbl = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.35, 4.78, 5.5, 0.62, fill=GREEN_DK, line=None, adj=0.14)
    text(s, MX + 0.5, 4.78, 5.2, 0.62, "=  One reliable, governed Delta TABLE", size=11.5,
         color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, MX + 0.35, 5.6, 5.6, 0.7,
         "Parquet data files + a JSON transaction log turn a folder of files into a database-grade table.",
         size=10.5, color=GRAY_2, italic=True, spacing=1.1)
    # right: features
    feats = [
        dict(icon="check", color=GREEN, title="ACID Transactions",
             desc="Reliable concurrent reads & writes — no corrupt, partial data."),
        dict(icon="down", color=BLUE, title="Time Travel",
             desc="Query or roll back to any previous version of the table."),
        dict(icon="shield", color=YELLOW, title="Schema Enforcement",
             desc="Rejects bad data; supports safe schema evolution."),
        dict(icon="bolt", color=LAVA, title="Batch + Streaming",
             desc="One table for both, with MERGE/upsert & OPTIMIZE / Z-ORDER."),
    ]
    x0 = 7.1
    gy = 0.22
    th = (4.3 - 3 * gy) / 4
    for i, it in enumerate(feats):
        y = 2.1 + i * (th + gy)
        card(s, x0, y, CW + MX - x0, th, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x0 + 0.5, y + th / 2, 0.6, it["icon"], it["color"], shadow=False)
        text(s, x0 + 0.95, y + 0.1, CW + MX - x0 - 1.1, 0.34, it["title"], size=12.5,
             color=NAVY, bold=True)
        text(s, x0 + 0.95, y + 0.43, CW + MX - x0 - 1.1, th - 0.5, it["desc"], size=10,
             color=GRAY_2, spacing=1.05)
    footer(s)
    notes(s,
          "Delta Lake is the technology that makes the Lakehouse possible — explain the mechanism. Underneath, "
          "a Delta table is just Parquet data files in cloud storage PLUS a transaction log (the _delta_log "
          "folder of ordered JSON commits). That log is the magic: it records every change atomically, giving "
          "you ACID transactions, time travel (version history & rollback), schema enforcement and evolution, "
          "and a single table that serves both batch and streaming. So you get database reliability directly "
          "on cheap object storage, in an OPEN format. Mention OPTIMIZE (compaction) and Z-ORDER (data "
          "skipping) as performance features. Without Delta, a lake is just files with no guarantees.")


def s_medallion(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "The Medallion Architecture")
    steps = [
        dict(title="Bronze", icon="database", color=BRONZE, badge=None,
             desc="RAW — ingest as-is from source. Full history, append-only, schema-light."),
        dict(title="Silver", icon="gear", color=SILVER, badge=None,
             desc="CLEANSED — validated, de-duplicated, conformed & joined. Queryable."),
        dict(title="Gold", icon="diamond", color=GOLD, badge=None,
             desc="CURATED — business-level aggregates & features for BI, ML & reporting."),
    ]
    # custom 3-step with big chevrons
    n = 3
    cw = (CW - 2 * 0.55) / 3
    labels_extra = ["Source of truth, replayable", "Single version of the cleaned data", "Ready for dashboards & models"]
    for i, st in enumerate(steps):
        x = MX + i * (cw + 0.55)
        card(s, x, 2.25, cw, 2.7, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.25, cw, 0.85, st["color"])
        icon(s, st["icon"], x + 0.6, 2.66, 0.46, WHITE)
        text(s, x + 1.05, 2.25, cw - 1.1, 0.85, st["title"], size=18, color=WHITE,
             bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + 0.3, 3.25, cw - 0.6, 1.2, st["desc"], size=11.5, color=GRAY, spacing=1.18)
        text(s, x + 0.3, 4.45, cw - 0.6, 0.4,
             [[{"t": "▸  ", "color": st["color"], "bold": True, "size": 11},
               {"t": labels_extra[i], "color": GRAY_2, "size": 10.5, "italic": True}]])
        if i < n - 1:
            arrow_h(s, x + cw + 0.08, 3.6, 0.4, LAVA, h=0.26)
    # quality gradient bar
    band(s, MX, 5.35, CW, 0.5, OAT_2)
    text(s, MX + 0.3, 5.35, 4, 0.5, "Data quality & business value", size=11, color=NAVY,
         bold=True, anchor=MSO_ANCHOR.MIDDLE)
    grad_bar = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 4.3, 5.46, 7.0, 0.28, fill=None, line=None, adj=0.5)
    grad(grad_bar, BRONZE, GOLD, angle=0)
    a = shape(s, MSO_SHAPE.RIGHT_ARROW, 11.35, 5.45, 0.7, 0.3, fill=GOLD, line=None)
    text(s, MX, 6.05, CW, 0.55,
         "A proven, incremental refinement pattern — raw data is progressively cleaned and enriched into trusted, analytics-ready tables.",
         size=12, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "The medallion (or multi-hop) architecture is the recommended data-design pattern on Databricks, "
          "and a very common interview topic. Data flows through three quality tiers: BRONZE is raw ingestion "
          "exactly as received (your replayable source of truth); SILVER is cleansed, de-duplicated, validated "
          "and conformed — the trustworthy, queryable layer where most joins happen; GOLD is curated, "
          "aggregated, business-level tables and ML features that power dashboards and models. Each hop "
          "increases quality and business value. Because every layer is a Delta table, the whole pipeline is "
          "reliable and can run incrementally with streaming. This pattern operationalizes everything in the "
          "course: it's the ecosystem pipeline, built on Delta, governed by Unity Catalog.")


def s_clusters(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "Cluster & Compute Architecture")
    # left: anatomy
    card(s, MX, 2.05, 6.0, 4.35, fill=WHITE, line=LINE, shadow=True)
    text(s, MX + 0.35, 2.24, 5.4, 0.3, "ANATOMY OF A CLUSTER", size=11, color=LAVA, bold=True, font=FONT_SB)
    # driver
    drv = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.35, 2.66, 5.3, 0.7, fill=NAVY, line=None, adj=0.12)
    text(s, MX + 0.5, 2.66, 5.0, 0.7, "Driver Node  ·  coordinates the cluster", size=12,
         color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    # workers (sized so 3 workers + autoscale ghost fit inside the card)
    ww, step, wx0 = 1.23, 1.355, MX + 0.35
    for i in range(3):
        wx = wx0 + i * step
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, wx, 3.55, ww, 0.75, fill=OAT_2, line=BLUE, line_w=1.5, adj=0.12)
        text(s, wx, 3.55, ww, 0.75, "Worker " + str(i + 1), size=10.5, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # autoscale ghost worker
    gx = wx0 + 3 * step
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, gx, 3.55, ww, 0.75, fill=None, line=GREEN, line_w=1.5, adj=0.12)
    text(s, gx, 3.55, ww, 0.75, "+ auto", size=10, color=GREEN_DK, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, MX + 0.35, 4.45, 5.4, 0.3,
         [[{"t": "Autoscaling ", "color": GREEN_DK, "bold": True, "size": 10.5},
           {"t": "adds/removes workers with load", "color": GRAY_2, "size": 10.5, "italic": True}]])
    band(s, MX + 0.35, 4.85, 5.3, 0.012, OAT_3)
    text(s, MX + 0.35, 4.98, 5.4, 0.3, "Databricks Runtime (DBR)", size=10.5, color=NAVY, bold=True)
    bullets(s, MX + 0.35, 5.3, 5.4, 1.1, [
        "Pre-tuned Spark + Photon + Delta + libraries",
        "ML runtime variant bundles PyTorch / TF / CUDA",
    ], size=10.3, marker=LAVA, gap=5)
    # right: cluster types
    types = [
        dict(icon="people", color=BLUE, title="All-Purpose",
             desc="Interactive, shared clusters for collaborative development in notebooks."),
        dict(icon="flow", color=LAVA, title="Job Clusters",
             desc="Ephemeral compute created for a job and torn down after — cost-efficient."),
        dict(icon="chart", color=PURPLE, title="SQL Warehouses",
             desc="Optimized Photon compute for BI & SQL analytics workloads."),
        dict(icon="cloud", color=GREEN, title="Serverless",
             desc="Instant, fully-managed pools — no infrastructure to configure."),
    ]
    x0 = 6.9
    gy = 0.2
    th = (4.35 - 3 * gy) / 4
    for i, it in enumerate(types):
        y = 2.05 + i * (th + gy)
        card(s, x0, y, CW + MX - x0, th, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x0 + 0.48, y + th / 2, 0.58, it["icon"], it["color"], shadow=False)
        text(s, x0 + 0.92, y + 0.08, CW + MX - x0 - 1.05, 0.32, it["title"], size=12, color=NAVY, bold=True)
        text(s, x0 + 0.92, y + 0.38, CW + MX - x0 - 1.05, th - 0.45, it["desc"], size=9.6,
             color=GRAY_2, spacing=1.02)
    footer(s)
    notes(s,
          "A cluster = one driver node + one or more worker nodes, all running the Databricks Runtime (DBR) — "
          "a pre-optimized bundle of Spark, Photon, Delta and common libraries (the ML runtime adds GPU/DL "
          "frameworks). AUTOSCALING adds and removes workers automatically with workload, controlling cost. "
          "Cover the four compute types and when to use each: All-Purpose for interactive dev (shared), Job "
          "clusters for scheduled production jobs (ephemeral, cheapest), SQL Warehouses for BI/SQL, and "
          "Serverless for instant startup with zero infra management. Cost tip: use job clusters for "
          "production and auto-termination on interactive clusters.")


def s_security(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "Security & Governance — Unity Catalog")
    # left: 3-level namespace
    card(s, MX, 2.05, 5.3, 4.4, fill=WHITE, line=LINE, shadow=True)
    text(s, MX + 0.35, 2.26, 4.6, 0.3, "ONE NAMESPACE, ALL ASSETS", size=11, color=LAVA, bold=True, font=FONT_SB)
    levels = [("Catalog", BLUE, "top-level container"), ("Schema", TEAL, "database / namespace"),
              ("Table / View / Volume / Model", GREEN, "the governed asset")]
    for i, (name, col, sub) in enumerate(levels):
        y = 2.7 + i * 0.82
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.35 + i * 0.35, y, 4.5 - i * 0.35, 0.66,
                   fill=col, line=None, adj=0.16)
        text(s, MX + 0.5 + i * 0.35, y, 4.2 - i * 0.35, 0.66,
             [[{"t": name, "color": WHITE, "size": 12, "bold": True},
               {"t": "   " + sub, "color": RGBColor(0xEA, 0xF2, 0xF0), "size": 9, "italic": True}]],
             anchor=MSO_ANCHOR.MIDDLE)
        if i < 2:
            shape(s, MSO_SHAPE.DOWN_ARROW, MX + 0.7 + i * 0.35, y + 0.66, 0.18, 0.16, fill=GRAY_LT, line=None)
    chip(s, MX + 0.35, 5.55, 4.6, 0.62, "catalog . schema . table", NAVY, LAVA_LT, size=13, radius=0.16)
    text(s, MX + 0.35, 6.2, 4.7, 0.3, "One consistent name & permission across all clouds & workspaces",
         size=9.3, color=GRAY_2, italic=True)
    # right: governance pillars
    items = [
        dict(icon="lock", color=LAVA, title="Fine-Grained Access",
             desc="Row/column-level security, ANSI SQL GRANTs, identity & SSO integration."),
        dict(icon="link", color=BLUE, title="Automated Lineage",
             desc="Column-level lineage and audit logs across notebooks, jobs & dashboards."),
        dict(icon="globe", color=GREEN, title="Discovery & Sharing",
             desc="Search, tags & Delta Sharing — open data sharing across organizations."),
        dict(icon="shield", color=PURPLE, title="Protection & Compliance",
             desc="Encryption, network isolation, GDPR / HIPAA / SOC 2 readiness."),
    ]
    grid_cards(s, items, cols=2, x=6.55, y=2.05, w=CW + MX - 6.55, h=4.4, gx=0.25, gy=0.25,
               icon_d=0.66, title_size=12.5, desc_size=10)
    footer(s)
    notes(s,
          "Unity Catalog is Databricks' unified governance layer — one place to secure and discover every "
          "data and AI asset across all workspaces and clouds. The three-level namespace "
          "catalog.schema.table replaces the old two-level hive metastore and gives every asset one "
          "consistent, governable name. Highlight the four pillars: fine-grained access control (down to "
          "rows and columns, via standard SQL GRANTs tied to your corporate identity/SSO); automatic "
          "column-level lineage and audit; discovery plus Delta Sharing (an open protocol to share live data "
          "across organizations without copying); and platform protections — encryption, network isolation, "
          "and compliance certifications. Governance is centralized and consistent, not bolted onto each tool.")


def s_dataflow(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "End-to-End Data Flow")
    # plane labels
    chip(s, MX, 1.95, 2.5, 0.4, "USERS & CONTROL", LAVA, WHITE, size=10, radius=0.3)
    chip(s, MX + 2.7, 1.95, 2.9, 0.4, "COMPUTE PLANE (your cloud)", GREEN_DK, WHITE, size=10, radius=0.3)
    chip(s, MX + 5.8, 1.95, 2.6, 0.4, "OPEN STORAGE", BLUE, WHITE, size=10, radius=0.3)
    chip(s, MX + 8.6, 1.95, 2.4, 0.4, "CONSUMPTION", PURPLE, WHITE, size=10, radius=0.3)
    stages = [
        dict(t="Users", sub="Engineers · Analysts\nScientists", icon="people", col=LAVA),
        dict(t="Workspace", sub="Notebooks · SQL\nJobs · Dashboards", icon="doc", col=NAVY_2),
        dict(t="Clusters", sub="Driver + Workers\nAutoscaling", icon="cluster", col=TEAL),
        dict(t="Spark + Photon", sub="Distributed\nprocessing engine", icon="bolt", col=YELLOW),
        dict(t="Delta Lake", sub="Bronze · Silver · Gold\nACID tables", icon="delta", col=GREEN),
        dict(t="Cloud Storage", sub="S3 · ADLS · GCS\nopen formats", icon="cloud", col=BLUE),
        dict(t="BI & AI", sub="Dashboards · ML\nPower BI · Tableau", icon="chart", col=PURPLE),
    ]
    n = len(stages)
    aw = 0.16
    cw = (CW - (n - 1) * aw) / n
    y = 2.6
    h = 2.55
    for i, st in enumerate(stages):
        x = MX + i * (cw + aw)
        card(s, x, y, cw, h, fill=WHITE, line=LINE, shadow=True)
        band(s, x, y, cw, 0.1, st["col"])
        icon_tile(s, x + cw / 2, y + 0.7, 0.8, st["icon"], st["col"], shadow=False)
        text(s, x + 0.04, y + 1.2, cw - 0.08, 0.55, st["t"], size=11.3, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER, spacing=0.9)
        text(s, x + 0.04, y + 1.72, cw - 0.08, 0.8, st["sub"], size=8.4, color=GRAY_2,
             align=PP_ALIGN.CENTER, spacing=1.0)
        number_badge(s, x + 0.26, y + 0.26, 0.34, i + 1, fill=st["col"], size=10)
        if i < n - 1:
            arrow_h(s, x + cw + 0.0, y + h / 2, aw, GRAY_LT, h=0.16)
    # governance underlay
    gov = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 5.35, CW, 0.72, fill=NAVY, line=None, adj=0.2)
    icon(s, "lock", MX + 0.5, 5.71, 0.36, LAVA_LT)
    text(s, MX + 0.95, 5.35, CW - 1.2, 0.72,
         [[{"t": "Unity Catalog", "color": LAVA_LT, "size": 12, "bold": True},
           {"t": "  governs every step — access control, lineage, audit & discovery across the entire flow",
            "color": WHITE, "size": 11.5}]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, MX, 6.2, CW, 0.4,
         "From a user's query to a governed dashboard — one platform, your data, end to end.",
         size=11.5, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "This is the capstone diagram — it ties the whole course together. Trace a request end to end: a "
          "USER works in the WORKSPACE (a notebook, SQL query or job); that triggers a CLUSTER in the compute "
          "plane; SPARK + PHOTON process the data in parallel; results are read/written as DELTA LAKE tables "
          "following the medallion pattern; those tables live in the customer's own CLOUD STORAGE in open "
          "formats; and finally the curated Gold data powers BI & AI consumption — dashboards, Power BI, "
          "Tableau, ML models. Underneath it all, UNITY CATALOG governs every step. Walk left-to-right slowly; "
          "this single slide is the architecture in one picture.")


def s_integration(prs):
    s = slide(prs)
    header(s, "Databricks Architecture", "Integration Architecture — An Open Hub")
    cx, cy = SW / 2, 4.35
    spokes = [
        dict(title="Cloud Storage", desc="S3 · ADLS · GCS", icon="cloud", color=BLUE, pos=(2.55, 2.85)),
        dict(title="Ingestion", desc="Kafka · Fivetran · Lakeflow", icon="down", color=TEAL, pos=(2.15, 4.35)),
        dict(title="Orchestration", desc="Airflow · Workflows · dbt", icon="flow", color=GREEN, pos=(2.55, 5.85)),
        dict(title="BI & Reporting", desc="Power BI · Tableau", icon="chart", color=PURPLE, pos=(10.75, 2.85)),
        dict(title="ML & AI", desc="MLflow · HuggingFace", icon="ml", color=LAVA, pos=(11.15, 4.35)),
        dict(title="Governance", desc="Purview · Collibra", icon="lock", color=YELLOW, pos=(10.75, 5.85)),
    ]
    hub_spoke(s, cx, cy, "Databricks\nLakehouse", spokes)
    # languages strip
    text(s, cx - 2.0, 3.35, 4.0, 0.3, "SQL · Python · Scala · R", size=10, color=GRAY_LT,
         align=PP_ALIGN.CENTER, italic=True)
    footer(s)
    notes(s,
          "Databricks is deliberately OPEN — it sits at the center of an enterprise's data ecosystem rather "
          "than replacing everything. Because data is stored in open formats in the customer's own cloud "
          "account, Databricks integrates with what teams already use: any cloud object store; ingestion "
          "tools like Kafka, Fivetran and the native Lakeflow Connect; orchestration via Airflow, dbt or "
          "native Workflows; BI tools like Power BI and Tableau over Databricks SQL; the ML ecosystem through "
          "MLflow and HuggingFace; and external governance catalogs. You can drive it in SQL, Python, Scala "
          "or R. The message for architects: adopt incrementally, no rip-and-replace, no lock-in.")


def s_summary(prs):
    s = slide(prs)
    header(s, "Wrap-Up", "Key Takeaways")
    cols = [
        dict(no="01", color=BLUE, title="Big Data Fundamentals", points=[
            "Scale OUT, not up — distributed compute",
            "The 5 V's define the problem space",
            "Sources → ... → Visualization pipeline"]),
        dict(no="02", color=LAVA, title="Databricks", points=[
            "Unified Lakehouse for data + AI",
            "Warehouse reliability + lake openness",
            "Spark, Delta, MLflow, Unity Catalog"]),
        dict(no="03", color=GREEN, title="Architecture", points=[
            "Control plane vs. your compute plane",
            "Delta + Medallion = trusted data",
            "Unity Catalog governs end to end"]),
    ]
    cw = (CW - 2 * 0.35) / 3
    for i, c in enumerate(cols):
        x = MX + i * (cw + 0.35)
        card(s, x, 2.0, cw, 2.8, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.0, cw, 0.12, c["color"])
        number_badge(s, x + 0.55, 2.6, 0.66, c["no"][-1], fill=c["color"], size=18)
        text(s, x + 1.05, 2.3, cw - 1.2, 0.6, c["title"], size=13.5, color=NAVY, bold=True,
             anchor=MSO_ANCHOR.MIDDLE, spacing=0.95)
        bullets(s, x + 0.32, 3.18, cw - 0.6, 1.5, c["points"], size=11.3, marker=c["color"], gap=9)
    # final takeaway banners
    hw = (CW - 0.3) / 2
    takeaway(s, MX, 4.98, hw, "The Lakehouse unifies all data, analytics & AI on one open, governed platform.",
             color=LAVA, icon_kind="star")
    takeaway(s, MX + hw + 0.3, 4.98, hw,
             "Your data stays in your cloud — Databricks manages the experience, you keep control.",
             color=GREEN, icon_kind="check")
    takeaway(s, MX, 5.88, hw, "Delta Lake + the medallion pattern turn raw files into trusted tables.",
             color=BLUE, icon_kind="delta")
    takeaway(s, MX + hw + 0.3, 5.88, hw,
             "One governance model (Unity Catalog) secures every asset, every step.",
             color=PURPLE, icon_kind="lock")
    footer(s)
    notes(s,
          "Recap the three sections and land the four big takeaways. Check understanding by asking the room "
          "to explain, in their own words: (1) why we scale out instead of up, (2) what the Lakehouse unifies "
          "and why, (3) the difference between the control and compute planes, and (4) what the medallion "
          "layers are. If they can answer those four, the session succeeded. Transition to the knowledge-check "
          "and Q&A.")


def s_knowledge(prs):
    s = slide(prs)
    header(s, "Reinforce & Assess", "Knowledge Check & Interview Questions")
    # knowledge check
    card(s, MX, 2.05, 6.0, 4.45, fill=WHITE, line=LINE, shadow=True)
    band(s, MX, 2.05, 6.0, 0.6, BLUE)
    icon(s, "check", MX + 0.45, 2.35, 0.36, WHITE)
    text(s, MX + 0.85, 2.05, 5.0, 0.6, "KNOWLEDGE CHECK", size=13, color=WHITE, bold=True,
         anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    qs = [
        "Name the 5 V's of Big Data — which two decide success?",
        "Scale UP vs scale OUT — which is Big Data, and why?",
        "What does Delta Lake add on top of Parquet files?",
        "Control plane vs compute plane — where does your data live?",
        "List the three medallion layers in order.",
    ]
    bullets(s, MX + 0.35, 2.85, 5.4, 3.5, [(f"Q{i+1}.  {q}", 0) for i, q in enumerate(qs)],
            size=11.8, marker=BLUE, gap=12)
    # interview questions
    card(s, 6.95, 2.05, CW + MX - 6.95, 4.45, fill=NAVY, line=None, shadow=True)
    band(s, 6.95, 2.05, CW + MX - 6.95, 0.6, LAVA)
    icon(s, "star", 6.95 + 0.45, 2.35, 0.36, WHITE)
    text(s, 6.95 + 0.85, 2.05, 4.5, 0.6, "COMMON INTERVIEW QUESTIONS", size=13, color=WHITE,
         bold=True, anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    iq = [
        "Explain the Lakehouse — how does it differ from a warehouse and a lake?",
        "How does Spark execute a job? (driver, executors, partitions)",
        "What problems does Unity Catalog solve?",
        "Describe ACID & time travel in Delta Lake.",
        "When would you use job vs all-purpose vs serverless clusters?",
    ]
    bullets(s, 6.95 + 0.35, 2.85, CW + MX - 6.95 - 0.7, 3.5, [(q, 0) for q in iq],
            size=11.5, marker=LAVA_LT, color=RGBColor(0xD6, 0xDE, 0xE1), gap=11)
    footer(s)
    notes(s,
          "Use the left column as a live quiz — ask the room and let them answer aloud. Model answers: "
          "(1) Volume/Velocity/Variety/Veracity/Value; Veracity & Value decide success. (2) Big Data scales "
          "OUT (more commodity nodes) because single machines hit a ceiling. (3) Delta adds a transaction "
          "log giving ACID, time travel, schema enforcement, and batch+streaming. (4) Two planes; your data "
          "stays in YOUR cloud storage / compute plane. (5) Bronze → Silver → Gold. The right column lists "
          "real interview questions so learners can self-study — full answers are throughout the deck's notes.")


def s_thanks(prs):
    s = slide(prs, bg=NAVY)
    dark_bg(s)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 2.2, 0.09, 1.5, fill=LAVA, line=None, adj=0.5)
    text(s, MX + 0.3, 2.1, 10, 1.1, "Thank You", size=54, color=WHITE, bold=True)
    text(s, MX + 0.32, 3.3, 10.5, 0.6,
         "You now have the full picture — from Big Data fundamentals to the Databricks Lakehouse architecture.",
         size=15, color=RGBColor(0xC4, 0xD0, 0xD4), spacing=1.2)
    # next steps chips
    text(s, MX + 0.32, 4.25, 8, 0.3, "KEEP LEARNING", size=11.5, color=LAVA_LT, bold=True, font=FONT_SB)
    res = ["docs.databricks.com", "Databricks Academy", "Free Community Edition", "Delta Lake & Spark docs"]
    cx = MX + 0.32
    for r in res:
        w = 0.32 + len(r) * 0.105
        chip(s, cx, 4.62, w, 0.52, r, NAVY_2, WHITE, size=11, radius=0.5, line=LINE_DK)
        cx += w + 0.22
    # recap mini icons
    recap = [("Big Data", "database", BLUE), ("Lakehouse", "delta", LAVA),
             ("Spark", "bolt", YELLOW), ("Delta", "check", GREEN),
             ("Medallion", "diamond", GOLD), ("Unity Catalog", "lock", PURPLE)]
    cx = MX + 0.32
    for name, ic, col in recap:
        icon_tile(s, cx + 0.4, 5.85, 0.78, ic, col, shadow=True)
        text(s, cx - 0.1, 6.34, 1.0, 0.4, name, size=9.5, color=RGBColor(0xC4, 0xD0, 0xD4),
             align=PP_ALIGN.CENTER, spacing=0.9)
        cx += 1.15
    text(s, 8.7, 6.55, CW + MX - 8.7, 0.3, "Questions & discussion welcome",
         size=12, color=GRAY_LT, italic=True, align=PP_ALIGN.RIGHT)
    notes(s,
          "Close by congratulating the audience and recapping the six pillars shown as icons. Point to the "
          "self-study resources — the official docs, Databricks Academy (free role-based learning paths and "
          "certifications), and the free Community Edition / Express tier where they can practice hands-on. "
          "Invite questions and offer to go deeper on any architecture topic. If this is part of a series, "
          "preview the next session (e.g., hands-on notebooks, Delta Live Tables / Lakeflow, or Mosaic AI).")


# ===========================================================================
#  ASSEMBLE
# ===========================================================================
def main():
    prs = new_deck()
    s_cover(prs)
    s_agenda(prs)
    # Section 1
    s_divider(prs, "01", "Section One", "Big Data Fundamentals",
              ["Why Big Data matters & the 5 V's", "Traditional vs Big Data & key challenges",
               "Technologies, ecosystem & real-world use cases"], "database", color=LAVA)
    s_what_bigdata(prs)
    s_history(prs)
    s_5vs(prs)
    s_trad_vs_big(prs)
    s_challenges(prs)
    s_technologies(prs)
    s_ecosystem(prs)
    s_usecases(prs)
    # Section 2
    s_divider(prs, "02", "Section Two", "Introduction to Databricks",
              ["What & why Databricks · the evolution", "The Lakehouse concept & unified platform",
               "Core components & enterprise benefits"], "bolt", color=LAVA)
    s_what_databricks(prs)
    s_why_databricks(prs)
    s_evolution(prs)
    s_lakehouse(prs)
    s_platform(prs)
    s_components(prs)
    s_db_benefits(prs)
    # Section 3
    s_divider(prs, "03", "Section Three", "Databricks Architecture",
              ["Control & compute planes · Spark internals", "Delta Lake, medallion & cluster architecture",
               "Security, end-to-end data flow & integration"], "cluster", color=LAVA)
    s_arch_overview(prs)
    s_planes(prs)
    s_spark(prs)
    s_delta(prs)
    s_medallion(prs)
    s_clusters(prs)
    s_security(prs)
    s_dataflow(prs)
    s_integration(prs)
    # Wrap up
    s_summary(prs)
    s_knowledge(prs)
    s_thanks(prs)

    out = "Big-Data-and-Databricks-Training.pptx"
    prs.save(out)
    print(f"Saved {out} with {len(prs.slides._sldIdLst)} slides")


if __name__ == "__main__":
    main()

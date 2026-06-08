# Big Data & Databricks — From Fundamentals to the Lakehouse

A polished, **32-slide, training-ready presentation** covering Big Data
fundamentals, an introduction to Databricks, and Databricks architecture —
built for corporate training, client demonstrations, technical workshops and
executive reviews.

The deck is generated programmatically with [`python-pptx`](https://python-pptx.readthedocs.io)
and rendered entirely from **native PowerPoint vector shapes** (no external
images, no emoji), so it looks identical in Microsoft PowerPoint, Google
Slides, Keynote and LibreOffice, and every element stays fully editable.

---

## 📦 Deliverables

| File | What it is |
|------|------------|
| **`Big-Data-and-Databricks-Training.pptx`** | The presentation — 32 slides, 16:9, with detailed speaker notes on every slide. |
| **`Big-Data-and-Databricks-Training.pdf`** | A flat PDF preview for quick viewing without PowerPoint. |
| **`SLIDE-SPECIFICATIONS.md`** | Per-slide design document & facilitator guide (Objective · Content · Visual · Diagram · Speaker Notes · Design Tips). |
| `build_deck.py` | The deck generator (slide content & layout). |
| `deck_kit.py` | The reusable design system (palette, typography, shapes, vector icons). |
| `make_specs.py` | Generates `SLIDE-SPECIFICATIONS.md`, pulling speaker notes from the deck. |
| `render.sh` | Renders the `.pptx` → `.pdf` → per-slide PNGs for visual QA. |

---

## 🗂️ Contents

**Section 1 · Big Data Fundamentals**
1. Title / Cover
2. Your Learning Journey (Agenda)
3. *Section 01 Divider*
4. What Is Big Data?
5. The Evolution of Big Data *(timeline)*
6. The 5 V's of Big Data *(carousel)*
7. Traditional Data vs. Big Data *(comparison table)*
8. Big Data Challenges
9. The Big Data Technology Landscape
10. The Big Data Ecosystem — End to End *(pipeline)*
11. Big Data in the Real World *(use cases)*

**Section 2 · Introduction to Databricks**
12. *Section 02 Divider*
13. What Is Databricks?
14. Why Databricks? The Problem It Solves
15. The Databricks Evolution *(timeline)*
16. The Lakehouse — Best of Both Worlds
17. One Unified Platform, Every Persona
18. Databricks Core Components *(carousel)*
19. Why Enterprises Choose Databricks

**Section 3 · Databricks Architecture**
20. *Section 03 Divider*
21. Architecture Overview — Two Planes
22. Control Plane & Compute Plane in Detail
23. Apache Spark — Distributed Execution
24. Delta Lake — Reliability on the Lake
25. The Medallion Architecture *(Bronze → Silver → Gold)*
26. Cluster & Compute Architecture
27. Security & Governance — Unity Catalog
28. End-to-End Data Flow *(capstone diagram)*
29. Integration Architecture — An Open Hub

**Wrap-up**
30. Key Takeaways
31. Knowledge Check & Interview Questions
32. Thank You / Closing

---

## 🎨 Design system

- **Palette:** Databricks-inspired — *Lava* `#FF3621`, *Navy 800* `#1B3139`,
  *Oat* `#F9F7F4`, plus a supporting set (blue, green, teal, yellow, purple)
  and medal tones for the medallion architecture.
- **Typography:** Segoe UI family (broadly available on Office installs; falls
  back gracefully elsewhere).
- **Icons:** drawn as native PowerPoint auto-shapes (cylinders, lightning,
  gears, clouds, a neural-graph mark, lock, chain, globe, etc.) inside colored
  tiles — crisp at any zoom, consistent across apps.
- **System:** a kicker + lava-bar header, consistent footer with page numbers,
  card/shadow language, carousels, pipelines, timelines, comparison tables and
  a hub-and-spoke — all from reusable helpers in `deck_kit.py`.

---

## 🔧 Regenerating / customizing the deck

**Requirements**

```bash
pip install python-pptx        # build the .pptx
pip install pymupdf pillow     # only needed for render.sh QA previews
```

**Build the presentation**

```bash
python3 build_deck.py          # → Big-Data-and-Databricks-Training.pptx
python3 make_specs.py          # → SLIDE-SPECIFICATIONS.md
```

**Render previews (optional, needs LibreOffice + poppler/pymupdf)**

```bash
./render.sh                    # → build/slide_##.png  +  build/*.pdf
```

**Customize**

- Edit content in `build_deck.py` — each slide is a small, self-contained
  `s_*` function; repeated layouts use the `flow_steps`, `grid_cards`,
  `pipeline`, `timeline`, `vs_table` and `hub_spoke` composites.
- Re-brand by editing the color constants and `FONT` in `deck_kit.py`.
- Add an icon by extending the `icon()` dispatcher in `deck_kit.py`.

> 💡 Every slide already includes presenter-ready **speaker notes** (visible in
> PowerPoint's notes pane). The same notes are mirrored in
> `SLIDE-SPECIFICATIONS.md`.

---

## 👥 Audience & use

Designed for a mixed technical audience — Data Engineers, Data Analysts, Data
Scientists, ML Engineers, Cloud Architects and technical leaders — and adjusts
depth as it goes: conceptual framing up front, architecture deep-dives in
Section 3, and a knowledge-check + interview-prep slide to reinforce learning.

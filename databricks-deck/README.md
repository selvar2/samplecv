# Databricks Enterprise Training Series

Polished, **training-ready presentation decks** for Databricks enablement —
built for corporate training, client demonstrations, technical workshops and
executive reviews.

Each deck is generated programmatically with
[`python-pptx`](https://python-pptx.readthedocs.io) and rendered entirely from
**native PowerPoint vector shapes** (no external images, no emoji), so it looks
identical in Microsoft PowerPoint, Google Slides, Keynote and LibreOffice, and
every element stays fully editable. Both days share one design system
(`deck_kit.py`), so they look and feel like one series.

| Day | Deck | Slides | Topics |
|-----|------|:------:|--------|
| **Day 1** | `Big-Data-and-Databricks-Training.pptx` | 32 | Big Data Fundamentals · Introduction to Databricks · Databricks Architecture |
| **Day 2** | `Databricks-Day2-Spark-Workspace-Lakehouse.pptx` | 34 | Apache Spark Fundamentals · Workspace Components · Lakehouse Architecture |

---

## 📦 Deliverables

| File | What it is |
|------|------------|
| **`Big-Data-and-Databricks-Training.pptx`** | Day 1 deck — 32 slides, 16:9, speaker notes on every slide. |
| **`Big-Data-and-Databricks-Training.pdf`** | Day 1 flat PDF preview. |
| **`SLIDE-SPECIFICATIONS.md`** | Day 1 per-slide design doc & facilitator guide. |
| **`Databricks-Day2-Spark-Workspace-Lakehouse.pptx`** | Day 2 deck — 34 slides, 16:9, speaker notes on every slide. |
| **`Databricks-Day2-Spark-Workspace-Lakehouse.pdf`** | Day 2 flat PDF preview. |
| **`SLIDE-SPECIFICATIONS-Day2.md`** | Day 2 per-slide design doc & facilitator guide. |
| `deck_kit.py` | Shared design system — palette, typography, shapes, vector icons, page furniture and layout composites. |
| `build_deck.py` | Day 1 generator (also defines composites reused by Day 2). |
| `build_deck_day2.py` | Day 2 generator (imports the shared kit + composites). |
| `make_specs.py` / `make_specs_day2.py` | Generate the spec docs, pulling speaker notes from each deck. |
| `render.sh` | Renders a `.pptx` → `.pdf` → per-slide PNGs for visual QA. |

---

## 🗂️ Day 2 contents

**Part 1 · Apache Spark Fundamentals**
1. Title / Cover  2. Day 2 Roadmap  3. *Part 01 Divider*
4. What Is Apache Spark?  5. Why Spark Won  6. Spark Architecture *(Driver→…→Tasks)*
7. Component Stack *(SQL · DataFrames · Streaming · MLlib · GraphX)*
8. Execution Flow *(Query→DAG→Stages→Tasks→Results)*  9. Spark vs. Hadoop *(table)*
10. Use Cases  11. Best Practices & Takeaways

**Part 2 · Databricks Workspace Components**
12. *Part 02 Divider*  13. The Workspace  14. Workspace Architecture *(layered)*
15. Seven Building Blocks  16. Notebook Lifecycle  17. Cluster Types *(table)*
18. Repos & Git Integration *(workflow)*  19. Unity Catalog  20. Best Practices & Takeaways

**Part 3 · Databricks Lakehouse Architecture**
21. *Part 03 Divider*  22. Evolution of Data Platforms  23. What Is the Lakehouse?
24. Lakehouse Architecture *(layered pipeline)*  25. Medallion *(detailed)*
26. Delta Lake Fundamentals  27. Delta Transaction Flow *(diagram)*  28. Governance & Sharing
29. AI & ML on the Lakehouse  30. End-to-End Data Pipeline *(capstone)*
31. Benefits  32. Real-World Example  33. Key Takeaways  34. Thank You

> Day 2 includes all nine required diagrams: Spark architecture, Spark execution,
> Workspace architecture, Notebook lifecycle, Git workflow, Lakehouse architecture,
> Medallion, Delta transaction flow, and the end-to-end pipeline.

**Day 1 contents** are documented in `SLIDE-SPECIFICATIONS.md` (Big Data → 5 V's →
ecosystem → Databricks → Lakehouse → control/compute planes → Spark → Delta →
medallion → Unity Catalog → end-to-end flow).

---

## 🎨 Design system

- **Palette:** Databricks-inspired — *Lava* `#FF3621`, *Navy 800* `#1B3139`,
  *Oat* `#F9F7F4`, plus a supporting set and medal tones for the medallion.
- **Typography:** Segoe UI family (broadly available; falls back gracefully).
- **Icons:** native PowerPoint auto-shapes (cylinders, lightning, gears, clouds,
  a neural-graph mark, lock, chain, globe, etc.) inside colored tiles — crisp at
  any zoom and consistent across apps.
- **Composites:** carousels (`flow_steps`), card grids (`grid_cards`), labelled
  pipelines (`pipeline`), timelines (`timeline`), comparison tables (`vs_table`),
  hub-and-spoke (`hub_spoke`), section dividers and a kicker/lava-bar header with
  a consistent footer + page numbers. Day 2 reuses all of these for a matching look.

---

## 🔧 Regenerating / customizing

**Requirements**

```bash
pip install python-pptx        # build the .pptx decks
pip install pymupdf pillow     # only needed for render.sh QA previews
```

**Build**

```bash
python3 build_deck.py          # → Big-Data-and-Databricks-Training.pptx
python3 build_deck_day2.py     # → Databricks-Day2-Spark-Workspace-Lakehouse.pptx
python3 make_specs.py          # → SLIDE-SPECIFICATIONS.md
python3 make_specs_day2.py     # → SLIDE-SPECIFICATIONS-Day2.md
```

**Render previews (optional, needs LibreOffice + pymupdf)**

```bash
./render.sh Databricks-Day2-Spark-Workspace-Lakehouse.pptx   # → build/slide_##.png
```

**Customize**

- Edit content in `build_deck*.py` — each slide is a small, self-contained
  function; repeated layouts use the shared composites.
- Re-brand by editing the color constants and `FONT` in `deck_kit.py`.
- Add an icon by extending the `icon()` dispatcher in `deck_kit.py`.

> 💡 Every slide includes presenter-ready **speaker notes** (visible in
> PowerPoint's notes pane), mirrored in the `SLIDE-SPECIFICATIONS*.md` guides.

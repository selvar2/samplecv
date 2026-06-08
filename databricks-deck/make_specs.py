#!/usr/bin/env python3
"""
make_specs.py
-------------
Generates SLIDE-SPECIFICATIONS.md — a per-slide design document and
facilitator guide in the requested OUTPUT FORMAT. Speaker notes are read
straight from the built .pptx so the document can never drift from the deck.
"""
from pptx import Presentation

PPTX = "Big-Data-and-Databricks-Training.pptx"
OUT = "SLIDE-SPECIFICATIONS.md"

# Per-slide design metadata (speaker notes come from the deck itself).
# Order matches the slides produced by build_deck.py.
SPECS = [
    dict(title="Title / Cover",
         objective="Set the stage and frame the three-part learning arc.",
         content="Course title, subtitle, the three section chips, target audience and platform tagline.",
         visual="Dark navy gradient cover with a lava accent bar, oversized title, decorative rings/hexagon and section chips.",
         diagram="—",
         design="Databricks navy (#1B3139) + lava (#FF3621). Title in bold; subtitle in lava."),
    dict(title="Your Learning Journey (Agenda)",
         objective="Preview the 12 concepts grouped into three sections and the outcome of each.",
         content="Three section cards, each with four sub-topics and a learning outcome.",
         visual="Three equal cards with colored top bars, icon badges, bulleted topics and an OUTCOME line.",
         diagram="Three-column roadmap (Section 01 / 02 / 03).",
         design="Color-code sections: blue, lava, green. Keep bullets to four per card."),
    dict(title="Section 01 Divider — Big Data Fundamentals",
         objective="Transition into Section 1 and preview its scope.",
         content="Section number, title and three covered themes.",
         visual="Full-bleed navy with a giant '01' watermark, lava underline and a large database icon.",
         diagram="—",
         design="Oversized ghost number in navy-2; lava kicker and underline."),
    dict(title="What Is Big Data?",
         objective="Define Big Data precisely and make its scale tangible.",
         content="Definition card, three clarifying bullets and four headline statistics.",
         visual="Navy definition card on the left; 2x2 stat tiles with colored accent bars on the right.",
         diagram="—",
         design="Lead with a strong definition; let the big numbers carry the right side."),
    dict(title="The Evolution of Big Data",
         objective="Show how each era broke the previous bottleneck — scale, speed, unification, intelligence.",
         content="Seven milestones from 1990s RDBMS to 2023+ Data + AI.",
         visual="Horizontal timeline with alternating above/below captions and colored nodes.",
         diagram="Timeline: RDBMS → MapReduce → Hadoop → NoSQL/Cloud → Spark → Lakehouse → Data + AI.",
         design="Color-grade nodes warm→cool to imply progress; keep captions short."),
    dict(title="The 5 V's of Big Data",
         objective="Teach the canonical definition and which V's decide success.",
         content="Volume, Velocity, Variety, Veracity, Value with a one-line definition and an enterprise example strip.",
         visual="Five-step icon carousel with numbered badges, connectors and an 'Enterprise lens' band.",
         diagram="Carousel: Volume → Velocity → Variety → Veracity → Value.",
         design="One color per V; reinforce that Veracity & Value determine ROI."),
    dict(title="Traditional Data vs. Big Data",
         objective="Contrast the two paradigms to justify why new tooling is needed.",
         content="Seven-row comparison across volume, types, schema, processing, scaling, architecture and cost.",
         visual="Three-column comparison table with header chips and zebra striping.",
         diagram="Comparison table (Aspect | Traditional | Big Data).",
         design="Emphasise the Scaling row — scale up vs scale out is the crux."),
    dict(title="Big Data Challenges",
         objective="Frame the problems any platform must solve (and that Databricks will).",
         content="Six challenges: storage/scale, quality, integration, real-time, skills, governance.",
         visual="2x3 card grid with colored accent bars and icons.",
         diagram="—",
         design="Foreshadow solutions: quality→Delta, governance→Unity Catalog."),
    dict(title="The Big Data Technology Landscape",
         objective="Map the ecosystem by function, not vendor, to expose tool sprawl.",
         content="Six functional layers with representative tools.",
         visual="2x3 card grid (Ingestion, Storage, Processing, Orchestration, Query, ML/AI).",
         diagram="—",
         design="Sets up the Databricks consolidation story on later slides."),
    dict(title="The Big Data Ecosystem — End to End",
         objective="Establish the reference pipeline that the Lakehouse implements.",
         content="Six stages, each with example technologies.",
         visual="Horizontal pipeline of colored stage headers over example cards, joined by arrows.",
         diagram="Sources → Ingestion → Storage → Processing → Analytics → BI & Viz.",
         design="Left-to-right value gain; tie the closing line to 'one unified platform'."),
    dict(title="Big Data in the Real World",
         objective="Make Big Data concrete with industry use cases.",
         content="Six verticals with a flagship use case each.",
         visual="2x3 card grid with industry icons.",
         diagram="—",
         design="Go deep on the two verticals closest to the audience."),
    dict(title="Section 02 Divider — Introduction to Databricks",
         objective="Transition into Section 2.",
         content="Section number, title and three covered themes.",
         visual="Navy divider with a giant '02' watermark and a lightning icon.",
         diagram="—",
         design="Consistent divider system across all three sections."),
    dict(title="What Is Databricks?",
         objective="Give a precise, credible definition and key facts.",
         content="Definition card, four fact cards and a 'vague vs precise' contrast band.",
         visual="Navy definition card; a vertical stack of four fact cards; an oat contrast band.",
         diagram="—",
         design="Model precision — contrast the weak one-liner with the strong definition."),
    dict(title="Why Databricks? The Problem It Solves",
         objective="Explain the two-system pain and the Lakehouse answer.",
         content="Problem list (lake + warehouse silos) vs solution list (one open platform).",
         visual="Problem card and solution card separated by a large lava arrow.",
         diagram="Problem → (arrow) → Solution.",
         design="Red-toned problem header; green-toned solution header for instant read."),
    dict(title="The Databricks Evolution",
         objective="Show the product arc from engine to Data Intelligence Platform.",
         content="Seven milestones from 2013 founding to 2024+ Mosaic AI / Lakeflow.",
         visual="Horizontal timeline matching the Section-1 evolution slide.",
         diagram="Spark → Cloud → Delta → Lakehouse → Unity Catalog → GenAI → Data Intelligence.",
         design="Reuse the timeline style for visual consistency."),
    dict(title="The Lakehouse — Best of Both Worlds",
         objective="Cement the defining concept: warehouse + lake = Lakehouse.",
         content="Warehouse strengths/limits, lake strengths/limits, and the unified Lakehouse.",
         visual="Two comparison cards + (=) a navy Lakehouse card, with a closing equation line.",
         diagram="Data Warehouse  +  Data Lake  =  Lakehouse.",
         design="Use +/= operators as large connectors; green=strengths, lava=limitations."),
    dict(title="One Unified Platform, Every Persona",
         objective="Show one platform on one open copy of data serving all personas.",
         content="Five personas → platform capabilities → open storage foundation.",
         visual="Persona row, arrows down into a navy platform band, capability tiles, storage chips.",
         diagram="Personas ↓ Platform (Delta/SQL/AI/Workflows/Unity) ↓ Open cloud storage.",
         design="Three stacked layers (people / platform / storage) communicate 'unified'."),
    dict(title="Databricks Core Components",
         objective="Introduce the five building blocks of the platform.",
         content="Workspace, Spark+Photon, Delta Lake, Mosaic AI, Unity Catalog.",
         visual="Five-step icon carousel with numbered badges and a summary band.",
         diagram="Carousel: Workspace → Spark+Photon → Delta Lake → Mosaic AI → Unity Catalog.",
         design="Each component a distinct color; summary band ties them into the Lakehouse."),
    dict(title="Why Enterprises Choose Databricks",
         objective="Summarise the value proposition in leadership language.",
         content="Six benefits: unified, open, performant, elastic, collaborative, governed.",
         visual="2x3 benefit card grid.",
         diagram="—",
         design="Tie each benefit back to a challenge from Section 1."),
    dict(title="Section 03 Divider — Databricks Architecture",
         objective="Transition into Section 3.",
         content="Section number, title and three covered themes.",
         visual="Navy divider with a giant '03' watermark and a cluster icon.",
         diagram="—",
         design="Same divider system; signals the deep-dive section."),
    dict(title="Architecture Overview — Two Planes",
         objective="Teach the control-plane vs compute-plane split (the key security idea).",
         content="Control plane components (managed) and compute plane components (your cloud).",
         visual="Two stacked bands joined by a vertical double-arrow; component chips in each.",
         diagram="Control Plane (Databricks-managed) ⇅ Compute Plane (your cloud account).",
         design="Navy band = managed; white band = your tenancy. Stress 'data never leaves'."),
    dict(title="Control Plane & Compute Plane in Detail",
         objective="Go deeper on each plane and the classic vs serverless compute models.",
         content="Control-plane responsibilities and compute-plane responsibilities side by side.",
         visual="Two detailed cards with colored headers and bulleted responsibilities.",
         diagram="—",
         design="Indent the classic/serverless sub-points; answer 'where does my data live?'"),
    dict(title="Apache Spark — Distributed Execution",
         objective="Explain Spark's driver/executor model and Photon acceleration.",
         content="Driver, cluster manager, executors with partitioned tasks; Photon callout.",
         visual="Driver card → connectors → three executor cards (P1–P4 tasks); Photon panel.",
         diagram="Driver → Cluster Manager → Executors (parallel tasks on partitions).",
         design="Use the chef/line-cooks analogy; Photon = drop-in 2–3x speedup."),
    dict(title="Delta Lake — Reliability on the Lake",
         objective="Show how Parquet + a transaction log create a reliable table.",
         content="Storage layer + _delta_log → Delta table; four feature cards.",
         visual="Layered 'how it works' card on the left; ACID/Time-Travel/Schema/Streaming cards on the right.",
         diagram="Parquet files + _delta_log (JSON) = one ACID Delta table.",
         design="The transaction log is the 'aha'; mention OPTIMIZE / Z-ORDER."),
    dict(title="The Medallion Architecture",
         objective="Teach the Bronze→Silver→Gold refinement pattern.",
         content="Three quality tiers with roles and a value gradient.",
         visual="Three large cards with arrows and a bronze→gold quality gradient bar.",
         diagram="Raw → Bronze → Silver → Gold → Dashboards / ML.",
         design="Medal tones (bronze/silver/gold); quality and value rise left-to-right."),
    dict(title="Cluster & Compute Architecture",
         objective="Explain cluster anatomy, autoscaling, the runtime, and cluster types.",
         content="Driver + workers + autoscaling + DBR; four cluster types.",
         visual="Anatomy card (driver/workers/ghost autoscale) + four cluster-type cards.",
         diagram="Driver Node + Worker Nodes (+ autoscale) on the Databricks Runtime.",
         design="Note cost guidance: job clusters for prod, auto-terminate interactive."),
    dict(title="Security & Governance — Unity Catalog",
         objective="Show unified governance via the three-level namespace and four pillars.",
         content="catalog.schema.table namespace; access, lineage, sharing, compliance.",
         visual="Nested namespace diagram + a 2x2 governance pillar grid.",
         diagram="Catalog → Schema → Table/View/Volume/Model  (catalog.schema.table).",
         design="One governance model across clouds; mention Delta Sharing."),
    dict(title="End-to-End Data Flow (Capstone)",
         objective="Tie the whole course together by tracing a request source-to-dashboard.",
         content="Seven numbered stages grouped by plane, with a Unity Catalog governance underlay.",
         visual="Seven-stage horizontal flow with plane-grouping chips and a governance band.",
         diagram="Users → Workspace → Clusters → Spark+Photon → Delta Lake → Cloud Storage → BI & AI.",
         design="Walk left-to-right slowly; this single slide IS the architecture."),
    dict(title="Integration Architecture — An Open Hub",
         objective="Position Databricks as an open hub, not a rip-and-replace.",
         content="Central Lakehouse with six integration categories and supported languages.",
         visual="Hub-and-spoke: central lava hub with six connected spoke cards.",
         diagram="Lakehouse hub ↔ Storage / Ingestion / Orchestration / BI / ML / Governance.",
         design="Reinforce openness and incremental adoption; no lock-in."),
    dict(title="Key Takeaways",
         objective="Recap the three sections and land four memorable takeaways.",
         content="Three recap cards + four takeaway banners.",
         visual="Three numbered recap cards over four icon takeaway banners.",
         diagram="—",
         design="Quiz the room on the four takeaways before moving on."),
    dict(title="Knowledge Check & Interview Questions",
         objective="Reinforce learning and prep for interviews.",
         content="Five knowledge-check questions and five common interview questions.",
         visual="Two cards: blue 'Knowledge Check' and navy/lava 'Interview Questions'.",
         diagram="—",
         design="Run the left column as a live quiz; model answers are in the notes."),
    dict(title="Thank You / Closing",
         objective="Close, recap visually and point to self-study resources.",
         content="Thank-you, resource chips and a six-icon recap.",
         visual="Navy closing slide with resource chips and recap icon row.",
         diagram="—",
         design="Mirror the cover; invite questions and preview any next session."),
]


def main():
    prs = Presentation(PPTX)
    slides = list(prs.slides)
    assert len(slides) == len(SPECS), f"{len(slides)} slides vs {len(SPECS)} specs"

    lines = []
    A = lines.append
    A("# Big Data & Databricks — Slide Specifications & Facilitator Guide\n")
    A("_From Fundamentals to the Lakehouse · Enterprise Data Platform Training Series_\n")
    A("This document specifies every slide in **Big-Data-and-Databricks-Training.pptx** "
      "using the design format below. Speaker notes are extracted directly from the deck, "
      "so they always match what a presenter sees in PowerPoint's notes pane.\n")
    A("> **Format:** Objective · Content · Visual Layout · Diagram · Speaker Notes · Design Tips\n")
    A("\n---\n")

    section_breaks = {3: "Section 1 · Big Data Fundamentals",
                      11: "Section 2 · Introduction to Databricks",
                      19: "Section 3 · Databricks Architecture"}

    for i, (sp, slide) in enumerate(zip(SPECS, slides), start=1):
        if i in section_breaks:
            A(f"\n## {section_breaks[i]}\n")
        notes = ""
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
        A(f"### Slide {i}: {sp['title']}\n")
        A(f"**Objective:** {sp['objective']}\n")
        A(f"**Content:** {sp['content']}\n")
        A(f"**Visual Layout:** {sp['visual']}\n")
        A(f"**Diagram:** {sp['diagram']}\n")
        A(f"**Speaker Notes:** {notes}\n")
        A(f"**Design Tips:** {sp['design']}\n")
        A("\n---\n")

    with open(OUT, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUT} ({len(SPECS)} slides documented)")


if __name__ == "__main__":
    main()

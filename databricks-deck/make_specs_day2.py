#!/usr/bin/env python3
"""
make_specs_day2.py
------------------
Generates SLIDE-SPECIFICATIONS-Day2.md — per-slide design document &
facilitator guide for the Day 2 deck. Speaker notes are read directly from
the built .pptx so the document always matches the deck.
"""
from pptx import Presentation

PPTX = "Databricks-Day2-Spark-Workspace-Lakehouse.pptx"
OUT = "SLIDE-SPECIFICATIONS-Day2.md"

SPECS = [
    dict(title="Title / Cover",
         objective="Open Day 2 and frame the three pillars: engine, environment, architecture.",
         content="Course title, subtitle, three part-chips, audience and a 'builds on Day 1' note.",
         visual="Dark navy gradient cover with lava accent bar, oversized title and part chips.",
         diagram="—",
         design="Mirror Day 1's cover system — navy + lava, bold title, lava subtitle."),
    dict(title="Day 2 Roadmap — What We'll Build Today",
         objective="Preview the three parts and the outcome of each.",
         content="Three part cards (Spark, Workspace, Lakehouse) with topics and outcomes.",
         visual="Three colored cards with icon badges, topic bullets and an OUTCOME line.",
         diagram="Three-column roadmap (Part 01 / 02 / 03).",
         design="Color-code parts blue / lava / green; four topics each."),
    dict(title="Part 01 Divider — Apache Spark Fundamentals",
         objective="Transition into the Spark deep-dive.",
         content="Part number, title and three covered themes.",
         visual="Navy divider with a giant '01' watermark and a lightning icon.",
         diagram="—",
         design="Reuse the shared divider system across all three parts."),
    dict(title="What Is Apache Spark?",
         objective="Define Spark precisely and make its scale tangible.",
         content="Definition card, three clarifying bullets and four headline stats.",
         visual="Navy definition card + 2x2 stat tiles (100x, 4 langs, 2009, 1000s).",
         diagram="—",
         design="Stress 'unified' and 'in-memory'; let the stats carry the right side."),
    dict(title="Why Spark Won",
         objective="Explain the advantages that displaced Hadoop MapReduce.",
         content="Six benefits: speed, unified engine, easy APIs, scalability, fault tolerance, ecosystem.",
         visual="2x3 card grid with icons.",
         diagram="—",
         design="Tie the last card forward — Spark is the engine Databricks productized."),
    dict(title="Spark Architecture",
         objective="Teach the master/worker execution model.",
         content="Driver, Cluster Manager, Executors and Tasks, with a 'how it runs' note.",
         visual="Four-step icon carousel with numbered badges and a summary band.",
         diagram="Driver → Cluster Manager → Executors → Tasks.",
         design="Chef / line-cooks analogy; note Databricks manages it all."),
    dict(title="Spark's Unified Component Stack",
         objective="Show that Spark is one core engine with specialized libraries.",
         content="Spark SQL, DataFrames, Structured Streaming, MLlib, GraphX.",
         visual="Five-card carousel over a 'one engine, one core' note band.",
         diagram="Spark SQL · DataFrames · Structured Streaming · MLlib · GraphX (on Spark Core).",
         design="One color per library; emphasise mixing them in one pipeline."),
    dict(title="Spark Execution Flow",
         objective="Explain lazy evaluation and how a query becomes parallel work.",
         content="Code/Query → DAG → Stages → Tasks → Results, plus a lazy-evaluation note.",
         visual="Five-step icon carousel with arrows.",
         diagram="Query → DAG → Stages → Tasks → Results.",
         design="Highlight that nothing runs until an action fires."),
    dict(title="Spark vs. Hadoop MapReduce",
         objective="Contrast the two engines to crystallize Spark's advantages.",
         content="Seven-row comparison across processing, speed, programming, workloads, real-time, ML, fault tolerance.",
         visual="Three-column comparison table with header chips and zebra striping.",
         diagram="Comparison table (Aspect | Hadoop MapReduce | Apache Spark).",
         design="The Processing row (in-memory vs disk) is the crux of the speedup."),
    dict(title="What Teams Build with Spark",
         objective="Make Spark tangible through real workloads.",
         content="Six use cases: ETL, streaming, ML, SQL/BI, graph, data-lake processing.",
         visual="2x3 card grid with icons.",
         diagram="—",
         design="Land the last card — Delta & medallion pipelines run on Spark."),
    dict(title="Best Practices & Part 1 Takeaways",
         objective="Give practical tuning guidance and recap Part 1.",
         content="Four best practices and a five-point takeaways panel.",
         visual="2x2 best-practice grid beside a navy takeaways panel.",
         diagram="—",
         design="Reassure that Databricks automates most tuning (Photon)."),
    dict(title="Part 02 Divider — Databricks Workspace Components",
         objective="Transition into the Workspace tour.",
         content="Part number, title and three covered themes.",
         visual="Navy divider with a giant '02' watermark and a notebook icon.",
         diagram="—",
         design="Consistent divider system."),
    dict(title="The Databricks Workspace",
         objective="Define the Workspace as the unified, collaborative hub.",
         content="Definition card, four attribute cards and a 'one place for everyone' note.",
         visual="Navy definition card + vertical stack of four cards + note band.",
         diagram="—",
         design="Stress consolidation and collaboration across personas."),
    dict(title="Workspace Architecture",
         objective="Show how the Workspace is layered from users to storage.",
         content="Personas → Workspace UI → Compute → Unity Catalog → Cloud storage.",
         visual="Stacked horizontal bands with component chips and connecting arrows.",
         diagram="Users ↓ Workspace UI ↓ Compute ↓ Unity Catalog ↓ Open cloud storage.",
         design="Read top-to-bottom; mirrors Day 1's two-plane model from the user side."),
    dict(title="The Seven Building Blocks",
         objective="Tour the seven components used daily.",
         content="Workspace, Notebook, Cluster, Jobs, Repos, Unity Catalog, Dashboards.",
         visual="Four-column card grid (7 cards) with icons.",
         diagram="—",
         design="Preview that notebooks, clusters, Repos and Unity Catalog get deep dives."),
    dict(title="The Notebook Lifecycle",
         objective="Show a notebook's arc from idea to production.",
         content="Create → Attach → Develop → Run & Visualize → Version → Operationalize.",
         visual="Six-step icon carousel with arrows and a note band.",
         diagram="Create → Attach → Develop → Run → Version → Operationalize.",
         design="Key point: no productionization rewrite — same artifact ships."),
    dict(title="Cluster Types — Choosing Compute",
         objective="Explain all-purpose vs job clusters and the specialized options.",
         content="Five-aspect comparison plus SQL Warehouse and Serverless cards.",
         visual="Comparison table over two highlight cards.",
         diagram="Comparison table (Aspect | All-Purpose | Job Cluster).",
         design="Rule of thumb: develop on all-purpose, run prod on job clusters."),
    dict(title="Repos & Git Integration",
         objective="Bring software-engineering discipline to data work.",
         content="Databricks Repo ↔ remote Git, plus the clone→…→deploy workflow.",
         visual="Two synced boxes with bidirectional arrows over a 7-step workflow strip.",
         diagram="Databricks Repo ⇄ Remote Git; Clone → Branch → Commit → Push → PR → Merge → CI/CD.",
         design="Message: pipelines get version control, review and CI/CD."),
    dict(title="Unity Catalog — Unified Governance",
         objective="Show the three-level namespace and governance pillars.",
         content="catalog.schema.object namespace plus four governance pillars.",
         visual="Nested namespace diagram + a 2x2 pillar grid.",
         diagram="Catalog → Schema → Table/View/Volume/Model (catalog.schema.object).",
         design="Unique angle: governs data AND AI assets together."),
    dict(title="Best Practices & Part 2 Takeaways",
         objective="Give Workspace operating discipline and recap Part 2.",
         content="Four best practices and a five-point takeaways panel.",
         visual="2x2 best-practice grid beside a navy takeaways panel.",
         diagram="—",
         design="Bridge to Part 3 — assemble engine + environment into architecture."),
    dict(title="Part 03 Divider — Databricks Lakehouse Architecture",
         objective="Transition into the architecture build.",
         content="Part number, title and three covered themes.",
         visual="Navy divider with a giant '03' watermark and a Delta icon.",
         diagram="—",
         design="Consistent divider system; signals the synthesis section."),
    dict(title="Evolution of Data Platforms",
         objective="Frame the Lakehouse as the resolution of a 40-year trade-off.",
         content="Data Warehouse → Data Lake → Lakehouse, each with its limitation.",
         visual="Three cards with arrows, limitations and a closing note.",
         diagram="Data Warehouse → Data Lake → Lakehouse.",
         design="Each generation fixed the last one's flaw."),
    dict(title="What Is the Lakehouse?",
         objective="Define the Lakehouse crisply for anyone new on Day 2.",
         content="Definition card, three bullets and four attribute tiles.",
         visual="Navy definition card + 2x2 attribute tiles (Open, Reliable, Unified, Governed).",
         diagram="—",
         design="The mechanism — Delta on object storage — is the key idea."),
    dict(title="Lakehouse Architecture — Layer by Layer",
         objective="Present the reference architecture to memorize.",
         content="Sources → Ingestion → Bronze → Silver → Gold → BI/AI/ML, on Delta + Unity Catalog.",
         visual="Six-stage pipeline over a Delta + Unity Catalog foundation band.",
         diagram="Sources → Ingestion → Bronze → Silver → Gold → BI/AI/ML.",
         design="Medal tones for Bronze/Silver/Gold; foundations make it a Lakehouse."),
    dict(title="The Medallion Architecture — In Detail",
         objective="Detail each medallion layer's data, ops, quality and users.",
         content="Bronze, Silver, Gold described across four dimensions, with a value gradient.",
         visual="Three detail cards with mini-tables, arrows and a bronze→gold gradient.",
         diagram="Bronze → Silver → Gold (quality & value rising).",
         design="Every layer is a Delta table, enabling incremental & streaming."),
    dict(title="Delta Lake Fundamentals",
         objective="Explain the four features that make the Lakehouse possible.",
         content="ACID, Time Travel, Schema Enforcement, Data Versioning + the 'under the hood' note.",
         visual="Four-card carousel over a Parquet + transaction-log note band.",
         diagram="ACID · Time Travel · Schema Enforcement · Versioning (Parquet + _delta_log).",
         design="The transaction log is the mechanism behind all four."),
    dict(title="Delta Lake — Transaction Flow",
         objective="Show how Delta guarantees reliability via the transaction log.",
         content="Write path, the versioned _delta_log, and the read path.",
         visual="Write-path cards → versioned log band → read-path card.",
         diagram="Write → validate → write Parquet → atomic commit to _delta_log (v0..vN) → consistent reads.",
         design="Atomic commit + ordered log = ACID and time travel on object storage."),
    dict(title="Governance & Open Sharing",
         objective="Show estate-wide governance and open data sharing.",
         content="Six governance pillars including Delta Sharing and data+AI governance.",
         visual="2x3 card grid with icons.",
         diagram="—",
         design="Delta Sharing = open, no-copy sharing readable by any client."),
    dict(title="AI & ML on the Lakehouse",
         objective="Show the ML/GenAI lifecycle on governed data.",
         content="Gold data → features → train → register → serve, plus a Mosaic AI note.",
         visual="Five-step icon carousel with arrows and a note band.",
         diagram="Gold Data → Feature Engineering → Train (MLflow) → Register → Serve & Monitor.",
         design="Models built on governed data get lineage & security end to end."),
    dict(title="End-to-End Data Pipeline",
         objective="Tie all three parts into one production pipeline (capstone).",
         content="Sources → Ingest → Bronze → Silver → Gold → Consume, with orchestration & governance.",
         visual="Six numbered stages grouped by phase over a Workflows + Unity Catalog band.",
         diagram="Sources → Ingest → Bronze → Silver → Gold → Consume (Spark · Delta · Workflows · UC).",
         design="Connect each box to the engine, environment and architecture learned today."),
    dict(title="Benefits of the Lakehouse",
         objective="Summarize the Lakehouse value in leadership terms.",
         content="Six benefits: unified, open, reliable, performant, governed, cost-effective.",
         visual="2x3 card grid with icons.",
         diagram="—",
         design="One-line ROI: consolidation + faster, governed delivery."),
    dict(title="Real-World Example — Omni-Channel Retailer",
         objective="Ground the architecture in a believable case study.",
         content="A retail pipeline and four outcome KPIs.",
         visual="Left pipeline card (4 stacked stages) + right 2x2 KPI tiles.",
         diagram="POS/Web/Mobile → Auto Loader → Bronze→Silver→Gold → Genie/ML/GenAI.",
         design="Present figures as representative outcomes; invite mapping to their use case."),
    dict(title="Day 2 — Key Takeaways",
         objective="Recap the three parts and land four takeaways.",
         content="Three recap cards (Spark / Workspace / Lakehouse) + four takeaway banners.",
         visual="Three numbered recap cards over four icon takeaway banners.",
         diagram="—",
         design="Quiz the room before the close."),
    dict(title="Thank You / Closing",
         objective="Close, recap visually and point to hands-on resources.",
         content="Thank-you, resource chips, six-icon recap and a next-session preview.",
         visual="Navy closing slide with resource chips and recap icon row.",
         diagram="—",
         design="Mirror the cover; preview the hands-on lab & Delta Live Tables."),
]


def main():
    prs = Presentation(PPTX)
    slides = list(prs.slides)
    assert len(slides) == len(SPECS), f"{len(slides)} slides vs {len(SPECS)} specs"

    L = []
    A = L.append
    A("# Databricks Day 2 — Slide Specifications & Facilitator Guide\n")
    A("_Spark, Workspace & Lakehouse · Enterprise Data Platform Training Series_\n")
    A("This document specifies every slide in **Databricks-Day2-Spark-Workspace-Lakehouse.pptx** "
      "using the design format below. Speaker notes are extracted directly from the deck, so they "
      "always match what a presenter sees in PowerPoint's notes pane.\n")
    A("> **Format:** Objective · Content · Visual Layout · Diagram · Speaker Notes · Design Tips\n")
    A("\n---\n")

    section_breaks = {3: "Part 1 · Apache Spark Fundamentals",
                      11: "Part 2 · Databricks Workspace Components",
                      19: "Part 3 · Databricks Lakehouse Architecture"}

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
        f.write("\n".join(L))
    print(f"Wrote {OUT} ({len(SPECS)} slides documented)")


if __name__ == "__main__":
    main()

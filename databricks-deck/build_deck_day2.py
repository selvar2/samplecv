#!/usr/bin/env python3
"""
build_deck_day2.py
------------------
DAY 2 of the Databricks training series — same design system as Day 1.

Topics:  Apache Spark Fundamentals · Databricks Workspace Components ·
         Databricks Lakehouse Architecture

Reuses the shared design kit (deck_kit.py) and the layout composites defined
for Day 1 (build_deck.py) so the two decks are visually identical in style.

Run:  python3 build_deck_day2.py
Out:  Databricks-Day2-Spark-Workspace-Lakehouse.pptx
"""

from math import ceil
from deck_kit import *
from build_deck import (flow_steps, grid_cards, pipeline, timeline,
                        vs_table, hub_spoke, dark_bg, takeaway, s_divider)
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

OUT = "Databricks-Day2-Spark-Workspace-Lakehouse.pptx"


# ===========================================================================
#  Local helpers (kept tiny; everything heavy comes from the shared kit)
# ===========================================================================
def note_band(s, y, text_runs, h=1.0, fill=OAT_2):
    card(s, MX, y, CW, h, fill=fill, line=LINE, shadow=False)
    text(s, MX + 0.38, y, CW - 0.76, h, text_runs, anchor=MSO_ANCHOR.MIDDLE, spacing=1.25)


def section_progress(s, active):
    """Tiny 3-dot section progress marker, top-right under the header rule."""
    labels = ["Spark", "Workspace", "Lakehouse"]
    x = SW - MX - 3.5
    for i, lab in enumerate(labels):
        on = (i == active)
        cxp = x + i * 1.18
        circle(s, cxp, 1.46, 0.12 if on else 0.085, LAVA if on else OAT_3)
        text(s, cxp - 0.55, 1.55, 1.1, 0.22, lab, size=7.5,
             color=(NAVY if on else GRAY_LT), align=PP_ALIGN.CENTER,
             bold=on, font=FONT_SB)


# ===========================================================================
#  TITLE & AGENDA
# ===========================================================================
def d2_cover(prs):
    s = slide(prs, bg=NAVY)
    dark_bg(s)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 1.45, 0.09, 2.0, fill=LAVA, line=None, adj=0.5)
    text(s, MX + 0.30, 1.40, 9.5, 0.3, "DATABRICKS PLATFORM ENABLEMENT  ·  DAY 2",
         size=12.5, color=LAVA_LT, bold=True, font=FONT_SB)
    text(s, MX + 0.27, 1.82, 11.6, 1.2,
         [[{"t": "Spark, Workspace ", "color": WHITE, "size": 49, "bold": True},
           {"t": "& Lakehouse", "color": WHITE, "size": 49, "bold": True}]], spacing=1.0)
    text(s, MX + 0.29, 2.82, 11.4, 0.8, "The engine, the environment, and the architecture",
         size=27, color=LAVA, bold=True, font=FONT_LT)
    text(s, MX + 0.30, 3.74, 9.7, 0.7,
         "Go under the hood of Apache Spark, master the Databricks Workspace, and see how "
         "the Lakehouse unifies engineering, analytics and AI on one governed platform.",
         size=14, color=RGBColor(0xC4, 0xD0, 0xD4), spacing=1.25)
    chips = [("01", "Apache Spark Fundamentals"), ("02", "Workspace Components"),
             ("03", "Lakehouse Architecture")]
    cx = MX + 0.30
    for no, label in chips:
        w = 3.62
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx, 4.85, w, 0.62, fill=None,
              line=LINE_DK, line_w=1.3, adj=0.5)
        text(s, cx + 0.30, 4.85, w - 0.45, 0.62,
             [[{"t": no + "    ", "color": LAVA, "size": 13, "bold": True},
               {"t": label, "color": WHITE, "size": 12, "bold": True}]],
             anchor=MSO_ANCHOR.MIDDLE)
        cx += w + 0.26
    band(s, MX + 0.30, 6.05, 6.5, 0.02, LINE_DK)
    text(s, MX + 0.30, 6.22, 11, 0.4,
         "Audience:  Data Engineers · Analysts · Data Scientists · Platform & Cloud Architects",
         size=11.5, color=GRAY_LT)
    text(s, MX + 0.30, 6.62, 11, 0.4,
         "Builds on Day 1 — Big Data fundamentals & the Lakehouse foundations",
         size=11.5, color=GRAY_LT, italic=True)
    notes(s,
          "Welcome back for Day 2. Day 1 covered the 'what and why' — Big Data, the Lakehouse concept and "
          "a high-level platform tour. Day 2 is the 'how': we go deep on the three pillars an engineer touches "
          "every day. Part 1 opens up Apache Spark — the distributed engine under everything. Part 2 is a "
          "working tour of the Databricks Workspace — notebooks, clusters, jobs, repos and governance. Part 3 "
          "assembles it all into the Lakehouse architecture, from Delta Lake to the medallion pattern to an "
          "end-to-end pipeline. By the end, attendees can read an architecture diagram and explain how a query "
          "becomes a governed dashboard.")


def d2_agenda(prs):
    s = slide(prs)
    header(s, "Day 2 Roadmap", "What We'll Build Today")
    secs = [
        dict(no="01", color=BLUE, icon="bolt", title="Apache Spark Fundamentals",
             items=["What & why Spark", "Architecture & components",
                    "Execution flow & Spark vs Hadoop", "Use cases & best practices"],
             outcome="Explain how Spark runs a job in parallel."),
        dict(no="02", color=LAVA, icon="doc", title="Workspace Components",
             items=["Workspace & notebooks", "Clusters, jobs & lifecycle",
                    "Repos & Git integration", "Unity Catalog & best practices"],
             outcome="Navigate and operate the Databricks Workspace."),
        dict(no="03", color=GREEN, icon="delta", title="Lakehouse Architecture",
             items=["Evolution & Delta Lake", "Medallion & governance",
                    "AI / ML integration", "End-to-end data flow"],
             outcome="Design a governed, end-to-end Lakehouse pipeline."),
    ]
    cw = (CW - 2 * 0.4) / 3
    for i, sec in enumerate(secs):
        x = MX + i * (cw + 0.4)
        card(s, x, 2.05, cw, 4.5, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.05, cw, 0.14, sec["color"])
        icon_tile(s, x + 0.78, 2.95, 1.0, sec["icon"], sec["color"], shadow=True)
        text(s, x + 1.5, 2.62, cw - 1.6, 0.4, "PART " + sec["no"], size=11,
             color=sec["color"], bold=True, font=FONT_SB)
        text(s, x + 1.5, 2.92, cw - 1.6, 0.7, sec["title"], size=15.5, color=NAVY,
             bold=True, spacing=0.98)
        band(s, x + 0.42, 3.66, cw - 0.84, 0.014, OAT_3)
        bullets(s, x + 0.46, 3.84, cw - 0.8, 2.0,
                [(it, 0) for it in sec["items"]], size=12.5, marker=sec["color"],
                gap=12, spacing=1.05)
        band(s, x + 0.42, 5.72, cw - 0.84, 0.014, OAT_3)
        text(s, x + 0.46, 5.86, cw - 0.86, 0.6,
             [[{"t": "OUTCOME   ", "color": sec["color"], "bold": True, "size": 9.5, "font": FONT_SB},
               {"t": sec["outcome"], "color": GRAY_2, "size": 10.5, "italic": True}]], spacing=1.12)
    text(s, MX, 6.74, CW, 0.3,
         "From the engine, to the environment, to the architecture — one continuous build.",
         size=11.5, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "Set the map for the day. Three parts, each answering a practical question: Part 1 — how does the "
          "engine actually run my code? Part 2 — where and how do I do my work? Part 3 — how does it all fit "
          "together into a production architecture? Tell learners each part ends with best practices and a "
          "summary, and that the day culminates in a single end-to-end pipeline diagram that uses everything "
          "we covered. No deep prior Spark knowledge required.")


# ===========================================================================
#  PART 1 — APACHE SPARK FUNDAMENTALS
# ===========================================================================
def d2_what_spark(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "What Is Apache Spark?")
    section_progress(s, 0)
    card(s, MX, 2.0, 6.55, 2.55, fill=NAVY, line=None, shadow=True)
    text(s, MX + 0.4, 2.28, 5.8, 0.3, "DEFINITION", size=11, color=LAVA_LT, bold=True, font=FONT_SB)
    text(s, MX + 0.4, 2.62, 5.85, 1.85,
         [[{"t": "Apache Spark is a ", "color": WHITE, "size": 14.5},
           {"t": "unified, open-source, distributed engine", "color": LAVA_LT, "size": 14.5, "bold": True},
           {"t": " for large-scale data processing — running computations ", "color": WHITE, "size": 14.5},
           {"t": "in memory", "color": LAVA_LT, "size": 14.5, "bold": True},
           {"t": " across a cluster to power batch, streaming, SQL, machine learning and graph workloads.",
            "color": WHITE, "size": 14.5}]], spacing=1.3)
    bullets(s, MX + 0.05, 4.85, 6.5, 1.8, [
        "One engine, many workloads — no separate tools to stitch",
        "Lazy evaluation + a DAG optimizer plan work efficiently",
        "The compute foundation beneath Databricks & the Lakehouse",
    ], size=12.8, marker=LAVA, gap=10)
    facts = [("100x", "faster than disk-based\nMapReduce (in-memory)", BLUE),
             ("4 langs", "Python · SQL · Scala · R\n(+ Java) — one API", LAVA),
             ("2009", "born at UC Berkeley\nAMPLab; open-sourced", GREEN),
             ("1000s", "of nodes — scales from\nlaptop to data center", PURPLE)]
    gx, gy = 0.3, 0.3
    tw, th = (4.55 - gx) / 2, (4.55 - gy) / 2
    x0 = 7.55
    for i, (big, lab, col) in enumerate(facts):
        r, c = divmod(i, 2)
        x = x0 + c * (tw + gx); y = 2.0 + r * (th + gy)
        card(s, x, y, tw, th, fill=WHITE, line=LINE, shadow=True)
        band(s, x, y, 0.10, th, col)
        text(s, x + 0.28, y + 0.18, tw - 0.4, 0.6, big, size=25, color=col, bold=True)
        text(s, x + 0.30, y + 0.78, tw - 0.45, 0.9, lab.replace("\n", " "),
             size=10.5, color=GRAY, spacing=1.05)
    footer(s)
    notes(s,
          "Define Spark precisely: a unified, distributed, in-memory engine. The two words that matter most "
          "are 'unified' (one engine for batch, streaming, SQL, ML and graph — versus the old world of a "
          "different tool per workload) and 'in-memory' (it keeps working data in RAM across the cluster "
          "rather than writing to disk between steps, which is why it's up to 100x faster than Hadoop "
          "MapReduce for iterative work). Spark came out of UC Berkeley's AMPLab in 2009 — the same team that "
          "founded Databricks. Emphasise that everything in Databricks ultimately runs on Spark.")


def d2_why_spark(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "Why Spark Won")
    section_progress(s, 0)
    items = [
        dict(icon="bolt", color=LAVA, title="In-Memory Speed",
             desc="Keeps data in RAM and optimizes a DAG of work — up to 100x faster than MapReduce."),
        dict(icon="hex", color=BLUE, title="Unified Engine",
             desc="Batch, streaming, SQL, ML and graph share one runtime and one set of APIs."),
        dict(icon="doc", color=GREEN, title="Easy, High-Level APIs",
             desc="DataFrames & SQL replace verbose MapReduce code in Python, SQL, Scala or R."),
        dict(icon="cluster", color=TEAL, title="Massive Scalability",
             desc="Scales out linearly from a single laptop to thousands of cluster nodes."),
        dict(icon="shield", color=YELLOW, title="Fault Tolerance",
             desc="Lineage (the DAG) lets Spark recompute lost partitions automatically."),
        dict(icon="globe", color=PURPLE, title="Open Ecosystem",
             desc="Huge community, rich libraries, and the foundation of the Databricks platform."),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=14, desc_size=11)
    footer(s)
    notes(s,
          "Frame these as the reasons Spark displaced Hadoop MapReduce as the default big-data engine. Speed "
          "and the unified model are the headline wins, but ease of use was just as important — DataFrames and "
          "SQL let analysts and engineers be productive without writing low-level Java. Fault tolerance comes "
          "'for free' from lineage: because Spark knows the DAG that produced each dataset, it can recompute "
          "just the lost pieces if a node fails. Tie the last card forward: this ecosystem and engine are "
          "exactly what Databricks productized and made effortless to run.")


def d2_spark_arch(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "Spark Architecture")
    section_progress(s, 0)
    steps = [
        dict(title="Driver", icon="gear", color=NAVY_2, badge=1,
             desc="Runs your program & SparkSession; builds the DAG and schedules work."),
        dict(title="Cluster Manager", icon="cluster", color=BLUE, badge=2,
             desc="Allocates resources — Standalone, YARN, Kubernetes or Databricks."),
        dict(title="Executors", icon="cube", color=TEAL, badge=3,
             desc="JVM processes on worker nodes that run tasks and cache data in memory."),
        dict(title="Tasks", icon="bolt", color=LAVA, badge=4,
             desc="The unit of work — one task processes one partition, in parallel."),
    ]
    flow_steps(s, steps, y_top=2.3, card_h=2.35, icon_d=1.0, arrow=True)
    note_band(s, 5.05,
              [[{"t": "How it runs:  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "the Driver turns your code into a DAG, the Cluster Manager grants Executors, and "
                      "each Executor runs Tasks in parallel — one per data partition. ", "color": GRAY, "size": 12.5},
                {"t": "On Databricks, all of this is fully managed.", "color": LAVA, "size": 12.5, "bold": True}]],
              h=1.0)
    text(s, MX, 6.25, CW, 0.4,
         "Master / worker model:  one Driver coordinates, many Executors do the work in parallel.",
         size=12, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "Walk the four-part chain left to right. The DRIVER is the brain — it hosts the SparkSession, "
          "translates your code into a logical plan, optimizes it into a DAG of stages, and schedules tasks. "
          "The CLUSTER MANAGER is the resource broker (Standalone, YARN, Kubernetes, or Databricks' own). "
          "EXECUTORS are JVM worker processes that actually run computation and cache data in memory. TASKS "
          "are the atoms of work — each one processes a single partition, and they run simultaneously across "
          "executors, which is where the parallelism (and the speed) comes from. Analogy: the driver is the "
          "head chef writing the plan; executors are line cooks; tasks are individual dishes cooked at once. "
          "Reassure them Databricks provisions and tunes all of this automatically.")


def d2_spark_components(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "Spark's Unified Component Stack")
    section_progress(s, 0)
    steps = [
        dict(title="Spark SQL", icon="database", color=BLUE, badge=1,
             desc="ANSI SQL + the Catalyst query optimizer."),
        dict(title="DataFrames", icon="variety", color=TEAL, badge=2,
             desc="Typed distributed tables — the core API."),
        dict(title="Structured\nStreaming", icon="bolt", color=LAVA, badge=3,
             desc="Real-time pipelines, same DataFrame code."),
        dict(title="MLlib", icon="ml", color=GREEN, badge=4,
             desc="Scalable ML algorithms & pipelines."),
        dict(title="GraphX", icon="link", color=PURPLE, badge=5,
             desc="Graph processing on connected data."),
    ]
    flow_steps(s, steps, y_top=2.3, card_h=2.65, icon_d=1.0, arrow=False,
               desc_size=9.8, desc_dy=1.78)
    note_band(s, 5.2,
              [[{"t": "One engine, one core.  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "Every library sits on the same Spark Core (RDDs, scheduler, memory manager), so you "
                      "can mix SQL, streaming and ML in a single pipeline — and Photon accelerates them on Databricks.",
                 "color": GRAY, "size": 12.5}]], h=1.05)
    footer(s)
    notes(s,
          "Spark is not five separate products — it's one core engine with specialized libraries on top, all "
          "sharing the same execution model. SPARK SQL brings ANSI SQL and the Catalyst query optimizer. "
          "DATAFRAMES are the high-level, optimized API most people use daily (think distributed tables). "
          "STRUCTURED STREAMING lets you write streaming pipelines with the exact same DataFrame code as "
          "batch — a huge simplification. MLLIB provides distributed machine learning. GRAPHX handles graph "
          "analytics. The key teaching point: because they share a core, you can combine them in one job — "
          "e.g., stream data in, transform with SQL, score with an ML model — and on Databricks the Photon "
          "engine accelerates it all.")


def d2_spark_execution(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "Spark Execution Flow")
    section_progress(s, 0)
    steps = [
        dict(title="Code / Query", icon="doc", color=NAVY_2, badge=1,
             desc="DataFrame, SQL or RDD operations — lazily recorded, not yet run."),
        dict(title="DAG", icon="link", color=BLUE, badge=2,
             desc="Catalyst builds & optimizes a Directed Acyclic Graph of the work."),
        dict(title="Stages", icon="cube", color=TEAL, badge=3,
             desc="The DAG is split at shuffle boundaries into stages."),
        dict(title="Tasks", icon="bolt", color=LAVA, badge=4,
             desc="Each stage fans out into parallel tasks — one per partition."),
        dict(title="Results", icon="chart", color=GREEN, badge=5,
             desc="An action triggers execution; results return or are written out."),
    ]
    flow_steps(s, steps, y_top=2.35, card_h=2.45, icon_d=1.0, arrow=True)
    note_band(s, 5.25,
              [[{"t": "Lazy by design.  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "Transformations just build the plan; nothing runs until an ", "color": GRAY, "size": 12.5},
                {"t": "action", "color": LAVA, "size": 12.5, "bold": True},
                {"t": " (e.g. count, write, collect) fires — letting Catalyst optimize the whole DAG first.",
                 "color": GRAY, "size": 12.5}]], h=1.0)
    footer(s)
    notes(s,
          "This explains the single most misunderstood part of Spark: lazy evaluation. When you write "
          "transformations (filter, join, select) Spark does NOT execute them — it just records them, building "
          "a logical plan. The Catalyst optimizer turns that into an optimized DAG. The DAG is divided into "
          "STAGES at shuffle boundaries (points where data must move across the network). Each stage becomes a "
          "set of TASKS, one per partition, run in parallel by executors. Only when you call an ACTION (count, "
          "show, write, collect) does the whole thing actually run. Why this matters: laziness lets Spark see "
          "the entire computation and optimize it globally — reordering filters, pruning columns, minimizing "
          "shuffles — before doing any work.")


def d2_spark_vs_hadoop(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "Spark vs. Hadoop MapReduce")
    section_progress(s, 0)
    rows = [
        ("Processing", "Disk-based, step-by-step", "In-memory, DAG-optimized"),
        ("Speed", "Baseline", "Up to 100x faster (iterative)"),
        ("Programming", "Verbose low-level Java", "Concise DataFrame / SQL APIs"),
        ("Workloads", "Batch only", "Batch + streaming + SQL + ML"),
        ("Real-Time", "Not supported", "Structured Streaming, near real-time"),
        ("Iterative / ML", "Slow — re-reads from disk", "Excellent — caches in memory"),
        ("Fault Tolerance", "Data replication", "Lineage (recompute partitions)"),
    ]
    vs_table(s, MX, 2.0, CW, ("Aspect", "Hadoop MapReduce", "Apache Spark"),
             rows, hcolors=(NAVY_2, LAVA))
    footer(s)
    notes(s,
          "Use this to make Spark's advantages concrete. The crux is the Processing row: MapReduce writes "
          "intermediate results to disk between every map and reduce step, while Spark keeps them in memory — "
          "that's the source of the dramatic speedup, especially for iterative algorithms like ML training "
          "that loop over the same data. Spark is also far easier to program (DataFrames/SQL vs hand-written "
          "Java) and handles many workloads in one engine, including streaming, which MapReduce can't do. Be "
          "fair: Hadoop's HDFS is still a valid storage layer, and Spark can run on it — Spark replaced the "
          "MapReduce compute model, not the whole ecosystem. On Databricks you rarely manage either directly.")


def d2_spark_usecases(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "What Teams Build with Spark")
    section_progress(s, 0)
    items = [
        dict(icon="gear", color=BLUE, title="Large-Scale ETL",
             desc="Cleaning, joining and transforming terabytes of data into analytics-ready tables."),
        dict(icon="bolt", color=LAVA, title="Streaming Analytics",
             desc="Real-time pipelines for fraud, IoT, clickstream and operational dashboards."),
        dict(icon="ml", color=GREEN, title="Machine Learning",
             desc="Distributed feature engineering and model training with MLlib & Spark ML."),
        dict(icon="database", color=TEAL, title="Interactive SQL & BI",
             desc="Ad-hoc and production SQL analytics over the data lake at scale."),
        dict(icon="link", color=PURPLE, title="Graph Analytics",
             desc="Recommendations, fraud rings and network analysis with GraphX."),
        dict(icon="cube", color=YELLOW, title="Data Lake Processing",
             desc="The compute behind Delta Lake and the medallion architecture."),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=14, desc_size=10.8)
    footer(s)
    notes(s,
          "Make Spark tangible by tying each workload to outcomes the audience recognizes. ETL is the bread "
          "and butter — most Spark jobs in production are pipelines turning raw data into clean tables. "
          "Streaming powers real-time use cases like fraud detection. ML and SQL/BI show the unified-engine "
          "payoff: the same platform trains models and serves analysts. Land the last card — when we get to "
          "the Lakehouse, remember that Delta Lake and the medallion pipelines you'll see are all executed by "
          "Spark under the hood.")


def d2_spark_best(prs):
    s = slide(prs)
    header(s, "Apache Spark Fundamentals", "Best Practices & Part 1 Takeaways")
    section_progress(s, 0)
    items = [
        dict(icon="variety", color=LAVA, title="Prefer DataFrames / SQL",
             desc="Let Catalyst & Photon optimize — avoid low-level RDDs unless necessary."),
        dict(icon="cube", color=BLUE, title="Partition Wisely",
             desc="Right-size partitions and watch for data skew that overloads one task."),
        dict(icon="bolt", color=GREEN, title="Minimize Shuffles",
             desc="Shuffles move data across the network — filter early, broadcast small tables."),
        dict(icon="database", color=TEAL, title="Cache Reused Data",
             desc="Persist datasets you reuse across actions to avoid recomputation."),
    ]
    grid_cards(s, items, cols=2, x=MX, y=2.0, w=7.35, h=4.45, gx=0.28, gy=0.28,
               icon_d=0.66, title_size=13, desc_size=10.3)
    # takeaways panel
    card(s, 7.85, 2.0, CW + MX - 7.85, 4.45, fill=NAVY, line=None, shadow=True)
    band(s, 7.85, 2.0, CW + MX - 7.85, 0.6, LAVA)
    icon(s, "star", 7.85 + 0.42, 2.3, 0.34, WHITE)
    text(s, 7.85 + 0.82, 2.0, 4.0, 0.6, "KEY TAKEAWAYS", size=12.5, color=WHITE, bold=True,
         anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    bullets(s, 7.85 + 0.35, 2.85, CW + MX - 7.85 - 0.7, 3.5, [
        "Spark = unified, in-memory, distributed engine",
        "Driver → Cluster Manager → Executors → Tasks",
        "Lazy: a DAG is optimized, then run by an action",
        "One core powers SQL, streaming, ML & graph",
        "Databricks manages & accelerates it (Photon)",
    ], size=12, marker=LAVA_LT, color=RGBColor(0xD6, 0xDE, 0xE1), gap=12)
    footer(s)
    notes(s,
          "Close Part 1 with practical guidance and a recap. Best practices, briefly: prefer the DataFrame/SQL "
          "APIs so Catalyst and Photon can optimize for you; size partitions sensibly and watch for skew "
          "(one giant partition stalls the whole stage); minimize shuffles because moving data across the "
          "network is the main cost — filter early and broadcast small lookup tables; and cache datasets you "
          "reuse. Then recap the five takeaways aloud and check understanding before moving to the Workspace. "
          "Reassure them Databricks automates most tuning, but understanding these concepts helps them write "
          "efficient code and debug slow jobs.")


# ===========================================================================
#  PART 2 — DATABRICKS WORKSPACE COMPONENTS
# ===========================================================================
def d2_workspace_overview(prs):
    s = slide(prs)
    header(s, "Workspace Components", "The Databricks Workspace")
    section_progress(s, 1)
    card(s, MX, 2.0, 7.1, 2.5, fill=NAVY, line=None, shadow=True)
    text(s, MX + 0.4, 2.26, 6.4, 0.3, "DEFINITION", size=11, color=LAVA_LT, bold=True, font=FONT_SB)
    text(s, MX + 0.4, 2.6, 6.4, 1.9,
         [[{"t": "The Workspace is the ", "color": WHITE, "size": 14.5},
           {"t": "unified, collaborative environment", "color": LAVA_LT, "size": 14.5, "bold": True},
           {"t": " where every team builds, runs and governs all data & AI assets — "
                 "notebooks, clusters, jobs, dashboards, repos and data — in ", "color": WHITE, "size": 14.5},
           {"t": "one browser-based hub", "color": LAVA_LT, "size": 14.5, "bold": True},
           {"t": ".", "color": WHITE, "size": 14.5}]], spacing=1.32)
    facts = [
        dict(icon="people", color=LAVA, title="Collaborative",
             desc="Shared notebooks, comments & co-editing for the whole team."),
        dict(icon="globe", color=BLUE, title="Browser-Based",
             desc="Nothing to install — work from anywhere, any cloud."),
        dict(icon="lock", color=GREEN, title="Governed",
             desc="Unity Catalog secures every asset with fine-grained control."),
        dict(icon="flow", color=PURPLE, title="Production-Ready",
             desc="From exploration to scheduled jobs in the same place."),
    ]
    x0 = MX + 7.1 + 0.4
    rw = CW + MX - x0
    gy = 0.10
    th = (2.5 - 3 * gy) / 4
    for i, it in enumerate(facts):
        y = 2.0 + i * (th + gy)
        card(s, x0, y, rw, th, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x0 + 0.42, y + th / 2, 0.5, it["icon"], it["color"], shadow=False)
        text(s, x0 + 0.80, y + 0.07, rw - 0.95, 0.26, it["title"], size=12, color=NAVY, bold=True)
        text(s, x0 + 0.80, y + 0.31, rw - 0.95, 0.24, it["desc"], size=9.3, color=GRAY_2, spacing=1.0)
    note_band(s, 4.75,
              [[{"t": "One place for everyone.  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "Engineers, analysts and scientists share the same notebooks, compute and governed "
                      "data — eliminating the hand-offs and tool-switching of traditional stacks.",
                 "color": GRAY, "size": 12.5}]], h=1.85)
    footer(s)
    notes(s,
          "Introduce the Workspace as the 'home base' of Databricks — the web UI where all work happens. The "
          "key value is consolidation and collaboration: instead of one tool for notebooks, another for "
          "scheduling, another for Git, another for governance, it's all one environment in the browser, on "
          "any cloud. Stress that the same place spans the full lifecycle — interactive exploration through "
          "to production jobs — and that everything is governed by Unity Catalog. Over the next slides we'll "
          "tour each component.")


def d2_workspace_arch(prs):
    s = slide(prs)
    header(s, "Workspace Components", "Workspace Architecture")
    section_progress(s, 1)
    # Layer 1: personas
    personas = ["Data Engineers", "Analysts", "Data Scientists", "ML Engineers", "BI Users"]
    pw = (CW - 4 * 0.22) / 5
    for i, p in enumerate(personas):
        x = MX + i * (pw + 0.22)
        chip(s, x, 2.0, pw, 0.5, p, OAT_2, NAVY, size=10.5, radius=0.3, line=LINE)
    # arrows down
    for i in range(5):
        x = MX + i * (pw + 0.22) + pw / 2
        shape(s, MSO_SHAPE.DOWN_ARROW, x - 0.06, 2.56, 0.12, 0.16, fill=GRAY_LT, line=None)
    # Layer 2: workspace UI
    card(s, MX, 2.8, CW, 1.05, fill=NAVY, line=None, shadow=True)
    text(s, MX + 0.3, 2.88, 3.0, 0.3, "WORKSPACE UI", size=10.5, color=LAVA_LT, bold=True, font=FONT_SB)
    uis = ["Notebooks", "SQL Editor", "Jobs / Workflows", "Repos (Git)", "Dashboards / Genie"]
    uw = (CW - 0.6 - 4 * 0.18) / 5
    for i, u in enumerate(uis):
        x = MX + 0.3 + i * (uw + 0.18)
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 3.22, uw, 0.5, fill=NAVY_2, line=LINE_DK, line_w=1, adj=0.16)
        text(s, x + 0.04, 3.22, uw - 0.08, 0.5, u, size=9.6, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=0.9)
    shape(s, MSO_SHAPE.DOWN_ARROW, SW / 2 - 0.08, 3.9, 0.16, 0.18, fill=GRAY_LT, line=None)
    # Layer 3: compute
    card(s, MX, 4.2, CW, 0.95, fill=WHITE, line=LINE, shadow=True)
    text(s, MX + 0.3, 4.28, 3.0, 0.3, "COMPUTE", size=10.5, color=LAVA, bold=True, font=FONT_SB)
    comps = [("All-Purpose Clusters", BLUE), ("Job Clusters", LAVA), ("SQL Warehouses", PURPLE), ("Serverless", GREEN)]
    cwd = (CW - 0.6 - 3 * 0.2) / 4
    for i, (c, col) in enumerate(comps):
        x = MX + 0.3 + i * (cwd + 0.2)
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 4.6, cwd, 0.42, fill=OAT_2, line=col, line_w=1.5, adj=0.16)
        band(s, x, 4.6, 0.08, 0.42, col)
        text(s, x + 0.14, 4.6, cwd - 0.2, 0.42, c, size=10, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Layer 4: governance + storage
    gov = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 5.32, CW, 0.5, fill=NAVY, line=None, adj=0.2)
    icon(s, "lock", MX + 0.45, 5.57, 0.3, LAVA_LT)
    text(s, MX + 0.85, 5.32, CW - 1.0, 0.5,
         [[{"t": "Unity Catalog", "color": LAVA_LT, "size": 11.5, "bold": True},
           {"t": "  — unified governance, access control & lineage across every asset", "color": WHITE, "size": 11}]],
         anchor=MSO_ANCHOR.MIDDLE)
    found = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 5.92, CW, 0.5, fill=OAT_2, line=LINE, adj=0.2)
    icon(s, "cloud", MX + 0.45, 6.17, 0.3, BLUE)
    text(s, MX + 0.85, 5.92, CW - 1.0, 0.5,
         [[{"t": "Open Cloud Storage", "color": NAVY, "size": 11.5, "bold": True},
           {"t": "  — Delta Lake on S3 / ADLS / GCS  (your account, open formats)", "color": GRAY, "size": 11}]],
         anchor=MSO_ANCHOR.MIDDLE)
    footer(s)
    notes(s,
          "This is the mental model of how the Workspace is layered. At the top, every PERSONA uses the same "
          "environment. They interact through the WORKSPACE UI — notebooks, the SQL editor, Jobs/Workflows, "
          "Repos for Git, and dashboards/Genie. That UI drives COMPUTE: all-purpose clusters for interactive "
          "work, job clusters for production, SQL warehouses for BI, and serverless options. Everything is "
          "governed by UNITY CATALOG, and all data ultimately lives as Delta tables in the customer's own "
          "OPEN CLOUD STORAGE. Read it top-to-bottom: people → tools → compute → governance → storage. This "
          "mirrors the two-plane model from Day 1, viewed from the user's side.")


def d2_workspace_components(prs):
    s = slide(prs)
    header(s, "Workspace Components", "The Seven Building Blocks")
    section_progress(s, 1)
    items = [
        dict(icon="people", color=BLUE, title="Workspace",
             desc="The collaborative hub organizing all assets, folders & permissions."),
        dict(icon="doc", color=LAVA, title="Notebook",
             desc="Multi-language (Python/SQL/Scala/R) cells for code, viz & narrative."),
        dict(icon="cluster", color=TEAL, title="Cluster",
             desc="The Spark compute that notebooks and jobs attach to and run on."),
        dict(icon="flow", color=GREEN, title="Jobs / Workflows",
             desc="Schedule and orchestrate notebooks & tasks into production pipelines."),
        dict(icon="link", color=PURPLE, title="Repos",
             desc="Native Git integration for version control and CI/CD."),
        dict(icon="lock", color=YELLOW, title="Unity Catalog",
             desc="Central governance for data, ML models, files & permissions."),
        dict(icon="chart", color=TEAL, title="Dashboards",
             desc="AI/BI dashboards & Genie for SQL analytics and natural-language Q&A."),
    ]
    grid_cards(s, items, cols=4, x=MX, y=2.0, w=CW, h=4.45, gx=0.26, gy=0.28,
               icon_d=0.64, title_size=12.5, desc_size=9.6)
    footer(s)
    notes(s,
          "A quick tour of the seven components you'll use constantly. WORKSPACE is the container — folders, "
          "assets and permissions. NOTEBOOKS are where you write and run code in multiple languages with "
          "inline visualizations. CLUSTERS are the Spark compute that notebooks attach to. JOBS/WORKFLOWS turn "
          "notebooks into scheduled, orchestrated production pipelines. REPOS give native Git for version "
          "control and CI/CD. UNITY CATALOG governs all data and AI assets. DASHBOARDS (and Genie) deliver "
          "analytics and natural-language Q&A to business users. We'll zoom into the most important ones — "
          "notebook lifecycle, cluster types, Repos/Git and Unity Catalog — next.")


def d2_notebook_lifecycle(prs):
    s = slide(prs)
    header(s, "Workspace Components", "The Notebook Lifecycle")
    section_progress(s, 1)
    steps = [
        dict(title="Create", icon="doc", color=NAVY_2, badge=1,
             desc="New notebook; pick a default language & folder."),
        dict(title="Attach", icon="cluster", color=BLUE, badge=2,
             desc="Connect to a cluster or SQL warehouse for compute."),
        dict(title="Develop", icon="variety", color=TEAL, badge=3,
             desc="Mix Python, SQL, Scala, R & magic commands."),
        dict(title="Run & Visualize", icon="chart", color=LAVA, badge=4,
             desc="Execute cells; chart results inline; iterate fast."),
        dict(title="Version", icon="link", color=PURPLE, badge=5,
             desc="Commit to Git via Repos; review & branch."),
        dict(title="Operationalize", icon="flow", color=GREEN, badge=6,
             desc="Schedule as a Job or publish a dashboard."),
    ]
    flow_steps(s, steps, y_top=2.35, card_h=2.6, icon_d=0.92, arrow=True,
               title_size=12.5, desc_size=9.6, desc_dy=1.82)
    note_band(s, 5.3,
              [[{"t": "Exploration to production, in one artifact.  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "The same notebook you prototype in can be version-controlled and scheduled — no rewrite, "
                      "no hand-off to a different tool.", "color": GRAY, "size": 12.5}]], h=0.95)
    footer(s)
    notes(s,
          "Show the natural arc of a notebook from idea to production. You CREATE it and ATTACH it to compute. "
          "You DEVELOP interactively, mixing languages in the same notebook with magic commands like %sql or "
          "%python, and you RUN cells with inline visualizations to iterate quickly. When it's solid you "
          "VERSION it with Repos (Git) for review and collaboration, then OPERATIONALIZE it — schedule it as a "
          "Job or surface its output as a dashboard. The big idea: there's no painful 'productionization' "
          "rewrite — the artifact you explore in is the artifact you ship, which collapses the usual gap "
          "between data science and engineering.")


def d2_cluster_types(prs):
    s = slide(prs)
    header(s, "Workspace Components", "Cluster Types — Choosing Compute")
    section_progress(s, 1)
    rows = [
        ("Purpose", "Interactive development", "Automated production runs"),
        ("Lifecycle", "Long-running, manual start", "Created per job, auto-terminated"),
        ("Sharing", "Shared by a team", "Dedicated to one job"),
        ("Cost", "Higher — stays on", "Lower — runs only when needed"),
        ("Best For", "Notebooks, ad-hoc, EDA", "Scheduled ETL & pipelines"),
    ]
    vs_table(s, MX, 2.0, CW, ("Aspect", "All-Purpose Cluster", "Job Cluster"),
             rows, hcolors=(BLUE, LAVA))
    # bottom strip: SQL Warehouse & Serverless
    y = 5.55
    for i, (name, desc, col, ic) in enumerate([
            ("SQL Warehouse", "Photon-optimized compute for BI & SQL analytics", PURPLE, "chart"),
            ("Serverless", "Instant, fully-managed pools — zero infra to configure", GREEN, "cloud")]):
        x = MX + i * ((CW - 0.3) / 2 + 0.3)
        w = (CW - 0.3) / 2
        card(s, x, y, w, 0.92, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x + 0.5, y + 0.46, 0.58, ic, col, shadow=False)
        text(s, x + 0.95, y + 0.13, w - 1.1, 0.34, name, size=12.5, color=NAVY, bold=True)
        text(s, x + 0.95, y + 0.46, w - 1.1, 0.4, desc, size=10, color=GRAY_2, spacing=1.0)
    footer(s)
    notes(s,
          "The most important compute decision: all-purpose vs job clusters. ALL-PURPOSE clusters are "
          "long-running and shared — perfect for interactive development, exploration and collaboration, but "
          "they cost money whenever they're on (always set auto-termination). JOB clusters are created "
          "automatically for a scheduled job and torn down when it finishes — cheaper and isolated, ideal for "
          "production pipelines. The rule of thumb: develop on all-purpose, run production on job clusters. "
          "Then mention the two specialized options — SQL Warehouses (Photon-tuned for BI/SQL) and Serverless "
          "(instant startup, no infrastructure to manage). Cluster policies let admins standardize and control "
          "cost across all of these.")


def d2_repos_git(prs):
    s = slide(prs)
    header(s, "Workspace Components", "Repos & Git Integration")
    section_progress(s, 1)
    # two-box sync diagram
    card(s, MX, 2.05, 4.7, 1.55, fill=NAVY, line=None, shadow=True)
    icon_tile(s, MX + 0.6, 2.82, 0.7, "doc", LAVA, shadow=False)
    text(s, MX + 1.05, 2.42, 3.4, 0.4, "Databricks Repo", size=14, color=WHITE, bold=True)
    text(s, MX + 1.05, 2.82, 3.5, 0.6, "Notebooks & code, versioned inside the Workspace",
         size=10, color=RGBColor(0xC4, 0xD0, 0xD4), spacing=1.05)
    # sync arrows
    a1 = shape(s, MSO_SHAPE.RIGHT_ARROW, 5.55, 2.5, 1.55, 0.3, fill=GREEN, line=None)
    text(s, 5.5, 2.22, 1.7, 0.25, "commit · push", size=9, color=GREEN_DK, bold=True, align=PP_ALIGN.CENTER)
    a2 = shape(s, MSO_SHAPE.LEFT_ARROW, 5.55, 3.0, 1.55, 0.3, fill=BLUE, line=None)
    text(s, 5.5, 3.32, 1.7, 0.25, "pull · clone", size=9, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    card(s, 7.3, 2.05, CW + MX - 7.3, 1.55, fill=WHITE, line=LINE, shadow=True)
    icon_tile(s, 7.3 + 0.6, 2.82, 0.7, "link", NAVY_2, shadow=False)
    text(s, 7.3 + 1.05, 2.42, 3.8, 0.4, "Remote Git Provider", size=14, color=NAVY, bold=True)
    text(s, 7.3 + 1.05, 2.82, 4.0, 0.6, "GitHub · GitLab · Azure DevOps · Bitbucket",
         size=10, color=GRAY_2, spacing=1.05)
    # workflow strip
    text(s, MX, 4.0, CW, 0.3, "TYPICAL WORKFLOW", size=10.5, color=LAVA, bold=True, font=FONT_SB)
    flow = ["Clone", "Branch", "Edit in\nNotebooks", "Commit &\nPush", "Pull\nRequest", "Merge", "CI/CD\nDeploy"]
    fcols = [NAVY_2, BLUE, TEAL, LAVA, PURPLE, GREEN, GREEN_DK]
    n = len(flow); aw = 0.34
    bw = (CW - (n - 1) * aw) / n
    for i, (st, col) in enumerate(zip(flow, fcols)):
        x = MX + i * (bw + aw)
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 4.4, bw, 0.95, fill=WHITE, line=col, line_w=1.6, adj=0.1)
        band(s, x, 4.4, bw, 0.1, col)
        number_badge(s, x + 0.26, 4.62, 0.3, i + 1, fill=col, size=9)
        text(s, x + 0.04, 4.66, bw - 0.08, 0.62, st, size=10, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=0.9)
        if i < n - 1:
            arrow_h(s, x + bw + 0.02, 4.87, aw - 0.06, GRAY_LT, h=0.14)
    note_band(s, 5.65,
              [[{"t": "Engineering discipline, built in.  ", "color": NAVY, "size": 12, "bold": True},
                {"t": "Repos bring branches, pull requests and CI/CD to notebooks — so data pipelines are "
                      "reviewed, tested and deployed like any other software.", "color": GRAY, "size": 12}]], h=0.85)
    footer(s)
    notes(s,
          "Repos brings real software-engineering practices to data work. Picture two synced sides: your "
          "DATABRICKS REPO (notebooks and code versioned inside the Workspace) and a REMOTE GIT PROVIDER "
          "(GitHub, GitLab, Azure DevOps, Bitbucket). You commit and push changes out, and pull or clone "
          "changes in. The workflow strip is the everyday loop: clone the repo, create a feature branch, edit "
          "notebooks, commit and push, open a pull request for review, merge, and let CI/CD deploy to "
          "production. The takeaway: pipelines get the same rigor as application code — version history, peer "
          "review, automated testing and controlled releases — which is essential for reliable production "
          "data engineering.")


def d2_unity_catalog(prs):
    s = slide(prs)
    header(s, "Workspace Components", "Unity Catalog — Unified Governance")
    section_progress(s, 1)
    # left: namespace
    card(s, MX, 2.05, 5.3, 4.4, fill=WHITE, line=LINE, shadow=True)
    text(s, MX + 0.35, 2.26, 4.6, 0.3, "ONE NAMESPACE FOR EVERY ASSET", size=11, color=LAVA, bold=True, font=FONT_SB)
    levels = [("Catalog", BLUE, "top-level container"), ("Schema", TEAL, "database / namespace"),
              ("Table · View · Volume · Model", GREEN, "the governed asset")]
    for i, (name, col, sub) in enumerate(levels):
        y = 2.7 + i * 0.82
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.35 + i * 0.35, y, 4.5 - i * 0.35, 0.66,
              fill=col, line=None, adj=0.16)
        text(s, MX + 0.5 + i * 0.35, y, 4.2 - i * 0.35, 0.66,
             [[{"t": name, "color": WHITE, "size": 11.5, "bold": True},
               {"t": "   " + sub, "color": RGBColor(0xEA, 0xF2, 0xF0), "size": 8.5, "italic": True}]],
             anchor=MSO_ANCHOR.MIDDLE)
        if i < 2:
            shape(s, MSO_SHAPE.DOWN_ARROW, MX + 0.7 + i * 0.35, y + 0.66, 0.18, 0.16, fill=GRAY_LT, line=None)
    chip(s, MX + 0.35, 5.55, 4.6, 0.62, "catalog . schema . object", NAVY, LAVA_LT, size=13, radius=0.16)
    text(s, MX + 0.35, 6.2, 4.7, 0.3, "One name & permission across all clouds & workspaces",
         size=9.3, color=GRAY_2, italic=True)
    # right: pillars
    items = [
        dict(icon="lock", color=LAVA, title="Fine-Grained Access",
             desc="Row/column security via standard SQL GRANTs tied to SSO identity."),
        dict(icon="link", color=BLUE, title="Automated Lineage",
             desc="Column-level lineage & audit across notebooks, jobs & dashboards."),
        dict(icon="globe", color=GREEN, title="Discovery & Sharing",
             desc="Search, tags and open Delta Sharing across organizations."),
        dict(icon="ml", color=PURPLE, title="Data + AI Assets",
             desc="Governs tables, files, ML models & functions in one place."),
    ]
    grid_cards(s, items, cols=2, x=6.55, y=2.05, w=CW + MX - 6.55, h=4.4, gx=0.25, gy=0.25,
               icon_d=0.66, title_size=12.5, desc_size=10)
    footer(s)
    notes(s,
          "Unity Catalog is the single governance layer for the whole Workspace — and uniquely, it governs "
          "BOTH data and AI assets (tables, files/volumes, ML models, and functions) in one model. The "
          "three-level namespace catalog.schema.object gives every asset one consistent, governable name "
          "across all clouds and workspaces, replacing the old two-level hive metastore. Highlight the four "
          "pillars: fine-grained access control via standard SQL GRANTs tied to corporate SSO; automatic "
          "column-level lineage and audit; discovery plus open Delta Sharing; and unified governance of data "
          "and AI together. This is what lets large teams collaborate safely in a shared Workspace.")


def d2_workspace_best(prs):
    s = slide(prs)
    header(s, "Workspace Components", "Best Practices & Part 2 Takeaways")
    section_progress(s, 1)
    items = [
        dict(icon="link", color=LAVA, title="Version Everything",
             desc="Use Repos & Git for all notebooks — branches, reviews, CI/CD."),
        dict(icon="flow", color=BLUE, title="Job Clusters for Prod",
             desc="Run scheduled pipelines on ephemeral job clusters to cut cost."),
        dict(icon="gear", color=GREEN, title="Parametrize Notebooks",
             desc="Use widgets & job parameters to make code reusable and testable."),
        dict(icon="lock", color=TEAL, title="Govern with Unity Catalog",
             desc="Centralize permissions; grant least privilege, audit lineage."),
    ]
    grid_cards(s, items, cols=2, x=MX, y=2.0, w=7.35, h=4.45, gx=0.28, gy=0.28,
               icon_d=0.66, title_size=13, desc_size=10.3)
    card(s, 7.85, 2.0, CW + MX - 7.85, 4.45, fill=NAVY, line=None, shadow=True)
    band(s, 7.85, 2.0, CW + MX - 7.85, 0.6, LAVA)
    icon(s, "star", 7.85 + 0.42, 2.3, 0.34, WHITE)
    text(s, 7.85 + 0.82, 2.0, 4.0, 0.6, "KEY TAKEAWAYS", size=12.5, color=WHITE, bold=True,
         anchor=MSO_ANCHOR.MIDDLE, font=FONT_SB)
    bullets(s, 7.85 + 0.35, 2.85, CW + MX - 7.85 - 0.7, 3.5, [
        "Workspace = one collaborative, governed hub",
        "Notebooks span exploration → production",
        "All-purpose for dev, job clusters for prod",
        "Repos bring Git & CI/CD to data work",
        "Unity Catalog governs every data & AI asset",
    ], size=12, marker=LAVA_LT, color=RGBColor(0xD6, 0xDE, 0xE1), gap=12)
    footer(s)
    notes(s,
          "Wrap Part 2 with operating discipline and a recap. Best practices: version everything in Repos; run "
          "production on job clusters (and set auto-termination on interactive ones); parametrize notebooks "
          "with widgets so they're reusable and testable; and centralize permissions in Unity Catalog with "
          "least-privilege grants. Recap the five takeaways aloud. Bridge to Part 3: now that we know the "
          "engine (Spark) and the environment (Workspace), let's see how they assemble into the Lakehouse "
          "architecture that ties data, analytics and AI together.")


# ===========================================================================
#  PART 3 — DATABRICKS LAKEHOUSE ARCHITECTURE
# ===========================================================================
def d2_evolution(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "Evolution of Data Platforms")
    section_progress(s, 2)
    steps = [
        dict(title="Data Warehouse", icon="warehouse", color=BLUE, badge=1,
             desc="1980s+ · Structured, reliable SQL & BI — but rigid, costly and no ML."),
        dict(title="Data Lake", icon="lake", color=TEAL, badge=2,
             desc="2010s+ · Cheap, scalable, any data & ML — but unreliable & ungoverned."),
        dict(title="Lakehouse", icon="delta", color=LAVA, badge=3,
             desc="2020s+ · One open platform — lake economics + warehouse reliability."),
    ]
    n = 3
    cw = (CW - 2 * 0.55) / 3
    extra = ["Limitation: can't handle scale, unstructured data or ML",
             "Limitation: becomes a 'data swamp' — no ACID, weak governance",
             "Resolves both — reliable, governed, open & AI-ready"]
    for i, st in enumerate(steps):
        x = MX + i * (cw + 0.55)
        card(s, x, 2.25, cw, 2.65, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.25, cw, 0.85, st["color"])
        icon(s, st["icon"], x + 0.6, 2.66, 0.46, WHITE)
        text(s, x + 1.05, 2.25, cw - 1.1, 0.85, st["title"], size=15.5, color=WHITE,
             bold=True, anchor=MSO_ANCHOR.MIDDLE, spacing=0.9)
        text(s, x + 0.3, 3.25, cw - 0.6, 1.1, st["desc"], size=11.3, color=GRAY, spacing=1.18)
        col2 = GREEN_DK if i == 2 else LAVA
        text(s, x + 0.3, 4.32, cw - 0.6, 0.5,
             [[{"t": ("▸  " if i == 2 else "✕  "), "color": col2, "bold": True, "size": 11},
               {"t": extra[i], "color": GRAY_2, "size": 9.8, "italic": True}]], spacing=1.05)
        if i < n - 1:
            arrow_h(s, x + cw + 0.08, 3.55, 0.4, NAVY_2, h=0.26)
    note_band(s, 5.3,
              [[{"t": "Each generation fixed the last one's flaw.  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "The Lakehouse keeps the lake's low-cost openness and adds the warehouse's reliability "
                      "and performance — so you no longer need both.", "color": GRAY, "size": 12.5}]], h=0.95)
    footer(s)
    notes(s,
          "Tell the 40-year story as a sequence of trade-offs. The DATA WAREHOUSE (1980s onward) gave reliable, "
          "fast SQL and BI on structured data, but it's rigid, expensive to scale, and can't do ML or "
          "unstructured data. The DATA LAKE (2010s) flipped that — cheap, scalable storage for any data and "
          "great for ML — but with no transactions or governance it often degraded into a 'data swamp'. The "
          "LAKEHOUSE (2020s) resolves the dilemma: add a transactional, governed metadata layer (Delta Lake) "
          "on top of cheap open storage, so you get warehouse reliability AND lake flexibility in one place. "
          "That's why you no longer need to run and sync two separate systems.")


def d2_what_lakehouse(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "What Is the Lakehouse?")
    section_progress(s, 2)
    card(s, MX, 2.0, 6.55, 2.55, fill=NAVY, line=None, shadow=True)
    text(s, MX + 0.4, 2.28, 5.8, 0.3, "DEFINITION", size=11, color=LAVA_LT, bold=True, font=FONT_SB)
    text(s, MX + 0.4, 2.62, 5.85, 1.85,
         [[{"t": "A Lakehouse is a single platform that adds a ", "color": WHITE, "size": 14},
           {"t": "transactional, governed layer (Delta Lake)", "color": LAVA_LT, "size": 14, "bold": True},
           {"t": " directly on low-cost cloud object storage — delivering ", "color": WHITE, "size": 14},
           {"t": "warehouse reliability & performance with lake openness & scale", "color": LAVA_LT, "size": 14, "bold": True},
           {"t": " for every workload.", "color": WHITE, "size": 14}]], spacing=1.28)
    bullets(s, MX + 0.05, 4.85, 6.5, 1.8, [
        "One open copy of data — no warehouse/lake duplication",
        "ACID transactions & performance on cheap storage",
        "Serves BI, SQL, streaming, data science & AI together",
    ], size=12.5, marker=LAVA, gap=10)
    attrs = [("Open", "Delta & Parquet —\nno proprietary lock-in", BLUE),
             ("Reliable", "ACID transactions\n& schema enforcement", GREEN),
             ("Unified", "all workloads on\none copy of data", LAVA),
             ("Governed", "one security model\nvia Unity Catalog", PURPLE)]
    gx, gy = 0.3, 0.3
    tw, th = (4.55 - gx) / 2, (4.55 - gy) / 2
    x0 = 7.55
    for i, (big, lab, col) in enumerate(attrs):
        r, c = divmod(i, 2)
        x = x0 + c * (tw + gx); y = 2.0 + r * (th + gy)
        card(s, x, y, tw, th, fill=WHITE, line=LINE, shadow=True)
        band(s, x, y, 0.10, th, col)
        text(s, x + 0.28, y + 0.2, tw - 0.4, 0.5, big, size=19, color=col, bold=True)
        text(s, x + 0.30, y + 0.74, tw - 0.45, 0.9, lab.replace("\n", " "),
             size=10.5, color=GRAY, spacing=1.08)
    footer(s)
    notes(s,
          "Define the Lakehouse crisply for anyone who joined fresh on Day 2. The mechanism is the key idea: a "
          "transactional metadata layer — Delta Lake — sits directly on cheap cloud object storage, turning a "
          "folder of files into a reliable, governed table. That single move gives you warehouse-grade "
          "reliability and performance with lake-grade cost, openness and ML support. The four attribute tiles "
          "summarize the value: open (no lock-in), reliable (ACID), unified (all workloads, one copy of data), "
          "and governed (Unity Catalog). Everything else in Part 3 — medallion, Delta features, end-to-end "
          "flow — is just this definition made concrete.")


def d2_lakehouse_arch(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "Lakehouse Architecture — Layer by Layer")
    section_progress(s, 2)
    stages = [
        dict(title="Data\nSources", icon="globe", color=NAVY_2,
             examples=["Apps & DBs", "IoT / events", "Files & APIs"]),
        dict(title="Ingestion", icon="down", color=TEAL,
             examples=["Auto Loader", "Lakeflow", "Batch + stream"]),
        dict(title="Bronze", icon="database", color=BRONZE,
             examples=["Raw, as-is", "Full history", "Append-only"]),
        dict(title="Silver", icon="gear", color=SILVER,
             examples=["Cleansed", "Conformed", "Joined"]),
        dict(title="Gold", icon="diamond", color=GOLD,
             examples=["Aggregates", "Business KPIs", "ML features"]),
        dict(title="BI · AI · ML", icon="chart", color=PURPLE,
             examples=["Dashboards", "Genie / SQL", "ML & GenAI"]),
    ]
    pipeline(s, stages, y_top=2.4, box_h=1.0, ex_h=1.35, label_size=11, ex_size=9.8)
    # foundation underlay
    found = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 5.4, CW, 0.62, fill=NAVY, line=None, adj=0.2)
    icon(s, "delta", MX + 0.45, 5.71, 0.32, GREEN)
    text(s, MX + 0.85, 5.4, CW - 1.0, 0.62,
         [[{"t": "Delta Lake", "color": GREEN, "size": 11.5, "bold": True},
           {"t": "  open storage for every layer        ", "color": WHITE, "size": 11},
           {"t": "Unity Catalog", "color": LAVA_LT, "size": 11.5, "bold": True},
           {"t": "  governs the entire pipeline", "color": WHITE, "size": 11}]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, MX, 6.2, CW, 0.4,
         "Raw data flows left-to-right through Delta tables of rising quality — all open, all governed.",
         size=11.5, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "This is the reference architecture for the whole platform — and the diagram to memorize. Data flows "
          "left to right: SOURCES (apps, databases, IoT, files) are ingested by tools like Auto Loader and "
          "Lakeflow into the medallion layers — BRONZE (raw), SILVER (cleansed and conformed), GOLD (curated "
          "business aggregates and ML features) — and finally consumed by BI, AI and ML. The two foundations "
          "underneath are what make it a Lakehouse: every layer is a Delta Lake table in open storage, and "
          "Unity Catalog governs the entire pipeline end to end. Note this is the same six-stage ecosystem "
          "from Day 1, now realized as one platform. We'll zoom into the medallion next.")


def d2_medallion(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "The Medallion Architecture — In Detail")
    section_progress(s, 2)
    cols = [
        dict(name="Bronze", color=BRONZE, icon="database",
             rows=[("Data", "Raw, exactly as ingested"), ("Ops", "Append, capture metadata"),
                   ("Quality", "Unvalidated source of truth"), ("Users", "Data engineers")]),
        dict(name="Silver", color=SILVER, icon="gear",
             rows=[("Data", "Cleansed & conformed"), ("Ops", "Dedupe, validate, join"),
                   ("Quality", "Trusted, queryable"), ("Users", "Engineers & analysts")]),
        dict(name="Gold", color=GOLD, icon="diamond",
             rows=[("Data", "Curated & aggregated"), ("Ops", "Business logic, features"),
                   ("Quality", "Consumption-ready"), ("Users", "BI, ML & business")]),
    ]
    cw = (CW - 2 * 0.5) / 3
    for i, c in enumerate(cols):
        x = MX + i * (cw + 0.5)
        card(s, x, 2.15, cw, 3.55, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.15, cw, 0.72, c["color"])
        icon(s, c["icon"], x + 0.55, 2.51, 0.42, WHITE)
        text(s, x + 1.0, 2.15, cw - 1.05, 0.72, c["name"], size=17, color=WHITE, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        yy = 3.05
        for k, v in c["rows"]:
            text(s, x + 0.3, yy, cw - 0.55, 0.6,
                 [[{"t": k + "   ", "color": c["color"], "size": 9.5, "bold": True, "font": FONT_SB},
                   {"t": v, "color": GRAY, "size": 10.5}]], spacing=1.0)
            band(s, x + 0.3, yy + 0.58, cw - 0.6, 0.01, OAT_2)
            yy += 0.66
        if i < 2:
            arrow_h(s, x + cw + 0.05, 3.9, 0.4, LAVA, h=0.26)
    # quality gradient
    band(s, MX, 6.0, CW, 0.46, OAT_2)
    text(s, MX + 0.3, 6.0, 4, 0.46, "Quality & business value", size=10.5, color=NAVY,
         bold=True, anchor=MSO_ANCHOR.MIDDLE)
    gb = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 4.3, 6.09, 6.9, 0.26, fill=None, line=None, adj=0.5)
    grad(gb, BRONZE, GOLD, angle=0)
    shape(s, MSO_SHAPE.RIGHT_ARROW, 11.25, 6.07, 0.66, 0.3, fill=GOLD, line=None)
    footer(s)
    notes(s,
          "Now the detailed view of the medallion pattern, layer by layer. BRONZE is raw data exactly as "
          "ingested — appended with metadata, your replayable source of truth, owned by data engineers. SILVER "
          "is where the real work happens: deduplicate, validate, conform and join into trusted, queryable "
          "tables used by engineers and analysts. GOLD applies business logic and aggregation to produce "
          "consumption-ready tables and ML features for BI, ML and business users. Each hop raises data "
          "quality and business value, shown by the bronze-to-gold gradient. Because every layer is a Delta "
          "table, the whole pipeline is reliable and can run incrementally, even with streaming. This is the "
          "pattern that operationalizes the Lakehouse.")


def d2_delta_fundamentals(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "Delta Lake Fundamentals")
    section_progress(s, 2)
    steps = [
        dict(title="ACID\nTransactions", icon="check", color=GREEN, badge=1,
             desc="Reliable concurrent reads & writes — no corrupt or partial data."),
        dict(title="Time Travel", icon="down", color=BLUE, badge=2,
             desc="Query or roll back to any earlier version of the table."),
        dict(title="Schema\nEnforcement", icon="shield", color=YELLOW, badge=3,
             desc="Rejects bad data on write; supports safe schema evolution."),
        dict(title="Data\nVersioning", icon="delta", color=LAVA, badge=4,
             desc="Every commit is a version — full audit history & reproducibility."),
    ]
    flow_steps(s, steps, y_top=2.3, card_h=2.5, icon_d=1.0, arrow=False,
               title_size=13.5, desc_size=10.5, desc_dy=1.8)
    note_band(s, 5.2,
              [[{"t": "Under the hood:  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "a Delta table is just ", "color": GRAY, "size": 12.5},
                {"t": "Parquet data files + a JSON transaction log (_delta_log)", "color": LAVA, "size": 12.5, "bold": True},
                {"t": " — the log is what delivers all four guarantees, plus MERGE, OPTIMIZE & Z-ORDER.",
                 "color": GRAY, "size": 12.5}]], h=1.05)
    footer(s)
    notes(s,
          "Delta Lake is the open-storage layer that makes the Lakehouse possible — these four features are why. "
          "ACID TRANSACTIONS bring database reliability to the lake: concurrent writers can't corrupt the "
          "table. TIME TRAVEL lets you query or restore any previous version — invaluable for audits, "
          "debugging and reproducible ML. SCHEMA ENFORCEMENT rejects malformed data on write while still "
          "allowing controlled evolution. DATA VERSIONING means every change is a numbered version with full "
          "history. The mechanism (from Day 1) is worth repeating: a Delta table is Parquet files plus a JSON "
          "transaction log — that log is the magic that delivers all of this on top of cheap object storage, "
          "plus operations like MERGE (upserts), OPTIMIZE (compaction) and Z-ORDER (data skipping).")


def d2_delta_transaction(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "Delta Lake — Transaction Flow")
    section_progress(s, 2)
    # writer path (top)
    text(s, MX, 1.95, 6, 0.3, "WRITE PATH", size=10.5, color=LAVA, bold=True, font=FONT_SB)
    wsteps = [("Write\nrequest", "doc", NAVY_2), ("Validate\nschema", "shield", YELLOW),
              ("Write Parquet\ndata files", "cube", BLUE), ("Atomic commit\nto _delta_log", "check", GREEN)]
    n = len(wsteps); aw = 0.45
    bw = (CW - (n - 1) * aw) / n
    for i, (t, ic, col) in enumerate(wsteps):
        x = MX + i * (bw + aw)
        card(s, x, 2.28, bw, 1.05, fill=WHITE, line=LINE, shadow=True)
        icon_tile(s, x + 0.5, 2.8, 0.56, ic, col, shadow=False)
        text(s, x + 0.86, 2.32, bw - 0.95, 0.95, t, size=10.5, color=NAVY, bold=True,
             anchor=MSO_ANCHOR.MIDDLE, spacing=0.92)
        if i < n - 1:
            arrow_h(s, x + bw + 0.04, 2.8, aw - 0.08, LAVA, h=0.18)
    # transaction log in the middle
    log = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 3.7, CW, 1.15, fill=NAVY, line=None, adj=0.08)
    text(s, MX + 0.35, 3.82, 4.0, 0.3, "_delta_log/  (ordered JSON commits)", size=11,
         color=LAVA_LT, bold=True, font=FONT_SB)
    versions = ["v0  initial", "v1  +rows", "v2  update", "v3  merge", "v4  current"]
    vw = (CW - 0.7 - 4 * 0.2) / 5
    for i, v in enumerate(versions):
        x = MX + 0.35 + i * (vw + 0.2)
        cur = (i == len(versions) - 1)
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 4.18, vw, 0.5,
                   fill=(LAVA if cur else NAVY_2), line=(None if cur else LINE_DK), line_w=1, adj=0.18)
        text(s, x + 0.04, 4.18, vw - 0.08, 0.5, v, size=9.5, color=WHITE,
             bold=cur, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(versions) - 1:
            arrow_h(s, x + vw + 0.02, 4.43, 0.18, RGBColor(0x7E, 0x91, 0x99), h=0.12)
    # reader path (bottom)
    text(s, MX, 5.05, 6, 0.3, "READ PATH", size=10.5, color=GREEN_DK, bold=True, font=FONT_SB)
    card(s, MX, 5.35, CW, 1.05, fill=OAT_2, line=LINE, shadow=False)
    icon_tile(s, MX + 0.55, 5.87, 0.6, "people", GREEN, shadow=False)
    text(s, MX + 1.05, 5.35, CW - 1.4, 1.05,
         [[{"t": "Readers always see a consistent snapshot:  ", "color": NAVY, "size": 12, "bold": True},
           {"t": "Delta reads the log to serve the latest committed version (or any past version for time "
                 "travel) — never partial or dirty data, even while writes are in flight.",
            "color": GRAY, "size": 12}]], anchor=MSO_ANCHOR.MIDDLE, spacing=1.2)
    footer(s)
    notes(s,
          "This shows HOW Delta guarantees reliability — the transaction mechanism. WRITE PATH: a write request "
          "first validates against the table schema, then writes new Parquet data files, and finally makes an "
          "ATOMIC commit to the _delta_log. That commit is all-or-nothing — if it doesn't complete, the table "
          "is untouched, so there's never a half-written state. The _DELTA_LOG is an ordered series of JSON "
          "commits; each one is a new VERSION of the table (v0, v1, v2…), which is exactly what powers time "
          "travel. READ PATH: readers consult the log and always get a consistent snapshot of the latest "
          "committed version — or any historical version on request — even while writers are active. Delta "
          "uses optimistic concurrency control to manage simultaneous writers. This log-based design is the "
          "entire basis of ACID on object storage.")


def d2_governance(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "Governance & Open Sharing")
    section_progress(s, 2)
    items = [
        dict(icon="lock", color=LAVA, title="Centralized Access",
             desc="One permission model — ANSI SQL GRANTs with row & column security."),
        dict(icon="link", color=BLUE, title="Lineage & Audit",
             desc="Automatic column-level lineage and full audit logs for compliance."),
        dict(icon="globe", color=GREEN, title="Delta Sharing",
             desc="Open protocol to share live data across orgs — no copying, any client."),
        dict(icon="doc", color=TEAL, title="Discovery & Tags",
             desc="Search, tag and classify all assets in one governed catalog."),
        dict(icon="shield", color=PURPLE, title="Compliance Ready",
             desc="Encryption, network isolation and GDPR / HIPAA / SOC 2 controls."),
        dict(icon="ml", color=YELLOW, title="Data + AI Together",
             desc="Govern tables, files, ML models & features under one roof."),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=13.5, desc_size=10.5)
    footer(s)
    notes(s,
          "Governance is what turns a data lake into a trustworthy Lakehouse, and Unity Catalog provides it "
          "across the whole estate. Centralized access control uses standard SQL GRANTs down to rows and "
          "columns, tied to corporate identity. Lineage and audit are automatic and column-level — critical "
          "for compliance and impact analysis. Delta Sharing is a standout: an OPEN protocol to share live "
          "data with other organizations or tools without copying it, readable by any client (not just "
          "Databricks). Add discovery/tagging, enterprise compliance controls, and the unique ability to "
          "govern data and AI assets together. The theme for architects: one consistent governance model "
          "spanning every cloud, workspace and asset type.")


def d2_ai_ml(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "AI & ML on the Lakehouse")
    section_progress(s, 2)
    steps = [
        dict(title="Gold Data", icon="diamond", color=GOLD, badge=1,
             desc="Curated, governed features straight from the medallion."),
        dict(title="Feature\nEngineering", icon="gear", color=TEAL, badge=2,
             desc="Build & share features in the governed Feature Store."),
        dict(title="Train &\nTrack", icon="ml", color=BLUE, badge=3,
             desc="Experiment & tune with MLflow tracking and AutoML."),
        dict(title="Register", icon="lock", color=PURPLE, badge=4,
             desc="Version & stage models in the Unity Catalog registry."),
        dict(title="Serve &\nMonitor", icon="globe", color=LAVA, badge=5,
             desc="Real-time Model Serving with quality & drift monitoring."),
    ]
    flow_steps(s, steps, y_top=2.3, card_h=2.5, icon_d=0.96, arrow=True,
               title_size=12.5, desc_size=9.8, desc_dy=1.8)
    note_band(s, 5.2,
              [[{"t": "Mosaic AI:  ", "color": NAVY, "size": 12.5, "bold": True},
                {"t": "the full ML & GenAI lifecycle on governed data — MLflow, AutoML, Feature Store, "
                      "Model Serving, Vector Search and LLM fine-tuning, all under Unity Catalog.",
                 "color": GRAY, "size": 12.5}]], h=1.05)
    footer(s)
    notes(s,
          "A major payoff of the Lakehouse: ML and AI run on the SAME governed data as analytics — no separate "
          "ML data silo. Walk the lifecycle: start from GOLD data (governed features from the medallion), do "
          "FEATURE ENGINEERING in a shared Feature Store, TRAIN and track experiments with MLflow and AutoML, "
          "REGISTER versioned models in the Unity Catalog model registry, then SERVE them in real time with "
          "built-in monitoring for quality and drift. Databricks calls this Mosaic AI, and it now spans "
          "generative AI too — Vector Search for RAG, and LLM fine-tuning and serving — all governed by Unity "
          "Catalog. The key message: because models are built on governed Lakehouse data, you get lineage and "
          "security across the entire AI lifecycle, not just the data.")


def d2_end_to_end(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "End-to-End Data Pipeline")
    section_progress(s, 2)
    chip(s, MX, 1.95, 2.6, 0.4, "INGEST", TEAL, WHITE, size=10, radius=0.3)
    chip(s, MX + 2.78, 1.95, 5.0, 0.4, "TRANSFORM  ·  MEDALLION (Delta)", LAVA, WHITE, size=10, radius=0.3)
    chip(s, MX + 8.5, 1.95, 2.5, 0.4, "CONSUME", PURPLE, WHITE, size=10, radius=0.3)
    stages = [
        dict(t="Sources", sub="Apps · DBs · IoT\nfiles · events", icon="globe", col=NAVY_2),
        dict(t="Ingest", sub="Auto Loader\nLakeflow Connect", icon="down", col=TEAL),
        dict(t="Bronze", sub="Raw Delta\nappend-only", icon="database", col=BRONZE),
        dict(t="Silver", sub="Cleansed &\nconformed", icon="gear", col=SILVER),
        dict(t="Gold", sub="Aggregates &\nML features", icon="diamond", col=GOLD),
        dict(t="Consume", sub="BI · Genie\nML · GenAI · apps", icon="chart", col=PURPLE),
    ]
    n = len(stages)
    aw = 0.2
    cw = (CW - (n - 1) * aw) / n
    y = 2.6
    h = 2.5
    for i, st in enumerate(stages):
        x = MX + i * (cw + aw)
        card(s, x, y, cw, h, fill=WHITE, line=LINE, shadow=True)
        band(s, x, y, cw, 0.1, st["col"])
        icon_tile(s, x + cw / 2, y + 0.72, 0.82, st["icon"], st["col"], shadow=False)
        text(s, x + 0.04, y + 1.24, cw - 0.08, 0.4, st["t"], size=12, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER)
        text(s, x + 0.04, y + 1.64, cw - 0.08, 0.8, st["sub"], size=8.6, color=GRAY_2,
             align=PP_ALIGN.CENTER, spacing=1.0)
        number_badge(s, x + 0.26, y + 0.26, 0.34, i + 1, fill=st["col"], size=10)
        if i < n - 1:
            arrow_h(s, x + cw + 0.0, y + h / 2, aw, GRAY_LT, h=0.16)
    # orchestration + governance underlay
    gov = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 5.35, CW, 0.72, fill=NAVY, line=None, adj=0.2)
    icon(s, "flow", MX + 0.48, 5.71, 0.32, BLUE_LT)
    text(s, MX + 0.9, 5.35, CW - 1.1, 0.72,
         [[{"t": "Workflows", "color": BLUE_LT, "size": 11.5, "bold": True},
           {"t": "  orchestrate every step        ", "color": WHITE, "size": 11},
           {"t": "Unity Catalog", "color": LAVA_LT, "size": 11.5, "bold": True},
           {"t": "  governs data & AI end to end", "color": WHITE, "size": 11}]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, MX, 6.2, CW, 0.4,
         "Spark + Photon execute every stage · Delta stores it · Workflows run it · Unity Catalog governs it.",
         size=11.5, color=GRAY_2, italic=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s,
          "The capstone — everything from all three parts in one picture. Trace it left to right: raw SOURCES "
          "are INGESTED (Auto Loader, Lakeflow Connect) into BRONZE, refined to SILVER, curated to GOLD, and "
          "CONSUMED by BI, Genie, ML and GenAI apps. Underneath, the four pillars we learned: SPARK + PHOTON "
          "execute every stage (Part 1), the WORKSPACE Workflows orchestrate the pipeline (Part 2), DELTA LAKE "
          "stores each layer reliably, and UNITY CATALOG governs the whole thing (Part 3). This single diagram "
          "is how a real production data platform is built on Databricks — walk it slowly and connect each "
          "box back to what we covered today.")


def d2_benefits(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "Benefits of the Lakehouse")
    section_progress(s, 2)
    items = [
        dict(icon="hex", color=LAVA, title="Unified",
             desc="One platform for ETL, BI, streaming, data science & AI."),
        dict(icon="cube", color=BLUE, title="Open",
             desc="Delta & Parquet open formats on your storage — zero lock-in."),
        dict(icon="check", color=GREEN, title="Reliable",
             desc="ACID transactions and schema enforcement on the lake."),
        dict(icon="bolt", color=YELLOW, title="Performant",
             desc="Photon and Delta optimizations deliver warehouse-class speed."),
        dict(icon="lock", color=PURPLE, title="Governed",
             desc="One security & lineage model for all data and AI assets."),
        dict(icon="diamond", color=TEAL, title="Cost-Effective",
             desc="One copy of data, elastic compute — no duplicate systems."),
    ]
    grid_cards(s, items, cols=3, x=MX, y=2.0, w=CW, h=4.5, icon_d=0.72,
               title_size=14.5, desc_size=11)
    footer(s)
    notes(s,
          "Summarize why the Lakehouse matters in six leadership-friendly words. Unified eliminates tool "
          "sprawl; Open avoids lock-in and keeps data in your own account; Reliable brings ACID guarantees to "
          "cheap storage; Performant means you don't sacrifice speed for openness (Photon + Delta); Governed "
          "gives one consistent security and lineage model for data AND AI; and Cost-Effective comes from "
          "keeping a single copy of data with elastic compute instead of running and syncing separate "
          "warehouse and lake systems. If asked for the one-line ROI: consolidation plus faster, governed "
          "delivery of analytics and AI.")


def d2_realworld(prs):
    s = slide(prs)
    header(s, "Lakehouse Architecture", "Real-World Example — Omni-Channel Retailer")
    section_progress(s, 2)
    # left: scenario flow
    card(s, MX, 2.05, 6.7, 4.4, fill=WHITE, line=LINE, shadow=True)
    text(s, MX + 0.35, 2.24, 6.0, 0.3, "THE PIPELINE", size=11, color=LAVA, bold=True, font=FONT_SB)
    flow = [("POS · Web · Mobile · Inventory feeds", NAVY_2, "globe"),
            ("Auto Loader ingests streams + batch", TEAL, "down"),
            ("Bronze → Silver → Gold (Delta)", LAVA, "delta"),
            ("Genie BI · personalization ML · GenAI", PURPLE, "chart")]
    for i, (t, col, ic) in enumerate(flow):
        y = 2.66 + i * 0.86
        sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX + 0.35, y, 6.0, 0.66, fill=OAT_2, line=col, line_w=1.4, adj=0.14)
        band(s, MX + 0.35, y, 0.09, 0.66, col)
        icon_tile(s, MX + 0.85, y + 0.33, 0.46, ic, col, shadow=False)
        text(s, MX + 1.25, y, 5.0, 0.66, t, size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(flow) - 1:
            shape(s, MSO_SHAPE.DOWN_ARROW, MX + 1.0, y + 0.66, 0.16, 0.16, fill=GRAY_LT, line=None)
    # right: outcomes
    text(s, 7.5, 2.24, 5.0, 0.3, "THE OUTCOMES", size=11, color=GREEN_DK, bold=True, font=FONT_SB)
    kpis = [("10x", "faster pipelines vs the\nlegacy warehouse + lake", LAVA),
            ("Real-time", "personalization &\ninventory visibility", BLUE),
            ("1 copy", "of governed data for\nBI, ML and GenAI", GREEN),
            ("~50%", "lower total cost of\nownership", PURPLE)]
    gx, gy = 0.28, 0.26
    tw, th = (CW + MX - 7.5 - gx) / 2, (4.4 - 0.45 - gy) / 2
    for i, (big, lab, col) in enumerate(kpis):
        r, c = divmod(i, 2)
        x = 7.5 + c * (tw + gx); y = 2.66 + r * (th + gy)
        card(s, x, y, tw, th, fill=WHITE, line=LINE, shadow=True)
        band(s, x, y, 0.1, th, col)
        text(s, x + 0.26, y + 0.16, tw - 0.4, 0.5, big, size=20, color=col, bold=True)
        text(s, x + 0.28, y + 0.66, tw - 0.45, 0.9, lab.replace("\n", " "), size=10, color=GRAY, spacing=1.05)
    footer(s)
    notes(s,
          "Ground the architecture in a believable scenario — an omni-channel retailer (representative of many "
          "real Databricks customers). The PIPELINE: point-of-sale, web, mobile and inventory feeds stream in "
          "via Auto Loader, flow through Bronze→Silver→Gold Delta tables, and surface as Genie BI, a "
          "personalization model, and GenAI assistants — all on one platform. The OUTCOMES are the kinds of "
          "results these projects report: roughly an order-of-magnitude faster pipelines than a stitched "
          "warehouse-plus-lake setup, genuine real-time personalization and inventory visibility, a single "
          "governed copy of data serving BI/ML/GenAI, and substantially lower total cost of ownership. Present "
          "the figures as representative outcomes, and invite the audience to map their own use case onto this "
          "shape.")


def d2_summary(prs):
    s = slide(prs)
    header(s, "Wrap-Up", "Day 2 — Key Takeaways")
    cols = [
        dict(no="1", color=BLUE, title="Apache Spark", points=[
            "Unified, in-memory, distributed engine",
            "Driver → Cluster Mgr → Executors → Tasks",
            "Lazy DAG; one core for SQL/stream/ML"]),
        dict(no="2", color=LAVA, title="Workspace", points=[
            "One collaborative, governed hub",
            "Notebooks: exploration → production",
            "Repos + Git; Unity Catalog governance"]),
        dict(no="3", color=GREEN, title="Lakehouse", points=[
            "Delta + medallion = trusted data",
            "ACID, time travel on open storage",
            "Governed BI, ML & GenAI, end to end"]),
    ]
    cw = (CW - 2 * 0.35) / 3
    for i, c in enumerate(cols):
        x = MX + i * (cw + 0.35)
        card(s, x, 2.0, cw, 2.8, fill=WHITE, line=LINE, shadow=True)
        band(s, x, 2.0, cw, 0.12, c["color"])
        number_badge(s, x + 0.55, 2.6, 0.66, c["no"], fill=c["color"], size=18)
        text(s, x + 1.05, 2.3, cw - 1.2, 0.6, c["title"], size=14.5, color=NAVY, bold=True,
             anchor=MSO_ANCHOR.MIDDLE, spacing=0.95)
        bullets(s, x + 0.32, 3.18, cw - 0.6, 1.5, c["points"], size=11.3, marker=c["color"], gap=9)
    hw = (CW - 0.3) / 2
    takeaway(s, MX, 4.98, hw, "Spark is the engine; Databricks makes it effortless and fast (Photon).",
             color=LAVA, icon_kind="bolt")
    takeaway(s, MX + hw + 0.3, 4.98, hw,
             "The Workspace unifies notebooks, compute, Git and governance in one hub.",
             color=BLUE, icon_kind="people")
    takeaway(s, MX, 5.88, hw, "Delta Lake + medallion turn raw files into reliable, governed tables.",
             color=GREEN, icon_kind="delta")
    takeaway(s, MX + hw + 0.3, 5.88, hw,
             "One platform, one governed copy of data — for analytics and AI alike.",
             color=PURPLE, icon_kind="star")
    footer(s)
    notes(s,
          "Tie the whole day together. Three pillars: the ENGINE (Spark — unified, in-memory, driver/executor "
          "model, lazy DAG), the ENVIRONMENT (Workspace — collaborative hub, notebooks from exploration to "
          "production, Repos and Unity Catalog), and the ARCHITECTURE (Lakehouse — Delta + medallion, ACID and "
          "time travel on open storage, governed analytics and AI end to end). Quiz the room on the four "
          "takeaways. If they can explain how a query runs on Spark, navigate the Workspace, and sketch a "
          "medallion pipeline, Day 2 succeeded. Move to Q&A and the close.")


def d2_thanks(prs):
    s = slide(prs, bg=NAVY)
    dark_bg(s)
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, MX, 2.2, 0.09, 1.5, fill=LAVA, line=None, adj=0.5)
    text(s, MX + 0.3, 2.1, 10, 1.1, "Thank You", size=54, color=WHITE, bold=True)
    text(s, MX + 0.32, 3.3, 10.6, 0.6,
         "Day 2 complete — you can now read the engine, the workspace and the Lakehouse architecture end to end.",
         size=15, color=RGBColor(0xC4, 0xD0, 0xD4), spacing=1.2)
    text(s, MX + 0.32, 4.25, 8, 0.3, "KEEP BUILDING", size=11.5, color=LAVA_LT, bold=True, font=FONT_SB)
    res = ["docs.databricks.com", "Databricks Academy", "Free Edition — hands-on", "Delta Lake & Spark docs"]
    cx = MX + 0.32
    for r in res:
        w = 0.32 + len(r) * 0.105
        chip(s, cx, 4.62, w, 0.52, r, NAVY_2, WHITE, size=11, radius=0.5, line=LINE_DK)
        cx += w + 0.22
    recap = [("Spark", "bolt", BLUE), ("Workspace", "doc", LAVA), ("Clusters", "cluster", TEAL),
             ("Delta", "delta", GREEN), ("Medallion", "diamond", GOLD), ("Unity Catalog", "lock", PURPLE)]
    cx = MX + 0.32
    for name, ic, col in recap:
        icon_tile(s, cx + 0.4, 5.85, 0.78, ic, col, shadow=True)
        text(s, cx - 0.1, 6.34, 1.0, 0.4, name, size=9.5, color=RGBColor(0xC4, 0xD0, 0xD4),
             align=PP_ALIGN.CENTER, spacing=0.9)
        cx += 1.15
    text(s, 8.7, 6.55, CW + MX - 8.7, 0.3, "Next: hands-on lab & Delta Live Tables",
         size=12, color=GRAY_LT, italic=True, align=PP_ALIGN.RIGHT)
    notes(s,
          "Congratulate the group on completing Day 2 and recap the six icons — Spark, Workspace, Clusters, "
          "Delta, Medallion and Unity Catalog. Point to hands-on resources: the docs, Databricks Academy "
          "(free role-based learning and certifications) and the free edition for practice. Preview the next "
          "session — a hands-on lab building a medallion pipeline, plus Delta Live Tables / Lakeflow "
          "Declarative Pipelines and Workflows orchestration. Open the floor for questions.")


# ===========================================================================
#  ASSEMBLE
# ===========================================================================
def main():
    prs = new_deck()
    prs.core_properties.title = "Databricks Day 2 — Spark, Workspace & Lakehouse"
    prs.core_properties.subject = "Apache Spark Fundamentals · Workspace Components · Lakehouse Architecture"

    d2_cover(prs)
    d2_agenda(prs)
    # Part 1 — Spark
    s_divider(prs, "01", "Part One", "Apache Spark Fundamentals",
              ["What & why Spark · architecture & components",
               "Execution flow · Spark vs Hadoop",
               "Use cases & best practices"], "bolt", color=LAVA)
    d2_what_spark(prs)
    d2_why_spark(prs)
    d2_spark_arch(prs)
    d2_spark_components(prs)
    d2_spark_execution(prs)
    d2_spark_vs_hadoop(prs)
    d2_spark_usecases(prs)
    d2_spark_best(prs)
    # Part 2 — Workspace
    s_divider(prs, "02", "Part Two", "Databricks Workspace Components",
              ["Workspace, notebooks & architecture",
               "Clusters, jobs & Git integration",
               "Unity Catalog & best practices"], "doc", color=LAVA)
    d2_workspace_overview(prs)
    d2_workspace_arch(prs)
    d2_workspace_components(prs)
    d2_notebook_lifecycle(prs)
    d2_cluster_types(prs)
    d2_repos_git(prs)
    d2_unity_catalog(prs)
    d2_workspace_best(prs)
    # Part 3 — Lakehouse
    s_divider(prs, "03", "Part Three", "Databricks Lakehouse Architecture",
              ["Evolution · Lakehouse & Delta Lake",
               "Medallion · governance · AI & ML",
               "End-to-end pipeline & benefits"], "delta", color=LAVA)
    d2_evolution(prs)
    d2_what_lakehouse(prs)
    d2_lakehouse_arch(prs)
    d2_medallion(prs)
    d2_delta_fundamentals(prs)
    d2_delta_transaction(prs)
    d2_governance(prs)
    d2_ai_ml(prs)
    d2_end_to_end(prs)
    d2_benefits(prs)
    d2_realworld(prs)
    # Wrap-up
    d2_summary(prs)
    d2_thanks(prs)

    prs.save(OUT)
    print(f"Saved {OUT} with {len(prs.slides._sldIdLst)} slides")


if __name__ == "__main__":
    main()

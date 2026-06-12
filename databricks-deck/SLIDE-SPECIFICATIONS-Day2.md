# Databricks Day 2 — Slide Specifications & Facilitator Guide

_Spark, Workspace & Lakehouse · Enterprise Data Platform Training Series_

This document specifies every slide in **Databricks-Day2-Spark-Workspace-Lakehouse.pptx** using the design format below. Speaker notes are extracted directly from the deck, so they always match what a presenter sees in PowerPoint's notes pane.

> **Format:** Objective · Content · Visual Layout · Diagram · Speaker Notes · Design Tips


---

### Slide 1: Title / Cover

**Objective:** Open Day 2 and frame the three pillars: engine, environment, architecture.

**Content:** Course title, subtitle, three part-chips, audience and a 'builds on Day 1' note.

**Visual Layout:** Dark navy gradient cover with lava accent bar, oversized title and part chips.

**Diagram:** —

**Speaker Notes:** Welcome back for Day 2. Day 1 covered the 'what and why' — Big Data, the Lakehouse concept and a high-level platform tour. Day 2 is the 'how': we go deep on the three pillars an engineer touches every day. Part 1 opens up Apache Spark — the distributed engine under everything. Part 2 is a working tour of the Databricks Workspace — notebooks, clusters, jobs, repos and governance. Part 3 assembles it all into the Lakehouse architecture, from Delta Lake to the medallion pattern to an end-to-end pipeline. By the end, attendees can read an architecture diagram and explain how a query becomes a governed dashboard.

**Design Tips:** Mirror Day 1's cover system — navy + lava, bold title, lava subtitle.


---

### Slide 2: Day 2 Roadmap — What We'll Build Today

**Objective:** Preview the three parts and the outcome of each.

**Content:** Three part cards (Spark, Workspace, Lakehouse) with topics and outcomes.

**Visual Layout:** Three colored cards with icon badges, topic bullets and an OUTCOME line.

**Diagram:** Three-column roadmap (Part 01 / 02 / 03).

**Speaker Notes:** Set the map for the day. Three parts, each answering a practical question: Part 1 — how does the engine actually run my code? Part 2 — where and how do I do my work? Part 3 — how does it all fit together into a production architecture? Tell learners each part ends with best practices and a summary, and that the day culminates in a single end-to-end pipeline diagram that uses everything we covered. No deep prior Spark knowledge required.

**Design Tips:** Color-code parts blue / lava / green; four topics each.


---


## Part 1 · Apache Spark Fundamentals

### Slide 3: Part 01 Divider — Apache Spark Fundamentals

**Objective:** Transition into the Spark deep-dive.

**Content:** Part number, title and three covered themes.

**Visual Layout:** Navy divider with a giant '01' watermark and a lightning icon.

**Diagram:** —

**Speaker Notes:** Section 01: Apache Spark Fundamentals. Transition slide — pause, then preview the four ideas listed. Use it to re-anchor the narrative and tell the audience what they'll be able to do by the end of this section.

**Design Tips:** Reuse the shared divider system across all three parts.


---

### Slide 4: What Is Apache Spark?

**Objective:** Define Spark precisely and make its scale tangible.

**Content:** Definition card, three clarifying bullets and four headline stats.

**Visual Layout:** Navy definition card + 2x2 stat tiles (100x, 4 langs, 2009, 1000s).

**Diagram:** —

**Speaker Notes:** Define Spark precisely: a unified, distributed, in-memory engine. The two words that matter most are 'unified' (one engine for batch, streaming, SQL, ML and graph — versus the old world of a different tool per workload) and 'in-memory' (it keeps working data in RAM across the cluster rather than writing to disk between steps, which is why it's up to 100x faster than Hadoop MapReduce for iterative work). Spark came out of UC Berkeley's AMPLab in 2009 — the same team that founded Databricks. Emphasise that everything in Databricks ultimately runs on Spark.

**Design Tips:** Stress 'unified' and 'in-memory'; let the stats carry the right side.


---

### Slide 5: Why Spark Won

**Objective:** Explain the advantages that displaced Hadoop MapReduce.

**Content:** Six benefits: speed, unified engine, easy APIs, scalability, fault tolerance, ecosystem.

**Visual Layout:** 2x3 card grid with icons.

**Diagram:** —

**Speaker Notes:** Frame these as the reasons Spark displaced Hadoop MapReduce as the default big-data engine. Speed and the unified model are the headline wins, but ease of use was just as important — DataFrames and SQL let analysts and engineers be productive without writing low-level Java. Fault tolerance comes 'for free' from lineage: because Spark knows the DAG that produced each dataset, it can recompute just the lost pieces if a node fails. Tie the last card forward: this ecosystem and engine are exactly what Databricks productized and made effortless to run.

**Design Tips:** Tie the last card forward — Spark is the engine Databricks productized.


---

### Slide 6: Spark Architecture

**Objective:** Teach the master/worker execution model.

**Content:** Driver, Cluster Manager, Executors and Tasks, with a 'how it runs' note.

**Visual Layout:** Four-step icon carousel with numbered badges and a summary band.

**Diagram:** Driver → Cluster Manager → Executors → Tasks.

**Speaker Notes:** Walk the four-part chain left to right. The DRIVER is the brain — it hosts the SparkSession, translates your code into a logical plan, optimizes it into a DAG of stages, and schedules tasks. The CLUSTER MANAGER is the resource broker (Standalone, YARN, Kubernetes, or Databricks' own). EXECUTORS are JVM worker processes that actually run computation and cache data in memory. TASKS are the atoms of work — each one processes a single partition, and they run simultaneously across executors, which is where the parallelism (and the speed) comes from. Analogy: the driver is the head chef writing the plan; executors are line cooks; tasks are individual dishes cooked at once. Reassure them Databricks provisions and tunes all of this automatically.

**Design Tips:** Chef / line-cooks analogy; note Databricks manages it all.


---

### Slide 7: Spark's Unified Component Stack

**Objective:** Show that Spark is one core engine with specialized libraries.

**Content:** Spark SQL, DataFrames, Structured Streaming, MLlib, GraphX.

**Visual Layout:** Five-card carousel over a 'one engine, one core' note band.

**Diagram:** Spark SQL · DataFrames · Structured Streaming · MLlib · GraphX (on Spark Core).

**Speaker Notes:** Spark is not five separate products — it's one core engine with specialized libraries on top, all sharing the same execution model. SPARK SQL brings ANSI SQL and the Catalyst query optimizer. DATAFRAMES are the high-level, optimized API most people use daily (think distributed tables). STRUCTURED STREAMING lets you write streaming pipelines with the exact same DataFrame code as batch — a huge simplification. MLLIB provides distributed machine learning. GRAPHX handles graph analytics. The key teaching point: because they share a core, you can combine them in one job — e.g., stream data in, transform with SQL, score with an ML model — and on Databricks the Photon engine accelerates it all.

**Design Tips:** One color per library; emphasise mixing them in one pipeline.


---

### Slide 8: Spark Execution Flow

**Objective:** Explain lazy evaluation and how a query becomes parallel work.

**Content:** Code/Query → DAG → Stages → Tasks → Results, plus a lazy-evaluation note.

**Visual Layout:** Five-step icon carousel with arrows.

**Diagram:** Query → DAG → Stages → Tasks → Results.

**Speaker Notes:** This explains the single most misunderstood part of Spark: lazy evaluation. When you write transformations (filter, join, select) Spark does NOT execute them — it just records them, building a logical plan. The Catalyst optimizer turns that into an optimized DAG. The DAG is divided into STAGES at shuffle boundaries (points where data must move across the network). Each stage becomes a set of TASKS, one per partition, run in parallel by executors. Only when you call an ACTION (count, show, write, collect) does the whole thing actually run. Why this matters: laziness lets Spark see the entire computation and optimize it globally — reordering filters, pruning columns, minimizing shuffles — before doing any work.

**Design Tips:** Highlight that nothing runs until an action fires.


---

### Slide 9: Spark vs. Hadoop MapReduce

**Objective:** Contrast the two engines to crystallize Spark's advantages.

**Content:** Seven-row comparison across processing, speed, programming, workloads, real-time, ML, fault tolerance.

**Visual Layout:** Three-column comparison table with header chips and zebra striping.

**Diagram:** Comparison table (Aspect | Hadoop MapReduce | Apache Spark).

**Speaker Notes:** Use this to make Spark's advantages concrete. The crux is the Processing row: MapReduce writes intermediate results to disk between every map and reduce step, while Spark keeps them in memory — that's the source of the dramatic speedup, especially for iterative algorithms like ML training that loop over the same data. Spark is also far easier to program (DataFrames/SQL vs hand-written Java) and handles many workloads in one engine, including streaming, which MapReduce can't do. Be fair: Hadoop's HDFS is still a valid storage layer, and Spark can run on it — Spark replaced the MapReduce compute model, not the whole ecosystem. On Databricks you rarely manage either directly.

**Design Tips:** The Processing row (in-memory vs disk) is the crux of the speedup.


---

### Slide 10: What Teams Build with Spark

**Objective:** Make Spark tangible through real workloads.

**Content:** Six use cases: ETL, streaming, ML, SQL/BI, graph, data-lake processing.

**Visual Layout:** 2x3 card grid with icons.

**Diagram:** —

**Speaker Notes:** Make Spark tangible by tying each workload to outcomes the audience recognizes. ETL is the bread and butter — most Spark jobs in production are pipelines turning raw data into clean tables. Streaming powers real-time use cases like fraud detection. ML and SQL/BI show the unified-engine payoff: the same platform trains models and serves analysts. Land the last card — when we get to the Lakehouse, remember that Delta Lake and the medallion pipelines you'll see are all executed by Spark under the hood.

**Design Tips:** Land the last card — Delta & medallion pipelines run on Spark.


---


## Part 2 · Databricks Workspace Components

### Slide 11: Best Practices & Part 1 Takeaways

**Objective:** Give practical tuning guidance and recap Part 1.

**Content:** Four best practices and a five-point takeaways panel.

**Visual Layout:** 2x2 best-practice grid beside a navy takeaways panel.

**Diagram:** —

**Speaker Notes:** Close Part 1 with practical guidance and a recap. Best practices, briefly: prefer the DataFrame/SQL APIs so Catalyst and Photon can optimize for you; size partitions sensibly and watch for skew (one giant partition stalls the whole stage); minimize shuffles because moving data across the network is the main cost — filter early and broadcast small lookup tables; and cache datasets you reuse. Then recap the five takeaways aloud and check understanding before moving to the Workspace. Reassure them Databricks automates most tuning, but understanding these concepts helps them write efficient code and debug slow jobs.

**Design Tips:** Reassure that Databricks automates most tuning (Photon).


---

### Slide 12: Part 02 Divider — Databricks Workspace Components

**Objective:** Transition into the Workspace tour.

**Content:** Part number, title and three covered themes.

**Visual Layout:** Navy divider with a giant '02' watermark and a notebook icon.

**Diagram:** —

**Speaker Notes:** Section 02: Databricks Workspace Components. Transition slide — pause, then preview the four ideas listed. Use it to re-anchor the narrative and tell the audience what they'll be able to do by the end of this section.

**Design Tips:** Consistent divider system.


---

### Slide 13: The Databricks Workspace

**Objective:** Define the Workspace as the unified, collaborative hub.

**Content:** Definition card, four attribute cards and a 'one place for everyone' note.

**Visual Layout:** Navy definition card + vertical stack of four cards + note band.

**Diagram:** —

**Speaker Notes:** Introduce the Workspace as the 'home base' of Databricks — the web UI where all work happens. The key value is consolidation and collaboration: instead of one tool for notebooks, another for scheduling, another for Git, another for governance, it's all one environment in the browser, on any cloud. Stress that the same place spans the full lifecycle — interactive exploration through to production jobs — and that everything is governed by Unity Catalog. Over the next slides we'll tour each component.

**Design Tips:** Stress consolidation and collaboration across personas.


---

### Slide 14: Workspace Architecture

**Objective:** Show how the Workspace is layered from users to storage.

**Content:** Personas → Workspace UI → Compute → Unity Catalog → Cloud storage.

**Visual Layout:** Stacked horizontal bands with component chips and connecting arrows.

**Diagram:** Users ↓ Workspace UI ↓ Compute ↓ Unity Catalog ↓ Open cloud storage.

**Speaker Notes:** This is the mental model of how the Workspace is layered. At the top, every PERSONA uses the same environment. They interact through the WORKSPACE UI — notebooks, the SQL editor, Jobs/Workflows, Repos for Git, and dashboards/Genie. That UI drives COMPUTE: all-purpose clusters for interactive work, job clusters for production, SQL warehouses for BI, and serverless options. Everything is governed by UNITY CATALOG, and all data ultimately lives as Delta tables in the customer's own OPEN CLOUD STORAGE. Read it top-to-bottom: people → tools → compute → governance → storage. This mirrors the two-plane model from Day 1, viewed from the user's side.

**Design Tips:** Read top-to-bottom; mirrors Day 1's two-plane model from the user side.


---

### Slide 15: The Seven Building Blocks

**Objective:** Tour the seven components used daily.

**Content:** Workspace, Notebook, Cluster, Jobs, Repos, Unity Catalog, Dashboards.

**Visual Layout:** Four-column card grid (7 cards) with icons.

**Diagram:** —

**Speaker Notes:** A quick tour of the seven components you'll use constantly. WORKSPACE is the container — folders, assets and permissions. NOTEBOOKS are where you write and run code in multiple languages with inline visualizations. CLUSTERS are the Spark compute that notebooks attach to. JOBS/WORKFLOWS turn notebooks into scheduled, orchestrated production pipelines. REPOS give native Git for version control and CI/CD. UNITY CATALOG governs all data and AI assets. DASHBOARDS (and Genie) deliver analytics and natural-language Q&A to business users. We'll zoom into the most important ones — notebook lifecycle, cluster types, Repos/Git and Unity Catalog — next.

**Design Tips:** Preview that notebooks, clusters, Repos and Unity Catalog get deep dives.


---

### Slide 16: The Notebook Lifecycle

**Objective:** Show a notebook's arc from idea to production.

**Content:** Create → Attach → Develop → Run & Visualize → Version → Operationalize.

**Visual Layout:** Six-step icon carousel with arrows and a note band.

**Diagram:** Create → Attach → Develop → Run → Version → Operationalize.

**Speaker Notes:** Show the natural arc of a notebook from idea to production. You CREATE it and ATTACH it to compute. You DEVELOP interactively, mixing languages in the same notebook with magic commands like %sql or %python, and you RUN cells with inline visualizations to iterate quickly. When it's solid you VERSION it with Repos (Git) for review and collaboration, then OPERATIONALIZE it — schedule it as a Job or surface its output as a dashboard. The big idea: there's no painful 'productionization' rewrite — the artifact you explore in is the artifact you ship, which collapses the usual gap between data science and engineering.

**Design Tips:** Key point: no productionization rewrite — same artifact ships.


---

### Slide 17: Cluster Types — Choosing Compute

**Objective:** Explain all-purpose vs job clusters and the specialized options.

**Content:** Five-aspect comparison plus SQL Warehouse and Serverless cards.

**Visual Layout:** Comparison table over two highlight cards.

**Diagram:** Comparison table (Aspect | All-Purpose | Job Cluster).

**Speaker Notes:** The most important compute decision: all-purpose vs job clusters. ALL-PURPOSE clusters are long-running and shared — perfect for interactive development, exploration and collaboration, but they cost money whenever they're on (always set auto-termination). JOB clusters are created automatically for a scheduled job and torn down when it finishes — cheaper and isolated, ideal for production pipelines. The rule of thumb: develop on all-purpose, run production on job clusters. Then mention the two specialized options — SQL Warehouses (Photon-tuned for BI/SQL) and Serverless (instant startup, no infrastructure to manage). Cluster policies let admins standardize and control cost across all of these.

**Design Tips:** Rule of thumb: develop on all-purpose, run prod on job clusters.


---

### Slide 18: Repos & Git Integration

**Objective:** Bring software-engineering discipline to data work.

**Content:** Databricks Repo ↔ remote Git, plus the clone→…→deploy workflow.

**Visual Layout:** Two synced boxes with bidirectional arrows over a 7-step workflow strip.

**Diagram:** Databricks Repo ⇄ Remote Git; Clone → Branch → Commit → Push → PR → Merge → CI/CD.

**Speaker Notes:** Repos brings real software-engineering practices to data work. Picture two synced sides: your DATABRICKS REPO (notebooks and code versioned inside the Workspace) and a REMOTE GIT PROVIDER (GitHub, GitLab, Azure DevOps, Bitbucket). You commit and push changes out, and pull or clone changes in. The workflow strip is the everyday loop: clone the repo, create a feature branch, edit notebooks, commit and push, open a pull request for review, merge, and let CI/CD deploy to production. The takeaway: pipelines get the same rigor as application code — version history, peer review, automated testing and controlled releases — which is essential for reliable production data engineering.

**Design Tips:** Message: pipelines get version control, review and CI/CD.


---


## Part 3 · Databricks Lakehouse Architecture

### Slide 19: Unity Catalog — Unified Governance

**Objective:** Show the three-level namespace and governance pillars.

**Content:** catalog.schema.object namespace plus four governance pillars.

**Visual Layout:** Nested namespace diagram + a 2x2 pillar grid.

**Diagram:** Catalog → Schema → Table/View/Volume/Model (catalog.schema.object).

**Speaker Notes:** Unity Catalog is the single governance layer for the whole Workspace — and uniquely, it governs BOTH data and AI assets (tables, files/volumes, ML models, and functions) in one model. The three-level namespace catalog.schema.object gives every asset one consistent, governable name across all clouds and workspaces, replacing the old two-level hive metastore. Highlight the four pillars: fine-grained access control via standard SQL GRANTs tied to corporate SSO; automatic column-level lineage and audit; discovery plus open Delta Sharing; and unified governance of data and AI together. This is what lets large teams collaborate safely in a shared Workspace.

**Design Tips:** Unique angle: governs data AND AI assets together.


---

### Slide 20: Best Practices & Part 2 Takeaways

**Objective:** Give Workspace operating discipline and recap Part 2.

**Content:** Four best practices and a five-point takeaways panel.

**Visual Layout:** 2x2 best-practice grid beside a navy takeaways panel.

**Diagram:** —

**Speaker Notes:** Wrap Part 2 with operating discipline and a recap. Best practices: version everything in Repos; run production on job clusters (and set auto-termination on interactive ones); parametrize notebooks with widgets so they're reusable and testable; and centralize permissions in Unity Catalog with least-privilege grants. Recap the five takeaways aloud. Bridge to Part 3: now that we know the engine (Spark) and the environment (Workspace), let's see how they assemble into the Lakehouse architecture that ties data, analytics and AI together.

**Design Tips:** Bridge to Part 3 — assemble engine + environment into architecture.


---

### Slide 21: Part 03 Divider — Databricks Lakehouse Architecture

**Objective:** Transition into the architecture build.

**Content:** Part number, title and three covered themes.

**Visual Layout:** Navy divider with a giant '03' watermark and a Delta icon.

**Diagram:** —

**Speaker Notes:** Section 03: Databricks Lakehouse Architecture. Transition slide — pause, then preview the four ideas listed. Use it to re-anchor the narrative and tell the audience what they'll be able to do by the end of this section.

**Design Tips:** Consistent divider system; signals the synthesis section.


---

### Slide 22: Evolution of Data Platforms

**Objective:** Frame the Lakehouse as the resolution of a 40-year trade-off.

**Content:** Data Warehouse → Data Lake → Lakehouse, each with its limitation.

**Visual Layout:** Three cards with arrows, limitations and a closing note.

**Diagram:** Data Warehouse → Data Lake → Lakehouse.

**Speaker Notes:** Tell the 40-year story as a sequence of trade-offs. The DATA WAREHOUSE (1980s onward) gave reliable, fast SQL and BI on structured data, but it's rigid, expensive to scale, and can't do ML or unstructured data. The DATA LAKE (2010s) flipped that — cheap, scalable storage for any data and great for ML — but with no transactions or governance it often degraded into a 'data swamp'. The LAKEHOUSE (2020s) resolves the dilemma: add a transactional, governed metadata layer (Delta Lake) on top of cheap open storage, so you get warehouse reliability AND lake flexibility in one place. That's why you no longer need to run and sync two separate systems.

**Design Tips:** Each generation fixed the last one's flaw.


---

### Slide 23: What Is the Lakehouse?

**Objective:** Define the Lakehouse crisply for anyone new on Day 2.

**Content:** Definition card, three bullets and four attribute tiles.

**Visual Layout:** Navy definition card + 2x2 attribute tiles (Open, Reliable, Unified, Governed).

**Diagram:** —

**Speaker Notes:** Define the Lakehouse crisply for anyone who joined fresh on Day 2. The mechanism is the key idea: a transactional metadata layer — Delta Lake — sits directly on cheap cloud object storage, turning a folder of files into a reliable, governed table. That single move gives you warehouse-grade reliability and performance with lake-grade cost, openness and ML support. The four attribute tiles summarize the value: open (no lock-in), reliable (ACID), unified (all workloads, one copy of data), and governed (Unity Catalog). Everything else in Part 3 — medallion, Delta features, end-to-end flow — is just this definition made concrete.

**Design Tips:** The mechanism — Delta on object storage — is the key idea.


---

### Slide 24: Lakehouse Architecture — Layer by Layer

**Objective:** Present the reference architecture to memorize.

**Content:** Sources → Ingestion → Bronze → Silver → Gold → BI/AI/ML, on Delta + Unity Catalog.

**Visual Layout:** Six-stage pipeline over a Delta + Unity Catalog foundation band.

**Diagram:** Sources → Ingestion → Bronze → Silver → Gold → BI/AI/ML.

**Speaker Notes:** This is the reference architecture for the whole platform — and the diagram to memorize. Data flows left to right: SOURCES (apps, databases, IoT, files) are ingested by tools like Auto Loader and Lakeflow into the medallion layers — BRONZE (raw), SILVER (cleansed and conformed), GOLD (curated business aggregates and ML features) — and finally consumed by BI, AI and ML. The two foundations underneath are what make it a Lakehouse: every layer is a Delta Lake table in open storage, and Unity Catalog governs the entire pipeline end to end. Note this is the same six-stage ecosystem from Day 1, now realized as one platform. We'll zoom into the medallion next.

**Design Tips:** Medal tones for Bronze/Silver/Gold; foundations make it a Lakehouse.


---

### Slide 25: The Medallion Architecture — In Detail

**Objective:** Detail each medallion layer's data, ops, quality and users.

**Content:** Bronze, Silver, Gold described across four dimensions, with a value gradient.

**Visual Layout:** Three detail cards with mini-tables, arrows and a bronze→gold gradient.

**Diagram:** Bronze → Silver → Gold (quality & value rising).

**Speaker Notes:** Now the detailed view of the medallion pattern, layer by layer. BRONZE is raw data exactly as ingested — appended with metadata, your replayable source of truth, owned by data engineers. SILVER is where the real work happens: deduplicate, validate, conform and join into trusted, queryable tables used by engineers and analysts. GOLD applies business logic and aggregation to produce consumption-ready tables and ML features for BI, ML and business users. Each hop raises data quality and business value, shown by the bronze-to-gold gradient. Because every layer is a Delta table, the whole pipeline is reliable and can run incrementally, even with streaming. This is the pattern that operationalizes the Lakehouse.

**Design Tips:** Every layer is a Delta table, enabling incremental & streaming.


---

### Slide 26: Delta Lake Fundamentals

**Objective:** Explain the four features that make the Lakehouse possible.

**Content:** ACID, Time Travel, Schema Enforcement, Data Versioning + the 'under the hood' note.

**Visual Layout:** Four-card carousel over a Parquet + transaction-log note band.

**Diagram:** ACID · Time Travel · Schema Enforcement · Versioning (Parquet + _delta_log).

**Speaker Notes:** Delta Lake is the open-storage layer that makes the Lakehouse possible — these four features are why. ACID TRANSACTIONS bring database reliability to the lake: concurrent writers can't corrupt the table. TIME TRAVEL lets you query or restore any previous version — invaluable for audits, debugging and reproducible ML. SCHEMA ENFORCEMENT rejects malformed data on write while still allowing controlled evolution. DATA VERSIONING means every change is a numbered version with full history. The mechanism (from Day 1) is worth repeating: a Delta table is Parquet files plus a JSON transaction log — that log is the magic that delivers all of this on top of cheap object storage, plus operations like MERGE (upserts), OPTIMIZE (compaction) and Z-ORDER (data skipping).

**Design Tips:** The transaction log is the mechanism behind all four.


---

### Slide 27: Delta Lake — Transaction Flow

**Objective:** Show how Delta guarantees reliability via the transaction log.

**Content:** Write path, the versioned _delta_log, and the read path.

**Visual Layout:** Write-path cards → versioned log band → read-path card.

**Diagram:** Write → validate → write Parquet → atomic commit to _delta_log (v0..vN) → consistent reads.

**Speaker Notes:** This shows HOW Delta guarantees reliability — the transaction mechanism. WRITE PATH: a write request first validates against the table schema, then writes new Parquet data files, and finally makes an ATOMIC commit to the _delta_log. That commit is all-or-nothing — if it doesn't complete, the table is untouched, so there's never a half-written state. The _DELTA_LOG is an ordered series of JSON commits; each one is a new VERSION of the table (v0, v1, v2…), which is exactly what powers time travel. READ PATH: readers consult the log and always get a consistent snapshot of the latest committed version — or any historical version on request — even while writers are active. Delta uses optimistic concurrency control to manage simultaneous writers. This log-based design is the entire basis of ACID on object storage.

**Design Tips:** Atomic commit + ordered log = ACID and time travel on object storage.


---

### Slide 28: Governance & Open Sharing

**Objective:** Show estate-wide governance and open data sharing.

**Content:** Six governance pillars including Delta Sharing and data+AI governance.

**Visual Layout:** 2x3 card grid with icons.

**Diagram:** —

**Speaker Notes:** Governance is what turns a data lake into a trustworthy Lakehouse, and Unity Catalog provides it across the whole estate. Centralized access control uses standard SQL GRANTs down to rows and columns, tied to corporate identity. Lineage and audit are automatic and column-level — critical for compliance and impact analysis. Delta Sharing is a standout: an OPEN protocol to share live data with other organizations or tools without copying it, readable by any client (not just Databricks). Add discovery/tagging, enterprise compliance controls, and the unique ability to govern data and AI assets together. The theme for architects: one consistent governance model spanning every cloud, workspace and asset type.

**Design Tips:** Delta Sharing = open, no-copy sharing readable by any client.


---

### Slide 29: AI & ML on the Lakehouse

**Objective:** Show the ML/GenAI lifecycle on governed data.

**Content:** Gold data → features → train → register → serve, plus a Mosaic AI note.

**Visual Layout:** Five-step icon carousel with arrows and a note band.

**Diagram:** Gold Data → Feature Engineering → Train (MLflow) → Register → Serve & Monitor.

**Speaker Notes:** A major payoff of the Lakehouse: ML and AI run on the SAME governed data as analytics — no separate ML data silo. Walk the lifecycle: start from GOLD data (governed features from the medallion), do FEATURE ENGINEERING in a shared Feature Store, TRAIN and track experiments with MLflow and AutoML, REGISTER versioned models in the Unity Catalog model registry, then SERVE them in real time with built-in monitoring for quality and drift. Databricks calls this Mosaic AI, and it now spans generative AI too — Vector Search for RAG, and LLM fine-tuning and serving — all governed by Unity Catalog. The key message: because models are built on governed Lakehouse data, you get lineage and security across the entire AI lifecycle, not just the data.

**Design Tips:** Models built on governed data get lineage & security end to end.


---

### Slide 30: End-to-End Data Pipeline

**Objective:** Tie all three parts into one production pipeline (capstone).

**Content:** Sources → Ingest → Bronze → Silver → Gold → Consume, with orchestration & governance.

**Visual Layout:** Six numbered stages grouped by phase over a Workflows + Unity Catalog band.

**Diagram:** Sources → Ingest → Bronze → Silver → Gold → Consume (Spark · Delta · Workflows · UC).

**Speaker Notes:** The capstone — everything from all three parts in one picture. Trace it left to right: raw SOURCES are INGESTED (Auto Loader, Lakeflow Connect) into BRONZE, refined to SILVER, curated to GOLD, and CONSUMED by BI, Genie, ML and GenAI apps. Underneath, the four pillars we learned: SPARK + PHOTON execute every stage (Part 1), the WORKSPACE Workflows orchestrate the pipeline (Part 2), DELTA LAKE stores each layer reliably, and UNITY CATALOG governs the whole thing (Part 3). This single diagram is how a real production data platform is built on Databricks — walk it slowly and connect each box back to what we covered today.

**Design Tips:** Connect each box to the engine, environment and architecture learned today.


---

### Slide 31: Benefits of the Lakehouse

**Objective:** Summarize the Lakehouse value in leadership terms.

**Content:** Six benefits: unified, open, reliable, performant, governed, cost-effective.

**Visual Layout:** 2x3 card grid with icons.

**Diagram:** —

**Speaker Notes:** Summarize why the Lakehouse matters in six leadership-friendly words. Unified eliminates tool sprawl; Open avoids lock-in and keeps data in your own account; Reliable brings ACID guarantees to cheap storage; Performant means you don't sacrifice speed for openness (Photon + Delta); Governed gives one consistent security and lineage model for data AND AI; and Cost-Effective comes from keeping a single copy of data with elastic compute instead of running and syncing separate warehouse and lake systems. If asked for the one-line ROI: consolidation plus faster, governed delivery of analytics and AI.

**Design Tips:** One-line ROI: consolidation + faster, governed delivery.


---

### Slide 32: Real-World Example — Omni-Channel Retailer

**Objective:** Ground the architecture in a believable case study.

**Content:** A retail pipeline and four outcome KPIs.

**Visual Layout:** Left pipeline card (4 stacked stages) + right 2x2 KPI tiles.

**Diagram:** POS/Web/Mobile → Auto Loader → Bronze→Silver→Gold → Genie/ML/GenAI.

**Speaker Notes:** Ground the architecture in a believable scenario — an omni-channel retailer (representative of many real Databricks customers). The PIPELINE: point-of-sale, web, mobile and inventory feeds stream in via Auto Loader, flow through Bronze→Silver→Gold Delta tables, and surface as Genie BI, a personalization model, and GenAI assistants — all on one platform. The OUTCOMES are the kinds of results these projects report: roughly an order-of-magnitude faster pipelines than a stitched warehouse-plus-lake setup, genuine real-time personalization and inventory visibility, a single governed copy of data serving BI/ML/GenAI, and substantially lower total cost of ownership. Present the figures as representative outcomes, and invite the audience to map their own use case onto this shape.

**Design Tips:** Present figures as representative outcomes; invite mapping to their use case.


---

### Slide 33: Day 2 — Key Takeaways

**Objective:** Recap the three parts and land four takeaways.

**Content:** Three recap cards (Spark / Workspace / Lakehouse) + four takeaway banners.

**Visual Layout:** Three numbered recap cards over four icon takeaway banners.

**Diagram:** —

**Speaker Notes:** Tie the whole day together. Three pillars: the ENGINE (Spark — unified, in-memory, driver/executor model, lazy DAG), the ENVIRONMENT (Workspace — collaborative hub, notebooks from exploration to production, Repos and Unity Catalog), and the ARCHITECTURE (Lakehouse — Delta + medallion, ACID and time travel on open storage, governed analytics and AI end to end). Quiz the room on the four takeaways. If they can explain how a query runs on Spark, navigate the Workspace, and sketch a medallion pipeline, Day 2 succeeded. Move to Q&A and the close.

**Design Tips:** Quiz the room before the close.


---

### Slide 34: Thank You / Closing

**Objective:** Close, recap visually and point to hands-on resources.

**Content:** Thank-you, resource chips, six-icon recap and a next-session preview.

**Visual Layout:** Navy closing slide with resource chips and recap icon row.

**Diagram:** —

**Speaker Notes:** Congratulate the group on completing Day 2 and recap the six icons — Spark, Workspace, Clusters, Delta, Medallion and Unity Catalog. Point to hands-on resources: the docs, Databricks Academy (free role-based learning and certifications) and the free edition for practice. Preview the next session — a hands-on lab building a medallion pipeline, plus Delta Live Tables / Lakeflow Declarative Pipelines and Workflows orchestration. Open the floor for questions.

**Design Tips:** Mirror the cover; preview the hands-on lab & Delta Live Tables.


---

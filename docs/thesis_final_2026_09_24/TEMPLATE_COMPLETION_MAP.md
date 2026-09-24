# Template-preserving completion plan

The official template controls names, order and numbering. All six chapters, all original sections and the five Data Collection subsections are retained. Extra explanations use unnumbered paragraph labels rather than adding index entries. Original appendix titles and front-matter order are restored. Pagination necessarily changes with the manuscript content.

The original appendix source files were empty, although main.tex specified their titles. They now contain relevant manuscript build/version-control guidance under those exact titles. Earlier project-specific appendices are retained in supplement/ outside the official index.

## Required sections and remaining evidence

| Original location | Current content | Work needed before finalizing |
|---|---|---|
| 1.1 Background | Civic-service and RAG background | No new experiment needed |
| 1.2 Rational of the Study or Motivation | Dataset motivation and practical constraints | No new experiment needed |
| 1.3 Problem Statement | Research problem and questions | No new experiment needed |
| 1.4 Objective | Implemented objectives, not old planned training claims | Confirm final scope |
| 1.5 Methodology in Brief | Actual offline/online pipeline | No new experiment needed |
| 1.6 Scopes and Challenges | Three domains and evaluation coverage | No new experiment unless extending claims |
| 1.7 Team Overview | Names from prior submission | TEAM-01: authors confirm person-by-person responsibilities |
| 1.8 Key Learnings and Insights | Evidence/generation lessons | Author review |
| 2.1 Preliminaries | Retrieval, fusion, reranking | No new experiment needed |
| 2.2 Review of Existing Research | Verified NextRAG and related work | No unsupported replication claim |
| 2.3 Summary of Key Findings | Literature synthesis | No new experiment needed |
| 3.1 Final Specifications and Requirements | Implemented requirements/limits | Confirm recorded deployment hardware if adding specifications |
| 3.2 Societal Impact | Intended benefits and risks | SI-01 only if claiming measured user benefits: actual consented study |
| 3.3 Environmental Impact | Qualitative resource implications | EN-01 if quantifying: measured power/duration; no inference from latency alone |
| 3.4 Ethical Issues | Provenance, privacy, guidance limitations | Confirm permissions/disclosure policy |
| 3.5 Standards - if applicable | Encodings/formats; no certified compliance claim | Identify applicable standards only if actually maintained |
| 3.6 Project Management Plan | Dependency-based completion plan | PM-01: dates, responsibilities, resources, budget supplied by team |
| 3.7 Risk Management | Risks, controls, residual issues | Team review |
| 3.8 Economic Analysis | Cost components and calculation model | EC-01: measured/input costs and defensible comparator |
| 4.1 Design Process or Methodology Overview | Implemented architecture diagram and narrative | No new experiment needed |
| 4.2 Preliminary Design or Design (Model) Specification | Existing baseline and proposed-design executions | DS-01 optional selector-off ablation if component-level claims are needed |
| 4.3 Data Collection -(If Applicable) | Source families and provenance | Confirm unresolved original matches and redistribution permissions |
| 4.3.1 Data Cleaning | Actual normalization and separate candidates | No candidate activation implied |
| 4.3.2 Data Transformation | Typed chunks and representations | No new experiment needed |
| 4.3.3 Data Integration | ID-linked evidence/index storage | No new experiment needed |
| 4.3.4 Data Reduction | Conservative reduction and inclusion | No invented dimensionality-reduction experiment |
| 4.3.5 Summary of Preprocessed Data | Active inventory and flags | Regenerate only if frozen data version changes |
| 4.4 Implementation of Selected Design | Code-grounded retrieval/generation details | No new experiment needed |
| 5.1 Performance Evaluation | Saved outputs, operational metrics, RAGAS protocol | EV-01 finish automatic batch; EV-02 review correctness if claimed |
| 5.2 Analysis of Design Solutions | Diagnostics, strengths, failures | Extend using finalized EV-01/EV-02 results |
| 5.3 Final Design Adjustments | Recorded ordering fix | No additional changes described as implemented |
| 5.4 Statistical Analysis | Operational statistics and paired method | ST-01 calculate paired results after valid judgments exist |
| 5.5 Comparisons and Relationships | Matched baseline/model comparison | Add finalized evaluation, retain fair denominators |
| 5.6 Discussions | Interpretation/limitations | Reconcile with completed metrics |
| 6.1 Summary of Findings | Current evidence-supported conclusions | Update after Chapter 5 is finalized |
| 6.2 Contributions to the Field | Dataset and system integration | No architectural novelty inflation |
| 6.3 Recommendations for Future Work | Evidence selection, data and evaluation | No new experiment needed |

## Ready-to-use follow-up tasks

1. **EV-01:** "Inspect the existing saved-output RAGAS run without restarting it blindly. Validate its expected 180 attempts, failed-call counts, input hashes and completion state. If complete, summarize the paired results and update Sections 5.1, 5.4, 5.5 and 5.6, then reconcile Chapter 6. Do not modify the frozen answers, chapter headings or Abstract."
2. **EV-02:** "Prepare a blinded review sheet for all 30 paired saved answers with the actual supplied contexts. Review relevance, factual support and completeness separately; record reasons, uncertainty and pairwise preference. Distinguish automatic judgments from human-confirmed labels. Do not count preference alone as correctness."
3. **ST-01:** "Using completed valid per-question scores, compute paired CivicRAG-minus-Simple differences, denominators, ties and descriptive bootstrap intervals. Retain failures as disclosed missing values; do not present self-judging as independent factual verification. Update Section 5.4 without changing its heading."
4. **PM-01/EC-01:** "Use the team's confirmed dates, roles, hardware/access costs, tariff, measured wattage, run duration and logged hours to fill the project schedule/resource and cost tables. Keep unknown inputs pending. Estimate energy cost as watts/1000 x hours x tariff. Do not fabricate survey benefits or historical labour."
5. **DS-01 (optional):** "Before any new run, save a rollback and frozen manifest. Compare selector-on and selector-off with the same corpus, Qwen3 settings and questions. Save all contexts, answers, routes and timings. This is an ablation, not a replacement for the already matched baseline. Confirm scope before starting the costly run."

Missing evidence will be collected or generated in later work and inserted into the existing sections. This revision does not start new model generation, alter the chatbot or restart the website.

# From CivicRAG to a Journal-Level Research Project

## A literature review and research roadmap for Bangla and Bangladesh-focused RAG

**Research cutoff:** 5 October 2026  
**Prepared for:** Your next project after the CivicRAG conference paper  
**Local development environment:** Apple M2 MacBook Air, 16 GB unified memory  
**Document type:** Targeted, source-linked scoping review and research proposal guide. This is not a completed systematic literature review or a claim that the proposed methods are already novel.

### Quick Reading Routes

- **Choose a project:** Sections 1 and 7, followed by the supervisor proposal in Section 17.
- **Understand the literature:** Sections 4-6, then the reading order in Section 16.
- **Plan a theory-led study:** Sections 8-10.
- **Plan local implementation and publication:** Sections 11-15.
- **Prepare to pause and return:** Section 18.

---

## 1. The Recommendation in Plain Language

Your strongest next project is probably **not another Bangla chatbot with more components**. It is a general method that answers this question:

> How can a RAG system choose a small evidence set that contains the conditions actually needed to answer the question, rather than merely choosing passages that sound relevant?

Use Bangla public-service information as the primary research setting, but design the method so it can also work in another language or information domain. This gives you both local value and a broader methodological contribution.

My recommended direction is:

**Condition-preserving, token-budgeted evidence selection for multilingual RAG.**

In simpler words: **less evidence, but not missing the important rules.**

Your current applicability selector provides a useful starting point. The next step is to move from manually weighted relevance signals to a clearly defined selection problem, an algorithm, a condition-aware benchmark, and controlled experiments.

However, budgeted selection, context compression, evidence sufficiency, and evidence admissibility already have research behind them. The novelty cannot simply be “we select fewer relevant chunks.” The promising research opportunity is the more specific combination of **condition dependencies, actual tokenizer costs, and measurable loss of answer-critical information**. Even that must pass a full-text novelty audit before you commit to it.

### Three Practical Research Paths

| Priority | Direction | Main question | Why it fits you |
|---|---|---|---|
| 1 | Condition-preserving evidence selection | Can we reduce context tokens without losing the qualifications needed for a correct answer? | Direct continuation of your selector, with room for formal modeling and lightweight algorithms. |
| 2 | Bangla/Banglish language routing | When should a system retrieve and answer natively, translate, or use both? | Addresses your language and token-cost intuition, without requiring large-model training. |
| 3 | Version-aware public-service RAG | Can the system distinguish the currently applicable rule from a similar but outdated rule? | Strong Bangladesh application and a clear operational problem beyond semantic similarity. |

These are my judgments about fit, not measured rankings or predictions of acceptance. Choose **one main research question**. Do not combine all three into an unmanageable first journal project.

---

## 2. What Was Reviewed and How to Read This Report

The search covered primary research records from ACL Anthology, ICLR proceedings, PMLR, NeurIPS proceedings, OpenReview, publisher pages, arXiv, TREC, and relevant author repositories. Official government sources were used for deployment examples.

The emphasis was on 2024-2026 developments, with selected earlier papers where they establish essential concepts. Search topics included adaptive RAG, evidence sufficiency, budgeted evidence selection, prompt compression, multilingual evaluation, Bengali retrieval, tokenization, temporal drift, graph retrieval, and public-service adoption.

**Evidence depth:** Most papers were screened through their official abstract and publication metadata. Selected close competitors, including AdaGATE and the TREC submodular selection report, received closer method-level inspection. No paper's experiments were reproduced during this review. Repository descriptions and reported results are not independent validation.

Publication labels matter:

- **Conference/journal:** A publication record was found in the linked proceedings or publisher source.
- **Workshop:** A published workshop contribution, not the same status as a main-conference paper.
- **Preprint:** Useful recent work, but peer review was not verified here.
- **Author repository:** Evidence of an implementation or claimed paper; acceptance and results may need separate confirmation.
- **Government case report:** Evidence of an initiative or deployment, not proof of a particular algorithm's superiority.

“State of the art” is task- and benchmark-specific. There is no single RAG architecture that is best for direct fee lookup, multi-hop reasoning, large-corpus summarization, and multilingual dialogue simultaneously.

Two useful broad entry points are the 2026 journal survey [Retrieval-augmented generation for natural language processing: a survey](https://link.springer.com/article/10.1007/s10462-026-11605-7) and the evaluation-focused review [Evaluating Retrieval Augmented Generation: A Comprehensive Review of Evaluation Dimensions, Question Types, and Application](https://link.springer.com/article/10.1007/s42979-026-05134-x). Use them to map the field, then read the closest primary methods directly.

---

## 3. What You Already Have That Is Valuable

CivicRAG has given you practical experience with the entire pipeline: source preparation, structure-aware chunking, dense and lexical retrieval, fusion, reranking, applicability selection, generation, source display, and evaluation. That is a substantial advantage over starting from a theoretical idea without a working system.

The pilot values below come from your existing CivicRAG materials shared in this conversation. They are not newly reproduced measurements. The hardware recommendation is based on the local machine inspection; the research recommendations are proposed future work.

Your existing work also provides a useful research observation:

| Observation in your existing materials | What it can motivate | What it does not yet establish |
|---|---|---|
| Mean supplied context falls from about 5,219 to 3,948 characters. | Study whether selection improves evidence efficiency. | A 24% token, runtime, or monetary saving. |
| Custom context relevance is 28/30 versus 29/30 positive judgments. | Investigate the cases where evidence applicability changes. | A large, statistically established general advantage. |
| Dense retrieval is strong on several retrieval metrics. | Use dense retrieval as a serious baseline, not a weak opponent. | That hybrid retrieval must win when the corpus becomes cross-domain. |
| The selector uses action, service, and information-type signals. | Formalize what it means for evidence to satisfy a request. | That the exact weights are optimal or that this component alone caused the observed improvement. |

The character reduction is approximately:

\[
\frac{5219-3948}{5219}\times100 \approx 24.35\%.
\]

The original questions being written by domain experts is a strength. It supports their domain relevance. The separate questions for the next study are whether test questions were held out during development, whether evidence labels were independently reviewed, and whether the sample represents enough distinct intents. Expert question authorship and expert gold-label annotation are related but different tasks.

For the next paper, the strongest development is not a more confident description of the existing result. It is **new evidence explaining when, why, and by how much the method works**.

---

## 4. Where RAG Research Is Moving

### 4.1 Adaptive Retrieval and Search-Based Reasoning

The question is increasingly not just “which passages do we retrieve?” but “do we need retrieval, how much retrieval, and when should we search again?”

| Work and status | Main contribution | Relevance to your next project |
|---|---|---|
| [Self-RAG](https://arxiv.org/abs/2310.11511), ICLR 2024 | Learns retrieval and critique behavior using reflection tokens. | Establishes that retrieval decisions and generation assessment can be learned together. It is not simply a hand-written prompt or keyword selector. |
| [Adaptive-RAG](https://aclanthology.org/2024.naacl-long.389/), NAACL 2024 | Routes questions among different retrieval strategies based on complexity. | A strong conceptual baseline for deciding when an expensive pipeline is actually needed. |
| [Corrective Retrieval Augmented Generation](https://arxiv.org/abs/2401.15884), 2024 preprint | Evaluates retrieved evidence and changes retrieval behavior when evidence appears inadequate. | Relevant to insufficient-evidence handling and retrieval repair. Peer-reviewed publication was not verified here. |
| [Search-R1](https://openreview.net/pdf?id=Rwhi91ideu), COLM 2025 | Trains search-interleaved reasoning with reinforcement learning. | Important frontier work, but training such systems is not the most practical starting point on your laptop. |
| [RAG or Long-Context LLMs? A Comprehensive Study and Hybrid Approach](https://aclanthology.org/2024.emnlp-industry.66/), EMNLP Industry 2024 | Compares retrieval and long-context processing and introduces routing between them. | A reminder to test architecture choices rather than assume that RAG is always the best option. |

**Opportunity for you:** a small controller that decides whether the current evidence is sufficient, or whether a specific missing condition requires another retrieval. Start with frozen models and a lightweight controller rather than reinforcement-learning an entire LLM.

### 4.2 Evidence Sufficiency and Context Efficiency

This is the literature closest to your current interest. A passage may be related to the question without containing enough information to answer it. Conversely, a long context can contain many relevant words but still omit one decisive condition.

| Work and status | Main contribution | Implication |
|---|---|---|
| [Sufficient Context](https://proceedings.iclr.cc/paper_files/paper/2025/hash/33dffa2e3d2ab74a783d1a8c292f66d9-Abstract-Conference.html), ICLR 2025 | Studies whether retrieved context contains enough information to answer, separating this from model behavior. | Essential reading. Your next metric should distinguish topical relevance from answer sufficiency. |
| [RECOMP](https://proceedings.iclr.cc/paper_files/paper/2024/hash/bda88ed2892f5e61c9a9bf215c566913-Abstract-Conference.html), ICLR 2024 | Uses extractive or abstractive compression and selective augmentation. | “Shorter context” is established research territory. Compare against compression, not only top-k selection. |
| [LongLLMLingua](https://aclanthology.org/2024.acl-long.91/), ACL 2024 | Query-aware prompt compression for long-context settings. | A relevant efficiency baseline, especially when preserving original source qualifications matters. |
| [LLMLingua-2](https://aclanthology.org/2024.findings-acl.57/), Findings ACL 2024 | Learns task-agnostic prompt compression through token classification and distillation. | Test whether a generic compressor retains negations, table headers, exceptions, and Bangla conditions. |
| [Submodular Evidence Selection for Grounded Answer Generation in TREC RAG 2025](https://trec.nist.gov/pubs/trec34/papers/WING-II.rag.pdf), TREC participant report | Selects evidence using coverage, retrieval relevance, and diversity before compact evidence construction. | Budgeted coverage selection is already prior art. This is a track report, not a standard main-conference publication. |
| [AdaGATE](https://arxiv.org/abs/2605.05245), May 2026 preprint | Combines entity-gap tracking, targeted retrieval, and token-budgeted evidence assembly for multi-hop QA. | One of the closest competitors. A generic “gap-aware budget selector” would overlap heavily. |
| [Budgeted Evidence Set Construction for Cross-Library Compliance RAG](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6987087), June 2026 SSRN preprint | Frames selection around evidence-set coverage and redundancy for compliance information. | Especially close to public-service evidence selection; full-text comparison is required before claiming novelty. |
| [Towards Dependable RAG Using Factual Confidence Prediction](https://arxiv.org/abs/2605.05244), May 2026 preprint | Uses confidence prediction, including conformal selection of sources. | Statistical selection guarantees are also an active area. Their assumptions must be checked, not treated as universal guarantees. |

AdaGATE reports strong evidence-F1 results under its tested conditions, but its evaluation setup and answer-quality tradeoffs need to be considered separately from its headline efficiency claims. Do not transfer those results to Bangla administrative QA without reproduction.

**The important research distinction:** selecting a diverse evidence set is not automatically the same as preserving the exact combinations of action, applicant category, date, and exception that make a rule applicable.

### 4.3 Graphs, Hierarchies, and Multi-Hop Retrieval

| Work and status | Main contribution | When it matters |
|---|---|---|
| [RAPTOR](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html), ICLR 2024 | Retrieves from a hierarchy built through clustering and summarization. | Questions requiring both broad context and detailed passages. |
| [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130), 2024 preprint | Uses graph communities and summaries for corpus-level questions. | Global questions about a large collection, not necessarily simple fee lookup. |
| [LightRAG](https://aclanthology.org/2025.findings-emnlp.568/), Findings EMNLP 2025 | Combines graph-based and vector-based retrieval. | A graph baseline if relationships between services or entities are central. |
| [From RAG to Memory](https://proceedings.mlr.press/v267/gutierrez25a.html), ICML 2025, HippoRAG 2 | Develops graph-based associative retrieval for non-parametric knowledge use. | Relevant when the answer requires linking facts across documents. |

**Opportunity for Bangladesh:** evidence dependencies across services, such as one application requiring a document issued by another authority. But the research question should be about recovering necessary dependencies, not simply adding a graph database.

### 4.4 Temporal Reliability and Evidence Admissibility

Semantic similarity cannot, by itself, establish that a fee schedule is current or that a rule applies to the requested jurisdiction. A highly similar old document can be the wrong evidence.

Recent work already considers evidence admissibility. The 2026 SSRN preprint [Operationalizing Evidence Admissibility in RAG: The DCA-TRAG Architecture](https://papers.ssrn.com/sol3/Delivery.cfm/7111618.pdf?abstractid=7111618&mirid=1&type=2) describes eligibility checks before similarity-based processing. Its existence means that “filter invalid documents before retrieval” is not a sufficient novelty claim. This review located the preprint, not independent validation of its results.

[FreshStack](https://arxiv.org/abs/2504.13128) offers an example of constructing retrieval benchmarks around realistic technical questions and source collections. The 2026 preprint [Still Fresh? Evaluating Temporal Drift in Retrieval Benchmarks](https://arxiv.org/abs/2603.04532) also provides a useful counterpoint: temporal changes did not automatically destroy benchmark usefulness in its studied setting.

**Opportunity for you:** controlled version conflicts, effective-date reasoning, and incremental index maintenance in public-service documents. Measure the problem rather than assume that every update creates a retrieval failure.

### 4.5 Evaluation Beyond One LLM-Judge Score

| Work and status | Main contribution | What to borrow |
|---|---|---|
| [ARES](https://aclanthology.org/2024.naacl-long.20/), NAACL 2024 | Evaluates RAG using trained judges with human-label-based statistical correction. | Calibrate automatic evaluation against independent annotations. |
| [RAGChecker](https://proceedings.neurips.cc/paper_files/paper/2024/hash/27245589131d17368cccdfa990cbf16e-Abstract.html), NeurIPS 2024 Datasets and Benchmarks | Diagnoses retrieval and generation using fine-grained claims. | Analyze where evidence acquisition and answer generation fail separately. |
| [MEMERAG](https://aclanthology.org/2025.acl-long.1101/), ACL 2025 | Builds multilingual RAG meta-evaluation with expert annotations. | Evaluate the evaluator itself. Do not assume every multilingual judge behaves equally across languages. |
| [MIRAGE-Bench](https://aclanthology.org/2025.naacl-long.14/), NAACL 2025 | Provides a multilingual RAG evaluation arena. | Wider multilingual comparison, with awareness of synthetic-data and judge assumptions. |
| [Enabling Large Language Models to Generate Text with Citations](https://aclanthology.org/2023.emnlp-main.398/), EMNLP 2023, ALCE | Evaluates generated answers with citations. | Displaying sources is useful, but citation support and coverage must also be measured. |

Your next evaluation should measure **evidence quality, answer quality, and cost separately**. A context metric is important, but a context improvement is not permission to ignore a decline in answer correctness or faithfulness.

---

## 5. Bangla and Indic Research You Must Position Against

Bangla RAG is not an empty research area. There is still room for strong work, but “we used hybrid RAG in Bangla” is now a weak novelty claim by itself.

| Work | Status and focus | What it means for you |
|---|---|---|
| [TraSe: Empowering Low-Resource Languages](https://aclanthology.org/2025.lm4uc-1.2/) | LM4UC 2025 workshop; Bangla RAG using translative prompting, with a 200-question setting. | Translation-assisted Bangla RAG is already studied. Compare evaluation conditions before comparing numerical results. |
| [HybridRAG-BN](https://arxiv.org/abs/2608.13004) | August 2026 preprint; Bangla KBQA with hybrid retrieval, a fine-tuned verifier, and fallback search. | Hybrid retrieval plus verification is already a close Bangla baseline. Its larger-model implementation is not automatically suitable for your hardware. |
| [BanglaGovRAG](https://github.com/shoumya-chy/banglagovrag) | Author repository for Bangladesh legal/administrative QA. The repository states MIET 2026 proceedings, but that publication status was not independently verified here. | Very close application overlap. It documents BM25, multilingual embeddings, RRF, cross-encoding, mixed-language questions, and source-linked evaluation. |
| [Cost-Efficient Cross-Lingual RAG for Bengali Agricultural Advisory](https://arxiv.org/abs/2601.02065) | January 2026 preprint; Bangla-to-English query translation, English-source retrieval, and Bangla output. | Direct prior art for your translation/cost idea. A stronger extension must measure routing decisions, semantic preservation, and total cost. |
| [KrishokBondhu](https://arxiv.org/abs/2510.18355) | Bengali voice agricultural RAG; the arXiv record lists an IEEE QPAIN 2026 publication. | Voice-first Bangla agricultural assistance is already being explored. The record is not evidence of a national production deployment. |
| [IndicIRSuite](https://aclanthology.org/2024.acl-short.46/) | ACL 2024 short paper; multilingual retrieval resources and models for 11 Indian languages, including Bengali. | Useful external resources, while recognizing translated-training-data limitations. |
| [MIRACL](https://aclanthology.org/2023.tacl-1.63/) | TACL 2023; multilingual retrieval benchmark with native-speaker-created questions, including Bengali. | A valuable external retrieval control, separate from your administrative corpus. |
| [Hindi-BEIR and NLLB-E5](https://aclanthology.org/2025.naacl-long.220/) | NAACL 2025; a Hindi retrieval benchmark and model study across varied tasks. | A model for the depth of evaluation possible in an underrepresented language. Hindi findings cannot simply be assumed to hold in Bangla. |

### Bangla Is a Language; Bangladesh Is a Deployment Context

A Bangla experiment may use Wikipedia, translated English questions, or Indian administrative terminology. A Bangladesh-focused experiment may involve local agencies, Banglish queries, mixed English abbreviations, forms, circulars, and local source-maintenance practices.

Separate these contributions:

- **Language contribution:** the system handles Bangla morphology, script, transliteration, or code-switching better.
- **Retrieval contribution:** the method improves evidence selection under controlled conditions.
- **Application contribution:** the corpus and questions represent a meaningful Bangladesh use case.
- **Deployment contribution:** the system works under measured local resource, usability, and maintenance constraints.

A stronger paper connects two of these convincingly. It does not need to claim all four.

---

## 6. Your Token-Cost Intuition: What Is Correct and What Needs Testing

### 6.1 Language Can Affect Token Cost

Different tokenizers may split equivalent information into different numbers of tokens across languages. This can affect effective context capacity and inference cost. [Language Model Tokenizers Introduce Unfairness Between Languages](https://proceedings.neurips.cc/paper_files/paper/2023/hash/74bb24dca8334adce292883b4b651eda-Abstract-Conference.html), NeurIPS 2023, establishes the broader issue.

More recent work, [Multilingual Tokenization through the Lens of Indian Languages](https://aclanthology.org/2026.findings-acl.1632/), Findings ACL 2026, studies normalization, tokenization algorithms, vocabulary design, and downstream behavior across Indic languages.

However, neither paper justifies assuming a fixed Bangla token penalty for every model. Measure the tokenizer of the generator and the tokenizer of the retriever separately.

For a meaning-matched Bangla/English pair, define:

\[
\rho_m=\frac{\operatorname{tokens}_m(x_{bn})}{\operatorname{tokens}_m(x_{en})}.
\]

Here, `m` is a particular model/tokenizer, and the two texts should express approximately the same information. A ratio above 1 indicates more Bangla tokens for that pair under that tokenizer. It does not establish lower semantic quality or a universal language ranking.

Also report token counts per answer-critical fact, truncation rates, and accuracy at a fixed token budget. “Tokens per word” alone is difficult to interpret across languages with different word structures.

### 6.2 Translation Does Not Automatically Save Total Cost

Suppose Bangla evidence uses 1,200 tokens and an English rendering uses 800. This hypothetical difference does not prove the English route is cheaper. You may also pay for query translation, evidence translation, answer translation, and an additional validation pass.

For API-based stages, an accounting model is:

\[
C_{\mathrm{request}}=
\sum_{s\in\mathrm{model\ calls}}
\left(p^{in}_sT^{in}_s+p^{out}_sT^{out}_s\right)
+C_{\mathrm{retrieval}}+C_{\mathrm{other}}.
\]

Prices must use consistent units, such as price per token. Offline translation and indexing costs should be reported separately and, if appropriate, amortized over a stated workload. For local inference, measure time, peak memory, and optionally energy instead of pretending an API price represents the actual cost.

There are at least three distinct translation decisions: translating the query, translating the retrieved evidence, and translating the answer. Query translation alone does not necessarily reduce the generator's evidence tokens.

### 6.3 A Strong Language-Routing Experiment

Compare these routes on the same underlying intents and source facts:

| Route | Query and evidence handling | What it tests |
|---|---|---|
| Native | Bangla question, Bangla evidence, Bangla answer. | Native-language baseline. |
| Query translation | Translate the question, retrieve appropriate English evidence, answer in Bangla. | Whether query-language alignment helps enough to justify translation. |
| Dual-query retrieval | Retrieve using both native and translated queries, then fuse. | Coverage gains versus redundancy and extra work. |
| Cross-lingual dense retrieval | Use a multilingual retriever without mandatory translation. | Whether a translation stage is needed at all. |
| Adaptive routing | Choose a route using uncertainty, script, cost, and corpus-language signals. | Whether a lightweight controller can approach the best route at lower average cost. |

Record errors in numbers, negation, service names, abbreviations, and conditions. If the source facts differ between the Bangla and English corpora, you are testing corpus availability as well as language routing; do not attribute the entire difference to translation.

Relevant foundations include [Retrieval-augmented generation in multilingual settings](https://aclanthology.org/2024.knowllm-1.15/), KnowLLM 2024, and [On the Consistency of Multilingual Context Utilization in RAG](https://aclanthology.org/2025.mrl-main.15/), MRL 2025.

### 6.4 Do Not Simply Replace a Pretrained Model's Tokenizer

A tokenizer is tied to the model's learned token embeddings. Creating a compact Bangla tokenizer and attaching it to an unchanged LLM is not a valid drop-in optimization. [Zero-Shot Tokenizer Transfer](https://proceedings.neurips.cc/paper_files/paper/2024/hash/532ce4fcf853023c4cf2ac38cbc5d002-Abstract-Conference.html), NeurIPS 2024, addresses this as a specialized adaptation problem.

Tokenizer adaptation could become a later research project with stronger compute support. For now, **tokenizer-aware evidence selection or route selection is the more feasible option**.

---

## 7. Five Candidate Projects, Ranked for Your Situation

### A. Condition-Preserving Evidence Selection: Recommended

**Question:** Can a selector preserve all necessary qualifications while reducing generator context tokens?

**Method candidate:** Represent source spans and their governing conditions as dependency-linked evidence units. Choose a budgeted set that covers the request without dropping required parent conditions or combining incompatible facts.

**Possible contribution:** An explicit condition-aware optimization problem, a practical selection algorithm, and evaluation that distinguishes topical relevance from complete applicable support.

**Main risk:** Existing work on sufficiency, submodular selection, gap repair, and admissibility may cover parts of the idea. The contribution must survive a detailed comparison with the closest papers in Section 4.2.

**Local feasibility:** High for a frozen-model algorithmic study. No new foundation model is required.

### B. Quality-Constrained Bangla/Banglish Routing

**Question:** Which language-processing route minimizes total cost while retaining answer quality across native Bangla, transliterated Banglish, and mixed-language queries?

**Method candidate:** Train or calibrate a small router using query features, retrieval agreement, estimated token cost, and uncertainty. Compare it with always-native, always-translate, and dual-query policies.

**Possible contribution:** A general decision rule or cost-quality analysis, with Bangla as the primary test case and an additional language for transfer if resources permit.

**Main risk:** Translation-assisted Bengali RAG already exists. A translation pipeline alone is not enough. The interesting question is when translation should be avoided or selected.

**Local feasibility:** High to moderate, depending on the translation models and number of generation experiments.

### C. Version-Aware Public-Service Evidence

**Question:** Can a RAG system answer using the correct effective version of a rule when old and new documents are both retrievable?

**Method candidate:** Maintain source snapshots, effective dates, supersession links, and a query-specific applicability filter. Evaluate both current-time and historical-time questions.

**Possible contribution:** A formal temporal evidence model, a versioned benchmark, and measured update/retrieval behavior.

**Main risk:** Collecting reliable version histories and authoritative effective dates may be harder than implementing the retrieval method.

**Local feasibility:** Good computationally, but dependent on source access and domain-expert availability.

### D. Bangla RAG Evaluation and Judge Calibration

**Question:** Do automatic evaluators correctly distinguish relevant, sufficient, faithful, and condition-correct outputs in Bangla?

**Method candidate:** Build expert-adjudicated examples with controlled error types, then compare judges across languages, model families, and answer styles. A new calibration method would strengthen the contribution beyond a dataset alone.

**Possible contribution:** A benchmark plus a validated evaluation protocol or a method that reduces judge bias and uncertainty.

**Main risk:** A small benchmark with a single automatic judge will not be a major advance. Annotation quality and external validity are central.

**Local feasibility:** Good for inference, but annotation is the main investment.

### E. Structure-Preserving Bangla Document Retrieval

**Question:** How much retrieval and answer error comes from losing table headers, footnotes, lists, or OCR structure before retrieval even begins?

**Method candidate:** Preserve row-header relationships and rule-exception dependencies; compare these representations with fixed-size and ordinary structure-aware chunks.

**Possible contribution:** A document representation method and a benchmark that separates extraction errors from retrieval errors.

**Main risk:** Adding an OCR library is engineering, not sufficient research novelty. A reproducible error model or a better representation is needed.

**Local feasibility:** Moderate. Start with text and tables before attempting large vision-language models.

**My choice:** A as the main paper, with E as a narrowly scoped representation component if your source documents require it. Keep B and C as separate future projects unless experiments show they are essential to the central question.

---

## 8. A Concrete Theory-Led Version of Project A

### 8.1 The Research Problem

Ordinary relevance ranking treats passages mainly as independent items. Public-service evidence often is not independent: a table row may require its header, a rule may require an exception, and a document requirement may apply only to a particular action or applicant category.

The proposed problem is:

> Select a small set of evidence units whose joint meaning supports the requested answer, preserving the conditions that make each unit applicable.

This is a proposed formulation, not a claim that no prior paper has considered dependencies.

### 8.2 A Bangla Example

Question:

> **“পাসপোর্ট নবায়ন করতে কী কী কাগজপত্র লাগবে?”**

Meaning: What documents are required to renew a passport?

The query expresses:

| Element | Value in this example |
|---|---|
| Service | Passport |
| Action | Renewal |
| Requested information | Required documents |
| Unspecified details | Any applicant category or special circumstance that changes the requirements |

A passage about passport renewal processing time is related but does not answer the document question. A document list for a lost-passport replacement may share many words but describe a different procedure. A renewal list with a separate eligibility note may be incomplete if that note is removed.

No actual government requirements are asserted in this example. It illustrates evidence relationships, not administrative advice.

### 8.3 Formal Variables

Let the candidate evidence set be:

\[
\mathcal{C}=\{c_1,\ldots,c_n\}.
\]

| Symbol | Meaning | Example |
|---|---|---|
| `q` | User question | The Bangla renewal-document question above. |
| `c_i` | Candidate evidence unit | A source paragraph, table row, or linked rule span. |
| `x_i` | Whether unit `i` is selected, 0 or 1 | `x_3 = 1` means include the third unit. |
| `t_i` | Token cost under the chosen tokenizer and serialization convention | Tokens required for the paragraph and its source marker. |
| `B` | Evidence-token budget | A proposed experimental budget, not necessarily your old character cap. |
| `a_j` | Answer requirement or aspect | The main document list, or an applicable exception. |
| `y_j` | Whether aspect `j` is supported by the selected set | A necessary exception is included with its governing rule. |
| `w_j` | Weight for an aspect | Equal weights initially; alternatives tuned only on development data. |
| `D` | Dependency links | Selecting a table row requires its governing header. |
| `V_i(q)` | Query-specific eligibility of unit `i` | Correct service, procedure, and effective version when known. |

Gold aspects and dependencies are used for evaluation and oracle analysis. The deployed selector must predict or derive them from available text and metadata. It must not receive test-set gold annotations.

### 8.4 A Starting Optimization Model

One possible starting objective is:

\[
\max_x\;\sum_j w_j y_j
-\lambda\sum_{i<k}r_{ik}x_ix_k,
\]

where `r_ik` measures duplicated information and `lambda` controls the redundancy penalty.

The simplified constraints are:

\[
\sum_i t_i x_i\le B,
\qquad x_i\in\{0,1\},
\]

\[
x_i\le x_p \quad\text{if evidence unit }i\text{ requires parent }p,
\]

\[
x_i\le V_i(q).
\]

For two genuinely incompatible claims about the same requested case, one possible constraint is:

\[
x_i+x_k\le1.
\]

Do not apply this last constraint to legitimate comparisons, such as a user explicitly asking how old and new rules differ. Applicability is query-dependent. Unknown eligibility should remain unknown or trigger clarification, not be silently treated as certain.

Simple aspect coverage can use `y_j <= sum_i s_ij x_i`, where `s_ij` indicates support. But some aspects require several jointly applicable units. Those need conjunction or bundle constraints; otherwise the system may incorrectly combine a renewal passage with a replacement-fee passage and claim complete coverage.

The additive token model is an approximation unless serialization is carefully designed. The final constraint should use the tokenizer on the complete prompt:

\[
T_m(\operatorname{format}(\mathrm{instructions},q,E))
+T_{\mathrm{reserved\ output}}
\le W_m.
\]

This includes source labels, separators, question, instructions, and output reservation. Shared parent evidence should be counted once, not once per dependent unit.

### 8.5 A Small Numerical Example

These numbers are hypothetical and are not CivicRAG measurements.

Suppose the budget is 500 tokens and the answer needs three aspects: A, B, and C.

| Unit | Relevance rank | Token cost | Supported aspects |
|---|---:|---:|---|
| Passage 1 | 1 | 240 | A |
| Passage 2 | 2 | 240 | A, mostly duplicated |
| Passage 3 | 3 | 220 | B and C |

Taking the first two passages costs 480 tokens but covers only A. Taking passages 1 and 3 costs 460 tokens and covers A, B, and C.

That demonstrates why selecting a set can be better than blindly taking the highest-ranked individual passages. But **this example alone is not novel**; coverage-based methods already address it.

Your harder case is when Passage 3's meaning is valid only with a governing condition elsewhere. The selector should include the required bundle, select an alternative, or report insufficient support. It should not remove the condition just to meet the budget.

### 8.6 What Would Make This Theoretical Research?

Possible contributions include a proof about a clearly restricted problem, a characterization of when independent ranking fails, an approximation analysis under explicit assumptions, or a calibrated bound on selection errors. Equations alone do not make a method theoretical.

A realistic sequence is:

1. Define the evidence-selection problem precisely, including what counts as support and a dependency.
2. Analyze a simplified setting with known support labels and dependencies.
3. Compare a practical algorithm with an exact optimizer on small candidate sets.
4. Introduce noisy predicted labels and measure how extraction errors affect the result.
5. Evaluate whether the formal improvement survives real Bangla evidence and generation.

Weighted coverage is a familiar submodular objective. However, dependency conjunctions, incompatibility constraints, and negative redundancy terms can change the mathematical properties. Do not automatically claim the classic `1 - 1/e` approximation guarantee for your full problem.

An exact optimization result is an oracle only relative to the supplied evidence labels and candidate pool. It does not prove that the labels are correct or that retrieval found every necessary passage.

### 8.7 The Novelty Gate Before Coding

Prepare a side-by-side comparison with Sufficient Context, the TREC selector, AdaGATE, the compliance evidence-set preprint, and the admissibility preprint. Compare their optimization units, dependency handling, budget model, supervision, and evaluation tasks.

If the proposed method reduces to “coverage plus a budget,” stop and refine it. If existing work already handles the exact condition model, consider shifting to a stronger error analysis, cross-language transfer result, or a genuinely different constraint/algorithm.

This is how you aim high without spending months rediscovering an existing method.

---

## 9. Experiments That Could Support a Strong Paper

### 9.1 State Falsifiable Hypotheses

Use hypotheses that could genuinely fail:

**H1:** At the same evidence-token budget, condition-aware selection improves independently annotated condition-complete support compared with relevance-only selection.

**H2:** At comparable answer quality, the proposed method uses fewer generator input tokens than strong selection/compression baselines.

**H3:** Improvements remain visible with at least two generator families and are not limited to one domain or one query-writing style.

**H4:** The benefit is larger when distractors are topically similar but procedurally incompatible, rather than merely unrelated.

These hypotheses do not require hybrid retrieval to beat dense retrieval. Your selector could be valuable on top of either retriever.

### 9.2 Separate Two Experimental Questions

**Controlled selection experiment:** Give every selector the same candidate pool, query, tokenizer, and budget. This isolates the selector.

**End-to-end experiment:** Allow complete retrieval pipelines to produce their own candidates. This measures the whole system, including failure to retrieve required evidence.

You need both. Otherwise a selector may receive better candidates than a baseline and get credit for a gain that came from retrieval. Conversely, a good selector cannot select evidence that never entered its candidate pool.

### 9.3 Use Serious Baselines

| Baseline family | Minimum useful comparison | Why it is necessary |
|---|---|---|
| Lexical retrieval | BM25 with suitable text normalization. | Measures exact terminology matching. |
| Dense retrieval | BGE-M3 plus another credible multilingual retriever if feasible. | Prevents the conclusion from depending on one embedding model. |
| Hybrid retrieval | Tuned BM25+dense fusion. | Tests complementarity without assuming fixed weights are optimal. |
| Reranking | The same cross-encoder candidate reranking where applicable. | Prevents confusing reranker improvements with selector improvements. |
| Simple selection | Fixed top-k and token-budgeted top-ranked passages. | Essential low-complexity baselines. |
| Diversity selection | MMR or a coverage/diversity selector. | Tests whether simple duplicate removal explains the gain. |
| Existing CivicRAG | Your original applicability heuristic. | Shows what has changed beyond the conference system. |
| Compression | A suitable RECOMP/LLMLingua-style baseline. | Tests whether existing compression already solves the problem. |
| Closest contemporary method | AdaGATE or a faithfully scoped comparable method where the task assumptions match. | Establishes a comparison beyond home-built baselines. |
| Oracle analysis | Exact selection with gold support/dependency labels on a small pool. | Shows the available headroom and where prediction errors occur. |

BGE-M3 itself supports more than the dense mode used in many pipelines. Its [M3-Embedding paper](https://aclanthology.org/2024.findings-acl.137/) describes dense, sparse, and multi-vector representations. Be explicit about which mode you evaluate; “BGE-M3” alone is not a complete retriever specification.

Not every baseline needs to run in every configuration. First compare selectors on cached candidates, then run the most informative systems end to end. If you simplify another paper's method, label it as an adaptation and document the differences.

### 9.4 Build a Fresh Evaluation Set

Use the existing 30 questions as a development resource unless you can establish that they were untouched during every relevant design decision. Do not discard them; they are useful for understanding errors and building the annotation guide.

A practical new-data plan is:

- **Pilot:** approximately 150-250 independently authored base intents, enough to test annotation consistency and estimate error rates.
- **Main study:** consider 600-1,000 distinct base intents if annotation resources permit, with the final target chosen using the pilot and a power analysis.
- **Language variants:** native Bangla, meaning-preserving Banglish, and selected English/code-switched versions of the same intents.
- **Generalization:** at least one held-out domain, plus an external retrieval benchmark or second-language/task evaluation relevant to the claim.

These are planning ranges, not universal publication requirements. Paraphrasing one question ten times does not create ten independent research cases. Keep variants of the same intent in the same train/development/test partition.

Include direct questions, paraphrases, multi-condition questions, table-dependent questions, and genuine missing-information cases. The latter are not a reason to call the whole dataset a “safety dataset.” They test whether the system knows when the available sources cannot support the requested answer.

### 9.5 Gold Annotation Should Be Independent of Your Method

For each case, annotate the question intent, acceptable answer facts, supporting source spans, necessary qualifications, and any valid alternative evidence sets. If relevant, record the source's effective date and applicant category.

Have two knowledgeable annotators work independently on an agreed subset or the complete test set, then adjudicate disagreements. Report agreement with the annotation unit and label definition clearly stated. Do not treat the number of source URLs as evidence completeness.

Annotators should not be told which system generated an answer or selected a passage. More importantly, they should not define “relevant” as “contains the three keywords that our selector checks.” That would make the evaluation circular.

Where a rule does not specify a needed detail, annotate the uncertainty. Do not invent a gold answer just to make every question answerable.

### 9.6 Metrics: Keep the Different Questions Separate

| Measurement | What it asks | Use in the next paper |
|---|---|---|
| Hit@5 | Did at least one labeled relevant passage appear in the first five? | Basic retrieval coverage. |
| Precision@5 | What fraction of the first five passages are labeled relevant? | Top-five evidence concentration. |
| nDCG or rank-sensitive measures | Are better passages placed earlier? | Retrieval ordering, with a disclosed labeling protocol. |
| Evidence sufficiency | Does the selected set contain enough information for the requested answer? | Central to the proposed method. |
| Condition-complete support | Are the necessary facts present with the qualifications that make them applicable? | A proposed evaluation dimension requiring a published rubric and human validation. |
| Faithfulness | Are answer claims supported by the supplied evidence? | Still necessary; a better selector does not excuse unsupported output. |
| Answer relevance | Does the answer address the question? | Detects answers that are grounded but off-target. |
| Answer correctness/completeness | Is the answer correct and complete against expert-reviewed facts for this case? | Prevents improving a context metric while harming the task. |
| Citation support and coverage | Do cited sources support the claims, and are important claims cited? | More informative than simply displaying evidence links. |
| Actual input/output tokens | How much text is processed by each model? | Replaces character count as the token-efficiency measurement. |
| End-to-end latency and peak memory | What does the complete system cost locally? | Accounts for extra retrieval and selection work. |

For clarity, your original custom context relevance metric is a particular evaluator with its own rubric. It is not automatically identical to evidence sufficiency or to any similarly named metric in another framework. A new condition-complete metric also needs validation; naming it does not establish validity.

The most persuasive result would be a **quality-cost curve**: at each token budget, show answer quality and condition-complete evidence coverage. A single winning budget can hide a method that works poorly elsewhere.

### 9.7 Necessary Ablations

Remove one proposed component at a time: dependency preservation, condition compatibility, redundancy handling, tokenizer-specific budgeting, and any learned routing. Also compare predicted dependencies with gold dependencies to separate extraction quality from selection quality.

Hold generator model, quantization, prompt, output budget, and sampling configuration constant within comparisons. If a method changes the prompt or makes extra model calls, disclose and count them. Use repeated runs where stochastic behavior materially affects results.

Record candidate-pool quality before selection. Test several candidate-pool sizes and budgets, but choose the development grid before inspecting the final test outcomes.

### 9.8 Statistics and Negative Results

Report paired per-question differences and confidence intervals, not just mean bars. Bootstrap or permutation procedures should respect grouping by underlying intent or source family where appropriate. Ten paraphrases of one case should not be treated as ten independent cases.

For a quality-preserving efficiency claim, set the allowed quality-loss margin before the final test and justify it with domain experts. Merely finding a non-significant difference in a small sample is not proof of equal quality.

If dense retrieval wins, report it. If the selector helps only under constrained budgets or condition-heavy questions, that can still be a useful contribution when the regime is clearly defined and the result is reliable.

---

## 10. Cross-Domain RAG: A Good Hypothesis, Not an Automatic Win

Your intuition is understandable: when several domains contain words like “application,” “renewal,” “fee,” and “documents,” a system may need more than general semantic similarity.

But it does not follow that dense retrieval will automatically perform worse than hybrid retrieval. Dense representations can encode domain distinctions; lexical retrieval can also be confused by shared terminology. A domain filter may solve some errors more cheaply than either a complex selector or a graph.

Use four controlled settings:

| Setting | Corpus and question | What changes |
|---|---|---|
| Domain-scoped | Passport question, passport corpus. | Existing-style retrieval. |
| Mixed corpus, single-domain question | Same passport question, all domains searchable. | Distractor competition changes while the task stays fixed. |
| Mixed corpus with predicted routing | Same question, a learned or rule-based domain route. | Tests domain selection errors and efficiency. |
| Genuine cross-domain question | Answer requires evidence from two services. | The reasoning and evidence requirements change. |

Do not combine the last setting with the second and call all gains “cross-domain robustness.” One tests distractor resistance; the other tests multi-source composition.

A useful research hypothesis is:

> Condition-aware selection may be especially helpful when semantically similar evidence refers to different procedures or when a valid answer requires compatible facts from multiple sources.

That is stronger scientifically than predicting that a competing retrieval method must fail.

---

## 11. Bangladesh Opportunities and Lessons from Other Countries

### 11.1 International Examples

| Example | What the primary source establishes | Lesson worth adapting |
|---|---|---|
| United Kingdom: [GOV.UK Chat transparency record](https://www.gov.uk/algorithmic-transparency-records/dsit-gov-dot-uk-chat) | Describes a RAG-based government-information assistant, source links, and both automated and manual evaluation. | Treat content ownership, source navigation, and expert evaluation as part of the system, not extras after model selection. |
| United Kingdom: [2026 GOV.UK Chat testing lessons](https://insidegovuk.blog.gov.uk/2026/03/16/5-things-we-learned-testing-gov-uk-chat-an-ai-assistant-for-government/) | Reports lessons from testing the service with users. | Evaluate whether people can successfully complete an information task, not only whether an LLM judge likes the answer. |
| Singapore: [Pair](https://pair.gov.sg/) | Official public-sector AI tooling with document and knowledge-work capabilities; its materials also discuss long-context approaches. | Architecture should follow the use case. Do not describe every government assistant, or every Pair capability, as RAG. |
| India: [Kisan e-Mitra government report](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2100755&lang=2&reg=48) | Documents multilingual AI assistance for agricultural scheme information. | A useful service-delivery precedent. This source alone does not establish that its backend uses a particular RAG architecture. |

The transferable idea is not “copy their chatbot.” It is to connect a research method with an institution that owns the documents, understands the users, and can evaluate whether the answer is useful.

### 11.2 Bangladesh Is Not Starting from Zero

Bangladesh's [333 service already has a public chat interface](https://333.gov.bd/chat/). This establishes an existing service channel, not proof of its internal retrieval architecture. The Bangla research projects in Section 5 also show that local-language public-service and agricultural assistance are already active areas.

Possible institutional discussions include a university service office, a public-information team, an agricultural extension partner, or a service-information provider. These are potential collaborators, not partnerships established by this report.

### 11.3 Local Applications Ranked by Research Practicality

| Application | Research opportunity | Main dependency |
|---|---|---|
| University admissions, scholarships, and administrative circulars | Versioned rules, eligibility conditions, mixed Bangla/English questions, tables. | Access to authoritative circulars and staff who can annotate. Often a practical first partner. |
| Passport, birth registration, and BRTA information | Build directly on CivicRAG; study procedure and condition mismatches. | Fresh sources, balanced domains, and independent test questions. |
| Local-government service navigation | Multi-step procedures and agency-specific evidence. | Clear separation between official guidance and unofficial descriptions. |
| Agriculture | Native terminology, colloquial questions, multilingual manuals, optional voice. | Agricultural experts, seasonal/local applicability, and strong existing baselines. |
| Benefits or social-support information | Eligibility and evidence completeness are central. | Sensitive cases and reliable rule interpretation; start with information retrieval rather than automated eligibility decisions. |
| Land or legal information | Version conflicts, jurisdiction, and source authority. | Substantial expert effort. Not the easiest first expansion. |

For a first journal project, a well-documented institutional domain can be more valuable than a national-scale corpus with weak labels. You need a setting where the research claim can be tested carefully.

### 11.4 What to Measure in a Small Adoption Study

Compare the prototype with the existing search or FAQ workflow. Measure task completion, time to find the correct source, whether users identify the governing condition, and whether source links actually help verification.

Do not equate “users preferred the interface” with factual correctness. Keep usability and correctness results separate. If collecting real user questions, obtain appropriate consent and institutional approval, minimize personal data, and agree on what can be released.

---

## 12. A Plan That Fits Your M2 MacBook Air

The local hardware check showed an **Apple M2 MacBook Air with 16 GB unified memory**, with 8 CPU cores and 8 GPU cores. That is a useful research machine for this direction, provided you avoid treating it as a large-model training server.

### Good Local Workloads

- Corpus preparation, source versioning, BM25 indexing, and annotation tooling.
- Frozen multilingual embeddings with batched encoding and cached results.
- Cross-encoder reranking on limited candidate sets, with cached scores.
- Evidence-selection algorithms, small optimization problems, and statistical analysis.
- Serialized generation with appropriately quantized small models, after a memory/runtime pilot.
- Small routing or calibration models based on cached features.

### Workloads Not to Make Essential

- Pretraining a foundation model or training a large search agent from scratch.
- Keeping multiple large embedding, reranking, and generation models loaded simultaneously.
- Depending on a 31B-class model as the normal local experimental configuration.
- Running every combination of retriever, selector, generator, language, and budget before estimating runtime.

Four-to-eight-billion-parameter quantized generators are reasonable candidates to test, not guaranteed performance specifications. Context length, quantization format, backend, and other running applications affect memory and throughput.

### Efficient Experimental Sequence

1. Freeze the corpus snapshot and benchmark split.
2. Build lexical and embedding indices once per representation.
3. Cache candidate IDs, source text hashes, retrieval scores, and reranker scores.
4. Run selection experiments against those cached candidates without generating answers.
5. Eliminate clearly uninformative configurations using development data.
6. Generate answers only for the selected comparison systems and budgets.
7. Run final test evaluation after freezing the method and analysis plan.

Separate cold-start and warm-run latency. Report all required model calls; a method that saves generator tokens may still be slower overall because selection is expensive.

For compute planning:

\[
N_{\mathrm{generation}}=
N_{\mathrm{questions}}\times N_{\mathrm{systems}}
\times N_{\mathrm{generators}}\times N_{\mathrm{repeats}}.
\]

For example, 600 questions, 4 systems, 2 generators, and 1 run already require 4,800 generation calls, before translation or judging. Measure a representative pilot's seconds per call and peak memory before deciding the final matrix. This report does not claim measured throughput for your next experiment.

If a collaborator provides GPU access, use it for a bounded experiment such as adapting a small reranker or testing a stronger generator. The core contribution should still be evaluable locally and should not depend on continuous paid API access.

---

## 13. What a Journal-Level Contribution Could Look Like

The goal should be a paper whose contribution can be described without naming the application interface.

**Weak framing:** “We created an improved Bangla chatbot using BM25, dense retrieval, reranking, and a larger LLM.”

**Stronger framing:** “We formulate evidence selection with condition dependencies and tokenizer-specific budgets, develop a practical algorithm, and show when it improves complete support per unit of context across multiple retrieval and generation settings.”

A persuasive package could include:

1. A precisely defined problem that existing baselines do not adequately address.
2. An algorithm or analysis beyond hand-picked weights and pipeline assembly.
3. A source-linked, independently annotated evaluation resource.
4. Comparisons with strong modern methods, including methods that may outperform yours in some regimes.
5. Ablations, uncertainty estimates, failure analysis, and reproducible artifacts.

Not every strong journal paper needs a theorem. An excellent empirical paper can instead establish a new phenomenon, a reliable benchmark, or a well-supported method. If you explicitly target theoretical work, make the formal claim central rather than adding notation after implementing the system.

### Possible Titles, Pending Results

- **Condition-Preserving Evidence Selection under Token Budgets for Multilingual Retrieval-Augmented Generation**
- **Beyond Topical Relevance: Modeling Applicability Dependencies in Evidence-Grounded Question Answering**
- **When Should Bangla RAG Translate? Quality-Constrained Language Routing under Local Compute Budgets**

These are working titles, not claims of completed contributions or verified novelty.

---

## 14. Journal Fit and the Meaning of Q1

Q1 is not a permanent property independent of the ranking system. It refers to a journal's position within a specified database, subject category, and year. JCR and SJR are different systems; a journal can have different positions across categories. The [Clarivate JCR glossary](https://journalcitationreports.zendesk.com/hc/en-gb/articles/28351666061457-Glossary) explains the category-based ranking framework.

**The following is a scope-based shortlist, not a certification that each journal currently satisfies your institution's exact Q1 requirement.** Individual current quartiles were not verified from an authoritative ranking record in this review. Confirm the required database and year with your supervisor or university library before selecting a target.

| Journal to investigate | Fit for this project | What would make the submission credible |
|---|---|---|
| [Information Processing & Management](https://shop.elsevier.com/journals/information-processing-and-management/0306-4573) | Particularly natural for retrieval, evidence organization, multilingual information access, and rigorous application-method studies. | A substantive method and broad evaluation, not only a local chatbot demonstration. |
| [Knowledge-Based Systems](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) | Potential fit for explicit applicability representations, dependency reasoning, or hybrid symbolic-neural selection. | A generalizable intelligent-system method with strong baselines and analysis. |
| [IEEE Transactions on Knowledge and Data Engineering](https://www.computer.org/digital-library/journals/tk/cfp-ieee-transactions-on-knowledge-data-engineering) | A stretch target if the work becomes a strong knowledge/data-management or retrieval algorithm contribution. | Significant methodological depth, convincing scalability/generalization, and a clear match to its stated scope. |

My initial scope preference is **Information Processing & Management** for Project A or B. Reassess after the pilot, the novelty audit, and an examination of recently accepted papers. That is a fit recommendation, not an acceptance prediction.

Before submission, verify the latest author instructions, page/word limits, review model, artifact expectations, publication charges, open-access options, and your institution's funding rules. Do not budget based on an old quoted publication fee.

### Extending the Conference Work

The next paper should explicitly identify CivicRAG as prior work and explain what is new. A credible extension could add the formal problem, a new selector, fresh independent data, token-level measurements, cross-model testing, and a new analysis of failure regimes.

Simply adding pages, changing the generator, or polishing the same experiment is not the target. Keep an extension table showing “conference paper” versus “new journal work.” Exact republication rules depend on the venue and publisher; do not assume a universal percentage-of-new-text rule. Check the destination journal's policy and disclose related publications and submissions as required.

---

## 15. A 16-24 Week Research Roadmap

This is a planning estimate for the work, not a journal acceptance timeline. Annotation access and your available weekly time may change it substantially.

| Phase | Suggested time | Deliverable | Decision gate |
|---|---|---|---|
| Literature and novelty audit | Weeks 1-2 | Comparison of the closest 6-8 methods and a one-page problem statement. | Is there a specific gap beyond existing selection/compression? |
| Pilot corpus and annotation | Weeks 3-5 | Annotation guide, pilot intents, source-condition labels, disagreement report. | Can experts consistently identify the target error? |
| Baseline reproduction | Weeks 6-8 | Cached retrieval/reranking, basic selectors, first token-quality curves. | Does the proposed problem occur often enough to matter? |
| Method and formal analysis | Weeks 9-12 | Implemented method, restricted formal analysis, oracle comparison. | Does the method improve on a simple diversity/coverage baseline? |
| Expanded evaluation | Weeks 13-16 | Frozen held-out test set, multiple models/domains, efficiency measurements. | Does the benefit survive beyond development cases? |
| Ablations and writing | Weeks 17-20 | Failure taxonomy, statistics, paper draft, release package. | Are claims no stronger than the evidence? |
| External review and revision | Weeks 21-24 | Supervisor/peer feedback and journal-specific submission. | Are novelty, scope, and reproducibility clear? |

### Stop or Redirect Early When Needed

If experts cannot agree on “applicable evidence,” improve the definition before training anything. If simple MMR performs equally well, study why instead of adding more layers. If the main bottleneck is OCR, move toward document representation rather than insisting on a selector paper.

If Bangla tokenization is not the main cost driver under your chosen models, report that and redirect the efficiency analysis. A useful negative result can guide the next design decision.

---

## 16. Your First Ten Reading Sessions

Read in this order for the recommended project. The goal is not to read every paper before starting; it is to find out whether your central idea is already solved.

1. **Sufficient Context:** distinguish relevance, sufficiency, and generator capability. [Paper](https://proceedings.iclr.cc/paper_files/paper/2025/hash/33dffa2e3d2ab74a783d1a8c292f66d9-Abstract-Conference.html)
2. **AdaGATE:** compare its gap representation and evidence assembly with your proposed condition dependencies. [Paper](https://arxiv.org/abs/2605.05245)
3. **TREC submodular evidence selection:** understand the coverage/diversity baseline you must beat or extend. [Report](https://trec.nist.gov/pubs/trec34/papers/WING-II.rag.pdf)
4. **Budgeted compliance evidence construction and DCA-TRAG:** check the closest domain/constraint overlap before claiming novelty. [Budgeted sets](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6987087), [admissibility](https://papers.ssrn.com/sol3/Delivery.cfm/7111618.pdf?abstractid=7111618&mirid=1&type=2)
5. **RECOMP and LLMLingua-2:** compare selection with compression and identify which information must be preserved. [RECOMP](https://proceedings.iclr.cc/paper_files/paper/2024/hash/bda88ed2892f5e61c9a9bf215c566913-Abstract-Conference.html), [LLMLingua-2](https://aclanthology.org/2024.findings-acl.57/)
6. **TraSe, HybridRAG-BN, and BanglaGovRAG:** map the existing Bangla/local contribution space. [TraSe](https://aclanthology.org/2025.lm4uc-1.2/), [HybridRAG-BN](https://arxiv.org/abs/2608.13004), [BanglaGovRAG](https://github.com/shoumya-chy/banglagovrag)
7. **Tokenizer unfairness and the Indic tokenization study:** formulate a measured token-cost question. [NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/74bb24dca8334adce292883b4b651eda-Abstract-Conference.html), [Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1632/)
8. **MEMERAG and RAGChecker:** design an evaluator that can tell retrieval failure from generation failure. [MEMERAG](https://aclanthology.org/2025.acl-long.1101/), [RAGChecker](https://proceedings.neurips.cc/paper_files/paper/2024/hash/27245589131d17368cccdfa990cbf16e-Abstract.html)
9. **Adaptive-RAG and multilingual RAG:** consider whether a simple route decision solves the problem more cheaply. [Adaptive-RAG](https://aclanthology.org/2024.naacl-long.389/), [multilingual RAG](https://aclanthology.org/2024.knowllm-1.15/)
10. **GOV.UK Chat case materials:** think about the institution, content maintenance, and user task around the algorithm. [Official record](https://www.gov.uk/algorithmic-transparency-records/dsit-gov-dot-uk-chat)

For each paper, record five things: its exact problem, what it assumes, what it changes, how it is evaluated, and the strongest remaining limitation relevant to your hypothesis. This turns reading into a usable research argument.

---

## 17. A One-Page Proposal to Discuss with Your Supervisor

### Working Topic

**Condition-Preserving Evidence Selection under Token Budgets for Multilingual RAG**

### Motivation

RAG systems can retrieve passages that are related to a question but fail to preserve the qualifications required for the answer. Under a limited context budget, selecting the most similar passages or compressing text can retain repeated general information while omitting a governing condition. Bangla public-service documents provide a meaningful setting in which to study this problem, while the underlying selection problem is language-independent.

### Research Question

Can a dependency-aware selector produce more condition-complete evidence than relevance-only and existing budgeted-selection methods, at the same measured token budget, without degrading answer quality?

### Proposed Method

Represent evidence as source-linked units with predicted support relations and governing-condition dependencies. Formulate a token-budgeted selection problem and develop a practical approximation or exact-small-pool method. Separate the quality of dependency extraction from the quality of selection through oracle and predicted-label experiments.

### Planned Evaluation

Construct a fresh expert-reviewed Bangla benchmark with direct, paraphrased, condition-heavy, and insufficient-evidence questions. Compare against dense, hybrid, reranked top-k, diversity, coverage, and compression baselines. Evaluate controlled candidate pools and complete pipelines, using multiple generators and an external domain or language test. Measure evidence sufficiency, condition completeness, answer correctness, faithfulness, citations, tokens, latency, and memory.

### Expected Contribution

The intended contribution is a general evidence-selection method and a rigorous characterization of its operating conditions, not merely another Bangla application. Whether it is genuinely novel and beneficial will be determined by the close-prior-work audit and controlled experiments.

### Feasibility

Most experiments can use frozen models, cached retrieval outputs, and lightweight selection on an M2 MacBook Air with 16 GB memory. Expert annotation and careful source preparation are likely to be more important bottlenecks than large-model training.

---

## 18. What to Preserve Before You Take a Break

Before the next incremental update is finished, preserve a reproducible starting point for your future self:

- A labeled conference-version snapshot of the code, without mixing it with new research experiments.
- The exact submitted paper and the source files used to generate it.
- The corpus manifest, source URLs, retrieval dates, document hashes, and redistribution permissions.
- The actual experiment settings, model versions, prompts, tokenizers, and package versions.
- Saved questions, selected evidence, generated answers, judge prompts, and per-question results.
- A record of which questions influenced development and which, if any, remained untouched.
- A short list of unresolved failures and promising examples, including cases where dense retrieval wins.
- This report and a one-page decision about which new research question to pursue first.

Keep source text and search aliases distinguishable in the saved corpus. Future experiments should be able to tell whether a gain came from the selector, the retrieval representation, or a source update.

This report does not modify your application, submit a paper, or schedule future work. It provides the reading map and research plan for when you return.

---

## 19. Bottom Line

There is a credible path from CivicRAG to a stronger journal project, but the next contribution should be **a testable method**, not a larger collection of familiar RAG components.

The strongest direction for your background and machine is:

> **Select fewer tokens while preserving the conditions necessary for a correct answer, and demonstrate exactly when that improves the quality-cost tradeoff.**

Bangla and Bangladesh can provide the research motivation, data, and adoption setting. The journal-level ambition comes from making the problem precise, positioning it against close prior work, and producing evidence that extends beyond your current 30-question comparison.

If the novelty audit closes that route, the next-best alternative is **quality-constrained Bangla/Banglish language routing**, where the research question is not whether translation is possible, but when it is worth its full cost.

# Shihab's Architecture Guide: Simple Explanation to Technical Implementation

## Reading Scope

This is a technical reading document, NOT a presentation script. It revises and deepens the original architecture breakdown for Sections 4.1, 4.2 and 4.4. The original guide remains unchanged.

Each stage starts with intuition, then explains the actual mechanism, rationale and limits. The examples are illustrative unless explicitly identified as actual records. They do not represent a newly executed query or verified government guidance.

Checked against local implementation on 1 October 2026. GitHub links point to the corresponding files on main, not an immutable experimental snapshot. The locally inspected files are the basis for implementation statements.

## 1. The Complete Design in One View

**Simple:** Prepare searchable evidence, find useful passages, check applicability, and give selected text to a language model.

**Technical:** This is a domain-scoped retrieval-augmented generation pipeline. It uses a pretrained dense encoder, a BM25 index, weighted rank fusion, a cross-encoder or lexical fallback, deterministic applicability rules, and local LLM inference.

The live request path and the evaluation path are distinct. RAGAS is not called to approve every citizen-facing answer.

```text
Offline / initialization:
source derivatives -> normalized, structured chunks
                   -> retrieval_text -> embeddings -> Chroma
                   -> retrieval_text -> BM25 index
                   -> content + metadata + IDs -> local JSONL records

Question time:
question + selected domain -> checks -> normalized query
 -> dense results + BM25 results -> weighted RRF
 -> reranking -> applicable evidence + compatible expansion
 -> whole-chunk budget -> prompt -> Qwen -> output handling
```

“Offline” distinguishes preparation from answering a question. BM25 is built during retriever initialization rather than persisted as another Chroma vector collection.

## 2. Read the Figures Correctly

The system architecture figure explains operation. The comparison-boundary figure explains experiments on that operation.

In the architecture, the top and middle bands run mainly left to right. The bottom band runs right to left. Solid arrows represent processing flow; dashed arrows indicate index access.

The figures are conceptual groupings, not strict source-code instruction sequences. For example, evidence text is already accessed before the “resolve content” box, and source-footer formatting occurs within the generator wrapper.

## 3. Offline Data Preparation and Indexing

### 3.1 Source Preparation and Normalization

**Simple:** Both documents and questions are normalized; normalization is not restricted to user input.

**Technical:** Passport/BRTA ingestion calls `parse_markdown()`. It converts CRLF and CR line endings to LF, reads simple front matter, applies Unicode NFC, removes explicit authoring citation markers and selected invisible characters, and strips outer whitespace.

Registration uses a separate `normalize_text()`: NFC, selected zero-width character removal, carriage-return removal, repeated-space/tab reduction and excessive-blank-line reduction. These functions are not identical.

NFC [canonical Unicode normalization] standardizes canonically equivalent character sequences. It does not translate text or automatically correct every OCR mistake. CRLF (`\r\n`) and LF (`\n`) are different internal representations of line breaks; standardizing them helps consistent parsing.

**Where in the diagram?** The top-band “Data preparation: text normalization” box covers document normalization. The middle-band “Normalize query” box covers user text.

**Why:** Reduce avoidable encoding differences and make heading/paragraph processing consistent.

**Code:** `parse_markdown` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/scripts/manage_experimental_domains.py); `normalize_text` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/scripts/prepare_chunks.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/domains/birth_death_registration/scripts/prepare_chunks.py).

### 3.2 Structure-Aware Splitting: What the Algorithm Actually Does

**Simple:** Split according to document organization, not only every N characters. Carry section context with the passage.

**Technical: active passport/BRTA heading-aware v2 route**

1. A regular expression detects Markdown headings with one to six leading hash marks.
2. Heading positions become section boundaries.
3. A heading stack retains parents and removes headings at the same or deeper level when a new heading is encountered.
4. Joining that stack forms a breadcrumb such as `Passport > New application > Documents`.
5. Recognized question-and-answer labels cause an FAQ unit to remain together.
6. Other long sections are split with a nominal 1,400-character body-span limit, preferring paragraph, line or word boundaries.
7. Each emitted piece is prefixed with the document title and its section breadcrumb.
8. Metadata records its normalized-body start/end offsets and section title.

Illustrative structure:

```markdown
# Passport
## New application
### Documents
[long document-requirements text]
## Collection
[collection information]
```

Two pieces split from Documents retain `Passport > New application > Documents`. The Collection section is not silently labeled New application.

The nominal span limit is not a universal maximum for complete stored chunks. Prefixes add characters; detected FAQ units can remain longer. The versioned builder checks embedding input length and rejects oversized input rather than silently relying on truncation.

**Why this helps:** A fragment such as “bring the receipt” is ambiguous without its governing section. Heading context supports retrieval and selector scope matching.

**Why Bangla questions still work:** Chunking occurs before the question and relies primarily on Markdown structure. Bangla headings can be retained as text. At question time, the semantic encoder, keyword matching and selector vocabulary operate over those prepared records.

**Boundary:** This is not perfect semantic segmentation. Poor headings, broad sections, mixed procedures and OCR noise remain possible. The registration corpus uses its own document-type-aware builders, not this exact algorithm for every record.

**Code:** `section_spans`, `spans`, `prepare`, `rechunk` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/scripts/manage_experimental_domains.py).

### 3.3 Retrieval Text Versus Content: Storage and Purpose

**Simple:** Search text helps FIND a passage; evidence content supplies what the model READS.

A chunk record can be represented as:

$$
c_i=(id_i,r_i,e_i,m_i)
$$

Here (r_i) is retrieval text, (e_i) is evidence content, and (m_i) is metadata.

**Actual construction:** Active passport/BRTA content includes title, section breadcrumb and a body slice. Its retrieval text prefixes the domain. Registration starts from content and can append deterministic search aliases.

These are not LLM-generated summaries. Most importantly, we are not embedding aliases INSTEAD OF the content.

**Storage distinction:**

- JSONL retains `id`, `retrieval_text`, `content` and `metadata`.
- Chroma's `embeddings` field stores the vector computed from retrieval text.
- Chroma's `documents` field stores content.
- Chroma also stores the matching ID and metadata.
- The code does not insert two independent document-text columns for retrieval text and content.

```python
vectors = model.encode(retrieval_texts, normalize_embeddings=True)
collection.add(
    ids=chunk_ids,
    embeddings=vectors,
    documents=contents,
    metadatas=metadata_records,
)
```

The arrays align by position during insertion. Later, the ID provides the linkage. Vector similarity itself does not reconstruct exact source text.

**Why:** Search descriptors can improve discoverability while extra aliases need not become answer evidence. They can also add noise; better retrieval is not guaranteed merely by adding aliases.

**Code:** [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/build_index.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/scripts/build_index.py); registration `make_chunk` and `english_retrieval_aliases` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/scripts/prepare_chunks.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/domains/birth_death_registration/scripts/prepare_chunks.py).

### 3.4 Dense Embeddings: From Text to a Searchable Representation

**Simple:** BGE-M3 represents text numerically so differently worded but related passages can be compared.

**Technical:** Tokenization converts text to the encoder's input units. The pretrained encoder maps the input into a dense representation. This pipeline uses the returned sentence embedding and enables L2 normalization.

$$
v_i=\frac{f_\theta(r_i)}{\|f_\theta(r_i)\|_2},
\qquad
v_q=\frac{f_\theta(q)}{\|f_\theta(q)\|_2}.
$$

The same encoder is used for source search text and the query. We do not train its parameters on this corpus during index construction.

**Illustration:** The question “কী কী কাগজপত্র লাগবে?” and a passage headed “প্রয়োজনীয় নথিপত্র” may be semantically close despite wording differences. Their actual similarity must be computed; we are not claiming a measured result for this example.

For normalization alone, a toy vector ((3,4)) becomes ((0.6,0.8)), with length one. Real embeddings have many more coordinates; these two numbers are just a teaching example.

For unit vectors:

$$
\|v_q-v_i\|_2^2=2-2v_q^\top v_i.
$$

Thus exact squared-Euclidean and cosine-based rankings are related for normalized vectors. Do not claim the index builder explicitly selected cosine distance: it does not override Chroma's distance configuration. Approximate index search is not identical to exhaustive mathematical ranking.

**Why BGE-M3:** Its multilingual representation supports semantic matching across Bangla text and English terminology. This is a design rationale, not evidence that it is the best possible encoder.

**Code:** [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/build_index.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/scripts/build_index.py); `_dense_search` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/retrieval/hybrid_retriever.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/retrieval/hybrid_retriever.py).

### 3.5 Chroma Persistence and Source Linkage

**Simple:** Chroma keeps the searchable vector and its linked record; it does not generate an answer.

**Technical:** The configured persistent client opens a domain-specific directory and collection. A dense query returns IDs and requested linked information. The retriever reconstructs results through its ID-to-chunk dictionary.

There are separate configured persistence paths for the three domains. Passport/BRTA use versioned collection names and active JSONL snapshots. The corpus and index must remain synchronized.

Source-derived content is also retained locally. The original files, archived snapshots and normalized chunks are different layers; Chroma documents are not universally byte-identical original PDF contents.

**Code:** `HybridRetriever.__init__` and `_dense_search` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/retrieval/hybrid_retriever.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/retrieval/hybrid_retriever.py).

### 3.6 BM25 Index: Lexical Retrieval, Not Embedding or Generation

**Simple:** BM25 ranks existing passages using matching terms.

**Technical:** At initialization, each chunk's retrieval text is tokenized using NFC normalization, invisible-character removal, word/Bangla token extraction and lowercasing. The lists initialize `BM25Okapi`.

At query time, `get_scores(tokenize(query))` scores the corpus. Results are sorted, limited and filtered to positive scores.

The scoring idea is:

$$
\operatorname{BM25}(q,d)=\sum_{t\in q}\operatorname{IDF}(t)
\frac{f(t,d)(k_1+1)}
{f(t,d)+k_1(1-b+b|d|/\overline L)}.
$$

Term frequency rewards matches with saturation; IDF reflects term rarity; length normalization accounts for passage length. The implementation uses the installed library's defaults rather than explicit parameter tuning.

**Why:** Exact names and procedure terms complement semantic search. But matching words can also appear in the wrong procedure.

**Code:** `tokenize`, constructor, `_bm25_search` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/retrieval/hybrid_retriever.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/retrieval/hybrid_retriever.py).

## 4. Online Domain-Scoped Retrieval

### 4.1 Domain Selection

**Simple:** A passport question searches the selected passport corpus.

**Technical:** The domain configuration chooses the JSONL path, Chroma persistence directory and collection. Domain scoping is configuration-based restriction, not a model autonomously discovering the correct domain.

**Why:** Reduce cross-domain mixing and support independently maintained corpora. It does not distinguish every procedure inside a domain.

### 4.2 Input Policy and Cross-Domain Aggregate Guard

**Simple:** Check supported input and ask for a narrower question for certain combined-service requests.

**Technical:** The visible interface uses a Unicode Bengali-block presence check, not a trained language-identification classifier. A question containing a Bengali-block character is not necessarily entirely natural Bangla.

The pipeline's aggregate guard defines term lists for registration, passport and BRTA. It counts how many domain groups are mentioned and checks for aggregation phrases such as “মোট”, “একসাথে” and “সব মিলিয়ে”.

```text
if mentioned_domain_groups >= 2 AND aggregation_term_present:
    return clarification without retrieval
```

For example, “পাসপোর্ট আর জন্ম নিবন্ধন করতে মোট কত টাকা?” can match the guard. This is deterministic lexical intent screening [explicit string rules], not comprehensive semantic intent detection.

**Why:** Avoid producing unsupported combined totals from independently scoped services. It will miss some paraphrases and is not a universal ambiguity detector.

**Code:** [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/app.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/app.py); `_is_cross_domain_aggregate_query` and `_cross_domain_aggregate_response` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/pipeline.py).

### 4.3 Query Normalization

**Simple:** Standardize the question before matching.

**Technical:** `_normalize_query_text` applies NFC, removes selected zero-width characters, performs a small fixed replacement dictionary, and strips outer whitespace. Examples include selected variants of online wording and a status-to-English-token replacement.

Document normalization already happened during preparation. Query normalization performs the corresponding runtime cleanup; BM25 tokenization and selector matching normalize again for their particular operations.

**Why:** Reduce superficial mismatches. This is not general spelling correction, translation, stemming or an LLM query rewrite.

**Code:** `_normalize_query_text` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/pipeline.py).

### 4.4 Initial Candidate Retrieval

Dense and BM25 return up to 20 IDs each. Overlap means this is not necessarily 40 unique candidates. BM25 may return fewer because non-positive results are omitted.

Twenty is an engineering shortlist setting: enough alternatives for later processing while bounding downstream work. No top-k sweep has been established here to prove it optimal.

The diagram's branches represent two retrieval channels, not a claim that they execute concurrently.

### 4.5 Weighted RRF: Rank Fusion in Detail

**Simple:** Combine how highly each method ranks a passage, rather than adding unlike raw scores.

$$
S(d)=\sum_{m:d\in L_m}\frac{w_m}{50+r_m(d)},
\qquad w_D=0.55,\quad w_B=0.45.
$$

Ranks start at one. A missing channel contributes zero. The top 15 fused candidates proceed.

**Illustrative example:** Dense rank 2 and BM25 rank 5 yields (0.55/52+0.45/55\approx0.01876). The score is not a probability of correctness. The constant 50 smooths differences between adjacent ranks; the weights slightly favor dense.

বাংলায়: দুই search-এর score-এর scale আলাদা। তাই score সরাসরি যোগ না করে, passage কোন তালিকায় কত নম্বরে আছে তা ব্যবহার করি। একই passage দুই তালিকায় থাকলে দুই দিকের contribution পায়।

**Why:** Combine complementary rankings without requiring calibrated raw-score scales. The selected weights are not proven optimal, and fusion need not outperform dense on every metric.

**Code:** `_rrf_fuse` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/retrieval/hybrid_retriever.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/retrieval/hybrid_retriever.py).

### 4.6 Reranking: Joint Query-Passage Scoring

**Simple:** Inspect the shortlist more closely.

**Technical:** The configured cross-encoder receives pairs ((q,r_i)), jointly processes each question and candidate search text, and outputs a relevance score. Unlike precomputed passage embeddings, this scoring depends on the specific query-passage pair.

This is more computationally expensive than reusing passage vectors, so it operates on the fused shortlist. The selected-evidence path requests up to 15 reranked candidates through an explicit override.

When the cross-encoder is unavailable, the implemented fallback adds:

$$
0.05\frac{|T_q\cap T_d|}{\max(|T_q|,1)}
$$

to the incoming score, then sorts. This lexical adjustment is not equivalent to cross-encoder inference and is not a calibrated confidence measure.

**Code:** [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/reranking/reranker.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/reranking/reranker.py); `retrieve` in [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/pipeline.py).

### 4.7 Registration-Specific Rules Are Separate

The cross-encoder is shared. Birth/death-only adjustments can add or subtract hand-written increments for detected query/document-type conditions. Passport and BRTA do not get those registration-specific increments.

Registration correction queries can also receive an existing fee row through `_augment_contexts`. This is separate from the selector's cross-domain-compatible family expansion.

**Why:** These rules came from the earlier registration implementation and depend on its schema. They are not universally learned rules. Their isolated benefit was not measured by the bundled comparison.

### 4.8 Resolving IDs and the In-Memory Chunk Map

**Simple:** The ID links a numerical search match to readable evidence.

**Technical:** JSONL records are loaded and placed into dictionaries keyed by chunk ID. The retriever uses `chunk_by_id`; the pipeline also has `chunks_by_id`.

This avoids scanning files repeatedly to resolve a candidate. It consumes RAM and depends on index/corpus consistency. There is no separate persistent “RAM map dataset”; the map is rebuilt from JSONL on load.

Text is accessed earlier during retrieval and reranking too. The figure's content-resolution box summarizes evidence preparation, not the first source-text access.

## 5. Applicable Evidence and Generation

### 5.1 Reranker Versus Selector

**Simple distinction:** Reranker scores relevance; selector applies compatibility rules and manages final evidence composition.

বাংলা example: “নতুন পাসপোর্টের কাগজপত্র” প্রশ্নের জন্য “পাসপোর্ট সংগ্রহের কাগজপত্র” passage-এ মিল থাকা শব্দ আছে। Reranker সেটিকে কতটা relevant মনে করছে তা score করে। Selector যদি application বনাম collection mismatch চিহ্নিত করে, passage বাদ দিতে পারে।

Do not describe the reranker as merely keyword-based or the selector as a perfect semantic verifier. Both can make imperfect decisions, but their mechanisms differ.

### 5.2 What the Selector Actually Implements

**Technical:** `select_evidence(query,candidates,corpus)` uses vocabulary-based service/action/product/location labels. Section scope is preferred over broad document titles where available.

The procedure includes duplicate-ID removal, heading-only screening, detected scope-conflict rejection, historical-alternative handling, initial priority, checklist coherence, compatible-family expansion, grouping and greedy budgeting.

Initial eligible-candidate priority:

$$
h(q,c_i)=3A_i+S_i+2T_i.
$$

Indicators mark action overlap, service overlap and a fee/document-type match. These are binary rule features, not learned probabilities. Ties preserve incoming candidate order. Subsequent procedural steps can change the eventual selection, so the equation is not the full algorithm.

**Code:** [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/generation/evidence_selection.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/generation/evidence_selection.py).

### 5.3 Expansion and Grouping

**Simple:** Add an existing missing continuation, not an invented answer.

**Technical:** For fee/document questions, the selector derives document-and-parent-section families from retained candidates. It scans the loaded domain corpus for unseen compatible family members, checking scope and type. Checklist expansion is more restrictive about exact section than fee expansion.

Compatible continuations are grouped near their first anchor before budgeting. This prevents tail-appended continuations being excluded merely because unrelated candidates came earlier.

Not every same-document chunk qualifies. Not every appended candidate survives the budget. This is not a second unrestricted semantic search.

### 5.4 Whole-Chunk Budget

$$
|E|\leq6,\qquad\sum_{i:c_i\in E}\operatorname{len}(e_i)\leq14{,}000.
$$

`E` contains chunk records, and `e_i` is the evidence string of each record. Python character length is used, not model token count.

Candidates are considered in order. An oversized chunk is skipped, not truncated; a later smaller chunk can fit. This is greedy selection, not global combinatorial optimization.

**Why:** Bound evidence volume and preserve each included chunk. This does not guarantee the entire source procedure fits. Instructions and question text add further prompt length beyond the evidence count.

### 5.5 No Evidence Versus Some Evidence

No retained evidence produces a clarification without substantive LLM generation. It is not proof that no answer exists in the corpus or in reality.

Nonempty evidence enables generation, but does not certify that the passages completely support the question.

### 5.6 What Is an Evidence-Only Prompt? Is It a System Message?

**Simple:** A package of instructions, question and selected source text.

**Technical:** `build_prompt` starts with the string constant `SYSTEM_INSTRUCTIONS`, modifies some instructions for the selected route, and assembles source blocks with IDs and content. It then includes the question, requested language and evidence in one string passed to `ChatOllama.invoke`.

The variable name SYSTEM_INSTRUCTIONS does not mean this code sends a separately structured system-role message. Describe it as system-style instructions within an assembled prompt.

```text
Instructions:
  use supplied evidence; preserve conditions; avoid mixing procedures
Question:
  the normalized user question
Answer language:
  Bangla
Retrieved evidence:
  [Source 1] id=...
  actual content
  [Source 2] id=...
  actual content
Answer:
```

The selected route says source order is not authority. It asks the model to preserve fee categories and conditions and to identify missing information.

বাংলায়: source-এ “প্রযোজ্য ক্ষেত্রে” থাকলে সেটা “সবার জন্য বাধ্যতামূলক” বানানো যাবে না। Question plus selected content মানে প্রশ্ন এবং বাছাই করা passage; পুরো database নয়।

**Boundary:** Prompt instructions guide the model; they do not mathematically prevent unsupported generation or erase pretrained knowledge.

**Code:** [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/generation/ollama_generator.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/src/generation/ollama_generator.py).

### 5.7 Generation and Output Handling

The evaluated generator is Qwen3:8b served through Ollama using ChatOllama. Qwen3 thinking is disabled in the wrapper. The documented comparison uses temperature 0.05, top-p 0.9, 1,200 maximum output tokens, and an 8,192-token selected-route context setting, with repetition controls.

These are generation controls, not correctness guarantees or experimentally proven optima. The explicit comparison model can differ from legacy config defaults.

The wrapper canonicalizes the source footer. The pipeline applies heuristic language rejection and a warning for length-limited completion. It does not run a separate factual-verification model before every answer.

Even an exact stored FAQ question follows retrieval and LLM generation in this route; it is not automatically copied verbatim. Legacy controlled-answer branches exist but are bypassed by the enabled selected-evidence route.

## 6. How Section 4.4 Connects to the Architecture

The implementation equations describe operations within existing boxes, not additional architecture stages:

- Vector normalization: passage and query BGE-M3 encoding.
- BM25 scoring: lexical search channel.
- Weighted RRF: rank-merging box.
- Cross-encoder and registration adjustments: reranking stage.
- Applicability priority: part of the selector.
- Whole-chunk budget: final evidence preparation.

For understanding, keep the difference between **a mathematical description**, **a chosen numeric setting**, and **a measured improvement**. An equation can correctly describe implemented behavior without proving that its settings are optimal.

## 7. Evaluation Boundary: Technical Meaning

The matched answer comparison holds corpus access, questions, generator and generation settings comparable while changing the retrieval/selection bundle. Simple RAG uses dense top-six and the same whole-chunk budget and prompt instructions, without CivicRAG's RRF/reranking/selector expansion.

The baseline's `selected_evidence=True` flag selects the generator prompt, not the selector function.

The retrieval-only comparison stops before reranking, boosts, selection and generation. BM25, Dense and RRF scores therefore do not directly measure complete chatbot accuracy. RAGAS scores saved answers separately; it is not part of the live architecture.

**Code:** [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/run_simple_matched.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/scripts/run_simple_matched.py); [Local code](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/run_current_30q_retrieval_only.py) | [GitHub](https://github.com/Shihabsarker93/civic_ai_rag/blob/main/scripts/run_current_30q_retrieval_only.py).

## 8. Technical Vocabulary to Use Accurately

- **Structure-aware segmentation:** use headings and document units when forming chunks.
- **Canonical Unicode normalization:** standardize equivalent encoded character forms.
- **Dense semantic retrieval:** compare learned numerical text representations.
- **Lexical retrieval:** rank using matching terms.
- **Rank fusion:** combine result positions from multiple search channels.
- **Cross-encoder reranking:** jointly score a query and passage.
- **Deterministic scope screening:** apply explicit service/action/condition rules.
- **Compatible-family expansion:** add stored related sections under constrained provenance.
- **Greedy whole-chunk budgeting:** accept eligible chunks in order if limits permit.
- **Prompt assembly:** package instructions and evidence for generation.
- **Source traceability:** retain a route back to supplied evidence, not automatic claim verification.

## 9. What the Implementation Does Not Establish

There is no claim here that the exact top-k, fusion weights or priority weights are optimal; that all normalization repairs OCR; that all chunks are complete procedures; that the selector is a learned classifier; or that source IDs independently verify every answer claim.

These distinctions are technical precision, not reasons to dismiss the system. The implemented contribution is the integrated, source-linked retrieval and generation workflow and its documented evaluation.

## Related Documents

- [Original beginner architecture guide](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/presentation/Shihab_Architecture_Breakdown_and_Script.md)
- [Data and implementation questions, with real metadata and corpus paths](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/presentation/Team_Implementation_Questions_Explained.md)
- [Separate natural speaking script](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/presentation/Shihab_Natural_Architecture_Script_Running_Example.md)

This document intentionally contains no speaking script. Use it to understand the mechanisms before deciding how much detail belongs in your presentation.

# Implementation Questions: Data, Hashes, Retrieval and Traceability

Checked against local code, active domain configurations and sample JSONL records on 30 September 2026. This describes the evaluated selected-evidence route and distinguishes active ingestion from later cleanup candidates. Examples explain software behavior, not current government rules.

## SHA-256: What, Why and Where?

SHA-256 produces a 256-bit hash [a repeatable fingerprint of input bytes], commonly written as 64 hexadecimal characters. The same bytes produce the same hash; a changed file will normally produce a different hash.

It is NOT encryption, a source URL, an embedding, or proof that information is true. It cannot prove that a Markdown derivative faithfully represents its PDF.

Our project uses it for several different purposes:

- Source integrity: record the hash of a supplied file and compare it with its archived snapshot before rechunking.
- Normalized-body integrity: separately hash the processed text, because processed text differs from raw file bytes.
- Document identifiers: passport/BRTA document IDs use the domain plus the first 16 hexadecimal characters of the hash of the NFC-normalized RELATIVE PATH. This is a path-derived identifier, not the full content hash.
- Experimental consistency: save hashes of relevant code, configurations and corpus files; check them before matched runs.
- Thesis traceability: record which input files and evaluation runs supplied report values.

Benefit: detect accidental changes, trace a result to specific inputs, and avoid comparing systems whose corpus or settings changed unnoticed. A manifest records a state; enforcement requires running the comparison checks.

Code: [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:18): `digest`, `prepare`, `rechunk`. [scripts/run_simple_matched.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/run_simple_matched.py:46): comparison checks. [scripts/build_thesis_evidence.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/build_thesis_evidence.py:39): thesis evidence manifest.

Simple defense answer: "We use SHA-256 as a file fingerprint to check source and experiment consistency, not to verify factual correctness."

## 1. What Exactly Is Stored in ChromaDB?

It is not a mixed pile of unrelated vectors and evidence. A collection contains linked records identified by chunk ID. Our insertion supplies four aligned arrays:

```python
collection.add(
    ids=[c["id"] for c in batch],
    documents=[c["content"] for c in batch],
    metadatas=[c["metadata"] for c in batch],
    embeddings=vectors,
)
```

At position j in each array are the ID, evidence text, metadata and vector for the SAME chunk. Chroma supports these fields directly; this is visible in the actual insertion code.

An active example, abbreviated:

```text
id:
  passport_6e87d0783a373593_v2_0002

document/content:
  5 Steps to your e-Passport
  5 Steps to your e-Passport > Overview
  [the source-derived Overview section]

embedding:
  normalized BGE-M3 vector computed from retrieval_text

metadata:
  doc_id: passport_6e87d0783a373593
  section_title: 5 Steps to your e-Passport > Overview
  body_start: 30
  body_end: 147
  ...other fields
```

The vector is calculated from search text, but the Chroma document field stores content. Search text also remains in JSONL; it is not inserted as an additional dedicated Chroma field by this code. BM25 is outside Chroma.

Code: [scripts/build_index.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/build_index.py:52) and [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:233). Read these files; do not run an index rebuild just to inspect them, because rebuilding changes stored index state.

## 2. How Does BM25 Generate an Answer?

**BM25 does not generate answers. It ranks existing passages.**

The implemented sequence is:

1. At retriever initialization, load the domain chunks and tokenize each chunk's search text.
2. Build `BM25Okapi(tokenized_corpus)`.
3. Tokenize the user's question.
4. Calculate a BM25 score for each passage using `get_scores`.
5. Sort passages by score and keep up to the requested limit, excluding scores less than or equal to zero.
6. Return the corresponding chunk IDs.
7. In CivicRAG, combine BM25 ranks with dense ranks using RRF.
8. Rerank, screen applicability, expand eligible related sections and apply the evidence budget.
9. Give the actual selected text and question to Qwen, which writes the answer.

BM25 rewards matching terms according to factors including term frequency, rarity across documents and passage length. It does not understand all meanings or write new sentences.

Code: [src/retrieval/hybrid_retriever.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/retrieval/hybrid_retriever.py:63) (`_bm25_search`); its constructor builds BM25. The final route is [src/pipeline.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py:115).

The retrieval-only BM25 evaluation stops at ranking and scoring retrieval results. It does NOT run Qwen or produce a chatbot answer.

## 3. At Which Stages Do We Apply Unicode Normalization?

There is more than one stage:

- Registration preparation: `normalize_text` uses NFC, removes selected invisible characters and normalizes whitespace. [domains/birth_death_registration/scripts/prepare_chunks.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/scripts/prepare_chunks.py:62)
- Passport/BRTA Markdown parsing: `parse_markdown` standardizes line endings, parses metadata, then uses NFC and removes selected markers/invisible characters. [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:42)
- Query preparation: `_normalize_query_text` uses NFC, removes selected invisible characters and applies a small replacement dictionary. [src/pipeline.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py:1161)
- BM25 tokenization: `tokenize` uses NFC before splitting and lowercasing. [src/retrieval/hybrid_retriever.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/retrieval/hybrid_retriever.py:19)
- Selector matching: `norm` uses NFC and lowercase for consistent vocabulary matching. [src/generation/evidence_selection.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/generation/evidence_selection.py:13)

These are text-processing operations, not LLM calls. NFC does not translate Bangla, correct all spelling/OCR errors, or convert every legacy Bijoy-encoded document.

## 4. What Are Unicode NFC and Line-Ending Normalization?

### NFC

Unicode allows certain equivalent visible characters to be represented by different code-point sequences [different internal character encodings]. NFC means Normalization Form C. It standardizes canonically equivalent sequences, including composition where Unicode defines it.

A simple non-Bangla illustration is an accented letter represented as a base letter plus a combining accent versus an equivalent composed letter. They can look identical while their underlying strings differ.

Why use NFC? Reduce avoidable mismatches in comparisons, tokenization and rule matching. It does not mean all similar-looking letters become identical.

### Line endings

Pressing Enter inserts a line-ending sequence. Common representations are:

```text
LF:    \n
CRLF:  \r\n
CR:    \r
```

The passport/BRTA parser uses:

```python
text = text.replace("\r\n", "\n").replace("\r", "\n")
```

Thus `Heading\r\nBody` becomes `Heading\nBody`. Both represent two lines, but the stored representation becomes consistent. This is NOT joining every line into one paragraph.

Why? Heading detection, front-matter parsing, blank-line splitting and normalized-body offsets become more predictable across file origins.

Important implementation distinction: registration's `normalize_text` uses `text.replace("\r", "")`. This handles CRLF by leaving LF, but a bare CR in a string passed directly to that function would be removed rather than replaced by a newline. Do not describe the two functions as identical. It also reduces repeated spaces/tabs and three-or-more newlines to two.

Locations: the two preparation functions linked in Question 3.

## 5. What If the User Asks an Exact FAQ Question?

In the final selected-evidence route, there is no exact-question shortcut that simply returns the stored FAQ answer.

The question still goes through retrieval, reranking and selection. An exact FAQ question may help the matching FAQ rank highly, but that does not guarantee it is the only selected passage.

If the FAQ and several other chunks enter the prompt, Qwen receives them together. It can paraphrase, combine supported material or closely reproduce the FAQ. The prompt tells it not to mix incompatible conditions, but that is not a guarantee.

If only one FAQ is selected, the model still generates from that passage. It is not necessarily a verbatim copy.

The repository contains older controlled-answer functions; `ask` routes the enabled CivicRAG selected-evidence path to `_ask_selected_evidence` before those branches. Code: [src/pipeline.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py:57); prompt: [src/generation/ollama_generator.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/generation/ollama_generator.py:45).

## 6. What Are Source Spans and Audit Flags?

### Source spans

In active passport/BRTA chunks, `body_start` and `body_end` are character offsets into the NORMALIZED Markdown body, not PDF page coordinates or raw-file byte offsets.

For the real Overview chunk above:

```python
body[30:147]
```

recovers its source-body slice after applying the same parser. Start is inclusive, end is exclusive. The title and section breadcrumb prefixed to chunk content are outside that slice.

Why useful? Inspect where a passage came from, check coverage, and trace a chunk back through a snapshot. The unchanged snapshot hash and the same normalization procedure are necessary for reliable reconstruction.

The rechunker verifies that concatenating its section spans recovers the normalized body before skipping blank-only output units.

Later cleanup-candidate code also has `context_spans` for inherited context. Do not claim those fields are present in every active chunk: current passport/BRTA configs reference heading-aware v2 corpora.

Code: [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:79) and [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:102). Candidate-only context spans: [scripts/clean_service_corpora.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/clean_service_corpora.py:175).

### Audit flags

Audit flags are review warnings, not correctness labels. The ingestion script creates them from explicit tests and copies the document's flags into each chunk's metadata.

Implemented examples:

- `original_match_unresolved`: no original PDF filename match was found by the implemented name-matching procedure.
- `citation_markers_removed_from_derived_text`: authoring citation markers were detected and removed from derived text.
- `no_web_address`: no recognized web-address pattern was found in the supplied text.
- `nonstandard_metadata_layout`: the text did not begin with the expected front-matter marker.
- `dated_document_review_applicability`: the filename matched the script's date-like pattern; applicability needs review.
- `long_document_check_ocr`: normalized body exceeded 50,000 characters; length triggers review, not proven OCR failure.
- `temporary_service_notice`: the filename matched the implemented downtime term.

They help locate records needing inspection and preserve known concerns. A date flag does not prove a rule is obsolete; a missing-URL flag does not prove the document is false.

The selector checks the historical flag under specified alternative/scope conditions. It does NOT discard every flagged chunk, and it does not certify the remaining chunks as reliable.

Code: [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:158); selector historical handling: [src/generation/evidence_selection.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/generation/evidence_selection.py:165).

## 7. Does Heading-Aware Chunking Add the Heading to Every Chunk Under It?

For the active passport/BRTA heading-aware v2 ingestion, yes: each emitted chunk is prefixed with the document title and current section breadcrumb [parent and child heading names].

```python
content = f"{title}\n{section}\n\n{body_slice}"
retrieval_text = f"{domain}\n{content}"
```

If a long section is split into several chunks, they retain that section context. Encountering a new sibling heading updates the heading stack instead of attaching the old sibling's heading.

Detected FAQ question-answer units are kept together by `section_spans`; oversized units are subject to the embedding input-limit check rather than silently cut there.

This does not mean all source files have good headings or that all domain preparation follows an identical implementation. Registration has its own document-type-aware preparation functions.

## 8. What Exactly Is Search Text? Is It a Summary?

**It is not an LLM-generated summary. We generally embed the chunk content WITH search-oriented additions, not aliases instead of the content.**

Active passport/BRTA format:

```text
domain
document title
section breadcrumb

actual source-body slice
```

Active registration's `make_chunk` begins with normalized content, then can append deterministic retrieval aliases [rule-selected alternative search terms]. The aliases are also recorded as `search_aliases` metadata.

Why? Add service/heading context and alternative terminology so a useful passage can match different wording. Possible benefit is better discoverability; extra aliases can also introduce noise, so improvement is not guaranteed.

The distinction "content versus search text" means added retrieval aliases are not automatically presented as source facts. However, content itself can include structured source descriptors or supplied keywords; do not describe it universally as untouched PDF prose.

How is the vector linked to the exact chunk? The index builder calculates a vector for each chunk's `retrieval_text`, then inserts that vector with the same chunk's ID, content and metadata in aligned arrays. Passport/BRTA building checks that indexed IDs equal active chunk IDs. Runtime IDs then look up the same chunk record.

This is ID-based linkage, not the vector remembering or reconstructing exact text. It relies on keeping the corpus and index versions consistent.

Code: [domains/birth_death_registration/scripts/prepare_chunks.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/scripts/prepare_chunks.py:143) and `english_retrieval_aliases` at line 245; [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:118); [scripts/build_index.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/build_index.py:52).

## 9. Is Chunk ID the Same as Document ID? What Are the Fields?

No. One document can have many chunks.

Real example:

```text
chunk id:    passport_6e87d0783a373593_v2_0002
document id: passport_6e87d0783a373593
```

Here `v2` marks the chunking generation and `0002` the piece number. In these passport/BRTA records, metadata `doc_id` and `document_id` contain the same document identifier. They are not equal to the top-level chunk `id`.

Top-level chunk fields: `id`, `content`, `retrieval_text`, `metadata`.

Actual passport/BRTA example metadata fields:

```text
domain, doc_id, document_id, title, section_title, document_type,
source_path, source_relative_path, snapshot_path, source_sha256,
original_paths, document_date, date_verified, audit_flags,
experimental, body_start, body_end, source_url,
chunking_version, faq_unit
```

`original_paths` is a JSON-encoded string; `audit_flags` is a comma-separated string in these records. The application retains scalar-compatible metadata for insertion.

The actual registration FAQ example has a different schema:

```text
doc_id, title, title_en, source_url,
issuing_authority, issuing_authority_en, department, department_en,
system, last_updated, language, doc_type, domain, country, total_faqs,
source_path, document_type, category, faq_number, service, service_scope,
search_aliases, chunking_version, content_token_count,
retrieval_token_count, embedding_model_max_tokens
```

These are example field sets, not a promise every record contains every field. For example, the registration record's metadata domain is `civil_registration`, while its configured pipeline domain is `birth_death_registration`; these different fields should not be conflated.

Active chunk files:

- [domains/birth_death_registration/data/interim/birth_death_chunks.jsonl](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/birth_death_registration/data/interim/birth_death_chunks.jsonl)
- [domains/passport/data/interim/active_20260919_063632_508964.jsonl](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/passport/data/interim/active_20260919_063632_508964.jsonl)
- [domains/brta/data/interim/active_20260919_062310_302306.jsonl](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/domains/brta/data/interim/active_20260919_062310_302306.jsonl)

The authoritative choice is each domain's `config.json` -> `data.chunk_output_path`. Versioned filenames can change after a deliberate rebuild/publication.

## 10. Is There One Chroma Database for All Three Domains?

The current configuration uses three separate persistent storage directories, with a configured collection per active domain version:

- Registration: `domains/birth_death_registration/data/processed/chroma_birth_death_bge_m3`; collection `birth_death_registration_chunks`.
- Passport: `domains/passport/data/processed/chroma_experimental`; collection `passport_20260919_063632_508964`.
- BRTA: `domains/brta/data/processed/chroma_experimental`; collection `brta_20260919_062310_302306`.

These paths are relative to the repository root shown in the clickable chunk links above. Each is passed to `chromadb.PersistentClient(path=...)`. Chroma could support another organization, but this is ours.

Why? Keep search domain-scoped and allow independently maintained corpora and index versions.

Passport/BRTA rebuilding creates a versioned collection, validates ID coverage, writes the active JSONL, and publishes the configuration only after the build completes. Prior collections/configuration backups support rollback. Registration's generic index builder instead deletes/recreates its named collection; do not claim all three domains have identical version-publication behavior.

Code: [scripts/manage_experimental_domains.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/manage_experimental_domains.py:195); [scripts/build_index.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/build_index.py:63); each domain's `config.json`.

## 11. What Is the In-Memory Chunk Map?

It is a Python dictionary [a fast ID-to-record lookup] created in RAM when the pipeline loads.

```python
self.chunks = self._load_jsonl(...configured_chunk_path...)
self.chunks_by_id = {str(chunk["id"]): chunk for chunk in self.chunks}
```

The retriever also constructs its own `chunk_by_id` dictionary from the same chunk list.

Example:

```text
"passport_..._v2_0002" -> its complete JSONL record
```

Benefit: after a search returns an ID, code can recover text and metadata directly instead of scanning the whole JSONL again or rereading files for each candidate.

It is not a separate dataset file. The persistent dataset is the JSONL listed in Question 9; the map is a temporary runtime representation reconstructed from it. It consumes RAM and must stay consistent with the index.

Consumers: dense result reconstruction, BM25 result construction, fused-result construction, and pipeline helpers that resolve known chunk IDs.

Code: [src/pipeline.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py:32) and [src/retrieval/hybrid_retriever.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/retrieval/hybrid_retriever.py:50). The selector receives the full chunk list as its corpus for compatible expansion; that does not mean it performs a new dense search for each expansion.

## 12. How Can the Selector Append Evidence?

First, say "screen incompatible evidence," not "remove unreliable chunks." The selector is not a general reliability verifier.

It receives the question, retrieved candidates and the already loaded domain corpus:

```python
select_evidence(search_query, candidates, self.chunks)
```

For fee/document questions, it can find an eligible family [same document and parent section] among selected candidates, then inspect the local corpus for related chunks not already seen.

Example: a retrieved fee section has a compatible sibling fee category in the same document and parent section. That sibling might not have been in the initial top results. The selector can add it if its detected service, action, product, location and type are compatible.

Checklist expansion is more restrictive about the exact section. It does not indiscriminately concatenate every checklist in a document.

It appends EXISTING text and metadata, never invents a new passage. Related members are grouped near their anchor, then the six-passage/14,000-character budget applies. An appended candidate is not guaranteed to fit the final prompt.

Do not confuse this shared expansion with registration-only `_augment_contexts`, which can add a known correction-fee row before the selector.

Code: [src/generation/evidence_selection.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/generation/evidence_selection.py:104) (`family`); [src/generation/evidence_selection.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/generation/evidence_selection.py:197) (expansion); [src/pipeline.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/src/pipeline.py:115) (caller).

## 13. What Does Frozen State / Frozen Evidence Manifest Mean?

Frozen state means a recorded experimental snapshot [the versions and files used for a particular experiment]. It does not mean the operating system locks every file or that development can never continue.

The run plan records code/corpus/config hashes and a Git revision. The matched baseline runner checks relevant hashes against the earlier CivicRAG plan before proceeding. This helps ensure both runs use matching underlying inputs.

A manifest [an inventory of evidence and versions] records which artifacts underpin reported values. The thesis evidence builder checks the paired plans and hashes, then records corpus files, counts and run information.

Relevant files:

- [docs/evaluation/chunk_order_fixed_qwen3_30q_2026_09_23/plan.json](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/evaluation/chunk_order_fixed_qwen3_30q_2026_09_23/plan.json)
- [docs/evaluation/simple_matched_qwen3_30q_2026_09_24/plan.json](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/evaluation/simple_matched_qwen3_30q_2026_09_24/plan.json)
- [docs/thesis_final_2026_09_24/evidence_manifest.json](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/thesis_final_2026_09_24/evidence_manifest.json)
- [scripts/build_thesis_evidence.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/build_thesis_evidence.py:39)
- [scripts/run_simple_matched.py](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/run_simple_matched.py:46)

Why? Later improvements should not silently change what the thesis's saved experiment actually measured. A newer website or latest Git commit is not automatically identical to the frozen run.

A frozen manifest is NOT a gold-answer dataset, independent annotation, proof of factual accuracy, or a guarantee that every rerun produces bit-identical model output. It records reproducibility evidence; it does not eliminate model/hardware variability.

## One-Minute Summary for Your Teammate

"We preserve source snapshots and hashes so we can trace versions. Each chunk keeps source-derived text, search text and metadata under a unique chunk ID. Search text is embedded and linked to the evidence in Chroma; BM25 separately searches matching words. Neither search method writes the answer. The pipeline retrieves and reranks candidates, uses rules to screen procedure compatibility and optionally add existing related sections, then gives bounded evidence to Qwen. Exact FAQ questions still follow this generation path. The saved manifest records which corpus, code and settings were used for the reported comparison."


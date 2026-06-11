# Civic.ai RAG Codebase Onboarding Report

Prepared for thesis teammates who need to understand what has been built, why it was built this way, how the code is organized, and how to explain the system during P2/P3 discussion.

## 1. Repository and Current Branch

Main GitHub repository:

https://github.com/Shihabsarker93/civic_ai_rag

Current working branch:

https://github.com/Shihabsarker93/civic_ai_rag/tree/feature/add-birth-death-domain

Important note: domains are not separated by Git branches. The repository is designed as one multi-domain government-service RAG system. Each government-service domain gets its own folder under `domains/`. Git branches are only for feature development, for example `feature/add-birth-death-domain`, `feature/add-brta-domain`, or `feature/add-passport-domain`.

At the time of this report, the active implemented domain is:

```text
domains/birth_death_registration
```

The current codebase is focused on Bangladeshi birth and death registration documents. Passport and BRTA should not be treated as part of the active vector database right now.

## 2. What We Have Built

We have built a local Retrieval-Augmented Generation system for Bangladeshi government-service guidance. The active chatbot answers questions about birth and death registration using local documents, source IDs, retrieval scores and official/source links where available.

The system has two answer modes in the frontend:

```text
Simple RAG
CivicRAG (ours)
```

Simple RAG is a baseline. It uses dense vector retrieval and sends the retrieved chunks to the selected local LLM.

CivicRAG is the proposed thesis pipeline. It uses document-type-aware chunks, dense retrieval, BM25 sparse retrieval, RRF rank fusion, reranking, intent-aware boosting, safe controlled answer paths and local LLM fallback.

The local LLM backends available for comparison are:

```text
llama3.2
llama3
qwen2.5:7b
```

Important interpretation: our thesis system is not one of these LLMs. The proposed system is the CivicRAG pipeline. The LLM is only the final answer generator used after retrieval.

## 3. High-Level Pipeline

The current pipeline can be understood as:

```text
Raw government data
    ↓
Manual / semi-manual cleaning
    ↓
Domain folder: birth_death_registration
    ↓
Document-type-aware chunking
    ↓
Chunk metadata + source URLs
    ↓
Two text versions per chunk
    ↓
retrieval_text for searching
answer evidence/content for generation
    ↓
Embedding with BAAI/bge-m3
    ↓
Vector index in ChromaDB
    ↓
BM25 sparse index
    ↓
User query
    ↓
Language + intent detection
    ↓
Hybrid retrieval
Dense search + BM25 search
    ↓
RRF fusion
    ↓
BGE reranking or lexical fallback
    ↓
Civic intent boosting
    ↓
Top evidence chunks
    ↓
Safe answer path check
    ↓
Controlled answer if possible
    ↓
Local LLM fallback if needed
    ↓
Bangla language guard
    ↓
Final answer with source IDs, scores and links
```

## 4. Why This Architecture Exists

Government-service QA is different from a casual chatbot. The answer must be factual, grounded and explainable. For example, if a citizen asks about birth certificate correction or registration fees, a fluent but unsupported answer is dangerous.

The system is therefore designed around three priorities:

```text
1. retrieve the correct evidence
2. generate only from that evidence
3. expose the source so a human can verify it
```

This is why we use RAG instead of only an LLM. A local LLM may know general facts but may hallucinate specific government rules, fees, forms or procedures. RAG reduces that risk by forcing the answer to be based on our indexed documents.

## 5. Important Code Map

### Application Entry Point

```text
app.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/app.py

This file runs the local browser-based chatbot. It creates a small HTTP server, serves the frontend, receives user questions and calls `CivicRAGPipeline`.

The frontend has:

```text
method selector: Simple RAG / CivicRAG (ours)
model selector: llama3.2 / llama3 / qwen2.5:7b
chat window
source display
official/source links display
```

### Main RAG Orchestration

```text
src/pipeline.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/src/pipeline.py

This is the most important file. It connects retrieval, reranking, safe answer logic and LLM generation.

It decides:

```text
which retrieval method to use
which contexts should go to generation
whether a safe controlled answer can be used
whether the LLM should be called
whether the answer violates language rules
which sources should be returned
```

### Hybrid Retriever

```text
src/retrieval/hybrid_retriever.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/src/retrieval/hybrid_retriever.py

This file implements:

```text
dense vector search using BGE-M3 embeddings and ChromaDB
BM25 lexical search over retrieval_text
weighted RRF rank fusion
dense-only baseline
BM25-only baseline
```

### Reranker

```text
src/reranking/reranker.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/src/reranking/reranker.py

This file reranks retrieved chunks. It tries to use a BGE cross-encoder reranker when available. If not available, it uses a lexical fallback and domain-specific boosts.

It contains logic for query types such as:

```text
fee questions
correction questions
how-to application questions
lost certificate questions
document requirement questions
online visibility questions
single parent / special case questions
```

### Local LLM Generator

```text
src/generation/ollama_generator.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/src/generation/ollama_generator.py

This file calls local Ollama models through LangChain Ollama. It builds the final prompt and enforces important generation instructions:

```text
answer only from retrieved evidence
answer Bangla queries in Bangla
answer English queries in English
do not treat retrieval aliases as factual evidence
do not invent portal names or extra requirements
for how-to questions, give direct steps
```

### Chunk Preparation

```text
domains/birth_death_registration/scripts/prepare_chunks.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/domains/birth_death_registration/scripts/prepare_chunks.py

This file converts the cleaned JSON and Markdown domain data into retrieval-ready chunks.

It does:

```text
NFC Unicode normalization
zero-width character removal
FAQ JSON chunking
Markdown heading-based chunking
legal section chunking
fee table and fee-row chunking
OCR guideline and notice chunking
metadata creation
retrieval alias generation
token-count auditing using the BGE-M3 tokenizer
duplicate chunk ID detection
```

### Build Vector Index

```text
scripts/build_index.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/scripts/build_index.py

This file builds the ChromaDB vector database. It embeds `retrieval_text` but stores clean `content` as the document.

This is very important:

```text
retrieval_text = optimized for search
content = original/source evidence shown to LLM and users
```

### Query from Terminal

```text
scripts/query_rag.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/scripts/query_rag.py

This lets us test the RAG pipeline without the browser UI.

### Evaluation Scripts

```text
scripts/evaluate_retrieval.py
scripts/evaluate_generation.py
scripts/run_p2_experiments.py
scripts/run_reduced_eval_plan.py
scripts/evaluate_collected_faq_pairs.py
scripts/run_collected_faq_actual_answers.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/tree/feature/add-birth-death-domain/scripts

These scripts produce retrieval and generation evaluation outputs for P2-level comparison.

### Evaluation Metrics

```text
src/evaluation/metrics.py
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/src/evaluation/metrics.py

This file implements:

```text
Recall@k / Hit@k
Precision@k / Context Precision@k
MRR
nDCG@k
Token F1
Cosine similarity
```

## 6. Domain Data Organization

The active domain config is:

```text
domains/birth_death_registration/config.json
```

GitHub:

https://github.com/Shihabsarker93/civic_ai_rag/blob/feature/add-birth-death-domain/domains/birth_death_registration/config.json

The domain has the following important data locations:

```text
domains/birth_death_registration/data/raw/json
domains/birth_death_registration/data/raw/md
domains/birth_death_registration/data/interim/birth_death_chunks.jsonl
domains/birth_death_registration/data/processed/chroma_birth_death_bge_m3
domains/birth_death_registration/data/evaluation
```

Current chunk file:

```text
domains/birth_death_registration/data/interim/birth_death_chunks.jsonl
```

The current indexed chunk count is:

```text
187 chunks
```

Current chunk type breakdown:

```text
legal_rules: 45
legal_act: 30
application_process: 30
faq: 26
correction_process: 12
guidelines_ocr: 12
portal_summary: 9
general_guidance: 8
fee_row: 7
correction_notice_ocr: 6
faq_preamble: 1
fees_table: 1
```

All indexed chunks are Bangla:

```text
language: bn
```

Service scope:

```text
birth_death: 116 chunks
birth: 71 chunks
```

## 7. Why We Use Typed Chunks

The documents are not all the same type. Some are FAQ-style. Some are legal rules. Some are application process pages. Some are tables. Some are OCR or notice-style content.

If we use only one generic chunking method, important structure is lost. For example:

```text
FAQ should preserve question-answer pair
legal documents should preserve section or rule number
fee tables should preserve individual rows
application process documents should preserve steps/headings
OCR notices should preserve instruction blocks
```

So the chunker assigns a `document_type` to each chunk. Examples:

```text
faq
legal_rules
legal_act
application_process
correction_process
fee_row
fees_table
guidelines_ocr
correction_notice_ocr
portal_summary
```

This helps retrieval and reranking. For example, if the user asks “কীভাবে জন্ম নিবন্ধন করব?”, application process chunks should be preferred over legal-background chunks.

## 8. Why We Have retrieval_text and Answer Evidence

Each chunk has two useful text forms:

```text
retrieval_text
content
```

`retrieval_text` is used for searching. It may include aliases, English keywords and alternate phrasings. For example:

```text
birth certificate
birth registration
how to apply
জন্ম নিবন্ধন আবেদন
জন্ম সনদ
```

These aliases help cross-lingual and code-mixed retrieval. A user may ask in English, Bangla, or mixed Bangla-English.

`content` is the clean answer evidence. This is what the LLM sees as factual source content. The aliases are not treated as evidence.

This design prevents a major RAG problem: if search aliases are sent as factual content, the LLM may treat them as real source statements. Our pipeline avoids that by using aliases only for retrieval.

## 9. Why We Use BAAI/bge-m3

The embedding model is:

```text
BAAI/bge-m3
```

Reasons:

```text
it is multilingual
it works better for Bangla than English-only embedding models
it supports dense retrieval
it is suitable for cross-lingual search
it can run locally
```

The code also audits token count using the BGE-M3 tokenizer during chunk preparation. This reduces the risk of feeding oversized chunks to the embedding model.

Config:

```text
"embedding": {
  "provider": "sentence_transformers",
  "model": "BAAI/bge-m3",
  "device": "cpu",
  "normalize_embeddings": true,
  "local_files_only": true
}
```

## 10. Why We Use BM25

Dense retrieval is good for semantic similarity. BM25 is good for exact keyword matching.

For government documents, exact terms matter:

```text
BDRIS
১৬১৫২
জন্ম তারিখ
ফি
ধারা
বিধি
সনদের প্রতিলিপি
```

Dense retrieval may understand meaning, but BM25 is useful when exact legal or procedural terms appear in both the query and the document.

Even though dense-only currently scores highest on the 58-question evaluation set, BM25 is still useful as an alternative retrieval design and as a safety net for exact terms.

## 11. Why We Use RRF

RRF means Reciprocal Rank Fusion. It combines ranked results from multiple retrievers without directly comparing raw scores.

Dense scores and BM25 scores are not naturally on the same scale. So instead of adding raw scores, RRF uses ranks:

```text
RRF(d) = sum over retrievers of weight_r / (k + rank_r(d))
```

In our config:

```text
rrf_k = 50
dense weight = 0.55
BM25 weight = 0.45
```

If the same chunk appears high in both dense search and BM25 search, RRF tends to promote it. If a chunk appears only in one retriever but very high, it can still survive.

Important clarification: RRF does not only find common chunks. It combines rankings. Common high-ranked chunks often get a boost, but unique chunks can also appear if they are strongly ranked by one retriever.

## 12. Why We Use Reranking and Intent Boosting

After dense and BM25 results are fused, we still need to decide which evidence chunks should be passed to answer generation.

The reranker handles that. It can use:

```text
BGE cross-encoder reranker
lexical fallback
domain-specific boosts
```

Domain-specific boosts are not magic. They are simple engineering rules based on observed government-service query types.

Examples:

```text
if query asks about fees, fee_row and fees_table chunks are boosted
if query asks how to apply, application_process chunks are boosted
if query asks about correction, correction_process chunks are boosted
if query asks about lost certificate, legal_rules section about certificate copy is boosted
```

This makes the system more explainable because we can say exactly why a certain type of chunk was preferred.

## 13. Safe Answer Paths

CivicRAG has controlled safe answer paths in `src/pipeline.py`.

The idea is simple:

If the question falls into a known high-risk or common category, and the correct evidence is available, we answer with a controlled extractive/template-style response instead of fully relying on the LLM.

Examples:

```text
fee waiver questions
lost certificate questions
birth/death registration application status questions
upload error questions
manual-to-online migration questions
online visibility questions
overseas registration questions
single parent or divorce-related registration questions
data correction questions
multi-intent long questions
```

This is why all three LLMs sometimes produce the same answer. In those cases, CivicRAG found a safe path and produced a controlled answer before the model had much freedom. For civic QA, this is not necessarily bad. It means the answer is stable and grounded.

## 14. Bangla Language Guard

The system detects the answer language from the query.

If a user asks in Bangla, the answer should be in Bangla. If a user asks in English, the answer should be in English. If the evidence is Bangla but the user asks in English, the model should translate the evidence instead of switching to Bangla.

This is handled in:

```text
src/generation/ollama_generator.py
src/pipeline.py
```

This guard was added because earlier Qwen sometimes produced Chinese or mixed-language output. The current system has stricter prompt rules and fallback behavior.

## 15. Simple RAG vs CivicRAG

Simple RAG:

```text
query
    ↓
dense vector search
    ↓
top chunks
    ↓
local LLM
    ↓
answer
```

CivicRAG:

```text
query
    ↓
query normalization
    ↓
dense search + BM25 search
    ↓
weighted RRF fusion
    ↓
reranking / domain boosts
    ↓
safe answer path check
    ↓
controlled answer or local LLM fallback
    ↓
language guard
    ↓
answer with sources
```

For thesis explanation, Simple RAG is the baseline and CivicRAG is the proposed system.

## 16. Current Evaluation Datasets

Evaluation files live mainly in:

```text
domains/birth_death_registration/data/evaluation
docs/evaluation
```

Important evaluation dataset:

```text
domains/birth_death_registration/data/evaluation/p2_20q_eval_set.json
```

Mixed paraphrase evaluation:

```text
domains/birth_death_registration/data/evaluation/mixed_paraphrase_eval_set_v1.json
domains/birth_death_registration/data/evaluation/mixed_paraphrase_eval_flat_v1.json
```

Collected FAQ-pair evaluation outputs:

```text
docs/evaluation/collected_faq_pairs_2026_06_09
```

P2 experiment outputs:

```text
docs/evaluation/p2_experiments
docs/evaluation/reduced_eval_plan_v1
docs/evaluation/reduced_eval_plan_v1_llm_backend
```

## 17. Evaluation Theory

The retrieval evaluation uses expected source IDs. For each test question, we manually define which chunk IDs should be considered correct evidence.

Then the pipeline retrieves top-k chunks. We compare retrieved chunk IDs with expected chunk IDs.

### Hit@k / Recall@k

For our current implementation, Recall@k is used as a hit-style metric:

```text
Recall@k = 1 if any expected source appears in top-k retrieved chunks
Recall@k = 0 otherwise
```

This is suitable when one correct evidence chunk is enough to answer the question.

### Precision@k / Context Precision

```text
Precision@k = relevant chunks in top-k / k
```

This measures how clean the retrieved context is. High recall but low precision means the system finds the correct chunk but also brings extra noise.

### MRR

MRR means Mean Reciprocal Rank.

```text
RR = 1 / rank of first relevant chunk
```

If the correct chunk is rank 1, RR is 1. If it is rank 5, RR is 0.2. MRR is the average over all questions.

### nDCG@k

nDCG rewards relevant chunks appearing earlier in the ranking.

It is useful because rank order matters in RAG. The LLM usually receives only the top few chunks, so a correct chunk at rank 1 is more valuable than a correct chunk at rank 5.

### Generation Metrics

The generation scripts include automatic proxy metrics:

```text
semantic similarity to expected answer
token F1
answer relevance
faithfulness proxy using context similarity
expected source retrieved
expected source cited
```

These are useful for screening, but they are not a replacement for manual evaluation. For Bangla government-service QA, manual review is still necessary.

## 18. Current Retrieval Results

On the 20-question P2 fast retrieval run:

```text
dense_only Recall@5 = 0.900
bm25_only Recall@5 = 0.800
hybrid_rrf Recall@5 = 0.850
hybrid_rrf_rerank Recall@5 = 0.850
```

On the larger 58-question Bangla evaluation set:

```text
BM25-only Hit@5 = 0.7586
Dense-only Hit@5 = 0.9828
Hybrid RRF Hit@5 = 0.9483
```

Interpretation:

Dense-only currently performs best on this birth/death registration evaluation subset. This does not mean the dataset is bad. It means many test questions are semantically close to the cleaned Bangla chunks, so BGE-M3 dense retrieval is very strong.

BM25 is weaker overall but still useful for exact-match terms, legal numbers, fees, phone numbers and named services.

Hybrid RRF is still academically defensible because it is an alternative design and may become more useful when more domains are added, such as BRTA, passport, birth certificate and death certificate together.

## 19. How to Run the System Locally

Clone and switch branch:

```bash
git clone https://github.com/Shihabsarker93/civic_ai_rag.git
cd civic_ai_rag
git checkout feature/add-birth-death-domain
```

Check Ollama models:

```bash
ollama list
```

Pull models if missing:

```bash
ollama pull llama3.2
ollama pull llama3
ollama pull qwen2.5:7b
```

Prepare chunks:

```bash
python3 domains/birth_death_registration/scripts/prepare_chunks.py
```

Build index:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 scripts/build_index.py
```

Run terminal query:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 scripts/query_rag.py "জন্ম নিবন্ধনের ফি কত?"
```

Run chatbot:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 app.py --host 127.0.0.1 --port 7860
```

Open:

```text
http://127.0.0.1:7860
```

## 20. How to Run Evaluation

Retrieval evaluation:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 scripts/evaluate_retrieval.py \
  --eval-file domains/birth_death_registration/data/evaluation/p2_20q_eval_set.json
```

P2 experiment framework:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 scripts/run_p2_experiments.py \
  --eval-file domains/birth_death_registration/data/evaluation/p2_20q_eval_set.json \
  --fast-rerank
```

Reduced evaluation plan:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 scripts/run_reduced_eval_plan.py
```

The output reports are written under:

```text
docs/evaluation
```

## 21. How to Add a Future Domain

The repository already supports the multi-domain idea.

For a new domain such as BRTA, passport, birth certificate or death certificate:

```text
1. create a new folder under domains/
2. add raw data under that domain
3. create a domain config file
4. write or adapt a chunk preparation script
5. create domain-specific evaluation questions
6. build a separate Chroma collection for that domain
7. add domain routing later if multiple domains are active at once
```

Example future folders:

```text
domains/brta
domains/passport
domains/birth_certificate
domains/death_certificate
```

Do not create a separate GitHub repository for each domain. That would make shared retrieval, evaluation, UI and generation code harder to maintain.

## 22. What Is Strong in the Current System

The current system already has several thesis-defensible strengths:

```text
domain-specific data organization
Bangla-first retrieval
local LLM deployment
clear Simple RAG vs CivicRAG comparison
dense, sparse and hybrid retrieval alternatives
document-type-aware chunking
metadata and source IDs
source links in the UI
evaluation scripts with ranking metrics
safe answer paths for high-risk questions
Bangla language guard
repeatable configuration
```

## 23. Current Limitations

The system is still not final. Main limitations:

```text
only one active domain is indexed
manual evaluation dataset is still small
generation metrics are proxy metrics, not full human judgment
cross-encoder reranking may be slow on local CPU
safe answer paths require maintenance
some long multi-intent questions still need better decomposition
dense-only currently beats hybrid on our present evaluation set
the UI is simple and not production-grade
source documents may still contain cleaning errors
```

These limitations are not failures. They are useful discussion points for P2 because P2 expects alternative designs, preliminary verification and constraints.

## 24. Recommended Next Steps

For thesis progress:

```text
1. keep the current pipeline stable
2. expand the evaluation set to 80-100 Bangla scenario questions
3. manually label expected source IDs
4. add manual scores for correctness, faithfulness and language quality
5. test dense-only vs BM25-only vs hybrid on the larger set
6. decide whether CivicRAG should keep RRF, tune RRF or use dense-first retrieval for this domain
7. add one more domain only after birth/death registration is stable
8. prepare a demo script with 8-10 representative questions
```

For code:

```text
1. keep safe answer paths for high-risk civic questions
2. avoid adding too many rules before evaluation proves the need
3. keep retrieval_text and answer evidence separate
4. keep all new domains under domains/
5. keep evaluation datasets versioned
```

## 25. Q/A for Teammates and Supervisor

### Q1. Which model is ours?

Our model is not `llama3.2`, `llama3` or `qwen2.5:7b`. Those are LLM backends. Our proposed system is the CivicRAG pipeline.

### Q2. Why do we compare with Simple RAG?

Simple RAG is the baseline. It lets us show whether our engineering additions improve retrieval, grounding or answer reliability.

### Q3. Why do we need both dense and BM25?

Dense retrieval understands meaning. BM25 catches exact words. Government-service documents need both semantic and exact matching.

### Q4. Why is dense-only currently better in evaluation?

The current domain is small and the evaluation questions are semantically close to the cleaned Bangla chunks. BGE-M3 handles this well. Hybrid may help more when the dataset becomes larger, noisier and multi-domain.

### Q5. Is it bad if all LLMs produce the same answer?

Not always. If the answer comes from a safe answer path, identical answers mean the system is stable and controlled. For factual civic QA, consistency is often good.

### Q6. Why not just use ChatGPT or another API?

The thesis goal includes local, explainable and reproducible RAG. Local models avoid API dependency and make comparison easier in a controlled academic setup.

### Q7. Why did we separate retrieval_text from answer evidence?

Search needs aliases and alternate phrasing. Answer generation needs original evidence. Mixing them can cause hallucination because the LLM may treat aliases as facts.

### Q8. What prevents hallucination?

Several things:

```text
retrieved evidence only prompt
safe answer paths
source IDs
Bangla language guard
controlled answer templates for high-risk topics
fallback evidence answers
manual evaluation
```

### Q9. Why use ChromaDB?

ChromaDB is simple, local and persistent. It is suitable for thesis prototyping before moving to a production vector database.

### Q10. Why use BGE-M3?

BGE-M3 is multilingual and works better for Bangla/cross-lingual retrieval than English-only embeddings.

### Q11. Why do we need metadata?

Metadata tells us document type, source file, source URL, section title, category and service scope. This helps reranking, debugging, source display and evaluation.

### Q12. How do we know the answer is correct?

We check whether the correct source chunk was retrieved and whether the final answer is faithful to that source. Numerical metrics help retrieval. Manual review is still needed for final answer correctness.

### Q13. Can the system answer English questions?

Yes, the design supports English and mixed queries. The indexed evidence is Bangla, but retrieval aliases and BGE-M3 help cross-lingual search.

### Q14. What happens if a user asks outside the domain?

The system should say the available dataset does not contain enough information. Out-of-domain refusal still needs more testing.

### Q15. What is the biggest current risk?

The biggest risk is not the LLM. The biggest risk is bad retrieval or imperfect source data. If the wrong chunk is retrieved, even a good LLM may answer badly.

## 26. What Is Local but Not Necessarily on GitHub

The codebase is on GitHub in the branch:

```text
feature/add-birth-death-domain
```

However, some local thesis-writing artifacts may not be pushed or may live outside the repo, especially files under paths like:

```text
/Users/shihab/01 Thesis/Rag/miscellaneous /p2 write update
/Users/shihab/01 Thesis/Rag/miscellaneous /Thesis tempalte
```

There is also an untracked local repo folder at the time of this report:

```text
docs/merged_p1_p2_draft/
```

So teammates should treat GitHub as the source of truth for code, but local thesis documents may need to be shared separately unless committed.

## 27. Short Demo Explanation

If we need to explain the project in one minute:

```text
We built a Bangla-first RAG chatbot for Bangladeshi birth and death registration services. The system cleans government documents, converts them into typed chunks, embeds searchable retrieval text with BGE-M3, stores vectors in ChromaDB and also builds a BM25 sparse index. At query time, CivicRAG combines dense and sparse retrieval using RRF, reranks evidence using a BGE reranker or lexical fallback, applies intent-specific boosts and uses safe controlled answer paths for sensitive civic questions. If no safe path exists, it sends only original Bangla evidence to a local Ollama LLM. The answer includes source IDs, retrieval scores and links so the result is explainable and verifiable.
```

## 28. One-Line File Ownership Guide

```text
app.py                                      → local chatbot UI/server
src/pipeline.py                            → main CivicRAG logic
src/retrieval/hybrid_retriever.py          → dense, BM25 and RRF retrieval
src/reranking/reranker.py                  → reranking and domain boosts
src/generation/ollama_generator.py         → Ollama prompting and language rules
src/evaluation/metrics.py                  → retrieval/generation metric helpers
scripts/build_index.py                     → ChromaDB index builder
scripts/query_rag.py                       → terminal query runner
scripts/run_p2_experiments.py              → P2 experiment runner
scripts/run_reduced_eval_plan.py           → reduced hyperparameter/evaluation runner
domains/birth_death_registration/config.json → domain config
domains/birth_death_registration/scripts/prepare_chunks.py → data chunking pipeline
domains/birth_death_registration/data/interim/birth_death_chunks.jsonl → generated chunks
docs/evaluation                            → evaluation outputs
```

## 29. Final Takeaway

The project is now beyond a tutorial RAG chatbot. It has a thesis-oriented architecture with clear baselines, domain-specific chunking, multilingual retrieval choices, local LLM comparison and measurable retrieval evaluation.

The main remaining work is not to add more flashy techniques. The main work is to evaluate carefully, clean the data further where needed, expand the test set and justify which retrieval design is best for the domain.


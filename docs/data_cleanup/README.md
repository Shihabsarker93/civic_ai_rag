# Passport and BRTA source-preserving cleanup

**Latest whole-corpus pass:** [2026-09-22 corpus release](2026_09_22_corpus_release/README.md). This adds all-document/all-chunk validation, stronger structural context preservation, and an original-PDF-reviewed repair. The earlier experiment below is retained as historical evidence, not replaced or relabelled.

## Scope and preservation

This revision prepares cleaned, traceable derived Markdown and candidate chunks for all 30 Passport and 132 BRTA documents. It does not certify the factual accuracy, legal currency, or original-PDF fidelity of the supplied Markdown. Original snapshots, active domain configs, active registers, and existing Chroma collections are retained.

The rollback code tag is `codex/pre-passport-brta-cleanup-20260922`. Each domain's `baseline_config.json` records the exact pre-cleanup data version. The cleaned candidate data lives under `2026_09_22_plain/`; its manifests map every document to its source hash, derived Markdown, changes, chunks, and review flags.

| Domain | Source files retained | Baseline chunks | Structural candidate chunks | Heading-only fragments retained in Markdown but omitted from search |
|---|---:|---:|---:|---:|
| Passport | 30 | 361 | 297 | 59 |
| BRTA | 132 | 3,161 | 2,801 | 306 |

Chunk-count reductions also include consolidation of section fragments. No entire document is excluded. Eight long unstructured BRTA OCR documents, accounting for 1,119 existing chunks, remain unchanged in the candidate index because their legal clauses cannot safely be reconstructed through punctuation substitutions.

## Implemented cleanup

- Reuse the existing NFC, line-ending, invisible-character, and unresolved citation-marker cleanup.
- Extract the unfenced metadata preamble in the 2012 MRP guide so metadata is not embedded as answer evidence; preserve its declared date as unverified metadata.
- Remove the FAQ's explicit RAG-authoring boilerplate from the derived body, recording the removed text in the manifest.
- Keep FAQ pairs together and partition sibling headings separately.
- Split longer structured sections at whole paragraphs, top-level list items, or table rows. Do not split a list item's nested condition or a table cell. Oversized indivisible units must pass the embedding model's token-limit check.
- Retain heading-only sections in the derived Markdown and manifest, while omitting them as standalone searchable answer chunks.
- Keep source text separate from optional search labels. Search labels are disabled by default following the diagnostic experiment.

This does not resolve every semantic dependency between separate sections or validate every table against its original PDF. In particular, factual contradictions across documents are preserved for explicit review rather than silently resolved by choosing a value.

## Readable document registers

- [Passport: every document and its pending checks](2026_09_22_plain/passport/REVIEW.md)
- [BRTA: every document and its pending checks](2026_09_22_plain/brta/REVIEW.md)
- [Passport machine-readable manifest](2026_09_22_plain/passport/manifest.json)
- [BRTA machine-readable manifest](2026_09_22_plain/brta/manifest.json)

Flags such as `no_web_address` describe the supplied source and are not proof that its facts are wrong. Four Passport files and six BRTA files have unresolved original-file associations. There are 26 Passport and 109 BRTA documents flagged for absent web addresses. None are silently removed.

Priority review remains:

1. Passport applicability: distinguish MRP, e-passport, foreigner identity certificates, application, collection, and correction procedures. A source year alone does not prove that a rule is superseded.
2. Passport fees and dates: compare the original documents when schedules differ; do not combine values from different services.
3. BRTA requirements: retain learner, professional/nonprofessional, renewal, and replacement conditions. The existing-licence requirement in the supplied guide is conditional; the previous Qwen output dropped that condition even though it exists in the source.
4. BRTA OCR: review the 1983 ordinance, 1984 rules, Finance Act 2021, National Land Transport Policy 2004, both road-sign manuals, Road Transport Rules 2022, and Road Transport Act 2018 against the PDFs. These are explicitly listed in the BRTA register.
5. Generation: negation reversals, invented steps, and unsupported totals in model answers require separate fixes and testing; they are not repaired merely by producing cleaner Markdown.

## Diagnostics and publication gate

`scripts/evaluate_service_cleanup.py` compares a baseline and a specific staged candidate using unchanged retrieval parameters. Both sides use MPS in this local diagnostic to reduce runtime. It requires the actual cross-encoder and makes no LLM calls. Each domain has five explicitly defined source/content checks, covering known failures and preservation cases. These are development diagnostics, not held-out Recall@k, factual accuracy, or an independent thesis benchmark. Additional relevant sources can exist beyond the predefined hints.

The initial Passport experiment added heading-derived search vocabulary. It reduced the number of cases with designated support in the selected generation context from 5/5 to 4/5. That experiment was not activated. Its raw results are preserved in [the exploratory comparison](2026_09_22/passport/retrieval_diagnostics.json). Its BRTA build was stopped before publication; any partial collection is unreferenced.

The structural-only Passport candidate also scored 4/5 on that context-support diagnostic versus the baseline's 5/5. Both variants retained designated evidence somewhere in the top six for all five cases and placed it first for two cases. In the fee case, the designated fee-table chunk moved from rank 2 to rank 5. The unrelated Certificate of Identity chunk remained first. Consequently Passport is not activated. This does not mean that the baseline answers are reliable; it means that this cleanup does not yet justify replacing the baseline.

BRTA was unchanged at 3/5 for designated evidence at rank 1, in the top six, and in generation context. Both versions missed the specified driving-test and lost-licence evidence; renewal, learner, and fitness checks passed. BRTA is also left staged because no retrieval improvement was demonstrated and no new generated-answer comparison has been run.

| Diagnostic (five cases per domain) | Passport baseline | Passport cleaned | BRTA baseline | BRTA cleaned |
|---|---:|---:|---:|---:|
| Designated support at rank 1 | 2 | 2 | 3 | 3 |
| Designated support in top 6 | 5 | 5 | 3 | 3 |
| Designated support in generation context | 5 | 4 | 3 | 3 |

The final staged configs are `domains/passport/config.candidate_20260922_054145_038328.json` and `domains/brta/config.candidate_20260922_054337_899630.json`. Neither is active. Validation passed 25 tests, original and derived SHA-256 checks for all 162 files, unique chunk IDs, full document representation, and unchanged active-config checks. Both staged builds passed their tokenizer-limit and Chroma-ID consistency checks. The existing website health endpoint remains available.

- [Structural-only Passport diagnostics](2026_09_22_plain/passport/retrieval_diagnostics.json)
- [Structural-only BRTA diagnostics](2026_09_22_plain/brta/retrieval_diagnostics.json)

## Reproduce without changing the live chatbot

Use a new output directory; preparation refuses to overwrite an existing revision:

```bash
.venv/bin/python scripts/clean_service_corpora.py --domain passport --output docs/data_cleanup/NEW_REVISION
.venv/bin/python scripts/clean_service_corpora.py --domain brta --output docs/data_cleanup/NEW_REVISION
.venv/bin/python scripts/manage_experimental_domains.py build --domain passport --device mps --chunks-path docs/data_cleanup/NEW_REVISION/passport/chunks.jsonl --stage-only
.venv/bin/python scripts/manage_experimental_domains.py build --domain brta --device mps --chunks-path docs/data_cleanup/NEW_REVISION/brta/chunks.jsonl --stage-only
```

Run the diagnostic script with the exact candidate config filename printed by the staged build and the corresponding saved baseline config. Do not use the newest file implicitly. Retained originals, manifests, code, candidate chunks, and diagnostic JSON make the operation reviewable and reproducible; binary Chroma storage remains local.

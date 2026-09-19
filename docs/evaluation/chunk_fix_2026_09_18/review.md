# Experimental-domain chunking correction

Work performed September 18-19, 2026. This is a debugging comparison, not a held-out thesis benchmark or verification of current government policy.

## Cause and scope

The heading/body mismatch was in our preparation code, not in the supplied passport FAQ Markdown. The earlier splitter could stop before a heading, then label the next span using the previous heading. It could also split related FAQ material across spans. In the original FAQ, passport collection, lost delivery slips and retired government employees are separate sections.

The corrected `section_spans()` in `scripts/manage_experimental_domains.py` partitions at Markdown headings before splitting long sections. It preserves the parent heading hierarchy and keeps explicitly labelled question/answer sections together. Ordinary sections remain bounded at 1,400 characters. Every parsed-body character is covered; source files and byte-identical snapshots are not rewritten.

An initial candidate's FAQ heuristic was too broad: ordinary mentions of question/answer in a BRTA legal document incorrectly made the whole section atomic. The embedding guard rejected it instead of truncating it or replacing the live index. FAQ detection now requires explicit labels. The corrected BRTA candidate has 3,161 chunks, a maximum of 837 BGE-M3 tokens and no inputs above the model's 8,192-token limit.

Failed builds can leave unreferenced partial collections. They were not published or deleted. New collections and configs are versioned; original baseline collections remain available.

No change was made to RRF weights, retrieval top-k, reranker choice, application generation settings or the birth/death corpus. No new passport or BRTA controlled-answer templates were added.

## Retrieval diagnostic

`scripts/evaluate_chunk_fix.py retrieval` runs real BGE-M3, BM25, RRF and the configured reranker. It does not call an LLM. Six questions per domain use predefined source-filename and content checks. These checks are intentionally incomplete: they can miss alternative valid sources, and several BRTA checks identify only the expected document. They are not gold relevance judgements and must not be reported as Recall@k or answer accuracy.

Passport results from `retrieval_passport.json`:

| Question topic | Baseline support rank | Corrected support rank |
|---|---:|---:|
| Super Express collection location | 2 | 2 |
| Collection documents | 6 | 3 |
| Lost delivery slip | 1 | 1 |
| Retired government employee enrolment | 1 | 1 |
| Collection for a minor | 1 | 1 |
| Visa form language | 1 | 1 |

For collection documents, the corrected ranking also places the collection step from `5 Steps to your e-Passport` first. The targeted FAQ checklist is third, inside the application's three generation contexts rather than sixth. Retired-employee evidence still appears second, so this is an improvement, not perfect retrieval.

## Generation diagnostic

`scripts/evaluate_chunk_fix.py generation` supplies one selected, supporting passport chunk directly to each of the three actual local Ollama models. This deliberately removes retrieval as a variable. It uses the existing prompt, temperature 0.05 and top-p 0.9, but an experimental 600-token output limit rather than the app's unchanged 1,200. Raw answers, response metadata and evidence are preserved in `fixed_evidence_generation.json`.

This is not an end-to-end model benchmark. Timings include model loading and concurrent local work and are not suitable for a model-speed comparison. Review `done_reason` before interpreting incomplete output. Answer-quality observations here are assistant source-grounding checks, not independent human scores.

All six actual model calls completed with `done_reason=stop`, not an output-limit cutoff.

| Model | Super Express collection | Collection checklist |
|---|---|---|
| llama3.2 | Incorrect: invented office/department wording, including "আগরা হাউজ". | Substantially supported items; old-passport requirement loses the explicit renewal/reissue condition in the English evidence. |
| llama3 | Incorrect: named "দিল্লি ভিশা অফিস". | Substantially supported items; same old-passport condition issue and some English in the Bangla answer. |
| qwen2.5:7b | Incorrect: altered the locality and invented "ইমিডিয়েট হোল্ডিং অফিস". | Recognizable checklist but garbled wording, omitted age condition and confusing renewal/reissue phrasing. |

The supplied Super Express evidence names Agargaon Divisional Passport and Visa Office. These failures occur even without competing retrieved chunks. Fixing retrieval alone therefore cannot establish generation reliability. No model is declared a winner or made the new default from this diagnostic.

## Verification and preservation

The automated tests cover section coverage, sibling headings, atomic labelled FAQs, ordinary question/answer words in prose, unchanged source snapshots, isolation from birth-specific answer rules, staged-build isolation and versioned rollback. Ten tests passed.

Before activation, index IDs and stored text matched the active JSONL for all three domains. Hash checks confirmed all 162 supplied Markdown files, their snapshots and all 160 referenced PDFs were unchanged. No source document was excluded. The original birth/death index still contained 187 chunks.

## Activation

Both corrected candidates were activated after the targeted retrieval comparison: passport improved one targeted case without a regression in the other five, and BRTA matched the baseline ranks in all six targeted cases. The active indexes were then verified against their JSONL files. The chatbot has been restarted and now lists birth/death registration, BRTA and Passport and Immigration.

Rollback remains available through the versioned `config.before_activate_*.json` files in each domain directory. The previous data collections were retained.

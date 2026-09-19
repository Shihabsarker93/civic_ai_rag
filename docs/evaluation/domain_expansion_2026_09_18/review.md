# Initial BRTA and passport integration review

## What was completed

- All 132 BRTA Markdown files were indexed into 1,695 chunks.
- All 30 passport/immigration Markdown files were indexed into 148 chunks.
- No Markdown files were excluded or failed preparation in this initial version.
- The original 187 birth/death chunks remain in their separate collection; its configuration has no Git diff.
- Index IDs and stored texts match their active JSONL datasets. Document IDs cover every included register entry.
- All supplied MD/PDF hashes and byte-identical Markdown snapshots match the initial ingestion records.
- The local app exposes three domain choices and a persistent data register. Domain source isolation was checked in all four generated responses.
- Seven regression tests passed. The five experimental-domain tests were rerun after adding register-aware rollback and passed again.

## Actual answer smoke tests

Four convenience questions were submitted to the running `/chat` endpoint using CivicRAG and `llama3.2`. All four response routes were `llm`; birth-specific safe answers were not used. These are engineering smoke tests, not a held-out benchmark. No current-law verification or all-model comparison was performed.

| Question | Observed result against supplied evidence | Interpretation |
|---|---|---|
| Minimum ages for professional/non-professional driving licences | Expected source retrieved; answer gives 18/21 but adds unrequested application details and a malformed extra fee figure | Core age answer supported, overall response needs better focus and numeric fidelity |
| Documents needed for vehicle colour change | Expected source retrieved; answer lists signed application, registration certificate, fee receipt, current fitness and tax-token copies | Sample answer matches the supplied checklist; not a guarantee of current policy |
| Where to collect a super-express passport | Expected urgent-applications source appears among candidates, but answer says contradictory location wording and invents/garbles the office name | Generation failure despite relevant retrieved evidence; general collection instructions also contaminate the answer |
| What to bring to collect an e-passport | Expected five-step guide absent from the returned six candidates; answer lists retirement/application paperwork and garbled instructions | Retrieval intent mismatch plus unsupported generalization; collection and application requirements were confused |

Full outputs, candidate chunks and flags are in `smoke_results.json`; the readable output transcript is `smoke_report.md`.

Observed complete request latencies were approximately 209, 100, 88 and 75 seconds on this local machine. These include retrieval, reranking and generation, plus any cold-start effects. They are not LLM-only timing measurements or a controlled model-speed comparison.

## Decisions

Keep the complete initial experimental indexes as requested. Do not automatically delete a document because a generated answer failed: the passport examples show that ranking, context selection and generation can each contribute. The data register retains audit flags and provenance. No tuning, new safe-answer rules or architecture upgrade was applied in response to these four outputs.

Before treating the new domains as reliable guidance, evaluate additional representative questions with expected evidence and review failures. The immediate diagnostic targets are application-versus-collection intent and preserving office names, numbers and conditions. These are recommendations for the next iteration, not implemented fixes.

## Reversibility and access

Read `docs/experimental_domains.md` for inclusion changes, rebuilding, exporting and rollback. A status change records intent; building publishes a validated version and restarting activates it in the app. Prior active collections and chunk files are preserved. The `activate` command also reconciles the register, so rollback does not silently leave an incorrect inclusion record.

No original sources were modified or deleted. No GitHub push was performed in this task.

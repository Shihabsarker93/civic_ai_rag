# Source-preference experiment (not deployed)

Rollback tag: `codex/pre-source-selection-trial-20260922`.
The live chatbot, active data and production code are unchanged.

This generation-only experiment replays saved evidence from the earlier 30-question
Qwen3 audit. It does not rerun retrieval or the entire application. It compares:

1. Exact existing prompt and existing context selector.
2. Neutral source-selection instructions, with identical selected evidence.
3. The neutral prompt with the dominant-top-one shortcut disabled, only when this
   changes the selected evidence. Identical variants are recorded as no-ops and
   skipped, not reported as additional independent model evaluations.

The existing 22 Qwen LLM-route cases are inspected for shortcut effects. Three known
failure questions are selected before running: new-passport documents, passport
fees and lost driving licence. These are development cases, not unseen test data.
The comparison uses Qwen3:8b, the existing temperature, output limit and penalties,
reasoning off, the same combined-user-message structure and no JSON-output demand.
The neutral variant changes only the three source-priority instruction sentences.
No new filtering, citations, controlled route, model or database is deployed.

Full prompts, contexts, generation options and input hash are saved in `plan.json`.
Raw and post-language-guard answers are saved after each call in `results.json`
and `results.md`. Ollama completion metadata, including finish reason and token
counts, is retained to detect truncation. Source footers remain context IDs, not
verified claim-level citations. Identical settings do not guarantee deterministic
generation. One run per variant cannot establish a general accuracy improvement.

The server can remain open but simultaneous manual model calls can affect latency.
No automatic monitor or repeated notification is created. Inspect `run.log` for
progress. Failures stop the experiment and are saved without automatic reruns.

```sh
.venv/bin/python scripts/test_source_preference.py --dry-run
.venv/bin/python scripts/test_source_preference.py
```

Manual review must distinguish correct service/action, source conditions, unsupported
facts and absent supporting evidence. If the right evidence was never retrieved,
the prompt comparison cannot fix that retrieval failure. Changes will not be
promoted to the live chatbot just because they produce more answers.

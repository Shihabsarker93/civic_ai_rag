# BRTA and passport experimental expansion

The existing birth/death domain remains separate. New domain choices reuse BGE-M3 dense retrieval, BM25, weighted RRF, the existing cross-encoder/lexical fallback and local Ollama models. Birth/death-specific ranking boosts, safe-answer templates, query substitutions and evidence injection do not run for BRTA or passport. No new domain-specific controlled-answer rules have been asserted or invented.

## Persistent data register

Start with `domains/brta/data/register.json` and `domains/passport/data/register.json`. These are the authoritative document-level records. The app's **Data register** link opens the selected domain's register. Do not rely on chat memory to track exclusions.

Every document records its stable ID, original MD path, SHA-256, byte-identical snapshot path, candidate original PDF paths and hashes, declared metadata, audit flags, chunk IDs, requested status, actual indexing status and revision history. Candidate PDF matches are filename/metadata associations, not a certification of accuracy.

Initial policy: include all 132 BRTA and 30 passport Markdown files, including flagged/historical material, as explicitly experimental evidence. Original PDFs are references; separately embedding them would duplicate many MD sources. No original source is deleted or edited. Unknown provenance and dates remain unknown. No official links are invented.

Derived preprocessing normalizes Unicode NFC, line endings and selected invisible characters, removes unresolved `[cite: ...]` artifacts and separates simple frontmatter. The corrected `heading_faq_v2` chunker partitions Markdown at heading boundaries and retains the heading hierarchy. Ordinary sections are split into spans of at most 1,400 characters; explicitly labelled FAQ question/answer sections stay together and may exceed that character count. Title/section context is repeated for retrieval. Span coverage is exhaustive. Long forms/tables may still need better semantic boundaries; the pilot does not certify chunk quality for every document. Token lengths are checked against the actual loaded embedding model limit before insertion; an oversized FAQ stops publication rather than silently truncating evidence. Files with parsing failures are explicitly registered as failed.

Snapshots live under each domain's `data/source_snapshots/`; `data/interim/all_chunks.jsonl` contains all prepared chunks. Active JSONL files and Chroma collections are versioned. Runtime BM25 uses the same active JSONL as dense result lookup. A new config is published only after the new collection's IDs match the prepared active set. Older collections and config backups are retained for rollback.

The checked-in code defaults to CPU. This machine's initial new-domain indexing used MPS acceleration with the same BGE-M3 model and normalized vectors; this changes computation device, not the retrieval architecture. Small device-dependent floating-point differences are possible.

## Prepare and build

Run from the repository root using its `.venv`:

```bash
.venv/bin/python scripts/manage_experimental_domains.py prepare --domain brta --source-root '/Users/shihab/01 Thesis/p3 final/data/new data'
.venv/bin/python scripts/manage_experimental_domains.py prepare --domain passport --source-root '/Users/shihab/01 Thesis/p3 final/data/new data'
.venv/bin/python scripts/manage_experimental_domains.py build --domain brta --device mps
.venv/bin/python scripts/manage_experimental_domains.py build --domain passport --device mps
```

Preparation intentionally refuses to overwrite an existing register. `build` reads the existing prepared master dataset and requested inclusion statuses. Do not run the old destructive `scripts/build_index.py` against these experimental domain configs; use the versioned manager.

## Review a chunking correction before activation

`rechunk` reads the unchanged snapshots and creates a new master JSONL without modifying the active config or register. A staged build creates a separate collection and candidate config. Use the exact filenames printed by each command:

```bash
.venv/bin/python scripts/manage_experimental_domains.py rechunk --domain passport
.venv/bin/python scripts/manage_experimental_domains.py build --domain passport --device mps --chunks-path domains/passport/data/interim/all_chunks_heading_v2_TIMESTAMP.jsonl --stage-only
.venv/bin/python scripts/evaluate_chunk_fix.py retrieval --domain passport
.venv/bin/python scripts/manage_experimental_domains.py activate --domain passport --config-backup config.candidate_TIMESTAMP.json
```

Restart after activation. Repeat for BRTA as appropriate. The diagnostic script compares the current published config against the latest candidate, so run it **before** activation. Its source/content checks are a small debugging set, not exhaustive relevance labels or thesis benchmark accuracy. Failed builds can leave partial, unreferenced collections; they are never published by this workflow and have not been deleted.

## Exclude a faulty document without deleting it

Find its `document_id` in the register or a retrieved chunk's metadata. Then:

```bash
.venv/bin/python scripts/manage_experimental_domains.py set-status --domain brta --document-id DOCUMENT_ID --status excluded --reason 'Describe the observed evidence problem'
.venv/bin/python scripts/manage_experimental_domains.py build --domain brta --device mps
```

Restart the chatbot after a successful build. `set-status` alone records an intention; it does not silently modify the currently serving collection. Until a build and restart, the existing app continues using its prior data. After restart, both dense retrieval and BM25 use the newly selected corpus. Restoring a document uses the same commands with `--status included` and a reason. This changes inclusion only; correcting the document's actual text requires a reviewed new preparation revision, not editing an active snapshot in place.

No active records are irreversibly destroyed by this workflow. To roll back a published data version, select the relevant `config.before_REVISION.json` backup filename within that domain, then run:

```bash
.venv/bin/python scripts/manage_experimental_domains.py activate --domain brta --config-backup config.before_REVISION.json
```

Restart the app. The previous chunk file and collection remain available, and activation reconciles the register to that version while preserving history. The app's register response also shows the published collection, loaded collection and whether a restart is required.

## Export database contents

```bash
.venv/bin/python scripts/manage_experimental_domains.py export --domain passport --output /tmp/passport_index_export.json
```

This returns stored chunk IDs, document text and metadata. It does not reconstruct the original PDF or export vectors. Existing destination files are not overwritten.

## Run the website

```bash
ollama serve
.venv/bin/python app.py --host 127.0.0.1 --port 7860
```

If Ollama is already serving, do not start another copy. Visit `http://127.0.0.1:7860/` and select a domain. The two new domains load lazily and share model weights with the initial pipeline. Inference is serialized to avoid simultaneous access to shared models. Restart after rebuilding an index. Response badges identify the actual answer route (controlled, LLM, or fallback) rather than treating every selected model as proof of generation.

## Limits and follow-up

- Experimental metadata is displayed with retrieved sources and passed to the generator. This is a prompt-level caution, not a verified policy engine or guarantee against outdated answers.
- All readable material is initially included. Historical notices, unverified claims and noisy OCR therefore can affect results. A small successful test does not validate the whole corpus.
- Original audit: `/Users/shihab/01 Thesis/p3 final/data/audit_2026_09_18/audit_report.md` and companion mapping/overlap CSVs.
- Existing birth/death config and dataset remain unchanged. Baseline code commit before this expansion: `cdb390e`.
- No GitHub publication is implied by local ingestion. Chroma and generated JSONL remain gitignored; source snapshots, registers and code must be deliberately committed if sharing later.

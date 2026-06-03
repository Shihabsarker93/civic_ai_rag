# Birth and Death Registration Domain

This is the active Civic.ai thesis domain. It contains Bangla government-service material for Bangladesh birth and death registration, including FAQ JSON, cleaned Markdown guides, legal acts/rules, fee tables, application processes, correction instructions, and BDRIS support information.

## Current Source Mix

The active raw dataset is the manually updated/corrected set under:

```text
domains/birth_death_registration/data/raw/json/
domains/birth_death_registration/data/raw/md/
```

No other domain data is part of the active repository state.

## Chunking Strategy

This domain uses lightweight document-type-aware chunking:

- FAQ JSON: one Q/A pair per chunk; preamble as one context chunk.
- Legal act/rules: one legal unit per `ধারা` or `বিধি`, with long sections split into smaller parts.
- Fees: one full-table chunk plus row-level fee chunks.
- Application/correction guides: section, step, and scenario chunks.
- Portal/homepage content: only citizen-service/support sections are retained as chunks.

Run:

```bash
python3 domains/birth_death_registration/scripts/prepare_chunks.py
```

This writes:

```text
domains/birth_death_registration/data/interim/birth_death_chunks.jsonl
```

Build the vector index only after reviewing the prepared chunks:

```bash
python3 scripts/build_index.py --config domains/birth_death_registration/config.json
```

## Metadata Strategy

Use `service_scope` to prevent confusion between birth-only, death-only, and shared documents:

- `birth`
- `death`
- `birth_death`

This allows Civic.ai to answer birth certificate questions while still using shared legal/fee documents when relevant.

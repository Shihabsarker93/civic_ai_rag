# Birth and Death Registration Domain

This domain contains Bangla government-service material for Bangladesh birth and death registration. The first imported dataset came from manually converted Markdown files created from mixed government sources: Bijoy PDFs, converted DOCX files, Unicode HTML pages, and scanned/source PDFs.

## Current Source Mix

The imported ZIP is not birth-only. It contains both birth-specific and shared birth/death registration material.

Birth-focused files include:

- `birth_registration_application_process.md`
- `birth_registration_application_process_02.md`
- `application_for_birth_information_correction.md`

Shared birth/death files include:

- `birth_and_death_registration_fees.md`
- `faqs_on_birth_and_death_registration.md`
- `faqs_on_birth_and_death_registration_02.md`
- `know_this_01.md`
- `birth_and_death_registration_act_2004.md`
- `birth_and_death_registration_rules_2018.md`
- `home_registrar_generals_office_birth_and_death_registration.md`

## Preprocessing

Run:

```bash
python3 domains/birth_death_registration/scripts/clean_and_chunk_markdown.py
```

This writes:

```text
domains/birth_death_registration/data/processed/clean_markdown/
domains/birth_death_registration/data/interim/birth_death_chunks.jsonl
```

The cleaner removes obvious portal/navigation boilerplate, preserves YAML source metadata, and creates section-aware retrieval chunks with metadata for source file, URL, document type, service scope, language, heading, and chunk position.

## Metadata Strategy

Use `service_scope` to prevent confusion between birth-only, death-only, and shared documents:

- `birth`
- `death`
- `birth_death`

This allows Civic.ai to answer birth certificate questions while still using shared legal/fee documents when relevant.

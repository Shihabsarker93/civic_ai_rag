# Repository and Branching Strategy

This project should stay as one GitHub repository for all Bangladeshi government-service RAG domains.

## Repository Rule

Use one repository:

```text
civic-ai-rag
```

Do not create separate repositories for passport, BRTA, birth certificate, death certificate, or other government-service domains.

## Domain Rule

Each domain gets its own folder and config:

```text
domains/passport/
domains/brta/
domains/birth_certificate/
domains/death_certificate/
```

Each active domain should contain:

```text
config.json
data/raw/
data/processed/
data/interim/
data/evaluation/
```

## Branch Rule

Use Git branches for feature development only, not for separating domains.

Examples:

```bash
git checkout -b feature/add-brta-domain
git checkout -b feature/add-birth-certificate-domain
git checkout -b feature/add-death-certificate-domain
git checkout -b feature/evaluate-qwen-generator
git checkout -b feature/add-cross-encoder-reranker
```

After review, merge feature branches back into the main branch so all domains remain in one repository.

## Current Active Domain

```text
domains/passport
```

The BRTA manual is currently stored under:

```text
domains/_incoming/brta
```

It should be moved to `domains/brta` only when the BRTA domain is actively implemented.

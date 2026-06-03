# Repository and Branching Strategy

This project should stay as one GitHub repository for all Bangladeshi government-service RAG domains.

## Repository Rule

Use one repository:

```text
civic-ai-rag
```

Do not create separate repositories for future government-service domains.

## Domain Rule

Each domain gets its own folder and config:

```text
domains/birth_death_registration/
domains/<future_domain>/
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
git checkout -b feature/add-new-domain
git checkout -b feature/evaluate-qwen-generator
git checkout -b feature/add-cross-encoder-reranker
```

After review, merge feature branches back into the main branch so all domains remain in one repository.

## Current Active Domain

```text
domains/birth_death_registration
```

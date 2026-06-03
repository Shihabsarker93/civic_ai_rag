# Domain Template

Use this folder layout when adding a new government-service domain.

```text
domains/<domain-name>/
├── config.json
└── data/
    ├── raw/
    ├── processed/
    ├── interim/
    └── evaluation/
```

Domains should be added in feature branches, for example:

```bash
git checkout -b feature/add-brta-domain
git checkout -b feature/add-birth-certificate-domain
```

Do not create separate repositories for separate domains.

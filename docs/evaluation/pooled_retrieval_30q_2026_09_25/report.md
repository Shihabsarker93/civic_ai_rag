# Provisional pooled evidence evaluation

**Machine-drafted relevance labels; human review pending. Not thesis-final ground truth.**

Same 30 saved questions and final supplied evidence; no answer regeneration or fresh retrieval. The judge does not see system names, ranks or chatbot answers. Its labels are shared by both systems.

Recall and nDCG use the judged union of saved candidate and supplied passages, not exhaustive corpus relevance. The pool can miss valid alternatives and inherits retrieval/development-set bias. No-relevant pools or incomplete/uncertain judgments exclude the question for BOTH systems. Precision@5 always divides by 5, including when a system supplied fewer than five passages. MRR@5 is truncated, not full-list MRR. Relevance is binary, not legal correctness.

| Domain | System | Scored / total | Hit@5 | Precision@5 | Pooled recall@5 | MRR@5 | Pooled nDCG@5 |
|---|---|---:|---:|---:|---:|---:|---:|
| birth_death_registration | simple | 0/10 | pending | pending | pending | pending | pending |
| birth_death_registration | civic | 0/10 | pending | pending | pending | pending | pending |
| passport | simple | 1/10 | 1.0000 | 0.8000 | 0.8000 | 1.0000 | 0.8688 |
| passport | civic | 1/10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| brta | simple | 0/10 | pending | pending | pending | pending | pending |
| brta | civic | 0/10 | pending | pending | pending | pending | pending |
| overall | simple | 1/30 | 1.0000 | 0.8000 | 0.8000 | 1.0000 | 0.8688 |
| overall | civic | 1/30 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

Local Qwen3:8b also generated the evaluated answers; correlated model bias remains. Scores do not establish overall superiority, answer accuracy or statistical significance. Review labels and search for missed alternatives before using recall as a final thesis claim.

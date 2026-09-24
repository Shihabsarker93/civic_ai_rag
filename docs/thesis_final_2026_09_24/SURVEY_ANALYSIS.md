# Needs-analysis survey audit

The private input is `need analysis survey.zip`, supplied by the authors. Its SHA-256 is recorded in `generated/survey_aggregate.json`. Raw exports, timestamp records and free text are deliberately not copied into this repository or the thesis bundle.

## Inclusion and denominator rules

- Three nested CSV exports: 66 + 13 + 7 = 86 submissions, each with 46 columns. Service blocks change order; the final nine AI-related items are common.
- 85 affirmative-consent submissions; one explicit refusal is excluded from substantive analysis.
- Four consenting under-18 submissions and two missing-age submissions are held out, not deleted. Adult primary cohort: 79.
- Exact full-record duplicate check after domain-block alignment found zero duplicates. This is not proof of 79 unique people. No reliable participant identifier is available.
- Per-item denominators exclude only blank answers within the primary cohort. Other responses remain in the denominator. Multiple selections use semicolons and count distinct explicit options once per row.
- One desired-feature response says "all options". It is not expanded. Counting it as all four choices would add one to each count; main reporting uses the explicit selections only.
- Nonstandard free text is aggregated as other, not publicly quoted. No qualitative coding or inter-rater agreement is claimed.
- Age and gender imbalance are disclosed. No representative national estimate, causal impact, measured satisfaction or chatbot correctness follows from this survey.

## Reproduction

Use Python 3 with matplotlib (analysis used 3.11.2). Run from the repository root:

```sh
python scripts/analyze_needs_survey.py '/private/path/need analysis survey.zip'
```

Outputs: aggregate JSON, a LaTeX summary table and two vector-PDF charts under `generated/`. Respondent data are not used as RAG knowledge or evaluation reference answers.

## Key results

| Item | Count | Percent |
|---|---:|---:|
| Would use prospective assistant | 55/77 | 71.4% |
| Would not use | 13/77 | 16.9% |
| Unsure | 9/77 | 11.7% |
| Would recheck verified information | 42/76 | 55.3% |
| Documents/information requested | 62/77 | 80.5% |
| Form help requested | 64/77 | 83.1% |
| Uploaded-document checking requested | 56/77 | 72.7% |
| Payment/appointment information requested | 58/77 | 75.3% |
| Bangla more comfortable | 19/77 | 24.7% |
| Either Bangla or English acceptable | 50/77 | 64.9% |
| Would recommend if it works well | 67/76 | 88.2% |

## Thesis placement

- 1.2: motivation; 1.4: survey no longer incorrectly listed as missing work.
- 3.1: need-to-requirement mapping and unimplemented features.
- 3.2/3.4/3.8: societal interpretation, consent/privacy and hypothetical payment preferences.
- 4.3: instrument, harmonization and analysis method.
- 5.1: cohort, table, charts and interpretation; 5.4: statistical limitations.
- 6.1: bounded summary. Ethics Statement updated; Abstract and all numbered headings unchanged.

## Author confirmation still needed

Confirm recruitment channels, distribution/collection dates, who was invited, whether one person could submit different forms, how the three versions were assigned, the original full consent information and any ethics authorization. Confirm guardian/participant consent arrangements before considering under-18 records. No approval is inferred from a checkbox. No response rate is calculable without invitation data. The BRTA website-use item includes `rsta.gov.bt`; it is not used to claim verified Bangladesh BRTA usage.

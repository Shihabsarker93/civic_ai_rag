# First-round three-domain manual audit

This audit has 30 Bangla questions: 10 each for birth/death registration, BRTA, and Passport and Immigration. It intentionally mixes direct factual questions, paraphrases, scenarios, long conditional questions, and multi-condition questions.

The questions are in questions.json. The raw Llama 3.2 chatbot outputs are in answers_llama3_2.json and answers_llama3_2.md. The latter is easier to read during a manual review.

## What was checked

Each question was sent to the active local CivicRAG website with its matching domain explicitly selected. Expected-evidence-present means that one of the returned sources contained a predefined source/title/content hint. It is a retrieval diagnostic only. It does not prove that the final answer is factually correct, complete, current, or faithful.

| Domain | Questions | Expected evidence present | Answer route | Mean response time |
|---|---:|---:|---|---:|
| Birth/death registration | 10 | 10/10 | 9 controlled, 1 LLM | 26.95 s |
| BRTA | 10 | 9/10 | 10 LLM | 65.59 s |
| Passport | 10 | 10/10 | 10 LLM | 52.40 s |

## Manual-review priorities

1. brta_09_multi_change: the intended combined renewal/address-change Form 4(b) was absent from the returned evidence. The answer instead focused on address change and Form 5, so mark it as a retrieval/coverage concern.
2. passport_10_super_express: the correct Super Express source was retrieved. The answer includes extra, awkward procedural wording beyond the key collection location. Review it for faithfulness and conciseness.
3. Review every LLM answer for unsupported details, missing conditions, correct Bangla, and whether it actually resolves the user's situation. The birth/death controlled answers should also be checked, but they are not LLM-generated in most cases.

## Suggested scoring sheet

For each row in the Markdown answer file, assign four manual scores:

| Field | Allowed values |
|---|---|
| Retrieval support | 0 = unsupported, 1 = partly supported, 2 = clearly supported |
| Faithfulness | 0 = contradicts/invents, 1 = minor unsupported detail, 2 = fully grounded |
| Answer completeness | 0 = does not answer, 1 = partial, 2 = complete for the question |
| Bangla quality | 0 = poor/other language, 1 = understandable, 2 = clear natural Bangla |

Do not score current-policy validity unless it has been separately checked against an authoritative current source. Several experimental BRTA and passport documents may be historical.

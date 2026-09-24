# Frozen Simple RAG versus CivicRAG evaluation

## Scope

30 paired development questions, three domains, saved Qwen3:8b outputs.
No answer regeneration, live pipeline edits or baseline weakening.
Inputs are the matched dense-only run and the ordering-fixed CivicRAG run.
The runner checks identical question records and frozen configuration hashes.
Only answer_contexts actually supplied to generation are evaluated, not all candidates.
The appended Sources footer is removed; answer wording is unchanged.

## Metrics

- RAGAS 0.2.15 Faithfulness: support of generated claims by supplied context, not current factual truth.
- RAGAS ResponseRelevancy: question reconstruction and BGE-M3 similarity, strictness 3; not answer correctness.
- Custom RAGAS AspectCritic context_relevance_binary: whether most context applies to the requested service/procedure. Not standard context precision or recall.
- Saved mean, median and nearest-rank p95 generation latency; separate runs are not a controlled hardware speed benchmark.
- Completion counts, answer routes, finish reasons, context size, and Bangla-letter fraction. Letter fraction is not a fluency/correctness score.
- Paired mean metric differences with descriptive bootstrap intervals; small reused set, not population or held-out generalization evidence.

## Local judge limitations

Qwen3:8b judges its own outputs. This is exploratory self-evaluation, not independent verification.
Temperature 0, seed 20260924, reasoning disabled, context 16384, output limit 4096.
RAGAS stock English prompts assess Bangla text; multilingual judging may fail.
Two synthetic Bangla supported/contradicted faithfulness checks must pass before batch execution.
Passing these checks does not validate the judge for complex civic-service questions.
All judge outputs are retained; errors/non-finite scores are missing, not zero-filled.
Three consecutive scoring errors stop the job. Missing denominators are reported.
No hosted model calls or paid API use. Dependencies are isolated from the chatbot environment.

## Not computed without reviewed labels

Factual accuracy, reference semantic similarity, retrieval Recall/Hit@k, MRR, nDCG and reference-based context precision/recall.
Neither the supplied source IDs nor an LLM-generated answer constitute gold relevance labels.
Earlier informal assistant correctness counts are not imported as ground truth.

## Run

Environment: /Users/shihab/.cache/civic-ragas-env (restored from environment.txt after the previous /tmp environment disappeared).
Install the versions in environment.txt into a separate environment.
Run `python scripts/evaluate_saved_ragas.py --descriptive-only` for non-judge statistics.
Run `python scripts/evaluate_saved_ragas.py` for resumable local judging.
The job saves each metric attempt; it does not silently retry failed records on resume.
Inspect failure.json if present; completion.json indicates the full batch finished, not that all scores are valid.

## Resume record

On 24 September 2026, no evaluator screen session or Ollama listener was present. The previous temporary environment and temporary log were also absent. The precise cause of the interruption is unknown. All 66 saved scores were retained; evaluation resumes at the first unscored item using the same dependency versions and judge settings. No chatbot answer is regenerated. This comparison contains only Simple RAG and CivicRAG on the existing 30 paired Qwen3 answers, not another paper's system or financial-domain benchmark.

The resumed evaluator uses the persistent screen session `civic-ragas-eval`, with its log under this evaluation directory as `resume.log`. The website remains stopped. RAGAS judge calls produce evaluation judgments, not replacement answers to the original questions.

References: https://docs.ragas.io/en/v0.2.12/references/metrics/

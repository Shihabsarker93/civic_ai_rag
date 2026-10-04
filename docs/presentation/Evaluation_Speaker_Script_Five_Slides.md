# Evaluation and Results: Five-Slide Speaker Script

Prepared 1 October 2026 for the five supplied slide screenshots. Values checked against the saved answer-evaluation summary and assistant-reviewed retrieval report. No slides or thesis files have been edited.

## How to Use This Script

The extended script is designed for approximately 8-10 minutes with pointing and pauses. Actual time depends on speaking speed; rehearse it. A shorter 4-5-minute version follows at the end. Do not read both versions.

Lead with supported strengths: usable source-linked retrieval across three domains, higher judged context applicability, and specific hybrid retrieval gains. Briefly acknowledge other methods' higher values rather than presenting the charts as universal CivicRAG superiority. This gives the panel a confident, defensible explanation.

Bracketed text contains presenter instructions, not words to read aloud. Optional paragraphs can be removed first. Do not read every number on a chart.

Suggested extended timing: Slide 1 about 1:45; Slide 2 about 2:00; Slide 3 about 1:30; Slide 4 about 1:30; Slide 5 and closing about 1:45. Total about 8:30, allowing additional pauses up to 10 minutes.

## Slide 1: Evaluation and Results

### Main message

We evaluated both finding evidence and producing answers, using a matched baseline and a separate retrieval-only comparison.

### Extended spoken script

[Receive the handover from the architecture presenter.]

"Now that we have explained the system architecture, I will present how we evaluated it and what the results demonstrate.

Our main contribution includes turning scattered civic-service material into a structured, source-traceable corpus. Therefore, we wanted to examine two things: whether the system could retrieve useful evidence from that corpus, and how effectively it used the evidence to produce answers.

[Point to Evaluation Goals, then Answer-Level Evaluation.]

At the answer level, we compared Simple RAG with CivicRAG using thirty Bangla questions, ten from each domain. Both systems used the same Qwen3 eight-billion-parameter model, the same corpus access and matched generation settings. The key difference was how they retrieved and prepared the evidence supplied to the model.

This means we did not give our proposed system a stronger generator than the baseline. We evaluated the saved answers and the contexts actually used to generate them.

[Point to the three answer metrics.]

Faithfulness asks whether the answer's claims are supported by the supplied evidence. Answer relevancy asks whether the response addresses the question. Our custom context-relevance measure asks whether most of the supplied context applies to the requested service, procedure and conditions.

These are complementary measurements. Relevant evidence and a well-supported answer are related, but they are not the same thing.

[Point to Retrieval-Level Evaluation.]

Separately, we compared BM25, dense BGE-M3 retrieval and Hybrid RRF before reranking or answer generation. We reviewed three hundred and nine question-passage pairs. Twenty-six questions were eligible for hit, precision and reciprocal-rank measurements, and twenty-five for pooled recall and normalized ranking quality.

These were development questions with assistant-reviewed retrieval labels and model-judged answer scores. We use them as scoped experimental evidence, not as an independently verified factual-accuracy percentage.

The strength of this design is that it helps us distinguish evidence retrieval from answer generation, rather than reducing the entire project to one score."

### Optional explanation if the panel looks confused

"Think of retrieval as choosing the right pages of a book, and generation as writing an answer using those pages. We tested both stages separately."

### Transition

"First, let us look at the complete answer-pipeline comparison."

## Slide 2: Answer Level Results

### Main message

CivicRAG achieved higher custom context relevance on this set; answer relevancy was numerically close, while Simple RAG had higher faithfulness. These metrics describe different parts of the task.

### Extended spoken script

[Identify the colors: blue is Simple RAG; orange is CivicRAG. Start at the rightmost pair.]

"The clearest positive result for CivicRAG here is in custom context relevance. Its score is zero point nine six six seven, compared with zero point nine three three three for Simple RAG.

This metric checks whether most of the supplied context is applicable to the service and procedure in the question. Because it is a binary judgment for each question, these averages correspond to twenty-nine positive judgments out of thirty for CivicRAG, compared with twenty-eight for Simple RAG.

This is an observed improvement of one question, or about three point three percentage points. We interpret it as a positive indication of context applicability on this set, rather than saying that ninety-six percent of all individual passages or answers were correct.

[Move to the middle pair.]

For answer relevancy, CivicRAG scored approximately zero point eight three eight, while Simple RAG scored approximately zero point eight four six. The observed difference is about zero point zero zero eight five. Both averages are numerically close on this measure, although this is not a formal claim that the systems are equivalent.

[Move briefly to faithfulness.]

Simple RAG scored higher on faithfulness: approximately zero point seven nine eight compared with zero point seven three two. We report that distinction because selecting applicable context and producing fully supported claims are different tasks.

[Return the pointer to the context-relevance bars.]

Our positive finding is therefore specific: CivicRAG supplied context that received a higher applicability score in this matched comparison. We do not claim that adding retrieval and selection components automatically increases every answer metric.

That distinction is valuable for understanding the system. It tells us which aspect showed a gain and which aspect still requires focused improvement, instead of hiding both behind a single overall accuracy number.

The chart contains thirty paired scores for each measure. The judge was also Qwen3, so these are self-judge measurements of the saved outputs, not independent confirmation of government-service facts.

Overall, this comparison provides evidence about the behavior of our full pipeline under matched conditions. The next charts examine the retrieval stage directly, allowing us to see how the prepared corpus performs in each service domain."

### Optional paragraph for the longer version

"It is also important that this was a bundled comparison. CivicRAG changes retrieval fusion, reranking and evidence preparation together. Therefore, the context-relevance difference cannot be attributed to the selector alone without an additional component-specific experiment."

### Delivery advice

Spend most time explaining the context metric and its practical meaning. Acknowledge the faithfulness result clearly once; do not repeatedly apologize for it. Do not call the small context difference statistically significant or a proven general improvement.

## Slide 3: Retrieval Results, Passport

### Main message

Both Dense and Hybrid retrieved at least one labeled relevant passage in the top five for every eligible passport question. Dense placed relevant evidence earlier and achieved higher precision.

### Extended spoken script

[Explain that chart colors now change meaning: blue BM25, orange Dense, green Hybrid.]

"We now move from complete answers to retrieval alone. In these three charts, blue represents BM25, orange represents dense retrieval, and green represents Hybrid RRF. Reranking and evidence selection are not included in these measurements.

[Point to Passport Hit@5.]

For passport, both Dense and Hybrid achieved a Hit at five of one point zero. This means that, for all eight eligible passport questions, each method found at least one labeled relevant passage within its first five results.

This is an encouraging result for the passport corpus: the prepared evidence was retrievable for every question included in this particular scored subset. It does not mean every retrieved passage was relevant or every final answer was correct.

BM25 achieved zero point seven five, corresponding to six of the eight questions. So both methods incorporating dense retrieval achieved higher top-five hit coverage than keyword retrieval alone here.

[Point to Precision@5 and MRR@5.]

Dense retrieval was strongest at concentrating useful passages near the top. Its precision at five was zero point six five, and its reciprocal-rank score was zero point eight seven five. Hybrid's corresponding values were zero point four seven five and zero point six five six two.

Precision tells us how much of the top-five list was relevant, while reciprocal rank rewards finding the first relevant passage early. Therefore, equal Hit at five does not mean identical ranking quality.

Our main takeaway is that both Dense and Hybrid successfully located relevant passport evidence across the eligible subset, while Dense produced the stronger ordering. This supports the usefulness of the prepared corpus and shows why we measure more than just whether a search found anything relevant."

### Optional explanation

"The starred recall and nDCG measures use the reviewed pool of passages. They do not assume we labeled every relevant passage in the entire database."

### Transition

"Birth registration shows a different pattern, including a specific advantage for Hybrid retrieval."

## Slide 4: Retrieval Results, Birth Registration

### Main message

Hybrid achieved the highest Hit@5: eight of nine eligible questions, compared with seven for Dense and six for BM25. Dense and Hybrid tied on Precision@5.

### Extended spoken script

[Point directly to the Hit@5 bars.]

"Birth registration gives us the clearest domain-specific gain for Hybrid RRF. Hybrid reached a Hit at five of zero point eight eight eight nine, compared with zero point seven seven seven eight for Dense and zero point six six six seven for BM25.

In question counts, that means Hybrid retrieved relevant evidence within the first five results for eight of nine eligible questions. Dense did so for seven, and BM25 for six.

So Hybrid increased the number of questions with a relevant top-five result by one compared with Dense on this subset. This is the particular result we highlight, rather than describing Hybrid as the winner on every metric.

[Point to Precision@5.]

Dense and Hybrid also had the same average precision at five, approximately zero point four two two two. That makes the pattern interesting: Hybrid had a hit on more questions while matching Dense's average top-five precision.

[Briefly gesture to the remaining metrics.]

Dense still placed relevant results earlier on several ranking measures. Hit coverage, the number of relevant retrieved passages, and their positions measure different properties, so they can favor different methods.

For our project, the positive conclusion is that rank fusion produced a useful top-five hit gain in birth registration. This is consistent with the motivation for combining lexical and semantic signals, although the aggregate scores alone do not prove exactly why each additional hit occurred.

It is also important that these are retrieval-only results. We are not attributing this difference to the later evidence selector or registration-specific reranking rules, because those stages were not part of this comparison."

### Optional explanation

"With only nine eligible questions, a single question changes Hit at five by about eleven point one percentage points. We therefore describe the actual eight-versus-seven count, which makes the scale of the result transparent."

### Transition

"Finally, BRTA demonstrates the value of semantic retrieval on another newly integrated service corpus."

## Slide 5: Retrieval Results, BRTA

### Main message

The BRTA corpus supported strong dense retrieval. Both Dense and Hybrid outperformed BM25 on the displayed metrics, with Dense leading most comparisons and matching Hybrid on Precision@5.

### Extended spoken script

[Point to Hit@5 and then Hit@1.]

"For BRTA, Dense achieved a Hit at five of zero point eight eight eight nine, corresponding to eight of nine eligible questions. Hybrid achieved seven of nine, and BM25 five of nine.

Dense also achieved a Hit at one of zero point seven seven seven eight. That means its very first result was labeled relevant for seven of the nine questions. This is a useful sign that the prepared BRTA corpus supports targeted semantic retrieval, rather than requiring the user to match exact document wording.

[Point to Precision@5.]

Dense and Hybrid tied on average precision at five at approximately zero point four four four four. Both were above BM25's zero point two six six seven.

[Gesture to MRR and nDCG.]

Dense also led the ranking measures, including a reciprocal-rank score of approximately zero point eight three three three. Hybrid remained above BM25 across all the displayed BRTA measures.

The correct comparison is therefore that Dense was strongest in this domain, while Hybrid also improved over keyword-only retrieval. Dense retrieval is a shared building block of our architecture, but we do not present Dense's standalone score as the score of the complete CivicRAG pipeline.

This result matters to our dataset contribution. It shows that the work of preparing BRTA documents produced evidence that the retrieval methods could locate for these questions. We are evaluating practical access to the corpus, not simply reporting how many files we collected.

[Pause, then summarize the whole section.]

Across these slides, we have three positive findings: higher judged context applicability for CivicRAG in the matched answer comparison; a Hybrid top-five hit advantage in birth registration; and useful retrieval from the passport and BRTA corpora, with Dense particularly strong.

Our contribution is therefore a working, source-traceable civic-service system together with a reproducible comparison that identifies its strengths by stage and by domain. We do not need one method to win every chart to demonstrate the value of that work."

### Optional closing detail

"For BRTA, hit, precision and reciprocal rank use nine questions, while pooled recall and nDCG use eight. The extra question had no labeled relevant passage in its reviewed pool, so recall and normalized gain were undefined rather than assigned an invented value."

### Handover

"I will now hand over for our overall contributions, conclusions and future directions."

## Shorter Script: Approximately 4-5 Minutes

Use this instead of the extended script when the group's total presentation time is tight. Allow pauses to point at the graphs; rehearse rather than relying on the estimated duration.

### Slide 1

"We evaluated two stages: finding relevant evidence and generating an answer from it.

At the answer level, we compared Simple RAG and CivicRAG on thirty Bangla development questions, ten per domain, using the same corpus, Qwen3 model and matched generation settings.

We measured faithfulness, answer relevancy and a custom measure of whether the context applied to the requested service and procedure.

Separately, we compared BM25, Dense and Hybrid retrieval before reranking and generation. There were twenty-six eligible questions for hit, precision and reciprocal rank, and twenty-five for pooled recall and nDCG. Retrieval labels were assistant-reviewed and answer scores were model-judged, so these are scoped evaluation results rather than independent factual accuracy."

### Slide 2

"CivicRAG's clearest gain was custom context relevance: zero point nine six six seven versus zero point nine three three three. That corresponds to twenty-nine positive judgments out of thirty, compared with twenty-eight for Simple RAG.

The answer-relevancy scores were numerically close, at approximately zero point eight three eight and zero point eight four six. Simple RAG scored higher on faithfulness, at zero point seven nine eight versus zero point seven three two.

The positive finding is therefore specific: CivicRAG received a higher context-applicability score on this comparison. We distinguish that from answer support, rather than claiming every metric improved. These scores use Qwen3 as the judge and are not independently verified accuracy percentages."

### Slide 3

"For passport, both Dense and Hybrid reached one point zero Hit at five. Each retrieved at least one labeled relevant passage for all eight eligible questions, compared with six of eight for BM25.

This shows that relevant passport evidence was accessible through both methods on the scored subset. Dense gave the stronger ranking, with precision at five of zero point six five and reciprocal rank of zero point eight seven five.

The main distinction is that finding at least one useful passage and placing useful passages first are different achievements. These are retrieval-only scores, not final-answer accuracy."

### Slide 4

"Birth registration provides a specific advantage for Hybrid. Its Hit at five was eight out of nine, compared with seven out of nine for Dense and six out of nine for BM25.

Hybrid therefore covered one additional question compared with Dense, while matching Dense's average precision at five at approximately zero point four two two two.

Dense led several other ranking measures, so we describe the gain precisely as a top-five hit improvement. This is a useful result for the fusion stage, measured before the later selector or domain-specific reranking adjustments."

### Slide 5

"For BRTA, Dense had the strongest results: eight of nine questions had a relevant top-five result, and seven of nine had a relevant first result. Hybrid achieved seven top-five hits, compared with five for BM25.

Dense and Hybrid tied on precision at five, and both exceeded BM25 across the displayed measures. This demonstrates that the prepared BRTA corpus supports retrieval beyond exact keyword matching on these questions.

Overall, our strengths are higher judged context applicability in the CivicRAG answer comparison, a Hybrid hit gain for birth registration, and retrievable source evidence across the expanded service domains. These are concrete contributions supported by our saved comparisons, with different methods showing strengths at different stages."

## Preparation Notes: Do Not Read These Aloud

### Keep the comparisons distinct

- Slide 2 compares complete matched Simple RAG and CivicRAG answer pipelines.
- Slides 3-5 compare retrievers BEFORE reranking, boosts and evidence selection.
- Dense is used inside CivicRAG, but standalone Dense results are not full CivicRAG results.
- Hybrid RRF in the retrieval charts is not shorthand for the entire chatbot.

### Metric explanations for questions

- Hit@1: did the first passage have a relevant label?
- Hit@5: did any of the first five have a relevant label?
- Precision@5: relevant passages among the first five, divided by five.
- Pooled Recall@5: fraction of known relevant passages in the reviewed pool found in the first five; not exhaustive database recall.
- MRR@5: reciprocal of the first relevant rank within five, or zero if absent, averaged across questions.
- nDCG@5: quality of the top-five ordering relative to an ideal ordering under the pooled binary labels.
- Custom context relevance: one binary judgment per question's context set, not individual-passage precision.

### Exact figures to remember

- Context relevance: CivicRAG 0.9667; Simple 0.9333; net positive-count difference 29 versus 28 out of 30. This does not identify which individual paired outcomes changed.
- Answer relevancy: CivicRAG 0.8375; Simple 0.8460.
- Faithfulness: CivicRAG 0.7323; Simple 0.7983.
- Passport Hit@5: Dense and Hybrid 8/8; BM25 6/8.
- Birth Hit@5: Hybrid 8/9; Dense 7/9; BM25 6/9. Do not reverse Dense and Hybrid.
- BRTA Hit@5: Dense 8/9; Hybrid 7/9; BM25 5/9.

### Scope and wording

The 309 labels are question-passage pairs, not 309 questions or independent human annotations. Four questions with uncertain labels were excluded for all three retrieval methods. One additional empty-relevance pool was excluded only from recall/nDCG, which require a nonempty relevant pool. The thirty-question answer evaluation and the eligible retrieval subsets are different denominators.

Avoid "statistically significant improvement," "96.67% accurate," "perfect passport answers," "Hybrid wins overall," or "the selector alone caused the gain." The saved bootstrap intervals do not establish a clear nonzero positive population effect for the custom context metric. None of these charts independently verifies legal or factual correctness.

Use "on the evaluated set," "higher observed score," "retrieved labeled relevant evidence," and "a domain-specific gain." State the scope briefly once, then focus on explaining the results.

The custom measure is implemented using RAGAS AspectCritic with a project-specific definition. It is separate from standard context precision/recall. The phrase "same setup" refers to matched corpus and generation conditions; runtime was not measured as a controlled hardware speed benchmark.

### Answers to likely panel questions

**Why is Simple RAG higher on two answer metrics?**

"The stages measure different things. CivicRAG received higher context-applicability judgments, but that did not translate into higher faithfulness in this run. Our contribution includes measuring this distinction rather than assuming a more complex pipeline must win everywhere."

**Why retain Hybrid when Dense leads many retrieval metrics?**

"Hybrid was the design investigated for combining lexical and semantic evidence. The study found a specific birth-registration Hit@5 gain and domain-dependent trade-offs, rather than a universal winner."

**Is one extra positive context judgment enough to claim a major improvement?**

"No. We report the one-question observed difference as a limited positive result, not a major or statistically established general gain."

**Why claim a dataset contribution if you did not compare different datasets?**

"The contribution is preparing and linking the civic-service evidence and making it usable in the system. Retrieval results demonstrate use of that resource on these questions; they do not isolate the causal benefit of cleaning or prove superiority over another dataset."

**Does Hit@5 equal answer accuracy?**

"No. It indicates that at least one relevant passage was found. The model can still omit, mix or misstate information, which is why we evaluated answers separately."

## Checked Sources

- [Saved answer-metric summary](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/evaluation/ragas_comparison_2026_09_24/ragas_summary.json)
- [Assistant-reviewed retrieval report, denominators and exclusions](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/evaluation/current_30q_retrieval_only_2026_09_25/assistant_metrics_report.md)
- [Custom context metric definition](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/scripts/evaluate_saved_ragas.py:130)
- [Passport thesis table](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/thesis_final_2026_09_24/generated/retrieval_passport.tex)
- [Birth-registration thesis table](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/thesis_final_2026_09_24/generated/retrieval_birth_death_registration.tex)
- [BRTA thesis table](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/thesis_final_2026_09_24/generated/retrieval_brta.tex)

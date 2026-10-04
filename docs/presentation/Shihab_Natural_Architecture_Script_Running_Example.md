# Shihab's Natural Architecture Script: From Documents to an Answer

Prepared 1 October 2026. Covers your part: Sections 4.1, 4.2 and 4.4.

This version follows your own rehearsal rather than starting from a different presentation structure. It is deliberately longer than a timed script so you can understand and shorten it yourself. Most spoken text is in simple English; the selector explanation is in Bangla. Bracketed cues and notes are for you, not for reading aloud.

Slide order: **System Architecture -> Implementation Decisions -> Comparison and Evaluation Boundaries -> handover.**

The running question is **“নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?”** [What documents do I need to apply for a new passport?]

The possible passages and ranking numbers used below are illustrative. They are not a replay of an actual saved retrieval trace, and no government-document checklist is being certified here.

## Before Rehearsing: Correct These Terms

- Say **retrieval**, not dictionary: it means finding relevant passages.
- Say **applicability**, not availability: it means whether the passage fits the requested service, action and conditions.
- Say **per-domain chunks**, not jumps: small source-linked pieces within each service domain.
- Say **weighted RRF**, not RLF: Reciprocal Rank Fusion.
- We have **two retrieval approaches**, not two embedding models. BGE-M3 creates dense embeddings; BM25 performs lexical keyword retrieval.
- Chroma stores dense vectors with linked content and metadata. The BM25 index is separate, built in memory when the retriever loads.
- Say **up to** 20 results per retrieval channel, **up to** 15 fused candidates, and **up to** six final passages. These are limits, not guaranteed counts.

## 1. Opening and the Three Stages

[Point to the complete architecture, without reading the small boxes yet.]

“Thank you, Tapu. Now that we have seen how the data was collected and prepared, I will explain how our system uses that data to answer a user's question.

This architecture has three main stages.

The first stage prepares and indexes our documents so that we can search them. The second stage retrieves candidate passages when a user asks a question. The third stage selects applicable evidence and uses a local language model to generate a Bangla answer.

I will use one question throughout this explanation: ‘নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?’ In English, that means: ‘What documents do I need to apply for a new passport?’

Before answering that question, we first need to prepare the information that the system will search.”

[Understanding: indexing = building searchable structures before a question arrives. This does not mean training Qwen on your documents.]

## 2. Per-Domain Chunks and Structure-Aware Splitting

[Point to source documents, data preparation, and per-domain chunks. Keep the cleaning recap brief because Tapu covered it.]

“We start with the prepared documents and organize their text into chunks within each domain: registration, passport and BRTA.

A chunk is a manageable piece of a document. Rather than treating the whole document as one search result, we try to keep useful structures such as headings, checklists, fee sections and question-answer units together where the source allows.

For example, a passport document may contain separate sections about a new application, collecting a passport and replacing a lost passport. These sections concern the same service, but they do not answer the same question.

Heading-aware splitting helps preserve that distinction. Each emitted passport chunk carries its document title and section information, so even a piece from a longer section retains its context.

Every chunk also receives an identifier and metadata that link it back to its source.”

[Understanding: metadata = descriptive fields such as document ID, section title, source path and available URL. Structure-aware does not mean every chunk is a complete procedure or that all documents are cleanly structured.]

## 3. Why Are There Two Boxes: Search Text and Source Content?

[Point to the split between `retrieval_text` and `content`.]

“Here we make an important distinction between the text used for searching and the text used as evidence.

The retrieval text contains the chunk content together with search-oriented context, such as its domain and section heading. In the registration corpus, it can also include alternative search terms, which we call aliases.

The content field retains the source-derived text that we will supply to the answer generator. We keep additional search aliases separate so they are not automatically presented as official facts.

So we are not replacing the passage with a summary. We are making the passage easier to find while keeping a clear link to its evidence content.”

[Simple mental example, not an actual saved record:]

```text
Chunk ID: example_passport_01
Content: document title + application-documents section + source passage
Retrieval text: passport + the content above
Metadata: document ID + section title + source information
```

[Understanding: for active passport/BRTA records, the search text is essentially domain plus title, section and source-body text. Do not claim every passport record has a separate alias expansion.]

## 4. Dense Embeddings: Searching by Meaning

[Point to BGE-M3 in the top band.]

“We use BGE-M3 to convert the retrieval text into a dense embedding, which is a numerical representation of the text.

The purpose is to support semantic matching: finding passages with related meaning even when the wording is different.

For example, a user might say ‘কী কী কাগজপত্র লাগবে?’ while a source uses wording such as ‘প্রয়োজনীয় নথিপত্র’. These expressions are not identical, but they can refer to the same information need.

Dense retrieval allows the system to compare their representations instead of depending only on exact words.

We normalize the vectors to unit length. I will briefly connect that operation to the equation on the next slide.”

[Understanding: the example explains the purpose of semantic search; it does not guarantee these phrases receive a particular similarity score. An embedding is a list of numbers, not a stored model-written answer.]

## 5. ChromaDB and BM25: Two Different Search Structures

[Point first to Chroma, then to BM25.]

“We store the dense vectors in ChromaDB, together with the corresponding chunk IDs, content and metadata. Each vector remains linked to the text it represents.

Alongside this, we use BM25 for lexical retrieval, which means searching through matching words and terms.

This is useful because exact service terminology can also matter. A question containing ‘পাসপোর্ট’ and a document-related term may benefit from passages containing those words.

BM25 breaks the retrieval text into searchable tokens and scores matches. It is not a second embedding model, and its index is not stored as another vector in Chroma. It is built separately when the retriever loads.

Together, these approaches give us two views of the same corpus: one based on meaning and one based on words.”

[Understanding: the diagram places BM25 in the preparation band conceptually, but the code constructs its index during retriever initialization.]

## 6. The User Now Asks the Running Question

[Move down to the middle-left user-query box.]

“Now let us return to the question: ‘নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?’

The user selects the passport domain. The system therefore searches the passport collection rather than mixing material from all three service domains.

We apply input and scope checks, then normalize the question. Normalization makes certain text representations more consistent, including Unicode forms and selected invisible characters or wording variations.

This is not another language model rewriting the question. It is a text-processing step that helps the search and matching rules work more consistently.”

[Understanding: the cross-domain guard handles certain unsupported aggregate requests; it is not a perfect intent detector. Domain selection does not ensure every passport passage fits the requested procedure.]

## 7. Dense Search and BM25 Search: Why Up to Twenty?

[Follow the two retrieval branches.]

“The normalized question goes through both retrieval approaches.

For dense search, BGE-M3 encodes the question using the same model used for the document passages. Chroma returns up to twenty nearby passage IDs.

For BM25, the system tokenizes the question, scores word matches, and returns up to twenty positive-scoring results.

At this point, these are only candidates. Some may discuss application documents, while others may discuss another passport procedure.

We retrieve a larger initial shortlist so later stages have alternatives to compare before choosing the final evidence. Twenty is our configured candidate limit: a practical choice controlling the search shortlist, not a number that we proved is universally optimal.”

[Understanding: two branches does not necessarily mean simultaneous execution. The inspected search method calls them sequentially. Also, twenty per channel does not mean forty unique chunks because their results can overlap.]

## 8. Weighted RRF: Combining the Two Lists

[Point to the merging RRF box.]

“The two search methods return different kinds of scores, so we do not simply add their raw scores together.

Instead, we use weighted Reciprocal Rank Fusion. It combines the positions of passages in the two ranked lists.

For example, if a passage appears near the top of both lists, it receives a contribution from both channels. A passage found by only one method can still remain a candidate.

The configured weights are zero point five five for dense retrieval and zero point four five for BM25, with a smoothing constant of fifty. We keep up to fifteen candidates after fusion.

These are implementation settings, not accuracy percentages. Their purpose is to combine semantic and lexical signals while slightly favoring the dense channel.”

[Understanding: do not claim these exact weights were optimized or that hybrid must outperform dense. If asked, say the study compared the selected configuration and found domain-dependent trade-offs.]

## 9. Reranking: A Closer Look at Each Candidate

[Point to the reranking box.]

“Next, the reranker compares the question and each candidate passage together.

This differs from the first dense search, where passage vectors were prepared beforehand. The cross-encoder reranker jointly reads the query and candidate text and produces a new relevance score.

The idea is to take a closer look at a smaller shortlist rather than perform that more expensive comparison against every passage in the database.

The system also has a word-overlap fallback if the cross-encoder cannot load.

The base reranker is shared across all three domains. The additional birth-registration-specific adjustments shown here apply only to that domain. Our passport example does not receive those extra registration rules.”

[Understanding: the final selected-evidence path can pass up to fifteen reranked candidates to selection, not automatically only six. The six-passage limit is applied later.]

## 10. Why Resolve Chunk IDs Back to Content?

[Point to Resolve Source Content.]

“Search results remain linked to their source records through chunk IDs. We use the local chunk map, which is a dictionary from each ID to its text and metadata, to prepare the evidence records.

This is important because the language model needs readable source text. We do not give it the dense vectors and expect it to reconstruct the document.

The identifier is the connection between finding a passage and supplying that same passage as evidence.”

[Understanding: the code already accesses chunk text during earlier stages such as reranking. This diagram box summarizes evidence preparation; it is not the first moment the program reads content. The map is built in RAM from JSONL, not a second independent dataset.]

## 11. Automatic Evidence Selector: Bangla Explanation

[Follow the arrow downward on the RIGHT. Explain this box in Bangla if that fits your presentation. From here, the diagram flows RIGHT TO LEFT.]

“এখন আমাদের কাছে কিছু candidate passage আছে। কিন্তু কোনো passage পাসপোর্ট নিয়ে কথা বললেই যে সেটি আমাদের প্রশ্নের উত্তর দেবে, তা নয়।

আমাদের প্রশ্ন হচ্ছে, ‘নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?’ অন্যদিকে কোনো passage হয়তো তৈরি হয়ে যাওয়া পাসপোর্ট সংগ্রহ করার কাগজপত্র নিয়ে আলোচনা করছে। দুটোতেই পাসপোর্ট আর কাগজপত্রের কথা আছে, কিন্তু কাজটা আলাদা।

এই পার্থক্য যাচাই করার জন্য আমরা automatic evidence selector ব্যবহার করেছি। এটি আরেকটি LLM নয়, এবং এখানে কোনো মানুষ প্রতিটি প্রশ্নের জন্য passage বেছে দিচ্ছে না। এটি code-এর একটি rule-based function।

এটি প্রশ্ন এবং passage-এর মধ্যে service, action এবং প্রযোজ্য conditions মিলিয়ে দেখে। এখানে service হচ্ছে passport, আর action হচ্ছে নতুন আবেদন। কোনো passage-এর action যদি collection বা cancellation হিসেবে চিহ্নিত হয় এবং প্রশ্নের সঙ্গে না মেলে, তাহলে সেটি বাদ দেওয়া হতে পারে।

Selector শুধু বাদ দেয় না। আগে পাওয়া কোনো checklist বা fee section-এর সঙ্গে সম্পর্কিত আরেকটি অংশ একই document-এর compatible section-এ থাকলে, সেটি আমাদের local corpus থেকে যোগও করতে পারে। অর্থাৎ নতুন তথ্য বানায় না; আগে থেকে সংরক্ষিত passage যোগ করে।

একই checklist-এর compatible continuation-গুলো কাছাকাছি রাখা হয়, যাতে context-এর limit দেওয়ার সময় তার পরের অংশ সহজে বাদ না পড়ে।

সবশেষে সর্বোচ্চ ছয়টি passage এবং মোট চৌদ্দ হাজার character-এর মধ্যে evidence রাখা হয়। কোনো chunk এই সীমার মধ্যে না ধরলে সেটিকে মাঝখান থেকে কেটে দেওয়ার বদলে বাদ দেওয়া হয়। পরে ছোট কোনো chunk থাকলে সেটি জায়গা পেতে পারে।

এখানে উদ্দেশ্য হলো শুধু একই topic-এর লেখা নয়, প্রশ্নে চাওয়া কাজের সঙ্গে মানানসই evidence পাঠানো। তবে এগুলো rule-based checks; প্রতিটি passage-এর factual correctness যাচাই করার ব্যবস্থা নয়।”

[Simpler keywords: applicability = এই প্রশ্নের এই কাজের জন্য তথ্যটি প্রযোজ্য কি না; candidate = সম্ভাব্য passage; continuation = একই অংশের পরের লেখা; corpus = আগে থেকে সংরক্ষিত সব source text.]

### English alternative if you want one language throughout

“A passage can mention passports but describe the wrong procedure. Our rule-based selector checks whether the detected service, action and conditions match the question. It can exclude incompatible passages and add existing compatible checklist or fee continuations from the local corpus. We then select up to six whole passages within fourteen thousand characters. This is applicability screening, not independent fact verification.”

## 12. What Does “Any Selected Evidence?” Mean?

[Point to the decision diamond.]

“After selection, we check whether any evidence remains.

If nothing remains, we return an insufficient-information or clarification message. We do not ask the model to invent the missing procedure.

If evidence remains, we move to the prompt-building stage.”

[Understanding: no selected evidence does not prove the database or government has no answer. Retrieval or screening may have missed it. Likewise, nonempty evidence does not guarantee complete support.]

## 13. The Evidence-Only Prompt: Explain Each Phrase

[Point to Evidence-Only Prompt.]

“The prompt is the package we send to the language model. It contains instructions, the user's question, and the selected passage text.

‘Question plus selected content’ means we give the actual question together with the evidence selected for it, not the whole database.

‘Preserve source conditions’ means the model should keep important qualifications. For example, if a passage says a requirement applies only to a particular applicant category, the answer should not present it as mandatory for everyone.

‘Request Bangla answer’ means the model is instructed to explain the supported information in Bangla.

The prompt also tells the model not to mix different procedures and to identify missing information rather than fill gaps with unsupported details.”

### Simple Bangla explanation for your understanding

“Prompt মানে model-কে দেওয়া নির্দেশনা এবং input। আমরা বলছি: এই প্রশ্নটির উত্তর দাও, নিচের নির্বাচিত source text ব্যবহার করো, source-এর শর্ত বাদ দিও না, এবং বাংলায় উত্তর দাও।

যেমন source-এ ‘প্রযোজ্য ক্ষেত্রে’ বলা থাকলে, সেটিকে ‘সবার জন্য বাধ্যতামূলক’ বানানো যাবে না।”

[Understanding: evidence-only is the intended instruction, not a technical guarantee that the model cannot draw on pretrained knowledge or hallucinate. Do not say prompt wording independently verifies facts.]

## 14. Local Qwen Generation Through Ollama

[Move left to Local LLM via Ollama.]

“Qwen3 eight-billion then generates the response from this question-and-evidence package. Ollama is the local software used to run the model.

This is the stage that writes the answer. BGE-M3 represented the text, BM25 matched words, the reranker scored candidates, and the selector chose evidence. None of those earlier stages generated the final response.

For the documented comparison, we used fixed generation settings, including a temperature of zero point zero five. This is a low-randomness setting, not a guarantee of accuracy or identical wording across runs.”

[Optional implementation detail if asked: top-p 0.9, output allowance 1,200 tokens, configured selected-route context window 8,192 tokens. Do not confuse tokens with the selector's 14,000-character evidence budget. These values are not proven optimal.]

## 15. Output Checks and the Final Answer

[Move left through Output Checks to Final Response.]

“Before displaying the response, the system applies output handling. It can reject unsuitable-language output and add a warning if generation stopped because the output limit was reached. It also formats the source identifiers consistently.

The user then receives a Bangla answer and can inspect the supplied evidence and available source links.

For our running question, the intended result is a document-requirements answer that retains the conditions supported by the selected passages.

The source links make the answer traceable. They do not mean that every generated sentence has been independently fact-checked.

So the complete journey is: prepared documents, searchable passages, retrieved candidates, applicable evidence, and finally a generated answer.”

[Understanding: do not promise a particular checklist or identical previously saved wording. This script explains the path, not a newly executed answer. Old controlled-answer branches in the code are bypassed by the evaluated selected-evidence route.]

## 16. Transition to the Implementation-Equation Slide

[Change slide.]

“The next slide summarizes four implementation decisions behind the boxes we just followed.”

[Point to vector normalization.]

“First, vector normalization gives our query and passage embeddings unit length for consistent vector comparison.”

[Point to weighted RRF.]

“Second, weighted RRF combines the rank positions from dense and keyword retrieval. A passage can receive contributions from either or both channels.”

[Point to applicability priority.]

“Third, the applicability priority gives preference to matching actions, services and requested information types. This is one rule within the broader selector, not the entire algorithm.”

[Point to whole-passage budget.]

“Finally, the budget limits the selected context to six whole passages and fourteen thousand characters. It bounds the input while avoiding cutting an included chunk in the middle.”

“These are the settings used in our implementation. We evaluate their combined behavior; we do not claim that every numerical value is optimal.”

[Notation reminder: use h(q,c_i) for the same question q checked against different chunks. In the budget equation, c_i is a chunk record and e_i its evidence text. You do not have to explain every symbol unless asked.]

## 17. Evaluation-Boundary Slide and Handover

[Change slide. Spend about 15-20 seconds here, not another full architecture explanation.]

“We evaluated this work in two ways: first, by comparing CivicRAG and Simple RAG answers under matched generation settings; second, by comparing BM25, Dense and Hybrid retrieval separately. My teammate will now explain the evaluation metrics and results.”

## Your Memory Chain

Read this once before rehearsing without the full script:

```text
Tapu's prepared documents
-> chunks with headings and source IDs
-> search text versus evidence content
-> dense vectors in Chroma + separate BM25 index
-> user selects passport and asks the question
-> normalize question
-> up to 20 results per retrieval channel
-> RRF combines ranks, keeps up to 15
-> reranker reads query and candidate together
-> IDs maintain the link to source content
-> selector checks action/service/conditions and expands compatible sections
-> up to 6 whole passages / 14,000 characters
-> none: clarification
-> otherwise: question + selected text + instructions
-> Qwen generates through Ollama
-> language/truncation/source-ID handling
-> Bangla response with inspectable evidence
-> four implementation equations
-> evaluation handover
```

## Five Points You Must Not Accidentally Change While Improvising

1. BM25 is not an embedding model and does not generate an answer.
2. BM25's index is not stored together with dense vectors inside Chroma in this implementation.
3. The selector is rule-based and automatic, not manual selection or another LLM.
4. Additional registration-specific adjustments apply to birth/death registration, not BRTA.
5. This is a source-grounded generation design, not a guarantee of factual correctness or a model-training pipeline.

## Related Detailed Guides

- [Architecture breakdown, equations and panel questions](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/presentation/Shihab_Architecture_Breakdown_and_Script.md)
- [Implementation clarifications with actual code and corpus paths](/Users/shihab/Downloads/AI/Courses/01Portfolio/LangChainKrisnaik/playground/bilingual-rag-thesis/docs/presentation/Team_Implementation_Questions_Explained.md)

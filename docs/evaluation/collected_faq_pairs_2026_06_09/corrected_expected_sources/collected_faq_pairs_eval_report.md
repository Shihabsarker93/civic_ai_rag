# Collected FAQ Pair Evaluation

Generated: 2026-06-09T21:47:50
Input dataset: `docs/evaluation/collected_faq_pairs_2026_06_09/collected_faq_pairs_corrected_expected_sources.json`
Evaluation cases: 24 query variants from 13 expected FAQ chunks.

## What This Measures

- Source retrieval: whether the expected FAQ chunk appears in top-k retrieved evidence.
- Answer-evidence similarity: whether the top retrieved chunk contains answer-like text similar to the collected reference answer.
- Paraphrase consistency: whether the curated question and original citizen-style question retrieve the same/similar expected evidence.
- This pass avoids local LLM generation so one slow model call cannot hide retrieval errors.

## Summary

| Method | Cases | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Top answer semantic sim | Top answer token F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dense_only | 24 | 0.7917 | 0.9583 | 1.0000 | 0.8854 | 0.9148 | 0.9051 | 0.7015 |
| bm25_only | 24 | 0.8333 | 0.9167 | 0.9167 | 0.8819 | 0.8859 | 0.8947 | 0.6842 |
| hybrid_rrf | 24 | 0.7917 | 0.9583 | 1.0000 | 0.8785 | 0.9093 | 0.8904 | 0.6812 |

## Paraphrase Consistency

- Both curated and original question hit expected source in top-5: 0.9394
- Curated and original question returned same top source: 0.6667

## hybrid_rrf Cases To Inspect

| Case | Category | Expected chunk | Rank | Top chunk | Similarity | Query |
|---|---|---|---:|---|---:|---|
| curated_question | parents_registration | `bdris_faq_01_q01` | 4 | `application_for_birth_information_correction_cleaned_005_01` | 0.7009 | পিতা-মাতার জন্ম নিবন্ধন নম্বর না থাকলে সন্তানের জন্ম নিবন্ধন করার ক্ষেত্রে কীভাবে এগোনো উচিত? |
| curated_question | bilingual_registration | `bdris_faq_01_q04` | 3 | `bdris_faq_01_q08` | 0.5818 | শুধুমাত্র বাংলা ভাষায় করা জন্ম বা মৃত্যু নিবন্ধনে ইংরেজি তথ্য যুক্ত করার প্রক্রিয়া কী? |
| curated_question | fee_and_challan | `bdris_faq_01_q13` | 1 | `bdris_faq_01_q13` | 0.7068 | জন্ম নিবন্ধনের ফি বাবদ চালানের তথ্য BDRIS-এ আপলোড করতে সমস্যা হলে করনীয় কী? |
| original_question | fee_and_challan | `bdris_faq_01_q13` | 1 | `bdris_faq_01_q13` | 0.7068 | জন্ম নিবন্ধনের ফি বাবদ চালানের তথ্য BDRIS-এ আপলোড করতে সমস্যা হলে করনীয় কী? |

## Interpretation

For this dataset, the strongest requirement is not that the generated wording is identical. The first requirement is that the expected official evidence is retrieved. If Hit@5 is high but answer similarity is lower, the issue is likely generation/answer formatting. If Hit@5 is low, the issue is retrieval, chunking, metadata, or query-intent handling.

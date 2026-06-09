# Collected FAQ Pair Qualitative Evaluation

Date: 2026-06-09

Pipeline commit: `c07637f`

Method focus: `Hybrid RRF retrieval` plus comparison against `dense_only` and `BM25-only`.

Question set: 13 collected FAQ answer pairs. Each pair is evaluated with two query variants where available:

- `curated_question`: cleaner/manual reformulation.
- `original_question`: original or alternate citizen-style question.

Important note: this report is the qualitative evidence-retrieval layer, not a full 3-model generation run. It checks whether the RAG system retrieves the expected official answer evidence for both the new question and alternate/original question. This is the layer we should trust before judging LLM wording.

## Evaluation Summary

| Method | Cases | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Top Answer Semantic Similarity |
|---|---:|---:|---:|---:|---:|---:|---:|
| dense_only | 24 | 0.7917 | 0.9583 | 1.0000 | 0.8854 | 0.9148 | 0.9051 |
| bm25_only | 24 | 0.8333 | 0.9167 | 0.9167 | 0.8819 | 0.8859 | 0.8947 |
| hybrid_rrf | 24 | 0.7917 | 0.9583 | 1.0000 | 0.8785 | 0.9093 | 0.8904 |

## Main Finding

After auditing source labels, `dense_only` and `hybrid_rrf` both retrieve the expected evidence in top-5 for all 24 query variants. This means the main retrieval backbone is working well for the collected FAQ-style questions. BM25 is slightly better at Hit@1, while dense/hybrid are better at Hit@5.

## Dataset Audit Finding

Two provided expected `chunk_id` values appeared mismatched with the answer text. The audit matched them to the correct chunks using answer-level semantic similarity:

| Provided chunk | Corrected expected chunk | Reason |
|---|---|---|
| `bdris_faq_01_q12` | `bdris_faq_01_q13` | answer similarity improved from 0.4489 to 0.7068 |
| `bdris_faq_01_q13` | `bdris_faq_01_q15` | answer similarity improved from 0.4755 to 0.8115 |

## Overall Question-Level Result

| FAQ | Category | Curated Question Result | Original/Alternate Question Result | Interpretation |
|---|---|---|---|---|
| `bdris_faq_01_q01` | `parents_registration` | Partial | Good / Needs ranking improvement | Expected evidence is found for both variants, but top ranking can be improved. |
| `bdris_faq_01_q02` | `manual_to_online_migration` | Strong | Strong | Stable across available query variant(s). |
| `bdris_faq_01_q03` | `data_correction_legacy` | Strong | No alternate | Stable across available query variant(s). |
| `bdris_faq_01_q04` | `bilingual_registration` | Partial | Strong | Expected evidence is found for both variants, but top ranking can be improved. |
| `bdris_faq_01_q05` | `special_cases` | Strong | Strong | Stable across available query variant(s). |
| `bdris_faq_01_q06` | `registration_number` | Strong | No alternate | Stable across available query variant(s). |
| `bdris_faq_01_q07` | `married_women_registration` | Good / Needs ranking improvement | Strong | Expected evidence is found for both variants, but top ranking can be improved. |
| `bdris_faq_01_q08` | `certificate_language` | Strong | Strong | Stable across available query variant(s). |
| `bdris_faq_01_q09` | `mobile_number_policy` | Good / Needs ranking improvement | Good / Needs ranking improvement | Expected evidence is found for both variants, but top ranking can be improved. |
| `bdris_faq_01_q10` | `special_cases` | Strong | Strong | Stable across available query variant(s). |
| `bdris_faq_01_q11` | `special_cases` | Strong | Strong | Stable across available query variant(s). |
| `bdris_faq_01_q13` | `fee_and_challan` | Partial | Partial | Expected evidence is found for both variants, but top ranking can be improved. |
| `bdris_faq_01_q15` | `duplicate_registration` | Good / Needs ranking improvement | Good / Needs ranking improvement | Expected evidence is found for both variants, but top ranking can be improved. |

## FAQ 1: `bdris_faq_01_q01`

Category: `parents_registration`

### Expected Reference Answer

জন্ম ও মৃত্যু নিবন্ধন আইন ২০০৪ অনুযায়ী জন্ম নিবন্ধন সকলের জন্য বাধ্যতামূলক (ধারা ৫(১), ৬ক এবং ৮(১))। আইন না মানলে অনধিক ৫০০০ টাকা অর্থদণ্ড হতে পারে। বিদ্যালয়ে ভর্তি, চাকরি, পাসপোর্ট, জাতীয় পরিচয়পত্রসহ ১৯টি ক্ষেত্রে জন্ম সনদ আবশ্যক। জন্ম নিবন্ধন ছাড়া মৃত্যু নিবন্ধন করা যাবে না এবং মৃত্যু নিবন্ধন ছাড়া উত্তরাধিকার নিশ্চিত করা যাবে না।

সন্তানের জন্ম নিবন্ধনের সঙ্গে পিতামাতার জন্ম নিবন্ধন একসাথে করা অপেক্ষাকৃত সহজ। সন্তানের নিবন্ধনের প্রয়োজনীয় তথ্যের সঙ্গে পিতামাতার বয়স প্রমাণের রেকর্ড (শিক্ষা সনদ বা আইনের ৭(১) ধারা অনুযায়ী তদন্তসহ এনআইডি) যোগ করলেই তাদের জন্ম নিবন্ধন করা সম্ভব।

আন্তর্জাতিকভাবে গৃহীত 'ফ্যামিলি ট্রি' পদ্ধতিতে সন্তানের নিবন্ধনের সঙ্গে পিতামাতার নম্বর যুক্ত করে পারিবারিক কাঠামো তৈরি করা হয়। এতে উত্তরাধিকার নিশ্চিত হয়, তথ্য পরিবর্তনের প্রবণতা রোধ হয় এবং ভবিষ্যতে 'পপুলেশন রেজিস্টার' প্রণয়নে সহায়ক হবে।

### Curated/New Question

পিতা-মাতার জন্ম নিবন্ধন নম্বর না থাকলে সন্তানের জন্ম নিবন্ধন করার ক্ষেত্রে কীভাবে এগোনো উচিত?

Judgement: **Partial**

Interpretation: Expected evidence is present, but the top answer is not close enough to the reference.

Expected source rank: `4`

Top retrieved source: `application_for_birth_information_correction_cleaned_005_01`

Top answer semantic similarity: `0.7009`

Token F1 against reference: `0.1860`

Retrieved answer/evidence used for comparison:

আপনার জন্ম নিবন্ধন করার সময় যদি পিতা বা মাতার জন্ম নিবন্ধন নম্বর প্রদান করা না হয়ে থাকে, তাহলে আপনার জন্ম নিবন্ধন নম্বরের সাথে পিতা বা মাতার জন্ম নিবন্ধন নম্বর ম্যাপ করতে হবে।

ম্যাপিং সম্পন্ন হওয়ার পর জন্ম নিবন্ধন সনদ পুনর্মুদ্রণ করলে সেখানে সংশোধিত নাম প্রদর্শিত হবে।

---

Top retrieved / selected candidates:

1. `application_for_birth_information_correction_cleaned_005_01`
2. `application_for_birth_information_correction_cleaned_006_01`
3. `application_for_birth_information_correction_cleaned_008_01`
4. `bdris_faq_01_q01`
5. `birth_registration_application_process_02_cleaned_007_01`
6. `bdris_faq_02_q01`

### Original/Alternate Question

জন্মের ৪৫ দিনের মধ্যে কিংবা পরবর্তী সময়েও নিবন্ধন করতে অনেক সময় পিতা মাতার জন্ম নিবন্ধন পাওয়া যায় না, করণীয় কী?

Judgement: **Good / Needs ranking improvement**

Interpretation: Expected evidence is retrieved in top-5, but not always as the first result.

Expected source rank: `2`

Top retrieved source: `bdris_faq_02_q01`

Top answer semantic similarity: `0.7931`

Token F1 against reference: `0.4792`

Retrieved answer/evidence used for comparison:

সন্তানের জন্ম নিবন্ধনের সঙ্গে পিতামাতার জন্ম নিবন্ধন একসাথে করা অপেক্ষাকৃত সহজ। সন্তানের নিবন্ধনের প্রয়োজনীয় তথ্যের সঙ্গে পিতামাতার বয়স প্রমাণের রেকর্ড (শিক্ষা সনদ বা আইনের ৭(১) ধারা অনুযায়ী তদন্তসহ এনআইডি) যোগ করলেই তাদের জন্ম নিবন্ধন করা সম্ভব। বিষয়টিকে সমস্যা না ভেবে 'সুযোগ' হিসেবে দেখা যেতে পারে।

তবে পূর্ব থেকে পিতামাতার নিবন্ধন থাকলে এবং তাতে ভুল থাকলে, সন্তানের নিবন্ধনের আগে সংশোধন আবেদন করে সংশোধন করে নিতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_02_q01`
2. `bdris_faq_01_q01`
3. `birth_and_death_registration_act_2004_ধারা_৮_01`
4. `birth_and_death_registration_rules_2018_বিধি_৯_02`
5. `birth_and_death_registration_rules_2018_বিধি_৮_01`
6. `application_for_birth_information_correction_cleaned_008_01`

## FAQ 2: `bdris_faq_01_q02`

Category: `manual_to_online_migration`

### Expected Reference Answer

ম্যানুয়াল জন্ম নিবন্ধনসমূহ অনলাইনে অন্তর্ভুক্তির জন্য একাধিকবার সময় দেওয়া হয়েছে। এখন একই নম্বর দিয়ে অনলাইনে অন্তর্ভুক্তির সুযোগ নেই। যে এলাকায় হাতে লেখা নিবন্ধন হয়েছিল সেই কার্যালয়ে রক্ষিত বইতে তথ্য পাওয়া গেলে, নিবন্ধক সরাসরি সেই তথ্য দিয়ে অনলাইন নিবন্ধন করে দেবেন — যদি ইতঃপূর্বে অন্য কোথাও নিবন্ধন না হয়ে থাকে। তবে নিবন্ধন নম্বর পরিবর্তিত হবে; এতে নাগরিকের কোনো ক্ষতি বা অসুবিধা হবে না।

### Curated/New Question

পুরোনো ম্যানুয়াল জন্ম নিবন্ধন অনলাইন সিস্টেমে অন্তর্ভুক্ত করার নিয়ম কী?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q02`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

ম্যানুয়াল জন্ম নিবন্ধনসমূহ অনলাইনে অন্তর্ভুক্তির জন্য একাধিকবার সময় দেওয়া হয়েছে। এখন একই নম্বর দিয়ে অনলাইনে অন্তর্ভুক্তির সুযোগ নেই। যে এলাকায় হাতে লেখা নিবন্ধন হয়েছিল সেই কার্যালয়ে রক্ষিত বইতে তথ্য পাওয়া গেলে, নিবন্ধক সরাসরি সেই তথ্য দিয়ে অনলাইন নিবন্ধন করে দেবেন — যদি ইতঃপূর্বে অন্য কোথাও নিবন্ধন না হয়ে থাকে। তবে নিবন্ধন নম্বর পরিবর্তিত হবে; এতে নাগরিকের কোনো ক্ষতি বা অসুবিধা হবে না।

Top retrieved / selected candidates:

1. `bdris_faq_01_q02`
2. `bdris_faq_02_q03`
3. `know_this_01_cleaned_002_01`
4. `birth_and_death_registration_rules_2018_বিধি_২০_01`
5. `birth_registration_application_process_cleaned_012_01`
6. `birth_and_death_registration_rules_2018_বিধি_১৯_01`

### Original/Alternate Question

ম্যানুয়াল জন্ম নিবন্ধন, যেগুলি এখনও অনলাইনে করা হয়নি — এগুলির বিষয়ে করণীয় কী?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q02`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

ম্যানুয়াল জন্ম নিবন্ধনসমূহ অনলাইনে অন্তর্ভুক্তির জন্য একাধিকবার সময় দেওয়া হয়েছে। এখন একই নম্বর দিয়ে অনলাইনে অন্তর্ভুক্তির সুযোগ নেই। যে এলাকায় হাতে লেখা নিবন্ধন হয়েছিল সেই কার্যালয়ে রক্ষিত বইতে তথ্য পাওয়া গেলে, নিবন্ধক সরাসরি সেই তথ্য দিয়ে অনলাইন নিবন্ধন করে দেবেন — যদি ইতঃপূর্বে অন্য কোথাও নিবন্ধন না হয়ে থাকে। তবে নিবন্ধন নম্বর পরিবর্তিত হবে; এতে নাগরিকের কোনো ক্ষতি বা অসুবিধা হবে না।

Top retrieved / selected candidates:

1. `bdris_faq_01_q02`
2. `bdris_faq_02_q03`
3. `birth_and_death_registration_rules_2018_বিধি_২০_01`
4. `bdris_faq_01_q01`
5. `birth_and_death_registration_rules_2018_বিধি_৯_04`
6. `know_this_01_cleaned_008_01`

## FAQ 3: `bdris_faq_01_q03`

Category: `data_correction_legacy`

### Expected Reference Answer

পূর্বে সংশোধিত তথ্য BDRIS-এ না পাওয়া গেলে, সংশোধনের বিস্তারিত তালিকা নির্বাহী অফিসার/ডিডিএলজির মাধ্যমে রেজিস্ট্রার জেনারেলের কার্যালয়ে পাঠালে তা হালনাগাদ করে দেওয়া হবে।

### Curated/New Question

পূর্বের সফটওয়্যারে সংশোধিত কোনো তথ্য BDRIS সফটওয়্যারে পাওয়া না গেলে কী করতে হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q03`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

পূর্বে সংশোধিত তথ্য BDRIS-এ না পাওয়া গেলে, সংশোধনের বিস্তারিত তালিকা নির্বাহী অফিসার/ডিডিএলজির মাধ্যমে রেজিস্ট্রার জেনারেলের কার্যালয়ে পাঠালে তা হালনাগাদ করে দেওয়া হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q03`
2. `notice_birth_and_death_registration_certificate_correction_steps_ocr_005_01`
3. `notice_birth_and_death_registration_certificate_correction_steps_ocr_003_01`
4. `notice_birth_and_death_registration_certificate_correction_steps_ocr_002_01`
5. `application_for_birth_information_correction_cleaned_005_01`
6. `home_registrar_generals_office_birth_and_death_registration_011_01`

## FAQ 4: `bdris_faq_01_q04`

Category: `bilingual_registration`

### Expected Reference Answer

সফটওয়্যারে যেকোনো তথ্য সংযোজন বা বিয়োজন সংশোধন হিসেবে গণ্য হয়। ইংরেজি তথ্য যোগ করা হলে তা সংশোধন হিসেবে গণ্য হবে এবং জন্ম ও মৃত্যু নিবন্ধন বিধিমালা ২০১৮-এর ১৫ বিধি অনুযায়ী সংশোধন প্রক্রিয়া অনুসরণ করতে হবে।

### Curated/New Question

শুধুমাত্র বাংলা ভাষায় করা জন্ম বা মৃত্যু নিবন্ধনে ইংরেজি তথ্য যুক্ত করার প্রক্রিয়া কী?

Judgement: **Partial**

Interpretation: Expected evidence is present, but the top answer is not close enough to the reference.

Expected source rank: `3`

Top retrieved source: `bdris_faq_01_q08`

Top answer semantic similarity: `0.5818`

Token F1 against reference: `0.2951`

Retrieved answer/evidence used for comparison:

হ্যাঁ, বাধ্যতামূলকভাবে উভয় ভাষায় সনদ দিতে হবে। আবেদনপত্র গ্রহণের সময় জন্ম তথ্য বাংলা ও ইংরেজি উভয় ভাষায় পূরণ করা হয়েছে কিনা তা নিশ্চিত করতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q08`
2. `birth_and_death_registration_fees_cleaned_fee_row_06`
3. `bdris_faq_01_q04`
4. `bdris_faq_02_q02`
5. `birth_registration_application_process_cleaned_013_01`
6. `birth_and_death_registration_fees_cleaned_fee_row_07`

### Original/Alternate Question

পূর্বের যে সকল জন্ম-মৃত্যু নিবন্ধন শুধু বাংলায় আছে সেগুলি কীভাবে ইংরেজিতে করা হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q04`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

সফটওয়্যারে যেকোনো তথ্য সংযোজন বা বিয়োজন সংশোধন হিসেবে গণ্য হয়। ইংরেজি তথ্য যোগ করা হলে তা সংশোধন হিসেবে গণ্য হবে এবং জন্ম ও মৃত্যু নিবন্ধন বিধিমালা ২০১৮-এর ১৫ বিধি অনুযায়ী সংশোধন প্রক্রিয়া অনুসরণ করতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q04`
2. `bdris_faq_02_q02`
3. `birth_and_death_registration_rules_2018_বিধি_৩_02`
4. `birth_registration_application_process_cleaned_012_01`
5. `bdris_faq_01_q08`
6. `birth_and_death_registration_fees_cleaned_fee_row_06`

## FAQ 5: `bdris_faq_01_q05`

Category: `special_cases`

### Expected Reference Answer

জমজ সন্তানের জন্ম নিবন্ধনের ক্ষেত্রে প্রথমে একটি আবেদন অনলাইনে সাবমিট করে নিবন্ধন সম্পন্ন করতে হবে, তারপর দ্বিতীয় আবেদন সাবমিট করতে হবে। একসাথে দুটি আবেদন সাবমিট করলে সমস্যা হবে।

### Curated/New Question

জমজ সন্তানের জন্ম নিবন্ধনের আবেদন অনলাইনে কীভাবে সম্পন্ন করতে হয়?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q05`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

জমজ সন্তানের জন্ম নিবন্ধনের ক্ষেত্রে প্রথমে একটি আবেদন অনলাইনে সাবমিট করে নিবন্ধন সম্পন্ন করতে হবে, তারপর দ্বিতীয় আবেদন সাবমিট করতে হবে। একসাথে দুটি আবেদন সাবমিট করলে সমস্যা হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q05`
2. `bdris_faq_02_q04`
3. `birth_registration_application_process_cleaned_003_01`
4. `birth_and_death_registration_rules_2018_বিধি_২০_01`
5. `birth_and_death_registration_rules_2018_বিধি_৯_04`
6. `birth_and_death_registration_rules_2018_বিধি_১০_01`

### Original/Alternate Question

জমজ সন্তানের জন্ম নিবন্ধন কীভাবে করা হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q05`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

জমজ সন্তানের জন্ম নিবন্ধনের ক্ষেত্রে প্রথমে একটি আবেদন অনলাইনে সাবমিট করে নিবন্ধন সম্পন্ন করতে হবে, তারপর দ্বিতীয় আবেদন সাবমিট করতে হবে। একসাথে দুটি আবেদন সাবমিট করলে সমস্যা হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q05`
2. `bdris_faq_02_q04`
3. `birth_registration_application_process_cleaned_003_01`
4. `bdris_faq_01_q10`
5. `bdris_faq_01_q11`
6. `bdris_faq_01_q01`

## FAQ 6: `bdris_faq_01_q06`

Category: `registration_number`

### Expected Reference Answer

১৭ ডিজিটের কম নম্বর হলে পুরাতন সনদটি সংশ্লিষ্ট নিবন্ধকের কার্যালয়ে জমা দিয়ে ১৭ ডিজিটের নম্বর সম্বলিত নতুন সনদ নেওয়া যাবে। এক্ষেত্রে নিবন্ধনাধীন ব্যক্তির নিজস্ব মোবাইল নম্বর ব্যবহার করতে হবে।

### Curated/New Question

১৭ ডিজিটের কম জন্ম নিবন্ধন নম্বর কিভাবে ১৭ ডিজিটে উন্নীত করা যাবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q06`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

১৭ ডিজিটের কম নম্বর হলে পুরাতন সনদটি সংশ্লিষ্ট নিবন্ধকের কার্যালয়ে জমা দিয়ে ১৭ ডিজিটের নম্বর সম্বলিত নতুন সনদ নেওয়া যাবে। এক্ষেত্রে নিবন্ধনাধীন ব্যক্তির নিজস্ব মোবাইল নম্বর ব্যবহার করতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q06`
2. `bdris_faq_02_q05`
3. `know_this_01_cleaned_009_01`
4. `bdris_faq_01_q16`
5. `application_for_birth_information_correction_cleaned_006_01`
6. `application_for_birth_information_correction_cleaned_008_01`

## FAQ 7: `bdris_faq_01_q07`

Category: `married_women_registration`

### Expected Reference Answer

আইনের ৪ ধারা অনুযায়ী, পূর্বে নিবন্ধন না হলে বিবাহিত নারীর বিলম্বিত জন্ম নিবন্ধন স্বামীর স্থায়ী ঠিকানায় করা যাবে অথবা তার জন্মস্থানের ঠিকানায়ও করা যাবে। তবে জন্ম নিবন্ধনে পিতা ও মাতার নাম লিখতে হবে — স্বামীর নাম লেখার সুযোগ নেই।

### Curated/New Question

বিবাহিত নারীর জন্ম নিবন্ধন কি স্বামীর ঠিকানায় করা যায় এবং এতে স্বামীর নাম অন্তর্ভুক্ত করা যায় কি?

Judgement: **Good / Needs ranking improvement**

Interpretation: Expected evidence is retrieved in top-5, but not always as the first result.

Expected source rank: `2`

Top retrieved source: `bdris_faq_02_q06`

Top answer semantic similarity: `0.9786`

Token F1 against reference: `0.7941`

Retrieved answer/evidence used for comparison:

আইনের ৪ ধারা অনুযায়ী বিবাহিত নারীর বিলম্বিত জন্ম নিবন্ধন স্বামীর স্থায়ী ঠিকানায় বা জন্মস্থানের ঠিকানায় করা যাবে। তবে সনদে পিতা ও মাতার নাম লিখতে হবে — স্বামীর নাম লেখার সুযোগ নেই।

Top retrieved / selected candidates:

1. `bdris_faq_02_q06`
2. `bdris_faq_01_q07`
3. `birth_registration_application_process_02_cleaned_005_01`
4. `bdris_faq_02_q08`
5. `bdris_faq_01_q10`
6. `birth_and_death_registration_rules_2018_বিধি_৩_01`

### Original/Alternate Question

পূর্বে নিবন্ধন না হয়ে থাকলে বিবাহিত নারীর জন্ম নিবন্ধন স্বামীর বাড়ির ঠিকানায় করা এবং সনদে স্বামীর নাম লিখা যাবে কি?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q07`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

আইনের ৪ ধারা অনুযায়ী, পূর্বে নিবন্ধন না হলে বিবাহিত নারীর বিলম্বিত জন্ম নিবন্ধন স্বামীর স্থায়ী ঠিকানায় করা যাবে অথবা তার জন্মস্থানের ঠিকানায়ও করা যাবে। তবে জন্ম নিবন্ধনে পিতা ও মাতার নাম লিখতে হবে — স্বামীর নাম লেখার সুযোগ নেই।

Top retrieved / selected candidates:

1. `bdris_faq_01_q07`
2. `bdris_faq_02_q06`
3. `application_for_birth_information_correction_cleaned_005_01`
4. `birth_and_death_registration_rules_2018_বিধি_৩_01`
5. `bdris_faq_01_q01`
6. `birth_and_death_registration_rules_2018_বিধি_৩_02`

## FAQ 8: `bdris_faq_01_q08`

Category: `certificate_language`

### Expected Reference Answer

হ্যাঁ, বাধ্যতামূলকভাবে উভয় ভাষায় সনদ দিতে হবে। আবেদনপত্র গ্রহণের সময় জন্ম তথ্য বাংলা ও ইংরেজি উভয় ভাষায় পূরণ করা হয়েছে কিনা তা নিশ্চিত করতে হবে।

### Curated/New Question

জন্ম ও মৃত্যু সনদ কি বাধ্যতামূলকভাবে বাংলা ও ইংরেজি উভয় ভাষায় প্রদান করতে হয়?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q08`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

হ্যাঁ, বাধ্যতামূলকভাবে উভয় ভাষায় সনদ দিতে হবে। আবেদনপত্র গ্রহণের সময় জন্ম তথ্য বাংলা ও ইংরেজি উভয় ভাষায় পূরণ করা হয়েছে কিনা তা নিশ্চিত করতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q08`
2. `birth_and_death_registration_fees_cleaned_fee_row_06`
3. `birth_and_death_registration_fees_cleaned_fee_row_07`
4. `bdris_faq_01_q04`
5. `bdris_faq_02_q02`
6. `birth_registration_application_process_cleaned_013_01`

### Original/Alternate Question

নিবন্ধনাধীন ব্যক্তিকে কি বাংলা ও ইংরেজি উভয় ভাষায় সনদ দিতে হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q08`

Top answer semantic similarity: `1.0000`

Token F1 against reference: `1.0000`

Retrieved answer/evidence used for comparison:

হ্যাঁ, বাধ্যতামূলকভাবে উভয় ভাষায় সনদ দিতে হবে। আবেদনপত্র গ্রহণের সময় জন্ম তথ্য বাংলা ও ইংরেজি উভয় ভাষায় পূরণ করা হয়েছে কিনা তা নিশ্চিত করতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q08`
2. `birth_and_death_registration_fees_cleaned_fee_row_06`
3. `birth_and_death_registration_fees_cleaned_fee_row_07`
4. `bdris_faq_01_q04`
5. `birth_registration_application_process_cleaned_013_01`
6. `bdris_faq_02_q02`

## FAQ 9: `bdris_faq_01_q09`

Category: `mobile_number_policy`

### Expected Reference Answer

সাধারণভাবে নিবন্ধনাধীন ব্যক্তি অথবা তার পিতা-মাতা-অভিভাবকের মোবাইল নম্বর ব্যবহার করতে হবে।

### Curated/New Question

জন্ম নিবন্ধন বা তথ্য সংশোধনের আবেদনের সময় নিবন্ধনাধীন ব্যক্তি বা তার পিতা-মাতা-অভিভাবক ছাড়া অন্য কারও মোবাইল নম্বর ব্যবহার করা যাবে কি?

Judgement: **Good / Needs ranking improvement**

Interpretation: Expected evidence is retrieved in top-5, but not always as the first result.

Expected source rank: `2`

Top retrieved source: `bdris_faq_02_q07`

Top answer semantic similarity: `0.8247`

Token F1 against reference: `0.3396`

Retrieved answer/evidence used for comparison:

ব্যক্তিগত তথ্যের সুরক্ষায় নিবন্ধনাধীন ব্যক্তি বা তার পিতামাতা-অভিভাবকের মোবাইল নম্বর ব্যবহার করতে হবে। একটি নম্বর সর্বোচ্চ ৫ জন পরিবার সদস্যের জন্য ব্যবহার করা যাবে। ৫-এর বেশি নিবন্ধনে একই নম্বর ব্যবহার করলে সেসব নিবন্ধন পরবর্তীতে খুঁজে পাওয়া যাবে না।

Top retrieved / selected candidates:

1. `bdris_faq_02_q07`
2. `bdris_faq_01_q09`
3. `application_for_birth_information_correction_cleaned_006_01`
4. `application_for_birth_information_correction_cleaned_008_01`
5. `application_for_birth_information_correction_cleaned_005_01`
6. `bdris_faq_01_q16`

### Original/Alternate Question

জন্ম-মৃত্যু নিবন্ধন বা তথ্য সংশোধনের আবেদনের সময় নিবন্ধনাধীন ব্যক্তি বা তার পিতা-মাতা-অভিভাবক ছাড়া অন্য কারও মোবাইল নম্বর ব্যবহার করা যাবে কি?

Judgement: **Good / Needs ranking improvement**

Interpretation: Expected evidence is retrieved in top-5, but not always as the first result.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q09`

Top answer semantic similarity: `0.8060`

Token F1 against reference: `0.2093`

Retrieved answer/evidence used for comparison:

ব্যক্তিগত তথ্যের সুরক্ষায় নিবন্ধনাধীন ব্যক্তি বা তার পিতামাতা-অভিভাবকের মোবাইল নম্বর ব্যবহার করতে হবে। একটি মোবাইল নম্বর সর্বোচ্চ ৫ জন পরিবার সদস্যের জন্য ব্যবহার করা যাবে। ৫-এর বেশি নিবন্ধনে একই নম্বর ব্যবহার করলে সেসব নিবন্ধন পরবর্তীতে খুঁজে পাওয়া যাবে না।

পরিবারে মোবাইল না থাকলে বা সদস্য সংখ্যা বেশি হলে নিবন্ধনাধীন ব্যক্তির সম্মতিতে নিকটজনের নম্বর ব্যবহার করা যাবে। তবে কোনো অবস্থায়ই নিবন্ধন কার্যালয়ের কোনো কর্মকর্তা বা কর্মচারীর ফোন নম্বর ব্যবহার করা যাবে না।

Top retrieved / selected candidates:

1. `bdris_faq_01_q09`
2. `bdris_faq_02_q07`
3. `application_for_birth_information_correction_cleaned_008_01`
4. `application_for_birth_information_correction_cleaned_006_01`
5. `bdris_faq_01_q16`
6. `application_for_birth_information_correction_cleaned_005_01`

## FAQ 10: `bdris_faq_01_q10`

Category: `special_cases`

### Expected Reference Answer

এই ক্ষেত্রে পিতা-মাতার একজনের পূর্ণ তথ্য দিয়ে এবং অপরজনের শুধুমাত্র নাম উল্লেখ করে সন্তানের জন্ম নিবন্ধন করা যাবে।

### Curated/New Question

বিবাহ বিচ্ছেদ বা পিতা-মাতার একজন নিখোঁজ হলে সন্তানের জন্ম নিবন্ধন কীভাবে হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q10`

Top answer semantic similarity: `0.9592`

Token F1 against reference: `0.7778`

Retrieved answer/evidence used for comparison:

এইরূপ ক্ষেত্রে পিতামাতার একজনের তথ্য দিয়ে এবং অপরজনের শুধু নাম উল্লেখ করে সন্তানের জন্ম নিবন্ধন করা যাবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q10`
2. `bdris_faq_02_q08`
3. `bdris_faq_02_q09`
4. `bdris_faq_01_q11`
5. `bdris_faq_01_q01`
6. `application_for_birth_information_correction_cleaned_005_01`

### Original/Alternate Question

বিবিবাহ বিচ্ছেদ বা পিতা-মাতার একজন অপ্রাপ্য/নিখোঁজ হলে সন্তানের জন্ম নিবন্ধন কীভাবে হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q10`

Top answer semantic similarity: `0.9592`

Token F1 against reference: `0.7778`

Retrieved answer/evidence used for comparison:

এইরূপ ক্ষেত্রে পিতামাতার একজনের তথ্য দিয়ে এবং অপরজনের শুধু নাম উল্লেখ করে সন্তানের জন্ম নিবন্ধন করা যাবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q10`
2. `bdris_faq_02_q08`
3. `bdris_faq_02_q09`
4. `bdris_faq_01_q11`
5. `bdris_faq_01_q01`
6. `birth_and_death_registration_rules_2018_বিধি_৩_01`

## FAQ 11: `bdris_faq_01_q11`

Category: `special_cases`

### Expected Reference Answer

মাতা অথবা পিতার একজন বিদেশি হলে বাংলাদেশি অভিভাবকের স্থায়ী ঠিকানার প্রয়োজনীয় দলিলাদি নিয়ে নিবন্ধন কার্যালয়ে যোগাযোগ করতে হবে। নিবন্ধক প্রয়োজনীয় অনুসন্ধান শেষে ঊর্ধ্বতন কর্তৃপক্ষের অনুমোদনক্রমে নিবন্ধন সম্পন্ন করবেন।

### Curated/New Question

পিতা অথবা মাতা যে কোনো একজন বিদেশি হলে সন্তানের জন্ম নিবন্ধন কীভাবে করা হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q11`

Top answer semantic similarity: `0.8647`

Token F1 against reference: `0.6800`

Retrieved answer/evidence used for comparison:

যিনি বাংলাদেশী তার স্থায়ী ঠিকানার প্রয়োজনীয় দলিলাদি নিয়ে নিবন্ধন অফিসে যোগাযোগ করতে হবে। নিবন্ধক প্রয়োজনীয় অনুসন্ধান শেষে ঊর্ধ্বতন কর্তৃপক্ষের অনুমতিক্রমে নিবন্ধন করবেন।

Top retrieved / selected candidates:

1. `bdris_faq_01_q11`
2. `bdris_faq_02_q09`
3. `bdris_faq_01_q10`
4. `bdris_faq_02_q08`
5. `birth_and_death_registration_rules_2018_বিধি_১০_01`
6. `notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01`

### Original/Alternate Question

পিতা-মাতার যে কোনো একজন বিদেশি হলে সন্তানের জন্ম নিবন্ধন কীভাবে করা হবে?

Judgement: **Strong**

Interpretation: Expected evidence is top-ranked and the retrieved answer is semantically close to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q11`

Top answer semantic similarity: `0.8647`

Token F1 against reference: `0.6800`

Retrieved answer/evidence used for comparison:

যিনি বাংলাদেশী তার স্থায়ী ঠিকানার প্রয়োজনীয় দলিলাদি নিয়ে নিবন্ধন অফিসে যোগাযোগ করতে হবে। নিবন্ধক প্রয়োজনীয় অনুসন্ধান শেষে ঊর্ধ্বতন কর্তৃপক্ষের অনুমতিক্রমে নিবন্ধন করবেন।

Top retrieved / selected candidates:

1. `bdris_faq_01_q11`
2. `bdris_faq_02_q09`
3. `bdris_faq_01_q10`
4. `bdris_faq_02_q08`
5. `birth_registration_application_process_cleaned_012_01`
6. `bdris_faq_01_q01`

## FAQ 12: `bdris_faq_01_q13`

Category: `fee_and_challan`

Source-label audit: provided `bdris_faq_01_q12` was corrected to `bdris_faq_01_q13` for this evaluation.

### Expected Reference Answer

ফাইলের আকার ১০২৪ কিলোবাইট বা তার কম রাখতে হবে এবং চালানের অর্থ ব্যালেন্সের সমান অথবা কম হতে হবে।

### Curated/New Question

জন্ম নিবন্ধনের ফি বাবদ চালানের তথ্য BDRIS-এ আপলোড করতে সমস্যা হলে করনীয় কী?

Judgement: **Partial**

Interpretation: Expected evidence is present, but the top answer is not close enough to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q13`

Top answer semantic similarity: `0.7068`

Token F1 against reference: `0.2136`

Retrieved answer/evidence used for comparison:

বিধি ২১(৬) অনুযায়ী প্রতি মাসে আদায়কৃত অর্থ পরবর্তী মাসের ৭ তারিখের মধ্যে সরকারি তহবিলে জমা বাধ্যতামূলক।

চালান আপলোড না হওয়ার দুটি কারণ হতে পারে:
(ক) সংযুক্ত ফাইলের পরিমাণ ১০২৪ কিলোবাইটের বেশি হওয়া — প্রতিটি ফাইল সর্বোচ্চ ১০২৪ কিলোবাইট হতে হবে।
(খ) চালানের টাকা ব্যালান্সের চেয়ে বেশি হওয়া — চালানের পরিমাণ সর্বদা ব্যালান্সের সমান বা কম হতে হবে।

বদলি বা অন্য কারণে 'অথরাইজড ইউজার' রিলিজ করতে হলে বিধি ২১(১) অনুযায়ী সমুদয় টাকা চালানে জমা দিয়ে ব্যালান্স শূন্য করার পর জেলা/উপজেলা অ্যাডমিনের মাধ্যমে রিলিজ করতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q13`
2. `birth_and_death_registration_fees_cleaned_fee_row_05`
3. `bdris_faq_01_q03`
4. `birth_and_death_registration_fees_cleaned_fee_row_04`
5. `home_registrar_generals_office_birth_and_death_registration_002_01`
6. `birth_and_death_registration_fees_cleaned_fee_row_01`

### Original/Alternate Question

জন্ম নিবন্ধনের ফি বাবদ চালানের তথ্য BDRIS-এ আপলোড করতে সমস্যা হলে করনীয় কী?

Judgement: **Partial**

Interpretation: Expected evidence is present, but the top answer is not close enough to the reference.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q13`

Top answer semantic similarity: `0.7068`

Token F1 against reference: `0.2136`

Retrieved answer/evidence used for comparison:

বিধি ২১(৬) অনুযায়ী প্রতি মাসে আদায়কৃত অর্থ পরবর্তী মাসের ৭ তারিখের মধ্যে সরকারি তহবিলে জমা বাধ্যতামূলক।

চালান আপলোড না হওয়ার দুটি কারণ হতে পারে:
(ক) সংযুক্ত ফাইলের পরিমাণ ১০২৪ কিলোবাইটের বেশি হওয়া — প্রতিটি ফাইল সর্বোচ্চ ১০২৪ কিলোবাইট হতে হবে।
(খ) চালানের টাকা ব্যালান্সের চেয়ে বেশি হওয়া — চালানের পরিমাণ সর্বদা ব্যালান্সের সমান বা কম হতে হবে।

বদলি বা অন্য কারণে 'অথরাইজড ইউজার' রিলিজ করতে হলে বিধি ২১(১) অনুযায়ী সমুদয় টাকা চালানে জমা দিয়ে ব্যালান্স শূন্য করার পর জেলা/উপজেলা অ্যাডমিনের মাধ্যমে রিলিজ করতে হবে।

Top retrieved / selected candidates:

1. `bdris_faq_01_q13`
2. `birth_and_death_registration_fees_cleaned_fee_row_05`
3. `bdris_faq_01_q03`
4. `birth_and_death_registration_fees_cleaned_fee_row_04`
5. `home_registrar_generals_office_birth_and_death_registration_002_01`
6. `birth_and_death_registration_fees_cleaned_fee_row_01`

## FAQ 13: `bdris_faq_01_q15`

Category: `duplicate_registration`

Source-label audit: provided `bdris_faq_01_q13` was corrected to `bdris_faq_01_q15` for this evaluation.

### Expected Reference Answer

এই ক্ষেত্রে তদন্ত করে একজনকে পুরোনো নম্বর এবং অপরজনকে নতুন নম্বর প্রদান করা যেতে পারে। সমঝোতা না হলে যার নিবন্ধন আগে হয়েছে, তিনি পুরোনো নম্বর রাখবেন। অন্য ব্যক্তিকে নতুন নম্বর (Reset) প্রদান করতে হবে।

### Curated/New Question

একই জন্ম নিবন্ধন নম্বরে একাধিক ব্যক্তির নিবন্ধন দেখালে করণীয় কী?

Judgement: **Good / Needs ranking improvement**

Interpretation: Expected evidence is retrieved in top-5, but not always as the first result.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q15`

Top answer semantic similarity: `0.8115`

Token F1 against reference: `0.3511`

Retrieved answer/evidence used for comparison:

অনলাইন নিবন্ধনের প্রথম দিকে অসাবধানতায় একই নম্বর একাধিক ব্যক্তির জন্য ব্যবহার হয়ে থাকতে পারে। সমাধান:

(১) সংশ্লিষ্ট সকলকে নিবন্ধন অফিসে এনে সম্মতির ভিত্তিতে একজনকে পুরোনো নম্বর এবং অপরজনকে নতুন নম্বর দেওয়া যাবে।
(২) সমঝোতা না হলে যার নিবন্ধন আগে হয়েছে তার নম্বর বহাল রাখতে হবে এবং অপরজনকে নতুন নম্বর (reset) দিতে হবে।
(৩) অপর ব্যক্তি হাজির না হলে উপস্থিত ব্যক্তিকে নতুন নম্বর দেওয়া যাবে।
(৪) তদন্তে অপর ব্যক্তি অস্তিত্বহীন প্রমাণিত হলে সেই নিবন্ধন বাতিল করতে হবে।

এই অপশনটি BDRIS-এর "জন্মতথ্য" মডিউলের "জন্ম নিবন্ধন বিষয় সঠিক করুন" অপশনে পাওয়া যাবে। শুধুমাত্র 'অথরাইজড ইউজার' এই অপশন দেখতে পাবেন।

Top retrieved / selected candidates:

1. `bdris_faq_01_q15`
2. `know_this_01_cleaned_007_01`
3. `bdris_faq_01_q14`
4. `bdris_faq_01_q02`
5. `notice_birth_and_death_registration_certificate_correction_steps_ocr_003_01`
6. `birth_and_death_registration_act_2004_ধারা_৪_01`

### Original/Alternate Question

একই জন্ম নিবন্ধন নম্বরে একাধিক ব্যক্তিকে দেখালে করণীয় কী?

Judgement: **Good / Needs ranking improvement**

Interpretation: Expected evidence is retrieved in top-5, but not always as the first result.

Expected source rank: `1`

Top retrieved source: `bdris_faq_01_q15`

Top answer semantic similarity: `0.8115`

Token F1 against reference: `0.3511`

Retrieved answer/evidence used for comparison:

অনলাইন নিবন্ধনের প্রথম দিকে অসাবধানতায় একই নম্বর একাধিক ব্যক্তির জন্য ব্যবহার হয়ে থাকতে পারে। সমাধান:

(১) সংশ্লিষ্ট সকলকে নিবন্ধন অফিসে এনে সম্মতির ভিত্তিতে একজনকে পুরোনো নম্বর এবং অপরজনকে নতুন নম্বর দেওয়া যাবে।
(২) সমঝোতা না হলে যার নিবন্ধন আগে হয়েছে তার নম্বর বহাল রাখতে হবে এবং অপরজনকে নতুন নম্বর (reset) দিতে হবে।
(৩) অপর ব্যক্তি হাজির না হলে উপস্থিত ব্যক্তিকে নতুন নম্বর দেওয়া যাবে।
(৪) তদন্তে অপর ব্যক্তি অস্তিত্বহীন প্রমাণিত হলে সেই নিবন্ধন বাতিল করতে হবে।

এই অপশনটি BDRIS-এর "জন্মতথ্য" মডিউলের "জন্ম নিবন্ধন বিষয় সঠিক করুন" অপশনে পাওয়া যাবে। শুধুমাত্র 'অথরাইজড ইউজার' এই অপশন দেখতে পাবেন।

Top retrieved / selected candidates:

1. `bdris_faq_01_q15`
2. `know_this_01_cleaned_007_01`
3. `bdris_faq_01_q14`
4. `bdris_faq_02_q10`
5. `bdris_faq_01_q02`
6. `birth_and_death_registration_act_2004_ধারা_৪_01`

## How To Read This For Thesis Demo

- If `Expected source rank = 1`, the system directly found the expected official evidence.
- If the expected source is in top-5 but not top-1, generation can still be grounded, but reranking/intent boosting may be improved.
- If the answer semantic similarity is high but token F1 is moderate, the meaning is close but wording differs; this is normal for Bangla paraphrases.
- If a dataset source label is wrong, retrieval may look bad even when the system retrieved the correct answer. This is why dataset audit is part of the evaluation pipeline.
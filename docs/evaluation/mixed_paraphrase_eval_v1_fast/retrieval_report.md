# Mixed Paraphrase Evaluation Fast Retrieval Check

Total flat questions: 58

## Summary

| Method | Hit@1 | Hit@3 | Hit@5 | MRR | nDCG@5 | Context Precision@5 |
|---|---:|---:|---:|---:|---:|---:|
| bm25_only | 0.5345 | 0.6897 | 0.7586 | 0.6132 | 0.6112 | 0.1793 |
| dense_only | 0.7931 | 0.9828 | 0.9828 | 0.8707 | 0.8693 | 0.2483 |
| hybrid_rrf | 0.7414 | 0.8793 | 0.9483 | 0.8193 | 0.8108 | 0.2414 |

## Hybrid RRF Misses

| ID | Category | Source type | Expected | Retrieved | Question |
|---|---|---|---|---|---|
| `para_lost_certificate_01_v01` | lost_certificate | legal_rules | `birth_and_death_registration_rules_2018_বিধি_১৩_01` | `bdris_faq_01_q02;application_for_birth_information_correction_cleaned_003_01;application_for_birth_information_correction_cleaned_013_01;bdris_faq_01_q01;application_for_birth_information_correction_cleaned_004_01` | জন্ম নিবন্ধন হারালে কী করব? |
| `para_lost_certificate_01_v02` | lost_certificate | legal_rules | `birth_and_death_registration_rules_2018_বিধি_১৩_01` | `notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01;birth_registration_application_process_cleaned_009_01;know_this_01_cleaned_006_01;birth_registration_application_process_cleaned_008_01;bdris_faq_02_q08` | আমার জন্মসনদ হারিয়ে গেছে, নতুন কপি পেতে হলে কোথায় যেতে হবে? |
| `para_registration_deadline_fee_01_v02` | fees | fee_row | `birth_and_death_registration_fees_cleaned_fee_row_01` | `bdris_faq_01_q01;birth_and_death_registration_fees_cleaned_table_full;birth_and_death_registration_fees_cleaned_fee_row_07;birth_and_death_registration_act_2004_ধারা_২১_01;bdris_faq_01_q13` | বাচ্চার জন্মের এক মাসের মধ্যে জন্মসনদ করতে চাই, টাকা লাগবে কি? |
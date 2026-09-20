# Manual audit answers

These are raw chatbot outputs. Expected-evidence-present checks only a predefined hint and is not an answer-correctness score.

## birth_deadline_direct (birth_death_registration / birth_deadline / direct)

Question: শিশুর জন্মের কত দিনের মধ্যে জন্ম নিবন্ধনের তথ্য দিতে হয়?

Model: qwen2.5:7b; route: controlled; time: 20.54 s; expected evidence present: True.

Answer:

জন্মের ৪৫ দিনের মধ্যে জন্ম সংক্রান্ত তথ্য নিবন্ধকের নিকট প্রদান করতে হবে।

প্রাসঙ্গিক বিধি/আইন: (১) শিশুর পিতা বা মাতা বা অভিভাবক বা নির্ধারিত ব্যক্তি উক্ত শিশুর জন্মের ৪৫ (পঁয়তাল্লিশ) দিনের মধ্যে জন্ম সংক্রান্ত তথ্য নিবন্ধকের নিকট প্রদানের জন্য বাধ্য থাকিবেন।

(২) মৃত ব্যক্তির পুত্র বা কন্যা বা অভিভাবক বা নির্ধারিত ব্যক্তি মৃত্যুর ৪৫ (পঁয়তাল্লিশ) দিনের মধ্যে মৃত্যু সংক্রান্ত তথ্য নিবন্ধকের নিকট প্রদানের জন্য বাধ্য থাকিবেন।

Sources: birth_and_death_registration_act_2004_ধারা_৮_01, birth_and_death_registration_rules_2018_বিধি_৮_01, birth_and_death_registration_rules_2018_বিধি_২০_01

Retrieved sources:
- birth_and_death_registration_act_2004_ধারা_৮_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৮_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- birth_and_death_registration_act_2004_ধারা_১০_01: unknown source
- bdris_faq_02_q01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source

## birth_deadline_paraphrase (birth_death_registration / birth_deadline / paraphrase)

Question: বাচ্চা জন্মের পরে জন্মসনদের তথ্য জমা দেওয়ার সময়সীমা কত?

Model: qwen2.5:7b; route: llm; time: 125.51 s; expected evidence present: True.

Answer:

শিশুর পিতা বা মাতা বা অভিভাবক বা নির্ধারিত ব্যক্তি উক্ত শিশুর জন্মের 45 (পঁয়তাল্লিশ) দিনের মধ্যে জন্মসনদের তথ্য জমা দেওয়ার সময়সীমা হল 45 (পঁয়তাল্লিশ) দিন।

Sources: birth_and_death_registration_act_2004_ধারা_৮_01, birth_and_death_registration_rules_2018_বিধি_৯_02, birth_and_death_registration_rules_2018_বিধি_২০_01

Retrieved sources:
- birth_and_death_registration_act_2004_ধারা_৮_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৮_01: unknown source
- bdris_faq_02_q01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১৮_01: unknown source

## birth_deadline_scenario (birth_death_registration / birth_deadline / scenario)

Question: আমার শিশুর জন্ম হয়েছে ৩০ দিন আগে। জন্ম নিবন্ধনের তথ্য দেওয়ার নির্ধারিত সময় কতদিন?

Model: qwen2.5:7b; route: llm; time: 94.77 s; expected evidence present: True.

Answer:

শিশুর জন্ম হওয়ার 45 (30) দিনের মধ্যে তথ্য প্রদান করতে হবে।

Sources: birth_and_death_registration_act_2004_ধারা_৮_01, birth_and_death_registration_rules_2018_বিধি_৮_01, birth_and_death_registration_rules_2018_বিধি_২০_01

Retrieved sources:
- birth_and_death_registration_act_2004_ধারা_৮_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৮_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source
- bdris_faq_02_q01: unknown source
- birth_and_death_registration_act_2004_ধারা_১৫_01: unknown source

## birth_deadline_code_mixed (birth_death_registration / birth_deadline / code_mixed)

Question: baby birth er por birth registration information kotodin er moddhe dite hoy?

Model: qwen2.5:7b; route: llm; time: 47.36 s; expected evidence present: False.

Answer:

The birth registration information must be provided within a day after the baby's birth. You need to provide:

- Baby’s name in Bangla and English
- Date of birth
- Gender
- Order of birth
- Place of birth address

These details should be accurately entered as per the records from your parents' online birth registrations if available. After entering this information, click on the "Verify" button.

Sources: birth_registration_application_process_02_cleaned_006_01, know_this_01_cleaned_003_01, birth_registration_application_process_cleaned_012_01

Retrieved sources:
- birth_registration_application_process_02_cleaned_006_01: unknown source
- know_this_01_cleaned_003_01: unknown source
- birth_registration_application_process_cleaned_012_01: unknown source
- application_for_birth_information_correction_cleaned_008_01: unknown source
- application_for_birth_information_correction_cleaned_006_01: unknown source
- application_for_birth_information_correction_cleaned_005_01: unknown source

## birth_lost_direct (birth_death_registration / lost_certificate / direct)

Question: জন্ম নিবন্ধনের মূল সনদ হারিয়ে গেলে কী করতে হবে?

Model: qwen2.5:7b; route: controlled; time: 23.28 s; expected evidence present: True.

Answer:

জন্ম নিবন্ধন সনদ হারিয়ে গেলে বা নষ্ট হলে নিবন্ধকের কাছে সনদের প্রতিলিপির জন্য আবেদন করতে হবে। বিধি ১৩ অনুযায়ী, আবেদন পাওয়ার ৭ কার্য দিবসের মধ্যে জন্ম/মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করা হয়। প্রতিলিপির জন্য বিধি ২১ অনুযায়ী নির্ধারিত ফি প্রযোজ্য হতে পারে।

প্রাসঙ্গিক বিধি: (১) নিবন্ধিত কোন ব্যক্তির সনদ হারাইয়া গেলে বা নষ্ট হইলে, নিবন্ধক, উপ-বিধি (২) ও (৩) এর বিধান সাপেক্ষে, জমনি ফরম-৭ অনুযায়ী উক্ত ব্যক্তির আবেদন প্রাপ্তির ৭ (সাত) কার্য দিবসের মধ্যে জমনি ফরম-৩ ও জমনি ফরম-৬ অনুযায়ী জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করিবেন। (২) বিধি ২১ এ নির্ধারিত ফিস প্রদান সাপেক্ষে, নিম্নবর্ণিত কোন ব্যক্তি জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপির জন্য জমনি ফরম-৭ অনুযায়ী নিবন্ধকের নিকট আবেদন করিতে পারিবেন, যথা:
(ক) যাহার জন্য জন্ম সনদ প্রদান করা হইবে তাহার বয়স ১৮ (আঠার) বৎসর বা তদূর্ধ্ব হইলে তিনি স্বয়ং অথবা (খ) জন্ম তথ্য প্রদানকারী অথবা (গ) মৃত্যু তথ্য প্রদানকারী অথবা (ঘ) জন্ম বা মৃত্যু তথ্য দ্বারা সংক্ষুব্ধ ব্যক্তি। (৩) উপ-বিধি (২) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক যদি নিশ্চিত হন যে, উক্ত আবেদনপত্র যথাযথভাবে পূরণ করা হইয়াছে এবং ফিস প্রদান করা হইয়াছে তাহা হইলে তিনি আবেদনকারীর অংশ স্বাক্ষরপূর্বক উহা আবেদনকারীর নিকট হস্তান্তর করিবেন। (৪) উপ-বিধি (৩) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক সনদের প্রতিলিপি প্রস্তুত করিবেন এবং আবেদনকারীর অংশ গ্রহণ করিয়া সনদের প্রতিলিপি আবেদনকারীর নিকট হস্তান্তরের ব্যবস্থা করিবেন। (৫) প্রতিলিপি সনদের উপরিভাগে প্রতিলিপি বা উঁঢ়ষরপধঃব শব্দটি এবং, ক্ষেত্রমত, সংশোধিত সনদের ক্ষেত্রে সংশোধিত শব্দটি উল্লেখ থাকিবে এবং প্রথম বার জন্ম বা মৃত্যু নিবন্ধন সনদ যে তারিখে ইস্যু হইয়াছে প্রতিলিপি সনদ ইস্যুর সেই তারিখ বহাল থাকিবে ও প্রতিলিপি সনদ ইস্যুর তারিখ লিপিবদ্ধ করিতে হইবে।

Sources: birth_and_death_registration_rules_2018_বিধি_১৩_01

Retrieved sources:
- birth_and_death_registration_rules_2018_বিধি_১৩_01: unknown source
- bdris_faq_01_q12: unknown source
- birth_and_death_registration_rules_2018_বিধি_১৫_01: unknown source
- birth_and_death_registration_act_2004_ধারা_১৫_01: unknown source
- birth_registration_application_process_cleaned_020_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১২_02: unknown source

## birth_lost_paraphrase (birth_death_registration / lost_certificate / paraphrase)

Question: জন্মসনদ খুঁজে পাচ্ছি না। নতুন কপি কোথা থেকে পাব?

Model: qwen2.5:7b; route: controlled; time: 21.24 s; expected evidence present: True.

Answer:

জন্ম নিবন্ধন সনদ হারিয়ে গেলে বা নষ্ট হলে নিবন্ধকের কাছে সনদের প্রতিলিপির জন্য আবেদন করতে হবে। বিধি ১৩ অনুযায়ী, আবেদন পাওয়ার ৭ কার্য দিবসের মধ্যে জন্ম/মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করা হয়। প্রতিলিপির জন্য বিধি ২১ অনুযায়ী নির্ধারিত ফি প্রযোজ্য হতে পারে।

প্রাসঙ্গিক বিধি: (১) নিবন্ধিত কোন ব্যক্তির সনদ হারাইয়া গেলে বা নষ্ট হইলে, নিবন্ধক, উপ-বিধি (২) ও (৩) এর বিধান সাপেক্ষে, জমনি ফরম-৭ অনুযায়ী উক্ত ব্যক্তির আবেদন প্রাপ্তির ৭ (সাত) কার্য দিবসের মধ্যে জমনি ফরম-৩ ও জমনি ফরম-৬ অনুযায়ী জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করিবেন। (২) বিধি ২১ এ নির্ধারিত ফিস প্রদান সাপেক্ষে, নিম্নবর্ণিত কোন ব্যক্তি জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপির জন্য জমনি ফরম-৭ অনুযায়ী নিবন্ধকের নিকট আবেদন করিতে পারিবেন, যথা:
(ক) যাহার জন্য জন্ম সনদ প্রদান করা হইবে তাহার বয়স ১৮ (আঠার) বৎসর বা তদূর্ধ্ব হইলে তিনি স্বয়ং অথবা (খ) জন্ম তথ্য প্রদানকারী অথবা (গ) মৃত্যু তথ্য প্রদানকারী অথবা (ঘ) জন্ম বা মৃত্যু তথ্য দ্বারা সংক্ষুব্ধ ব্যক্তি। (৩) উপ-বিধি (২) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক যদি নিশ্চিত হন যে, উক্ত আবেদনপত্র যথাযথভাবে পূরণ করা হইয়াছে এবং ফিস প্রদান করা হইয়াছে তাহা হইলে তিনি আবেদনকারীর অংশ স্বাক্ষরপূর্বক উহা আবেদনকারীর নিকট হস্তান্তর করিবেন। (৪) উপ-বিধি (৩) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক সনদের প্রতিলিপি প্রস্তুত করিবেন এবং আবেদনকারীর অংশ গ্রহণ করিয়া সনদের প্রতিলিপি আবেদনকারীর নিকট হস্তান্তরের ব্যবস্থা করিবেন। (৫) প্রতিলিপি সনদের উপরিভাগে প্রতিলিপি বা উঁঢ়ষরপধঃব শব্দটি এবং, ক্ষেত্রমত, সংশোধিত সনদের ক্ষেত্রে সংশোধিত শব্দটি উল্লেখ থাকিবে এবং প্রথম বার জন্ম বা মৃত্যু নিবন্ধন সনদ যে তারিখে ইস্যু হইয়াছে প্রতিলিপি সনদ ইস্যুর সেই তারিখ বহাল থাকিবে ও প্রতিলিপি সনদ ইস্যুর তারিখ লিপিবদ্ধ করিতে হইবে।

Sources: birth_and_death_registration_rules_2018_বিধি_১৩_01

Retrieved sources:
- birth_and_death_registration_rules_2018_বিধি_১৩_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১২_01: unknown source
- birth_registration_application_process_cleaned_009_01: unknown source
- bdris_faq_01_q12: unknown source
- birth_and_death_registration_rules_2018_বিধি_১০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source

## birth_lost_scenario (birth_death_registration / lost_certificate / scenario)

Question: ভর্তি করানোর সময় আমার ছেলের জন্ম নিবন্ধনের কাগজ হারিয়ে গেছে। আবার কপি পাওয়ার জন্য কী করব?

Model: qwen2.5:7b; route: controlled; time: 22.32 s; expected evidence present: True.

Answer:

জন্ম নিবন্ধন সনদ হারিয়ে গেলে বা নষ্ট হলে নিবন্ধকের কাছে সনদের প্রতিলিপির জন্য আবেদন করতে হবে। বিধি ১৩ অনুযায়ী, আবেদন পাওয়ার ৭ কার্য দিবসের মধ্যে জন্ম/মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করা হয়। প্রতিলিপির জন্য বিধি ২১ অনুযায়ী নির্ধারিত ফি প্রযোজ্য হতে পারে।

প্রাসঙ্গিক বিধি: (১) নিবন্ধিত কোন ব্যক্তির সনদ হারাইয়া গেলে বা নষ্ট হইলে, নিবন্ধক, উপ-বিধি (২) ও (৩) এর বিধান সাপেক্ষে, জমনি ফরম-৭ অনুযায়ী উক্ত ব্যক্তির আবেদন প্রাপ্তির ৭ (সাত) কার্য দিবসের মধ্যে জমনি ফরম-৩ ও জমনি ফরম-৬ অনুযায়ী জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করিবেন। (২) বিধি ২১ এ নির্ধারিত ফিস প্রদান সাপেক্ষে, নিম্নবর্ণিত কোন ব্যক্তি জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপির জন্য জমনি ফরম-৭ অনুযায়ী নিবন্ধকের নিকট আবেদন করিতে পারিবেন, যথা:
(ক) যাহার জন্য জন্ম সনদ প্রদান করা হইবে তাহার বয়স ১৮ (আঠার) বৎসর বা তদূর্ধ্ব হইলে তিনি স্বয়ং অথবা (খ) জন্ম তথ্য প্রদানকারী অথবা (গ) মৃত্যু তথ্য প্রদানকারী অথবা (ঘ) জন্ম বা মৃত্যু তথ্য দ্বারা সংক্ষুব্ধ ব্যক্তি। (৩) উপ-বিধি (২) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক যদি নিশ্চিত হন যে, উক্ত আবেদনপত্র যথাযথভাবে পূরণ করা হইয়াছে এবং ফিস প্রদান করা হইয়াছে তাহা হইলে তিনি আবেদনকারীর অংশ স্বাক্ষরপূর্বক উহা আবেদনকারীর নিকট হস্তান্তর করিবেন। (৪) উপ-বিধি (৩) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক সনদের প্রতিলিপি প্রস্তুত করিবেন এবং আবেদনকারীর অংশ গ্রহণ করিয়া সনদের প্রতিলিপি আবেদনকারীর নিকট হস্তান্তরের ব্যবস্থা করিবেন। (৫) প্রতিলিপি সনদের উপরিভাগে প্রতিলিপি বা উঁঢ়ষরপধঃব শব্দটি এবং, ক্ষেত্রমত, সংশোধিত সনদের ক্ষেত্রে সংশোধিত শব্দটি উল্লেখ থাকিবে এবং প্রথম বার জন্ম বা মৃত্যু নিবন্ধন সনদ যে তারিখে ইস্যু হইয়াছে প্রতিলিপি সনদ ইস্যুর সেই তারিখ বহাল থাকিবে ও প্রতিলিপি সনদ ইস্যুর তারিখ লিপিবদ্ধ করিতে হইবে।

Sources: birth_and_death_registration_rules_2018_বিধি_১৩_01

Retrieved sources:
- birth_and_death_registration_rules_2018_বিধি_১৩_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১০_01: unknown source
- bdris_faq_01_q01: unknown source
- birth_registration_application_process_02_cleaned_014_01: unknown source
- birth_registration_application_process_cleaned_009_01: unknown source
- birth_registration_application_process_cleaned_010_01: unknown source

## birth_lost_code_mixed (birth_death_registration / lost_certificate / code_mixed)

Question: birth certificate lost hoye geche, duplicate copy kivabe nibo?

Model: qwen2.5:7b; route: llm; time: 89.58 s; expected evidence present: True.

Answer:

Steps to obtain a copy of a birth or death registration certificate:

1. If the original document is lost or damaged:
   - Apply within 7 days using Form-3 and Form-6 as per U-form-7 guidelines (Source 2).

2. For individuals aged 18 years or older, their parent(s), guardian(s) or spouse can apply if they have relevant information about the event (Source 3).

3. The registrar will provide the copy upon receipt of an application form completed with required fees (Form-7).

4. Once received, the registrar will send the certified copy to the applicant after verifying it's correct and signed (Sources 2 & 3).

5. On the copy, "Copy" or "Amended" will be noted in appropriate places along with issue date details (Source 3).

Sources: birth_and_death_registration_rules_2018_বিধি_১৫_01, birth_and_death_registration_rules_2018_বিধি_১২_01, birth_and_death_registration_rules_2018_বিধি_১৩_01

Retrieved sources:
- birth_and_death_registration_rules_2018_বিধি_১৫_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১২_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১৩_01: unknown source
- bdris_faq_01_q14: unknown source
- bdris_faq_02_q10: unknown source
- bdris_faq_01_q02: unknown source

## birth_date_correction_direct (birth_death_registration / date_correction / direct)

Question: জন্ম তারিখ ভুল হলে কীভাবে সংশোধন করব এবং ফি কত?

Model: qwen2.5:7b; route: controlled; time: 20.41 s; expected evidence present: True.

Answer:

জন্ম তারিখ সংশোধনের জন্য আবেদন ফি: ১০০ টাকা

Sources: birth_and_death_registration_fees_cleaned_fee_row_04, birth_and_death_registration_fees_cleaned_fee_row_05, birth_and_death_registration_fees_cleaned_table_full

Retrieved sources:
- birth_and_death_registration_fees_cleaned_fee_row_04: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source
- birth_and_death_registration_fees_cleaned_table_full: unknown source
- birth_and_death_registration_rules_2018_বিধি_২১_01: unknown source
- birth_and_death_registration_act_2004_ধারা_১৫_01: unknown source
- notice_birth_and_death_registration_certificate_correction_steps_ocr_006_01: unknown source

## birth_date_correction_paraphrase (birth_death_registration / date_correction / paraphrase)

Question: জন্মসনদে আমার DOB ভুল আছে। ঠিক করার নিয়ম ও খরচ কী?

Model: qwen2.5:7b; route: controlled; time: 20.21 s; expected evidence present: True.

Answer:

জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা ইত্যাদি অন্যান্য তথ্য সংশোধনের জন্য আবেদন ফি: ৫০ টাকা

Sources: birth_and_death_registration_act_2004_ধারা_১৫_01, birth_and_death_registration_fees_cleaned_table_full, birth_and_death_registration_fees_cleaned_fee_row_05

Retrieved sources:
- birth_and_death_registration_act_2004_ধারা_১৫_01: unknown source
- birth_and_death_registration_fees_cleaned_table_full: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_06: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_04: unknown source
- birth_and_death_registration_rules_2018_বিধি_২১_01: unknown source

## birth_date_correction_scenario (birth_death_registration / date_correction / scenario)

Question: স্কুলের কাগজের সঙ্গে জন্ম নিবন্ধনের জন্ম তারিখ মিলছে না। জন্ম নিবন্ধনের তারিখ পরিবর্তনের আবেদন করতে চাই। ফি কত লাগবে?

Model: qwen2.5:7b; route: controlled; time: 19.77 s; expected evidence present: True.

Answer:

জন্ম তারিখ সংশোধনের জন্য আবেদন ফি: ১০০ টাকা

Sources: birth_and_death_registration_fees_cleaned_table_full, birth_and_death_registration_fees_cleaned_fee_row_04, birth_and_death_registration_fees_cleaned_fee_row_05

Retrieved sources:
- birth_and_death_registration_fees_cleaned_table_full: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_04: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source
- birth_and_death_registration_rules_2018_বিধি_২১_01: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_02: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_03: unknown source

## birth_date_correction_code_mixed (birth_death_registration / date_correction / code_mixed)

Question: birth certificate e date of birth wrong, correction fee koto?

Model: qwen2.5:7b; route: llm; time: 58.0 s; expected evidence present: True.

Answer:

The fee to correct a birth date in a birth certificate is 100 Bangladeshi Taka (BDT).

Sources: birth_and_death_registration_fees_cleaned_fee_row_04, birth_and_death_registration_fees_cleaned_table_full, birth_and_death_registration_fees_cleaned_fee_row_05

Retrieved sources:
- birth_and_death_registration_fees_cleaned_fee_row_04: unknown source
- birth_and_death_registration_fees_cleaned_table_full: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source
- birth_and_death_registration_rules_2018_বিধি_২১_01: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_06: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_02: unknown source

## birth_multi_parent_fee (birth_death_registration / multi_condition / multi_condition)

Question: আমার ছেলের জন্ম নিবন্ধনে বাবার নাম ভুল আছে। সঠিক নাম দিতে কীভাবে সংশোধন করব এবং নাম সংশোধনের ফি কত?

Model: qwen2.5:7b; route: controlled; time: 19.47 s; expected evidence present: True.

Answer:

জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা ইত্যাদি অন্যান্য তথ্য সংশোধনের জন্য আবেদন ফি: ৫০ টাকা

Sources: birth_and_death_registration_fees_cleaned_fee_row_05, birth_and_death_registration_fees_cleaned_table_full, application_for_birth_information_correction_cleaned_008_01

Retrieved sources:
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source
- birth_and_death_registration_fees_cleaned_table_full: unknown source
- application_for_birth_information_correction_cleaned_008_01: unknown source
- application_for_birth_information_correction_cleaned_006_01: unknown source
- application_for_birth_information_correction_cleaned_002_01: unknown source
- application_for_birth_information_correction_cleaned_003_01: unknown source

## birth_multi_application_documents (birth_death_registration / multi_condition / multi_condition)

Question: জন্ম নিবন্ধনের আবেদন করতে চাই। কী প্রমাণক লাগবে এবং আবেদন জমা হলে Application ID কোথায় পাব?

Model: qwen2.5:7b; route: controlled; time: 20.05 s; expected evidence present: True.

Answer:

আপনার প্রশ্নে কয়েকটি আলাদা বিষয় আছে। প্রাপ্ত সরকারি/উৎস ডেটার ভিত্তিতে অংশভাগ করে উত্তর দিচ্ছি:

1. আবেদন নম্বর, অগ্রগতি বা পরবর্তী করণীয়
জন্ম নিবন্ধনের আবেদন সফলভাবে সম্পন্ন হওয়ার পর আপনার মোবাইলে অ্যাপ্লিকেশন আইডি SMS হিসেবে যাবে।

"সাবমিট" বাটনে ক্লিক করার পর আবেদন সফলভাবে জমা হয়েছে মর্মে বার্তা প্রদর্শিত হবে।

এখানে একটি আবেদনপত্র নম্বর (Application ID) প্রদান করা হবে।

এই নম্বর:

- মোবাইল নম্বরে
- ইমেইলে

পাঠানো হবে।

নিম্নোক্ত নথিপত্র নিয়ে সংশ্লিষ্ট নিবন্ধন কার্যালয়ে যোগাযোগ করতে হবে:

- আবেদনপত্র
- সংযুক্ত ডকুমেন্টসমূহের ফটোকপি

সংশ্লিষ্ট নিবন্ধন কার্যালয়:

- ইউনিয়ন পরিষদ
- পৌরসভা
- সিটি কর্পোরেশন
- ক্যান্টনমেন্ট

নিবন্ধন সহকারী এবং নিবন্ধক কর্তৃক যাচাই-বাছাই শেষে তথ্য সঠিক পাওয়া গেলে জন্ম নিবন্ধন সনদ প্রদান করা হবে।

এই ডেটাসেটে নির্দিষ্ট আবেদন নম্বর দিয়ে অনলাইন progress/status যাচাই করার আলাদা পদ্ধতি পাওয়া যায়নি। তাই নির্দিষ্ট আবেদন নম্বরের বর্তমান অবস্থা জানতে সংশ্লিষ্ট নিবন্ধন কার্যালয় বা BDRIS নির্দেশনা অনুসরণ করা উচিত।

2. জন্ম নিবন্ধনের আবেদন
আবেদন করার পূর্ব প্রস্তুতি: নতুন জন্ম নিবন্ধন আবেদনের পূর্বে প্রয়োজনীয় তথ্য ও ডকুমেন্ট সংগ্রহ করে রাখুন।

জন্ম নিবন্ধনের ক্ষেত্রে নিম্নোক্ত তিন ধরনের ঠিকানার তথ্য প্রয়োজন হবে:

- জন্মস্থান
- স্থায়ী ঠিকানা
- বর্তমান ঠিকানা

প্রতিটি ঠিকানার জন্য নিম্নোক্ত তথ্য প্রয়োজন হতে পারে:

- ইউনিয়ন পরিষদ/পৌরসভা/সিটি কর্পোরেশন/ক্যান্টনমেন্টের নাম
- ওয়ার্ড নম্বর
- ডাকঘর
- গ্রাম/পাড়া/মহল্লা
- বাসা ও সড়কের নাম ও নম্বর

সকল তথ্য বাংলা ও ইংরেজি উভয় ভাষায় সঠিক বানানে লিখতে হবে।

ধাপ ১: ওয়েবসাইটে প্রবেশ: নতুন জন্ম নিবন্ধনের জন্য:

https://bdris.gov.bd

ওয়েবসাইটে প্রবেশ করুন।

হোমপেজে "জন্ম নিবন্ধন" মেনু নির্বাচন করুন।

এরপর "জন্ম নিবন্ধন আবেদন" অপশনে ক্লিক করুন।

ধাপ ২: সনদ সংগ্রহের স্থান নির্বাচন: এখানে আবেদনকারীকে নির্বাচন করতে হবে তিনি কোথা থেকে জন্ম সনদ গ্রহণ বা সংগ্রহ করতে চান।

নিম্নোক্ত ঠিকানার ভিত্তিতে সনদ সংগ্রহ করা যেতে পারে:

- জন্মস্থান
- স্থায়ী ঠিকানা

সাধারণভাবে স্থায়ী ঠিকানা থেকে সনদ সংগ্রহ করার জন্য উৎসাহিত করা হয়।

বিদেশে জন্মগ্রহণকারী শিশু নিকটস্থ বাংলাদেশ দূতাবাস থেকে জন্ম সনদ সংগ্রহ করতে পারে।

এরপর "পরবর্তী" বাটনে ক্লিক করুন।

ধাপ ৩: জন্ম তথ্য প্রদান: এই ধাপে আবেদনকারীর জন্মসংক্রান্ত তথ্য ধাপে ধাপে পূরণ করতে হবে।

তথ্য প্রদানের সময় সতর্কতা অবলম্বন করতে হবে।

জন্ম তারিখ প্রদান করার পর সিস্টেম প্রয়োজনীয় নির্দেশনা প্রদর্শন করবে।

নির্দেশনা পড়ে "আমার কাছে এই ডকুমেন্টগুলো আছে" অপশন নির্বাচন করতে হবে।

এরপর "পরবর্তী" বাটনে ক্লিক করুন।

ধাপ ৪: পিতা ও মাতার তথ্য প্রদান: এই ধাপে পিতা ও মাতার তথ্য প্রদান করতে হবে।

ধাপ ৫: স্থায়ী ও বর্তমান ঠিকানা প্রদান: এই ধাপে:

- স্থায়ী ঠিকানা
- বর্তমান ঠিকানা

প্রদান করতে হবে।

যদি জন্মস্থান এবং স্থায়ী ঠিকানা একই হয়, তাহলে নির্ধারিত ঘরে টিক চিহ্ন দিলে তথ্য স্বয়ংক্রিয়ভাবে পূরণ হবে।

অন্যথায় স্থায়ী ঠিকানা ও বর্তমান ঠিকানার তথ্য আলাদাভাবে পূরণ করতে হবে।

সব তথ্য সঠিকভাবে পূরণ করার পর "পরবর্তী" বাটনে ক্লিক করুন।

ধাপ ৬: আবেদনকারীর তথ্য ও ডকুমেন্ট সংযুক্তি: যদি ব্যক্তি নিজে আবেদন করেন, তাহলে "নিজ" অপশন নির্বাচন করতে হবে।

অন্য কেউ আবেদন করলে "অন্যান্য" অপশন নির্বাচন করতে হবে।

"অন্যান্য" নির্বাচন করলে আবেদনকারীর জন্ম নিবন্ধন নম্বর প্রদান করতে হবে।

এরপর ঘোষণা দিতে হবে যে:

- প্রদত্ত তথ্যসমূহ সঠিক
- পূর্বে জন্ম নিবন্ধন করা হয়নি

সংযুক্ত করতে হবে: - জন্ম তারিখের প্রমাণক
- জন্মস্থানের প্রমাণক
- স্থায়ী ঠিকানার প্রমাণক

সংযুক্তির জন্য ২ মেগাবাইটের কম আকারের ইমেজ ফাইল ব্যবহার করতে হবে।

এরপর "পরবর্তী" বাটনে ক্লিক করুন।

ধাপ ৭: তথ্য যাচাই ও OTP: এই ধাপে আবেদনকারীর পূরণকৃত সকল তথ্য প্রদর্শিত হবে।

সকল তথ্য সতর্কতার সাথে যাচাই করতে হবে।

ভুল থাকলে "পূর্ববর্তী" বাটনে ফিরে গিয়ে সংশোধন করতে হবে।

তথ্য সঠিক হলে:

- ইমেইল অথবা
- মোবাইল নম্বর

প্রদান করতে হবে।

OTP গ্রহণ: - দূতাবাসের মাধ্যমে আবেদনের ক্ষেত্রে ইমেইলে OTP যাবে।
- বাংলাদেশের অভ্যন্তরে আবেদনের ক্ষেত্রে মোবাইল নম্বরে OTP যাবে।

OTP প্রদান করার পর "সাবমিট" বাটনে ক্লিক করুন।

3. প্রয়োজনীয় কাগজপত্র/প্রমাণক
জন্ম নিবন্ধনের জন্য সাধারণত জন্মস্থান, স্থায়ী ঠিকানা এবং বর্তমান ঠিকানার তথ্য প্রস্তুত রাখতে হয়।

নতুন জন্ম নিবন্ধন আবেদনের পূর্বে প্রয়োজনীয় তথ্য ও ডকুমেন্ট সংগ্রহ করে রাখুন।

জন্ম নিবন্ধনের ক্ষেত্রে নিম্নোক্ত তিন ধরনের ঠিকানার তথ্য প্রয়োজন হবে:

- জন্মস্থান
- স্থায়ী ঠিকানা
- বর্তমান ঠিকানা

প্রতিটি ঠিকানার জন্য নিম্নোক্ত তথ্য প্রয়োজন হতে পারে:

- ইউনিয়ন পরিষদ/পৌরসভা/সিটি কর্পোরেশন/ক্যান্টনমেন্টের নাম
- ওয়ার্ড নম্বর
- ডাকঘর
- গ্রাম/পাড়া/মহল্লা
- বাসা ও সড়কের নাম ও নম্বর

সকল তথ্য বাংলা ও ইংরেজি উভয় ভাষায় সঠিক বানানে লিখতে হবে।

- জন্ম তারিখের প্রমাণক
- জন্মস্থানের প্রমাণক
- স্থায়ী ঠিকানার প্রমাণক

সংযুক্তির জন্য ২ মেগাবাইটের কম আকারের ইমেজ ফাইল ব্যবহার করতে হবে।

এরপর "পরবর্তী" বাটনে ক্লিক করুন।

বিধি ৯ অনুযায়ী প্রাসঙ্গিক প্রমাণের মধ্যে জন্মস্থান ও জন্ম তারিখের প্রমাণ, স্থায়ী ঠিকানার প্রমাণ, এবং প্রযোজ্য ক্ষেত্রে পিতা-মাতার জন্ম নিবন্ধন নম্বর বা জাতীয় পরিচয়পত্রের তথ্য থাকতে পারে।

Sources: birth_registration_application_process_02_cleaned_013_01, birth_registration_application_process_cleaned_019_01, birth_registration_application_process_cleaned_020_01, birth_registration_application_process_02_cleaned_010_01, birth_registration_application_process_cleaned_016_01, birth_and_death_registration_rules_2018_বিধি_৯_02, birth_registration_application_process_cleaned_005_01, birth_registration_application_process_cleaned_008_01

Retrieved sources:
- birth_registration_application_process_02_cleaned_010_01: unknown source
- birth_registration_application_process_cleaned_016_01: unknown source
- birth_registration_application_process_cleaned_019_01: unknown source
- birth_registration_application_process_02_cleaned_013_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source
- birth_registration_application_process_cleaned_005_01: unknown source
- birth_registration_application_process_cleaned_020_01: unknown source
- birth_registration_application_process_cleaned_008_01: unknown source
- birth_registration_application_process_cleaned_002_01: unknown source

## birth_boundary_passport (birth_death_registration / boundary / out_of_domain)

Question: ই-পাসপোর্টের সুপার এক্সপ্রেস ডেলিভারি কত দিনে হয়?

Model: qwen2.5:7b; route: llm_then_evidence_fallback; time: 75.9 s; expected evidence present: None.

Answer:

(১) বিদেশে অবস্থিত বাংলাদেশ দূতাবাসের নিবন্ধক জমনি ফরম-১ অনুযায়ী আবেদনপত্রের সহিত নিম্নবর্ণিত তথ্যাদি প্রাপ্তি সাপেক্ষে তাহার অধিক্ষেত্রে বসবাসকারী বা জন্ম গ্রহণকারী ব্যক্তির জন্ম নিবন্ধন করিবেন, যথা:- (ক) জন্মস্থান ও জন্ম তারিখের প্রমাণ হিসাবে সংশ্লিষ্ট চিকিৎসা প্রতিষ্ঠানের ছাড়পত্র বা উক্ত প্রতিষ্ঠান হইতে প্রাপ্ত জন্ম সংক্রান্ত সনদের অনুলিপি অথবা বার্থ এটেন্ডেন্টের প্রত্যয়ন বা সংশ্লিষ্ট ব্যক্তির মেশিন রিডেবল পাসপোর্টের প্রথম ২ (দুই) পাতার অনুলিপি (খ) পিতা বা মাতার মেশিন রিডেবল পাসপোর্টের প্রথম ০৭ (সাত) পাতার অনুলিপি (গ) পিতা বা মাতা অথবা নিজের পাসপোর্টে বর্ণিত স্থায়ী ঠিকানাই ব্যক্তির স্থায়ী ঠিকানা হিসাবে গণ্য হইবে (ঘ) আবেদনকারী কোন যৌক্তিক কারণে বাংলাদেশী পাসপোর্ট উপস্থাপনে ব্যর্থ হইলে নিবন্ধক কর্তৃক প্রয়োজনবোধে চাহিত স্থায়ী ঠিকানা বা বর্তমান ঠিকানা সংক্রান্ত অন্য কোন কাগজপত্রাদির অনুলিপি এবং (ঙ) পূর্বে জন্ম নিবন্ধন হয় নাই এই মর্মে আবেদনপত্রে আবেদনকারীর ঘোষণা। (২) আবেদন মুদ্রিত ফরমে বা অনলাইনে যে কোন পদ্ধতিতে করা যাইবে এবং মুদ্রিত ফরমে আবেদন করিলে নিবন্ধক উহা কার্যপ্রণালীতে বর্ণিত পদ্ধতি অনুসারে অনলাইনে এন্ট্রি করিবেন এবং অনলাইন আবেদনপত্রের ক্ষেত্রে, অনলাইনে আবেদন দাখিলের পর আবেদনকারী অনলাইন হইতে মুদ্রিত আবেদনপত্রের কপি নিবন্ধকের নিকট দাখিল করিবেন। (৩) উপ-বিধি (২) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক বা তৎকর্তৃক ক্ষমতাপ্রাপ্ত ব্যক্তি পরবর্তী ৭ (সাত) কার্য দিবসের মধ্যে সনদ প্রদানের তারিখ উল্লেখপূর্বক আবেদনকারীর অংশ স্বাক্ষর করিয়া উহা আবেদনকারীর নিকট হস্তান্তর করিবেন।

Sources: birth_and_death_registration_rules_2018_বিধি_১০_01, birth_and_death_registration_rules_2018_বিধি_৯_02, bdris_faq_01_q01

Retrieved sources:
- birth_and_death_registration_rules_2018_বিধি_১০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source
- bdris_faq_01_q01: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১৩_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১৮_01: unknown source

## brta_age_direct (brta / professional_license_age / direct)

Question: পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স কত?

Model: qwen2.5:7b; route: llm; time: 68.87 s; expected evidence present: True.

Answer:

পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূমতম বয়স ২১ বছর।

Sources: brta_cbe22ab64acf3d03_v2_0007, brta_cbe22ab64acf3d03_v2_0002, brta_846a4041fe96a64e_v2_0002

Retrieved sources:
- brta_cbe22ab64acf3d03_v2_0007: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_cbe22ab64acf3d03_v2_0002: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_846a4041fe96a64e_v2_0002: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_57a7e75567f9a5c3_v2_0007: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_4e08eb4e988d38e4_v2_0017: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_edcb265eccf9cd32_v2_0012: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md

## brta_age_paraphrase (brta / professional_license_age / paraphrase)

Question: প্রফেশনাল গাড়ি চালানোর লাইসেন্স করতে কত বছর বয়স লাগবে?

Model: qwen2.5:7b; route: llm; time: 78.01 s; expected evidence present: True.

Answer:

পেশাদার গাড়ি চালানোর জন্য আवশ্যক নূন্যতম বয়স ২১ বছর।

Sources: brta_cbe22ab64acf3d03_v2_0007, brta_4e08eb4e988d38e4_v2_0195, brta_57a7e75567f9a5c3_v2_0007

Retrieved sources:
- brta_cbe22ab64acf3d03_v2_0007: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_4e08eb4e988d38e4_v2_0195: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_57a7e75567f9a5c3_v2_0007: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_cbe22ab64acf3d03_v2_0002: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_846a4041fe96a64e_v2_0002: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_edcb265eccf9cd32_v2_0012: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md

## brta_age_scenario (brta / professional_license_age / scenario)

Question: আমার বয়স ২০ বছর। বাসচালকের পেশাদার লাইসেন্সের জন্য এখন আবেদন করতে পারব কি?

Model: qwen2.5:7b; route: llm; time: 63.03 s; expected evidence present: False.

Answer:

1. 申请人必须具备至少一年的轻型机动车驾驶经验，或在政府规定的项目下完成重型机动车驾驶培训并获得至少一年的经验。
2. 年龄需达到23岁及以上才能申请重型机动车驾驶证。 
3. 更改或更新驾照时需要提供相关细节，并且可能需要通过特定考试以证明其技能水平。

这些步骤基于提供的文档内容支持。具体操作还需参考官方指南和最新规定。

Sources: brta_57a7e75567f9a5c3_v2_0008, brta_4e08eb4e988d38e4_v2_0195, brta_4e08eb4e988d38e4_v2_0017

Retrieved sources:
- brta_57a7e75567f9a5c3_v2_0008: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_4e08eb4e988d38e4_v2_0195: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0017: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_57a7e75567f9a5c3_v2_0007: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_edcb265eccf9cd32_v2_0012: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md
- brta_cbe22ab64acf3d03_v2_0007: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md

## brta_age_code_mixed (brta / professional_license_age / code_mixed)

Question: professional driving licence er minimum age koto?

Model: qwen2.5:7b; route: llm; time: 87.04 s; expected evidence present: False.

Answer:

The minimum age to apply for a professional driving license in Bangladesh is 21 years old.

Sources: brta_4e08eb4e988d38e4_v2_0017, brta_cbe22ab64acf3d03_v2_0007, brta_57a7e75567f9a5c3_v2_0007

Retrieved sources:
- brta_4e08eb4e988d38e4_v2_0017: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_cbe22ab64acf3d03_v2_0007: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_57a7e75567f9a5c3_v2_0007: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_4e08eb4e988d38e4_v2_0195: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_cbe22ab64acf3d03_v2_0002: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_edcb265eccf9cd32_v2_0012: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md

## brta_colour_direct (brta / vehicle_colour_change / direct)

Question: গাড়ির রং পরিবর্তন করতে কী কী কাগজপত্র লাগবে?

Model: qwen2.5:7b; route: llm; time: 112.99 s; expected evidence present: True.

Answer:

গাড়ির রং পরিবর্তন করতে নিম্নলিখিত কাগজপত্র জমা দেবেন:

1. আবেদনপত্র - ০১ কপি (মালিকের স্বাক্ষর)
2. মূল নিবন্ধন সনদ (হোম কপি অস্থায়ী নিবন্ধন সনদের ক্ষেত্রে)
3. ফি জমার রশিদ - ০১ কপি (রং পরিবর্তন ফি)
4. ফিটনেস সনদের ফটোকপি - ০১ কপি
5. ট্যাক্স টোকেনের ফটোকপি - ০১ কপি

Sources: brta_a40ff0f214eb68b8_v2_0002, brta_a40ff0f214eb68b8_v2_0001, brta_e21467da1ba75db4_v2_0002

Retrieved sources:
- brta_a40ff0f214eb68b8_v2_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_v2_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_e21467da1ba75db4_v2_0002: fahim_brta/সেবাসমূহ/তথ্য সংশোধনপরিবর্তন.md
- brta_edcb265eccf9cd32_v2_0033: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md
- brta_4b4c003681ae6872_v2_0002: fahim_brta/সেবাসমূহ/মোটরযানের নিবন্ধন.md
- brta_29228d7f41bd4857_v2_0036: fahim_brta/ফরম/ফরম-১৭ মোটরযান রেজিস্ট্রেশনের আবেদন.md

## brta_colour_paraphrase (brta / vehicle_colour_change / paraphrase)

Question: রেজিস্ট্রেশনে এক রং আছে কিন্তু গাড়ি অন্য রং করতে চাই। কী দলিল লাগতে পারে?

Model: qwen2.5:7b; route: llm; time: 74.18 s; expected evidence present: True.

Answer:

根据《道路交通法》2018年，变更注册车辆的内部或外部特征需要获得相关部门批准。具体步骤如下：

1. 对于注册过的机动车进行任何改造（包括颜色改变），必须向有关部门申请并得到许可。
2. 政府有权指定特定类型的汽车的颜色，并且未经政府或主管部门同意不得更改这些规定颜色。

因此，在完成数字注册证书程序后，将通过短信通知申请人相关事宜。需要注意的是，颜色变化过程需由Fitnance和Taxtech共同完成。

Sources: brta_a40ff0f214eb68b8_v2_0002, brta_a40ff0f214eb68b8_v2_0001, brta_edcb265eccf9cd32_v2_0033

Retrieved sources:
- brta_a40ff0f214eb68b8_v2_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_v2_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_edcb265eccf9cd32_v2_0033: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md
- brta_4e08eb4e988d38e4_v2_0039: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0191: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0047: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md

## brta_colour_scenario (brta / vehicle_colour_change / scenario)

Question: আমার ব্যক্তিগত গাড়ি সাদা থেকে কালো করেছি। BRTA রেকর্ডে রং পরিবর্তনের জন্য কী কাগজ নিয়ে আবেদন করব?

Model: qwen2.5:7b; route: llm; time: 158.12 s; expected evidence present: True.

Answer:

ধন্যবাদ। আপনার গাড়ির রঙ পরিবর্তনের জন্য নিম্নলিখিত চলতি পদক্ষেপগুলো অনুসরণ করা উচিত:

1. ব্যাংকে রং পরিবর্তন ফি জমা দিন।
2. এরপর সার্কেলের মোটরযানের মালিকানা বদলী শাখায় আবেদন করুন। আবেদনে প্রমাণ ও উপযুক্ত কারণ থাকার সাদা কাগজ জোড়াই দিন।
3. মোটরযানটি হাজির করুন, যাতে সহকারী পরিচালক (ইঞ্জিনিয়ারিং) পরিদর্শন করতে পারেন।
4. পরিদর্শনের অনুমোদন পাইয়ে ডিজিটাল রেজিস্ট্রেশন সার্টিফিকেট প্রাপ্ত হওয়ার পর এ-সার্টিফিকেট ব্যবহার করে নিবন্ধন করুন।

Sources: brta_a40ff0f214eb68b8_v2_0001, brta_a40ff0f214eb68b8_v2_0002, brta_e21467da1ba75db4_v2_0002

Retrieved sources:
- brta_a40ff0f214eb68b8_v2_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_v2_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_e21467da1ba75db4_v2_0002: fahim_brta/সেবাসমূহ/তথ্য সংশোধনপরিবর্তন.md
- brta_4b4c003681ae6872_v2_0002: fahim_brta/সেবাসমূহ/মোটরযানের নিবন্ধন.md
- brta_4e08eb4e988d38e4_v2_0039: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_29228d7f41bd4857_v2_0036: fahim_brta/ফরম/ফরম-১৭ মোটরযান রেজিস্ট্রেশনের আবেদন.md

## brta_colour_code_mixed (brta / vehicle_colour_change / code_mixed)

Question: car er colour change BRTA te update korte ki documents lagbe?

Model: qwen2.5:7b; route: llm; time: 168.69 s; expected evidence present: True.

Answer:

### গাড়ির কাগজপত্ত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স এর জরিমানা ব্যতীত মূল কর বা ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্ত্র হালনাগাদ সংক্রান্ত আদেশ:

1. **আবেদনপত্র:** মালিকের স্বাক্ষর সম্বলিত আবেদন পত্র - ০১ কপি
2. **মূল নিবন্ধন সনদ:** মূল নিবন্ধন সনদ (কাগজের নিবন্ধন সনদ হলে হোম কপিও জমা দিতে হবে)
3. **ফি জমার রশিদ:** রং পরিবর্তন ফি জমার রশিদের বিআরটিএ'র কপি
4. **ফিটনেস সনদ:** হালনাগাদ ফিটনেস সনদের ফটোকপি ০১ কপি
5. **ট্যাক্স টোকেন:** হালনাগাদ ট্যাক্স টোকেনের ফটোকপি - ০১ কপি

**তারিখ:** ২২-০৬-২০২০  
**অফিসাল ডটকম:** [Source 1] id=brta_33c0c02c5416861c_v2_0005; [Source 2] id=brta_33c0c02c5416861c_v2_0007; [Source 3] id=brta_33c0c02c5416861c_v2_0005

Sources: brta_a40ff0f214eb68b8_v2_0001, brta_a40ff0f214eb68b8_v2_0002, brta_33c0c02c5416861c_v2_0005

Retrieved sources:
- brta_a40ff0f214eb68b8_v2_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_v2_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_33c0c02c5416861c_v2_0005: brta/আইন, বিধি ও নীতিমালা/গাড়ির কাগজপত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স এর জরিমানা ব্যতীত মূল কর বা ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্র হালনাগাদ সংক্রান্ত প্রজ্ঞাপন.md
- brta_4e08eb4e988d38e4_v2_0199: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_9a180bfd62e0eab9_v2_0004: brta/আইন, বিধি ও নীতিমালা/জরিমানা ব্যতীত মূল কর বা ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স হালনাগাদের সময়সীমা ১৫ এপ্রিল ২০২৪ খ্রিঃ পর্যন্ত বর্ধিতকরণ সংক্রান্ত প্রজ্ঞাপন.md
- brta_9a180bfd62e0eab9_v2_0002: brta/আইন, বিধি ও নীতিমালা/জরিমানা ব্যতীত মূল কর বা ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স হালনাগাদের সময়সীমা ১৫ এপ্রিল ২০২৪ খ্রিঃ পর্যন্ত বর্ধিতকরণ সংক্রান্ত প্রজ্ঞাপন.md

## brta_fitness_direct (brta / fitness_renewal / direct)

Question: গাড়ির ফিটনেস সনদ নবায়ন কীভাবে করব?

Model: qwen2.5:7b; route: llm; time: 80.52 s; expected evidence present: True.

Answer:

根据提供的信息，以下是关于摩托车注册后申请健身证书的步骤：

1. 在提交新登记或重新认证请求后的第15天（最多不超过30天）内完成车辆检查。
2. 由车辆检验员进行道路测试，并确保提供必要的设施如燃料等。
3. 车主、驾驶员或其他责任人需配合并提供所需服务以完成检测。
4. 检验完成后，如果合格，则会发放新的健康证明副本。若丢失或损坏需要补办时：
   - 向相关车辆检验员报告情况；
   - 支付相应的费用并提出复件申请；
   - 如原证已失效，在当地警局做GDI录入。

以上流程基于文档内容整理得出，具体操作可能因地区而异，请参考官方指南确认详细要求。

Sources: brta_d516e1b85b1f7144_v2_0001, brta_4e08eb4e988d38e4_v2_0062, brta_4e08eb4e988d38e4_v2_0065

Retrieved sources:
- brta_d516e1b85b1f7144_v2_0001: fahim_brta/সেবাসমূহ/ফিটনেস ইস্যু ও নবায়ন.md
- brta_4e08eb4e988d38e4_v2_0062: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0065: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0060: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_d516e1b85b1f7144_v2_0002: fahim_brta/সেবাসমূহ/ফিটনেস ইস্যু ও নবায়ন.md
- brta_09e8cbfff67f117e_v2_0020: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md

## brta_fitness_paraphrase (brta / fitness_renewal / paraphrase)

Question: আমার গাড়ির ফিটনেসের মেয়াদ শেষ। কোন প্রক্রিয়ায় রিনিউ করব?

Model: qwen2.5:7b; route: llm; time: 97.83 s; expected evidence present: True.

Answer:

### Steps to Apply for Motor Vehicle Fitness Renewal

1. **Register an Account on BRTA Service Portal**: Log in using a registered account.
2. **Link Your Vehicle**: Provide necessary vehicle information and link your motor vehicle through the portal.
3. **Submit Application**: After successful linking, submit an application for fitness renewal.
4. **Pay Fee Early**: Pay the applicable fee before the due date; 50% additional fee will be charged if paid after 15 days of submission or as per regulations.
5. **Vehicle Inspection**: Before the inspection day, ensure you have all required documents ready:
   - Auto-generated CF/CFR form with applicant's signature.
   - Receipt proof of payment.
   - Copy of excise tax token.
   - Proof of road tax (TIN certificate is needed).
6. **Attend Inspection**: On the scheduled date, bring the vehicle to the designated BRTA circle office for inspection.
7. **Additional Note**: If the last fitness expiry date has passed but no serial number is available yet, still apply for the appointment. An invalid appointment made without proper scheduling needs to be rescheduled.

These steps are supported by [Source 3], which details the process and requirements for applying for motor vehicle fitness renewal under the BRTA service charter.

Sources: brta_d516e1b85b1f7144_v2_0001, brta_4e08eb4e988d38e4_v2_0062, brta_09e8cbfff67f117e_v2_0020

Retrieved sources:
- brta_d516e1b85b1f7144_v2_0001: fahim_brta/সেবাসমূহ/ফিটনেস ইস্যু ও নবায়ন.md
- brta_4e08eb4e988d38e4_v2_0062: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_09e8cbfff67f117e_v2_0020: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_4e08eb4e988d38e4_v2_0067: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_09e8cbfff67f117e_v2_0037: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_09e8cbfff67f117e_v2_0019: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md

## brta_fitness_scenario (brta / fitness_renewal / scenario)

Question: আগামী সপ্তাহে গাড়ির ফিটনেস শেষ হবে। মেয়াদ শেষ হওয়ার আগে নবায়নের জন্য কী করতে হবে?

Model: qwen2.5:7b; route: llm; time: 103.92 s; expected evidence present: True.

Answer:

### Procedural Steps for Motor Vehicle Fitness Renewal

1. **Register an Account on BRITA Service Portal**: Log in to your registered account on the BRITA service portal.
2. **Link Your Vehicle**: Link your motor vehicle with the system as per instructions provided.
3. **Submit Application Online**: Apply online for fitness renewal before the expiry date through the same platform.
4. **Pay Fees and Obtain Receipt**: Pay the prescribed fee and obtain a money receipt prior to bringing the vehicle for inspection.
5. **Vehicle Inspection**: Bring the vehicle to the designated BRITA circle office at the scheduled time for inspection.
6. **Required Documents**:
   - Self-signed CF/CFR form generated from the BRITA service portal during application submission.
   - Copy of paid tax token (if applicable).
   - Proof of approved/duly paid tax if required based on the nature of the vehicle.
7. **Fees Details**:
   - Light vehicles: BDT 1,892/- 
   - Heavy vehicles: BDT 2,295/-

Ensure all documents are complete and up-to-date; late applications may be rejected. If you miss the appointment due to unforeseen circumstances, reapply accordingly.

Note that if the 'Fitness Expire Last Date' is reached but no serial number has been assigned yet, an application can still be submitted until the end of the day. However, any missed appointments will require rescheduling.

Sources: brta_d516e1b85b1f7144_v2_0001, brta_2dd33c08c48bf098_v2_0011, brta_09e8cbfff67f117e_v2_0020

Retrieved sources:
- brta_d516e1b85b1f7144_v2_0001: fahim_brta/সেবাসমূহ/ফিটনেস ইস্যু ও নবায়ন.md
- brta_2dd33c08c48bf098_v2_0011: brta/ফি, ট্যাক্স ও আয়কর/মোটরযানের অগ্রিম বা অনুমিত আয়কর ২০১৬-২০১৭ (মোটর কার, জীপ বা মাইক্রোবাস).md
- brta_09e8cbfff67f117e_v2_0020: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_4e08eb4e988d38e4_v2_0062: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0067: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_b2784bdfab996348_v2_0005: brta/আইন, বিধি ও নীতিমালা/এস,আর ও নং ১৬৫-আইন-আয়কর-২০২১.md

## brta_fitness_code_mixed (brta / fitness_renewal / code_mixed)

Question: vehicle fitness renew korar process ki?

Model: qwen2.5:7b; route: llm; time: 78.88 s; expected evidence present: True.

Answer:

To renew vehicle fitness in Bangladesh:

1. Go to any BRTA circle office with your vehicle.
2. Have a satisfactory inspection done by an inspector.
3. Fill out the application form and submit it along with the payment of the required fee.
4. Get the new fitness certificate issued after passing the inspection.

Sources: brta_d516e1b85b1f7144_v2_0001, brta_2dd33c08c48bf098_v2_0011, brta_0cfecd15e24b39b9_v2_0002

Retrieved sources:
- brta_d516e1b85b1f7144_v2_0001: fahim_brta/সেবাসমূহ/ফিটনেস ইস্যু ও নবায়ন.md
- brta_2dd33c08c48bf098_v2_0011: brta/ফি, ট্যাক্স ও আয়কর/মোটরযানের অগ্রিম বা অনুমিত আয়কর ২০১৬-২০১৭ (মোটর কার, জীপ বা মাইক্রোবাস).md
- brta_0cfecd15e24b39b9_v2_0002: brta/ফি, ট্যাক্স ও আয়কর/মোটরযানের অগ্রিম বা অনুমিত আয়কর ২০২৩-২০২৪ (মোটর কার, জীব বা মাইক্রোবাস).md
- brta_09e8cbfff67f117e_v2_0020: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_c621e9f59be18a98_v2_0010: brta/ফি, ট্যাক্স ও আয়কর/মোটরযানের অগ্রিম বা অনুমিত আয়কর ২০২৪-২০২৫ (মোটর কার, জীব বা মাইক্রোবাস).md
- brta_b2784bdfab996348_v2_0005: brta/আইন, বিধি ও নীতিমালা/এস,আর ও নং ১৬৫-আইন-আয়কর-২০২১.md

## brta_multi_renew_address (brta / multi_condition / multi_condition)

Question: ড্রাইভিং লাইসেন্স নবায়নের সঙ্গে ঠিকানা পরিবর্তনও করতে চাই। কোন ফরম প্রাসঙ্গিক?

Model: qwen2.5:7b; route: llm; time: 67.16 s; expected evidence present: True.

Answer:

为了申请变更驾驶执照上的地址，您需要填写表格5，并提供以下信息：

1. 个人信息：包括您的全名、旧住址和新住址。
2. 驾驶执照号码。

步骤如下：
- 前往相关部门或在线提交表格5（Form-5）；
- 提交更新后的水电费账单或其他证明文件以验证新的居住地址；
- 按要求支付相关费用；
- 在规定时间内收到并完成所有手续后，领取更新了新地址的驾驶执照。

Sources: brta_4e08eb4e988d38e4_v2_0203, brta_4e08eb4e988d38e4_v2_0016, brta_e640c49d6025cc8d_v2_0004

Retrieved sources:
- brta_4e08eb4e988d38e4_v2_0203: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0016: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_e640c49d6025cc8d_v2_0004: fahim_brta/ফরম/ফরম-৫ ড্রাইভিং লাইসেন্সের ঠিকানা পরিবর্তনের আবেদন.md
- brta_4e08eb4e988d38e4_v2_0199: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_258cf38650a6332b_v2_0023: fahim_brta/ফরম/ফরম-৪(খ) মোটর ড্রাইভিং লাইসেন্স নবায়ন,প্রতিলিপি,শ্রেণি পরিবর্তন বা সংযোজন,ধরন পরিবর্তন,ঠিকানা পরিবর্তন,তথ্য সংশোধনের আবেদন.md
- brta_e640c49d6025cc8d_v2_0007: fahim_brta/ফরম/ফরম-৫ ড্রাইভিং লাইসেন্সের ঠিকানা পরিবর্তনের আবেদন.md

## brta_multi_owner_docs (brta / multi_condition / multi_condition)

Question: ব্যবহৃত গাড়ি কিনেছি। মালিকানা বদলি করতে ক্রেতা ও বিক্রেতা উভয়ের কোন ঘোষণা বা কাগজ লাগতে পারে?

Model: qwen2.5:7b; route: llm; time: 138.71 s; expected evidence present: True.

Answer:

### বিক্রেতার করণীয়

1. **ফরম 'টিটিও' এবং বিক্রয় রশিদ:** ফরম 'টিটিও' এবং বিক্রয় রশিদে স্বাক্ষর করুন।
2. **বিক্রয় হলফনামা:** ছবিসহ বিক্রয় হলফনামা লিখুন।
3. **কোম্পানীর ক্ষেত্রে প্রয়োজনীয় কাগজপত্র:** 
   - লেটার হেড প্যাডে ইন্টিমেশন,
   - বোর্ড রেজুলেশন, 
   - অথরাইজেশন পত্র প্রদান করুন (এই তিনগুলি জন্য কোম্পানীর লেটার হেড প্যাডে চিঠি)।
4. **দায়বদ্ধকারী প্রতিষ্ঠানের ঋণ পরিশোধের ছাড়পত্র:** দায়বদ্ধকারী প্রতিষ্ঠানের ঋণ পরিশোধ সংক্রান্ত ছাড়পত্র সংগ্রহ করুন।

Sources: brta_09e8cbfff67f117e_v2_0022, brta_d9357851a61a163d_v2_0004, brta_d9357851a61a163d_v2_0003

Retrieved sources:
- brta_09e8cbfff67f117e_v2_0022: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_d9357851a61a163d_v2_0004: fahim_brta/সেবাসমূহ/মালিকানা বদলী.md
- brta_d9357851a61a163d_v2_0003: fahim_brta/সেবাসমূহ/মালিকানা বদলী.md
- brta_2d2e92b7e02c5193_v2_0002: fahim_brta/ফরম/ফরম-২১ মোটরযানের মালিকানা বদলি সংক্রান্ত ক্রেতার ঘোষণাপত্র.md
- brta_2d2e92b7e02c5193_v2_0007: fahim_brta/ফরম/ফরম-২১ মোটরযানের মালিকানা বদলি সংক্রান্ত ক্রেতার ঘোষণাপত্র.md
- brta_77a34fc07ff34054_v2_0004: fahim_brta/ফরম/ফরম-২০ মোটরযানের মালিকানা বদলি সংক্রান্ত বিক্রেতার ঘোষণাপত্র.md

## brta_boundary_passport (brta / boundary / out_of_domain)

Question: ই-পাসপোর্ট অনলাইন অ্যাকাউন্টের পাসওয়ার্ড ভুলে গেলে কী করব?

Model: qwen2.5:7b; route: llm; time: 144.02 s; expected evidence present: None.

Answer:

পাসওয়ার্ড ভুলে গেলে এই চক্রণগুলোতে পৌঁছুন:

1. ইমেইল/মোবাইল নাম্বার এবং পাসওয়ার্ড সঠিকভাবে তাকালে "Login" বাটনে ক্লিক করুন।
2. অথবা জাহির করা ফোর্ম থেকে নিজের অ্যাকাউন্ট ID ও পাসওয়ার্ড দিয়ে আবার লogin করুন।

এটি শেষ হলে আপনার অ্যাকাউন্টে পৌঁছানো যাবে।

Sources: brta_91979c30a91124e0_v2_0015, brta_6eb3d41986361dbd_v2_0005, brta_09e8cbfff67f117e_v2_0011

Retrieved sources:
- brta_91979c30a91124e0_v2_0015: brta/আইন, বিধি ও নীতিমালা/রাইড শেয়ারিং গাইডলাইন ২০১৭.md
- brta_6eb3d41986361dbd_v2_0005: brta/ফি, ট্যাক্স ও আয়কর/বিভিন্ন ফি জানার টিউটোরিয়াল ডকুমেন্ট.md
- brta_09e8cbfff67f117e_v2_0011: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_4e08eb4e988d38e4_v2_0149: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_6eb3d41986361dbd_v2_0003: brta/ফি, ট্যাক্স ও আয়কর/বিভিন্ন ফি জানার টিউটোরিয়াল ডকুমেন্ট.md
- brta_f609dec009c587e0_v2_0004: brta/আইন, বিধি ও নীতিমালা/ই-ড্রাইভিং লাইসেন্স সংক্রান্ত সংশোধিত প্রজ্ঞাপন.md

## passport_collect_direct (passport / passport_collection / direct)

Question: ই-পাসপোর্ট সংগ্রহ করতে অফিসে কী কী নিয়ে যেতে হবে?

Model: qwen2.5:7b; route: llm; time: 113.49 s; expected evidence present: False.

Answer:

ই-পাসপোর্ট বায়োমেট্রিক প্রক্রিয়ার জন্য পাসপোর্ট অফিসে নিম্ন লিখিত কাগজপত্র বহন করতে হবে:
1. পিআরএল (PRL) অর্ডার কপি。
2. জাতীয় পরিচয়পত্র (NID)。
3. পূর্ববর্তী মূল পাসপোর্ট。
4. আবেদনপত্রের হার্ড কপি（Application Form）。
5. প্রিন্ট সারাংশ（Summary Slip）。
6. পাসপোর্ট ফি প্রদানের রসিদ/পেমেন্ট স্লিপ。

Sources: passport_23d845d3ab38ea43_v2_0033, passport_6e87d0783a373593_v2_0008, passport_23d845d3ab38ea43_v2_0041

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0033: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_6e87d0783a373593_v2_0008: cleaned_md/5 Steps to your e-Passport.md
- passport_23d845d3ab38ea43_v2_0041: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_73ac41f2327257f9_v2_0003: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0004: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0001: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md

## passport_collect_paraphrase (passport / passport_collection / paraphrase)

Question: পাসপোর্ট রেডি হলে নিতে যাওয়ার সময় কোন কাগজ দেখাতে হয়?

Model: qwen2.5:7b; route: llm; time: 91.68 s; expected evidence present: True.

Answer:

পাসপোর্ট গ্রহণের সময় দেখাতে হবে:
- ডেলিভারি স্লিপ।
- অভিভাবকের NID/পাসপোরট (সন্তানের জন্য)।
- আদেশ পত্র এবং প্রতিনিধির NID (অনুমোদিত প্রতিনিধি থাকলে)।
- পূর্বের মূল পাসপোর্ট।

Sources: passport_23d845d3ab38ea43_v2_0040, passport_73ac41f2327257f9_v2_0004, passport_73ac41f2327257f9_v2_0003

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0040: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_73ac41f2327257f9_v2_0004: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0003: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_729010959c882773_v2_0004: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md
- passport_729010959c882773_v2_0003: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md
- passport_73ac41f2327257f9_v2_0001: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md

## passport_collect_scenario (passport / passport_collection / scenario)

Question: আমার পাসপোর্ট প্রস্তুত হয়েছে। আমি নিজে অফিসে গিয়ে সংগ্রহ করব। সঙ্গে কী রাখতে হবে?

Model: qwen2.5:7b; route: llm; time: 162.62 s; expected evidence present: True.

Answer:

আপনি পাসপোর্ট অফিসে গিয়ে সংগ্রহ করার সময় নিম্নলিখিত কাগজপত্র নিয়ে যেতে হবে:

1. আবেদনপত্রের সারংশের প্রিন্ট কপি (অ্যাপয়েন্টমেন্ট সহ)।
2. সনাক্তকরণ নথির প্রিন্ট কপি (জাতীয় পরিচয় পত্র/ জন্ম নিবন্ধন নং)।
3. পূর্ববর্তী পাসপোর্ট এবং ডাটা পেজের প্রিন্ট কপি (যদি থাকে)।
4. আবেদনপত্রের প্রিন্ট কপি।

এছাড়াও, অফিসে গিয়ে দেখাই করতে হলে পেমেন্ট স্লিপ (for Offline Payment only), প্রয়োজনীয় কাগজপত্র (সরকারি চাকরিজীবীদের ক্ষেত্রে GO/NOC, যদি থাকে) ও তথ্য সংশোধনের ক্ষেত্রে প্রয়োজনীয় কাগজপত্র (যদি থাকে) নিয়ে যেতে হবে।

Sources: passport_73ac41f2327257f9_v2_0001, passport_73ac41f2327257f9_v2_0004, passport_73ac41f2327257f9_v2_0002

Retrieved sources:
- passport_73ac41f2327257f9_v2_0001: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0004: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0002: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0003: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_23d845d3ab38ea43_v2_0041: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0040: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_collect_code_mixed (passport / passport_collection / code_mixed)

Question: e-passport collect korte office e ki documents niye jete hobe?

Model: qwen2.5:7b; route: llm; time: 60.79 s; expected evidence present: True.

Answer:

To collect a new passport from the passport office in Bangladesh, follow these steps:

- Bring the original delivery slip received during passport enrollment.
- If collecting on behalf of someone else:
  - Bring signed authorization letter from the applicant.
  - Both the authorized person and the applicant must present their National Identity Cards (NID).

Sources: passport_23d845d3ab38ea43_v2_0040, passport_23d845d3ab38ea43_v2_0033, passport_6e87d0783a373593_v2_0008

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0040: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0033: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_6e87d0783a373593_v2_0008: cleaned_md/5 Steps to your e-Passport.md
- passport_23d845d3ab38ea43_v2_0032: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_6f7d900581956bef_v2_0006: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_729010959c882773_v2_0003: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md

## passport_password_direct (passport / account_password_recovery / direct)

Question: অনলাইন পাসপোর্ট অ্যাকাউন্টের পাসওয়ার্ড ভুলে গেলে কী করতে হবে?

Model: qwen2.5:7b; route: llm; time: 91.68 s; expected evidence present: True.

Answer:

1. অ্যাকাউন্ট সাইন ইন অপশনে যান।
2. "Forgot password" লিঙ্কে ক্লিক করুন।
3. ই-মেইল অ্যাড্রেসে প্রবেশ করুন।
4. ই-মেইল অ্যাকাউন্টের রিকভারি মেসেজে দেওয়া নির্দেশনা অনুসরণ করুন।

Sources: passport_23d845d3ab38ea43_v2_0004, passport_23d845d3ab38ea43_v2_0005, passport_23d845d3ab38ea43_v2_0043

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0004: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0005: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0043: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0015: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_5eb6c21efe103a4f_v2_0034: cleaned_md/Bangladesh Machine Readable Passport (MRP) Online Application Guide 2012.md
- passport_23d845d3ab38ea43_v2_0036: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_password_paraphrase (passport / account_password_recovery / paraphrase)

Question: ই-পাসপোর্ট পোর্টালে লগইন করতে পারছি না, কারণ পাসওয়ার্ড মনে নেই। কীভাবে রিসেট করব?

Model: qwen2.5:7b; route: llm; time: 103.63 s; expected evidence present: True.

Answer:

পাসওয়ার্ড মনে নেই হচ্ছে? তাহলে ফলো করুন:

1. ই-পাসপোর্ট লগইন পোর্টালে যান।
2. "Forgot password" লিঙ্কটি খুঁড়ুন।
3. আপনার ই-মেইল এজেন্টে দাখিল করুন।
4. প্রদত্ত নির্দেশনাগুলো অনুসরণ করুন।

Sources: passport_23d845d3ab38ea43_v2_0004, passport_23d845d3ab38ea43_v2_0036, passport_5d0353de7b67a7b5_v2_0004

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0004: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0036: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_5d0353de7b67a7b5_v2_0004: cleaned_md/রক্ষণাবেক্ষণ ও আপগ্রেডেশনের জন্য ই-পাসপোর্ট অনলাইন রেজিস্ট্রেশন পোর্টালের ডাউনটাইম প্রসঙ্গে.md
- passport_9f4e9ffe9f2a07f4_v2_0002: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_f00b2a4caf73fc8e_v2_0004: cleaned_md/প্রতারণা প্রতিরোধে বিশেষ সতর্কতা.md
- passport_caccc3966e7586d0_v2_0002: cleaned_md/বিশেষ সতর্কতা ই-পাসপোর্ট.md

## passport_password_scenario (passport / account_password_recovery / scenario)

Question: আবেদনের অবস্থা দেখতে অনলাইন অ্যাকাউন্টে ঢুকতে চাই, কিন্তু পাসওয়ার্ড ভুলে গেছি। আমার করণীয় কী?

Model: qwen2.5:7b; route: llm; time: 82.65 s; expected evidence present: True.

Answer:

1. অ্যাকাউন্ট সাইন ইন অপশনে যান।
2. "Forgot password" লিঙ্কে ক্লিক করুন।
3. ই-মেইল অ্যাড্রেসে প্রবেশ করুন।
4. ই-মেইল অ্যাকাউন্টের রিকভারি মেসেজে দেওয়া নির্দেশনা অনুসরণ করুন।

Sources: passport_23d845d3ab38ea43_v2_0004, passport_23d845d3ab38ea43_v2_0043, passport_23d845d3ab38ea43_v2_0038

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0004: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0043: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0038: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0007: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0005: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0015: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_password_code_mixed (passport / account_password_recovery / code_mixed)

Question: e passport account password vule gechi, reset korbo kivabe?

Model: qwen2.5:7b; route: llm; time: 70.39 s; expected evidence present: True.

Answer:

To reset your forgotten password:

1. Go to the account sign-in page.
2. Click on "Forgot password."
3. Enter your email address.
4. Follow the instructions in your email to reset your password.

Sources: passport_23d845d3ab38ea43_v2_0004, passport_23d845d3ab38ea43_v2_0005, passport_23d845d3ab38ea43_v2_0036

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0004: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0005: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0036: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0003: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0006: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0019: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_regular_delivery_direct (passport / regular_delivery_time / direct)

Question: বায়োমেট্রিক দেওয়ার পর নিয়মিত ই-পাসপোর্ট সাধারণত কত সময়ের মধ্যে পাওয়া যায়?

Model: qwen2.5:7b; route: llm; time: 66.7 s; expected evidence present: True.

Answer:

বায়োমেট্রিক দেওয়ার পর নিয়মিত ই-পাসপোর্ট সাধারণত 15 কাজক্রমদিন / 21 দিনের মধ্যে পাওয়া যায়।

Sources: passport_12e10027cfdfeeee_v2_0005, passport_09c70e4e1e93efad_v2_0004, passport_09c70e4e1e93efad_v2_0005

Retrieved sources:
- passport_12e10027cfdfeeee_v2_0005: cleaned_md/e-Passport Fees and Payment Options.md
- passport_09c70e4e1e93efad_v2_0004: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0005: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0002: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0003: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0001: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md

## passport_regular_delivery_paraphrase (passport / regular_delivery_time / paraphrase)

Question: রেগুলার ই-পাসপোর্টের ডেলিভারি টাইম কত?

Model: qwen2.5:7b; route: llm; time: 57.24 s; expected evidence present: True.

Answer:

রেগুলার ই-পাসপোর্টের ডেলিভারি টাইম ১৫টি কর্মদিবস।

Sources: passport_12e10027cfdfeeee_v2_0005, passport_9f4e9ffe9f2a07f4_v2_0004, passport_5eb6c21efe103a4f_v2_0026

Retrieved sources:
- passport_12e10027cfdfeeee_v2_0005: cleaned_md/e-Passport Fees and Payment Options.md
- passport_9f4e9ffe9f2a07f4_v2_0004: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_5eb6c21efe103a4f_v2_0026: cleaned_md/Bangladesh Machine Readable Passport (MRP) Online Application Guide 2012.md
- passport_9f4e9ffe9f2a07f4_v2_0003: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_f2c0d221c70d21f2_v2_0003: cleaned_md/Urgent Applications e-Passport.md
- passport_6f7d900581956bef_v2_0006: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md

## passport_regular_delivery_scenario (passport / regular_delivery_time / scenario)

Question: আজ বায়োমেট্রিক দিলাম এবং নিয়মিত ডেলিভারি নিয়েছি। আনুমানিক কবে পাসপোর্ট পাব?

Model: qwen2.5:7b; route: llm; time: 94.65 s; expected evidence present: True.

Answer:

আপনার বায়োমেট্রিক গ্রহণ ও নিয়মিত ডেলিভারি করেছেন। আপনার পাসপোর্ট পолуч取中文翻译：

您已经完成了生物识别登记并选择了常规递送方式。根据现有信息，您的护照预计将在15个工作日（即21天）内送达。

请注意，如果选择加急服务，则可以在7个工作日内（约10天）收到；而超级加急服务则可在2个工作日内完成。
---

答案：您已完成生物识别注册，并选择了常规配送选项。预计在提交生物识别后的15个工 作日内（大约21天），您可以获得护照。如需更快的配送，请咨询相关部门了解加急和超级 加急服务的具体情况。

Sources: passport_12e10027cfdfeeee_v2_0005, passport_09c70e4e1e93efad_v2_0006, passport_09c70e4e1e93efad_v2_0004

Retrieved sources:
- passport_12e10027cfdfeeee_v2_0005: cleaned_md/e-Passport Fees and Payment Options.md
- passport_09c70e4e1e93efad_v2_0006: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0004: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0002: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_cd3935ff9dcc81c4_v2_0004: cleaned_md/বিশেষ নোটিশঃ নারায়ণগঞ্জ আঞ্চলিক পাসপোর্ট অফিসের কার্যক্রম পুনরায় শুরু প্রসঙ্গে.md
- passport_09c70e4e1e93efad_v2_0005: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md

## passport_regular_delivery_code_mixed (passport / regular_delivery_time / code_mixed)

Question: regular e-passport biometric er por delivery time koto?

Model: qwen2.5:7b; route: llm; time: 53.59 s; expected evidence present: True.

Answer:

The regular e-passport delivery time is within 15 working days from the biometric enrolment date.

Sources: passport_12e10027cfdfeeee_v2_0005, passport_9f4e9ffe9f2a07f4_v2_0004, passport_09c70e4e1e93efad_v2_0004

Retrieved sources:
- passport_12e10027cfdfeeee_v2_0005: cleaned_md/e-Passport Fees and Payment Options.md
- passport_9f4e9ffe9f2a07f4_v2_0004: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_09c70e4e1e93efad_v2_0004: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0005: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0006: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0003: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md

## passport_multi_minor_photo (passport / multi_condition / multi_condition)

Question: আমার সন্তানের বয়স ৫ বছর এবং তার NID নেই। ই-পাসপোর্ট আবেদনে পিতা বা মাতার NID এবং ছবি লাগবে কি?

Model: qwen2.5:7b; route: llm; time: 264.04 s; expected evidence present: True.

Answer:

### ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী

1. **ই-পাসপোর্ট আবেদন:** 
   - আবেদনপত্র অনলাইনে পূরণ করা যাবে (Source 3).

2. **কাগজপত্র সত্যায়ন:** 
   - কোন কাগজপত্র সত্যায়ন করার প্রয়োজন হবে না (Source 3).

3. **ছবি সত্যায়ন:** 
   - ছবি সংযোজন এবং তা সত্যায়নের প্রয়োজন হবে না (Source 3).

4. **আবেদনপত্র পূরণ:**
   - জাতীয় পরিচয়পত্র (NID) অথবা অনলাইন জন্মনিবন্ধন সনদ (BRC English Version) অনুযায়ী আবেদনপত্র পূরণ করতে হবে।
   - অপ্রাপ্ত বয়স্ক (১৮ বছরের কম) আবেদনকারীর জাতীয় পরিচয়পত্র (NID) নাই, তাদের পিতা/মাতার NID নম্বর উল্লেখ করতে হবে (Source 1).

5. **জাতীয় পরিচয়পত্র (NID):** 
   - ১৮-২০ বছর বয়সীদের: জাতীয় পরিচয়পত্র (NID) অথবা BRC English Version (Source 3).
   - ২০ বছর ও উর্ধ্ব বয়সীদের: জাতীয় পরিচয়পত্র (NID), যদি বিদেশস্থ বাংলাদেশ মিশন হতে আবেদন করা হয়, তাহলে BRC English Versionও গ্রহণযোগ্য।

6. **তারকা:** 
   - তারকা চিহ্নিত ক্রমিক নম্বরগুলো অবশ্যই পূরণীয় (Source 1).

7. **দত্তক/অভিভাবকত্ব:** 
   - পাসপোর্টের আবেদনের সাথে সুরক্ষা সেবা বিভাগ, স্বরাষ্ট্র মন্ত্রণালয় হতে জারিকৃত আদেশ দাখিল করতে হবে (Source 3).

Sources: passport_6f7d900581956bef_v2_0007, passport_6f7d900581956bef_v2_0006, passport_9f4e9ffe9f2a07f4_v2_0002

Retrieved sources:
- passport_6f7d900581956bef_v2_0007: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0006: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_9f4e9ffe9f2a07f4_v2_0002: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_23d845d3ab38ea43_v2_0034: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0032: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0045: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_multi_lost_gd (passport / multi_condition / multi_condition)

Question: আমার ই-পাসপোর্ট হারিয়েছে এবং নতুনটির জন্য আবেদন করতে চাই। জিডির মূল কপি লাগবে কি?

Model: qwen2.5:7b; route: llm; time: 166.76 s; expected evidence present: True.

Answer:

1. **একসেট সত্যায়িত জাতীয় পরিচয়পত্র** - আवদ্ধ।
2. **ইস্যুকারী কর্তৃপক্ষের ওয়েবসাইটে প্রদর্শিত অনাপত্তি সনদ (NOC)** - আবদ্ধ।
3. **ল্যাব প্রিন্ট রঙিন ছবি** - 6x4 সাইজের ল্যাব প্রিন্ট রঙিন ছবি দাখিল করা হবে।

**Spouse Name পরিবর্তন এবং Legal Guardian Name অন্তর্ভুক্তকরণ:** 
- ই-পাসপোর্ট সিস্টেমে Spouse Name পরিবর্তন করে Legal Guardian Name অন্তর্ভুক্ত করা হবে।

**তথ্য পরিবর্তনের জন্য:**
1. **স্মারক নং: ৫৮.০০.০০০০.০৪৩.৯৯.০০২.২৪.(অংশ-২).৯৭; তারিখ: ১৮ ফেব্রুয়ারি ২০২৫** - এই নির্দেশনার উল্লেখ থেকে আগের ডকুমেন্ট দাখিল করতে হবে।

Sources: passport_9f4e9ffe9f2a07f4_v2_0005, passport_6f7d900581956bef_v2_0007, passport_6f7d900581956bef_v2_0010

Retrieved sources:
- passport_9f4e9ffe9f2a07f4_v2_0005: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_6f7d900581956bef_v2_0007: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0010: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_729010959c882773_v2_0004: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md
- passport_729010959c882773_v2_0003: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md
- passport_6f7d900581956bef_v2_0006: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md

## passport_boundary_brta (passport / boundary / out_of_domain)

Question: পেশাদার ড্রাইভিং লাইসেন্সের ন্যূনতম বয়স কত?

Model: qwen2.5:7b; route: llm; time: 109.29 s; expected evidence present: None.

Answer:

### Steps to Apply for a Biometric Information Collection of Citizens Aged 06 Years and Above

1. **Submit Completed Passport Form**: Applicants aged 06 years and above must submit two copies of the completed passport form along with other required documents.
2. **Photographs**: Provide recent color photographs measuring 35 x 25 mm for all applicants except those under 15 years old.
3. **Verification Process**:
   - For minors below 15 years, both parents' signatures on their photograph are mandatory after attaching it.
4. **Supporting Documents**: 
   - National Identity Card or Birth Certificate.
   - Relevant technical certificates if applicable (e.g., medical doctor, engineer).
5. **Eligible Individuals for Fee Waiver**: Government employees, their spouses, and minor children can avail fee waivers as per government rules.
6. **Geographical/Technical Clearance (GO/NOC)**: Required in certain cases based on specific eligibility criteria.
7. **Retired Personnel**: Specific requirements may apply for retired personnel.

These steps ensure that citizens aged six years and older undergo biometric information collection when applying for passports.

Sources: passport_9f4e9ffe9f2a07f4_v2_0003, passport_09c70e4e1e93efad_v2_0002, passport_ed7b3ebc56c0094f_v2_0003

Retrieved sources:
- passport_9f4e9ffe9f2a07f4_v2_0003: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_09c70e4e1e93efad_v2_0002: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_ed7b3ebc56c0094f_v2_0003: cleaned_md/মেশিন রিডেবল পাসপোর্ট(এমআরপি).md
- passport_09c70e4e1e93efad_v2_0006: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_6f7d900581956bef_v2_0007: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_09c70e4e1e93efad_v2_0004: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md

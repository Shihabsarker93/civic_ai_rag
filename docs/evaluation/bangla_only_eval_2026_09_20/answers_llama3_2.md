# Manual audit answers

These are raw chatbot outputs. Expected-evidence-present checks only a predefined hint and is not an answer-correctness score.

## birth_deadline_direct (birth_death_registration / birth_deadline / direct)

Question: শিশুর জন্মের কত দিনের মধ্যে জন্ম নিবন্ধনের তথ্য দিতে হয়?

Model: llama3.2; route: controlled; time: 23.76 s; expected evidence present: True.

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

Model: llama3.2; route: llm; time: 67.92 s; expected evidence present: True.

Answer:

আইনি উপ-ধারা (৩) অনুযায়ী, জন্ম ও মৃত্যু নিবন্ধনের জন্য আবেদন করার সময়সীমা ছাড়া এটি করা যায় না।

শুরু{সারিবদ্ধ}
(1) &amp; \text{ }\\
\text{(2)} \\
\text{(3)}
\end{align*}

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

Model: llama3.2; route: llm_then_evidence_fallback; time: 58.66 s; expected evidence present: True.

Answer:

(১) শিশুর পিতা বা মাতা বা অভিভাবক বা নির্ধারিত ব্যক্তি উক্ত শিশুর জন্মের ৪৫ (পঁয়তাল্লিশ) দিনের মধ্যে জন্ম সংক্রান্ত তথ্য নিবন্ধকের নিকট প্রদানের জন্য বাধ্য থাকিবেন।

(২) মৃত ব্যক্তির পুত্র বা কন্যা বা অভিভাবক বা নির্ধারিত ব্যক্তি মৃত্যুর ৪৫ (পঁয়তাল্লিশ) দিনের মধ্যে মৃত্যু সংক্রান্ত তথ্য নিবন্ধকের নিকট প্রদানের জন্য বাধ্য থাকিবেন।

Sources: birth_and_death_registration_act_2004_ধারা_৮_01, birth_and_death_registration_rules_2018_বিধি_৮_01, birth_and_death_registration_rules_2018_বিধি_২০_01

Retrieved sources:
- birth_and_death_registration_act_2004_ধারা_৮_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৮_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source
- bdris_faq_02_q01: unknown source
- birth_and_death_registration_act_2004_ধারা_১৫_01: unknown source

## birth_lost_direct (birth_death_registration / lost_certificate / direct)

Question: জন্ম নিবন্ধনের মূল সনদ হারিয়ে গেলে কী করতে হবে?

Model: llama3.2; route: controlled; time: 21.66 s; expected evidence present: True.

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

Model: llama3.2; route: controlled; time: 18.46 s; expected evidence present: True.

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

Model: llama3.2; route: controlled; time: 22.8 s; expected evidence present: True.

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

## birth_date_correction_direct (birth_death_registration / date_correction / direct)

Question: জন্ম তারিখ ভুল হলে কীভাবে সংশোধন করব এবং ফি কত?

Model: llama3.2; route: controlled; time: 18.54 s; expected evidence present: True.

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

Model: llama3.2; route: controlled; time: 21.88 s; expected evidence present: True.

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

Model: llama3.2; route: controlled; time: 24.23 s; expected evidence present: True.

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

## brta_age_direct (brta / professional_license_age / direct)

Question: পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স কত?

Model: llama3.2; route: llm; time: 51.0 s; expected evidence present: True.

Answer:

পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স ২১ বছর।

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

Model: llama3.2; route: llm; time: 93.99 s; expected evidence present: True.

Answer:

এখানে ১৫টি প্রশ্ন আছে।

1. গাড়ি চালাতে জড়িত বয়স কত?
2. গাড়ি চালাতে জড়িত বয়সের উপর ভিত্তি করে মাথা ও অঙ্গহানি কী? 
3. গাড়ি চালাতে জড়িত বয়সের উপর ভিত্তি করে দৃষ্টিশক্তি কী? 
4. গাড়ি চালাতে জড়িত বয়সের উপর ভিত্তি করে এই ধরনের রোগে আক্রান্ত হওয়ার ফলে কী ঘটে? 
5. গাড়ি চালাতে জড়িত বয়সের উপর ভিত্তি করে মদ বা ড্রাগ আসক্তি কী?
6. গাড়ি চালাতে জড়িত বয়সের উপর ভিত্তি করে অক্ষমতা কী?
7. গাড়ি চালাতে জড়িত বয়সের উপর ভিত্তি করে শারীরিক এবং দৃষ্টিশক্তির স্বাভাবিক হওয়ার ফলে কোন নির্দিষ্ট ধরনের চিহ্ন থাকে?

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

Model: llama3.2; route: llm; time: 54.3 s; expected evidence present: False.

Answer:

যে চালকেরা 1 (এক) বৎসরের অভিজ্ঞতা থাকিয়াও না থাকিয়াও ভারী মোটরযান চালাইবার ড্রাইভিং লাইসেন্সের আবেদন করতে পারে না।

Sources: brta_57a7e75567f9a5c3_v2_0008, brta_4e08eb4e988d38e4_v2_0195, brta_4e08eb4e988d38e4_v2_0017

Retrieved sources:
- brta_57a7e75567f9a5c3_v2_0008: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_4e08eb4e988d38e4_v2_0195: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0017: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_57a7e75567f9a5c3_v2_0007: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_edcb265eccf9cd32_v2_0012: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md
- brta_cbe22ab64acf3d03_v2_0007: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md

## brta_colour_direct (brta / vehicle_colour_change / direct)

Question: গাড়ির রং পরিবর্তন করতে কী কী কাগজপত্র লাগবে?

Model: llama3.2; route: llm; time: 88.39 s; expected evidence present: True.

Answer:

গাড়ির রং পরিবর্তন করতে নিচে উল্লিখিত কাগজপত্রগুলো প্রয়োজন:

•   মালিকের স্বাক্ষর সম্বলিত আবেদন পত্র - 01 কপি
•   মূল নিবন্ধন সনদ (কাগজের নিবন্ধন সনদ হলে হোম কপিও জমা দিতে হবে)
•   ফি জমার রশিদের বিআরটিএ'র কপি
•   হালনাগাদ ফিটনেস সনদের ফটোকপি 01 কপি
•   হালনাগাদ ট্যাক্স টোকেনের ফটোকপি 01 কপি

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

Model: llama3.2; route: llm; time: 126.14 s; expected evidence present: True.

Answer:

এখানে উল্লিখিত চতুর্থ অধ্যায়ের ৫৩-৭৩ ধারা অনুযায়ী:

"৫৩(১) ট্রাফিক ও ওজনসীমা নিয়ন্ত্রণ— গতি সীমা দ্বারা আইনের শাসন হইতে পারিবে না।"

এছাড়া, এখানে উল্লিখিত ষষ্ঠ অধ্যায়ের ৪১| ধারা অনুযায়ী:

"৪১| ট্রাফিক নিয়ন্ত্রণ}   সরকার বা তৎকর্তৃক ক্ষমতাপ্রাপ্ত কোনো প্রতিষ্ঠান বা সংস্থা ট্রাফিক চলাচল নিয়ন্ত্রণ ও সড়ক নিরাপত্তা বিধানে মোটরযানের ব্যবহার, গতিসীমা, পার্কিং এলাকা, ট্রাফিক সাইন সংকেত ব্যবহার, চলাচল ইত্যাদি নির্ধারিত পদ্ধতিতে নিয়ন্ত্রণ করিতে পারিবে।"

অতঃপর, উভয় ধারার আলোচনা থেকে জেনে রাখা যায়:

*   গতি সীমা দ্বারা আইনের শাসন হওয়া উচিত।
*   ট্রাফিক চলাচল নিয়ন্ত্রণ ও সড়ক নিরাপত্তা বিধানে মোটরযানের ব্যবহার, গতিসীমা, পার্কিং এলাকা, ট্রাফিক সাইন সংকেত ব্যবহার, চলাচল ইত্যাদি নির্ধারিত পদ্ধতিতে নিয়ন্ত্রণ করা উচিত।

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

Model: llama3.2; route: llm; time: 68.82 s; expected evidence present: True.

Answer:

অনুমোদনের প্রথম ধাপ হচ্ছে ব্যাংকে মোটরযানের মডিফিকেশন (রং পরিবর্তন) ফি জমা দিতে।

1. আবেদনপত্র - মালিকের স্বাক্ষর সম্বলিত আবেদন পত্র
2. মূল নিবন্ধন সনদ - মূল নিবন্ধন সনদ 
3. ফি জমার রশিদ - রং পরিবর্তন ফি জমার রশিদের বিআরটিএ'র কপি

Sources: brta_a40ff0f214eb68b8_v2_0001, brta_a40ff0f214eb68b8_v2_0002, brta_e21467da1ba75db4_v2_0002

Retrieved sources:
- brta_a40ff0f214eb68b8_v2_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_v2_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_e21467da1ba75db4_v2_0002: fahim_brta/সেবাসমূহ/তথ্য সংশোধনপরিবর্তন.md
- brta_4b4c003681ae6872_v2_0002: fahim_brta/সেবাসমূহ/মোটরযানের নিবন্ধন.md
- brta_4e08eb4e988d38e4_v2_0039: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_29228d7f41bd4857_v2_0036: fahim_brta/ফরম/ফরম-১৭ মোটরযান রেজিস্ট্রেশনের আবেদন.md

## brta_fitness_direct (brta / fitness_renewal / direct)

Question: গাড়ির ফিটনেস সনদ নবায়ন কীভাবে করব?

Model: llama3.2; route: llm; time: 30.03 s; expected evidence present: True.

Answer:

অতিরিক্ত ফি 50% হারে জমা করুন।

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

Model: llama3.2; route: llm; time: 74.73 s; expected evidence present: True.

Answer:

*   এ্যাপয়েন্টমেন্ট গ্রহণের সময় স্বয়ংক্রিয়ভাবে পূরণকৃত সি.এফ.সি/সি.এফ.আর.এ ফরমে সেবাগ্রহণকারীর স্বাক্ষর;
*   প্রয়োজনীয় ফি জমার রশিদ;
*   হালনাগাদ ট্যাক্স টুকেন এর ফটোকপি; 
*   মোটরযানের অনুমিত/অগ্রিম আয়কর প্রদানের প্রমাণপত্র (অনুমিত/অগ্রিম আয়কর জমা দিতে TIN আবশ্যক);

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

Model: llama3.2; route: llm; time: 66.1 s; expected evidence present: True.

Answer:

1. এ্যাপয়েন্টমেন্ট গ্রহণের সময় স্বয়ংক্রিয়ভাবে পূরণকৃত সি.এফ.সি/সি.এফ.আর.এ ফরমে সেবাগ্রহণকারীর স্বাক্ষর;
2. প্রয়োজনীয় ফি জমার রশিদ; 
3. হালনাগাদ ট্যাক্স টুকেন এর ফটোকপি; 
4. মোটরযানের অনুমিত/অগ্রিম আয়কর প্রদানের প্রমাণপত্র (অনুমিত/অগ্রিম আয়কর জমা দিতে TIN আবশ্যক);

Sources: brta_d516e1b85b1f7144_v2_0001, brta_2dd33c08c48bf098_v2_0011, brta_09e8cbfff67f117e_v2_0020

Retrieved sources:
- brta_d516e1b85b1f7144_v2_0001: fahim_brta/সেবাসমূহ/ফিটনেস ইস্যু ও নবায়ন.md
- brta_2dd33c08c48bf098_v2_0011: brta/ফি, ট্যাক্স ও আয়কর/মোটরযানের অগ্রিম বা অনুমিত আয়কর ২০১৬-২০১৭ (মোটর কার, জীপ বা মাইক্রোবাস).md
- brta_09e8cbfff67f117e_v2_0020: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_4e08eb4e988d38e4_v2_0062: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0067: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_b2784bdfab996348_v2_0005: brta/আইন, বিধি ও নীতিমালা/এস,আর ও নং ১৬৫-আইন-আয়কর-২০২১.md

## passport_collect_direct (passport / passport_collection / direct)

Question: ই-পাসপোর্ট সংগ্রহ করতে অফিসে কী কী নিয়ে যেতে হবে?

Model: llama3.2; route: llm; time: 93.45 s; expected evidence present: False.

Answer:

ই-পাসপোর্ট সংগ্রহ করতে বলতে আপনার জন্য এখানে চারটি ধাপ:

*   প্রথমে আপনার অ্যাপ্লিকেশন সম্পূর্ণ করুন। 
*   দ্বিতীয়ে, আপনার পাসপোর্ট অফিসে উপস্থিত হয়ে ডেলিভারি স্লিপ ও NID কার্ড বা পূর্ববর্তী মূল পাসপোর্ট বহন করুন।
*   তৃতীয়ে, ই-পাসপোর্ট সংগ্রহের জন্য আপনার ডেলিভারি স্লিপ এবং নিদর্শন প্রদান করুন।
*   চতুর্থে, আপনার পাসপোর্ট সংগ্রহ করতে আপনার অ্যাপ্লিকেশন ফর্ম এবং উপস্থিত হয়ে আপনার পাসপোর্ট ও NID কার্ড বা পূর্ববর্তী মূল পাসপোর্ট বহন করুন।

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

Model: llama3.2; route: llm; time: 66.48 s; expected evidence present: True.

Answer:

নতুন পাসপোর্ট সংগ্রহের সময় ডেলিভারি স্লিপ, অভিভাবকের NID/পাসপোর্ট, আবেদনপত্রের সারংশের প্রিন্ট কপি, জাতীয় পরিচয় পত্র/ জন্ম নিবন্ধন নং-এর প্রিন্ট কপি, পেমেন্ট স্লিপ, পূর্ববর্তী পাসপোর্ট এবং ডাটা পেজের প্রিন্ট কপি (যদি থাকে), GO/NOC for government service holder (as applicable) এবং আবেদনপত্রের প্রিন্ট কপি অবশ্যই গ্রহণের সময় দেখানো উচিত।

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

Model: llama3.2; route: llm; time: 63.41 s; expected evidence present: True.

Answer:

এই ধরনের কাগজপত্র নিয়ে যাও:

1. আবেদনপত্রের সারংশের প্রিন্ট কপি (অ্যাপয়েন্টমেন্ট সহ)।
2. সনাক্তকরণ নথির প্রিন্ট কপি (জাতীয় পরিচয় পত্র/ জন্ম নিবন্ধন নং)।
3. পেমেন্ট স্লিপ (for Offline Payment only)
4. পূর্ববর্তী পাসপোর্ট এবং ডাটা পেজের প্রিন্ট কপি (যদি থাকে)।
5. সরকারি চাকরিজীবীদের ক্ষেত্রে GO/NOC (যদি থাকে)।
6. আবেদনপত্রের প্রিন্ট কপি।

Sources: passport_73ac41f2327257f9_v2_0001, passport_73ac41f2327257f9_v2_0004, passport_73ac41f2327257f9_v2_0002

Retrieved sources:
- passport_73ac41f2327257f9_v2_0001: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0004: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0002: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_73ac41f2327257f9_v2_0003: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_23d845d3ab38ea43_v2_0041: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0040: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_password_direct (passport / account_password_recovery / direct)

Question: অনলাইন পাসপোর্ট অ্যাকাউন্টের পাসওয়ার্ড ভুলে গেলে কী করতে হবে?

Model: llama3.2; route: llm; time: 56.66 s; expected evidence present: True.

Answer:

অনলাইন পাসপোর্ট অ্যাকাউন্টের পাসওয়ার্ড ভুলে গেলে, নিম্নলিখিত ধাপ অনুসরণ করুন:
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

Model: llama3.2; route: llm; time: 60.49 s; expected evidence present: True.

Answer:

আপনার ই-পাসপোর্টের জন্য পাসওয়ার্ড পুনরুদ্ধার করতে, নিম্নলিখিত পদক্ষেপ অনুসরণ করুন:

1. অ্যাকাউন্ট সাইন ইন অপশনে যান।
2. "Forgot password" লিঙ্কে ক্লিক করুন।
3. ই-মেইল অ্যাড্রেসে প্রবেশ করুন।
4. ই-মেইল অ্যাকাউন্টের রিকভারি মেসেজে দেওয়া নির্দেশনা অনুসরণ করুন।

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

Model: llama3.2; route: llm; time: 38.36 s; expected evidence present: True.

Answer:

অ্যাকাউন্ট সাইন ইন অপশনে যান।
"Forgot password" লিঙ্কে ক্লিক করুন।
ই-মেইল অ্যাড্রেসে প্রবেশ করুন।
ই-মেইল অ্যাকাউন্টের রিকভারি মেসেজে দেওয়া নির্দেশনা অনুসরণ করুন।

Sources: passport_23d845d3ab38ea43_v2_0004, passport_23d845d3ab38ea43_v2_0043, passport_23d845d3ab38ea43_v2_0038

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0004: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0043: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0038: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0007: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0005: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0015: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_regular_delivery_direct (passport / regular_delivery_time / direct)

Question: বায়োমেট্রিক দেওয়ার পর নিয়মিত ই-পাসপোর্ট সাধারণত কত সময়ের মধ্যে পাওয়া যায়?

Model: llama3.2; route: llm; time: 47.75 s; expected evidence present: True.

Answer:

আপনি বায়োমেট্রিক দেওয়ার পর নিয়মিত ই-পাসপোর্ট অর্জনের জন্য:

*   এখন থেকে, আপনি বায়োমেট্রিক দেওয়ার পর 15 কাজের দিন / 21 দিন ধরে ই-পাসপোর্ট পাওয়া যাচ্ছে।
*   উল্লেখযোগ্য ঘটনা হলে বা ভুল ফলাফল হলে আপনি শীঘ্রই সংশোধন পাবেন।

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

Model: llama3.2; route: llm; time: 55.6 s; expected evidence present: True.

Answer:

আপনার ই-পাসপোর্ট বিতরণের সময়সীমা হল ১৫ কর্মদিবস।

1. এখানে থেকে অনুরূপ উত্তর পাওয়া গেছে।
2. আপনার ই-পাসপোর্ট বিতরণের সময়সীমা জেনে নিন।

3. আপনি যদি ভূমিকা চান, তাহলে আপনাকে নিম্নলিখিত শপংশ অনুসরণ করতে হবে:
   * আপনার ডেটা সঠিক থাকা সাপেক্ষে 15 কর্মদিবসের মধ্যে ই-পাসপোর্ট বিতরণ করা হবে।

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

Model: llama3.2; route: llm; time: 49.07 s; expected evidence present: True.

Answer:

আপনি ই-পাসপোর্ট পাওয়ার উচিত কখন? 
1. আপনি বায়োমেট্রিক ডেলিভারি গ্রহণ করেছেন।
2. একজন সরকারি কর্মকর্তা (অনুমতি) থাকলে আপনি একটি স্পেশাল ডেলিভারি পাবেন।

3. আপনি 15 অক্টোবর, 2023 এর দিনে বায়োমেট্রিক ডেলিভারি গ্রহণ করেছেন।

Sources: passport_12e10027cfdfeeee_v2_0005, passport_09c70e4e1e93efad_v2_0006, passport_09c70e4e1e93efad_v2_0004

Retrieved sources:
- passport_12e10027cfdfeeee_v2_0005: cleaned_md/e-Passport Fees and Payment Options.md
- passport_09c70e4e1e93efad_v2_0006: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0004: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_09c70e4e1e93efad_v2_0002: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md
- passport_cd3935ff9dcc81c4_v2_0004: cleaned_md/বিশেষ নোটিশঃ নারায়ণগঞ্জ আঞ্চলিক পাসপোর্ট অফিসের কার্যক্রম পুনরায় শুরু প্রসঙ্গে.md
- passport_09c70e4e1e93efad_v2_0005: cleaned_md/Biometric_Enrolment_Citizens_Above_6_Years.md

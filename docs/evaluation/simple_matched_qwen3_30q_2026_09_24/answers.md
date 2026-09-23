# Matched Simple RAG / Qwen3 answers

Raw outputs; correctness review pending. Source IDs are supplied context, not verified citations.

## passport_01_documents

নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?

Route: llm_dense_evidence; time: 217.35 s

নতুন পাসপোর্ট সংগ্রহের জন্য নিচের কাগজপত্রগুলি দেখানো আবশ্যক:

- **ক.** ডেলিভারি স্লিপ (Delivery Slip)  
- **খ.** সন্তানের পাসপোর্ট হলে (১২ বছরের কম): অভিভাবকের NID/পাসপোর্ট  
- **গ.** প্রতিনিধি দিয়ে সংগ্রহ করতে চাইলে: আবেদনকারীর স্বাক্ষরযুক্ত অনুমোদনপত্র (Authorization Letter) এবং প্রতিনিধির NID  
- **ঘ.** পূর্বের মূল পাসপোর্ট (পুনর্জন্ম/পুনর্প্রস্থাপনের ক্ষেত্রে)

Sources: passport_23d845d3ab38ea43_v2_0040, passport_73ac41f2327257f9_v2_0004, passport_3fcbc40c98aa80bc_v2_0002, passport_73ac41f2327257f9_v2_0003, passport_ed7b3ebc56c0094f_v2_0003, passport_729010959c882773_v2_0004

Supplied evidence: passport_23d845d3ab38ea43_v2_0040, passport_73ac41f2327257f9_v2_0004, passport_3fcbc40c98aa80bc_v2_0002, passport_73ac41f2327257f9_v2_0003, passport_ed7b3ebc56c0094f_v2_0003, passport_729010959c882773_v2_0004

## passport_02_fee

পাসপোর্ট বানাতে কত টাকা লাগে?

Route: llm_dense_evidence; time: 229.83 s

আবেদনকারী ইলেকট্রনিক (e-Passport) পাসপোর্ট অর্জনের জন্য নিম্নলখিত দস্তাবেজগুলি উপস্থিত করতে হবে:

1. অনলাইনে/অফলাইনে পূরণকৃত আবেদন ফরম (ডি.আই.পি.-১) প্রিন্টেড কপি।  
2. পাসপোর্ট ফি জমা প্রদানের এ-চালান (Automated Challan) কপি।  
3. জাতীয় পরিচয়পত্র (NID - ২০ বছরের ঊর্ধ্বে) বা ডিজিটাল জন্ম নিবন্ধন সনদ (BRC - ১৮ বছরের নিম্নে)।  
4. বর্তমান ঠিকানা প্রমাণের স্বপক্ষে গ্যাস, বিদ্যুৎ, টেলিফোন, পানির বিলের কপি।  
5. অনাপত্তি সনদ (NOC/GO) ইস্যুকারী কর্তৃপক্ষের ওয়েবসাইটে আপলোড থাকা।  
6. পাসপোর্ট সাইজের ছবি (ল্যাব প্রিন্ট এবং রঙিন)।  
7. মেডিকেল সনদ (চোখের আইরিশ, ফিঙ্গারপ্রিন্ট মিসিং হবার ক্ষেত্রে)।  
8. ধূসর ব্যাকগ্রাউন্ডের 3R সাইজের ফটো (০৬ বছরের নিচে শিশুদের জন্য)।  
9. অপ্রাপ্ত বয়স্ক আবেদনকারীর ক্ষেত্রে পিতা/মাতার জাতীয় পরিচয়পত্রের কপি।

Sources: passport_6f7d900581956bef_v2_0016, passport_6f7d900581956bef_v2_0011, passport_ed7b3ebc56c0094f_v2_0003, passport_6f7d900581956bef_v2_0009, passport_6f7d900581956bef_v2_0006, passport_729010959c882773_v2_0003

Supplied evidence: passport_6f7d900581956bef_v2_0016, passport_6f7d900581956bef_v2_0011, passport_ed7b3ebc56c0094f_v2_0003, passport_6f7d900581956bef_v2_0009, passport_6f7d900581956bef_v2_0006, passport_729010959c882773_v2_0003

## passport_03_delivery_time

পাসপোর্ট পেতে কত দিন সময় লাগে?

Route: llm_dense_evidence; time: 129.13 s

পাসপোর্ট পেতে সময় এভাবে হতে পারে:

- **সাধারণ পাসপোর্ট:** ১৫ কর্মদিবস  
- **জরুরী পাসপোর্ট:** ৭ কর্মদিবস  
- **অতি জরুরী পাসপোর্ট (সুপার এক্সপ্রেস):** ২ কর্মদিবস

এগুলো তখন প্রয়োগ করা যাবে যখন অন্যান্য তথ্য সঠিক থাকবে।

Sources: passport_9f4e9ffe9f2a07f4_v2_0004, passport_6f7d900581956bef_v2_0031, passport_12e10027cfdfeeee_v2_0005, passport_6f7d900581956bef_v2_0011, passport_f2c0d221c70d21f2_v2_0003, passport_6f7d900581956bef_v2_0016

Supplied evidence: passport_9f4e9ffe9f2a07f4_v2_0004, passport_6f7d900581956bef_v2_0031, passport_12e10027cfdfeeee_v2_0005, passport_6f7d900581956bef_v2_0011, passport_f2c0d221c70d21f2_v2_0003, passport_6f7d900581956bef_v2_0016

## passport_04_apply

ই-পাসপোর্টের জন্য কীভাবে আবেদন করব?

Route: llm_dense_evidence; time: 217.96 s

ই-পাসপোর্ট আবেদন করতে নিচের ধাপগুলো অনুসরণ করুন:

1. [অনলাইনে আবেদন ফরমটি পূরণ করুন](https://passport.gov.bd)  
2. জাতীয় পরিচয়পত্র (NID) বা ডিজিটাল জন্ম নিবন্ধন সনদ (BRC) দখল করুন। ১৮ বছরের কম বয়সী হলে NID থাকলে এটি উল্লেখ করুন; যদি NID না থাকে, তবে পিতা/মাতার NID নম্বর দিন।
3. পাসপোর্ট ফি জমা দিতে এ-চালান কপি অনলাইনে প্রেরণ করুন।
4. আবেদন জমা দেওয়ার পর পাসপোর্ট অফিসে গেলে আপনার MRP, NID/BRC ও অন্যান্য প্রয়োজনীয় কাগজপত্রগুলো সঙ্গে নিয়ে আসুন।

Sources: passport_9f4e9ffe9f2a07f4_v2_0002, passport_6f7d900581956bef_v2_0006, passport_0b74faa4d85a2a58_v2_0003, passport_23d845d3ab38ea43_v2_0024, passport_6e87d0783a373593_v2_0005, passport_6f7d900581956bef_v2_0007

Supplied evidence: passport_9f4e9ffe9f2a07f4_v2_0002, passport_6f7d900581956bef_v2_0006, passport_0b74faa4d85a2a58_v2_0003, passport_23d845d3ab38ea43_v2_0024, passport_6e87d0783a373593_v2_0005, passport_6f7d900581956bef_v2_0007

## passport_05_renewal

পাসপোর্টের মেয়াদ শেষ হলে কীভাবে নবায়ন করব?

Route: llm_dense_evidence; time: 187.9 s

পাসপোর্টের মেয়াদ শেষ হলে নবায়ন করতে হবে এমআরপি ফরম পূরণ করে।  
- বর্তমান পাসপোর্টের ফটোকপি ও ব্যাংকে টাকা জমার রশিদ অবশ্যই সঙ্গে নিয়ে আসতে হবে।  
- মূল পাসপোর্টটি অবশ্যই সঙ্গে থাকতে হবে।  
- পাসপোর্ট রি-ইস্যু বা নবায়নের ক্ষেত্রে শুধুমাত্র বাংলাদেশ সরকার কর্তৃক নির্ধারিত নিয়মিত ফি প্রদান করতে হবে।

Sources: passport_3fcbc40c98aa80bc_v2_0002, passport_23d845d3ab38ea43_v2_0017, passport_9f4e9ffe9f2a07f4_v2_0003, passport_3fcbc40c98aa80bc_v2_0009, passport_ed7b3ebc56c0094f_v2_0003, passport_3fcbc40c98aa80bc_v2_0006

Supplied evidence: passport_3fcbc40c98aa80bc_v2_0002, passport_23d845d3ab38ea43_v2_0017, passport_9f4e9ffe9f2a07f4_v2_0003, passport_3fcbc40c98aa80bc_v2_0009, passport_ed7b3ebc56c0094f_v2_0003, passport_3fcbc40c98aa80bc_v2_0006

## passport_06_lost

পাসপোর্ট হারিয়ে গেলে কী করতে হবে?

Route: llm_dense_evidence; time: 236.55 s

পাসপোর্ট হারিয়ে গেলে নিম্নে করণীয়গুলো পালন করুন:

১. নিকটস্থ থানায় **জিডি** (General Diary) রিপোর্ট দাখিল করুন।  
২. আবেদনকালে অনলাইন ফরমে **DUPLICATE** এপ্লিকেশন টাইপ চয়ন করুন।  
৩. হারিয়েছে পাসপোর্টের নম্বর প্রতিষ্ঠাপন করুন।  
৪. জিডি কপি ও হারিয়েছে পাসপোর্টের ফটোকপি সহ আবেদনপত্র জমা দিন।

অফিসে গেলে মূল NID কার্ড, প্রিন্ট সামারি/অ্যাপয়েন্টমেন্ট কপি এবং ডেলিভারি স্লিপের ফটোকপি (যদি থাকে) প্রদর্শন করুন।

Sources: passport_23d845d3ab38ea43_v2_0041, passport_5eb6c21efe103a4f_v2_0034, passport_9f4e9ffe9f2a07f4_v2_0005, passport_ed7b3ebc56c0094f_v2_0004, passport_3fcbc40c98aa80bc_v2_0002, passport_6f7d900581956bef_v2_0006

Supplied evidence: passport_23d845d3ab38ea43_v2_0041, passport_5eb6c21efe103a4f_v2_0034, passport_9f4e9ffe9f2a07f4_v2_0005, passport_ed7b3ebc56c0094f_v2_0004, passport_3fcbc40c98aa80bc_v2_0002, passport_6f7d900581956bef_v2_0006

## passport_07_name_correction

পাসপোর্টে নাম ভুল থাকলে কীভাবে ঠিক করব?

Route: llm_dense_evidence; time: 139.49 s

পাসপোর্টে নাম ভুল থাকলে ঠিক করতে হলে—  
- **প্রিন্টকৃত 'Application Summary'** নিয়ে আপনার নির্ধারিত পাসপোর্ট অফিসে গেলে এনরোলমেন্ট অফিসার আপনার আবেদনটি দেখে ভুল তথ্য সংশোধন করে দেবেন।  
- তথ্য প্রমাণের জন্য **NID**, **BRC**, বা অন্যান্য প্রয়োজনীয় সরকারি দলিলগুলো সাথে নিয়ে যাওয়া উচিত।

Sources: passport_5eb6c21efe103a4f_v2_0033, passport_23d845d3ab38ea43_v2_0021, passport_23d845d3ab38ea43_v2_0042, passport_3fcbc40c98aa80bc_v2_0005, passport_3fcbc40c98aa80bc_v2_0004, passport_23d845d3ab38ea43_v2_0019

Supplied evidence: passport_5eb6c21efe103a4f_v2_0033, passport_23d845d3ab38ea43_v2_0021, passport_23d845d3ab38ea43_v2_0042, passport_3fcbc40c98aa80bc_v2_0005, passport_3fcbc40c98aa80bc_v2_0004, passport_23d845d3ab38ea43_v2_0019

## passport_08_birth_date

পাসপোর্টে জন্মতারিখ পরিবর্তন করা যায় কি?

Route: llm_dense_evidence; time: 135.92 s

পাসপোর্টে জন্মতারিখ পরিবর্তন করা যায় না। আবেদন করার সময় জন্মতারিখ আগের পাসপোর্টের সাথে মেলে থাকতে হবে। যদি জন্মতারিখ পরিবর্তন হয়, তখন আগের পাসপোর্টটি প্রমাণ করতে হবে এবং অফিশিয়াল দলিল (এনআইডি/বিআরসি) জমা দিতে হবে।

Sources: passport_3fcbc40c98aa80bc_v2_0007, passport_23d845d3ab38ea43_v2_0019, passport_5eb6c21efe103a4f_v2_0033, passport_3fcbc40c98aa80bc_v2_0005, passport_3fcbc40c98aa80bc_v2_0004, passport_3fcbc40c98aa80bc_v2_0002

Supplied evidence: passport_3fcbc40c98aa80bc_v2_0007, passport_23d845d3ab38ea43_v2_0019, passport_5eb6c21efe103a4f_v2_0033, passport_3fcbc40c98aa80bc_v2_0005, passport_3fcbc40c98aa80bc_v2_0004, passport_3fcbc40c98aa80bc_v2_0002

## passport_09_status

পাসপোর্টের আবেদন করার পর status কীভাবে দেখব?

Route: llm_dense_evidence; time: 179.96 s

আপনি আবেদন করার পর পাসপোর্টের status দেখতে হলে নিচের ধাপগুলো অনুসরণ করুন:

- [https://www.epassport.gov.bd/authorization/application-status](https://www.epassport.gov.bd/authorization/application-status) লিংকটি খুন এবং ই-পাসপোর্ট পোর্টালে **'স্ট্যাটাস চেক'** মেন্যুতে গেছুন।  
- Application ID বা Online Registration ID (OID) ও আবেদনকারীর জন্ম তারিখ ভরান।  
- "Search" বাটন চাপুন।

যদি কোনও তথ্য প্রদান করার পরও সমস্যা থাকে, তবে ব্রাউজারের Cache এবং Cookies ক্লিয়ার করুন অথবা Incognito/Private মোডে পুনরায় চেক করুন।

Sources: passport_23d845d3ab38ea43_v2_0038, passport_23d845d3ab38ea43_v2_0047, passport_23d845d3ab38ea43_v2_0044, passport_23d845d3ab38ea43_v2_0043, passport_6f7d900581956bef_v2_0012, passport_729010959c882773_v2_0004

Supplied evidence: passport_23d845d3ab38ea43_v2_0038, passport_23d845d3ab38ea43_v2_0047, passport_23d845d3ab38ea43_v2_0044, passport_23d845d3ab38ea43_v2_0043, passport_6f7d900581956bef_v2_0012, passport_729010959c882773_v2_0004

## passport_10_urgent

জরুরি পাসপোর্ট করতে কত দিন লাগে?

Route: llm_dense_evidence; time: 89.11 s

জরুরী পাসপোর্ট করতে ২ কর্মদিবসের মধ্যে পাসপোর্ট প্রদান হয়।

Sources: passport_9f4e9ffe9f2a07f4_v2_0004, passport_f2c0d221c70d21f2_v2_0003, passport_12e10027cfdfeeee_v2_0005, passport_6f7d900581956bef_v2_0011, passport_6f7d900581956bef_v2_0031, passport_6f7d900581956bef_v2_0015

Supplied evidence: passport_9f4e9ffe9f2a07f4_v2_0004, passport_f2c0d221c70d21f2_v2_0003, passport_12e10027cfdfeeee_v2_0005, passport_6f7d900581956bef_v2_0011, passport_6f7d900581956bef_v2_0031, passport_6f7d900581956bef_v2_0015

## birth_01_documents

জন্মনিবন্ধন করতে কী কী কাগজপত্র লাগে?

Route: llm_dense_evidence; time: 169.05 s

জন্মনিবন্ধন করতে নিচের কাগজপত্রগুলি দরকার:
- জন্মস্থান ও জন্ম তারিখের প্রমাণ (ছাড়পত্র/জন্ম সংক্রান্ত সনদের অনুলিপি বা বার্থ এটেন্ডেন্টের প্রত্যয়ন)
- স্থায়ী ঠিকানার প্রমাণ (হালনাগাদ কর পরিশোধের প্রমাণপত্র বা জাতীয় পরিচয়পত্রে ঘোষিত স্থায়ী ঠিকানা)  
- পিতা ও মাতার জন্ম নিবন্ধন সনদ (বিশেষ করে ২০১৩ সালের পর জন্মগ্রহণকারী ব্যক্তির ক্ষেত্রে)

Sources: birth_and_death_registration_rules_2018_বিধি_৯_02, bdris_faq_02_preamble, bdris_faq_01_q01, birth_registration_application_process_cleaned_016_01, birth_registration_application_process_cleaned_004_01, birth_registration_application_process_02_cleaned_010_01

Supplied evidence: birth_and_death_registration_rules_2018_বিধি_৯_02, bdris_faq_02_preamble, bdris_faq_01_q01, birth_registration_application_process_cleaned_016_01, birth_registration_application_process_cleaned_004_01, birth_registration_application_process_02_cleaned_010_01

## birth_02_online_apply

জন্মনিবন্ধন অনলাইনে কীভাবে করব?

Route: llm_dense_evidence; time: 170.52 s

জন্মনিবন্ধন অনলাইনে করতে হলে নিচের ধাপগুলি অনুসরণ করুন:

- **ধাপ ১:** [https://bdris.gov.bd](https://bdris.gov.bd) ওয়েবসাইটে ভিজিট করুন।  
- **ধাপ ২:** "জন্ম তথ্য যাচাই" অপশনে প্রবেশ করুন।  
- **ধাপ ৩:** ব্যক্তির জন্ম নিবন্ধন নম্বর এবং জন্ম তারিখ দিয়ে তথ্য প্রদান করুন।  
- **ধাপ ৪:** সফলভাবে জন্ম নিবন্ধন হওয়া নিশ্চিত করুন।

Sources: bdris_faq_01_q02, know_this_01_cleaned_008_01, birth_and_death_registration_rules_2018_বিধি_২০_01, birth_and_death_registration_rules_2018_বিধি_১৯_03, birth_registration_application_process_02_cleaned_003_01, birth_and_death_registration_rules_2018_বিধি_১৯_02

Supplied evidence: bdris_faq_01_q02, know_this_01_cleaned_008_01, birth_and_death_registration_rules_2018_বিধি_২০_01, birth_and_death_registration_rules_2018_বিধি_১৯_03, birth_registration_application_process_02_cleaned_003_01, birth_and_death_registration_rules_2018_বিধি_১৯_02

## birth_03_birth_date_correction

জন্মনিবন্ধনে জন্মতারিখ ভুল হলে কীভাবে সংশোধন করব?

Route: llm_dense_evidence; time: 135.04 s

জন্ম নিবন্ধনে জন্ম তারিখ ভুল হলে সংশোধন করতে হলে নিচগুলো করুন:

- আপনার জন্ম নিবন্ধন ফরমটি পুনরায় দাখিল করুন।  
- জন্ম তারিখ সঠিকভাবে পুনরায় লিখুন।  
- আবেদন করার সময় অবশ্যই পিতা/মাতার জন্ম নিবন্ধন নম্বর উল্লেখ করুন (যদি থাকে)।  
- জন্ম নিবন্ধন সনদ পুনর্মুদ্রণ করলে সংশোধিত তথ্য দেখা যাবে।

অতিরিক্ত প্রমাণক হিসেবে পিতা/মাতার পাসপোর্ট কপি দেওয়া চাই, যদি জাতীয়তা ভুল হয়।

Sources: application_for_birth_information_correction_cleaned_006_01, application_for_birth_information_correction_cleaned_008_01, application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_003_01, application_for_birth_information_correction_cleaned_004_01, notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01

Supplied evidence: application_for_birth_information_correction_cleaned_006_01, application_for_birth_information_correction_cleaned_008_01, application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_003_01, application_for_birth_information_correction_cleaned_004_01, notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01

## birth_04_name_spelling

জন্মনিবন্ধনে নামের বানান ভুল হলে কী করব?

Route: llm_dense_evidence; time: 150.59 s

জন্মনিবন্ধনে নামের বানান ভুল হলে নিচের পদক্ষেপগুলি অনুসরণ করুন:

- পিতা বা মাতার জন্ম নিবন্ধন নম্বর থাকলে এটি ব্যবহার করে জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করুন।  
- পিতা বা মাতার নাম সংশোধন করতে উপযুক্ত প্রমাণক (যেমন পাসপোর্ট) দখল করুন।  
- জন্ম নিবন্ধন সনদ পুনর্মুদ্রণ করলে সংশোধিত নাম স্বয়ংক্রিয়ভাবে প্রদর্শিত হবে।

অগ্রসর হওয়ার আগে, অবশ্যই পিতা/মাতার জন্ম নিবন্ধন নম্বর এবং জন্ম তারিখ চেক করুন।

Sources: application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_002_01, application_for_birth_information_correction_cleaned_004_01, application_for_birth_information_correction_cleaned_003_01, notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01, application_for_birth_information_correction_cleaned_006_01

Supplied evidence: application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_002_01, application_for_birth_information_correction_cleaned_004_01, application_for_birth_information_correction_cleaned_003_01, notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01, application_for_birth_information_correction_cleaned_006_01

## birth_05_lost

জন্মনিবন্ধন হারিয়ে গেলে নতুন কপি কীভাবে পাব?

Route: llm_dense_evidence; time: 200.99 s

জন্মনিবন্ধন হারিয়ে গেলে নতুন কপি পেতে হলে নিচের পদক্ষেপগুলো অনুসরণ করুন:

- জমনি ফরম-৭ অনুযায়ী আবেদনপত্র দাখিল করুন।  
- আবেদনপত্রে আপনার বা আপনার সন্তানের তথ্য এবং জন্ম তথ্য উল্লেখ করুন।  
- আবেদনপত্রে ফিস সহ সঠিকভাবে পূরণ করুন।  
- ৭ কার্য দিবসের মধ্যে আবেদনপত্র দাখিল করুন।  
- আবেদনপত্র গ্রহণ করার পর, নিবন্ধক আপনার জন্ম নিবন্ধন সনদের প্রতিলিপি প্রদান করবেন।

Sources: birth_and_death_registration_rules_2018_বিধি_১৩_01, bdris_faq_02_q08, birth_and_death_registration_rules_2018_বিধি_১২_01, bdris_faq_01_q10, bdris_faq_01_q12, birth_and_death_registration_rules_2018_বিধি_১২_02

Supplied evidence: birth_and_death_registration_rules_2018_বিধি_১৩_01, bdris_faq_02_q08, birth_and_death_registration_rules_2018_বিধি_১২_01, bdris_faq_01_q10, bdris_faq_01_q12, birth_and_death_registration_rules_2018_বিধি_১২_02

## birth_06_verify

অনলাইনে জন্মনিবন্ধন যাচাই কীভাবে করব?

Route: llm_dense_evidence; time: 162.05 s

অনলাইনে জন্মনিবন্ধন যাচাই করতে হলে নিচের পদক্ষেপগুলো অনুসরণ করুন:

- **orgbdr.gov.bd** ওয়েবসাইটে ভ্রমণ করুন।  
- "জন্ম তথ্য যাচাই" অপশনটি খুঁড়ে ফাংশনটি সক্রিয় করুন।  
- ব্যক্তির জন্ম নিবন্ধন নম্বর এবং জন্ম তারিখ দিন।  
- আপনার জন্ম নিবন্ধন হয়েছে কিনা তা প্রদর্শিত হবে।

Sources: know_this_01_cleaned_008_01, birth_and_death_registration_rules_2018_বিধি_২০_01, birth_registration_application_process_cleaned_012_01, birth_and_death_registration_rules_2018_বিধি_৯_04, bdris_faq_01_q02, birth_and_death_registration_rules_2018_বিধি_১৯_03

Supplied evidence: know_this_01_cleaned_008_01, birth_and_death_registration_rules_2018_বিধি_২০_01, birth_registration_application_process_cleaned_012_01, birth_and_death_registration_rules_2018_বিধি_৯_04, bdris_faq_01_q02, birth_and_death_registration_rules_2018_বিধি_১৯_03

## birth_07_correction_fee

জন্মনিবন্ধন সংশোধন করতে কত টাকা লাগে?

Route: llm_dense_evidence; time: 88.05 s

জন্মতারিখ সংশোধনের জন্য ১০০ টাকা ফি লাগে।

Sources: birth_and_death_registration_fees_cleaned_fee_row_04, birth_and_death_registration_fees_cleaned_table_full, birth_and_death_registration_fees_cleaned_fee_row_05, birth_and_death_registration_rules_2018_বিধি_২১_01, bdris_faq_02_preamble, birth_and_death_registration_act_2004_ধারা_২১_01

Supplied evidence: birth_and_death_registration_fees_cleaned_fee_row_04, birth_and_death_registration_fees_cleaned_table_full, birth_and_death_registration_fees_cleaned_fee_row_05, birth_and_death_registration_rules_2018_বিধি_২১_01, bdris_faq_02_preamble, birth_and_death_registration_act_2004_ধারা_২১_01

## birth_08_birth_date_proof

জন্মতারিখ সংশোধনের জন্য কী কী প্রমাণ লাগবে?

Route: llm_dense_evidence; time: 109.12 s

জন্মতারিখ সংশোধনের জন্য প্রমাণ হল:

- পিতা বা মাতার জন্ম নিবন্ধন নম্বর (যদি থাকে)
- পিতা বা মাতার মৃত্যুর প্রমাণপত্র (যদি পিতা/মাতা মৃত হন)  
- আপনার জন্ম নিবন্ধন নম্বর

অতিরিক্তভাবে, যদি আপনার জন্ম তারিখ ০১/০১/২০০১-এর পূর্বে হয়, তবে পিতা বা মাতার নাম সংশোধনের জন্য এই প্রমাণগুলো প্রয়োজন।

Sources: application_for_birth_information_correction_cleaned_006_01, application_for_birth_information_correction_cleaned_008_01, application_for_birth_information_correction_cleaned_009_01, application_for_birth_information_correction_cleaned_003_01, application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_004_01

Supplied evidence: application_for_birth_information_correction_cleaned_006_01, application_for_birth_information_correction_cleaned_008_01, application_for_birth_information_correction_cleaned_009_01, application_for_birth_information_correction_cleaned_003_01, application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_004_01

## birth_09_parent_name

বাবা-মায়ের নাম ভুল থাকলে কীভাবে সংশোধন করব?

Route: llm_dense_evidence; time: 182.16 s

আপনি বাবা-মায়ের নাম ভুল থাকলে নিচের পদক্ষেপগুলো অনুসরণ করুন:

- **পরিস্থিতি ১:** যদি বাবা বা মায়ের জন্ম নিবন্ধন নম্বর আছে, তাহলে প্রথমে তাদের জন্ম নিবন্ধন নম্বর ব্যবহার করে জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করুন।  
- **পরিস্থিতি ২:** যদি বাবা বা মায়ের জন্ম নিবন্ধন নম্বর না থাকে এবং আপনার জন্ম তারিখ ০১/০১/২০০১-এর পূর্বে হয়, তখন জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করতে হবে।
- **পরিস্থিতি ৩:** যদি বাবা বা মায়ের জন্ম নিবন্ধন নম্বর না থাকে, তারা মৃত হন এবং আপনার জন্ম তারিখ ০১/০১/২০০১-এর পরে হয়, তখনও জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করতে হবে।  
- আবেদন করার পর জন্ম নিবন্ধন সনদ পুনর্মুদ্রণ করলে সংশোধিত নাম প্রদর্শিত হবে।

Sources: application_for_birth_information_correction_cleaned_002_01, application_for_birth_information_correction_cleaned_003_01, application_for_birth_information_correction_cleaned_006_01, application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_004_01, application_for_birth_information_correction_cleaned_008_01

Supplied evidence: application_for_birth_information_correction_cleaned_002_01, application_for_birth_information_correction_cleaned_003_01, application_for_birth_information_correction_cleaned_006_01, application_for_birth_information_correction_cleaned_005_01, application_for_birth_information_correction_cleaned_004_01, application_for_birth_information_correction_cleaned_008_01

## birth_10_delivery_time

জন্মনিবন্ধন করতে কত দিন সময় লাগে?

Route: llm_dense_evidence; time: 175.81 s

জন্মনিবন্ধন করতে আবেদনকারী ব্যক্তির জন্মের ৪৫ দিনের মধ্যে অবশ্যই নিবন্ধন করা উচিত। এছাড়াও, নিবন্ধক জন্ম নিবন্ধন আবেদনপত্রটি পরীক্ষা করিয়া সর্বোচ্চ ৫ (পাঁচ) কার্য দিবসের মধ্যে জন্ম নিবন্ধন সম্পন্ন করিবেন।

Sources: birth_and_death_registration_rules_2018_বিধি_৯_02, bdris_faq_01_q01, birth_and_death_registration_rules_2018_বিধি_৯_04, bdris_faq_02_q01, birth_and_death_registration_rules_2018_বিধি_৯_03, birth_and_death_registration_act_2004_ধারা_৮_01

Supplied evidence: birth_and_death_registration_rules_2018_বিধি_৯_02, bdris_faq_01_q01, birth_and_death_registration_rules_2018_বিধি_৯_04, bdris_faq_02_q01, birth_and_death_registration_rules_2018_বিধি_৯_03, birth_and_death_registration_act_2004_ধারা_৮_01

## brta_01_documents

ড্রাইভিং লাইসেন্স করতে কী কী কাগজপত্র লাগবে?

Route: llm_dense_evidence; time: 319.91 s

ড্রাইভিং লাইসেন্স করতে নিম্নলিখিত কাগজপত্র দরকার:

* **আবেদনপত্র:** নির্ধারিত ফরমে আবেদন।  
* **ছবি:** পাসপোর্ট সাইজের ১-২ কপি ছবি (সদ্য তোলা)।  
* **মেডিকেল সার্টিফিকেট:** রেজিষ্টার্ড ডাক্তার কর্তৃক জারি হওয়া মেডিকেল সার্টিফিকেট (সর্বোচ্চ ৬০০ কে.বি)।  
* **পরিচয়পত্র:** জাতীয় পরিচয়পত্রের স্ক্যান কপি (সর্বোচ্চ ৬০০ কে.বি)।  
* **ইউটিলিটি বিল:** আবেদনকারীর ঠিকানার ইউটিলিটি বিলের স্ক্যান কপি (আবেদনকারীর ঠিকানা এবং জাতীয় পরিচয়পত্রের ঠিকানা ভিন্ন হলে বর্তমান ঠিকানার ইউটিলিটি বিল উপস্থাপন করতে হবে)।  
* **বর্তমান ড্রাইভিং লাইসেন্স:** বর্তমান ড্রাইভিং লাইসেন্সের স্ক্যান কপি (যদি অস্তিত্বে থাকে)।  
* **ফি জমাদানের রশিদ:** নির্ধারিত ফি বিআরটিএ'র নির্ধারিত ব্যাংকে জমাদানের রশিদ।  
* **জিডি ও ট্রাফিক ক্লিয়ারেন্স:** (ডুপ্লিকেট লাইসেন্সের ক্ষেত্রে)।

**লক্ষণীয়:** সকল প্রমাণপত্র স্ক্যান কপি হিসাবে উপস্থাপন করতে হবে, ভুয়া তথ্য দেওয়া হলে আইনানুগ ব্যবস্থা গ্রহণ করা হবে।

Sources: brta_cbe22ab64acf3d03_v2_0004, brta_cbe22ab64acf3d03_v2_0006, brta_cbe22ab64acf3d03_v2_0013, brta_cbe22ab64acf3d03_v2_0011, brta_4b8c25d391e48121_v2_0003, brta_4b8c25d391e48121_v2_0004

Supplied evidence: brta_cbe22ab64acf3d03_v2_0004, brta_cbe22ab64acf3d03_v2_0006, brta_cbe22ab64acf3d03_v2_0013, brta_cbe22ab64acf3d03_v2_0011, brta_4b8c25d391e48121_v2_0003, brta_4b8c25d391e48121_v2_0004

## brta_02_fee

ড্রাইভিং লাইসেন্স করতে মোট কত টাকা লাগে?

Route: llm_dense_evidence; time: 135.98 s

ড্রাইভিং লাইসেন্স করতে নিম্নলিখিত অর্থ প্রয়োজন:

- **শিক্ষানবিশ ড্রাইভিং লাইসেন্স ফি (মেয়াদ ০৬ মাস):** ২৫০ টাকা  
- **ড্রাইভিং লাইসেন্স দক্ষতা যাচাই ফি:** ৪০০ টাকা  
- **ভ্যাট (১৫%):** ৯৮ টাকা  
- **সর্বমোট:** ৭৪৮ টাকা

আপনি এই ফি দিয়ে দুই শ্রেণীর মোটরযানের জন্য ড্রাইভিং লাইসেন্স পেতে পারেন।

Sources: brta_3cae1ecd59682fa3_v2_0005, brta_3cae1ecd59682fa3_v2_0017, brta_3cae1ecd59682fa3_v2_0004, brta_3cae1ecd59682fa3_v2_0014, brta_3cae1ecd59682fa3_v2_0018, brta_3cae1ecd59682fa3_v2_0008

Supplied evidence: brta_3cae1ecd59682fa3_v2_0005, brta_3cae1ecd59682fa3_v2_0017, brta_3cae1ecd59682fa3_v2_0004, brta_3cae1ecd59682fa3_v2_0014, brta_3cae1ecd59682fa3_v2_0018, brta_3cae1ecd59682fa3_v2_0008

## brta_03_learner

লার্নার ড্রাইভিং লাইসেন্স কীভাবে করব?

Route: llm_dense_evidence; time: 260.61 s

লার্নার ড্রাইভিং লাইসেন্স অর্জনের পদক্ষেপগুলো নিচের মতো:

- আপনি `bsp.brta.gov.bd` এর মাধ্যমে অনলাইনে আবেদন করুন। আবেদন করতে আপনার জাতীয় পরিচয়পত্র (NID), ছবি, মেডিকেল সার্টিফিকেট, ইউটিলিটি বিল ও শিক্ষাগত যোগ্যতা দরকার।  
- আবেদন করার পর আপনার লার্নার ড্রাইভিং লাইসেন্স অনলাইনে প্রিন্ট করে নিন।  
- ২/৩ মাস প্রশিক্ষণ গ্রহণ করার পর নির্ধারিত তারিখ এবং সময়ে নির্ধারিত কেন্দ্রে লিখিত, মৌখিক ও ফিল্ড টেস্ট দিন।  
- টেস্টে উত্তীর্ণ হওয়ার পর আপনার স্থায়ী ড্রাইভিং লাইসেন্স পেতে হবে।

Sources: brta_cbe22ab64acf3d03_v2_0003, brta_cbe22ab64acf3d03_v2_0004, brta_846a4041fe96a64e_v2_0011, brta_09e8cbfff67f117e_v2_0005, brta_846a4041fe96a64e_v2_0007, brta_846a4041fe96a64e_v2_0002

Supplied evidence: brta_cbe22ab64acf3d03_v2_0003, brta_cbe22ab64acf3d03_v2_0004, brta_846a4041fe96a64e_v2_0011, brta_09e8cbfff67f117e_v2_0005, brta_846a4041fe96a64e_v2_0007, brta_846a4041fe96a64e_v2_0002

## brta_04_delivery_time

ড্রাইভিং লাইসেন্স পেতে কত দিন সময় লাগে?

Route: llm_dense_evidence; time: 173.12 s

শিক্ষানবিশ ড্রাইভিং লাইসেন্স আবেদন করার পর থেকে ৩ কার্যদিবসের মধ্যে লাইসেন্সটি প্রদান করা হয়। এছাড়াও, অনলাইন আবেদনের ক্ষেত্রে আবেদনকারী তার লাইসেন্সটি সিস্টেম থেকেই প্রিন্ট করে নিতে পারেন।

Sources: brta_4e08eb4e988d38e4_v2_0009, brta_cbe22ab64acf3d03_v2_0003, brta_cbe22ab64acf3d03_v2_0007, brta_846a4041fe96a64e_v2_0002, brta_4e08eb4e988d38e4_v2_0013, brta_846a4041fe96a64e_v2_0016

Supplied evidence: brta_4e08eb4e988d38e4_v2_0009, brta_cbe22ab64acf3d03_v2_0003, brta_cbe22ab64acf3d03_v2_0007, brta_846a4041fe96a64e_v2_0002, brta_4e08eb4e988d38e4_v2_0013, brta_846a4041fe96a64e_v2_0016

## brta_05_test

BRTA-এর ড্রাইভিং পরীক্ষায় কী কী থাকে?

Route: llm_dense_evidence; time: 312.24 s

BRTA-এর ড্রাইভিং পরীক্ষায় নিমন্টে বিষয়গুলি উপস্থাপিত হয়:

- মোটরযান চালকদের কর্ম ঘণ্টা  
- মোটরযান চালনার নিয়মাবলি এবং সিগন্যাল প্রদান  
- পাবলিক সার্ভিস মোটরযান চালকদের দাযিত্ব ও কর্তব্য  
- ট্রাফিক রুলস এবং রেগুলেশনের জ্ঞান, মোটরযানের লাইট ব্যবহার, পার্কিং, জরুরি পরিস্থিতিতে মোটরযান থামানো, সড়কের অধিকার, পথচারী পারাপার, লাইট সিগন্যাল, ওয়ানওয়ে ট্রাফিক, লেইন ডিসিপ্লিন, রাতে মোটরযান চালনা  
- ট্রাফিক সাইন, সিগন্যাল ও রোড মার্কিং সংক্রান্ত জ্ঞান  
- পেশাদার চালকদের জন্য আরও বিষয়গুলি: মোটরযানের শক্তি এবং ভার (GVW), মোটরযান চালনার উপযুক্ততা, মোটরযান চালনার অভ্যস্ততা, মোটরযান চালনার সময় ধরণ, মোটরযান চালনার সহজতা, মোটরযান চালনার স্থান এবং সময় নির্ণয়, মোটরযান চালনার সম্পর্কিত ঘটনা ও সমাধান।

Sources: brta_4e08eb4e988d38e4_v2_0158, brta_57a7e75567f9a5c3_v2_0010, brta_4e08eb4e988d38e4_v2_0196, brta_57a7e75567f9a5c3_v2_0012, brta_57a7e75567f9a5c3_v2_0001, brta_4e08eb4e988d38e4_v2_0207

Supplied evidence: brta_4e08eb4e988d38e4_v2_0158, brta_57a7e75567f9a5c3_v2_0010, brta_4e08eb4e988d38e4_v2_0196, brta_57a7e75567f9a5c3_v2_0012, brta_57a7e75567f9a5c3_v2_0001, brta_4e08eb4e988d38e4_v2_0207

## brta_06_renewal

ড্রাইভিং লাইসেন্সের মেয়াদ শেষ হলে কীভাবে নবায়ন করব?

Route: llm_dense_evidence; time: 335.42 s

ড্রাইভিং লাইসেন্সের মেয়াদ শেষ হলে নবায়ন করতে হবে নিচোকে বিবরণগুলি অনুসরণ করুন:

- **ফি জমা দিন:**  
  - মেয়াদোত্তীর্ণের ১৫ দিনের মধ্যে আবেদন করলে ৪,২১২/- টাকা (অপেশাদার) বা ২,৪৮৭/- টাকা (পেশাদার)।  
  - মেয়াদোত্তীর্ণের ১৫ দিন পরে প্রতি বছর ৫১৮/- টাকা বিলম্ব ফি দিতে হবে।

- **আবেদন করুন:**  
  - বিআরটিএ সার্ভিস পোর্টালে অনলাইনে আবেদন করতে পারেন (সার্ভিস পোর্টালে অ্যাকাউন্ট থাকলে)।  
  - বা বিআরটিএ সার্কেল অফিসে গেলে আবেদন করতে হবে।

- **প্রয়োজনীয় কাগজপত্র:**  
  - জাতীয় পরিচয়পত্রের ফটোকপি, পূর্বের ড্রাইভিং লাইসেন্সের ফটোকপি, মেডিকেল সার্টিফিকেট, ডোপ টেস্ট রিপোর্ট।

- **বায়োমেট্রিক্স নথিভুক্ত করুন:**  
  - ডিজিটাল ছবি, ডিজিটাল স্বাক্ষর ও আঙ্গুলের ছাপ দিতে হবে (অফিসে উপস্থিত হওয়া প্রয়োজন)।

- **ই-ড্রাইভিং লাইসেন্স অর্জন:**  
  - ফি প্রদান করার পর এসএমএস মাধ্যমে ই-ড্রাইভিং লাইসেন্স পেতে হবে।

Sources: brta_cbe22ab64acf3d03_v2_0009, brta_09e8cbfff67f117e_v2_0009, brta_cbe22ab64acf3d03_v2_0011, brta_09e8cbfff67f117e_v2_0011, brta_4e08eb4e988d38e4_v2_0014, brta_cbe22ab64acf3d03_v2_0010

Supplied evidence: brta_cbe22ab64acf3d03_v2_0009, brta_09e8cbfff67f117e_v2_0009, brta_cbe22ab64acf3d03_v2_0011, brta_09e8cbfff67f117e_v2_0011, brta_4e08eb4e988d38e4_v2_0014, brta_cbe22ab64acf3d03_v2_0010

## brta_07_lost

ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?

Route: llm_dense_evidence; time: 276.73 s

আবেদনকারী ড্রাইভিং লাইসেন্স প্রাপ্তির জন্য নিম্নলিখিত প্রক্রিয়া অনুসরণ করতে হবে:

1. **অনলাইন অ্যাকাউন্ট তৈরি:** শিক্ষানবিশ ড্রাইভিং লাইসেন্সের জন্য বিআরটিএ সার্ভিস পোর্টালে (BSP) আবেদন করতে হবে। এজন্য আবেদনকারী তাদের NID ব্যবহার করে একটি ইউজার অ্যাকাউন্ট তৈরি করতে হবে।  
2. **সার্কেল অফিস নির্ধারণ:** ইউজার প্রোফাইলে বিভাগ, জেলা ও থানা পূরণ করতে হবে। এর ভিত্তিতে আবেদনটি সংশ্লিষ্ট বিআরটিএ সার্কেল অফিসের আওতাধীন হবে।  
3. **পরীক্ষা কেন্দ্রে উপস্থিতি ও বায়োমেট্রিক:** নির্ধারিত দিনে শিক্ষানবিশ ড্রাইভিং লাইসেন্স ও অন্যান্য প্রয়োজনীয় ডকুমেন্টগুলি ছাড়া বায়োমেট্রিক তথ্য (ফিঙ্গার প্রিন্ট) প্রদান করতে হবে, যাচাইকরণ সম্পন্ন হলেই পরীক্ষার জন্য অনুমোদন ঘটবে।  
4. **পরীক্ষার ফলাফল:** আবেদনকারীর মোবাইলে SMS এবং অনলাইনে উত্তীর্ণ/অনুত্তীর্ণ ফলাফল প্রদান করা হবে।  
5. **আবেদন ফি প্রদান:** আবেদনকারী বিআরটিএ কর্তৃক নির্ধারিত ফি ১ ক্যাটাগরি-৫১৮/-টাকা ও ২ ক্যাটাগরি-৭৪৮/-টাকা অনলাইনে (মোবাইল ব্যাংকিং, অনলাইন ব্যাংকিং) দিতে হবে।

Sources: brta_cbe22ab64acf3d03_v2_0003, brta_4e08eb4e988d38e4_v2_0200, brta_4e08eb4e988d38e4_v2_0023, brta_cbe22ab64acf3d03_v2_0004, brta_4e08eb4e988d38e4_v2_0025, brta_846a4041fe96a64e_v2_0007

Supplied evidence: brta_cbe22ab64acf3d03_v2_0003, brta_4e08eb4e988d38e4_v2_0200, brta_4e08eb4e988d38e4_v2_0023, brta_cbe22ab64acf3d03_v2_0004, brta_4e08eb4e988d38e4_v2_0025, brta_846a4041fe96a64e_v2_0007

## brta_08_correction

ড্রাইভিং লাইসেন্সে নাম বা জন্মতারিখ ভুল হলে কীভাবে ঠিক করব?

Route: llm_dense_evidence; time: 215.22 s

ড্রাইভিং লাইসেন্সে নাম অথবা জন্মতারিখ ভুল হলে নিচের পদক্ষেপগুলো গ্রহণ করুন:

1. **ফরম-৪(খ)** এ আবেদন করুন।  
   - ফরমটি বিশেষ করে "জন্ম তারিখ" বিষয়ে দুইটি ক্ষেত্র থাকবে: **বিদ্যমান তথ্য** ও **প্রস্তাবিত সংশোধন**।

2. **বর্তমান তথ্য** ক্ষেত্রে ভুল তথ্যটি লিখুন (উদাহরণ: ১৩ ডিসেম্বর, ১৯৮০)।  
3. **প্রস্তাবিত সংশোধন** ক্ষেত্রে ঠিক তথ্যটি লিখুন (উদাহরণ: ১৪ ডিসেম্বর, ১৯৮০)।

4. আবেদনকারীর জন্মতারিখ অথবা নাম ভুল ছাড়া অন্য তথ্যগুলোও চেক করুন (যেমন: পিতার ও মাতার নাম, স্বামী/স্ত্রীর নাম ইত্যাদি)।

5. ফরমে স্ট্যাম্প এবং ছবি আঠাইয়ে সংযোজন করুন।  
6. আবেদনপত্রটি **বিআরটিএ** কার্যালয়ে জমা দিন।

Sources: brta_258cf38650a6332b_v2_0021, brta_258cf38650a6332b_v2_0018, brta_258cf38650a6332b_v2_0019, brta_4e08eb4e988d38e4_v2_0199, brta_258cf38650a6332b_v2_0020, brta_00cf734ebafbc7c2_v2_0034

Supplied evidence: brta_258cf38650a6332b_v2_0021, brta_258cf38650a6332b_v2_0018, brta_258cf38650a6332b_v2_0019, brta_4e08eb4e988d38e4_v2_0199, brta_258cf38650a6332b_v2_0020, brta_00cf734ebafbc7c2_v2_0034

## brta_09_online_apply

ড্রাইভিং লাইসেন্সের আবেদন অনলাইনে কীভাবে করব?

Route: llm_dense_evidence; time: 261.69 s

অনলাইনে ড্রাইভিং লাইসেন্স আবেদন করতে হয় এমন ভাবে—

- আপনার NID ব্যবহার করে [বিআরটিএ সার্ভিস পোর্টাল](https://bsp.brta.gov.bd) তে অ্যাকাউন্ট খুলুন।  
- অ্যাকাউন্ট তৈরি করার সময় আপনার বিভাগ, জেলা ও থানা ফিল্ড করুন।  
- আবেদনকারীর ছবি (150 KB), মেডিকেল সার্টিফিকেট (600 KB), জাতীয় পরিচয়পত্রের স্ক্যান কপি (600 KB), ইউটিলিটি বিল (600 KB), শিক্ষাগত যোগ্যতার সনদ (600 KB) এবং ডোপ টেস্ট রিপোর্ট (যথাযথ ক্ষেত্রে) আপলোড করুন।  
- অনলাইনে আবেদন ফি ১ ক্যাটাগরি—৫১৮ টাকা, ২ ক্যাটাগরি—৭৪৮ টাকা দিন।  
- আবেদন করার পর আপনার লার্নার ড্রাইভিং লাইসেন্স ও স্মার্ট কার্ড ড্রাইভিং লাইসেন্স জমা হবে।

Sources: brta_846a4041fe96a64e_v2_0007, brta_cbe22ab64acf3d03_v2_0003, brta_846a4041fe96a64e_v2_0011, brta_4e08eb4e988d38e4_v2_0149, brta_cbe22ab64acf3d03_v2_0004, brta_846a4041fe96a64e_v2_0003

Supplied evidence: brta_846a4041fe96a64e_v2_0007, brta_cbe22ab64acf3d03_v2_0003, brta_846a4041fe96a64e_v2_0011, brta_4e08eb4e988d38e4_v2_0149, brta_cbe22ab64acf3d03_v2_0004, brta_846a4041fe96a64e_v2_0003

## brta_10_status

আমার ড্রাইভিং লাইসেন্সের বর্তমান status কীভাবে দেখব?

Route: llm_dense_evidence; time: 213.47 s

আপনি ড্রাইভিং লাইসেন্সের বর্তমান status দেখতে পারেন নিম্নলিখিত ভাবে:

- আপনার ড্রাইভিং লাইসেন্সে উল্লিখিত **বর্তমান ঠিকানা** যথাক্রমে:
  - গ্রাম/হাউস
  - ইউনিয়ন
  - ওয়ার্ড নম্বর
  - উপজেলা
  - জেলা
  - পোস্ট কোড নম্বর

- আপনার ড্রাইভিং লাইসেন্সে উল্লিখিত **শিক্ষানবিশ লাইসেন্স নম্বর (Learner License Number)** হতে পারে:  
  - ফরম-৪(ক) এর অধীনে "Most Recent DL/Learner License Number" বিভাগ।

- আপনি যদি ড্রাইভিং লাইসেন্সটি দখল করছেন, তবে আপনার ঠিকানা বর্ণনা করতে হবে:
  - বাড়ি/গ্রাম/রাস্তা (বাংলা)
  - থানা
  - উপজেলা/শহর
  - জেলা
  - পোস্ট কোড

আপনি যদি ড্রাইভিং লাইসেন্সের **বর্তমান status** চেক করতে চান, তবে আপনার ড্রাইভিং লাইসেন্সে উল্লিখিত ঠিকানা অনুযায়ী এই ফরমগুলো পরিষ্কার করুন।

Sources: brta_00cf734ebafbc7c2_v2_0017, brta_a207b925ed0dc4a9_v2_0020, brta_e640c49d6025cc8d_v2_0006, brta_4e08eb4e988d38e4_v2_0196, brta_00cf734ebafbc7c2_v2_0026, brta_91979c30a91124e0_v2_0011

Supplied evidence: brta_00cf734ebafbc7c2_v2_0017, brta_a207b925ed0dc4a9_v2_0020, brta_e640c49d6025cc8d_v2_0006, brta_4e08eb4e988d38e4_v2_0196, brta_00cf734ebafbc7c2_v2_0026, brta_91979c30a91124e0_v2_0011

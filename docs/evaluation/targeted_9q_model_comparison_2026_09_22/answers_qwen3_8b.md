# Manual audit answers

These are raw chatbot outputs. Expected-evidence-present checks only a predefined hint and is not an answer-correctness score.

## passport_01_documents (passport / direct / single)

Question: নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?

Model: qwen3:8b; route: llm; time: 189.93 s; expected evidence present: None.

Answer:

- **ক.** ডেলিভারি স্লিপ (Delivery Slip)।
- **খ.** সন্তানের পাসপোর্ট হলে (১২ বছরের কম): অভিভাবকের NID/পাসপোর্ট।
- **গ.** প্রতিনিধি দিয়ে সংগ্রহ করতে চাইলে: আবেদনকারীর স্বাক্ষরযুক্ত অনুমোদনপত্র (Authorization Letter) এবং প্রতিনিধির NID।
- **ঘ.** পূর্বের মূল পাসপোর্ট।

Sources: passport_23d845d3ab38ea43_v2_0040, passport_73ac41f2327257f9_v2_0004, passport_729010959c882773_v2_0003

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0040: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_73ac41f2327257f9_v2_0004: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_729010959c882773_v2_0003: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md
- passport_729010959c882773_v2_0004: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md
- passport_73ac41f2327257f9_v2_0003: cleaned_md/পাসপোর্ট অফিসে আবেদনপত্র জমা দেওয়ার সময় যে সকল প্রয়োজনীয় কাগজপত্র নিয়ে যেতে হবে.md
- passport_23d845d3ab38ea43_v2_0033: cleaned_md/Bangladesh_ePassport_FAQ.md

## passport_02_fee (passport / direct / single)

Question: পাসপোর্ট বানাতে কত টাকা লাগে?

Model: qwen3:8b; route: llm; time: 162.06 s; expected evidence present: None.

Answer:

পাসপোর্ট বানাতে মূলত নিচের প্রকাশিত ফি হবে:

- **সাধারণ ফি:** ৫০০ টাকা + ১৫% ভ্যাট = ৫৭৫ টাকা
- **জরুরি ফি:** ১০,০০০ টাকা + ১৫% ভ্যাট = ১১,৫০০ টাকা

যদি আপনি ই-পাসপোর্ট চাওয়া হয় তবে ফি হবে:

- **সাধারণ ডেলিভারি (২১ দিন):** ৩,৪৫০ টাকা
- **জরুরি ডেলিভারি (১১ দিন):** ৬,৯০০ টাকা
- **সুপার জরুরি ডেলিভারি (৮ দিন):** ১০,৩৫০ টাকা

Sources: passport_6f7d900581956bef_v2_0016, passport_12e10027cfdfeeee_v2_0010, passport_5eb6c21efe103a4f_v2_0026

Retrieved sources:
- passport_6f7d900581956bef_v2_0016: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_12e10027cfdfeeee_v2_0010: cleaned_md/e-Passport Fees and Payment Options.md
- passport_5eb6c21efe103a4f_v2_0026: cleaned_md/Bangladesh Machine Readable Passport (MRP) Online Application Guide 2012.md
- passport_6f7d900581956bef_v2_0011: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0019: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_729010959c882773_v2_0003: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md

## passport_03_timeline (passport / direct / single)

Question: পাসপোর্ট পেতে কত দিন সময় লাগে?

Model: qwen3:8b; route: llm; time: 96.21 s; expected evidence present: None.

Answer:

পাসপোর্ট পেতে সময়সীমা নিমন্ত্রণ অনুযায়ী হয়:

- জরুরী পাসপোর্ট: ৭টি কর্মদিবস।
- রেগুলার পাসপোর্ট: ১৫টি কর্মদিবস।
- সুপার এক্সপ্রেস পাসপোর্ট: ২টি কর্মদিবস।

Sources: passport_9f4e9ffe9f2a07f4_v2_0004, passport_12e10027cfdfeeee_v2_0005, passport_f2c0d221c70d21f2_v2_0003

Retrieved sources:
- passport_9f4e9ffe9f2a07f4_v2_0004: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_12e10027cfdfeeee_v2_0005: cleaned_md/e-Passport Fees and Payment Options.md
- passport_f2c0d221c70d21f2_v2_0003: cleaned_md/Urgent Applications e-Passport.md
- passport_6f7d900581956bef_v2_0031: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0019: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0011: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md

## birth_01_documents (birth_death_registration / direct / single)

Question: জন্মনিবন্ধন করতে কী কী কাগজপত্র লাগে?

Model: qwen3:8b; route: controlled; time: 29.43 s; expected evidence present: None.

Answer:

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

Sources: birth_registration_application_process_cleaned_002_01, birth_registration_application_process_cleaned_016_01, birth_registration_application_process_02_cleaned_010_01

Retrieved sources:
- birth_registration_application_process_cleaned_002_01: unknown source
- birth_registration_application_process_cleaned_016_01: unknown source
- birth_registration_application_process_02_cleaned_010_01: unknown source
- know_this_01_cleaned_003_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১০_01: unknown source
- know_this_01_cleaned_002_01: unknown source

## birth_02_online (birth_death_registration / procedure / single)

Question: জন্মনিবন্ধন অনলাইনে কীভাবে করব?

Model: qwen3:8b; route: controlled; time: 26.59 s; expected evidence present: None.

Answer:

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

Sources: birth_registration_application_process_cleaned_008_01, birth_registration_application_process_02_cleaned_003_01, bdris_faq_01_q02

Retrieved sources:
- birth_registration_application_process_cleaned_008_01: unknown source
- birth_registration_application_process_02_cleaned_003_01: unknown source
- bdris_faq_01_q02: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_04: unknown source
- birth_and_death_registration_rules_2018_বিধি_১৯_03: unknown source

## birth_03_birth_date_correction (birth_death_registration / correction / single)

Question: জন্মনিবন্ধনে জন্মতারিখ ভুল হলে কীভাবে সংশোধন করব?

Model: qwen3:8b; route: controlled; time: 22.68 s; expected evidence present: None.

Answer:

রেজিস্ট্রেশন ও ইস্যু তারিখ সংশোধনের ধাপ: ধাপ ১: `https://bdris.gov.bd` ওয়েবসাইটে নিবন্ধক সহকারীর আইডি দিয়ে প্রবেশ করতে হবে।

ধাপ ২: `জন্ম তথ্য` বাটনে ক্লিক করতে হবে।

ধাপ ৩: `বিশেষ তথ্য সংশোধন` বাটনে ক্লিক করতে হবে।

ধাপ ৪: জন্ম নিবন্ধন নম্বর ও জন্ম তারিখ লিখে `অনুসন্ধান` বাটনে ক্লিক করতে হবে।

ধাপ ৫: সংশোধিত রেজিস্ট্রেশন তারিখ ও ইস্যু তারিখ প্রদান করে পরবর্তী ধাপে সংযুক্তির জন্য যেতে হবে।

ধাপ ৬: প্রয়োজনীয় সংযুক্তি দিতে হবে, যেমন ব্যক্তির অঙ্গীকারনামা, নিবন্ধকের প্রত্যয়নপত্র, হাতে লেখা নিবন্ধন বহির সংশ্লিষ্ট পৃষ্ঠার নিবন্ধক কর্তৃক সত্যায়িত কপি এবং হাতে লেখা জন্ম সনদের কপি।

ধাপ ৭: ক্ষেত্রমত ঊর্ধ্বতন কর্তৃপক্ষের সুপারিশক্রমে রেজিস্ট্রার জেনারেল কার্যালয়ের অনুমোদন সাপেক্ষে সংশ্লিষ্ট নিবন্ধন কার্যালয় থেকে নিষ্পত্তি হবে।

Sources: notice_birth_and_death_registration_certificate_correction_steps_ocr_006_01, notice_birth_and_death_registration_certificate_correction_steps_ocr_005_01, notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01

Retrieved sources:
- notice_birth_and_death_registration_certificate_correction_steps_ocr_006_01: unknown source
- notice_birth_and_death_registration_certificate_correction_steps_ocr_005_01: unknown source
- notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01: unknown source
- application_for_birth_information_correction_cleaned_008_01: unknown source
- application_for_birth_information_correction_cleaned_006_01: unknown source
- birth_and_death_registration_act_2004_ধারা_১৫_01: unknown source

## brta_01_documents (brta / direct / single)

Question: ড্রাইভিং লাইসেন্স করতে কী কী কাগজপত্র লাগবে?

Model: qwen3:8b; route: llm; time: 249.42 s; expected evidence present: None.

Answer:

ড্রাইভিং লাইসেন্স করতে নিম্নলখ কাগজপত্র প্রয়োগ:

* **১. আবেদনপত্র:** নির্ধারিত ফরমে অনলাইনে আবেদন।
* **২. ছবি:** আবেদনকারীর ছবি (ছবির সাইজ সর্বোচ্চ ১৫০ কেবি)।
* **৩. মেডিকেল সার্টিফিকেট:** রেজিষ্টার্ড ডাক্তার কর্তৃক মেডিকেল সার্টিফিকেট (সর্বোচ্চ ৬০০ কে.বি)।
* **৪. পরিচয়পত্র:** জাতীয় পরিচয়পত্রের স্ক্যান কপি (সর্বোচ্চ ৬০০ কে.বি)।
* **৫. ইউটিলিটি বিল:** ইউটিলিটি বিলের স্ক্যান কপি (সর্বোচ্চ ৬০০ কে.বি)।
* **৬. বিদ্যমান ড্রাইভিং লাইসেন্স:** বিদ্যমান ড্রাইভিং লাইসেন্সের স্ক্যান কপি (সর্বোচ্চ ৬০০ কে.বি)।
* **৭. আবেদন ফি:** নির্ধারিত ফি, ১ ক্যাটাগরি-৫১৮/-টাকা ও ২ ক্যাটাগরি-৭৪৮/-টাকা অনলাইনে পরিশোধ।

Sources: brta_cbe22ab64acf3d03_v2_0004, brta_cbe22ab64acf3d03_v2_0006, brta_cbe22ab64acf3d03_v2_0011

Retrieved sources:
- brta_cbe22ab64acf3d03_v2_0004: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_cbe22ab64acf3d03_v2_0006: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_cbe22ab64acf3d03_v2_0011: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_cbe22ab64acf3d03_v2_0003: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_4b8c25d391e48121_v2_0003: fahim_brta/সেবাসমূহ/ড্রাইভিং ইন্সট্রাক্টর লাইসেন্স.md
- brta_cbe22ab64acf3d03_v2_0013: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md

## brta_02_fee (brta / direct / single)

Question: ড্রাইভিং লাইসেন্স করতে মোট কত টাকা লাগে?

Model: qwen3:8b; route: llm; time: 111.72 s; expected evidence present: None.

Answer:

অপেশাদার লাইসেন্সের জন্য মোট খরচ ৪,৪৯৭ টাকা (১০ বছরের মেয়াদ)।
পেশাদার লাইসেন্সের জন্য মোট খরচ ২,৮৬৯ টাকা (৫ বছরের মেয়াদ)।
ডাক মাশুল ছাড়াও ৬০ টাকা অতিরিক্ত দিতে হবে।

Sources: brta_846a4041fe96a64e_v2_0006, brta_3cae1ecd59682fa3_v2_0012, brta_3cae1ecd59682fa3_v2_0004

Retrieved sources:
- brta_846a4041fe96a64e_v2_0006: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_3cae1ecd59682fa3_v2_0012: brta/ফি, ট্যাক্স ও আয়কর/ড্রাইভিং লাইসেন্স ফি.md
- brta_3cae1ecd59682fa3_v2_0004: brta/ফি, ট্যাক্স ও আয়কর/ড্রাইভিং লাইসেন্স ফি.md
- brta_3cae1ecd59682fa3_v2_0017: brta/ফি, ট্যাক্স ও আয়কর/ড্রাইভিং লাইসেন্স ফি.md
- brta_846a4041fe96a64e_v2_0005: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_3cae1ecd59682fa3_v2_0018: brta/ফি, ট্যাক্স ও আয়কর/ড্রাইভিং লাইসেন্স ফি.md

## brta_03_learner (brta / procedure / single)

Question: লার্নার ড্রাইভিং লাইসেন্স কীভাবে করব?

Model: qwen3:8b; route: llm; time: 229.2 s; expected evidence present: None.

Answer:

- আপনি `bsp.brta.gov.bd` ওয়েবসাইটে অনলাইনে আবেদন করুন।
- আবেদন করতে হবে জাতীয় পরিচয়পত্র (NID), ছবি, মেডিকেল সার্টিফিকেট, ইউটিলিটি বিল এবং অন্যান্য প্রয়োজনীয় দখলকৃত ডকুমেন্টগুলি উপস্থাপন করুন।
- আবেদন ফি জমা দিন (১ ক্যাটাগরি - ৫১৮ টাকা, ২ ক্যাটাগরি - ৭৪৮ টাকা)।
- আপনার লার্নার ড্রাইভিং লাইসেন্স অনলাইনে প্রিন্ট করে নিন।
- ২/৩ মাস প্রশিক্ষণ গ্রহণ করুন।
- তারিখ ও সময় বরাবর নির্ধারিত কেন্দ্রে লিখিত, মৌখিক এবং ফিল্ড টেস্ট দিন।

Sources: brta_cbe22ab64acf3d03_v2_0003, brta_cbe22ab64acf3d03_v2_0004, brta_846a4041fe96a64e_v2_0011

Retrieved sources:
- brta_cbe22ab64acf3d03_v2_0003: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_cbe22ab64acf3d03_v2_0004: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_846a4041fe96a64e_v2_0011: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_09e8cbfff67f117e_v2_0005: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_846a4041fe96a64e_v2_0002: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_cbe22ab64acf3d03_v2_0002: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md

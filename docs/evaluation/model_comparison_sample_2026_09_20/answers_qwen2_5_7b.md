# Manual audit answers

These are raw chatbot outputs. Expected-evidence-present checks only a predefined hint and is not an answer-correctness score.

## birth_deadline_direct (birth_death_registration / birth_deadline / direct)

Question: শিশুর জন্মের কত দিনের মধ্যে জন্ম নিবন্ধনের তথ্য দিতে হয়?

Model: qwen2.5:7b; route: controlled; time: 20.11 s; expected evidence present: True.

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

## birth_deadline_code_mixed (birth_death_registration / birth_deadline / code_mixed)

Question: baby birth er por birth registration information kotodin er moddhe dite hoy?

Model: qwen2.5:7b; route: llm; time: 54.7 s; expected evidence present: False.

Answer:

The birth registration information must be provided within a day after the baby's birth. You need to provide:

- Baby’s name in Bangla and English
- Date of birth
- Gender
- Order of birth
- Place of birth address

These details should be entered correctly as per their online birth registration record. After providing this information, click on the "Verify" button.

Sources: birth_registration_application_process_02_cleaned_006_01, know_this_01_cleaned_003_01, birth_registration_application_process_cleaned_012_01

Retrieved sources:
- birth_registration_application_process_02_cleaned_006_01: unknown source
- know_this_01_cleaned_003_01: unknown source
- birth_registration_application_process_cleaned_012_01: unknown source
- application_for_birth_information_correction_cleaned_008_01: unknown source
- application_for_birth_information_correction_cleaned_006_01: unknown source
- application_for_birth_information_correction_cleaned_005_01: unknown source

## brta_age_direct (brta / professional_license_age / direct)

Question: পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স কত?

Model: qwen2.5:7b; route: llm; time: 76.89 s; expected evidence present: True.

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

## brta_colour_code_mixed (brta / vehicle_colour_change / code_mixed)

Question: car er colour change BRTA te update korte ki documents lagbe?

Model: qwen2.5:7b; route: llm; time: 203.09 s; expected evidence present: True.

Answer:

### গাড়ির কাগজপত্ত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স এর জরিমানা ব্যতীত মূল কর / ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্ত্র হালনাগাদ সংক্রান্ত শর্তগুলি:

1. **আবেদনপত্র:** 
   - মালিকের স্বাক্ষর সম্বলিত আবেদন পত্র ১ কপি

2. **মূল নিবন্ধন সনদ:**
   - মূল নিবন্ধন সনদ (কাগজের নিবন্ধন সনদ হলে হোম কপিও জমা দিতে হবে)

3. **ফি জমার রশিদ:**
   - রং পরিবর্তন ফি জমার রশিদের বিআরটিএ'র কপি

4. **ফিটনেস সনদ:**
   - হালনাগাদ ফিটনেস সনদের ফটোকপি ১ কপি

5. **ট্যাক্স টোকেন:** 
   - হালনাগাদ ট্যাক্স টোকেনের ফটোকপি ১ কপি

**তারিখ:** ২২-০৬-২০২০  
**অফিস:** বিআরটিএ সংস্থাপন শাখা, সড়ক পরিবহন ও মহাসড়ক বিভাগ, সড়ক পরিবহন ও সেতু মন্ত্রণালয়, গণপ্রজাতন্ত্রী বাংলাদেশ সরকার

Sources: brta_a40ff0f214eb68b8_v2_0001, brta_a40ff0f214eb68b8_v2_0002, brta_33c0c02c5416861c_v2_0005

Retrieved sources:
- brta_a40ff0f214eb68b8_v2_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_v2_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_33c0c02c5416861c_v2_0005: brta/আইন, বিধি ও নীতিমালা/গাড়ির কাগজপত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স এর জরিমানা ব্যতীত মূল কর বা ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্র হালনাগাদ সংক্রান্ত প্রজ্ঞাপন.md
- brta_4e08eb4e988d38e4_v2_0199: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_9a180bfd62e0eab9_v2_0004: brta/আইন, বিধি ও নীতিমালা/জরিমানা ব্যতীত মূল কর বা ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স হালনাগাদের সময়সীমা ১৫ এপ্রিল ২০২৪ খ্রিঃ পর্যন্ত বর্ধিতকরণ সংক্রান্ত প্রজ্ঞাপন.md
- brta_9a180bfd62e0eab9_v2_0002: brta/আইন, বিধি ও নীতিমালা/জরিমানা ব্যতীত মূল কর বা ফি জমা প্রদানপূর্বক গাড়ির কাগজপত্র (ফিটনেস, ট্যাক্স টোকেন ও রুট পারমিট) এবং ড্রাইভিং লাইসেন্স হালনাগাদের সময়সীমা ১৫ এপ্রিল ২০২৪ খ্রিঃ পর্যন্ত বর্ধিতকরণ সংক্রান্ত প্রজ্ঞাপন.md

## passport_collect_direct (passport / passport_collection / direct)

Question: ই-পাসপোর্ট সংগ্রহ করতে অফিসে কী কী নিয়ে যেতে হবে?

Model: qwen2.5:7b; route: llm; time: 178.51 s; expected evidence present: False.

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

## passport_password_direct (passport / account_password_recovery / direct)

Question: অনলাইন পাসপোর্ট অ্যাকাউন্টের পাসওয়ার্ড ভুলে গেলে কী করতে হবে?

Model: qwen2.5:7b; route: llm; time: 96.42 s; expected evidence present: True.

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

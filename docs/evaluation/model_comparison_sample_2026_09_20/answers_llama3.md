# Manual audit answers

These are raw chatbot outputs. Expected-evidence-present checks only a predefined hint and is not an answer-correctness score.

## birth_deadline_direct (birth_death_registration / birth_deadline / direct)

Question: শিশুর জন্মের কত দিনের মধ্যে জন্ম নিবন্ধনের তথ্য দিতে হয়?

Model: llama3; route: controlled; time: 18.78 s; expected evidence present: True.

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

Model: llama3; route: llm; time: 45.26 s; expected evidence present: False.

Answer:

According to Source 1, after a baby's birth, birth registration information is provided in the following format:

* Name (Bangla and English)
* Date of Birth
* Gender
* Number of children
* Place of birth address

This information must be submitted online with accurate data entry and storage in the database, as well as issuance of a birth certificate.

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

Model: llama3; route: llm; time: 85.83 s; expected evidence present: True.

Answer:

পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স হলো ২১ বছর। (For professional driving license, the minimum age is 21 years.)

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

Model: llama3; route: llm; time: 53.55 s; expected evidence present: True.

Answer:

To obtain a copy of your registration certificate (Rashid), you need to provide:

* A fitness certificate with a photocopy of the original document
* A tax token with a photocopy of the original document

These documents must be up-to-date and submitted along with the application fee.

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

Model: llama3; route: llm; time: 73.2 s; expected evidence present: False.

Answer:

ই-পাসপোর্ট সংগ্রহ করতে অফিসে কী কী নিয়ে যেতে হবে?

When visiting the passport office for enrolment/fingerprints, bring:

1. PRL / Post Retirement Leave Order copy.
2. NID card.
3. Previous Passport (Original).
4. Hard copy of Application Form.
5. Printed Summary Slip.
6. Payment Slip / Fee Receipt.

(Note: This information is based on Source 1 and provides a comprehensive list of required documents.)

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

Model: llama3; route: llm; time: 118.41 s; expected evidence present: True.

Answer:

অনলাইন পাসপোর্ট অ্যাকাউন্টের পাসওয়ার্ড ভুলে গেছি। এখন কি করা উচিত?

আমার পাসওয়ার্ড পুনরুদ্ধারে নিম্নবর্ণিত পন্থা অবলম্বন করুন:

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

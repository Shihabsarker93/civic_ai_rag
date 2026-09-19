# Experimental domain integration check

Four convenience smoke questions using llama3.2; not a gold-label benchmark or full corpus validation.

Source hashes, indexed document coverage and Chroma/JSONL IDs and text were checked. No claims of measured answer accuracy are made.

| Domain | Documents | Chunks | Integrity |
|---|---:|---:|---|
| birth_death_registration | Existing corpus | 187 | Passed |
| brta | 132 | 1695 | Passed |
| passport | 30 | 148 | Passed |

## brta: অপেশাদার ও পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স কত?

Model: llama3.2; route: llm; time: 208.96 s; expected source among retrieved candidates: True.

এখানে ড্রাইভিং লাইসেন্স পাওয়ার জন্য প্রয়োজনীয় পদক্ষেপ:

1. **আবেদন প্রক্রিয়া:** ড্রাইভিং লাইসেন্স পাওয়ার জন্য অনলাইনে (BRTA Service Portal) আবেদন করতে হবে।
2. **মাধ্যমিক শিক্ষাগত যোগ্যতা:** ড্রাইভিং লাইসেন্সের আবেদনকারীর ন্যূনতম 8th শ্রেণি পাশ থাকতে হবে।
3. **বয়সসীমা:** অপেশাদার চালকদের জন্য ন্যূনতম 18 বছর, এবং পেশাদার ড্রাইভিং লাইসেন্স-এর জন্য বয়স ন্যূনতম 21 বছর।
4. **শারীরিক যোগ্যতা:** মানসিক ও শারীরিকভাবে সুস্থ থাকতে হবে।

**আবেদনের ফলাফল:**

*   আবেদনকারীর ছবি (সর্বোচ্চ 150 KB)।
*   মেডিকেল সার্টিফিকেট (সর্বোচ্চ 600 KB)।
*   জাতীয় পরিচয়পত্রের স্ক্যান কপি (সর্বোচ্চ 600 KB)।
*   ইউটিলিটি বিলের স্ক্যান কপি (সর্বোচ্চ 600 KB), [আবেদনকারীর বর্তমান ঠিকানা এবং জাতীয় পরিচয়পত্রের ঠিকানা যদি ভিন্ন হয় তবে বর্তমান ঠিকানার ইউটিলিটি বিল সংযুক্ত করতে হবে]।
*   শিক্ষাগত যোগ্যতার সনদের স্ক্যান কপি (সর্বোচ্চ 600 KB)।

**ফিস:**

*   **1 ক্যাটাগরি:** 518/- টাকা। *   শুধু কার: 51,8/-
*   **2 ক্যাটাগরি:** 748/- টাকা।

Sources: brta_cbe22ab64acf3d03_0001, brta_846a4041fe96a64e_0001, brta_94f4ba4f5f79bcc1_0003

Retrieved source files:
- brta_cbe22ab64acf3d03_0001: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_846a4041fe96a64e_0001: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_94f4ba4f5f79bcc1_0003: fahim_brta/ফরম/ফরম-১ শিক্ষানবিশ ড্রাইভিং লাইসেন্স আবেদন.md
- brta_4e08eb4e988d38e4_0017: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_edcb265eccf9cd32_0012: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md
- brta_4e08eb4e988d38e4_0195: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md

## brta: গাড়ির রং পরিবর্তনের জন্য কী কী কাগজপত্র লাগবে?

Model: llama3.2; route: llm; time: 99.51 s; expected source among retrieved candidates: True.

গাড়ির রঙ পরিবর্তনের জন্য নিচের দলিলা প্রয়োজন:

• আবেদনপত্র (মালিকের স্বাক্ষর সম্বলিত) - 01 কপি
• মূল নিবন্ধন সনদ (কাগজের নিবন্ধন সনদ থাকলে হোম কপিও জমা দিতে হবে)
• ফি জমার রশিদ (রং পরিবর্তন ফি জমার রশিদের বিআরটিএ'র কপি)
• ফিটনেস সনদ (হালনাগাদ ফিটনেস সনদের ফটোকপি 01 কপি)
• ট্যাক্স টোকেন (হালনাগাদ ট্যাক্স টোকেনের ফটোকপি - 01 কপি)

Sources: brta_a40ff0f214eb68b8_0002, brta_a40ff0f214eb68b8_0001, brta_e21467da1ba75db4_0002

Retrieved source files:
- brta_a40ff0f214eb68b8_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_e21467da1ba75db4_0002: fahim_brta/সেবাসমূহ/তথ্য সংশোধনপরিবর্তন.md
- brta_b5a9e5763aa87a48_0002: fahim_brta/সেবাসমূহ/টায়ার সাইজ(প্রস্থ) সংশোধন.md
- brta_edcb265eccf9cd32_0033: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md
- brta_4b4c003681ae6872_0003: fahim_brta/সেবাসমূহ/মোটরযানের নিবন্ধন.md

## passport: সুপার এক্সপ্রেস পাসপোর্ট কোথা থেকে সংগ্রহ করতে হবে?

Model: llama3.2; route: llm; time: 87.84 s; expected source among retrieved candidates: True.

সুপার এক্সপ্রেস পাসপোর্ট সংগ্রহ করা যেতে পারে আবেদন করে ঢাকা থেকে নয়। অতি জরুরি বা সুপার এক্সপ্রেস শ্রেণীর পাসপোর্ট আমলিয়া ভেটা ওফিস, আগারগাঁও, ঢাকা-1207 থেকে সংগ্রহ করা যায়।

* ডেলিভারি স্লিপে (Delivery Slip) এ উল্লিখিত আঞ্চলিক বা বিভাগীয় পাসপোর্ট অফিসের নাম অনুসরণ করে।
* শিপমেন্ট অন্য পাসপোর্ট অফিসে ঘটাই যায় না।

Sources: passport_23d845d3ab38ea43_0036, passport_f2c0d221c70d21f2_0001, passport_f2c0d221c70d21f2_0002

Retrieved source files:
- passport_23d845d3ab38ea43_0036: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_f2c0d221c70d21f2_0001: cleaned_md/Urgent Applications e-Passport.md
- passport_f2c0d221c70d21f2_0002: cleaned_md/Urgent Applications e-Passport.md
- passport_23d845d3ab38ea43_0019: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_ed7b3ebc56c0094f_0001: cleaned_md/মেশিন রিডেবল পাসপোর্ট(এমআরপি).md
- passport_6f7d900581956bef_0007: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md

## passport: ই-পাসপোর্ট সংগ্রহ করতে কী নিয়ে যেতে হবে?

Model: llama3.2; route: llm; time: 74.88 s; expected source among retrieved candidates: False.

ই-পাসপোর্ট সংগ্রহ করতে হলে নিন্মরূপ কাগজপত্র ও ডকুমেন্ট আছে:

*   PRL / Post Retirement Leave Order copy
*   NID card
*   Previous Passport (Original)
*   Hard copy of Application Form
*   Printed Summary Slip
*   Payment Slip / Fee Receipt

এখন উভয় ধরনের পাসপোর্ট থেকে অফিসে যাওয়ার পর শুধুমাত্র দৃষ্টি বঞ্চিত কাগজপত্র বহন করুন।

Sources: passport_23d845d3ab38ea43_0023, passport_23d845d3ab38ea43_0029, passport_23d845d3ab38ea43_0033

Retrieved source files:
- passport_23d845d3ab38ea43_0023: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_0029: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_0033: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_729010959c882773_0002: cleaned_md/পাসপোর্টের আবেদন জমা নেওয়ার ক্ষেত্রে চেকলিস্ট.md
- passport_23d845d3ab38ea43_0022: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_0028: cleaned_md/Bangladesh_ePassport_FAQ.md

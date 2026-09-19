# Experimental domain integration check

Four convenience smoke questions using llama3.2; not a gold-label benchmark or full corpus validation.

Source hashes, indexed document coverage and Chroma/JSONL IDs and text were checked. No claims of measured answer accuracy are made.

| Domain | Documents | Chunks | Integrity |
|---|---:|---:|---|
| birth_death_registration | Existing corpus | 187 | Passed |
| brta | 132 | 3161 | Passed |
| passport | 30 | 361 | Passed |

## brta: অপেশাদার ও পেশাদার ড্রাইভিং লাইসেন্সের জন্য ন্যূনতম বয়স কত?

Model: llama3.2; route: llm; time: 82.63 s; expected source among retrieved candidates: True.

অপেশাদার চালকদের জন্য ন্যূনতম বয়স 18 বছর।

*   ড্রাইভিং লাইসেন্সের পূর্বশর্ত হলো লার্নার বা শিক্ষানবিশ ড্রাইভিং লাইসেন্স।
*   ড্রাইভিং লাইসেন্সের আবেদনকারীর ন্যূনতম শিক্ষাগত যোগ্যতা 8th শ্রেণি পাশ।
*   এটি উল্লেখ করা হয়েছে অপেশাদার চালকদের জন্য, পেশাদার ড্রাইভিং লাইসেন্স-এর জন্য বয়স ন্যূনতম 21 বছর।

Sources: brta_cbe22ab64acf3d03_v2_0002, brta_846a4041fe96a64e_v2_0002, brta_cbe22ab64acf3d03_v2_0007

Retrieved source files:
- brta_cbe22ab64acf3d03_v2_0002: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_846a4041fe96a64e_v2_0002: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_cbe22ab64acf3d03_v2_0007: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_4e08eb4e988d38e4_v2_0017: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_edcb265eccf9cd32_v2_0012: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহন আইন, ২০১৮.md
- brta_4e08eb4e988d38e4_v2_0195: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md

## brta: গাড়ির রং পরিবর্তনের জন্য কী কী কাগজপত্র লাগবে?

Model: llama3.2; route: llm; time: 63.22 s; expected source among retrieved candidates: True.

গাড়ির রং পরিবর্তনের জন্য নিচে উল্লিখিত কাগজপত্রগুলো প্রয়োজন:

• আবেদনপত্র (মালিকের স্বাক্ষর সম্বলিত)
• মূল নিবন্ধন সনদ
• রং পরিবর্তন ফি জমার রশিদ
• হালনাগাদ ফিটনেস সনদের ফটোকপি ০১ কপি
• হালনাগাদ ট্যাক্স টোকেনের ফটোকপি ০১ কপি

Sources: brta_a40ff0f214eb68b8_v2_0002, brta_a40ff0f214eb68b8_v2_0001, brta_e21467da1ba75db4_v2_0002

Retrieved source files:
- brta_a40ff0f214eb68b8_v2_0002: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_a40ff0f214eb68b8_v2_0001: fahim_brta/সেবাসমূহ/রং পরিবর্তন.md
- brta_e21467da1ba75db4_v2_0002: fahim_brta/সেবাসমূহ/তথ্য সংশোধনপরিবর্তন.md
- brta_4b4c003681ae6872_v2_0003: fahim_brta/সেবাসমূহ/মোটরযানের নিবন্ধন.md
- brta_4b4c003681ae6872_v2_0002: fahim_brta/সেবাসমূহ/মোটরযানের নিবন্ধন.md
- brta_29228d7f41bd4857_v2_0036: fahim_brta/ফরম/ফরম-১৭ মোটরযান রেজিস্ট্রেশনের আবেদন.md

## passport: সুপার এক্সপ্রেস পাসপোর্ট কোথা থেকে সংগ্রহ করতে হবে?

Model: llama3.2; route: llm; time: 65.34 s; expected source among retrieved candidates: True.

সুপার এক্সপ্রেস পাসপোর্ট সংগ্রহ করা যেতে পারে আবেদন করে ঢাকা থেকে।

1. অনলাইন আবেদন পরিষেবা (Online Application Portal) মাধ্যমে সুপার এক্সপ্রেস পাসপোর্ট জড়িত নয়।
2. শুধুমাত্র উচ্ছ্বাসপ্রণিত পাসপোর্ট ও ভিসা অফিস, আগারগাঁও, ঢাকা-1207 থেকে সংগ্রহ করা যায়।

আবেদন করে ঢাকা থেকে সংগ্রহ করতে হবে।

Sources: passport_23d845d3ab38ea43_v2_0048, passport_f2c0d221c70d21f2_v2_0006, passport_f2c0d221c70d21f2_v2_0005

Retrieved source files:
- passport_23d845d3ab38ea43_v2_0048: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_f2c0d221c70d21f2_v2_0006: cleaned_md/Urgent Applications e-Passport.md
- passport_f2c0d221c70d21f2_v2_0005: cleaned_md/Urgent Applications e-Passport.md
- passport_f2c0d221c70d21f2_v2_0007: cleaned_md/Urgent Applications e-Passport.md
- passport_23d845d3ab38ea43_v2_0028: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_f2c0d221c70d21f2_v2_0004: cleaned_md/Urgent Applications e-Passport.md

## passport: ই-পাসপোর্ট সংগ্রহ করতে কী নিয়ে যেতে হবে?

Model: llama3.2; route: llm; time: 53.8 s; expected source among retrieved candidates: True.

ই-পাসপোর্ট সংগ্রহ করতে হলে, উপরের জায়গা থেকে প্রদত্ত শর্তগুলি পাওয়া যাচ্ছে।

*   ডেলিভারি স্লিপ
*   আবহিত প্রতিনিধি (নিদননিদ) এর অফিস থেকে নিজের NID কার্ড।
*   পূর্বের মূল পাসপোর্ট 
*   আবেদন ফর্মের হার্ড কপি

Sources: passport_6e87d0783a373593_v2_0008, passport_23d845d3ab38ea43_v2_0033, passport_23d845d3ab38ea43_v2_0040

Retrieved source files:
- passport_6e87d0783a373593_v2_0008: cleaned_md/5 Steps to your e-Passport.md
- passport_23d845d3ab38ea43_v2_0033: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0040: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0041: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_9f4e9ffe9f2a07f4_v2_0005: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_23d845d3ab38ea43_v2_0032: cleaned_md/Bangladesh_ePassport_FAQ.md

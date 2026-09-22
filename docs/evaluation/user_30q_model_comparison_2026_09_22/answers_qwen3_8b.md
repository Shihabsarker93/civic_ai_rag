# Manual audit answers

These are raw chatbot outputs. Expected-evidence-present checks only a predefined hint and is not an answer-correctness score.

## passport_01_documents (passport / direct / single)

Question: নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?

Model: qwen3:8b; route: llm; time: 131.17 s; expected evidence present: None.

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

Model: qwen3:8b; route: llm; time: 136.06 s; expected evidence present: None.

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

## passport_03_delivery_time (passport / direct / single)

Question: পাসপোর্ট পেতে কত দিন সময় লাগে?

Model: qwen3:8b; route: llm; time: 68.67 s; expected evidence present: None.

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

## passport_04_apply (passport / direct / single)

Question: ই-পাসপোর্টের জন্য কীভাবে আবেদন করব?

Model: qwen3:8b; route: llm; time: 153.06 s; expected evidence present: None.

Answer:

ই-পাসপোর্ট আবেদন করতে হলে নিচের ভাগগুলো অনুসরণ করুন:

* **১।** ই-পাসপোর্ট আবেদন ফরমটি অনলাইনে পূরণ করুন।  
* **২।** আবেদন ফরমে জাতীয় পরিচয়পত্র (NID) বা ডিজিটাল জন্ম নিবন্ধন সনদ (BRC English Version) দখল করুন। ১৮ বছরের কম বয়সীদের জন্য পিতা/মাতার NID নম্বর উল্লেখ করুন।  
* **৩।** আবেদনকারী এলাকার বিভাগীয় পাসপোর্ট ও ভিসা অফিস বা আঞ্চলিক পাসপোর্ট অফিসে আবেদনটি জমা দিন।  
* **৪।** পাসপোর্ট ফির জমা দিতে এ-চালান ব্যবহার করুন।

Sources: passport_9f4e9ffe9f2a07f4_v2_0002, passport_6e87d0783a373593_v2_0005, passport_6f7d900581956bef_v2_0006

Retrieved sources:
- passport_9f4e9ffe9f2a07f4_v2_0002: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_6e87d0783a373593_v2_0005: cleaned_md/5 Steps to your e-Passport.md
- passport_6f7d900581956bef_v2_0006: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_0b74faa4d85a2a58_v2_0003: cleaned_md/অনলাইন সেবাসমূহ (নাগরিক ই-সেবাসমূহের তালিকা).md
- passport_23d845d3ab38ea43_v2_0024: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_6e87d0783a373593_v2_0008: cleaned_md/5 Steps to your e-Passport.md

## passport_05_renewal (passport / direct / single)

Question: পাসপোর্টের মেয়াদ শেষ হলে কীভাবে নবায়ন করব?

Model: qwen3:8b; route: llm; time: 148.07 s; expected evidence present: None.

Answer:

পাসপোর্টের মেয়াদ শেষ হলে নবায়ন করতে হবে এমআরপি (পাসপোর্ট) ফরমটি পূরণ করুন।  
- বর্তমান পাসপোর্টের ফটোকপি ও ব্যাংকে টাকা জমার রশিদ অবশ্যই সংযুক্ত করুন।  
- মূল পাসপোর্টটি সঙ্গে নিয়ে আসুন।  
- পাসপোর্ট রি-ইস্যু বা নবায়নের জন্য শুধুমাত্র সাধারণ ফি প্রদান করতে হবে, মেয়াদ উত্তীর্ণের জন্য কোনো অতিরিক্ত ফি বা জরিমানা থাকবে না।

Sources: passport_3fcbc40c98aa80bc_v2_0002, passport_23d845d3ab38ea43_v2_0017, passport_9f4e9ffe9f2a07f4_v2_0003

Retrieved sources:
- passport_3fcbc40c98aa80bc_v2_0002: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর নিয়মাবলী.md
- passport_23d845d3ab38ea43_v2_0017: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_9f4e9ffe9f2a07f4_v2_0003: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_23d845d3ab38ea43_v2_0029: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_ed7b3ebc56c0094f_v2_0003: cleaned_md/মেশিন রিডেবল পাসপোর্ট(এমআরপি).md
- passport_3fcbc40c98aa80bc_v2_0009: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর নিয়মাবলী.md

## passport_06_lost (passport / direct / single)

Question: পাসপোর্ট হারিয়ে গেলে কী করতে হবে?

Model: qwen3:8b; route: llm; time: 114.99 s; expected evidence present: None.

Answer:

পাসপোর্ট হারিয়ে গেলে আপনি নিচের বিষয়গুলো করতে হবে:

- দ্রুত নিকটস্থ থানায় জিডি রিপোর্ট করুন।  
- অনলাইন এপাসপোর্ট আবেদন ফরম পূরণ করুন এবং `DUPLICATE` ধরন নির্বাচন করুন।  
- হারিয়েছে পাসপোর্টের নম্বর লিখুন।  
- মূল জিডি কপি ও পুরাতন পাসপোর্টের ফটোকপি ছাড়া আবেদনপত্র দাখিল করুন।

Sources: passport_9f4e9ffe9f2a07f4_v2_0005, passport_5eb6c21efe103a4f_v2_0034, passport_23d845d3ab38ea43_v2_0041

Retrieved sources:
- passport_9f4e9ffe9f2a07f4_v2_0005: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_5eb6c21efe103a4f_v2_0034: cleaned_md/Bangladesh Machine Readable Passport (MRP) Online Application Guide 2012.md
- passport_23d845d3ab38ea43_v2_0041: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0036: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_6f7d900581956bef_v2_0007: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_3fcbc40c98aa80bc_v2_0002: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর নিয়মাবলী.md

## passport_07_name_correction (passport / direct / single)

Question: পাসপোর্টে নাম ভুল থাকলে কীভাবে ঠিক করব?

Model: qwen3:8b; route: llm; time: 157.21 s; expected evidence present: None.

Answer:

পাসপোর্টে নাম ভুল থাকলে নিচু হদিশ ফলো করুন:

- প্রিন্টকৃত 'আবেদন সারাংশ' নিয়ে আপনার নির্ধারিত পাসপোর্ট অফিসে গেছো।  
- এনরোলমেন্ট অফিসার আপনার আবেদনটি দেখে ভুল তথ্য সংশোধন করে দেবেন।  
- NID, BRC, বা পূর্বের পাসপোর্ট জমা দিও যেন ঠিক তথ্য প্রমাণ করা যায়।  
- ডেলিভারী রশিদে আপনার তথ্য চেক করুন এবং কোনও ভুল থাকলে তৎক্ষণাৎ সংশোধন করতে হবে।  
- পাসপোর্ট নেয়ার ১ মাসের মধ্যে আপনার আঞ্চলিক পাসপোর্ট অফিস (RPO) এ যোগাযোগ করুন।

Sources: passport_23d845d3ab38ea43_v2_0021, passport_ed7b3ebc56c0094f_v2_0004, passport_23d845d3ab38ea43_v2_0042

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0021: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_ed7b3ebc56c0094f_v2_0004: cleaned_md/মেশিন রিডেবল পাসপোর্ট(এমআরপি).md
- passport_23d845d3ab38ea43_v2_0042: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_5eb6c21efe103a4f_v2_0033: cleaned_md/Bangladesh Machine Readable Passport (MRP) Online Application Guide 2012.md
- passport_a4d61a4d583daa54_v2_0004: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর আবেদন ফরম.md
- passport_a4d61a4d583daa54_v2_0010: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর আবেদন ফরম.md

## passport_08_birth_date (passport / direct / single)

Question: পাসপোর্টে জন্মতারিখ পরিবর্তন করা যায় কি?

Model: qwen3:8b; route: llm; time: 110.55 s; expected evidence present: None.

Answer:

পাসপোর্টে জন্ম তারিখ পরিবর্তন করা যায় না।  
- জন্ম তারিখ পরিবর্তনের জন্য কোনও কাগজপত্র প্রয়োজন হয় না।  
- অথচ, ই-পাসপোর্ট আবেদনে জন্ম তারিখ পরিবর্তনের ক্ষেত্রে এনআইডি (NID)/বিআরসি (BRC) এবং আগের পাসপোর্ট দখল করতে হবে।  
- ডেটা পরিবর্তনের জন্য সম্পৃক্ত দলিল জমা দিতে হবে।

Sources: passport_3fcbc40c98aa80bc_v2_0007, passport_5eb6c21efe103a4f_v2_0033, passport_23d845d3ab38ea43_v2_0019

Retrieved sources:
- passport_3fcbc40c98aa80bc_v2_0007: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর নিয়মাবলী.md
- passport_5eb6c21efe103a4f_v2_0033: cleaned_md/Bangladesh Machine Readable Passport (MRP) Online Application Guide 2012.md
- passport_23d845d3ab38ea43_v2_0019: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_a4d61a4d583daa54_v2_0012: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর আবেদন ফরম.md
- passport_3fcbc40c98aa80bc_v2_0004: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর নিয়মাবলী.md
- passport_3fcbc40c98aa80bc_v2_0005: cleaned_md/পাসপোর্ট (এমআরপি) রি-ইস্যু বা তথ্য পরিবর্তন বা সংশোধন এর নিয়মাবলী.md

## passport_09_status (passport / direct / single)

Question: পাসপোর্টের আবেদন করার পর স্ট্যাটাস কীভাবে দেখব?

Model: qwen3:8b; route: llm; time: 127.27 s; expected evidence present: None.

Answer:

আপনি নিম্নলিখিত ধাপগুলি অনুসরণ করে পাসপোর্ট আবেদনের অগ্রগতি দেখতে পারবেন:

- ই-পাসপোর্ট পোর্টালে **'স্ট্যাটাস চেক'** মেন্যুতে যান।  
- আবেদনকারীর জন্ম তারিখ এবং Application ID বা Online Registration ID (OID) প্রবেশ করিয়ে সার্চ বাটন চাপুন।  
- অথবা [https://www.epassport.gov.bd/authorization/application-status](https://www.epassport.gov.bd/authorization/application-status) লিংকটি থেকেও অগ্রগতি দেখতে পারেন।

Sources: passport_23d845d3ab38ea43_v2_0038, passport_23d845d3ab38ea43_v2_0044, passport_23d845d3ab38ea43_v2_0043

Retrieved sources:
- passport_23d845d3ab38ea43_v2_0038: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0044: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0043: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0047: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_23d845d3ab38ea43_v2_0027: cleaned_md/Bangladesh_ePassport_FAQ.md
- passport_0b74faa4d85a2a58_v2_0006: cleaned_md/অনলাইন সেবাসমূহ (নাগরিক ই-সেবাসমূহের তালিকা).md

## passport_10_urgent (passport / direct / single)

Question: জরুরি পাসপোর্ট করতে কত দিন লাগে?

Model: qwen3:8b; route: llm; time: 76.31 s; expected evidence present: None.

Answer:

জরুরী পাসপোর্ট করতে ৩ কর্মদিবসের মধ্যে পাসপোর্ট প্রদান করা হবে।

Sources: passport_f2c0d221c70d21f2_v2_0003, passport_9f4e9ffe9f2a07f4_v2_0004, passport_6f7d900581956bef_v2_0016

Retrieved sources:
- passport_f2c0d221c70d21f2_v2_0003: cleaned_md/Urgent Applications e-Passport.md
- passport_9f4e9ffe9f2a07f4_v2_0004: cleaned_md/ই-পাসপোর্ট ফরম পূরণের নির্দেশাবলী.md
- passport_6f7d900581956bef_v2_0016: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0011: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0031: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md
- passport_6f7d900581956bef_v2_0012: cleaned_md/সেবা প্রদান প্রতিশ্রুতি (Citizen's Charter) - ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর.md

## birth_01_documents (birth_death_registration / direct / single)

Question: জন্মনিবন্ধন করতে কী কী কাগজপত্র লাগে?

Model: qwen3:8b; route: controlled; time: 22.42 s; expected evidence present: None.

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

## birth_02_online_apply (birth_death_registration / direct / single)

Question: জন্মনিবন্ধন অনলাইনে কীভাবে করব?

Model: qwen3:8b; route: controlled; time: 24.56 s; expected evidence present: None.

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

## birth_03_birth_date_correction (birth_death_registration / direct / single)

Question: জন্মনিবন্ধনে জন্মতারিখ ভুল হলে কীভাবে সংশোধন করব?

Model: qwen3:8b; route: controlled; time: 28.12 s; expected evidence present: None.

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

## birth_04_name_spelling (birth_death_registration / direct / single)

Question: জন্মনিবন্ধনে নামের বানান ভুল হলে কী করব?

Model: qwen3:8b; route: controlled; time: 26.95 s; expected evidence present: None.

Answer:

নাম/ঠিকানা/তথ্য ভুল হলে জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করতে হবে।

তথ্য সংশোধনের জন্য যোগাযোগ মাধ্যম: জন্ম নিবন্ধনের তথ্য সংশোধনের আবেদন করতে হলে যোগাযোগের তথ্য সংযুক্ত থাকতে হবে।

যোগাযোগের তথ্য সংযুক্ত না থাকলে: মোবাইল নম্বর বা ইমেইল সংযুক্ত না থাকলে সংশ্লিষ্ট নিবন্ধন কার্যালয়ের সাথে যোগাযোগ করতে হবে।

জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা ইত্যাদি তথ্য সংশোধনের আবেদন ফি: ৫০ টাকা।

এই ডেটাসেটে নাম/ঠিকানা সংশোধনের পূর্ণ ধাপে-ধাপে প্রক্রিয়া নেই; তাই সংশ্লিষ্ট নিবন্ধন কার্যালয় বা BDRIS সংশোধন পোর্টালের নির্দেশনা অনুসরণ করা উচিত।

Sources: application_for_birth_information_correction_cleaned_010_01, application_for_birth_information_correction_cleaned_013_01, birth_and_death_registration_fees_cleaned_fee_row_05

Retrieved sources:
- notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01: unknown source
- application_for_birth_information_correction_cleaned_003_01: unknown source
- application_for_birth_information_correction_cleaned_013_01: unknown source
- application_for_birth_information_correction_cleaned_010_01: unknown source
- application_for_birth_information_correction_cleaned_008_01: unknown source
- application_for_birth_information_correction_cleaned_002_01: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source

## birth_05_lost (birth_death_registration / direct / single)

Question: জন্মনিবন্ধন হারিয়ে গেলে নতুন কপি কীভাবে পাব?

Model: qwen3:8b; route: controlled; time: 27.06 s; expected evidence present: None.

Answer:

জন্ম নিবন্ধন সনদ হারিয়ে গেলে বা নষ্ট হলে নিবন্ধকের কাছে সনদের প্রতিলিপির জন্য আবেদন করতে হবে। বিধি ১৩ অনুযায়ী, আবেদন পাওয়ার ৭ কার্য দিবসের মধ্যে জন্ম/মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করা হয়। প্রতিলিপির জন্য বিধি ২১ অনুযায়ী নির্ধারিত ফি প্রযোজ্য হতে পারে।

প্রাসঙ্গিক বিধি: (১) নিবন্ধিত কোন ব্যক্তির সনদ হারাইয়া গেলে বা নষ্ট হইলে, নিবন্ধক, উপ-বিধি (২) ও (৩) এর বিধান সাপেক্ষে, জমনি ফরম-৭ অনুযায়ী উক্ত ব্যক্তির আবেদন প্রাপ্তির ৭ (সাত) কার্য দিবসের মধ্যে জমনি ফরম-৩ ও জমনি ফরম-৬ অনুযায়ী জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপি প্রদান করিবেন। (২) বিধি ২১ এ নির্ধারিত ফিস প্রদান সাপেক্ষে, নিম্নবর্ণিত কোন ব্যক্তি জন্ম ও মৃত্যু নিবন্ধন সনদের প্রতিলিপির জন্য জমনি ফরম-৭ অনুযায়ী নিবন্ধকের নিকট আবেদন করিতে পারিবেন, যথা:
(ক) যাহার জন্য জন্ম সনদ প্রদান করা হইবে তাহার বয়স ১৮ (আঠার) বৎসর বা তদূর্ধ্ব হইলে তিনি স্বয়ং অথবা (খ) জন্ম তথ্য প্রদানকারী অথবা (গ) মৃত্যু তথ্য প্রদানকারী অথবা (ঘ) জন্ম বা মৃত্যু তথ্য দ্বারা সংক্ষুব্ধ ব্যক্তি। (৩) উপ-বিধি (২) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক যদি নিশ্চিত হন যে, উক্ত আবেদনপত্র যথাযথভাবে পূরণ করা হইয়াছে এবং ফিস প্রদান করা হইয়াছে তাহা হইলে তিনি আবেদনকারীর অংশ স্বাক্ষরপূর্বক উহা আবেদনকারীর নিকট হস্তান্তর করিবেন। (৪) উপ-বিধি (৩) এর অধীন আবেদনপত্র প্রাপ্তির পর নিবন্ধক সনদের প্রতিলিপি প্রস্তুত করিবেন এবং আবেদনকারীর অংশ গ্রহণ করিয়া সনদের প্রতিলিপি আবেদনকারীর নিকট হস্তান্তরের ব্যবস্থা করিবেন। (৫) প্রতিলিপি সনদের উপরিভাগে প্রতিলিপি বা উঁঢ়ষরপধঃব শব্দটি এবং, ক্ষেত্রমত, সংশোধিত সনদের ক্ষেত্রে সংশোধিত শব্দটি উল্লেখ থাকিবে এবং প্রথম বার জন্ম বা মৃত্যু নিবন্ধন সনদ যে তারিখে ইস্যু হইয়াছে প্রতিলিপি সনদ ইস্যুর সেই তারিখ বহাল থাকিবে ও প্রতিলিপি সনদ ইস্যুর তারিখ লিপিবদ্ধ করিতে হইবে।

Sources: birth_and_death_registration_rules_2018_বিধি_১৩_01

Retrieved sources:
- birth_and_death_registration_rules_2018_বিধি_১৩_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১২_03: unknown source
- birth_and_death_registration_rules_2018_বিধি_১২_01: unknown source
- bdris_faq_01_q12: unknown source
- birth_and_death_registration_act_2004_ধারা_১৫_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source

## birth_06_verify (birth_death_registration / direct / single)

Question: অনলাইনে জন্মনিবন্ধন যাচাই কীভাবে করব?

Model: qwen3:8b; route: controlled; time: 25.67 s; expected evidence present: None.

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

Sources: birth_registration_application_process_cleaned_017_01, know_this_01_cleaned_008_01, birth_and_death_registration_rules_2018_বিধি_১৯_03

Retrieved sources:
- know_this_01_cleaned_008_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_১৯_03: unknown source
- birth_registration_application_process_cleaned_017_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- bdris_faq_01_q02: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_04: unknown source

## birth_07_correction_fee (birth_death_registration / direct / single)

Question: জন্মনিবন্ধন সংশোধন করতে কত টাকা লাগে?

Model: qwen3:8b; route: controlled; time: 25.23 s; expected evidence present: None.

Answer:

জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা ইত্যাদি অন্যান্য তথ্য সংশোধনের জন্য আবেদন ফি: ৫০ টাকা

Sources: birth_and_death_registration_fees_cleaned_table_full, birth_and_death_registration_fees_cleaned_fee_row_05, birth_and_death_registration_fees_cleaned_fee_row_04

Retrieved sources:
- birth_and_death_registration_fees_cleaned_table_full: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_04: unknown source
- birth_and_death_registration_rules_2018_বিধি_২১_01: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_06: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_02: unknown source

## birth_08_birth_date_proof (birth_death_registration / direct / single)

Question: জন্মতারিখ সংশোধনের জন্য কী কী প্রমাণ লাগবে?

Model: qwen3:8b; route: llm; time: 97.17 s; expected evidence present: None.

Answer:

জন্মতারিখ সংশোধনের জন্য নিচগুলি প্রমাণ দাখিল করতে হবে:

- পিতা বা মাতার মৃত্যুর প্রমাণপত্র  
- পিতা বা মাতার পাসপোর্টের কপি (যদি বিদেশী নাগরিক)  
- অন্য যুক্তিগ্রাহ্য প্রমাণক যেটি ভুল জাতীয়তা ঠিক করতে পারে।

Sources: application_for_birth_information_correction_cleaned_009_01, notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01, application_for_birth_information_correction_cleaned_007_01

Retrieved sources:
- application_for_birth_information_correction_cleaned_009_01: unknown source
- notice_birth_and_death_registration_certificate_correction_steps_ocr_007_01: unknown source
- application_for_birth_information_correction_cleaned_007_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source
- application_for_birth_information_correction_cleaned_008_01: unknown source
- application_for_birth_information_correction_cleaned_006_01: unknown source

## birth_09_parent_name (birth_death_registration / direct / single)

Question: বাবা-মায়ের নাম ভুল থাকলে কীভাবে সংশোধন করব?

Model: qwen3:8b; route: controlled; time: 18.78 s; expected evidence present: None.

Answer:

নাম/ঠিকানা/তথ্য ভুল হলে জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করতে হবে।

পিতা বা মাতার নাম সংশোধন সংক্রান্ত নির্দেশনা: আপনার পিতা বা মাতার নাম সংশোধন করতে হলে নিম্নোক্ত নির্দেশনা অনুসরণ করতে হবে।

পরিস্থিতি ১: পিতা বা মাতার জন্ম নিবন্ধন নম্বর আছে: যদি আপনার পিতা বা মাতার জন্ম নিবন্ধন নম্বর থাকে, তাহলে প্রথমে তাদের জন্ম নিবন্ধন নম্বর ব্যবহার করে জন্ম নিবন্ধন তথ্য সংশোধনের আবেদন করে তাদের নাম সংশোধন করতে হবে।

যদি পূর্বে জন্ম নিবন্ধনে পিতা বা মাতার জন্ম নিবন্ধন নম্বর যুক্ত করা থাকে: আপনার জন্ম নিবন্ধন করার সময় যদি পিতা বা মাতার জন্ম নিবন্ধন নম্বর প্রদান করা হয়ে থাকে, তাহলে তাদের নাম সংশোধনের পর আপনার জন্ম নিবন্ধন সনদ পুনর্মুদ্রণ করলে সেখানে সংশোধিত নাম স্বয়ংক্রিয়ভাবে প্রদর্শিত হবে।

যদি পূর্বে জন্ম নিবন্ধনে পিতা বা মাতার জন্ম নিবন্ধন নম্বর যুক্ত করা না থাকে: আপনার জন্ম নিবন্ধন করার সময় যদি পিতা বা মাতার জন্ম নিবন্ধন নম্বর প্রদান করা না হয়ে থাকে, তাহলে আপনার জন্ম নিবন্ধন নম্বরের সাথে পিতা বা মাতার জন্ম নিবন্ধন নম্বর ম্যাপ করতে হবে।

ম্যাপিং সম্পন্ন হওয়ার পর জন্ম নিবন্ধন সনদ পুনর্মুদ্রণ করলে সেখানে সংশোধিত নাম প্রদর্শিত হবে।

জন্ম তারিখ ব্যতীত নাম, পিতার নাম, মাতার নাম, ঠিকানা ইত্যাদি তথ্য সংশোধনের আবেদন ফি: ৫০ টাকা।

Sources: application_for_birth_information_correction_cleaned_002_01, application_for_birth_information_correction_cleaned_003_01, application_for_birth_information_correction_cleaned_004_01, application_for_birth_information_correction_cleaned_005_01, birth_and_death_registration_fees_cleaned_fee_row_05

Retrieved sources:
- application_for_birth_information_correction_cleaned_008_01: unknown source
- application_for_birth_information_correction_cleaned_002_01: unknown source
- application_for_birth_information_correction_cleaned_006_01: unknown source
- application_for_birth_information_correction_cleaned_003_01: unknown source
- application_for_birth_information_correction_cleaned_005_01: unknown source
- application_for_birth_information_correction_cleaned_004_01: unknown source
- birth_and_death_registration_fees_cleaned_fee_row_05: unknown source

## birth_10_delivery_time (birth_death_registration / direct / single)

Question: জন্মনিবন্ধন করতে কত দিন সময় লাগে?

Model: qwen3:8b; route: llm; time: 114.26 s; expected evidence present: None.

Answer:

জন্মনিবন্ধন করতে ৪৫ দিনের মধ্যে আবেদন করতে হয়।

Sources: bdris_faq_02_q01, bdris_faq_01_q01, birth_and_death_registration_rules_2018_বিধি_৯_02

Retrieved sources:
- bdris_faq_02_q01: unknown source
- bdris_faq_01_q01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_02: unknown source
- birth_and_death_registration_rules_2018_বিধি_২০_01: unknown source
- birth_and_death_registration_rules_2018_বিধি_৯_04: unknown source
- birth_and_death_registration_act_2004_ধারা_৮_01: unknown source

## brta_01_documents (brta / direct / single)

Question: ড্রাইভিং লাইসেন্স করতে কী কী কাগজপত্র লাগবে?

Model: qwen3:8b; route: llm; time: 249.79 s; expected evidence present: None.

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

Model: qwen3:8b; route: llm; time: 107.23 s; expected evidence present: None.

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

## brta_03_learner (brta / direct / single)

Question: লার্নার ড্রাইভিং লাইসেন্স কীভাবে করব?

Model: qwen3:8b; route: llm; time: 215.19 s; expected evidence present: None.

Answer:

- আপনি `bsp.brta.gov.bd` ওয়েবসাইটে অনলাইনে আবেদন করুন।  
- আবেদন করতে হবে জাতীয় পরিচয়পত্র (NID), ছবি, মেডিকেল সার্টিফিকেট, ইউটিলিটি বিল এবং অন্যান্য প্রয়োজনীয় দখলকৃত ডকুমেন্টগুলি উপস্থাপন করুন।  
- আবেদন ফি অনলাইনে ভর্তি করুন (১ ক্যাটাগরি - ৫১৮ টাকা, ২ ক্যাটাগরি - ৭৪৮ টাকা)।  
- আপনার লার্নার ড্রাইভিং লাইসেন্স অনলাইন প্রিন্ট করে নিন।  
- ২/৩ মাস পড়াশুনার পর নির্ধারিত তারিখে নির্ধারিত কেন্দ্রে লিখিত, মৌখিক ও ফিল্ড টেস্ট দিবেন।  
- টেস্ট উত্তীর্ণ হওয়ার পর আপনার ড্রাইভিং লাইসেন্স প্রদান করা হবে।

Sources: brta_cbe22ab64acf3d03_v2_0003, brta_cbe22ab64acf3d03_v2_0004, brta_846a4041fe96a64e_v2_0011

Retrieved sources:
- brta_cbe22ab64acf3d03_v2_0003: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_cbe22ab64acf3d03_v2_0004: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_846a4041fe96a64e_v2_0011: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_09e8cbfff67f117e_v2_0005: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md
- brta_846a4041fe96a64e_v2_0002: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_cbe22ab64acf3d03_v2_0002: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md

## brta_04_delivery_time (brta / direct / single)

Question: ড্রাইভিং লাইসেন্স পেতে কত দিন সময় লাগে?

Model: qwen3:8b; route: llm; time: 95.49 s; expected evidence present: None.

Answer:

অপেশাদার শিক্ষানবিশ ড্রাইভিং লাইসেন্স প্রদানের জন্য ধাপ-৬ এ স্মার্ট কার্ড ড্রাইভিং লাইসেন্সটি পোস্ট অফিস/কুরিয়ার সার্ভিসের মাধ্যমে গ্রাহকের দোরগোড়ায় ০৭ দিনের মধ্যে প্রেরণ করা হইবে।

Sources: brta_4e08eb4e988d38e4_v2_0013, brta_4e08eb4e988d38e4_v2_0009, brta_846a4041fe96a64e_v2_0016

Retrieved sources:
- brta_4e08eb4e988d38e4_v2_0013: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0009: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_846a4041fe96a64e_v2_0016: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_4e08eb4e988d38e4_v2_0014: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_846a4041fe96a64e_v2_0007: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_cbe22ab64acf3d03_v2_0003: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md

## brta_05_test (brta / direct / single)

Question: BRTA-এর ড্রাইভিং পরীক্ষায় কী কী থাকে?

Model: qwen3:8b; route: llm; time: 213.01 s; expected evidence present: None.

Answer:

- **ডোপ টেস্ট:** Opioids, Amphetamines, Cannabis, Cocaine, Benzodiazepines এগুলো পরীক্ষা হয়।  
- **মেডিকেল ফিটনেস সার্টিফিকেট:** রেজিস্টার্ড মেডিকেল ফিজিশিয়ান দ্বারা প্রদত্ত হবে।  
- **ডোপ টেস্ট রিপোর্ট:** সরকারি ল্যাবরেটরি বা অনুমোদিত হাসপাতাল থেকে নেগেটিভ রিপোর্ট আবশ্যক।  
- **জাতীয় পরিচয়পত্র (NID):** সত্যায়িত কপি উপস্থাপন করতে হবে।  
- **নূন্যতম অষ্টম শ্রেণী পাসের প্রমানপত্র:** প্রয়োজন।  
- **পূর্ববর্তী ড্রাইভিং লাইসেন্সের অনুলিপি:** মানোন্নয়নের জন্য দরকার।

Sources: brta_57a7e75567f9a5c3_v2_0012, brta_4b8c25d391e48121_v2_0001, brta_57a7e75567f9a5c3_v2_0010

Retrieved sources:
- brta_57a7e75567f9a5c3_v2_0012: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_4b8c25d391e48121_v2_0001: fahim_brta/সেবাসমূহ/ড্রাইভিং ইন্সট্রাক্টর লাইসেন্স.md
- brta_57a7e75567f9a5c3_v2_0010: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md
- brta_4e08eb4e988d38e4_v2_0013: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0158: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_57a7e75567f9a5c3_v2_0004: brta/আইন, বিধি ও নীতিমালা/বিআরটিএ মধ্যম ও ভারী শ্রেণীর পেশাদার ড্রাইভিং লাইসেন্স নিয়ন্ত্রণ সংক্রান্ত নির্দেশিকা ও প্রবিধানমালা.md

## brta_06_renewal (brta / direct / single)

Question: ড্রাইভিং লাইসেন্সের মেয়াদ শেষ হলে কীভাবে নবায়ন করব?

Model: qwen3:8b; route: llm; time: 237.71 s; expected evidence present: None.

Answer:

ড্রাইভিং লাইসেন্সের মেয়াদ শেষ হলে নবায়ন করতে হবে নিচুন বিষয়গুলি:

- আপনার লাইসেন্সের মেয়াদ উত্তীর্ণ হওয়ার ১৫ দিনের মধ্যে অথবা পরে নির্ধারিত ফি (মেয়াদোত্তীর্ণের ১৫ দিনের মধ্যে ৪,২১২/- টাকা ও মেয়াদোত্তীর্ণের ১৫ দিন পরে প্রতি বছর ৫১৮/- টাকা) জমা দিন।  
- প্রয়োজনীয় কাগজপত্র একত্র করে বিআরটিএ নির্দিষ্ট সার্কেল অফিসে আবেদন করুন।  
- আবেদনপত্র ও কাগজপত্র ঠিক হওয়ার পর আপনার ডিজিটাল ছবি, ডিজিটাল স্বাক্ষর ও আঙুলের ছাপ দিয়ে বায়োমেট্রিকস নথিভূক্ত করুন।  
- স্মার্ট কার্ড প্রিন্ট হওয়ার পর আপনাকে এসএমএস মধ্য দিয়ে জানিয়ে দেয়া হবে।

Sources: brta_cbe22ab64acf3d03_v2_0009, brta_4e08eb4e988d38e4_v2_0014, brta_cbe22ab64acf3d03_v2_0010

Retrieved sources:
- brta_cbe22ab64acf3d03_v2_0009: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_4e08eb4e988d38e4_v2_0014: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_cbe22ab64acf3d03_v2_0010: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_4e08eb4e988d38e4_v2_0015: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0026: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_09e8cbfff67f117e_v2_0009: brta/বিআরটিএ সম্পর্কিত/বিআরটিএ এর সেবা প্রদান প্রতিশ্রুতি (সিটিজেন্স চার্টার).md

## brta_07_lost (brta / direct / single)

Question: ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?

Model: qwen3:8b; route: llm; time: 99.03 s; expected evidence present: None.

Answer:

আবেদনপত্র সঠিক বিবেচিত হওয়ার পরে, আবেদনকারীকে তাৎক্ষণিকভাবে প্রাপ্তিস্বীকার রসিদ প্রদান করা হবে। এছাড়া, 30 (ত্রিশ) দিনের মধ্যে ড্রাইভিং লাইসেন্স প্রদান করা হবে।

Sources: brta_4e08eb4e988d38e4_v2_0200, brta_4e08eb4e988d38e4_v2_0018, brta_4e08eb4e988d38e4_v2_0023

Retrieved sources:
- brta_4e08eb4e988d38e4_v2_0200: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0018: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0023: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_258cf38650a6332b_v2_0012: fahim_brta/ফরম/ফরম-৪(খ) মোটর ড্রাইভিং লাইসেন্স নবায়ন,প্রতিলিপি,শ্রেণি পরিবর্তন বা সংযোজন,ধরন পরিবর্তন,ঠিকানা পরিবর্তন,তথ্য সংশোধনের আবেদন.md
- brta_4e08eb4e988d38e4_v2_0025: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_cbe22ab64acf3d03_v2_0003: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md

## brta_08_correction (brta / direct / single)

Question: ড্রাইভিং লাইসেন্সে নাম বা জন্মতারিখ ভুল হলে কীভাবে ঠিক করব?

Model: qwen3:8b; route: llm; time: 183.51 s; expected evidence present: None.

Answer:

ড্রাইভিং লাইসেন্সে নাম অথবা জন্মতারিখ ভুল হলে নিচের পদক্ষেপগুলো গ্রহণ করুন:

- **ফরম-৪(খ)** এ আবেদন করুন যেখানে তথ্য সংশোধনের জন্য প্রয়োজনীয় ফরমটি ডাউনলোড করুন।  
- আবেদন করার সময় বর্তমান তথ্য ও প্রস্তাবিত সংশোধন দুইটি বৃত্তচিত্রে ছাপুন।  
- আবেদন করার সঙ্গে সঙ্গে আবেদনকারীর স্বাক্ষরও দিন।  
- আবেদন করার পর লাইসেন্স পুনর্মূল্যাঙ্কনের অপেক্ষা করুন।

Sources: brta_4e08eb4e988d38e4_v2_0237, brta_258cf38650a6332b_v2_0021, brta_00cf734ebafbc7c2_v2_0034

Retrieved sources:
- brta_4e08eb4e988d38e4_v2_0237: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_258cf38650a6332b_v2_0021: fahim_brta/ফরম/ফরম-৪(খ) মোটর ড্রাইভিং লাইসেন্স নবায়ন,প্রতিলিপি,শ্রেণি পরিবর্তন বা সংযোজন,ধরন পরিবর্তন,ঠিকানা পরিবর্তন,তথ্য সংশোধনের আবেদন.md
- brta_00cf734ebafbc7c2_v2_0034: fahim_brta/ফরম/ফরম-৪(ক) ড্রাইভিং লাইসেন্সের আবেদন.md
- brta_4e08eb4e988d38e4_v2_0016: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_00cf734ebafbc7c2_v2_0007: fahim_brta/ফরম/ফরম-৪(ক) ড্রাইভিং লাইসেন্সের আবেদন.md
- brta_4e08eb4e988d38e4_v2_0199: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md

## brta_09_online_apply (brta / direct / single)

Question: ড্রাইভিং লাইসেন্সের আবেদন অনলাইনে কীভাবে করব?

Model: qwen3:8b; route: llm; time: 196.18 s; expected evidence present: None.

Answer:

- এনআইডি ব্যবহার করে বিআরটিএ সার্ভিস পোর্টাল (BSP)-এ অ্যাকাউন্ট তৈরি করুন।  
- অনলাইনে আবেদন করতে ছবি, জাতীয় পরিচয়পত্র, ইউটিলিটি বিল, শিক্ষাগত যোগ্যতা ও ডোপ টেস্ট রিপোর্ট আপলোড করুন।  
- আবেদন নম্বর দেখে অপেক্ষা করুন এবং শিক্ষানবিশ ড্রাইভিং লাইসেন্স প্রাপ্ত হওয়ার পর ২/৩ মাস প্রশিক্ষণ গ্রহণ করুন।  
- প্রশিক্ষণের পর নির্ধারিত তারিখে লিখিত, মৌখিক ও ফিল্ড টেস্ট দিয়ে প্রশিক্ষণ সমাপ্ত করুন।

Sources: brta_846a4041fe96a64e_v2_0007, brta_cbe22ab64acf3d03_v2_0003, brta_846a4041fe96a64e_v2_0003

Retrieved sources:
- brta_846a4041fe96a64e_v2_0007: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_cbe22ab64acf3d03_v2_0003: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_846a4041fe96a64e_v2_0003: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_846a4041fe96a64e_v2_0011: fahim_brta/সেবাসমূহ/নতুন ড্রাইভিং লাইসেন্স ইস্যু.md
- brta_cbe22ab64acf3d03_v2_0004: fahim_brta/সেবাসমূহ/ড্রাইভিং লাইসেন্স ইস্যু ও নবায়ন.md
- brta_4e08eb4e988d38e4_v2_0148: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md

## brta_10_status (brta / direct / single)

Question: আমার ড্রাইভিং লাইসেন্সের বর্তমান স্ট্যাটাস কীভাবে দেখব?

Model: qwen3:8b; route: llm; time: 177.73 s; expected evidence present: None.

Answer:

আপনি আপনার ড্রাইভিং লাইসেন্সের বর্তমান স্ট্যাটাস দেখতে পারেনঃ

- **বিআরটিএ ওয়েবসাইটে** ভ্রমণ করুন।  
- অথবা **ড্রাইভিং লাইসেন্স নম্বর** দিয়ে খোজ চালান।  
- আপনার ড্রাইভিং লাইসেন্সের মেয়াদ, ইস্যুকারী কর্তৃপক্ষ এবং অবস্থা দেখতে পারবেন।  
- আপনার ঠিকানা বা অন্যান্য তথ্য হলে ফরম-৫ ব্যবহার করুন।

Sources: brta_4e08eb4e988d38e4_v2_0237, brta_4e08eb4e988d38e4_v2_0203, brta_a207b925ed0dc4a9_v2_0020

Retrieved sources:
- brta_4e08eb4e988d38e4_v2_0237: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_4e08eb4e988d38e4_v2_0203: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_a207b925ed0dc4a9_v2_0020: fahim_brta/ফরম/ফরম-৩ শিক্ষানবিশ ড্রাইভিং লাইসেন্স.md
- brta_4e08eb4e988d38e4_v2_0205: brta/আইন, বিধি ও নীতিমালা/সড়ক পরিবহণ বিধিমালা, ২০২২.md
- brta_00cf734ebafbc7c2_v2_0017: fahim_brta/ফরম/ফরম-৪(ক) ড্রাইভিং লাইসেন্সের আবেদন.md
- brta_00cf734ebafbc7c2_v2_0026: fahim_brta/ফরম/ফরম-৪(ক) ড্রাইভিং লাইসেন্সের আবেদন.md

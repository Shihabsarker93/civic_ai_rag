# Manually selected evidence diagnostic

Generation-only experiment, not end-to-end retrieval or accuracy evaluation.
Evidence relevance was inspected against saved corpus text, not independently verified against current government rules.
Controlled answer paths, retrieval, reranking and language fallback are bypassed intentionally. Raw model output is retained.
Source IDs list supplied evidence; they are not verified claim-level citations. Manual correctness review is pending.

## passport_01_documents / qwen3:8b

নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?

Time: 121.71 s; finish: stop; route: diagnostic_llm

* **ক্রমিক ১:** আবেদনপত্রের সারংশের প্রিন্ট কপি (অ্যাপয়েন্টমেন্ট সহ)  
* **ক্রমিক ২:** সনাক্তকরণ নথির প্রিন্ট কপি (জাতীয় পরিচয় পত্র/ জন্ম নিবন্ধন নং)  
* **ক্রমিক ৩:** পেমেন্ট স্লিপ (অফলাইন পেমেন্টের জন্য)  
* **ক্রমিক ৪:** পূর্ববর্তী পাসপোর্ট এবং ডাটা পেজের প্রিন্ট কপি (যদি থাকে)  
* **ক্রমিক ৫:** সরকারি চাকরিজীবীদের ক্ষেত্রে GO/NOC (যদি থাকে)  
* **ক্রমিক ৭:** তথ্য সংশোধনের ক্ষেত্রে প্রয়োজনীয় কাগজপত্র (যদি থাকে)

Sources: passport_73ac41f2327257f9_v2_0004

## passport_02_fee / qwen3:8b

পাসপোর্ট বানাতে কত টাকা লাগে?

Time: 173.66 s; finish: stop; route: diagnostic_llm

পাসপোর্ট বানাতে খরচ হয় মূলত পাসপোর্টের ধরন এবং ডেলিভারি অপশনের উপর। নিচে দেওয়া হল কিছু গড় ফি:

- ৪৮ পেজ ও ৫ বছর বৈধতা থাকলে আমলাতন্ত্র ফি ঘটে টক ৪,০২৫ (সাধারণ), টক ৬,৩২৫ (এক্সপ্রেস) এবং টক ৮,৬২৫ (সুপার এক্সপ্রেস)
- ৪৮ পেজ ও ১০ বছর বৈধতা থাকলে আমলাতন্ত্র ফি ঘটে টক ৫,৭৫০ (সাধারণ), টক ৮,০৫০ (এক্সপ্রেস) এবং টক ১০,৩৫০ (সুপার এক্সপ্রেস)
- ৬৪ পেজ ও ৫ বছর বৈধতা থাকলে আমলাতন্ত্র ফি ঘটে টক ৬,৩২৫ (সাধারণ), টক ৮,৬২৫ (এক্সপ্রেস) এবং টক ১২,০৭৫ (সুপার এক্সপ্রেস)
- ৬৪ পেজ ও ১০ বছর বৈধতা থাকলে আমলাতন্ত্র ফি ঘটে টক ৮,০৫০ (সাধারণ), টক ১০,৩৫০ (এক্সপ্রেস) এবং টক ১৩,৮০০ (সুপার এক্সপ্রেস)

Sources: passport_12e10027cfdfeeee_v2_0007, passport_12e10027cfdfeeee_v2_0008, passport_12e10027cfdfeeee_v2_0009, passport_12e10027cfdfeeee_v2_0010

## brta_07_lost / qwen3:8b

ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?

Time: 85.23 s; finish: stop; route: diagnostic_llm

ড্রাইভিং লাইসেন্স হারিয়ে গেলে নতুন লাইসেন্স পেতে হলে অবশ্যই নিচের কাগজপত্রগুলো জমা দিতে হবে:

- **আবেদনপত্র:** নির্ধারিত ফরমে আবেদন।  
- **জিডি ও ট্রাফিক ক্লিয়ারেন্স:** জিডি কপি এবং ট্রাফিক ক্লিয়ারেন্স।  
- **ফি জমাদানের রশিদ:** বিআরটিএ'র নির্ধারিত ব্যাংকে ফি জমা দেওয়ার রশিদ।  
- **ছবি:** সদ্য তোলা ১ কপি পাসপোর্ট সাইজ ছবি।

Sources: brta_cbe22ab64acf3d03_v2_0013

## passport_01_documents / llama3

নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?

Time: 64.91 s; finish: stop; route: diagnostic_llm

নতুন পাসপোর্ট করতে লাগবে:

1. আবেদনপত্রের সারংশের প্রিন্ট কপি
2. সনাক্তকরণ নথির প্রিন্ট কপি
3. পেমেন্ট স্লিপ (Offline Payment only)
4. পূর্ববর্তী পাসপোর্ট এবং ডাটা পেজের প্রিন্ট কপি (if available)
5. সরকারি চাকরিজীবীদের ক্ষেত্রে GO/NOC (if applicable)

Note: These documents are required to be carried while enrolling at Passport offices, as per the evidence provided.

Sources: passport_73ac41f2327257f9_v2_0004

## passport_02_fee / llama3

পাসপোর্ট বানাতে কত টাকা লাগে?

Time: 57.71 s; finish: stop; route: diagnostic_llm

পাসপোর্ট বানাতে কত টাকা লাগে?

আমি দেখছি যে একটি পাসপোর্ট বানাতে হলে ভিন্ন রকম ফি লাগে। উদাহরণস্বরূপ, একটি e-Passport with 48 pages and 5 years validity-এর জন্য অনুমান 4,025 টাকা (Regular delivery) থেকে 8,625 টাকা (Super Express delivery)-এর মধ্যে হওয়া যেতে পারে।

(Translation: How much money is needed to make a passport? I see that making a passport requires different fees. For example, an e-Passport with 48 pages and 5 years validity can cost between Tk 4,025 (Regular delivery) and Tk 8,625 (Super Express delivery).

Sources: passport_12e10027cfdfeeee_v2_0007, passport_12e10027cfdfeeee_v2_0008, passport_12e10027cfdfeeee_v2_0009, passport_12e10027cfdfeeee_v2_0010

## brta_07_lost / llama3

ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?

Time: 23.08 s; finish: stop; route: diagnostic_llm

ড্রাইভিং লাইসেন্স হারিয়ে গেলে আপনাকে অবশ্যই উকিল করতে হবে।

(Note: The retrieved source directly answers the question.)

Sources: brta_cbe22ab64acf3d03_v2_0013

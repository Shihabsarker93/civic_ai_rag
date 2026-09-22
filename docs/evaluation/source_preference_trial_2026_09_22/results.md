# Source-preference trial

Frozen-evidence generation experiment, not an end-to-end accuracy benchmark.
Sources are supplied context IDs, not verified claim-level citations.

## passport_01_documents / baseline

নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?

Model: qwen3:8b; time: 148.88 s; route: llm
Finish reason: stop

- **ক.** ডেলিভারি স্লিপ (Delivery Slip)।  
- **খ.** সন্তানের পাসপোর্ট হলে (১২ বছরের কম): অভিভাবকের NID/পাসপোর্ট।  
- **গ.** প্রতিনিধি দিয়ে সংগ্রহ করতে চাইলে: আবেদনকারীর স্বাক্ষরযুক্ত অনুমোদনপত্র (Authorization Letter) এবং প্রতিনিধির NID।  
- **ঘ.** পূর্বের মূল পাসপোর্ট।

Sources: passport_23d845d3ab38ea43_v2_0040, passport_73ac41f2327257f9_v2_0004, passport_729010959c882773_v2_0003

## passport_01_documents / neutral_prompt

নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?

Model: qwen3:8b; time: 156.53 s; route: llm
Finish reason: stop

- **ক.** ডেলিভারি স্লিপ (Delivery Slip)।  
- **খ.** সন্তানের পাসপোর্ট হলে (১২ বছরের কম): অভিভাবকের NID/পাসপোর্ট।  
- **গ.** প্রতিনিধি দিয়ে সংগ্রহ করতে চাইলে: আবেদনকারীর স্বাক্ষরযুক্ত অনুমোদনপত্র (Authorization Letter) এবং প্রতিনিধির NID।  
- **ঘ.** পূর্বের মূল পাসপোর্ট।

Sources: passport_23d845d3ab38ea43_v2_0040, passport_73ac41f2327257f9_v2_0004, passport_729010959c882773_v2_0003

## passport_02_fee / baseline

পাসপোর্ট বানাতে কত টাকা লাগে?

Model: qwen3:8b; time: 134.98 s; route: llm
Finish reason: stop

পাসপোর্ট বানাতে মূলত নিচের প্রকাশিত ফি হবে:

- **সাধারণ ফি:** ৫০০ টাকা + ১৫% ভ্যাট = ৫৭৫ টাকা  
- **জরুরি ফি:** ১০,০০০ টাকা + ১৫% ভ্যাট = ১১,৫০০ টাকা

যদি আপনি ই-পাসপোর্ট চাওয়া হয় তবে ফি হবে:

- **সাধারণ ডেলিভারি (২১ দিন):** ৩,৪৫০ টাকা  
- **জরুরি ডেলিভারি (১১ দিন):** ৬,৯০০ টাকা  
- **সুপার জরুরি ডেলিভারি (৮ দিন):** ১০,৩৫০ টাকা

Sources: passport_6f7d900581956bef_v2_0016, passport_12e10027cfdfeeee_v2_0010, passport_5eb6c21efe103a4f_v2_0026

## passport_02_fee / neutral_prompt

পাসপোর্ট বানাতে কত টাকা লাগে?

Model: qwen3:8b; time: 95.6 s; route: llm
Finish reason: stop

পাসপোর্ট বানাতে মূলত নিচের ফি প্রয়োগ হয়:

- **সাধারণ ফি:** ৫০০ টাকা + ১৫% ভ্যাট = **৬৫০ টাকা**
- **জরুরি ফি:** ১০,০০০ টাকা + ১৫% ভ্যাট = **১১,৫০০ টাকা**

টাকা অবশ্যই আবেদনকালে পরিশোধ করতে হবে।

Sources: passport_6f7d900581956bef_v2_0016, passport_12e10027cfdfeeee_v2_0010, passport_5eb6c21efe103a4f_v2_0026

## brta_07_lost / baseline

ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?

Model: qwen3:8b; time: 86.88 s; route: llm
Finish reason: stop

আবেদনপত্র সঠিক বিবেচিত হওয়ার পরে, আবেদনকারীকে তাৎক্ষণিকভাবে প্রাপ্তিস্বীকার রসিদ প্রদান করা হবে। এছাড়া, 30 (ত্রিশ) দিনের মধ্যে ড্রাইভিং লাইসেন্স প্রদান করা হবে।

Sources: brta_4e08eb4e988d38e4_v2_0200, brta_4e08eb4e988d38e4_v2_0018, brta_4e08eb4e988d38e4_v2_0023

## brta_07_lost / neutral_prompt

ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?

Model: qwen3:8b; time: 43.1 s; route: llm
Finish reason: stop

আবেদনপত্র সঠিক বিবেচিত হওয়ার পরে, আবেদনকারীকে তাৎক্ষণিকভাবে প্রাপ্তিস্বীকার রসিদ প্রদান করা হবে। এছাড়া, 30 (ত্রিশ) দিনের মধ্যে ড্রাইভিং লাইসেন্স প্রদান করা হবে।

Sources: brta_4e08eb4e988d38e4_v2_0200, brta_4e08eb4e988d38e4_v2_0018, brta_4e08eb4e988d38e4_v2_0023

title: "Bangladesh Machine Readable Passport (MRP) Online Application Guide 2012"
original_title_bn: "মেশিন রিডেবল পাসপোর্ট অনলাইন নির্দেশিকা'২০১২"
document_id: "BD-MRP-GUIDE-2012-V1"
jurisdiction: "Bangladesh (BD)"
issuing_authority: "Department of Immigration and Passports (DIP) / ইমিগ্রেশন ও পাসপোর্ট অধিদপ্তর"
document_type: "Official Application Guidelines & Field Specifications"
effective_date: "2012-01-01"
language: "bilingual (en, bn)"
rag_metadata:
chunk_strategy: "hierarchical_markdown_section_split"
context_denormalized: true
embedding_optimized: true
primary_entity: "Bangladesh Machine Readable Passport (MRP)"
tags:

* Bangladesh Passport

* MRP Online Application

* মেশিন রিডেবল পাসপোর্ট

* DIP Guidelines 2012

* Passport Form Field Rules

* Challan Payment

# Bangladesh Machine Readable Passport (MRP) Online Application Guide (2012)

*মেশিন রিডেবল পাসপোর্ট অনলাইন নির্দেশিকা'২০১২*

## 1. Document Overview & General Instructions | বিবরণ ও সাধারণ নির্দেশাবলী

### 1.1 Context & Scope | প্রসঙ্গ ও আওতা

* **Context**: Official specification and filling instructions for the online Machine Readable Passport (MRP) application form implemented by the Department of Immigration and Passports (DIP), Ministry of Home Affairs, Government of the People's Republic of Bangladesh.

* **Target Audience**: Applicants submitting MRP forms online within Bangladesh or via Bangladesh Foreign Missions abroad, as well as RAG/QA automated knowledge bases.

* **Language Policy**: Primary data entry for text fields must be completed in **English (CAPITAL LETTERS)** unless specified for Bengali script fields.

### 1.2 Core Rules for Online Form Submission | অনলাইন ফরম পূরণের মৌলিক নিয়মাবলী

1. **Self-Attestation & Accuracy**: All information provided must strictly match official identification documents: National ID (NID) Card or 17-digit Digitized Birth Registration Certificate (BRC).

2. **Name Matching**: The applicant's name must be entered in capital English letters matching previous educational certificates, NID, or official civil status records.

3. **Draft Retention & Expiry**: Online draft applications remain accessible in the DIP portal system for 15 days prior to final submission and payment verification.

4. **Physical Submission Requirement**: Online submission MUST be followed by a physical visit to the designated Regional Passport Office (RPO) or Bangladesh Mission for biometric data capture (photograph, 10 fingerprints, and digital signature).

## 2. Field-Level Application Specifications | ক্ষেত্র-ভিত্তিক ফরম পূরণের নির্দেশাবলী

### 2.1 Section A: Personal Information | ব্যক্তিগত তথ্যাবলী

#### Field A1: Application Type | আবেদনের ধরন

* **Context**: Specifies whether the application is a fresh issuance or a renewal/re-issue.

* **Field Label (EN)**: Application Type

* **Field Label (BN)**: আবেদনের ধরন

* **Allowed Values**:

  * `NEW ISSUE` / নতুন পাসপোর্ট

  * `RE-ISSUE` / পুনঃইস্যু

  * `DUPLICATE` (In case of lost or damaged passport) / হারানো বা ক্ষতিগ্রস্ত

* **RAG Context Note**: Re-issue and Duplicate applications require previous MRP/handwritten passport details in Section D.

#### Field A2: Applicant's Name | আবেদনকারীর নাম

* **Context**: The legal name of the applicant.

* **Field Label (EN)**: Full Name / Given Name & Surname

* **Field Label (BN)**: আবেদনকারীর নাম (প্রদেয় নাম ও বংশগত নাম)

* **Data Format**: Uppercase ASCII characters (A-Z). No special symbols, prefixes, or titles (e.g., MD., DR., ALHAJ, SIR are prohibited unless part of the official legal name on NID/BRC).

* **Validation Rule**: Max 45 characters across Given Name and Surname.

#### Field A3: Date of Birth | জন্ম তারিখ

* **Context**: Official birth date of the applicant.

* **Field Label (EN)**: Date of Birth (DOB)

* **Field Label (BN)**: জন্ম তারিখ

* **Data Format**: `YYYY-MM-DD` or `DD/MM/YYYY`.

* **Validation Rule**: Must match NID Card or 17-digit BRC exactly.

#### Field A4: Place of Birth | জন্মস্থান

* **Context**: Geographic origin of the applicant.

* **Field Label (EN)**: District of Birth / Country of Birth

* **Field Label (BN)**: জন্ম জেলা / জন্ম দেশ

* **Rules**: If born in Bangladesh, select the home district (e.g., Dhaka, Chittagong, Sylhet). If born abroad, select the country of birth.

#### Field A5: Gender | লিঙ্গ

* **Field Label (EN)**: Gender

* **Field Label (BN)**: লিঙ্গ

* **Allowed Values**: `MALE` (পুরুষ), `FEMALE` (মহিলা), `OTHERS` (অন্যান্য).

#### Field A6: National ID or Birth Registration Number | জাতীয় পরিচয়পত্র বা জন্ম নিবন্ধন নম্বর

* **Context**: Primary civil registration identifier.

* **Field Label (EN)**: National ID No. / Birth Registration Certificate No.

* **Field Label (BN)**: জাতীয় পরিচয়পত্র নম্বর / জন্ম সনদের নম্বর

* **Validation Rules**:

  * National ID (NID): Must be 10, 13, or 17 digits.

  * Birth Registration Certificate (BRC): Must be a 17-digit online verifiable number.

#### Field A7: Father's & Mother's Details | পিতা ও মাতার বিবরণ

* **Field Label (EN)**: Father's Name, Father's Nationality, Mother's Name, Mother's Nationality.

* **Field Label (BN)**: পিতার নাম, পিতার জাতীয়তা, মাতার নাম, মাতার জাতীয়তা.

* **Rules**: Must match NID/BRC records. If deceased, do not prefix with "LATE" or "মৃত" unless registered as such in official documents.

#### Field A8: Marital Status & Spouse Details | বৈবাহিক অবস্থা ও স্বামী/স্ত্রীর বিবরণ

* **Field Label (EN)**: Marital Status (Single, Married, Divorced, Widowed)

* **Field Label (BN)**: বৈবাহিক অবস্থা (অবিবাহিত, বিবাহিত, বিবাহবিচ্ছিন্ন, বিধবা/বিপত্নীক)

* **Rules**: If `MARRIED`, Spouse's Name and Nationality are mandatory fields. Marriage certificate (Nikkahnama) may be requested.

#### Field A9: Profession / Occupation | পেশা

* **Field Label (EN)**: Profession

* **Field Label (BN)**: পেশা

* **Allowed Values**: Government Service, Private Service, Business, Student, Housewife, Unemployed, Medical Practitioner, Engineer, Lawyer, Retired, Others.

* **Documentation Requirement**:

  * Government Service/Autonomous body employees must submit NOC (No Objection Certificate) or GO (Government Order).

  * Students must submit a valid Student ID copy.

### 2.2 Section B: Address Details | ঠিকানা বিবরণী

#### Field B1: Permanent Address | স্থায়ী ঠিকানা

* **Context**: Applicant's legal permanent residence in Bangladesh.

* **Field Label (EN)**: Permanent Address (Village/House/Road, District, Upazila/Thana, Post Office, Police Station).

* **Field Label (BN)**: স্থায়ী ঠিকানা (গ্রাম/বাসা/রাস্তা, জেলা, উপজেলা/থানা, ডাকঘর, পুলিশ স্টেশন).

* **RAG Context Note**: Mandatory for police verification in Bangladesh unless applicant holds a valid NID with matching permanent address.

#### Field B2: Present Address | বর্তমান ঠিকানা

* **Context**: Location where the applicant currently resides.

* **Field Label (EN)**: Present Address

* **Field Label (BN)**: বর্তমান ঠিকানা

* **Rules**: Police verification will be conducted at the Present Address if different from Permanent Address.

#### Field B3: Emergency Contact Details | জরুরি যোগাযোগের তথ্য

* **Context**: Person to contact in case of emergency.

* **Field Label (EN)**: Emergency Contact Person (Name, Relationship, Address, Telephone/Mobile, Email).

* **Field Label (BN)**: জরুরি যোগাযোগকারী ব্যক্তির নাম, সম্পর্ক, ঠিকানা, মোবাইল নম্বর.

* **Allowed Relationships**: Father, Mother, Spouse, Brother, Sister, Relative, Legal Guardian.

### 2.3 Section C: Passport Type & Previous Passport Info | পাসপোর্টের ধরন ও পূর্ববর্তী পাসপোর্টের তথ্য

#### Field C1: Passport Type | পাসপোর্টের ধরন

* **Field Label (EN)**: Type of Passport Requested

* **Field Label (BN)**: পাসপোর্টের প্রকার

* **Allowed Values**:

  * `ORDINARY` (সাধারণ) - Green cover for general citizens.

  * `OFFICIAL` (সরকারি) - Blue cover for eligible government employees.

  * `DIPLOMATIC` (কূটনৈতিক) - Red cover for diplomats and high officials.

#### Field C2: Previous Passport Information | পূর্ববর্তী পাসপোর্টের বিবরণ

* **Context**: Mandatory for Re-issue or Lost Passport applications.

* **Field Labels**:

  * Previous Passport No. (পূর্ববর্তী পাসপোর্ট নম্বর)

  * Place of Issue (প্রদানের স্থান)

  * Date of Issue (প্রদানের তারিখ)

  * Expiry Date (মেয়াদ উত্তীর্ণের তারিখ)

### 2.4 Section D: Fee Payment Details | ফি প্রদান বিবরণী

#### Field D1: Payment & Bank Challan Specifications | ব্যাংক চালানের তথ্য

* **Context**: Payment verification for processing fees.

* **Field Labels (EN/BN)**:

  * Bank Name (ব্যাংকের নাম) - e.g., Sonali Bank, Premier Bank, Bank Asia, One Bank, Trust Bank, Dhaka Bank.

  * Branch Name (শাখার নাম)

  * Payment Mode (অনলাইন/চালান/পিও)

  * Challan / Receipt No (চালান বা ট্রানজেকশন নম্বর)

  * Date of Payment (টাকা জমাদানের তারিখ)

  * Amount Paid (জমাকৃত টাকার পরিমাণ)

#### Field D2: Fee Structure (2012 Standard Schedule) | ফি এর হার (২০১২ নির্দেশিকা অনুযায়ী)

* **Regular Delivery (সাধারণ ডেলিভারি - 21 Days)**:

  * Ordinary Passport Fee: BDT 3,000 + 15% VAT = **BDT 3,450**

* **Express Delivery (জরুরি ডেলিভারি - 11 Days)**:

  * Ordinary Passport Fee: BDT 6,000 + 15% VAT = **BDT 6,900**

## 3. Required Enclosures & Verification | প্রয়োজনীয় সংযুক্তি ও সত্যায়ন

### 3.1 Document Checklist | প্রয়োজনীয় দলিলের তালিকা

1. **Printed Online Application Form**: Summary page containing the Online Application ID and barcode.

2. **Identification Proof**:

   * For adults (18+): Original NID card copy or 17-digit online BRC.

   * For minors (Under 18): 17-digit BRC copy + Father's and Mother's NID copies + 3R size photograph.

3. **Payment Receipt**: Original Sonali Bank / designated bank deposit slip/challan copy.

4. **Previous Passport**: Original old passport + photocopy of information pages (for Re-issue).

5. **NOC / GO**: Mandatory for Government, Semi-Government, or Autonomous organization employees.

6. **GD (General Diary) Copy**: Mandatory for lost passport applications, certified by the local police station.

### 3.2 Attestation Rules | সত্যায়ন নিয়মাবলী

* All submitted copies of NID, BRC, and photographs must be attested by a Gazetted Officer (Class-1), University Teacher, MP, Mayor, City Corporation Councilor, or Union Parishad Chairman.

* The attestor's name, designation, seal, and official contact number must be clearly visible on the document.

## 4. Biometric Enrollment & Processing Workflow | বায়োমেট্রিক ও প্রক্রিয়াকরণ ধাপসমূহ

```
[Online Application Submission] 
             │
             ▼
[Payment at Authorized Bank / Online]
             │
             ▼
[Visit Regional Passport Office (RPO)]
             │
             ▼
[Document Verification at Counter]
             │
             ▼
[Biometric Enrollment: Photo, 10 Fingerprints, Digital Signature]
             │
             ▼
[Police Verification (SB / DSB)]
             │
             ▼
[Passport Printing & Quality Control]
             │
             ▼
[Collection by Applicant with Enrolment Slip]

```

### 4.1 Steps at Regional Passport Office (RPO)

1. **Queue & Verification**: Present printed online application form along with original documents and bank challan at the verification counter.

2. **Biometric Capture**: Proceed to the biometric booth for digital facial photo, 10-fingerprint scanning, and electronic signature capture.

3. **Receipt of Delivery Slip**: Obtain the physical **Enrolment Slip / Delivery Slip** containing the Enrolment ID and tentative delivery date.

4. **Tracking**: Track status online using the Enrolment ID or Application ID.

## 5. Frequently Asked Questions (FAQ) & Answers | প্রশ্ন ও উত্তর

### Q1: Can I correct my name or date of birth during an online MRP application?

**Answer**: No. The name and date of birth in the MRP application must strictly align with your National ID (NID) or 17-digit Birth Registration Certificate (BRC). Any alterations to key personal details require prior correction of the underlying NID/BRC records before submitting the passport application.

### Q2: What should I do if my passport is lost?

**Answer**: File a General Diary (GD) report at the nearest police station immediately. When filling out the online MRP form, select `DUPLICATE` as the application type, enter the lost passport number, and present the original GD copy along with your application at the RPO.

### Q3: Are government employees required to undergo police verification?

**Answer**: Government employees who submit an official No Objection Certificate (NOC) or Government Order (GO) in the prescribed format are generally exempt from pre-issuance police verification, enabling faster processing.

*End of Preprocessed Markdown Document — BD-MRP-GUIDE-2012-V1*
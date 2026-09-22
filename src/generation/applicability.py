"""Conservative lexical exclusion of explicit service/action conflicts.

Unknown labels are retained for the model to assess, not declared relevant.
These rules apply to service categories, never exact evaluation questions or IDs.
"""
import re
import unicodedata


ACTION_PATTERNS = {
    "collection": r"সংগ্রহ|collect(?:ion)?|ডেলিভারি স্লিপ|delivery slip",
    "renewal": r"নবায়ন|নবায়ন|renew",
    "replacement": r"হারিয়ে|হারিয়ে|হারালে|হারানো|lost|duplicate|প্রতিলিপি",
    "correction": r"সংশোধন|correct|বানান ভুল|নাম ভুল|তারিখ ভুল",
    "status": r"স্ট্যাটাস|status|অবস্থা|যাচাই|verification",
    "application": r"আবেদন|application|apply|enrol|enroll",
}
SUBJECT_PATTERNS = {
    "passport": r"পাসপোর্ট|পাসপোর্ট|passport",
    "identity_certificate": r"certificate of identity|বিদেশীদের পরিচিতি|বিদেশিদের পরিচিতি",
    "licence": r"লাইসেন্স|licen[cs]e",
    "fitness": r"ফিটনেস|fitness",
    "vehicle_registration": r"মোটরযান রেজিস্ট্রেশন|মোটরযান নিবন্ধন|vehicle registration",
    "birth": r"জন্ম\s*নিবন্ধন|জন্মসনদ|birth registration|birth certificate",
    "death": r"মৃত্যু\s*নিবন্ধন|মৃত্যুসনদ|death registration|death certificate",
}


def labels(text, patterns):
    text = unicodedata.normalize("NFC", text).casefold()
    return {label for label, pattern in patterns.items() if re.search(pattern, text)}


def filter_applicable(query, contexts):
    query = unicodedata.normalize("NFC", query)
    actions = labels(query, ACTION_PATTERNS)
    # Explicit special actions take precedence over the generic word "application".
    if actions - {"application"}:
        actions.discard("application")
    if not actions and re.search(r"নতুন|বানাতে|করতে|করব|করবো", query):
        actions = {"application"}
    subjects = labels(query, SUBJECT_PATTERNS)
    kept, rejected = [], []
    for context in contexts:
        metadata = context.get("metadata", {})
        content = context["content"]
        leaf = str(metadata.get("section_title") or metadata.get("title") or "").split(">")[-1]
        questions = " ".join(line for line in content.splitlines()
                             if re.search(r"English Question|Bengali Question|\*\*প্রশ্ন", line, re.I))
        topic = leaf + " " + questions
        source_actions = labels(topic, ACTION_PATTERNS)
        source_subjects = labels(topic, SUBJECT_PATTERNS)
        reason = None
        if subjects and source_subjects and not subjects.intersection(source_subjects):
            reason = "different_service"
        elif actions and source_actions and not actions.intersection(source_actions):
            reason = "different_action"
        elif re.search(r"জন্ম\s*তারিখ|date of birth", query, re.I) and re.search(
                r"রেজিস্ট্রেশন.*ইস্যু.*তারিখ|registration.*issue.*date", topic, re.I) and not re.search(
                r"জন্ম\s*তারিখ|date of birth", topic, re.I):
            reason = "different_date_field"
        if reason:
            rejected.append({"source_id": str(context["id"]), "reason": reason})
        else:
            kept.append(context)
    return kept, rejected

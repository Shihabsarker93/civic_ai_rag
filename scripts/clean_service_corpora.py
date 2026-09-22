"""Prepare reversible source-preserving cleanup candidates, without publishing an index."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.manage_experimental_domains import digest, parse_markdown, read_chunks, section_spans, write_chunks, write_json
from scripts.corpus_structure import document_findings, packed_spans, scope_spans

VERSION = "service_cleanup_v4"
PREAMBLE_FIELDS = {
    'title', 'original_title_bn', 'document_id', 'source_pdf', 'jurisdiction',
    'issuing_authority', 'document_type', 'effective_date', 'language', 'date',
    'rag_metadata', 'chunk_strategy', 'context_denormalized', 'embedding_optimized',
    'primary_entity', 'tags', 'keywords', 'enabling_act', 'category', 'target_audience',
}
# Search vocabulary describes document sections, never supplies facts to the generator.
VOCABULARY = [
    (r"e[- ]?passport|ই[- ]?পাসপোর্ট", "ই-পাসপোর্ট e-passport"),
    (r"\bmrp\b|machine readable passport|এমআরপি", "এমআরপি MRP"),
    (r"certificate of identity|পরিচিতি সনদ", "বিদেশীদের পরিচিতি সনদ certificate of identity"),
    (r"driving licen[cs]e|ড্রাইভিং লাইসেন্স", "ড্রাইভিং লাইসেন্স driving licence"),
    (r"learner|লার্নার|শিক্ষানবিশ", "শিক্ষানবিশ লার্নার learner licence"),
    (r"ইন্সট্রাক্টর|ইনস্ট্রাক্টর|instructor", "প্রশিক্ষক instructor"),
    (r"renewal|নবায়ন|নবায়ন", "নবায়ন renewal"),
    (r"documents|কাগজপত্র|চেকলিস্ট", "প্রয়োজনীয় কাগজপত্র documents"),
    (r"collection|সংগ্রহ", "সংগ্রহ collection"),
    (r"enrolment|enrollment|এনরোলমেন্ট", "এনরোলমেন্ট enrolment"),
    (r"fees?|ফি(?:\s|$)|ফিস", "ফি খরচ fees"),
    (r"timelines?|delivery time|সময়সীমা|সময়সীমা", "বিতরণের সময়সীমা delivery timeline"),
    (r"duplicate|ডুপ্লিকেট|প্রতিলিপি", "প্রতিলিপি ডুপ্লিকেট হারানো duplicate replacement"),
    (r"status|স্ট্যাটাস|অগ্রগতি", "আবেদনের অবস্থা স্ট্যাটাস status"),
    (r"correction|সংশোধন", "তথ্য সংশোধন correction"),
    (r"inside bangladesh", "বাংলাদেশের ভিতরে inside Bangladesh"),
    (r"mission|মিশন", "বিদেশে বাংলাদেশ মিশন mission"),
]


def is_metadata_preamble(text):
    continuation = False
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.match(r'^(?:#{1,6}[ \t]+)?([A-Za-z_][\w-]*):', line)
        if match:
            if match[1] not in PREAMBLE_FIELDS:
                return False
            continuation = match[1] in {'tags', 'keywords'}
        elif not (continuation and (line.strip() == '$$' or line.lstrip().startswith(('* ', '- ', '"', '[')))):
            return False
    return True


def clean_document(raw: str):
    metadata, body = parse_markdown(raw)
    changes = []
    # Some supplied MDs use an unfenced metadata preamble. Extract only when
    # it starts with a known field and ends at the first actual Markdown heading.
    if re.match(r"(?:#{1,6}\s+)?(?:title|document_id|source_pdf):", body):
        heading = re.search(r"(?m)^#{1,6}\s+(?!title:|document_id:|source_pdf:)", body)
        if heading and is_metadata_preamble(body[:heading.start()]):
            preamble = body[:heading.start()]
            for key, value in re.findall(r"(?m)^(?:#{1,6}[ \t]+)?([A-Za-z_][\w-]*):[ \t]*([^\n]*)", preamble):
                metadata.setdefault(key, value.strip().strip("\"'"))
            changes.append({"reason": "unfenced_metadata", "text": preamble})
            body = body[heading.start():]
    boilerplate = r"(?m)^\*Optimized for Knowledge Base Retrieval and Searchable Context \(RAG\)\.\*[^\n]*\n?"
    for match in re.finditer(boilerplate, body):
        changes.append({"reason": "authoring_boilerplate", "text": match[0]})
    body = re.sub(boilerplate, "", body)
    return metadata, body, changes


def has_evidence(text):
    text = re.sub(r"(?m)^#{1,6}\s+.*$|^\s*---+\s*$", "", text)
    return bool(text.strip())


def evidence_units(body, title, limit=2200):
    """Keep ordinary short sections, FAQ pairs and list/table rows intact."""
    for start, end, heading, faq in section_spans(body, title, limit=10**9):
        text = body[start:end]
        if faq or len(text) <= limit:
            yield start, end, heading, faq
            continue
        for a, b in packed_spans(text, limit):
            yield start + a, start + b, heading, faq


def review_catalog(manifest, directory):
    lines = [f"# {manifest['domain'].upper()} cleanup register", "",
             "All supplied documents are retained. Review flags are unresolved provenance/quality checks, not exclusions.",
             "Source hashes and removed authoring text are preserved in manifest.json. No current legal validity is certified.", "",
             "| Document | Candidate chunks | Unresolved checks |", "|---|---:|---|"]
    for doc in manifest['documents']:
        relative = str(Path(doc['cleaned_path']).relative_to(directory.relative_to(ROOT)))
        name = Path(relative).name.replace('|', '\\|')
        flags = ', '.join(doc['review_flags']) or 'No automatic flag; still unverified'
        lines.append(f"| [{name}](<{relative}>) | {len(doc['chunk_ids'])} | {flags} |")
    (directory / 'REVIEW.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def prepare(domain, output, search_labels=False):
    base = ROOT / "domains" / domain
    config = json.loads((base / "config.json").read_text())
    register = json.loads((base / "data/register.json").read_text())
    previous = read_chunks(ROOT / config["data"]["master_chunk_path"])
    repairs_path = ROOT / 'docs/data_cleanup/reviewed_repairs.json'
    repairs = json.loads(repairs_path.read_text()) if repairs_path.exists() else {}
    by_document = {}
    for chunk in previous:
        by_document.setdefault(chunk["metadata"]["doc_id"], []).append(chunk)
    directory = output / domain
    if directory.exists():
        raise FileExistsError(f"Refusing to overwrite cleanup revision: {directory}")
    directory.mkdir(parents=True)
    write_json(directory / "baseline_config.json", config)
    prepared, documents = [], []
    for doc in register["documents"]:
        raw = (ROOT / doc["snapshot_path"]).read_bytes()
        if digest(raw) != doc["sha256"]:
            raise ValueError(f"Source snapshot changed: {doc['document_id']}")
        declared, body, changes = clean_document(raw.decode("utf-8"))
        repair = repairs.get(doc['document_id'])
        if repair:
            if digest(raw) != repair['source_sha256']:
                raise ValueError('Reviewed repair no longer matches the source snapshot')
            originals = [o for o in doc.get('original_candidates', [])
                         if o['sha256'] == repair['original_pdf_sha256']]
            if not originals or digest(Path(originals[0]['path']).read_bytes()) != repair['original_pdf_sha256']:
                raise ValueError('Reviewed original PDF missing or changed')
            changes.append({**repair, 'review_reason': repair['reason'],
                            'reason': 'original_pdf_reviewed_repair', 'text': body})
            body = (ROOT / repair['replacement_path']).read_text().strip()
        clean_path = directory / "markdown" / doc["relative_path"]
        clean_path.parent.mkdir(parents=True, exist_ok=True)
        clean_path.write_text(body, encoding="utf-8")
        original_chunks = by_document.get(doc["document_id"], [])
        record = {"document_id": doc["document_id"], "source": doc["snapshot_path"],
                  "source_sha256": doc["sha256"], "cleaned_path": str(clean_path.relative_to(ROOT)),
                  "cleaned_sha256": digest(body.encode()), "changes": changes,
                  "review_flags": list(doc.get("audit_flags", [])), "chunk_ids": [],
                  "retained_non_evidence_sections": [], "declared_metadata": declared,
                  "findings": document_findings(body), "context_spans": {}}
        if repair:
            record['review_flags'].append('assistant_pdf_reviewed_not_independently_verified')
        if not original_chunks:
            raise ValueError(f"No metadata template for registered document: {doc['document_id']}")
        template = original_chunks[0]["metadata"]
        title = declared.get("title", template["title"])
        # Unstructured OCR laws need PDF comparison; avoid pretending that
        # punctuation repairs can reconstruct legal clauses accurately.
        if len(body) > 50000 and len(re.findall(r"(?m)^#{1,6} ", body)) < 5:
            record["review_flags"].append("unstructured_ocr_preserved_requires_pdf_review")
            for old in original_chunks:
                prepared.append(old)
                record["chunk_ids"].append(old["id"])
            documents.append(record)
            continue
        units = list(evidence_units(body, title))
        assert "".join(body[a:b] for a, b, _, _ in units) == body
        for n, (start, end, section, faq) in enumerate(units, 1):
            evidence = body[start:end]
            if not has_evidence(evidence):
                record["retained_non_evidence_sections"].append({"start": start, "end": end, "text": evidence})
                continue
            scope = f"{title}\n{section}"
            aliases = [alias for pattern, alias in VOCABULARY if re.search(pattern, scope, re.I)] if search_labels else []
            inherited, pending = scope_spans(body, start)
            record['findings'].extend(pending)
            context = '\n\n'.join(body[s['start']:s['end']].strip() for s in inherited)
            content = f"{title}\n{section}\n\n" + (context + '\n\n' if context else '') + evidence
            metadata = {**template, "title": title, "section_title": section,
                        "body_start": start, "body_end": end, "faq_unit": faq,
                        "chunking_version": VERSION, "cleaned_path": str(clean_path.relative_to(ROOT)),
                        "context_spans": json.dumps(inherited),
                        "cleaned_sha256": record["cleaned_sha256"], "date_verified": False,
                        "document_date": declared.get("date", declared.get("effective_date", template.get("document_date", "unknown")))}
            cid = f"{doc['document_id']}_v4_{n:04d}"
            retrieval_text = f"{domain}\n{content}"
            if search_labels:
                retrieval_text = f"{domain}\n{scope}\nSearch labels: {'; '.join(aliases)}\n\n{evidence}"
            prepared.append({"id": cid, "content": content,
                             "retrieval_text": retrieval_text,
                             "metadata": metadata})
            record["chunk_ids"].append(cid)
            record['context_spans'][cid] = inherited
        documents.append(record)
    write_chunks(directory / "chunks.jsonl", prepared)
    manifest = {"version": VERSION, "domain": domain, "search_labels": search_labels, "source_documents": len(documents),
                "baseline_chunk_count": len(previous), "candidate_chunk_count": len(prepared),
                "documents": documents,
                "review_flag_counts": dict(Counter(flag for d in documents for flag in d["review_flags"]))}
    write_json(directory / "manifest.json", manifest)
    review_catalog(manifest, directory)
    print(domain, len(documents), "documents", len(previous), "->", len(prepared), "chunks", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", choices=["passport", "brta"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument('--search-labels', action='store_true', help='Experimental heading-derived aliases; validate before use')
    args = parser.parse_args()
    prepare(args.domain, args.output.resolve(), args.search_labels)

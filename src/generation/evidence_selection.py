"""Auditable service/action screening, not a correctness or entailment verifier.

Rules describe reusable service vocabulary, never question strings or chunk IDs.
Unclassified queries retain retrieval ordering. Text is never rewritten.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


def norm(text):
    return unicodedata.normalize('NFC', str(text)).lower()


ACTION_TERMS = {
    'replacement': ('হারিয়ে', 'হারিয়ে', 'হারাই', 'হারালে', 'হারানো', 'নষ্ট', 'প্রতিলিপি', 'ডুপ্লিকেট', 'lost', 'duplicate', 'replacement'),
    'renewal': ('নবায়ন', 'নবায়ন', 'মেয়াদ শেষ', 'মেয়াদ শেষ', 'renew', 'expired'),
    'correction': ('সংশোধন', 'ভুল', 'বানান', 'পরিবর্তন', 'correction', 'correcting', 'mistake', 'change'),
    'collection': ('সংগ্রহ', 'ডেলিভারি স্লিপ', 'collect', 'delivery slip'),
    'cancellation': ('বাতিল', 'স্থগিত', 'পুনর্বিবেচনা', 'আপিল', 'cancel', 'revok', 'revocation', 'appeal', 'disqualif'),
    'status': ('স্ট্যাটাস', 'অগ্রগতি', 'status', 'tracking'),
    'verification': ('যাচাই', 'verification', 'verify'),
}
SERVICE_TERMS = {
    'passport': ('পাসপোর্ট', 'passport'),
    'coi': ('বিদেশীদের পরিচিতি সনদ', 'certificate of identity'),
    'visa': ('ভিসা', 'visa'),
    'licence': ('ড্রাইভিং লাইসেন্স', 'ড্রাইভিং লাইসেনস', 'driving licen', 'ড্রাইভিং'),
    'fitness': ('ফিটনেস', 'fitness'),
    'vehicle_registration': ('মোটরযান রেজিস্ট্রেশন', 'গাড়ির রেজিস্ট্রেশন', 'গাড়ির রেজিস্ট্রেশন', 'vehicle registration'),
    'route_permit': ('রুট পারমিট', 'route permit'),
    'birth': ('জন্ম', 'birth'),
    'death': ('মৃত্যু', 'death'),
}
FEE_TERMS = ('ফি', 'টাকা', 'খরচ', 'fee', 'cost', 'payment')
DOCUMENT_TERMS = ('কাগজপত্র', 'কাগজ', 'প্রমাণ', 'documents', 'checklist', 'enrolment', 'enrollment')
APPLICATION_TERMS = ('আবেদন', 'করতে', 'করব', 'নতুন', 'প্রাপ্তির', 'apply', 'application', 'enrolment', 'enrollment')


def has(text, terms):
    text = norm(text)
    return any(norm(t) in text for t in terms)


def labels(text, vocabulary):
    return {key for key, terms in vocabulary.items() if has(text, terms)}


def actions(text):
    result = labels(text, ACTION_TERMS)
    # Specific procedures take precedence over the generic word 'application'.
    if not result and has(text, APPLICATION_TERMS):
        result.add('application')
    return result


def scope_text(context):
    metadata = context.get('metadata', {})
    section = str(metadata.get('section_title', ''))
    # Prefer the local section over a document-wide title listing many services.
    if section:
        return ' > '.join(section.split('>')[-2:])
    return str(metadata.get('title') or context.get('content', ''))


def service_labels(text):
    found = labels(text, SERVICE_TERMS)
    if 'coi' in found:
        found.discard('passport')
    return found


def product_labels(text):
    return labels(text, {'epassport': ('ই-পাসপোর্ট', 'ই পাসপোর্ট', 'epassport', 'e-passport'),
                         'mrp': ('এমআরপি', 'mrp', 'machine readable passport')})


def locations(text):
    return labels(text, {'domestic': ('দেশের ভিতরে', 'দেশের ভেতরে', 'বাংলাদেশের ভিতরে', 'inside bangladesh', 'domestic'),
                         'overseas': ('বিদেশে', 'দূতাবাস', 'মিশন', 'mission', 'overseas', 'abroad')})


def describe(context):
    scope = scope_text(context)
    specific = actions(scope)
    body = str(context.get('content', ''))
    if context.get('metadata', {}).get('section_title') and '\n\n' in body:
        body = body.split('\n\n', 1)[1]
    # Broad legal headings often contain no useful action information.
    if not specific and has(scope, DOCUMENT_TERMS):
        specific = {'application'}
    if not specific:
        specific = actions(body)
    services = service_labels(scope)
    return {'actions': specific, 'services': services, 'products': product_labels(scope), 'locations': locations(scope),
            'fee': has(scope, FEE_TERMS) or context.get('metadata', {}).get('document_type') in {'fee_row', 'fees_table'},
            'documents': has(scope, DOCUMENT_TERMS),
            'historical': 'dated_document_review_applicability' in str(context.get('metadata', {}).get('audit_flags', '')),
            'scope': scope}


def family(context):
    m = context.get('metadata', {})
    doc = m.get('doc_id') or m.get('document_id') or m.get('source_relative_path')
    section = str(m.get('section_title', ''))
    if not doc or '>' not in section:
        return None
    return (doc, section.rsplit('>', 1)[0].strip())


@dataclass
class Selection:
    contexts: list
    trace: dict


def select_evidence(query, candidates, corpus=(), *, max_contexts=6, max_chars=14000):
    query_actions = actions(query)
    query_services = service_labels(query)
    query_products = product_labels(query)
    query_locations = locations(query)
    fee = has(query, FEE_TERMS)
    documents = has(query, DOCUMENT_TERMS)
    if not query_actions and documents:
        query_actions = {'application'}
    trace = {'version': 'applicability_v1', 'query_actions': sorted(query_actions),
             'query_services': sorted(query_services), 'decisions': [], 'expanded_ids': [],
             'warning': 'Heuristic applicability screening, not verified relevance or factual correctness.'}
    seen = set()
    eligible = []
    for i, context in enumerate(candidates):
        if context['id'] in seen:
            continue
        seen.add(context['id'])
        d = describe(context)
        reason = None
        if query_services and d['services'] and not query_services & d['services']:
            reason = 'different_service'
        elif query_products and d['products'] and not query_products & d['products']:
            reason = 'different_product'
        elif query_locations and d['locations'] and not query_locations & d['locations']:
            reason = 'different_location'
        elif query_actions and d['actions'] and not query_actions & d['actions']:
            reason = 'different_action'
        if reason:
            trace['decisions'].append({'id': context['id'], 'decision': 'excluded', 'reason': reason})
            continue
        strength = int(bool(query_actions & d['actions'])) * 3
        strength += int(bool(query_services & d['services']))
        strength += 2 * int((fee and d['fee']) or (documents and d['documents']))
        eligible.append((strength, i, context, d))
    # Only suppress explicitly flagged historical documents when alternatives
    # exist; explicit requests for history/product-specific MRP remain eligible.
    historical_request = has(query, ('পুরোনো', 'আগের', 'ইতিহাস', 'histor', 'mrp', 'এমআরপি')) or bool(re.search(r'[12১২][0-9০-৯]{3}', query))
    nonhistorical = any(not d['historical'] and score >= 2 for score, _, _, d in eligible)
    if nonhistorical and not historical_request:
        retained = []
        for row in eligible:
            if row[3]['historical']:
                trace['decisions'].append({'id': row[2]['id'], 'decision': 'excluded', 'reason': 'historical_alternative_requires_explicit_scope'})
            else:
                retained.append(row)
        eligible = retained
    eligible.sort(key=lambda row: (-row[0], row[1]))
    # Once a direct action match exists, unclassified fragments should not
    # crowd it out. Unknown-only queries retain their candidates.
    matched = any(query_actions & d['actions'] for _, _, _, d in eligible)
    ordered = []
    for _, _, context, d in eligible:
        if matched and query_actions and not query_actions & d['actions'] and not (fee and d['fee']):
            trace['decisions'].append({'id': context['id'], 'decision': 'excluded', 'reason': 'unclassified_action_with_direct_alternative'})
        else:
            ordered.append(context)
    # Complete adjacent category/checklist sections only inside an already
    # retrieved document and parent section; never search arbitrary corpus IDs.
    if fee or documents:
        families = {family(c) for c in ordered if family(c)}
        sections = {str(c.get('metadata', {}).get('section_title', '')) for c in ordered}
        for c in corpus:
            if c['id'] in seen or family(c) not in families:
                continue
            d = describe(c)
            if documents and not fee and str(c.get('metadata', {}).get('section_title', '')) not in sections:
                continue
            if query_services and d['services'] and not query_services & d['services']:
                continue
            if query_actions and d['actions'] and not query_actions & d['actions']:
                continue
            if query_products and d['products'] and not query_products & d['products']:
                continue
            if query_locations and d['locations'] and not query_locations & d['locations']:
                continue
            if (fee and not d['fee']) or (documents and not fee and not d['documents']):
                continue
            ordered.append({'id': c['id'], 'content': c['content'], 'metadata': dict(c.get('metadata', {}))})
            seen.add(c['id'])
            trace['expanded_ids'].append(c['id'])
    chosen, length = [], 0
    for c in ordered:
        size = len(str(c.get('content', '')))
        if not size:
            continue
        if len(chosen) >= max_contexts or length + size > max_chars:
            trace['decisions'].append({'id': c['id'], 'decision': 'excluded', 'reason': 'whole_chunk_budget'})
            continue
        chosen.append(c)
        length += size
        trace['decisions'].append({'id': c['id'], 'decision': 'selected', 'reason': 'compatible_scope'})
    trace['selected_ids'] = [c['id'] for c in chosen]
    trace['selected_chars'] = length
    return Selection(chosen, trace)

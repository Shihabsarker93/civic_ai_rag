"""Compare a frozen cleanup candidate against baseline on transparent diagnostics."""
import argparse
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_OFFLINE', '1')
from src.pipeline import CivicRAGPipeline

# Source/section checks diagnose known failures, not held-out benchmark accuracy.
CASES = [
    ('passport', 'নতুন পাসপোর্ট করতে কী কী কাগজপত্র লাগবে?', ['passport_73ac41f2327257f9', 'passport_729010959c882773'], ''),
    ('passport', 'পাসপোর্ট বানাতে কত টাকা লাগে?', ['passport_12e10027cfdfeeee'], 'Inside Bangladesh'),
    ('passport', 'পাসপোর্ট পেতে কত দিন সময় লাগে?', ['passport_12e10027cfdfeeee'], 'Delivery Timelines'),
    ('passport', 'পাসপোর্টের আবেদন করার পর স্ট্যাটাস কীভাবে দেখব?', ['passport_23d845d3ab38ea43'], 'Application Status'),
    ('passport', 'ডেলিভারি স্লিপ হারিয়ে গেলে পাসপোর্ট কীভাবে সংগ্রহ করব?', ['passport_23d845d3ab38ea43'], 'Lost Delivery Slip'),
    ('brta', 'BRTA-এর ড্রাইভিং পরীক্ষায় কী কী থাকে?', ['brta_cbe22ab64acf3d03', 'brta_846a4041fe96a64e'], 'লিখিত'),
    ('brta', 'ড্রাইভিং লাইসেন্স হারিয়ে গেলে কী করতে হবে?', ['brta_cbe22ab64acf3d03'], 'ডুপ্লিকেট'),
    ('brta', 'ড্রাইভিং লাইসেন্সের মেয়াদ শেষ হলে কীভাবে নবায়ন করব?', ['brta_cbe22ab64acf3d03'], 'নবায়ন'),
    ('brta', 'লার্নার ড্রাইভিং লাইসেন্স কীভাবে করব?', ['brta_cbe22ab64acf3d03'], 'প্রাপ্তির প্রক্রিয়া'),
    ('brta', 'গাড়ির ফিটনেস সনদ নবায়ন করব কীভাবে?', ['brta_d516e1b85b1f7144'], ''),
]


def matches(c, prefixes, hint):
    return any(c['id'].startswith(prefix) for prefix in prefixes) and hint.casefold() in c['content'].casefold()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domain', choices=['passport', 'brta'], required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--device', default='mps')
    args = parser.parse_args()
    report = {'scope': 'Known-failure and preservation diagnostics, no LLM calls; not gold Recall or correctness.',
              'device': args.device, 'rows': [], 'configs': {}}
    shared = None
    for variant, path in [('baseline', args.baseline), ('candidate', args.candidate)]:
        pipeline = CivicRAGPipeline(ROOT, path, shared_pipeline=shared)
        if shared is None:
            shared = pipeline
            pipeline.retriever.embedding_model.to(args.device)
            if pipeline.reranker.cross_encoder is None:
                raise RuntimeError('Cross-encoder unavailable; refuse an unlabelled fallback comparison')
            pipeline.reranker.cross_encoder.model.to(args.device)
        report['configs'][variant] = pipeline.config
        for domain, query, prefixes, hint in CASES:
            if domain != args.domain:
                continue
            if not any(matches(c, prefixes, hint) for c in pipeline.chunks):
                raise ValueError(f'Invalid diagnostic evidence hint: {query} / {hint}')
            started = time.monotonic()
            result = pipeline.ask(query, generate=False)
            ranks = [i + 1 for i, c in enumerate(result['sources']) if matches(c, prefixes, hint)]
            evidence = pipeline._select_generation_contexts(query, result['sources'], pipeline.generation_config['top_k_for_generation'])
            report['rows'].append({'variant': variant, 'query': query, 'support_rank': min(ranks) if ranks else None,
                                   'generation_evidence_has_support': any(matches(c, prefixes, hint) for c in evidence),
                                   'source_prefixes': prefixes, 'content_hint': hint, 'sources': result['sources'],
                                   'seconds': round(time.monotonic() - started, 2)})
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            print(domain, variant, ranks, query, flush=True)
    report['summary'] = {}
    for variant in ['baseline', 'candidate']:
        rows = [r for r in report['rows'] if r['variant'] == variant]
        report['summary'][variant] = {'cases': len(rows), 'support_at_1': sum(r['support_rank'] == 1 for r in rows),
                                      'support_in_top_6': sum(r['support_rank'] is not None for r in rows),
                                      'support_in_generation_context': sum(r['generation_evidence_has_support'] for r in rows)}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(report['summary'], flush=True)


if __name__ == '__main__':
    main()

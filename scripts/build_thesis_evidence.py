"""Read-only project audit; write reproducible thesis tables, not model answers."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/thesis_final_2026_09_24'
GEN = OUT / 'generated'
PREVIOUS = Path('/Users/shihab/01 Thesis/p3 final/Writing/01 update/submited so far/core/abstract.tex')
RUNS = {
    'Simple RAG / Qwen3': 'simple_matched_qwen3_30q_2026_09_24',
    'CivicRAG / Qwen3': 'chunk_order_fixed_qwen3_30q_2026_09_23',
    'CivicRAG / Llama3': 'chunk_order_fixed_llama3_30q_2026_09_23',
    'CivicRAG / Qwen2.5': 'chunk_order_fixed_qwen25_30q_2026_09_23',
}


def esc(value):
    mapping = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}'}
    return ''.join(mapping.get(c, c) for c in str(value))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(name, caption, headers, rows, columns):
    text = ['\\begin{table}[htbp]\\centering\\small', '\\caption{' + caption + '}',
            '\\begin{tabularx}{\\linewidth}{' + columns + '}\\toprule',
            ' & '.join(esc(c) for c in headers) + r'\\\midrule']
    text += [' & '.join(esc(c) for c in row) + r'\\' for row in rows]
    text += [r'\bottomrule\end{tabularx}\end{table}']
    (GEN / name).write_text('\n'.join(text) + '\n')


def main():
    GEN.mkdir(parents=True, exist_ok=True)
    assert PREVIOUS.read_bytes() == (OUT / 'core/abstract.tex').read_bytes(), 'Abstract changed'
    manifest = {'abstract_sha256': digest(PREVIOUS), 'abstract_unchanged': True,
                'audit_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'files': {}, 'corpus': {}, 'runs': {}}
    primary_plan = json.loads((ROOT / 'docs/evaluation/chunk_order_fixed_qwen3_30q_2026_09_23/plan.json').read_text())
    baseline_plan = json.loads((ROOT / 'docs/evaluation/simple_matched_qwen3_30q_2026_09_24/plan.json').read_text())
    assert primary_plan['file_hashes'] == baseline_plan['file_hashes']
    for relative, expected in primary_plan['file_hashes'].items():
        assert digest(ROOT / relative) == expected, 'Current file differs from evaluated snapshot: ' + relative
    manifest['frozen_hashes_verified'] = primary_plan['file_hashes']
    catalog = []
    corpus_rows, flags_rows = [], []
    for domain, display in [('birth_death_registration', 'Birth/death'), ('passport', 'Passport'), ('brta', 'BRTA')]:
        config_path = ROOT / 'domains' / domain / 'config.json'
        config = json.loads(config_path.read_text())
        path = ROOT / config['data']['chunk_output_path']
        chunks = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        assert len({r['id'] for r in chunks}) == len(chunks)
        manifest['files'][str(path.relative_to(ROOT))] = digest(path)
        metas = [r['metadata'] for r in chunks]
        grouped = {}
        for chunk in chunks:
            m = chunk['metadata']
            source = m.get('source_relative_path') or m.get('source_path') or m.get('source_file') or m.get('doc_id')
            entry = grouped.setdefault(source, {'domain': domain, 'source': source, 'title': m.get('title', ''), 'chunk_ids': [], 'source_urls': set(), 'flags': set()})
            entry['chunk_ids'].append(chunk['id'])
            if m.get('source_url'):
                entry['source_urls'].add(m['source_url'])
            entry['flags'].update(f.strip() for f in m.get('audit_flags', '').split(',') if f.strip())
        catalog.extend({**v, 'source_urls': sorted(v['source_urls']), 'flags': sorted(v['flags'])} for v in grouped.values())
        source_ids = {m.get('source_relative_path') or m.get('source_path') or m.get('source_file') or m.get('doc_id') for m in metas}
        source_ids.discard(None)
        register_path = ROOT / 'domains' / domain / 'data/register.json'
        originals = 'Not comparable'
        if register_path.exists():
            register = json.loads(register_path.read_text())
            originals = len(register['originals'])
            assert len(source_ids) == len(register['documents'])
            doc_flags = {}
            for m in metas:
                doc_flags.setdefault(m['document_id'], set()).update(f.strip() for f in m.get('audit_flags', '').split(',') if f.strip())
            for flag in ['no_web_address', 'original_match_unresolved', 'dated_document_review_applicability', 'long_document_check_ocr']:
                flags_rows.append([display, flag.replace('_', ' '), sum(flag in fs for fs in doc_flags.values())])
        manifest['corpus'][domain] = {'chunks': len(chunks), 'source_units': len(source_ids), 'registered_originals': originals,
            'document_types': dict(Counter(m.get('document_type', '') for m in metas))}
        corpus_rows.append([display, len(source_ids), originals, len(chunks)])
    table('corpus_table.tex', 'Active corpus inventory computed from configured files. Source units are prepared documents, not independent facts.',
          ['Domain', 'Source units', 'Registered originals', 'Chunks'], corpus_rows, 'Xrrr')
    table('audit_table.tex', 'Selected unresolved active-corpus flags, counted once per derivative document. These counts may overlap.',
          ['Domain', 'Flag', 'Documents'], flags_rows, 'p{20mm}Xr')

    data = {}
    for label, folder in RUNS.items():
        path = ROOT / 'docs/evaluation' / folder / 'answers.json'
        rows = json.loads(path.read_text())['rows']
        assert len(rows) == 30
        data[label] = rows
        manifest['files'][str(path.relative_to(ROOT))] = digest(path)
        manifest['runs'][label] = {'n': len(rows), 'routes': dict(Counter(r['result']['answer_route'] for r in rows))}
    simple, civic = data['Simple RAG / Qwen3'], data['CivicRAG / Qwen3']
    assert [r['audit_item'] for r in simple] == [r['audit_item'] for r in civic]
    for label in ['CivicRAG / Llama3', 'CivicRAG / Qwen2.5']:
        assert [r['audit_item'] for r in data[label]] == [r['audit_item'] for r in civic]
        equal = all([(x['id'], x['content']) for x in a['result']['answer_contexts']] == [(x['id'], x['content']) for x in b['result']['answer_contexts']] for a, b in zip(data[label], civic))
        manifest['runs'][label]['contexts_equal_to_qwen3'] = equal
        assert equal, label
    markers = Counter(t for row in civic for c in row['result']['sources'] for t in c.get('retrievers', []))
    manifest['candidate_retriever_markers'] = dict(markers)
    comparison_rows = []
    for label, rows in [('Simple RAG', simple), ('CivicRAG', civic)]:
        ts = sorted(r['elapsed_seconds'] for r in rows)
        comparison_rows.append([label, len(rows), f'{statistics.mean(ts):.2f}', f'{statistics.median(ts):.2f}', f'{ts[math.ceil(.95*len(ts))-1]:.2f}', f'{statistics.mean(len(r["result"]["answer_contexts"]) for r in rows):.2f}'])
    table('comparison_table.tex', 'Saved Qwen3 comparison: operational results, not correctness scores. Times are in seconds.',
          ['System', 'n', 'Mean', 'Median', 'p95', 'Contexts'], comparison_rows, 'Xrrrrr')
    domain_rows = []
    for domain, display in [('passport','Passport'),('birth_death_registration','Birth'),('brta','BRTA')]:
        for label, rows in [('Simple',simple),('Civic',civic)]:
            rs = [r for r in rows if r['audit_item']['domain'] == domain]
            domain_rows.append([display, label, len(rs), f'{statistics.mean(r["elapsed_seconds"] for r in rs):.2f}', f'{statistics.mean(sum(len(c["content"]) for c in r["result"]["answer_contexts"]) for r in rs):.1f}'])
    table('domain_table.tex', 'Per-domain timing and actual supplied context size for the matched comparison.',
          ['Domain','System','n','Mean seconds','Mean characters'], domain_rows, 'XXrrr')
    model_rows = []
    for label, rows in data.items():
        if label.startswith('Simple'):
            continue
        model_rows.append([label.split(' / ')[1],len(rows),f'{statistics.mean(r["elapsed_seconds"] for r in rows):.2f}',sum('language_rejection' in r['result']['answer_route'] for r in rows)])
    table('model_table.tex', 'Secondary current-configuration model runs. Language rejection counts are operational outcomes, not error rates.',
          ['Model','Requests','Mean seconds','Language rejections'], model_rows, 'Xrrr')
    questions = [r'\begin{longtable}{p{15mm}p{121mm}}', r'\toprule ID & Question\\\midrule\endfirsthead',r'\toprule ID & Question\\\midrule\endhead']
    for n, row in enumerate(civic,1):
        questions.append(str(n) + ' & \\bn{' + esc(row['audit_item']['question']) + r'}\\[3mm]')
    questions.append(r'\bottomrule\end{longtable}')
    (GEN/'questions.tex').write_text('\n'.join(questions))
    ragas = ROOT/'docs/evaluation/ragas_comparison_2026_09_24'
    progress = json.loads((ragas/'progress.json').read_text()) if (ragas/'progress.json').exists() else {}
    manifest['ragas_progress_at_snapshot'] = progress
    if (ragas/'completion.json').exists():
        scores = json.loads((ragas/'ragas_scores.json').read_text())
        assert len(scores) == 180
        (GEN/'ragas_scores_snapshot.json').write_text(json.dumps(scores, ensure_ascii=False, indent=2))
        summary_rows = []
        for system in ['simple','civic']:
            for metric in ['faithfulness','answer_relevancy','context_relevance_binary']:
                rs=[r for r in scores if r['system']==system and r['metric']==metric]
                good=[r['score'] for r in rs if r['score'] is not None]
                summary_rows.append([system,metric.replace('_',' '),len(good),len(rs)-len(good),f'{statistics.mean(good):.3f}' if good else 'Missing'])
        table('ragas_status.tex','Completed local self-judge metrics. Means exclude failed calls; not independent correctness scores.', ['System','Metric','Valid','Failed','Mean'],summary_rows,'lXrrr')
    else:
        (GEN/'ragas_status.tex').write_text('\\textbf{Evaluation status at manuscript snapshot:} '+str(progress.get('metric_attempts',0))+' of 180 metric attempts had been saved. The batch was incomplete; full-set RAGAS values are therefore not reported here. This paragraph must be refreshed from the completed artifacts before final submission.\n')
    (OUT/'evidence_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    (OUT/'dataset_catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2))
    print(json.dumps({'abstract_unchanged':True,'corpus':manifest['corpus'],'runs':manifest['runs'],'ragas_attempts':progress.get('metric_attempts')},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()

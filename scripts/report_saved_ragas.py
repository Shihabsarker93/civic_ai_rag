"""Format the saved comparison; no inference or chatbot calls."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/evaluation/ragas_comparison_2026_09_24'


def main():
    descriptive = json.loads((OUT / 'descriptive_metrics.json').read_text())
    scores = json.loads((OUT / 'ragas_scores.json').read_text())
    keys = {(r['system'], r['question_id'], r['metric']) for r in scores}
    assert len(keys) == len(scores), 'Duplicate metric records'
    complete = (OUT / 'completion.json').exists() and len(keys) == 180
    lines = ['# Simple RAG versus CivicRAG: saved Qwen3 answers', '',
             'Same 30 questions and existing saved answers. No answer regeneration. No external-paper benchmark comparison.', '',
             f'Judge metric attempts: {len(scores)}/180. Status: {"complete" if complete else "incomplete"}.', '',
             '## Descriptive results for all 30 answers per system', '',
             '| Measure | Simple RAG | CivicRAG |', '|---|---:|---:|']
    for label, key in [('Completed requests (not correct answers)', 'completed_requests'),
                       ('Mean saved generation latency (seconds)', 'mean_latency_seconds'),
                       ('Median saved generation latency (seconds)', 'median_latency_seconds'),
                       ('95th percentile saved latency (seconds)', 'p95_latency_seconds_nearest_rank'),
                       ('Mean supplied passages', 'mean_context_count'),
                       ('Mean supplied context characters', 'mean_context_characters'),
                       ('Mean Bangla-letter fraction (not fluency)', 'mean_bangla_fraction_of_letters')]:
        lines.append(f'| {label} | {descriptive["simple"][key]:.3f} | {descriptive["civic"][key]:.3f} |')
    lines += ['', 'Saved latency comes from separate runs, not a controlled hardware speed experiment.', '', '## RAGAS comparison', '']
    if not complete:
        lines += ['Final full-set judge averages are withheld until the batch finishes. Partial scores are saved for recovery, not presented as final results.']
    else:
        summary = json.loads((OUT / 'ragas_summary.json').read_text())
        lines += ['| Metric | Simple mean (valid/30) | Civic mean (valid/30) | Paired Civic minus Simple |', '|---|---:|---:|---:|']
        for metric in ['faithfulness', 'answer_relevancy', 'context_relevance_binary']:
            cells = []
            for system in ['simple', 'civic']:
                item = summary['systems'][system][metric]
                mean = f'{item["mean"]:.4f}' if item['mean'] is not None else 'missing'
                cells.append(f'{mean} ({item["valid"]}/30; failed {item["failed"]})')
            paired = summary['paired_civic_minus_simple'].get(metric)
            diff = 'missing' if not paired else f'{paired["mean_difference"]:.4f} (n={paired["paired_n"]})'
            lines.append(f'| {metric} | {cells[0]} | {cells[1]} | {diff} |')
        lines += ['', 'Paired descriptive bootstrap intervals are retained in ragas_summary.json. Missing judgments are excluded, not treated as zero.']
    lines += ['', '## Interpretation limits', '',
              '- Qwen3:8b is both generator and evaluator: these are exploratory self-judge scores, not independent factual accuracy.',
              '- Faithfulness measures support by supplied text, not whether a government rule is current or applicable.',
              '- Response relevance is not gold-answer correctness.',
              '- context_relevance_binary is a custom RAGAS AspectCritic, not standard context precision or recall.',
              '- The 30 questions were reused during development; these results are not held-out generalization estimates.',
              '- No correctness percentage, MRR, nDCG or reference-answer similarity is invented without reviewed labels.',
              '- Full question-level scores and errors are in ragas_scores.json; original answer paths and hashes are in manifest.json.', '']
    target = OUT / 'comparison_report.md'
    temporary = target.with_suffix('.md.tmp')
    temporary.write_text('\n'.join(lines))
    temporary.replace(target)
    print(f'Report saved: {target}; complete={complete}', flush=True)


if __name__ == '__main__':
    main()

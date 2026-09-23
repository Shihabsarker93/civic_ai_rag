# Related-chunk ordering fix

Rollback: `codex/pre-chunk-order-fix-20260923` (saved on origin before edits).
The tracked working tree was clean. Untracked data, drafts and logs were left
untouched and are not included in this Git rollback tag.

## Change

Previously, expanded fee/checklist passages were appended after all eligible
candidates. The six-context limit could discard them before generation.
Compatible passages from the same document and parent section are now grouped
at their earliest ranked anchor before budgeting. Checklist grouping also
requires the same section title. Existing screening and whole-chunk limits
remain in force. No question strings or corpus IDs were added to production
selection rules.

Prompts, models, data, retrieval, reranking and answer routes were not changed.
This is not a new relevance verifier. Large families can still exceed the
unchanged context or character limits.

## Verification

- Full test suite: 65 passed, including fee-family budget regressions across
  passport, driving licence and birth registration, duplicate prevention and
  character-budget enforcement.
- Replayed all 30 saved overnight candidate lists, without retrieval or LLM calls.
- The old selector reproduced all 30 saved selections with the current corpus.
- Only `passport_02_fee` changed; the other 29 selections, including order,
  remained identical.
- All four passport fee categories (`0007` through `0010` in the fee document)
  now survive selection. Previously only `0010` survived.
- Two other passages still occupy the remaining slots, including the MRP
  charter passage. This narrow fix does not eliminate all possible distraction.
- No new answers were generated; answer quality remains untested.

Reproduce with `.venv/bin/python scripts/check_selection_order.py`.
See `selection_replay.json` for before/after IDs, decisions and corpus hashes.
This replay is not an end-to-end accuracy evaluation.

The existing web-server process was not restarted during this patch, so it
must be restarted before manually testing the updated selector.

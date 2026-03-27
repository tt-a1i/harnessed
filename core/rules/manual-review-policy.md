# Manual Review Policy

## Per-Criterion
- `MANUAL_REVIEW_NEEDED` means the criterion cannot be verified automatically.
- It is excluded from pass/fail counts.

## Overall Grade
- If at least one criterion is `MANUAL_REVIEW_NEEDED` and all remaining criteria pass, overall grade becomes `SHIP_WITH_HUMAN_REVIEW`.

## Verification Gate
- Do not fabricate automated evidence for manual-review criteria.
- List them under `Pending Human Review` with evaluator notes.
- Never silently omit them.

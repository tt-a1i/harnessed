# Grading Rubric

## Per-Criterion Grades

- **PASS** — Criterion fully satisfied. Code exists, is correct, edge cases handled. For Tier 1.5/2: execution confirms it works. Requires `file:line` evidence.
- **PARTIAL** — Core behavior works but edge cases unhandled, or minor correctness issue. Counts as failure for grading. Fixable in one iteration.
- **FAIL** — Not satisfied: no implementation, incorrect results, or regression introduced. For Tier 1.5/2: execution demonstrates failure. Requires `file:line` evidence.
- **MANUAL_REVIEW_NEEDED** — Cannot assess by automated means (visual design, UX feel, browser-specific). Excluded from pass/fail count. Does not block SHIP but must be listed in summary.

## Severity Classification (Additional Findings)

- **Critical** — Crash, data corruption, security vulnerability, core functionality broken. Any critical = BLOCKED.
- **Major** — Feature partially broken, significant UX issue, missing error handling at system boundary.
- **Minor** — Code style, missing non-essential error message, suboptimal but functional, doc mismatch.

## Overall Grade

- **SHIP** — All criteria PASS (MANUAL_REVIEW_NEEDED excluded), zero critical findings, zero major findings affecting core. For Tier 1.5: smoke tests pass; Tier 2: test suite passes. Only grade allowing verification-gate.
- **ITERATE** — One+ criteria FAIL/PARTIAL, or major findings exist. MUST list specific changes needed.
- **BLOCKED** — Critical findings, fundamentally flawed approach, >50% criteria FAIL, or implementation contradicts contract. MUST explain why and suggest alternative.
- **Precedence:** BLOCKED > ITERATE > SHIP when multiple conditions met.

## Grading Integrity Rules

1. **Never inflate.** PASS vs PARTIAL doubt → PARTIAL. ITERATE vs BLOCKED doubt → more evidence wins.
2. **Grade code, not intent.** "Probably meant to..." is not evidence.
3. **Pre-existing issues are not findings.** Only grade this diff.
4. **File:line or it didn't happen.** Every grade needs evidence.
5. **Grade independently.** One FAIL does not contaminate other criteria.

# QA Report Format Reference

Canonical format for `.harnessed/qa-report.md` across all platforms.
The evaluator prompt, report validator, verification gate, and docs must stay aligned with this file.

## Format

```markdown
# QA Report

## Overview
- **Verification Tier:** {1 | 1.5 | 2}
- **Overall Grade:** {SHIP | SHIP_WITH_HUMAN_REVIEW | ITERATE | BLOCKED}
- **Criteria Passed:** {X}/{Y} (Y excludes criteria graded MANUAL_REVIEW_NEEDED)
- **Critical Issues:** {count}

## Per-Criterion Evaluation

### Criterion: "{criterion text}"
- **Grade:** {PASS | FAIL | PARTIAL | MANUAL_REVIEW_NEEDED}
- **Evidence:** {file:line citation or command output}
- **Finding:** {what was observed}
- **Action Required:** {what must change, if FAIL/PARTIAL}

## Additional Findings

### {finding title}
- **Severity:** {critical | major | minor}
- **Location:** {file:line}
- **Description:** {what is wrong}
- **Recommendation:** {how to fix it}

## Execution Results (Tier 1.5 and Tier 2)

### HTTP Smoke Tests (Tier 1.5)
- **Command:** {curl command}
- **Expected:** {expected status/body}
- **Actual:** {actual status/body}
- **Verdict:** {PASS | FAIL}

### Test Suite (Tier 2)
- **Command:** {command run}
- **Result:** {pass/fail and counts}
- **Failures:** {details of failures}

### Manual Verification
- {what was checked and observed}

## Failure Categories
| Category | Criterion | Finding Summary |
|----------|-----------|-----------------|
| {short category} | {criterion text} | {summary} |
```

## Rules

- Omit `## Failure Categories` entirely when the overall grade is `SHIP` or `SHIP_WITH_HUMAN_REVIEW`.
- Every grade requires evidence. Missing evidence is a failure, not a note.
- `MANUAL_REVIEW_NEEDED` does not count as pass/fail, but it elevates the overall grade from `SHIP` to `SHIP_WITH_HUMAN_REVIEW`.
- Use this exact heading order so validators can parse reports deterministically.

# Verification Summary Format Reference

Canonical format for `.harnessed/verification-summary.md`.

## Format

```markdown
# Verification Summary

## Task
{task description}

## Status: VERIFIED | VERIFIED_PENDING_HUMAN_REVIEW

## Evidence

### Criterion: "{criterion text}"
- **Evidence:** {type}: {citation}
- **Verified:** Yes

## Pending Human Review
{List criteria marked MANUAL_REVIEW_NEEDED with evaluator notes. Omit section if none.}

## QA History
- Rounds: {number of QA iterations}
- Final grade: {SHIP | SHIP_WITH_HUMAN_REVIEW}
- Issues fixed during QA: {brief list or None}

## Files Changed
{list of modified files}
```

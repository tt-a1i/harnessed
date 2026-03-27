# Failure Patterns Format Reference

Canonical format for `.harnessed/failure-patterns.md`.

## Format

```markdown
| Category | Count | Last Seen | Example |
|----------|-------|-----------|---------|
| missing input validation | 2 | 2026-03-27 | Endpoint accepted malformed payload without returning 400. |
```

## Rules

- Categories are copied verbatim from evaluator output.
- Remove expired singleton rows older than 90 days.
- When the table exceeds 20 rows, trim rows in this order:
  1. expired singletons (already handled by decay)
  2. remaining `Count = 1` rows, oldest first
  3. only then lowest-count recurring rows, oldest first

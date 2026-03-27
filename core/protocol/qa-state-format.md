# QA State Format Reference

Canonical format for `.harnessed/qa-state.md`.

## Format

```yaml
iteration: {N}
dispatched_at: {ISO 8601 timestamp}
head_commit: {git rev-parse HEAD}
contract_hash: {md5 of .harnessed/contract.md}
```

## Rules

- `iteration` starts at `1` for the first QA round.
- `head_commit` is omitted only for non-git projects.
- `contract_hash` is required for tamper detection.
- This file is written by the orchestrator, never by the evaluator.

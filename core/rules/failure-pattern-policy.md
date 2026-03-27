# Failure Pattern Policy

- Failure categories come from the evaluator, not the orchestrator.
- Only `ITERATE` and `BLOCKED` results update `.harnessed/failure-patterns.md`.
- Keep categories verbatim to avoid silently rephrasing the evaluator's judgment.
- Apply decay and cap trimming exactly as defined in `core/protocol/failure-patterns-format.md`.

# Artifact Protocol

Harnessed uses `.harnessed/` as a cross-platform file communication channel.

| File | Purpose | Producer | Consumer |
|------|---------|----------|----------|
| `contract.md` | normalized acceptance criteria | contract-writing | evaluator, gate |
| `qa-report.md` | independent evaluation report | evaluator | orchestrator, gate |
| `qa-state.md` | iteration and staleness state | orchestrator | orchestrator, gate |
| `verification-summary.md` | final evidence report | verification-gate | user |
| `failure-patterns.md` | persistent learning store | orchestrator | contract-writing |
| `policies/*.md` | repo-specific policy summaries selected by scope | user or policy generator | contract-writing, evaluator |
| `.lock` | advisory session lock | adapter | adapter |

## Policy Store

`.harnessed/policies/` stores short repo-policy summaries that can be injected selectively based on the current change scope.

- split by domain: `auth.md`, `response.md`, `db.md`, `validation.md`, `security.md`, `testing.md`
- keep each file under 50 lines
- write summaries, not full source dumps
- users may author these files directly, or generate them from existing code and docs
- missing policy files are allowed; the workflow falls back to the existing contract + diff behavior when no policy matches

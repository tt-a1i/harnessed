# Artifact Protocol

Harnessed uses `.harnessed/` as a cross-platform file communication channel.

| File | Purpose | Producer | Consumer |
|------|---------|----------|----------|
| `contract.md` | normalized acceptance criteria | contract-writing | evaluator, gate |
| `qa-report.md` | independent evaluation report | evaluator | orchestrator, gate |
| `qa-state.md` | iteration and staleness state | orchestrator | orchestrator, gate |
| `verification-summary.md` | final evidence report | verification-gate | user |
| `failure-patterns.md` | persistent learning store | orchestrator | contract-writing |
| `.lock` | advisory session lock | adapter | adapter |

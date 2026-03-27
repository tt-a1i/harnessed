# Harnessed Feature Matrix

This file is the canonical cross-platform feature matrix.

| Harnessed capability | Core definition | Claude adapter | Codex adapter | OpenCode adapter | Notes |
|---|---|---|---|---|---|
| Meta-skill bootstrap | `core/rules/task-routing.md` | `hooks/session-start` injects `using-harnessed` | `hooks.json` + `hooks/session_start.py` inject `using-harnessed` | explicit commands + plugin events | OpenCode has no direct SessionStart equivalent |
| Contract writing | `core/protocol/contract-format.md` + `core/prompts/contract-writing-guidance.md` | skill | skill | skill or command | artifact stays `.harnessed/contract.md` |
| Independent QA | `core/prompts/evaluator-prompt.md` + `core/prompts/grading-rubric.md` | subagent workflow | custom agent or subagent | subagent | evaluator output stays `.harnessed/qa-report.md` |
| Verification gate | `core/prompts/verification-gate-guidance.md` | skill | skill | skill or command | summary stays `.harnessed/verification-summary.md` |
| Tier detection | `core/rules/tier-detection.md` | skill logic | skill logic | skill logic | rules must not fork |
| Manual review semantics | `core/rules/manual-review-policy.md` | skill logic | skill logic | skill logic | `SHIP_WITH_HUMAN_REVIEW` is canonical |
| Failure-pattern learning | `core/rules/failure-pattern-policy.md` | artifact update | artifact update | artifact update | `failure-patterns.md` never archived |
| Advisory lock | `core/docs/artifact-protocol.md` | skill logic | adapter logic | adapter logic | warning only, not strong locking |

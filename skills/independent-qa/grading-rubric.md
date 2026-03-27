# Grading Rubric

## Per-Criterion Grades

- **PASS** — Criterion fully satisfied. Evidence is direct, current, and strong enough that a skeptical reviewer can independently verify the claim.
- **PARTIAL** — Core behavior exists but the evidence is incomplete, edge cases are unhandled, or confidence is too weak to justify PASS. Weak evidence must be downgraded to PARTIAL rather than inflated.
- **FAIL** — Not satisfied: missing implementation, incorrect results, regression introduced, or execution/static analysis disproves the claim.
- **MANUAL_REVIEW_NEEDED** — Cannot assess by automated means (visual design, UX feel, browser-specific behavior, security-sensitive judgment without sufficient tooling, or unresolved evaluator uncertainty). Excluded from pass/fail count. Triggers SHIP_WITH_HUMAN_REVIEW instead of SHIP. Must be listed explicitly.

## Confidence Levels

- **High** — Direct code citation plus execution evidence, or corroborated agreement across evaluators.
- **Medium** — Strong code evidence without full execution, or execution on a limited surface.
- **Low** — Ambiguous evidence, excluded diff hunks, stale calibration, unresolved security uncertainty, or reviewer disagreement resolved only by escalation.

Low confidence cannot justify a fully automated SHIP for a high-risk task.

## Security Heuristic Rule

Security review in Harnessed is **issue flagging / heuristic review**, not a full security audit.

- Confirmed exploitable or tool-backed security defects remain **critical**.
- Suspicious patterns without proof of exploitability should still be reported, but they should usually force MANUAL_REVIEW_NEEDED or ITERATE rather than overconfident PASS/FAIL claims.
- Absence of a security finding is never proof that the change is secure.

## Severity Classification (Additional Findings)

- **Critical** — Crash, data corruption, confirmed security vulnerability, destructive behavior without guardrails, or core functionality broken. Any critical = BLOCKED.
- **Major** — Feature partially broken, significant UX issue, missing error handling at system boundary, or high-signal security concern requiring immediate follow-up.
- **Minor** — Code style, missing non-essential error message, suboptimal but functional behavior, doc mismatch.

## Overall Grade

- **SHIP** — All automatable criteria PASS, zero MANUAL_REVIEW_NEEDED, zero critical findings, zero major findings, confidence not low, and no unresolved reviewer disagreement.
- **SHIP_WITH_HUMAN_REVIEW** — All automatable criteria PASS, but at least one of the following is true: one+ criteria are MANUAL_REVIEW_NEEDED; the task is high-risk with stale/missing calibration; confidence is low or medium on a high-risk boundary; security review is heuristic rather than conclusive. The gate may proceed only if pending human review is listed explicitly.
- **ITERATE** — One+ criteria FAIL/PARTIAL, evidence is too weak to support the current implementation, or reviewer disagreement reveals fixable uncertainty.
- **BLOCKED** — Critical findings, fundamentally flawed approach, >50% criteria FAIL, or reviewer disagreement remains unresolved after the tie-break path.
- **Precedence:** BLOCKED > ITERATE > SHIP_WITH_HUMAN_REVIEW > SHIP when multiple conditions met.

## Grading Integrity Rules

1. **Never inflate.** PASS vs PARTIAL doubt → PARTIAL.
2. **Grade code, not intent.** "Probably meant to..." is not evidence.
3. **Weak evidence downgrades.** If support is indirect, ambiguous, or stale, do not PASS.
4. **Pre-existing issues are not findings unless the new code activates or worsens them.**
5. **File:line or it didn't happen.** Every grade needs evidence.
6. **Disagreement is information.** Treat material reviewer disagreement as a signal to escalate, not noise to ignore.

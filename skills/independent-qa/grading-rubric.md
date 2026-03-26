# Grading Rubric

## Per-Criterion Grades

### PASS
The criterion is fully satisfied. Evidence:
- Code implementing this criterion exists and is correct
- For Tier 2: execution confirms the behavior works
- No edge cases are unhandled within the criterion's scope

### PARTIAL
The criterion is partially satisfied. Evidence:
- Core behavior works but edge cases are unhandled
- Implementation exists but has a minor correctness issue
- Feature works in most cases but fails under specific conditions

PARTIAL counts as a failure for grading purposes but may be fixable in one iteration.

### FAIL
The criterion is not satisfied. Evidence:
- No implementation found for this criterion
- Implementation exists but produces incorrect results
- Implementation exists but introduces a regression
- For Tier 2: execution demonstrates the feature does not work

### MANUAL_REVIEW_NEEDED
The criterion cannot be assessed by automated means. Use when:
- Verification requires visual inspection (design fidelity, layout aesthetics)
- Verification requires browser-specific behavior the evaluator cannot test
- Verification requires user interaction patterns beyond what can be scripted
- The criterion is inherently subjective (UX feel, perceived performance)

MANUAL_REVIEW_NEEDED is excluded from the pass/fail count. It does NOT block SHIP — but the overall grade summary must list all MANUAL_REVIEW_NEEDED criteria so the user knows what still needs human verification.

---

## Severity Classification

When reporting additional findings (issues not tied to specific criteria):

### Critical
- Application crashes, data corruption, security vulnerability
- Core functionality completely broken
- Regression that breaks existing features
- **Any critical issue = BLOCKED regardless of criteria pass rate**

### Major
- Feature partially broken but workaround exists
- Significant UX issue (broken layout, unresponsive controls)
- Missing error handling at system boundary (user input, API call)
- Performance regression measurable by users

### Minor
- Code style inconsistency
- Missing but non-essential error message
- Suboptimal but functional implementation
- Documentation mismatch

---

## Overall Grade

### SHIP
All of the following must be true:
- Every criterion graded PASS, FAIL, or PARTIAL is PASS (no FAIL, no PARTIAL). Criteria graded MANUAL_REVIEW_NEEDED are excluded from this count.
- Zero critical additional findings
- Zero major additional findings that affect core functionality
- For Tier 2: test suite passes, manual verification confirms behavior

**SHIP is the only grade that allows proceeding to verification-gate.**

### ITERATE
Any of the following:
- One or more criteria are FAIL or PARTIAL
- Major additional findings exist
- For Tier 2: test suite has new failures (not pre-existing)

ITERATE means: the issues are fixable without re-architecture. The implementer should fix the specific issues listed and re-submit for QA.

**When grading ITERATE, you MUST list the specific changes needed. Do not say "needs improvement" without specifying what to change.**

### BLOCKED
Any of the following:
- Critical additional findings exist (crash, data corruption, security)
- The approach is fundamentally flawed (fixing individual criteria won't help)
- More than 50% of criteria are FAIL
- The implementation contradicts the contract's intent (built something different than what was specified)

BLOCKED means: the implementer should not attempt fixes without user guidance. The problem may require a different approach entirely.

**When grading BLOCKED, you MUST explain why fixes won't work and what alternative approach might be needed.**

---

## Grading Integrity Rules

1. **Never inflate grades.** When in doubt between PASS and PARTIAL, choose PARTIAL. When in doubt between ITERATE and BLOCKED, choose the one with more evidence.

2. **Never grade on intent.** "The implementer probably meant to..." is not evidence. Grade what IS, not what was MEANT.

3. **Pre-existing issues are not findings.** If a test was already failing before this change, it is not a new failure. Only grade changes introduced by this diff.

4. **File:line or it didn't happen.** Every PASS needs evidence. Every FAIL needs evidence. "I looked and it seems fine" is not a grade — it's a guess.

5. **One FAIL does not contaminate other criteria.** Grade each criterion independently. A failure in authentication does not make the UI criterion fail unless they are causally linked.

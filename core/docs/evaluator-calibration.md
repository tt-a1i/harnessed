# Evaluator Calibration

Harnessed treats evaluator quality as an operational concern, not a hidden assumption.

## Calibration Set

The calibration set is a curated collection of representative review cases used to sanity-check evaluator behavior after changes to:
- evaluator prompts
- grading rubric
- review mode routing
- model family or evaluator configuration

Each calibration case should include:
- task summary
- contract excerpt
- diff or fixture
- expected per-criterion grades
- expected confidence level
- expected human-review carry-through

## Drift Detection

Evaluator drift is any meaningful change in grading behavior after prompt, model, or workflow updates.

Check for drift when:
- the evaluator prompt changes
- the grading rubric changes
- high-risk review routing changes
- the underlying model changes

## Required Behaviors to Re-check

At minimum, calibration should verify that the evaluator:
- does not inflate weak evidence to PASS
- preserves MANUAL_REVIEW_NEEDED for human-judgment criteria
- downgrades low-certainty high-risk reviews to human follow-up
- treats self-review as non-evidence
- preserves prompt-level mitigation boundaries for untrusted artifacts
- reports uncertainty explicitly instead of guessing

## Operating Policy

- If calibration status is **missing** or **stale**, high-risk tasks cannot claim plain SHIP through QA alone.
- The evaluator may still review the code, but the final path must carry human review explicitly.
- Drift detection is part of release governance, not optional polish.

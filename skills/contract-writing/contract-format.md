# Contract Format Reference

This is the single source of truth for the Harnessed contract format. All producers (contract-writing, complementary mode synthesis) and consumers (independent-qa, evaluator, verification-gate) must use this format.

## Format

```markdown
# Contract: {task title}

## Task
{One-line description of what needs to be built or fixed}

## Acceptance Criteria

### Functional
- [ ] {Criterion — must be verifiable by reading code, running a command, or observing behavior}

### Edge Cases
- [ ] {Edge case that must be handled}

### Regression
- [ ] {Existing behavior that must NOT break}

## Verification Commands
{Commands that can be run to verify criteria. One per line.}
- `{command}` — verifies {which criterion}

## Out of Scope
- {Explicitly excluded items — things the evaluator should NOT penalize for missing}
```

## Rules

- Every criterion uses the `- [ ]` checkbox prefix
- Sections (Functional, Edge Cases, Regression) may be empty but should not be omitted
- Verification Commands maps criteria to runnable commands; use "Manual: {description}" for criteria that require human verification
- Out of Scope explicitly excludes items to prevent evaluator over-reach

## Complementary Mode

When synthesizing a contract from Superpowers specs, the output must follow this exact format. The `## Verification Commands` section should be synthesized from the spec's testing guidance or inferred from the project's test infrastructure (e.g., if the project uses pytest, generate `pytest -k "relevant_test"` commands).

---
name: using-harnessed
description: Use at the start of every session and before completing any task. Activates independent quality verification for coding work. Routes to contract-writing, independent-qa, and verification-gate skills.
---

# Harnessed: Independent Quality Verification

You have the Harnessed plugin active. Harnessed ensures that code you write is independently verified before being declared complete. Your work is not "done" until an isolated evaluator — separate from you — confirms it works.

## How Harnessed Works

Harnessed adds three capabilities to your workflow:

1. **Contract Writing** — Before coding, generate testable acceptance criteria
2. **Independent QA** — After coding, a separate evaluator subagent verifies your work
3. **Verification Gate** — Before declaring "done", provide structured evidence for every criterion

These skills are invoked via the `Skill` tool using `harnessed:<skill-name>`.

## When to Activate Skills

### Detect Operating Mode

First, determine if Superpowers is present:

**Check:** Does the skill `superpowers:using-superpowers` exist in the current session?

- **Superpowers detected → Complementary Mode**
  - SKIP `harnessed:contract-writing` (Superpowers handles planning/specs)
  - USE `harnessed:independent-qa` after each coding round (read Superpowers spec from `docs/superpowers/specs/` as the acceptance criteria)
  - USE `harnessed:verification-gate` before completion

- **Superpowers not detected → Standalone Mode**
  - USE `harnessed:contract-writing` before any coding task
  - USE `harnessed:independent-qa` after each coding round
  - USE `harnessed:verification-gate` before completion

### Skill Routing Rules

| Trigger | Action |
|---------|--------|
| User gives a coding task (new feature, bug fix, refactor) | Invoke `harnessed:contract-writing` (standalone) or proceed to coding (complementary) |
| A round of code generation is complete | Invoke `harnessed:independent-qa` |
| QA returns ITERATE | Fix issues, then re-invoke `harnessed:independent-qa` |
| QA returns SHIP | Invoke `harnessed:verification-gate` |
| QA returns BLOCKED | Stop. Present report to user. Do NOT attempt fixes without user input. |
| About to say "done", "complete", "finished", or any completion signal | Invoke `harnessed:verification-gate` FIRST |
| Max QA iterations (3) reached without SHIP | Escalate to user with full QA history |

### Task Size Routing

Not every change needs the full pipeline:

| Task Size | Indicators | Pipeline |
|-----------|-----------|----------|
| **Micro** | Single-line fix, typo, config value change, comment edit | Skip contract + QA. Use verification-gate only. |
| **Standard** | New function, bug fix, UI component, API endpoint | Full pipeline: contract → code → QA → gate |
| **Large** | New feature, multi-file refactor, architecture change | Full pipeline with explicit user review at contract stage |

**When in doubt, treat as Standard.** It is always safer to over-verify than under-verify.

## Priority Hierarchy

1. **User instructions** (CLAUDE.md, direct requests) — highest priority, always override
2. **Harnessed skills** — override default behavior for quality verification
3. **Superpowers skills** (if present) — process discipline
4. **Default system prompt** — lowest priority

## The Harnessed Directory

All Harnessed artifacts are written to `.harnessed/` in the project root:

```
.harnessed/
├── contract.md              # Acceptance criteria (standalone mode)
├── qa-report.md             # Latest QA evaluation report
└── verification-summary.md  # Evidence summary for completion
```

Create this directory if it does not exist. These files are the communication channel between skills — they ensure that the QA subagent and verification gate operate on the same criteria without sharing your conversation context.

## Anti-Rationalization

You WILL feel the urge to skip Harnessed steps. Every rationalization below has been observed in production and leads to bugs shipping:

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "This change is too small for QA" | 3-line diffs cause production outages. Size does not predict risk. | If it touches logic, run QA. Use micro routing ONLY for truly inert changes. |
| "I already tested it myself" | Self-testing is not independent testing. You share assumptions with your own code. Research shows 31% disagreement between self-eval and independent eval. | Run independent QA. Your self-test is worthless for verification. |
| "The tests pass" | Tests passing means tests pass. It does NOT mean the feature works correctly, edge cases are handled, or the UI is usable. | Tests are necessary but not sufficient. QA checks what tests don't cover. |
| "It's just a refactor" | Refactors are the #1 source of silent regressions. Behavior should be identical — prove it. | Run QA. If it's truly identical, QA will confirm quickly. |
| "QA will slow me down" | Shipping broken code slows the user down far more. 42% of AI-generated code fails tests initially. | QA is not overhead. QA is the product. |
| "The user didn't ask for QA" | The user installed Harnessed. That IS asking for QA. | Run QA. |
| "I'll QA everything at the end" | Compound bugs are exponentially harder to find and fix than incremental ones. | QA after each coding round, not at the end. |
| "The evaluator was too strict last time" | Strictness is the point. If criteria are wrong, fix the criteria. Never weaken the evaluator. | Adjust the contract, not the evaluator's standards. |

<HARD-GATE>
THESE RULES ARE NON-NEGOTIABLE.

Violating the letter of these rules IS violating the spirit.

"It's fine this one time" is NEVER true. If you catch yourself thinking any thought from the table above, STOP and follow the correct procedure.
</HARD-GATE>

## Quick Reference

```
Standalone Mode:
  Task → contract-writing → CODE → independent-qa → (fix loop) → verification-gate → Done

Complementary Mode (with Superpowers):
  Task → [Superpowers planning] → CODE → independent-qa → (fix loop) → verification-gate → Done

Micro Task:
  Task → CODE → verification-gate → Done
```

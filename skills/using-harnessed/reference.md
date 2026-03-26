# Harnessed Reference

This file contains detailed reference information for the Harnessed plugin. Load on-demand if you need more detail beyond what SKILL.md provides.

## How Harnessed Works

Harnessed adds three capabilities to your workflow:

1. **Contract Writing** — Before coding, generate testable acceptance criteria
2. **Independent QA** — After coding, a separate evaluator subagent verifies your work
3. **Verification Gate** — Before declaring "done", provide structured evidence for every criterion

These skills are invoked via the `Skill` tool using `harnessed:<skill-name>`.

## Priority Hierarchy

1. **User instructions** (CLAUDE.md, direct requests) — highest priority, always override
2. **Harnessed skills** — override default behavior for quality verification
3. **Superpowers skills** (if present) — process discipline
4. **Default system prompt** — lowest priority

**User overrides:** The user can adjust Harnessed scope (e.g., "treat this as a micro task", "skip the contract, just do QA") — always respected. The user can also disable verification entirely (e.g., "don't run QA", "skip all checks") — Harnessed will comply but will note in its response that independent verification was skipped at the user's request. The HARD-GATEs prevent the *agent* from rationalizing its way out of verification, not from obeying explicit user intent.

## The Harnessed Directory

All Harnessed artifacts are written to `.harnessed/` in the project root:

```
.harnessed/
├── contract.md              # Acceptance criteria (standalone mode)
├── qa-report.md             # Latest QA evaluation report
└── verification-summary.md  # Evidence summary for completion
```

Create this directory if it does not exist. These files are the communication channel between skills — they ensure that the QA subagent and verification gate operate on the same criteria without sharing your conversation context.

## Skill Routing Rules

| Trigger | Action |
|---------|--------|
| User gives a coding task (new feature, bug fix, refactor) | Invoke `harnessed:contract-writing` (standalone) or proceed to coding (complementary) |
| A round of code generation is complete | Invoke `harnessed:independent-qa` |
| QA returns ITERATE | Fix issues, then re-invoke `harnessed:independent-qa` |
| QA returns SHIP | Invoke `harnessed:verification-gate` |
| QA returns BLOCKED | Stop. Present report to user. Do NOT attempt fixes without user input. |
| About to say "done", "complete", "finished", or any completion signal | Invoke `harnessed:verification-gate` FIRST |
| Max QA iterations (3) reached without SHIP | Escalate to user with full QA history |

# Harnessed

Independent quality verification for AI coding agents. Code isn't done until an isolated evaluator confirms it works.

## What It Does

Harnessed adds an independent quality verification loop to your AI coding workflow. Instead of letting the coding agent evaluate its own work, Harnessed dispatches a separate evaluator with no knowledge of the generator's reasoning.

```
Task → Contract → Code → Independent QA → Fix Loop → Verification Gate → Done
```

- **Contract Writing** — Testable acceptance criteria before coding begins
- **Independent QA** — Isolated evaluator subagent grades code against the contract
- **Verification Gate** — Structured evidence (file:line citations) required before "done"

## Installation

### Claude Code

Clone or copy this repository into your project or a shared plugins directory:

```bash
# As a project plugin
cp -r harnessed/ your-project/.claude-plugin-harnessed/

# Or as a global plugin
cp -r harnessed/ ~/.claude/plugins/harnessed/
```

The SessionStart hook automatically activates on every new session.

### With Superpowers

Harnessed detects Superpowers automatically. When both are installed:

- Superpowers handles planning, TDD, and process discipline
- Harnessed handles independent QA and verification
- No duplication, no conflict

## How It Works

### Standalone Mode (no Superpowers)

1. You give a coding task
2. **Contract Writing** generates testable acceptance criteria → `.harnessed/contract.md`
3. Agent writes code
4. **Independent QA** dispatches an isolated evaluator subagent
   - Evaluator sees: diff + contract + project context
   - Evaluator does NOT see: generator's reasoning or self-assessment
   - Evaluator grades each criterion: PASS / FAIL / PARTIAL / MANUAL_REVIEW_NEEDED
   - Overall grade: SHIP / ITERATE / BLOCKED
5. If ITERATE: agent fixes issues, QA re-runs (max 3 rounds)
6. If SHIP: **Verification Gate** collects file:line evidence for every criterion
7. Task complete with full audit trail

### Complementary Mode (with Superpowers)

Same as above, but contract-writing is skipped (Superpowers' specs are used instead).

### Two-Tier Verification

- **Tier 1 (Code Review)** — Always available. Evaluator reads the diff and checks criteria.
- **Tier 2 (Execution Verification)** — Auto-detected when test frameworks or dev servers are present. Evaluator runs tests and interacts with the application.

## Skills

| Skill | Invocation | Purpose |
|-------|-----------|---------|
| using-harnessed | Auto-loaded at session start | Routes to other skills, manages modes |
| contract-writing | `harnessed:contract-writing` | Generates acceptance criteria |
| independent-qa | `harnessed:independent-qa` | Dispatches isolated QA evaluator |
| verification-gate | `harnessed:verification-gate` | Collects completion evidence |

## Artifacts

All Harnessed artifacts are written to `.harnessed/` in your project root:

```
.harnessed/
├── contract.md              # Acceptance criteria
├── qa-report.md             # QA evaluation report
└── verification-summary.md  # Completion evidence
```

## Design Principles

1. **Verification > Process** — A simple plan with verified results beats an elaborate plan with unverified results
2. **Independence > Thoroughness** — A quick independent check catches more than a thorough self-review
3. **Evidence > Assertion** — "It works because file:42 shows X" beats "It works because I wrote it correctly"
4. **Skepticism > Trust** — Default stance is "prove it works" not "assume it works"

## License

MIT

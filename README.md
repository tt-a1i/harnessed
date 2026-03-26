# Harnessed

Independent quality verification for AI coding agents. Code isn't done until an isolated evaluator confirms it works.

## Why

AI coding agents evaluate their own work — and get it wrong. Research shows self-evaluation disagrees with independent evaluation 31% of the time, and AI-generated code initially passes only 42% of comprehensive tests. The fix is simple: don't let the same agent that wrote the code judge the code.

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

```bash
# Clone the repository
git clone https://github.com/tt-a1i/harnessed.git

# Install as a project plugin
cp -r harnessed/ your-project/

# Or install globally
cp -r harnessed/ ~/.claude/plugins/harnessed/

# Ensure the hook is executable
chmod +x harnessed/hooks/session-start
```

To verify: start a new Claude Code session and give a coding task. You should see Harnessed generate a contract in `.harnessed/contract.md` before coding begins.

**Important:** Add `.harnessed/` to your project's `.gitignore` — Harnessed writes QA artifacts there.

### With Superpowers

Harnessed detects Superpowers automatically. When both are installed:

- Superpowers handles planning, TDD, and process discipline
- Harnessed handles independent QA and verification
- No duplication, no conflict

When both are installed, Harnessed QA runs after Superpowers' process completes.

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

## Example QA Report

After running independent QA, Harnessed produces a structured report at `.harnessed/qa-report.md`:

```markdown
# QA Report

## Overview
- **Verification Tier:** 2
- **Overall Grade:** ITERATE
- **Criteria Passed:** 7/9
- **Critical Issues:** 0

## Per-Criterion Evaluation

### Criterion: "Selected theme persists across page reloads"
- **Grade:** FAIL
- **Evidence:** src/hooks/useTheme.ts:24 — localStorage.setItem is called but getItem on line 8 reads from wrong key ("theme" vs "color-theme")
- **Finding:** Theme preference is written to localStorage under key "color-theme" but read back under key "theme", so it never persists.
- **Action Required:** Align the localStorage key in useTheme.ts lines 8 and 24.

### Criterion: "Dark mode applies to all UI elements"
- **Grade:** PARTIAL
- **Evidence:** src/components/Header.tsx:15 — className does not include theme variable
- **Finding:** Header component does not consume the theme context. Background stays white in dark mode.
- **Action Required:** Import and apply theme class in Header.tsx.
```

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

## Cost

Each QA round spawns one evaluator subagent. A typical task uses 1-2 QA rounds. Expect roughly 1.5x the token usage of coding without Harnessed. The tradeoff: catching bugs before the user reports them vs. catching them after.

## Design Principles

1. **Verification > Process** — A simple plan with verified results beats an elaborate plan with unverified results
2. **Independence > Thoroughness** — A quick independent check catches more than a thorough self-review
3. **Evidence > Assertion** — "It works because file:42 shows X" beats "It works because I wrote it correctly"
4. **Skepticism > Trust** — Default stance is "prove it works" not "assume it works"

## License

MIT

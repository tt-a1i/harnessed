# Harnessed

[中文版](README.zh-CN.md)

Independent quality verification for AI coding agents. Code isn't done until an isolated evaluator confirms it works.

## Why

AI coding agents evaluate their own work — and get it wrong. Research shows self-evaluation disagrees with independent evaluation 31% of the time, and AI-generated code initially passes only 42% of comprehensive tests. The fix is simple: don't let the same agent that wrote the code judge the code.

## What It Does

Harnessed adds an independent QA loop to your AI coding workflow:

```
Standalone:     Task → Contract → Code → QA → Fix Loop → Gate → Done
Complementary:  Task → SP Planning → Code → QA → Fix Loop → Gate → Done
Micro:          Task → Code → Gate → Done
```

- **Contract Writing** — Testable acceptance criteria before coding begins. After drafting, every user requirement is mapped to a criterion and gaps are filled automatically.
- **Independent QA** — Isolated evaluator subagent grades code against the contract
- **Verification Gate** — Structured evidence (file:line citations) required before "done". If code changed since QA last ran, the gate re-runs QA before accepting.

## Installation

### Claude Code (Plugin Marketplace — recommended)

```bash
# Register the Harnessed marketplace (one-time)
claude plugin marketplace add tt-a1i/harnessed

# Install the plugin
claude plugin install harnessed
```

Updates are automatic — Claude Code syncs plugins on startup.

### Manual Installation (alternative)

```bash
# Clone the repository
git clone https://github.com/tt-a1i/harnessed.git

# Option A: Install as a project plugin (project-local)
cp -r harnessed/ your-project/harnessed/

# Option B: Install globally for all projects
cp -r harnessed/ ~/.claude/plugins/harnessed/
```

> If you downloaded a zip instead of cloning, run `chmod +x harnessed/hooks/session-start`.

### After Installation

Verify: start a new Claude Code session — you should see Harnessed respond with "I'll draft acceptance criteria before coding" on your first coding task.

Harnessed automatically adds `.harnessed/` to your project's `.gitignore` on first use.

### With Superpowers

Harnessed detects Superpowers automatically. When both are installed:

- Superpowers handles planning, TDD, and process discipline
- Harnessed handles independent QA and verification
- No duplication, no conflict

When both are installed, Harnessed QA runs after Superpowers' process completes. If Superpowers is detected but no specs exist for the current task, Harnessed falls back to Standalone Mode.

## How It Works

### Standalone Mode (no Superpowers)

1. You give a coding task
2. **Contract Writing** generates testable acceptance criteria → `.harnessed/contract.md`
3. Agent writes code
4. **Independent QA** dispatches an isolated evaluator subagent
   - Evaluator sees: diff + contract + project context
   - Evaluator does NOT see: generator's reasoning or self-assessment
   - Evaluator grades each criterion: PASS / FAIL / PARTIAL / MANUAL_REVIEW_NEEDED
   - Overall grade: **SHIP** (all pass — ready to complete) / **SHIP_WITH_HUMAN_REVIEW** (code checks pass but some criteria need human verification) / **ITERATE** (issues found — agent fixes and re-runs QA) / **BLOCKED** (fundamental problems — requires your input)
5. If ITERATE: agent fixes issues, QA re-runs (max 3 rounds)
6. If SHIP or SHIP_WITH_HUMAN_REVIEW: **Verification Gate** collects file:line evidence for every criterion
7. Task complete with full audit trail

### Complementary Mode (with Superpowers)

Same as above, but contract-writing is skipped (Superpowers' specs are used instead).

### Three-Tier Verification

- **Tier 1 (Code Review)** — Always available. Evaluator reads the diff and checks criteria.
- **Tier 1.5 (HTTP Smoke Tests)** — Auto-detected when a dev server is running but no test suite is present. Evaluator uses curl/HTTP requests to verify behavior against the live server.
- **Tier 2 (Execution Verification)** — Auto-detected when test frameworks are present. Evaluator runs tests and interacts with the application.

### Project-Level Learning

The independent QA evaluator categorizes each failure it finds, and those categories are recorded in `.harnessed/failure-patterns.md` across tasks. During contract writing, patterns with Count ≥ 2 automatically inform acceptance criteria so the same class of bug doesn't recur. One-off patterns decay after 90 days.

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
├── contract.md              # Acceptance criteria (written in both modes)
├── failure-patterns.md      # Recurring failure categories (persistent across tasks)
├── qa-report.md             # QA evaluation report
├── qa-state.md              # Iteration count and dispatch timestamp
├── verification-summary.md  # Completion evidence
└── archive/                 # Archived artifacts from previous tasks
```

**Note:** Concurrent Claude Code sessions in the same project directory are not fully supported. Harnessed uses an advisory lock (`.harnessed/.lock`) to detect and warn about concurrent sessions, but this is best-effort only — artifacts from one session may still overwrite another's.

## Cost

Each QA round spawns one evaluator subagent. A typical task uses 1-2 QA rounds. Expect roughly 1.5x the token usage of coding without Harnessed. The tradeoff: catching bugs before the user reports them vs. catching them after.

## Customization

- **Skip QA for a task:** Tell Claude "skip QA" or "treat this as a micro task"
- **Skip the contract:** Tell Claude "skip the contract, just do QA"
- **Disable entirely:** Tell Claude "don't run Harnessed" — it will comply but note that verification was skipped
- Harnessed always respects explicit user instructions. The automated gates prevent the *agent* from skipping verification on its own, not the user from choosing to skip it.

## Design Principles

1. **Verification > Process** — A simple plan with verified results beats an elaborate plan with unverified results
2. **Independence > Thoroughness** — A quick independent check catches more than a thorough self-review
3. **Evidence > Assertion** — "It works because file:42 shows X" beats "It works because I wrote it correctly"
4. **Skepticism > Trust** — Default stance is "prove it works" not "assume it works"

## Troubleshooting

**Harnessed not loading (no contract generated on first task):**
- Run the hook manually: `bash harnessed/hooks/session-start` — it should output JSON containing the meta-skill
- If you get an error, check that `python3` is installed (used for JSON escaping)
- If you downloaded a zip, ensure the hook is executable: `chmod +x harnessed/hooks/session-start`

**QA evaluator fails to produce a report:**
- This usually means the evaluator prompt was too large. Try a smaller diff or fewer criteria.
- After one retry, Harnessed marks the task as BLOCKED and escalates to you.

**Artifacts appearing in git status:**
- Add `.harnessed/` to your project's `.gitignore`

**Concurrent sessions:**
- Running multiple Claude Code sessions on the same project is not fully supported — Harnessed warns via advisory lock but cannot guarantee artifact isolation

## License

MIT

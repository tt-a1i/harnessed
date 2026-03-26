# Harnessed — Design Specification

## Vision

A Claude Code plugin that gives coding agents an independent quality verification loop. Code is not "done" until an isolated evaluator confirms it works.

**Standalone:** Complete and effective without Superpowers — lightweight planning + independent verification produces better outcomes than elaborate process without verification.

**With Superpowers:** Complementary — Superpowers handles process discipline, Harnessed handles quality verification. Detects Superpowers presence and avoids duplication.

---

## Architecture

### Plugin Structure

```
harnessed/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── hooks.json
│   └── session-start
├── skills/
│   ├── using-harnessed/
│   │   ├── SKILL.md
│   │   └── reference.md
│   ├── contract-writing/
│   │   └── SKILL.md
│   ├── independent-qa/
│   │   ├── SKILL.md
│   │   ├── evaluator-prompt.md
│   │   └── grading-rubric.md
│   └── verification-gate/
│       └── SKILL.md
├── docs/
├── .gitignore
├── LICENSE
└── README.md
```

### Loading Mechanism

1. `session-start` hook reads `using-harnessed/SKILL.md`
2. JSON-escapes and injects via `hookSpecificOutput.additionalContext`
3. Wrapped in priority tags for reliable activation
4. All other skills loaded on-demand via Skill tool

### Superpowers Detection

The meta-skill checks for Superpowers presence:
- If detected: Harnessed defers planning/TDD to Superpowers, focuses exclusively on independent verification
- If not detected: Harnessed activates full mode including lightweight contract-writing for planning

---

## Skills Specification

### Skill 1: using-harnessed (Meta-Skill)

**Purpose:** Always-loaded skill that routes to other Harnessed skills and manages Superpowers interop.

**Behavior:**
- Detect task type and size
- Route to appropriate skill(s)
- Detect Superpowers: check if `superpowers:using-superpowers` skill exists
  - Present: skip contract-writing (Superpowers handles planning), invoke independent-qa after build
  - Absent: invoke contract-writing before build, independent-qa after build
- Always invoke verification-gate before declaring any task complete

**Anti-Rationalization Rules:**
- "This change is too small for QA" → If it touches logic, it gets QA
- "I already tested it myself" → Self-testing is not independent testing
- "The tests pass" → Tests passing != feature working correctly
- "It's just a refactor" → Refactors introduce regressions; QA is mandatory

**Priority:**
1. User instructions (CLAUDE.md) — highest
2. Harnessed skills
3. Superpowers skills (if present)
4. Default system prompt

### Skill 2: contract-writing

**Purpose:** Generate testable acceptance criteria before coding begins.

**When to invoke:**
- Standalone mode: at the start of any coding task
- With Superpowers: skipped (Superpowers brainstorming/writing-plans handles this)

**Output:** `.harnessed/contract.md` containing:

```markdown
## Task
{one-line description}

## Acceptance Criteria
- [ ] {criterion 1 — must be verifiable by reading code or running a command}
- [ ] {criterion 2}
...

## Verification Commands
- {command to verify criterion 1, e.g., "npm test", "curl endpoint", "check file exists"}

## Out of Scope
- {explicitly excluded items}
```

**Rules:**
- Each criterion must be independently verifiable
- No subjective criteria ("code should be clean") — only observable outcomes
- Include verification commands where possible
- Keep contracts short: 3-15 criteria max
- Contract is written to a file (not just context) so the QA subagent can read it independently

**Iron Law:**
```
NO CODE WITHOUT A CONTRACT FIRST
```

### Skill 3: independent-qa

**Purpose:** Dispatch an isolated evaluator subagent to verify code against the contract.

**This is the core differentiator of Harnessed.**

**Architecture:**
- QA runs as a separate subagent via Agent tool
- Fresh context — no access to generator's reasoning or assumptions
- Receives: git diff + contract.md + project context (stack, structure)
- Does NOT receive: generator's planning notes, self-assessment, or conversation history

**Two-tier evaluation:**

**Tier 1 — Code Review (always available):**
- Read the diff
- Check each contract criterion against the code
- Identify: missing implementations, logic errors, edge cases, regressions
- Output: structured report with PASS/FAIL per criterion

**Tier 2 — Execution Verification (auto-detected):**
Activated when ANY of these are detected:
- `package.json` with test script
- `pytest.ini`, `pyproject.toml` with test config
- `Makefile` with test target
- Running dev server (port open)
- Playwright/Cypress config present

Tier 2 adds:
- Run test suite, report results
- If dev server: navigate to relevant pages, verify UI behavior
- If API: call endpoints, verify responses
- Report execution results alongside code review

**Evaluator Prompt Design:**
- System prompt positions evaluator as a "skeptical senior engineer"
- Explicitly told: "The implementer may have cut corners. Your job is to find what's broken."
- Must cite specific file:line for every finding
- Must attempt to disprove each PASS (not just confirm)
- Structured output format (not prose)

**Grading:**
- Per-criterion: PASS / FAIL / PARTIAL / MANUAL_REVIEW_NEEDED (with explanation)
- Overall: SHIP / ITERATE / BLOCKED
  - SHIP: all criteria pass, no critical issues
  - ITERATE: some criteria fail, fixable issues identified
  - BLOCKED: fundamental problems requiring re-approach

**Iteration Loop:**
- If ITERATE: QA report fed back to generator, generator fixes, QA re-runs
- Max 3 iterations
- If still ITERATE after max: escalate to user with full report
- If BLOCKED at any point: escalate immediately

**Anti-Rationalization:**
- "QA passed last time on similar code" → Each change gets fresh QA
- "The diff is only 3 lines" → 3-line diffs cause production outages
- "I'll QA the whole feature at the end" → Compound bugs are harder to find; QA each increment
- "The evaluator is being too strict" → Strictness is the point; adjust criteria, not evaluator

### Skill 4: verification-gate

**Purpose:** Final checkpoint before any task is declared complete.

**When to invoke:** ALWAYS, before responding with "done", "complete", "finished", or any completion signal.

**Process:**
1. Read the contract (contract.md or Superpowers spec)
2. For each criterion, provide EVIDENCE of completion:
   - File path + line number where it's implemented
   - Test name that covers it
   - Command output proving it works
3. If any criterion lacks evidence: task is NOT complete
4. Present evidence summary to user

**Iron Law:**
```
NO COMPLETION CLAIMS WITHOUT EVIDENCE FOR EVERY CRITERION
```

**Anti-Rationalization:**
- "It's obviously done, I just wrote it" → Evidence is for the user, not you
- "The QA already passed" → QA checks correctness; gate checks completeness
- "I verified it mentally" → Mental verification is worthless; show file:line or command output

**Key difference from Superpowers' verification-before-completion:**
Superpowers' skill asks the agent to "verify" but the agent can write plausible prose without actually checking (phantom completion, Issue #578). Harnessed requires **structured evidence** (file:line citations, command outputs) that is hard to fabricate convincingly.

---

## File Communication Protocol

Skills communicate through files, not shared context:

| File | Written by | Read by |
|------|-----------|---------|
| `contract.md` | contract-writing | independent-qa, verification-gate |
| `qa-report.md` | independent-qa (evaluator subagent) | generator (for fixes), verification-gate |
| `verification-summary.md` | verification-gate | user (final deliverable) |

Files are written to `.harnessed/` directory in the project root to avoid polluting the workspace.

---

## Superpowers Interop Matrix

| Scenario | contract-writing | independent-qa | verification-gate |
|----------|-----------------|----------------|-------------------|
| Standalone | Active | Active | Active |
| With Superpowers | Skipped (SP plans) | Active (reads SP spec) | Active (reads SP spec) |

When Superpowers is present:
- independent-qa reads from `docs/superpowers/specs/` instead of `contract.md`
- verification-gate checks against Superpowers spec criteria
- No conflict with Superpowers' own verification-before-completion (Harnessed adds structured evidence on top)

---

## Design Principles

1. **Verification > Process** — A simple plan with verified results beats an elaborate plan with unverified results
2. **Independence > Thoroughness** — A quick independent check catches more than a thorough self-review
3. **Evidence > Assertion** — "It works because file:line shows X" beats "It works because I wrote it correctly"
4. **Files > Context** — Communicate through files, not shared conversation history
5. **Skepticism > Trust** — Default stance is "prove it works" not "assume it works"
6. **Adaptability** — Detect environment capabilities and use the strongest verification available

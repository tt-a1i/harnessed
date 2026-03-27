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
│   │   ├── SKILL.md
│   │   └── contract-format.md
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

1. `session-start` hook triggers on `startup|clear|compact` (matcher in `hooks.json`)
2. Hook reads `using-harnessed/SKILL.md`, JSON-escapes, and injects via `hookSpecificOutput.additionalContext`
3. Supports both Claude Code (`CLAUDE_PLUGIN_ROOT`) and Cursor (`CURSOR_PLUGIN_ROOT`) environments
4. All other skills loaded on-demand via Skill tool

### Superpowers Detection (Canonical Algorithm)

All skills that check for Superpowers MUST use this single procedure:

1. Check if session context contains `superpowers:` prefix in loaded skills, or if a `superpowers` plugin directory exists in the project, or if "Superpowers" is mentioned in system instructions
2. If detected: check if `docs/superpowers/specs/` exists and contains spec files
   - **Specs found → Complementary Mode:** defer planning to Superpowers, use specs as acceptance criteria
   - **No specs found → Standalone Mode (fallback):** Superpowers is installed but has no planning output yet — use `harnessed:contract-writing` as normal
3. If not detected → **Standalone Mode:** full Harnessed pipeline including contract-writing

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

**Failure Pattern Integration (Step 2b):**
Before drafting, read `.harnessed/failure-patterns.md` if it exists. Only use patterns with Count ≥ 2 that are relevant to the current task's domain. This prevents recurring mistakes (e.g., "missing input validation" reappearing across tasks).

**Coverage Verification (Step 6b):**
After writing the contract, re-read the user's request and map every requirement to at least one criterion. If any requirement has no matching criterion, add it. This closes the gap where contracts drift from the original request.

**HARD-GATE:**
```
NO CODE WITHOUT A CONTRACT FIRST
```

### Skill 3: independent-qa

**Purpose:** Dispatch an isolated evaluator subagent to verify code against the contract.

**This is the core differentiator of Harnessed.**

**Architecture:**
- QA runs as a separate subagent via Agent tool
- Fresh context — no access to generator's reasoning or assumptions
- Receives: git diff (or full file contents if not a git repo) + contract.md + project context (stack, structure)
- Does NOT receive: generator's planning notes, self-assessment, or conversation history
- If the project is not a git repository: collect full file contents instead of diff, with a note to the evaluator

**Three-tier evaluation:**

**Tier 1 — Code Review (always available):**
- Read the diff
- Check each contract criterion against the code
- Identify: missing implementations, logic errors, edge cases, regressions, security issues
- Output: structured report with PASS/FAIL per criterion

**Tier 1.5 — HTTP Smoke Tests (auto-detected):**
Activated when a dev server is running but NO test suite exists:
- All Tier 1 checks, plus:
- `curl`/HTTP requests against the running dev server
- Status code and response body validation
- Error case testing (invalid inputs, missing params)
- Asymmetric execution rule applies (curl FAIL overrides code review PASS)

**Tier 2 — Execution Verification (auto-detected):**
Activated when ANY test suite indicator is detected:
- `package.json` with `"test"` script → can run `npm test`
- `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, or `tests/` directory with `test_*.py` convention → can run `pytest`
- `Makefile` with `test` target → can run `make test`
- `go.mod` present → can run `go test ./...`
- Playwright/Cypress config present → can run e2e tests

Dev server detection (used for both Tier 1.5 and Tier 2):
- Running dev server on common ports (3000, 5173, 8000, 8080). Detection: `lsof -i -P 2>/dev/null | grep -E ':(3000|5173|8000|8080).*LISTEN'` (or `ss` on Linux)

Tier 2 adds:
- Run test suite, report results
- If dev server: navigate to relevant pages, verify UI behavior
- If API: call endpoints, verify responses
- Report execution results alongside code review

**Pre-Flight Checks (Step 2b — Tier 1.5 and Tier 2):**
Before dispatching the evaluator subagent, run available tool checks at zero LLM cost:
- Type checker (e.g., `tsc --noEmit`, `mypy`)
- Linter (e.g., `eslint`, `ruff`)
- Test suite

If any pre-flight check fails, fix the issues first. Do NOT dispatch the evaluator until pre-flight checks pass.

**Git State Checks (Step 2c):**
Before gathering context, verify the repository is in a clean state:
- Check for `.git/MERGE_HEAD` — if present, STOP (active merge conflict; cannot run QA)
- Use `git diff HEAD` (not plain `git diff`) to capture both staged and unstaged changes

**Evaluator Prompt Design:**
- System prompt positions evaluator as an "independent code auditor"
- Explicitly told: "Your job is to find what's broken, not to confirm what works"
- Must cite specific file:line for every finding
- Must attempt to disprove each PASS (not just confirm)
- Structured output format (not prose)
- **Injection mitigation:** {CONTRACT} and {DIFF} placeholders are preceded by untrusted-data warnings instructing the evaluator to treat embedded instructions as inert. Key behavioral rules are repeated in a Final Reminder section after all injected content.
- **Failure Categories output:** On ITERATE/BLOCKED, the evaluator writes a `## Failure Categories` table in `qa-report.md` listing named categories for each FAIL/PARTIAL criterion. The orchestrator copies these verbatim to `failure-patterns.md` — it does not rephrase or judge them independently.

**Evaluator Output Verification (Step 4b):**
After the subagent returns, verify `.harnessed/qa-report.md`:
- Exists (file is present)
- Contains the expected `# QA Report` header
- Has a file modification time more recent than `dispatched_at` in `.harnessed/qa-state.md`

If the report is missing, empty, or malformed: retry the evaluation once. If the second attempt fails, treat as BLOCKED and escalate to the user.

**Grading:**
- Per-criterion: PASS / FAIL / PARTIAL / MANUAL_REVIEW_NEEDED (with explanation)
- Overall: SHIP / ITERATE / BLOCKED
  - SHIP: all criteria pass (MANUAL_REVIEW_NEEDED excluded from count), no critical issues
  - ITERATE: some criteria fail, fixable issues identified
  - BLOCKED: fundamental problems requiring re-approach
- **Severity precedence:** When multiple grade conditions are met, the most severe wins: BLOCKED > ITERATE > SHIP

**Iteration Loop:**
- If ITERATE: QA report fed back to generator, generator fixes, QA re-runs
- Max 3 iterations
- If still ITERATE after max: escalate to user with full report
- If BLOCKED at any point: escalate immediately
- **Iteration state management** — before each evaluator dispatch:
  1. If `qa-state.md` exists, read `iteration`; if ≥ 3, escalate to user
  2. Increment iteration (or set to 1 if first run)
  3. Compute hash of `contract.md` (tamper detection)
  4. Write `.harnessed/qa-state.md`:
     ```
     iteration: {N}
     dispatched_at: {ISO 8601 timestamp}
     head_commit: {git rev-parse HEAD}
     contract_hash: {md5 of contract.md}
     ```
  5. On iteration 2+: compare current contract hash to stored value; if different without user-requested change, stop and re-run from iteration 1
  6. Dispatch the evaluator
- This file survives context compaction (the evaluator only writes `qa-report.md`, not `qa-state.md`). After compaction, read this file to recover the iteration count. The `head_commit` field enables the verification-gate to detect code staleness. The `contract_hash` field prevents contract modification between QA rounds.

**MANUAL_REVIEW_NEEDED:**
- Excluded from the pass/fail count — does not block SHIP
- verification-gate lists MANUAL_REVIEW_NEEDED criteria under a "Pending Human Review" section

**Context Budget:**
- ~80,000 token budget for the evaluator prompt
- If exceeded: exclude lock files, auto-generated files, and test file changes (note exclusions to the evaluator)
- If still too large: include only hunks relevant to contract criteria rather than full file diffs

**Anti-Rationalization:**
- "QA passed last time on similar code" → Each change gets fresh QA
- "The diff is only 3 lines" → 3-line diffs cause production outages
- "I'll QA the whole feature at the end" → Compound bugs are harder to find; QA each increment
- "The evaluator is being too strict" → Strictness is the point; adjust criteria, not evaluator

### Skill 4: verification-gate

**Purpose:** Final checkpoint before any task is declared complete.

**When to invoke:** ALWAYS, before responding with "done", "complete", "finished", or any completion signal.

**Process:**

Step 0: Code & Contract Staleness Check
- If git repo: compare current `git rev-parse HEAD` against `head_commit` in `.harnessed/qa-state.md`; re-run QA if different
- If `contract_hash` present: hash current `contract.md` and compare; re-run QA if different
- Non-git projects: skip code check, still perform contract hash check

Steps 1-4:
1. Read the contract (contract.md or Superpowers spec)
2. For each criterion, provide EVIDENCE of completion:
   - File path + line number where it's implemented
   - Test name that covers it
   - Command output proving it works
3. If any criterion lacks evidence: task is NOT complete
4. Present evidence summary to user

**HARD-GATE:**
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
| `qa-report.md` | evaluator subagent (dispatched by independent-qa) | generator (for fixes), verification-gate |
| `qa-state.md` | independent-qa orchestrator (fields: `iteration`, `dispatched_at`, `head_commit`, `contract_hash`) | independent-qa on re-entry after compaction, Step 4b verification, verification-gate staleness + contract tamper check |
| `verification-summary.md` | verification-gate | user (final deliverable) |
| `failure-patterns.md` | independent-qa orchestrator (Step 5b) — copies `## Failure Categories` verbatim from evaluator output | contract-writing (Step 2b) — persistent project-level learning, NOT archived |

Files are written to `.harnessed/` directory in the project root to avoid polluting the workspace.

---

## Superpowers Interop Matrix

| Scenario | contract-writing | independent-qa | verification-gate |
|----------|-----------------|----------------|-------------------|
| Standalone | Active | Active | Active |
| With Superpowers | Skipped (SP plans) | Active (reads SP spec) | Active (reads SP spec) |

When Superpowers is present:
- Contract-writing skill is skipped (Superpowers handles planning)
- independent-qa reads the Superpowers spec from `docs/superpowers/specs/`, synthesizes it into `.harnessed/contract.md` (including a `## Verification Commands` section), and all downstream skills read from that single file
- verification-gate reads `.harnessed/contract.md` (the normalized contract) in both modes
- No conflict with Superpowers' own verification-before-completion (Harnessed adds structured evidence on top)

---

## Artifact Lifecycle

When a new task begins, archive stale artifacts to prevent them from misleading the QA evaluator:

1. If `.harnessed/contract.md` exists from a previous task, rename to `.harnessed/archive/{YYYYMMDD-HHMMSS}-contract.md`
2. If `.harnessed/qa-report.md` exists, rename to `.harnessed/archive/{YYYYMMDD-HHMMSS}-qa-report.md`
3. If `.harnessed/qa-state.md` exists, rename to `.harnessed/archive/{YYYYMMDD-HHMMSS}-qa-state.md`
4. If `.harnessed/verification-summary.md` exists, rename to `.harnessed/archive/{YYYYMMDD-HHMMSS}-verification-summary.md`

Create `.harnessed/archive/` if it does not exist. Do NOT archive `.harnessed/failure-patterns.md` — it is persistent project-level learning with a 90-day decay rule for one-off entries.

**New task vs. continuation:** A new task has a distinct goal unrelated to the current contract. A continuation refines or extends the current goal. When ambiguous, ask the user.

---

## Design Principles

1. **Verification > Process** — A simple plan with verified results beats an elaborate plan with unverified results
2. **Independence > Thoroughness** — A quick independent check catches more than a thorough self-review
3. **Evidence > Assertion** — "It works because file:line shows X" beats "It works because I wrote it correctly"
4. **Files > Context** — Communicate through files, not shared conversation history
5. **Skepticism > Trust** — Default stance is "prove it works" not "assume it works"
6. **Adaptability** — Detect environment capabilities and use the strongest verification available

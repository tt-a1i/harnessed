---
name: independent-qa
description: Use after completing a round of code generation.
user-invocable: true
---

# Independent QA

Dispatch an isolated evaluator subagent to verify your code. The evaluator operates in a clean context with NO access to your reasoning, assumptions, or self-assessment. It grades your work against the contract.

**This is the core of Harnessed.** Self-evaluation is unreliable. You cannot objectively judge your own work.

## When This Skill Activates

- After completing a round of code changes (new code, bug fix, refactor)
- After fixing issues from a previous QA round (re-evaluation)
- NOT for micro tasks (single-line, config-only, comment-only changes)

## Execution Flow

### Step 1: Locate the Contract

Determine the acceptance criteria source:

- **Standalone mode:** Read `.harnessed/contract.md`
- **Complementary mode (Superpowers):** Read the spec from `docs/superpowers/specs/` (use the most recent spec file relevant to the current task). Extract discrete, verifiable criteria from the spec. If the spec is narrative without explicit criteria, synthesize one criterion per stated requirement. Present extracted criteria in the same format as a Harnessed contract — including a `## Verification Commands` section synthesized from the spec's testing guidance or inferred from the project's test infrastructure. Write the normalized contract to `.harnessed/contract.md` so that the verification-gate reads from the same source. Use this content for the `{CONTRACT}` placeholder. If the spec contains no identifiable requirements, invoke `harnessed:contract-writing` to create a contract.

If no contract/spec exists: STOP. Invoke `harnessed:contract-writing` first. Do NOT run QA without criteria.

### Step 2: Detect Verification Tier

Check the project for available verification infrastructure:

**Test suite indicators:**
- `package.json` with `"test"` script → can run `npm test`
- `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, or `tests/` directory with `test_*.py` → can run `pytest`
- `Makefile` with `test` target → can run `make test`
- `go.mod` present → can run `go test ./...`
- `playwright.config.*` or `cypress.config.*` → can run e2e tests

**Dev server indicators:**
- Dev server running (check common ports: 3000, 5173, 8000, 8080). Use `lsof -i -P 2>/dev/null | grep -E ':(3000|5173|8000|8080).*LISTEN'` to detect running servers. On Linux where `lsof` is unavailable, use `ss -tlnp 2>/dev/null | grep -E ':(3000|5173|8000|8080)'` instead.

**Tier assignment:**
- **Tier 2** (code review + full execution): any test suite indicator found
- **Tier 1.5** (code review + HTTP smoke tests): no test suite, but dev server is running — evaluator uses `curl`/HTTP requests to verify behavior against the live server
- **Tier 1** (code review only): no test suite and no dev server

Record which tier is active — include it in the evaluator prompt.

### Step 2b: Pre-Flight Checks (Tier 1.5 and Tier 2)

Before dispatching the expensive evaluator subagent, run available tool checks at zero LLM cost:

- If type checker available (e.g., `tsc --noEmit`, `mypy`): run it
- If linter available (e.g., `eslint`, `ruff`): run it
- If test suite available: run it

If any pre-flight check fails, fix the issues first. Do NOT dispatch the evaluator until pre-flight checks pass. This prevents wasting an evaluator round on errors that tools catch for free.

### Step 2c: Git State Checks

Before gathering context, verify the repository is in a clean state for evaluation:

- **Merge conflict active:** Check for `.git/MERGE_HEAD`. If present, STOP — do not dispatch the evaluator. Inform the user: "Cannot run QA during an active merge conflict. Resolve the conflict first."
- **Diff command:** Use `git diff HEAD` to capture both staged and unstaged changes. Plain `git diff` misses staged changes.

### Step 3: Gather Context for Evaluator

Collect the following — this is ALL the evaluator will see:

| Include | Why |
|---------|-----|
| The contract/spec content | Criteria to evaluate against |
| `git diff HEAD` output (captures both staged and unstaged changes) | The actual code to review |
| Project stack info (language, framework, test runner) | Context for evaluation |
| Verification tier (1 or 2) | What the evaluator can do |
| Available verification commands from contract | How to verify |

**DO NOT include:**
- Your reasoning or thought process
- Your self-assessment of the code
- Your conversation history with the user
- Your planning notes
- Any "helpful context" about why you made certain choices

The evaluator must judge the CODE, not your INTENT.

**If `git diff` produces no output:** STOP. Do not dispatch the evaluator. Inform the user that there are no code changes to evaluate. Offer: "If changes were already committed, I can evaluate the last commit using `git diff HEAD~1`. Would you like me to do that?" If the user agrees, use `git diff HEAD~1` as the diff source and proceed normally.

**If the project is not a git repository:** Collect changes by listing all files created or modified during this session. Provide full file contents to the evaluator in place of the diff, with a note: "No git repository. Full file contents provided." The evaluator should review these against the contract criteria.

**Context budget:** If the combined evaluator prompt exceeds ~80,000 tokens, reduce the diff by excluding lock files, auto-generated files (e.g., `package-lock.json`, `yarn.lock`, `*.min.js`, compiled output in `dist/` or `build/`, code-generated API clients), and test file changes (note exclusions to the evaluator). If still too large, include only hunks relevant to contract criteria rather than full file diffs.

**Binary files:** `git diff` shows only `Binary files differ` for images, fonts, and other binaries. If a contract criterion involves binary assets, note in the evaluator prompt: "Binary file {path} was changed but content is not diffable." The evaluator should mark such criteria as MANUAL_REVIEW_NEEDED rather than FAIL.

### Step 4: Dispatch Evaluator Subagent

Use the **Agent tool** to spawn the evaluator subagent with the description **"Independent QA evaluation"**.

**Construct the prompt:**

1. Read `skills/independent-qa/evaluator-prompt.md` to get the prompt template
2. Read `skills/independent-qa/grading-rubric.md` to get the grading rubric content
3. Replace all placeholders with collected context:
   - `{CONTRACT}` — the full contract/spec content
   - `{DIFF}` — the `git diff HEAD` output
   - `{STACK}` — project stack description (language, framework, package manager, test runner; use "unknown" for undetectable components)
   - `{TIER}` — 1, 1.5, or 2
   - `{MODE}` — "all-criteria" (default; reserved for future per-criterion evaluation)
   - `{VERIFICATION_COMMANDS}` — commands from contract
   - `{GRADING_RUBRIC}` — content from `grading-rubric.md`
4. Paste the FULL content of each placeholder. Never summarize, truncate, or paraphrase. The evaluator sees ONLY what you provide — omitted content is invisible content.

**Subagent configuration:**
- Tool: Agent tool
- Description: "Independent QA evaluation"
- Permissions: the subagent needs read, write, and execute permissions (required for Tier 2 execution verification and writing qa-report.md)
- The evaluator runs in the project directory with full filesystem access — it can read any file, run commands, and search the codebase beyond the diff
- The evaluator writes its report to `.harnessed/qa-report.md`

**Escalation protocol:** If the evaluator encounters a criterion it cannot assess (e.g., requires manual browser testing, visual design judgment, or UX feel that cannot be verified programmatically), it must mark that criterion as `MANUAL_REVIEW_NEEDED` rather than guessing. The evaluator should never fabricate a PASS or FAIL for something it cannot actually verify.

### Step 4b: Verify Evaluator Output

After the evaluator subagent returns, verify that `.harnessed/qa-report.md`:
- Exists (file is present)
- Contains the expected `# QA Report` header
- Has a file modification time more recent than the `dispatched_at` timestamp in `.harnessed/qa-state.md` (confirms the report is from this dispatch, not stale)

If the report is missing, empty, or malformed: retry the evaluation once with the same inputs. If the second attempt also fails, treat as BLOCKED with reason "QA evaluator failed to produce a valid report" and escalate to the user. Do NOT proceed without a valid QA report.

### Step 5: Process QA Results

Read `.harnessed/qa-report.md` after the evaluator completes.

**If overall grade is SHIP:**
- Proceed to `harnessed:verification-gate`
- Present a brief summary to the user

**If overall grade is ITERATE:**
- Read the specific failures and fix them
- After fixing, re-invoke this skill (go back to Step 1)
- Read the iteration count from `.harnessed/qa-state.md`. Maximum 3 iterations.
- On iteration 3 with no SHIP: escalate to user with full QA history

**If overall grade is BLOCKED:**
- Do NOT attempt to fix
- Present the full QA report to the user
- Explain what the evaluator found and why it's blocking
- Wait for user direction

### Step 5b: Record Failure Patterns

After a QA result of ITERATE or BLOCKED, update `.harnessed/failure-patterns.md` to help future contract-writing catch recurring issues:

1. Read `.harnessed/failure-patterns.md` if it exists (create it if not)
2. For each FAIL or PARTIAL criterion in the QA report, extract a short failure category (e.g., "missing error handling", "off-by-one", "null/undefined not checked", "missing input validation", "regression in existing behavior")
3. If the category already exists in the file, increment its count and update the last-seen date
4. If the category is new, add a row with count 1

The file uses a markdown table: `| Category | Count | Last Seen | Example |` — one row per failure pattern. Include a concrete example from the current QA report for new entries.

**Decay rule:** When reading the file, remove any row whose Last Seen date is more than 90 days ago AND whose Count is 1 (one-off failures that never recurred are noise, not patterns). Rows with Count ≥ 2 are kept regardless of age.

Skip this step on SHIP results. This file is project-level learning and is NOT archived when a new task begins.

### Step 6: Write QA Summary

After a SHIP result, append a brief log entry:

```
## QA Summary
- Tier: {1 or 2}
- Iterations: {count}
- Final grade: SHIP
- Key findings fixed: {brief list of issues caught and fixed during iterations, if any}
```

## Iteration Rules

```
Round 1: Code → QA → ITERATE? → Fix
Round 2: Fix → QA → ITERATE? → Fix
Round 3: Fix → QA → ITERATE? → ESCALATE to user
```

- Each QA round is a FRESH subagent (no accumulated context from previous rounds)
- Each round gets the LATEST diff (including fixes from previous rounds)
- The evaluator does NOT know about previous rounds — it judges the current state independently
- Never lower the bar between iterations. If criteria were fair in round 1, they are fair in round 3.
- **Iteration state persistence:** Before each evaluator dispatch, write the current iteration count and dispatch timestamp to `.harnessed/qa-state.md`:
  ```
  iteration: {N}
  dispatched_at: {ISO 8601 timestamp}
  head_commit: {git rev-parse HEAD}
  ```
  This file is NOT touched by the evaluator (which only writes `qa-report.md`), so it survives across QA rounds and context compaction. After compaction, read this file to recover the iteration count.

## Anti-Rationalization

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "I can include helpful context for the evaluator" | "Helpful context" biases the evaluator toward your assumptions. Independence requires ignorance of your intent. | Include ONLY what's specified in Step 3. Nothing else. |
| "The evaluator is wrong about this finding" | Maybe. But your default assumption should be that the evaluator is right and you are biased. | Fix the issue. If you truly believe the evaluator is wrong, present both views to the user. |
| "Let me just re-run QA, maybe it'll pass this time" | Re-running without fixes is hoping for randomness. The evaluator will find the same issues. | Fix the issues first, then re-run. |
| "I already ran QA on similar code before" | Previous QA verified previous code. Every diff is evaluated independently against the current contract. | Dispatch a fresh evaluator. Prior QA results do not transfer. |
| "I know the code works, I just need QA to confirm" | If you expect confirmation, you are not seeking independent evaluation — you are seeking validation. That mindset causes you to dismiss legitimate findings. | Dispatch the evaluator expecting to learn something. |
| "The user seems impatient, I should skip QA" | User impatience is about communication, not quality. A user who waits 60 extra seconds for verified code is happier than one who gets broken code instantly. | Run QA. Send a status update: "Running independent QA evaluation." |
| "This is my second attempt, I already know what was wrong" | Knowing the previous failure does not guarantee the fix is correct or regression-free. The fresh evaluator exists because your confidence is not evidence. | Dispatch a fresh evaluator with the full latest diff. Do not scope down the evaluation. |

<HARD-GATE>
INDEPENDENT QA IS MANDATORY FOR ALL STANDARD AND LARGE TASKS.

The evaluator subagent must NEVER see your reasoning or self-assessment. Context isolation is non-negotiable.

If you catch yourself adding "helpful context" to the evaluator prompt, STOP. You are compromising the independence that makes this evaluation valuable.
</HARD-GATE>

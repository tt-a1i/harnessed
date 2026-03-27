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
- **Complementary mode (Superpowers):** Read the spec from `docs/superpowers/specs/` (use the most recent spec file relevant to the current task). Extract discrete, verifiable criteria from the spec. If the spec is narrative without explicit criteria, synthesize one criterion per stated requirement. Present extracted criteria in the same format as a Harnessed contract for the `{CONTRACT}` placeholder. If the spec contains no identifiable requirements, invoke `harnessed:contract-writing` to create a contract.

If no contract/spec exists: STOP. Invoke `harnessed:contract-writing` first. Do NOT run QA without criteria.

### Step 2: Detect Verification Tier

Check the project for available verification infrastructure:

**Tier 2 indicators (execution verification):**
- `package.json` with `"test"` script → can run `npm test`
- `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, or `tests/` directory with `test_*.py` → can run `pytest`
- `Makefile` with `test` target → can run `make test`
- `go.mod` present → can run `go test ./...`
- Dev server running (check common ports: 3000, 5173, 8000, 8080). Use `lsof -i -P 2>/dev/null | grep -E ':(3000|5173|8000|8080).*LISTEN'` to detect running servers.
- `playwright.config.*` or `cypress.config.*` → can run e2e tests

**If ANY Tier 2 indicator is found:** use Tier 2 (code review + execution)
**If none found:** use Tier 1 (code review only)

Record which tier is active — include it in the evaluator prompt.

### Step 2b: Pre-Flight Checks (Tier 2 only)

Before dispatching the expensive evaluator subagent, run available tool checks at zero LLM cost:

- If type checker available (e.g., `tsc --noEmit`, `mypy`): run it
- If linter available (e.g., `eslint`, `ruff`): run it
- If test suite available: run it

If any pre-flight check fails, fix the issues first. Do NOT dispatch the evaluator until pre-flight checks pass. This prevents wasting an evaluator round on errors that tools catch for free.

### Step 3: Gather Context for Evaluator

Collect the following — this is ALL the evaluator will see:

| Include | Why |
|---------|-----|
| The contract/spec content | Criteria to evaluate against |
| `git diff` of changes (staged + unstaged) | The actual code to review |
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

**If `git diff` produces no output:** STOP. Do not dispatch the evaluator. Inform the user that there are no code changes to evaluate. If changes were already committed, suggest using `git diff HEAD~1` to diff against the previous commit.

**If the project is not a git repository:** Collect changes by listing all files created or modified during this session. Provide full file contents to the evaluator in place of the diff, with a note: "No git repository. Full file contents provided." The evaluator should review these against the contract criteria.

**Context budget:** If the combined evaluator prompt exceeds ~80,000 tokens, reduce the diff by excluding lock files, auto-generated files, and test file changes (note exclusions to the evaluator). If still too large, include only hunks relevant to contract criteria rather than full file diffs.

### Step 4: Dispatch Evaluator Subagent

Use the **Agent tool** to spawn the evaluator subagent with the description **"Independent QA evaluation"**.

**Construct the prompt:**

1. Read `skills/independent-qa/evaluator-prompt.md` to get the prompt template
2. Read `skills/independent-qa/grading-rubric.md` to get the grading rubric content
3. Replace all placeholders with collected context:
   - `{CONTRACT}` — the full contract/spec content
   - `{DIFF}` — the git diff
   - `{STACK}` — project stack description
   - `{TIER}` — 1 or 2
   - `{VERIFICATION_COMMANDS}` — commands from contract
   - `{GRADING_RUBRIC}` — content from `grading-rubric.md`
4. Paste the FULL content of each placeholder. Never summarize, truncate, or paraphrase. The evaluator sees ONLY what you provide — omitted content is invisible content.

**Subagent configuration:**
- Tool: Agent tool
- Description: "Independent QA evaluation"
- Permissions: the subagent needs read, write, and execute permissions (required for Tier 2 execution verification and writing qa-report.md)
- The evaluator writes its report to `.harnessed/qa-report.md`

**Escalation protocol:** If the evaluator encounters a criterion it cannot assess (e.g., requires manual browser testing, visual design judgment, or UX feel that cannot be verified programmatically), it must mark that criterion as `MANUAL_REVIEW_NEEDED` rather than guessing. The evaluator should never fabricate a PASS or FAIL for something it cannot actually verify.

### Step 4b: Verify Evaluator Output

After the evaluator subagent returns, verify that `.harnessed/qa-report.md`:
- Exists (file is present)
- Contains the expected `# QA Report` header
- Was written during this evaluation (not stale from a previous run)

If the report is missing, empty, or malformed: retry the evaluation once with the same inputs. If the second attempt also fails, treat as BLOCKED with reason "QA evaluator failed to produce a valid report" and escalate to the user. Do NOT proceed without a valid QA report.

### Step 5: Process QA Results

Read `.harnessed/qa-report.md` after the evaluator completes.

**If overall grade is SHIP:**
- Proceed to `harnessed:verification-gate`
- Present a brief summary to the user

**If overall grade is ITERATE:**
- Read the specific failures and fix them
- After fixing, re-invoke this skill (go back to Step 1)
- Track iteration count. Maximum 3 iterations.
- On iteration 3 with no SHIP: escalate to user with full QA history

**If overall grade is BLOCKED:**
- Do NOT attempt to fix
- Present the full QA report to the user
- Explain what the evaluator found and why it's blocking
- Wait for user direction

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
- Track the iteration count by appending a `## Iteration: {N}` header to `.harnessed/qa-report.md` before each QA dispatch. This persists the count across context compaction.

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

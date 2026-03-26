---
name: independent-qa
description: Use after completing a round of code generation. Dispatches an isolated evaluator subagent to independently verify code against acceptance criteria. The evaluator has no access to the generator's reasoning.
---

# Independent QA

Dispatch an isolated evaluator subagent to verify your code. The evaluator operates in a clean context with NO access to your reasoning, assumptions, or self-assessment. It grades your work against the contract.

**This is the core of Harnessed.** Self-evaluation has a 31% disagreement rate with independent evaluation. You cannot objectively judge your own work.

## When This Skill Activates

- After completing a round of code changes (new code, bug fix, refactor)
- After fixing issues from a previous QA round (re-evaluation)
- NOT for micro tasks (single-line, config-only, comment-only changes)

## Execution Flow

### Step 1: Locate the Contract

Determine the acceptance criteria source:

- **Standalone mode:** Read `.harnessed/contract.md`
- **Complementary mode (Superpowers):** Read the spec from `docs/superpowers/specs/` (use the most recent spec file relevant to the current task)

If no contract/spec exists: STOP. Invoke `harnessed:contract-writing` first. Do NOT run QA without criteria.

### Step 2: Detect Verification Tier

Check the project for available verification infrastructure:

**Tier 2 indicators (execution verification):**
- `package.json` with `"test"` script → can run `npm test`
- `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, or `tests/` directory with `test_*.py` → can run `pytest`
- `Makefile` with `test` target → can run `make test`
- `go.mod` present → can run `go test ./...`
- Dev server running (check common ports: 3000, 5173, 8000, 8080)
- `playwright.config.*` or `cypress.config.*` → can run e2e tests

**If ANY Tier 2 indicator is found:** use Tier 2 (code review + execution)
**If none found:** use Tier 1 (code review only)

Record which tier is active — include it in the evaluator prompt.

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

### Step 4: Dispatch Evaluator Subagent

Use the **Agent tool** (subagent) to dispatch the evaluator. Construct the prompt by reading `skills/independent-qa/evaluator-prompt.md` and filling in:

- `{CONTRACT}` — the full contract/spec content
- `{DIFF}` — the git diff
- `{STACK}` — project stack description
- `{TIER}` — 1 or 2
- `{VERIFICATION_COMMANDS}` — commands from contract
- `{GRADING_RUBRIC}` — content from `skills/independent-qa/grading-rubric.md`

**Subagent configuration:**
- Use the Agent tool to spawn the evaluator
- The evaluator must be able to read files and run commands (for Tier 2)
- The evaluator writes its report to `.harnessed/qa-report.md`

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

## Anti-Rationalization

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "I already know the code works" | You wrote it. Your knowledge is not evidence. Self-eval disagrees with independent eval 31% of the time. | Dispatch the evaluator. If it works, QA confirms quickly. |
| "QA just slows down the iteration" | Shipping broken code slows down the user infinitely more. 42% of AI code fails initial testing. | QA is not overhead. QA is the product. |
| "The diff is tiny, QA is overkill" | Tiny diffs cause outages. A 1-line off-by-one error can corrupt data. | If it touches logic, it gets QA. |
| "I can include helpful context for the evaluator" | "Helpful context" biases the evaluator toward your assumptions. Independence requires ignorance of your intent. | Include ONLY what's specified in Step 3. Nothing else. |
| "The evaluator is wrong about this finding" | Maybe. But your default assumption should be that the evaluator is right and you are biased. | Fix the issue. If you truly believe the evaluator is wrong, present both views to the user. |
| "Let me just re-run QA, maybe it'll pass this time" | Re-running without fixes is hoping for randomness. The evaluator will find the same issues. | Fix the issues first, then re-run. |

<HARD-GATE>
INDEPENDENT QA IS MANDATORY FOR ALL STANDARD AND LARGE TASKS.

The evaluator subagent must NEVER see your reasoning or self-assessment. Context isolation is non-negotiable.

If you catch yourself adding "helpful context" to the evaluator prompt, STOP. You are compromising the independence that makes this evaluation valuable.
</HARD-GATE>

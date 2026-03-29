---
name: independent-qa
description: Use after completing a round of code generation.
user-invocable: true
---

# Independent QA

Dispatch isolated reviewer subagents to verify your code. Harnessed uses independent QA to lower self-evaluation bias and improve issue-finding rate. Self-critique is useful for improving a draft, but it does not replace the independent QA loop.

## When This Skill Activates

- After completing a round of code changes (new code, bug fix, refactor)
- After fixing issues from a previous QA round (re-evaluation)
- NOT for micro tasks (single-line, config-only, comment-only changes)

## Execution Flow

### Step 1: Locate the Contract

Determine the acceptance criteria source:

- **Standalone mode:** Read `.harnessed/contract.md`
- **Complementary mode (Superpowers):** Read the spec from `docs/superpowers/specs/`, normalize it into `.harnessed/contract.md`, and use that as the shared criteria source

If no contract/spec exists: STOP. Invoke `harnessed:contract-writing` first.

### Step 2: Detect Verification Tier

Check the project for available verification infrastructure.

**Tier 2** — test suite indicators present (`package.json` test script, `pytest`, `go test`, Playwright/Cypress, or equivalent)
**Tier 1.5** — no test suite, but a dev server is running
**Tier 1** — code review only

Record the active tier.

### Step 2b: Pre-Flight Checks

Before dispatching reviewers, run available zero-LLM checks:
- type checker
- linter
- test suite

If these fail, fix them first.

### Step 2c: Git State Checks

Before gathering context:
- stop on active merge conflict (`.git/MERGE_HEAD`)
- use `git diff HEAD` to capture staged + unstaged changes
- include untracked files by appending their contents to the diff context

Extract the changed file paths from this diff. Use them to drive any scope-based policy selection.

### Step 2d: Risk Classification and Review Mode

Classify the task as **standard** or **high-risk**.

A task is **high-risk** if it touches auth, authz, secrets, crypto, payments, privacy, destructive data operations, infra/prod config, new public endpoints, or if the user explicitly says it is security-sensitive or release-blocking.

Choose one review mode:
- **standard-review** — one primary evaluator
- **corroborated-review** — primary evaluator + second independent evaluator for high-risk tasks
- **security-review** — primary evaluator + dedicated security reviewer for security-sensitive tasks
- **tie-break-review** — dispatched only when prior reviewers disagree materially

**Material disagreement** means any of the following:
- different overall grades
- one reviewer says PASS and another says FAIL/PARTIAL for the same criterion
- one reviewer says SHIP while another requires human review for a high-risk boundary

### Step 2e: Calibration and Drift Governance

Read `docs/evaluator-calibration.md` before dispatching reviewers.

This step exists to make evaluator **drift** explicit rather than silently trusted.

Set `Calibration Status` to:
- **current** — calibration guidance exists and matches the current evaluator configuration
- **stale** — evaluator prompt, model, or high-risk workflow changed since the last calibration review
- **missing** — no calibration guidance exists

For high-risk tasks, `stale` or `missing` calibration means the best possible fully automated outcome is **SHIP_WITH_HUMAN_REVIEW**, not plain SHIP.

### Step 2f: Select Relevant Policy Summaries

If `.harnessed/policies/` exists, select only the policy files relevant to the current diff scope.

Use simple path and keyword matching rather than semantic inference:

- auth-related paths or keywords -> `auth.md`
- service/API changes -> `response.md` + `db.md` + `validation.md`
- test changes -> `testing.md`
- security-sensitive paths or keywords -> `security.md`

Read only the matched files. Keep the token budget bounded: inject at most the small set of matching policy summaries, not the full policy directory. If no policy matches, skip policy injection entirely and keep the existing behavior.

### Step 3: Gather Context for Reviewers

Collect the following — this is ALL the reviewers see:

| Include | Why |
|---------|-----|
| The contract/spec content | Criteria to evaluate against |
| `git diff HEAD` output | The actual code to review |
| Project stack info | Context for evaluation |
| Verification tier | What the reviewer can do |
| Available verification commands | How to verify |
| Risk level | Whether corroboration is required |
| Review mode | Which reviewer path is active |
| Calibration status | Whether clean automation can be trusted fully |
| `{RELEVANT_POLICIES}` | Repo-specific constraints selected from `.harnessed/policies/` |

**DO NOT include:**
- your reasoning or thought process
- your self-assessment of the code
- your conversation history with the user
- planning notes

The reviewer must judge the code, not your intent.

### Step 4: Dispatch the Review Set

Construct reviewer prompts from the prompt files in `skills/independent-qa/`:
- primary evaluator → `evaluator-prompt.md`, writes `.harnessed/qa-report.md`
- second evaluator for corroborated-review → same prompt, writes `.harnessed/qa-report-secondary.md`
- security reviewer for security-review → `security-reviewer-prompt.md`, writes `.harnessed/qa-report-security.md`
- tie-break reviewer → `tie-break-reviewer-prompt.md`, writes `.harnessed/qa-report-tiebreak.md`

When using `evaluator-prompt.md`, replace:
- `{CONTRACT}`
- `{DIFF}`
- `{STACK}`
- `{TIER}`
- `{MODE}`
- `{RISK_LEVEL}`
- `{CALIBRATION_STATUS}`
- `{VERIFICATION_COMMANDS}`
- `{RELEVANT_POLICIES}`
- `{GRADING_RUBRIC}`

### Step 4b: Static Analysis for Security-Sensitive Tasks

If the task is security-sensitive, run available tooling before final synthesis:
- Semgrep
- CodeQL
- bandit

Treat tool findings as strong evidence. Treat tool absence as uncertainty, not as proof that the code is secure.

### Step 4c: Verify Reviewer Output

After reviewers return, verify that each expected report:
- exists
- contains `# QA Report`
- is newer than `dispatched_at` in `.harnessed/qa-state.md`

If a required report is missing or malformed, retry once. If it still fails, treat as BLOCKED.

### Step 5: Synthesize Results

Use the most conservative defensible outcome.

- If reviewers materially disagree, dispatch the tie-break reviewer
- If the tie-break reviewer still cannot resolve the issue, escalate to the user
- If any automatable criterion has weak evidence, downgrade it to PARTIAL or MANUAL_REVIEW_NEEDED rather than PASS
- If the task is high-risk and calibration is stale/missing, the best possible result is SHIP_WITH_HUMAN_REVIEW
- If the task is security-sensitive and security review remains heuristic or tooling is absent, force explicit human review even when all automatable checks pass

### Step 6: Process Final Grade

**If final grade is SHIP or SHIP_WITH_HUMAN_REVIEW:**
- proceed to `harnessed:verification-gate`
- note any pending human review items

**If final grade is ITERATE:**
- fix the issues
- re-run QA
- maximum 3 iterations

**If final grade is BLOCKED:**
- do not attempt speculative fixes
- present the blocking reason to the user

### Step 7: Record Failure Patterns

After ITERATE or BLOCKED, update `.harnessed/failure-patterns.md` from the evaluator's `## Failure Categories` table.

Apply the decay and cap rules already defined by Harnessed.

### Step 8: Write QA Summary

After a SHIP or SHIP_WITH_HUMAN_REVIEW result, append:

```
## QA Summary
- Tier: {1, 1.5, or 2}
- Risk level: {standard or high-risk}
- Review mode: {standard-review / corroborated-review / security-review / tie-break-review}
- Calibration status: {current / stale / missing}
- Confidence: {High / Medium / Low}
- Uncertainty: {brief list or None}
- Iterations: {count}
- Final grade: {SHIP or SHIP_WITH_HUMAN_REVIEW}
- Key findings fixed: {brief list of issues caught and fixed during iterations, if any}
```

## Iteration Rules

- Each QA round uses FRESH reviewer context
- Each round uses the latest diff
- Never lower the bar between iterations
- `qa-state.md` must track:
  - `iteration`
  - `dispatched_at`
  - `head_commit`
  - `contract_hash`
  - `risk_level`
  - `review_mode`
  - `calibration_status`

## Anti-Rationalization

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "I can include helpful context for the evaluator" | Helpful context biases the reviewer toward your assumptions. | Include only the approved context bundle. |
| "My self-review already found the issue" | Great — fix it. But self-review is still not independent evidence. | Use self-review to improve the draft, then run independent QA. |
| "The evaluator is wrong about this finding" | Maybe, but your bias is exactly why the reviewer exists. | Gather stronger evidence or use the tie-break path. |
| "High-risk mode is too expensive" | High-risk tasks are where unchecked bias is most costly. | Use corroboration and explicit human review. |
| "No tool found anything, so security is proven" | Tool silence is not proof of safety. | Record uncertainty and require human review where appropriate. |
| "The reviewer can infer repo policy from the codebase" | That makes coherence checking depend on model guesswork. | Inject only the relevant policy summaries selected from the diff scope. |

<HARD-GATE>
INDEPENDENT QA IS MANDATORY FOR ALL STANDARD AND LARGE TASKS.

Self-critique can improve a draft. It cannot replace independent verification.

High-risk disagreement must be resolved or escalated — never silently ignored.
</HARD-GATE>

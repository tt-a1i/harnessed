---
name: verification-gate
description: Use before declaring any coding task complete, done, or finished.
user-invocable: true
---

# Verification Gate

Before you say "done", PROVE it.

This is the final checkpoint. You must provide concrete, structured evidence for every acceptance criterion that can be verified automatically. Criteria marked MANUAL_REVIEW_NEEDED are listed for human follow-up, not skipped silently. Self-review notes may appear as background context, but they are not evidence.

<HARD-GATE>
NO COMPLETION CLAIMS WITHOUT EVIDENCE FOR EVERY AUTOMATABLE CRITERION. Criteria requiring human judgment must be explicitly listed as pending review — never silently omitted.
</HARD-GATE>

## When This Skill Activates

- After independent-qa returns SHIP or SHIP_WITH_HUMAN_REVIEW
- Before any completion signal to the user
- For micro tasks: this is the only Harnessed gate

## Process

### Step 0: Staleness and Governance Check

Before collecting evidence:
1. Read `.harnessed/qa-state.md` if it exists
2. Re-run QA if `head_commit` or `contract_hash` no longer match
3. Read the QA report overview and note:
   - Review Mode
   - Risk Level
   - Calibration Status
   - Confidence
   - Uncertainty
4. If confidence is low on a high-risk task, or calibration is stale/missing, the best possible outcome is `VERIFIED_PENDING_HUMAN_REVIEW`
5. If the QA path required corroboration, verify the corroborating report exists
6. If disagreement required a tie-break, verify the tie-break report exists

### Step 1: Locate Criteria Source

- **Standalone mode:** Read `.harnessed/contract.md`
- **Complementary mode:** Read `.harnessed/contract.md`
- **Micro task:** infer explicit criteria from the user's request

### Step 2: Collect Evidence Per Criterion

For each criterion, provide one primary evidence type:

| Evidence Type | Format | When to Use |
|--------------|--------|-------------|
| **Code citation** | `file.ext:42` — "{code snippet}" | Implementation exists at this location |
| **Test citation** | `test_file.ext:15` — test name: "{name}" | A test covers this criterion |
| **Command output** | `$ command` → `{output}` | Running a command proves behavior |
| **HTTP smoke test** | `$ curl ...` → `{status + body}` | Tier 1.5 behavior check |
| **Static analysis** | `semgrep` / `CodeQL` / `bandit` output | Security-sensitive evidence |

Supplementary context (cannot be used as evidence by itself):

| Context Type | Use |
|-------------|-----|
| **QA confirmation** | Supports, but never replaces, primary evidence |
| **Self-review** | Background only; useful for audit history, not proof |

Rules:
- evidence must be current
- if you cannot produce evidence for an automatable criterion, the task is not complete
- self-review can be cited only in a `Background` section, never in `Evidence`

### Step 3: Check for Gaps

Verify:
- every automatable criterion has primary evidence
- QA ended in SHIP or SHIP_WITH_HUMAN_REVIEW
- no unresolved ITERATE/BLOCKED findings remain
- high-risk tasks have corroborating review coverage
- tie-break reports exist when disagreement occurred
- low confidence, stale calibration, heuristic security review, or missing security tools are carried into pending human review rather than silently ignored

### Step 4: Write Verification Summary

Write `.harnessed/verification-summary.md`:

```markdown
# Verification Summary

## Task
{task description}

## Status: VERIFIED | VERIFIED_PENDING_HUMAN_REVIEW

## Review Governance
- Risk level: {standard or high-risk}
- Review mode: {mode}
- Calibration status: {current / stale / missing}
- Confidence: {High / Medium / Low}
- Uncertainty: {summary or None}

## Evidence

### Criterion: "{criterion text}"
- **Evidence:** {type}: {citation}
- **Verified:** Yes

## Pending Human Review
{manual-review criteria, low-confidence boundaries, security-sensitive follow-ups}

## Background
- Self-review notes: {optional, informational only}
- QA confirmation: {optional, informational only}

## QA History
- Rounds: {number of QA iterations}
- Final grade: {SHIP or SHIP_WITH_HUMAN_REVIEW}
- Issues fixed during QA: {brief list or None}

## Files Changed
{list of modified files}
```

### Step 5: Present to User

For fully verified work:
- say the task is complete
- mention criteria count and QA rounds
- point to `.harnessed/verification-summary.md`

For pending human review:
- say the task is code-complete or verified pending human review
- state exactly what still needs human review
- never imply the remaining checks were automated

## Micro Task Verification

For micro tasks:
1. state what changed and why
2. cite the file:line
3. confirm no obvious regression
4. present a one-line summary

## Anti-Rationalization

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "The QA already passed, this gate is redundant" | QA checks correctness; the gate checks evidence completeness and human-review carry-through. | Complete the gate. |
| "My self-review proves the behavior" | Self-review is biased background, not proof. | Use self-review as context only. |
| "The reviewer confidence was low, but I'll still call it fully done" | Low confidence is a governance signal. Ignoring it defeats the point of the gate. | Downgrade to pending human review. |
| "No security tool complained, so we're safe" | Tool silence is not proof of safety. | Record the limitation and keep human review where needed. |

## What Verification Gate Catches That QA Doesn't

QA asks: "Does the implementation appear correct?"
Verification Gate asks: "Can we prove every automatable requirement, and did we preserve uncertainty honestly?"

The combination of independent QA + verification gate creates a double-lock:
- QA lowers self-evaluation bias and increases issue-finding rate
- Gate ensures every requirement and every uncertainty is surfaced explicitly

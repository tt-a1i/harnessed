---
name: verification-gate
description: Use before declaring any coding task complete, done, or finished.
user-invocable: true
---

# Verification Gate

Before you say "done", PROVE it.

This is the final checkpoint. You must provide concrete, structured evidence that every acceptance criterion is satisfied. Prose assertions ("I implemented it correctly") are worthless. Evidence means: file paths, line numbers, test names, and command outputs.

<HARD-GATE>
NO COMPLETION CLAIMS WITHOUT EVIDENCE FOR EVERY CRITERION.

You may NOT use the words "done", "complete", "finished", "implemented", or any completion signal until you have passed through this gate. This is absolute.
</HARD-GATE>

## When This Skill Activates

- After independent-qa returns SHIP
- Before responding with ANY completion signal to the user
- For micro tasks: this is the ONLY Harnessed gate (no contract or QA needed)

## Process

### Step 1: Locate Criteria Source

- **Standalone mode:** Read `.harnessed/contract.md`
- **Complementary mode (Superpowers):** Read the Superpowers spec from `docs/superpowers/specs/`
- **Micro task (no contract):** Infer criteria from the user's original request. List them explicitly before verifying.

### Step 2: Collect Evidence Per Criterion

For EACH criterion, provide ONE of the following evidence types:

| Evidence Type | Format | When to Use |
|--------------|--------|-------------|
| **Code citation** | `file.ext:42` — "{code snippet}" | Implementation exists at this location |
| **Test citation** | `test_file.ext:15` — test name: "{name}" | A test covers this criterion |
| **Command output** | `$ command` → `{output}` | Running a command proves it works |
| **QA confirmation** | "QA Report: criterion PASS with evidence at file:line" | QA already verified this |

**Rules for evidence:**
- Each citation must be CURRENT — verify the file and line STILL contain what you claim
- Do not cite lines you have not read in this session
- If you cannot produce evidence for a criterion, the task is NOT complete
- "I wrote it so it works" is NOT evidence

### Step 3: Check for Gaps

After collecting evidence for all criteria, verify:

- [ ] Every criterion has at least one evidence item
- [ ] No criterion is marked with "will be done later" or "TODO"
- [ ] QA report (if exists) shows SHIP status
- [ ] No unresolved ITERATE or BLOCKED findings remain

If ANY gap exists: the task is NOT complete. Fix the gap before proceeding.

### Step 4: Write Verification Summary

Write to `.harnessed/verification-summary.md`:

```markdown
# Verification Summary

## Task
{task description}

## Status: VERIFIED

## Evidence

### Criterion: "{criterion text}"
- **Evidence:** {type}: {citation}
- **Verified:** Yes

{Repeat for each criterion}

## QA History
- Rounds: {number of QA iterations}
- Final grade: SHIP
- Issues fixed during QA: {brief list, or "None"}

## Files Changed
{list of files modified, added, or deleted}
```

### Step 5: Present to User

After writing the summary, present a brief completion message to the user:

```
Task complete. {one-line summary of what was built/fixed}.

Verified against {N} acceptance criteria. QA passed in {M} round(s).
{If issues were caught and fixed: "QA caught {X} issues that were fixed before completion."}

Full verification: .harnessed/verification-summary.md
```

## Micro Task Verification

For micro tasks (no contract, no QA), the gate is lighter:

1. State what was changed and why
2. Cite the specific file:line of the change
3. Confirm no regression (read surrounding code or run tests if available)
4. Present one-line summary to user

No `.harnessed/verification-summary.md` needed for micro tasks.

## Anti-Rationalization

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "It's obviously done, I just wrote it" | Obvious to you. Not obvious to the user. Not proven. Agents routinely claim completion without verification. | Collect evidence. If it's truly done, evidence is trivial to produce. |
| "The QA already passed, this gate is redundant" | QA checks correctness. The gate checks completeness and provides an audit trail. They serve different purposes. | Complete the gate. It takes 60 seconds. |
| "The user is waiting, let me just say done" | The user is waiting for WORKING code, not a false completion signal. One minute of verification saves hours of debugging. | Complete the gate, then respond. |
| "I'll just list the files I changed" | Listing files proves you changed them. It does NOT prove the changes are correct or complete. | Cite specific lines, not just files. |
| "The evidence is implicit in the code" | Implicit evidence is not evidence. If you cannot point to a specific file:line, you have not verified it — you have assumed it. | Produce explicit citations. Every criterion needs a concrete reference. |

## What Verification Gate Catches That QA Doesn't

QA verifies: "Does the code work correctly?"
Verification Gate verifies: "Is every requirement accounted for?"

These are different questions. QA might pass all criteria it can find, but miss that one criterion was never implemented (the code it expected to find simply doesn't exist). The gate forces YOU to produce evidence for EVERY criterion, catching omissions that QA might overlook.

The combination of independent QA + verification gate creates a double-lock:
- QA catches bugs you introduced
- Gate catches requirements you forgot

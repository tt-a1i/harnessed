---
name: using-harnessed
description: Use at the start of every session and before completing any coding task.
---

# Harnessed: Independent Quality Verification

<SUBAGENT-STOP>
This skill is for the main session agent only. Subagents (including QA evaluators) should not load or follow these instructions.
</SUBAGENT-STOP>

Harnessed ensures that code you write is independently verified before being declared complete. Your work is not "done" until an isolated evaluator — separate from you — confirms it works.

## Detect Operating Mode

**Detect Superpowers:** Check if the session context contains references to Superpowers skills (e.g., `superpowers:` prefix in loaded skills), or if a `superpowers` plugin directory exists in the project. If Superpowers was loaded by a SessionStart hook, its instructions will already be in your context — look for mentions of "Superpowers" in your system instructions.

- **Superpowers detected → Complementary Mode** — SKIP `harnessed:contract-writing`; use Superpowers specs as acceptance criteria.
- **Superpowers not detected → Standalone Mode** — USE `harnessed:contract-writing` before any coding task.
- **Superpowers detected but no specs available** → Fall back to Standalone Mode. This can happen if Superpowers is installed but the SessionStart hook failed or no planning specs exist yet. If the `superpowers` directory exists but `docs/superpowers/specs/` is empty or missing, treat as Standalone.

Both modes USE `harnessed:independent-qa` after each coding round and `harnessed:verification-gate` before completion.

## User Communication

Briefly inform the user at these moments:
- **Before contract:** "I'll draft acceptance criteria before coding."
- **Before QA:** "Running independent QA evaluation."
- **During ITERATE:** "QA found {N} issues — fixing them now."
- **At completion:** Use the verification-gate's presentation format.

Keep status messages to one sentence. Do not explain the Harnessed pipeline unless the user asks.

## Task Size Routing

| Task Size | Indicators | Pipeline |
|-----------|-----------|----------|
| **Micro** | Single-line fix, typo, config value change, comment edit | Skip contract + QA. Use verification-gate only. |
| **Standard** | New function, bug fix, UI component, API endpoint, single-function refactor | Full pipeline: contract → code → QA → gate |
| **Large** | New feature, multi-file refactor (>3 files or public interface changes), architecture change | Full pipeline with explicit user review at contract stage |

**When in doubt, treat as Standard.** It is always safer to over-verify than under-verify.

## Gitignore Setup

Before creating any `.harnessed/` artifacts, check if `.harnessed/` is already in the project's `.gitignore`. Only append if absent:

```
grep -qxF '.harnessed/' .gitignore 2>/dev/null || echo '.harnessed/' >> .gitignore
```

This is automatic, silent, and idempotent — running multiple times will not create duplicate entries. Do not ask the user for permission. QA artifacts should never be committed.

## Concurrent Session Detection

Before writing any artifacts, check for an active session lock:

1. If `.harnessed/.lock` exists, read its content (PID and timestamp)
2. Check if the PID is still running: `kill -0 {PID} 2>/dev/null`
3. If the process is alive: warn the user — "Another Harnessed session appears active (PID {PID}, started {timestamp}). Running concurrent sessions may corrupt QA artifacts. Continue anyway?" Wait for user confirmation.
4. If the process is dead (stale lock): remove the lock file silently and proceed
5. Write `.harnessed/.lock` with the current shell's PID (`$$`) and ISO 8601 timestamp

The lock file is advisory, not mandatory — it warns but does not block. Clean up the lock file when the task completes (after verification-gate or after the user ends the task).

## Artifact Lifecycle

When a new task begins, archive stale artifacts to prevent them from misleading the QA evaluator:

1. If `.harnessed/contract.md` exists from a previous task, rename it to `.harnessed/archive/{timestamp}-contract.md`
2. If `.harnessed/qa-report.md` exists, rename it to `.harnessed/archive/{timestamp}-qa-report.md`
3. If `.harnessed/qa-state.md` exists, rename it to `.harnessed/archive/{timestamp}-qa-state.md`
4. If `.harnessed/verification-summary.md` exists, rename it to `.harnessed/archive/{timestamp}-verification-summary.md`

Use the format `YYYYMMDD-HHMMSS` for `{timestamp}`. Create `.harnessed/archive/` if it does not exist. Do NOT archive `.harnessed/failure-patterns.md` — it is persistent project-level learning that accumulates across tasks.

**New task vs. continuation:** A new task has a distinct goal unrelated to the current contract. A continuation refines or extends the current goal. When ambiguous, ask the user: "Is this a new task or a continuation of the current one?"

## Anti-Rationalization

Every rationalization below has been observed in production and leads to bugs shipping:

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "This change is too small for QA" | 3-line diffs cause production outages. Size does not predict risk. | If it touches logic, run QA. Use micro routing ONLY for truly inert changes. |
| "The user didn't ask for QA" | The user installed Harnessed. That IS asking for QA. | Run QA. |
| "I'll QA everything at the end" | Compound bugs are exponentially harder to find and fix than incremental ones. | QA after each coding round, not at the end. |
| "The evaluator was too strict last time" | Strictness is the point. If criteria are wrong, fix the criteria. Never weaken the evaluator. | Adjust the contract, not the evaluator's standards. |
| "This project has no tests, so QA can't verify much" | Tier 1 code review alone catches logic errors, off-by-one bugs, missing error handling, and regressions. Independence is the value, not execution. | Run QA at Tier 1. Code review is still more reliable than self-assessment. |

<HARD-GATE>
NON-NEGOTIABLE. "It's fine this one time" is NEVER true. If you think any thought from the table above, STOP and follow the correct procedure.

**User override:** HARD-GATEs prevent agent rationalization, not explicit user instructions. If the user directly requests "skip QA for this task" or "treat this as micro", respect it — the user has authority over their workflow. But never skip on your own initiative.
</HARD-GATE>

## Quick Reference

```
Standalone Mode:
  Task → contract-writing → CODE → independent-qa → (fix loop) → verification-gate → Done

Complementary Mode (with Superpowers):
  Task → [Superpowers planning] → CODE → independent-qa → (fix loop) → verification-gate → Done

Micro Task:
  Task → CODE → verification-gate → Done
```


---
name: contract-writing
description: Use before starting any coding task when Superpowers is not present.
user-invocable: true
---

# Contract Writing

Write a testable contract BEFORE writing any code. The contract defines what "done" means in terms that an independent evaluator can verify without knowing your intent or reasoning.

<HARD-GATE>
NO CODE WITHOUT A CONTRACT FIRST.

If you have already started coding before writing a contract, STOP. Write the contract now. Retroactive contracts are better than no contracts.
</HARD-GATE>

## When This Skill Activates

- **Standalone mode** (Superpowers not detected): at the start of every Standard or Large coding task
- **Complementary mode** (Superpowers detected): SKIP this skill. Superpowers' brainstorming/writing-plans produces the spec. The independent-qa skill will read from `docs/superpowers/specs/` instead.

## Contract Format

Write the contract to `.harnessed/contract.md` using the format defined in `skills/contract-writing/contract-format.md`. The format includes: `# Contract: {title}`, `## Task`, `## Acceptance Criteria` (with Functional/Edge Cases/Regression subsections), `## Verification Commands`, and `## Out of Scope`.

## Rules for Good Criteria

### Each criterion MUST be:

1. **Independently verifiable** — An evaluator who has never seen your code can check it by reading the file or running a command
2. **Observable** — Describes an outcome, not an implementation detail
3. **Atomic** — Tests one thing. "Login works and session persists" is two criteria, not one
4. **Unambiguous** — No room for interpretation. "Fast" is bad. "Responds in <200ms" is good

### Each criterion MUST NOT be:

1. **Subjective** — "Code is clean", "Good UX", "Well-structured" are NOT criteria. Criteria that can only be verified by human judgment (visual design fidelity, UX feel) will be graded MANUAL_REVIEW_NEEDED by the evaluator. Prefer automatable criteria; if subjective ones are necessary, keep them to a minimum.
2. **Implementation-prescriptive** — "Use a HashMap" is not a criterion. "Lookup is O(1)" might be
3. **Untestable** — If you can't describe how to verify it, it's not a criterion
4. **Redundant** — Each criterion adds unique verification value

### Sizing

| Task Size | Criteria Count | Guidance |
|-----------|---------------|----------|
| Standard (bug fix, single feature) | 3–8 | Focus on the fix/feature + regression |
| Large (multi-file, new system) | 8–15 | Include integration points and edge cases |

More than 15 criteria suggests the task should be decomposed into smaller tasks.

**Minimum:** Every contract MUST have at least 1 criterion. If you cannot identify any verifiable criteria, the task is either micro (route accordingly) or requirements are unclear (ask the user before proceeding).

## Verification Commands

For each criterion, try to provide a verification command:

- **Has tests:** `npm test`, `pytest`, `go test ./...`
- **Has dev server:** `curl http://localhost:3000/endpoint`
- **Has UI:** "Navigate to /page and verify {behavior}" (for Playwright/browser verification)
- **File-based:** `grep -n "pattern" file.ext` to confirm implementation exists
- **No automation possible:** Mark as "Manual: {description}" — the evaluator will verify by code reading

If the project has no test infrastructure, the contract should note this under a `## Environment` section so the evaluator knows to use Tier 1 (code review only).

## Process

1. **Read the user's request** carefully. Identify explicit and implicit requirements.
2. **Examine the codebase** — understand existing patterns, test infrastructure, and constraints.
2b. **Check failure patterns** — if `.harnessed/failure-patterns.md` exists, read it. Only note patterns with Count ≥ 2 that are relevant to the current task's domain (e.g., "missing input validation" is relevant for API work but not for CSS refactoring). Ignore patterns unrelated to the task — the goal is targeted prevention, not a checklist of every past mistake.
3. **Draft the contract** — write criteria covering: functional requirements, edge cases, regression safety, and relevant failure patterns from step 2b.
4. **Add verification commands** — map each criterion to how it can be checked.
5. **Define out-of-scope** — explicitly exclude things the user did NOT ask for.
6. **Write to `.harnessed/contract.md`**
6b. **Coverage verification** — re-read the user's original request and extract every distinct requirement (explicit and strongly implied). Map each to at least one contract criterion. If any requirement has no matching criterion, add it now. This step is mandatory, not optional reflection.
7. **Present the contract to the user** — show a brief summary of the criteria. For **Large** tasks, wait for explicit user approval before coding. For **Standard** tasks, present the contract and proceed to coding unless the user objects.

## Requirement Changes

If the user modifies requirements after the contract is written:

1. Update `.harnessed/contract.md` to reflect the new requirements
2. If already coding: assess whether existing code satisfies the updated criteria
3. If QA has already run: the next QA round evaluates against the updated contract
4. If the change fundamentally alters the task: archive the current contract and start fresh

Never run QA against a stale contract.

## Anti-Rationalization

| Your Thought | Why It's Wrong | What To Do |
|-------------|---------------|------------|
| "The task is obvious, no contract needed" | Obvious tasks have implicit assumptions. Contracts make assumptions explicit. The evaluator cannot read your mind. | Write the contract. If it's truly obvious, it takes 30 seconds. |
| "I'll figure out the criteria as I code" | Post-hoc criteria are biased toward what you built, not what should be built. | Write criteria BEFORE coding. Adjust only if requirements change. |
| "The user just wants it done fast" | A broken feature delivered fast wastes more time than a working feature delivered with a 2-minute contract. | Write the contract. Speed without correctness is not speed. |
| "This is a refactor, there are no new requirements" | Refactors have the strictest contract: behavior must be IDENTICAL. List the behaviors that must not change. | Write regression criteria for every observable behavior. |

## Example

For the request "Add a search bar to the user list page":

```markdown
# Contract: Add search bar to user list page

## Task
Add a search input to the /users page that filters the displayed user list in real time.

## Acceptance Criteria

### Functional
- [ ] A text input is visible at the top of the /users page
- [ ] Typing in the input filters the user list to show only users whose name or email contains the query
- [ ] Filtering is case-insensitive
- [ ] Clearing the input restores the full user list
- [ ] Empty state message shown when no users match the query

### Edge Cases
- [ ] Search works correctly when user list is empty
- [ ] Special characters in query do not cause errors

### Regression
- [ ] Existing user list renders correctly without interaction
- [ ] User list pagination (if present) still works

## Verification Commands
- `npm test -- --grep "search"` — verifies search-related tests
- `curl http://localhost:3000/users` — verifies page loads
- Manual: Type "john" in search bar, verify only matching users shown

## Out of Scope
- Server-side search / API changes
- Search history or autocomplete
- URL query parameter sync
```

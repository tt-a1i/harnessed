# Harnessed — Implementation Plan

## Phase 1: Core Plugin Infrastructure

### Task 1.1: plugin.json + hooks
Create the plugin manifest and session-start hook.

**Files:**
- `.claude-plugin/plugin.json` — name, version, description, author, keywords
- `hooks/hooks.json` — register session-start hook
- `hooks/session-start` — shell script that reads `using-harnessed/SKILL.md`, JSON-escapes, outputs as `hookSpecificOutput.additionalContext`

**Acceptance:**
- [ ] `plugin.json` is valid JSON with required fields
- [ ] `hooks.json` registers session-start event
- [ ] `session-start` script reads SKILL.md and outputs valid JSON
- [ ] Script detects Claude Code vs Cursor environment and outputs correct format
- [ ] Script is executable (chmod +x)

### Task 1.2: using-harnessed meta-skill
The always-loaded skill that routes to other skills.

**File:** `skills/using-harnessed/SKILL.md`

**Content must include:**
- YAML frontmatter (name, description following CSO pattern)
- Superpowers detection logic (check for superpowers:using-superpowers)
- Task routing rules: when to invoke each skill
- Anti-rationalization table (at least 6 entries)
- Priority hierarchy
- Standalone vs complementary mode behavior

**Acceptance:**
- [ ] Frontmatter follows agentskills.io pattern
- [ ] Description contains ONLY triggering conditions
- [ ] Superpowers detection instructions are clear and actionable
- [ ] Anti-rationalization table covers the most common evasion patterns
- [ ] Priority hierarchy is explicit

---

## Phase 2: Contract Writing

### Task 2.1: contract-writing skill
Generate testable acceptance criteria.

**File:** `skills/contract-writing/SKILL.md`

**Content must include:**
- When to activate (standalone mode only, skip when Superpowers present)
- Contract format template (task, criteria, verification commands, out of scope)
- Rules for good criteria (verifiable, observable, no subjective)
- Iron Law: NO CODE WITHOUT A CONTRACT FIRST
- Anti-rationalization table
- Output location: `.harnessed/contract.md`

**Acceptance:**
- [ ] Contract format is clear and machine-parseable
- [ ] Each criterion rule is actionable
- [ ] Iron law and anti-rationalization are present
- [ ] Superpowers bypass condition is documented

---

## Phase 3: Independent QA (Core)

### Task 3.1: independent-qa skill
The QA orchestration flow.

**File:** `skills/independent-qa/SKILL.md`

**Content must include:**
- When to activate (after any code generation round)
- Subagent dispatch instructions (use Agent tool)
- What to include in subagent prompt (diff, contract, project context)
- What to EXCLUDE (generator's reasoning, self-assessment)
- Two-tier detection logic (code review vs execution verification)
- Iteration loop rules (max 3, escalation)
- Output format and location: `.harnessed/qa-report.md`
- Anti-rationalization table

**Acceptance:**
- [ ] Subagent dispatch is fully specified
- [ ] Context isolation is explicit (what goes in, what stays out)
- [ ] Tier 1/Tier 2 detection conditions are listed
- [ ] Iteration and escalation logic is clear
- [ ] Grading system (SHIP/ITERATE/BLOCKED) is defined

### Task 3.2: evaluator-prompt.md
The prompt template for the QA evaluator subagent.

**File:** `skills/independent-qa/evaluator-prompt.md`

**Content must include:**
- Role: skeptical senior engineer
- Instructions: attempt to disprove each PASS
- Input format: what data the evaluator receives
- Output format: structured per-criterion report
- Citation requirement: file:line for every finding
- Tier 1 (code review) instructions
- Tier 2 (execution verification) instructions
- Escalation protocol

**Acceptance:**
- [ ] Tone is skeptical, not helpful
- [ ] Output format is structured (not prose)
- [ ] Citation requirement is explicit
- [ ] Both tiers have clear instructions
- [ ] Evaluator cannot see generator's reasoning

### Task 3.3: grading-rubric.md
Scoring dimensions and thresholds.

**File:** `skills/independent-qa/grading-rubric.md`

**Content must include:**
- Per-criterion grading: PASS / FAIL / PARTIAL definitions
- Overall grading: SHIP / ITERATE / BLOCKED definitions
- Threshold rules (e.g., any FAIL on critical criterion = BLOCKED)
- Severity classification (critical, major, minor)
- Examples of each grade

**Acceptance:**
- [ ] Grading definitions are unambiguous
- [ ] Thresholds are concrete numbers/rules
- [ ] Examples cover common scenarios

---

## Phase 4: Verification Gate

### Task 4.1: verification-gate skill
Final checkpoint before completion.

**File:** `skills/verification-gate/SKILL.md`

**Content must include:**
- When to activate (before ANY completion signal)
- Evidence format: file:line citations, test names, command outputs
- Contract/spec source resolution (Harnessed contract vs Superpowers spec)
- Iron Law: NO COMPLETION CLAIMS WITHOUT EVIDENCE
- Anti-rationalization table
- Output: `.harnessed/verification-summary.md`

**Acceptance:**
- [ ] Evidence format is concrete and hard to fabricate
- [ ] Dual-source resolution (contract.md vs superpowers spec) works
- [ ] Iron law and anti-rationalization present
- [ ] Output summarizes evidence per criterion

---

## Phase 5: Polish & Documentation

### Task 5.1: README.md
Project documentation.

**Content:**
- What Harnessed is (one paragraph)
- Installation instructions
- How it works (flow diagram in text)
- Skills overview
- Superpowers compatibility
- Configuration options

### Task 5.2: Integration testing
Manually verify the complete flow:
1. Install plugin in Claude Code
2. Start new session → meta-skill loads
3. Give coding task → contract generated
4. Code written → independent QA dispatched
5. QA report generated → fixes applied
6. Verification gate → evidence collected
7. Task complete with full audit trail

---

## Execution Order

```
1.1 (plugin infra) → 1.2 (meta-skill) → 2.1 (contract) → 3.1-3.3 (QA) → 4.1 (gate) → 5.1-5.2 (polish)
```

Total: 9 tasks across 5 phases.

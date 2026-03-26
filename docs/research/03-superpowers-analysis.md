# Superpowers Plugin Analysis

## Overview

- **Repo:** github.com/obra/superpowers (115,130 stars)
- **Author:** Jesse Vincent (obra), founder of Prime Radiant
- **Version:** 5.0.6
- **License:** MIT
- **Platforms:** Claude Code (native), Cursor, Codex, OpenCode, Gemini CLI

---

## Architecture

### Plugin Loading
- SessionStart hook reads `using-superpowers/SKILL.md`
- Escapes for JSON, injects as `additionalContext`
- Wrapped in `<EXTREMELY_IMPORTANT>` tags
- Only ONE skill at session start; all others on-demand via Skill tool

### Skill Structure
```yaml
---
name: skill-name-with-hyphens
description: Use when [triggering conditions]
---
```
- Description = WHEN to use, never WHAT it does (Claude Search Optimization)
- Max 1024 chars in frontmatter
- Cross-references by name only, never `@` links (burns context)

### Anti-Rationalization Pattern (Core Innovation)

**Level 1: Iron Laws**
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**Level 2: Rationalization Tables**
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |

**Level 3: Red Flag Lists** — Specific thoughts that signal violation incoming

**Level 4: "Spirit vs letter" preemption** — "Violating the letter IS violating the spirit"

**Level 5: Pressure-testing** — New skills tested with time pressure + sunk cost + authority + exhaustion

**Level 6: CSO description trap** — If description summarizes workflow, Claude follows description not skill

### Subagent Dispatch

1. Controller reads plan, extracts all tasks
2. Per task: dispatch **implementer subagent** with full task text (pasted, not referenced)
3. **Spec reviewer subagent** — told "implementer finished suspiciously quickly"
4. **Code quality reviewer subagent**
5. Loop until both pass

Key decisions:
- Fresh subagent per task (no context pollution)
- Controller curates exact context per subagent
- Model tiering: cheap for mechanical, expensive for review
- Two-stage order enforced: spec THEN quality
- Escalation: DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT

### Priority System
1. User instructions (CLAUDE.md) — highest
2. Superpowers skills
3. Default system prompt — lowest

---

## 7-Stage Pipeline

1. **brainstorming** — Socratic design, spec to `docs/superpowers/specs/`, user gate
2. **using-git-worktrees** — Isolated branch
3. **writing-plans** — 2-5 min tasks, complete code, no placeholders
4. **subagent-driven-development** — Fresh agent per task + two-stage review
5. **test-driven-development** — RED-GREEN-REFACTOR
6. **requesting-code-review** — Review against plan
7. **finishing-a-development-branch** — Verify, present 4 options, cleanup

---

## Known Defects (from issue tracker)

### #578: Phantom Completion (Critical)
- Spec reviewer writes plausible prose without reading files
- Proposed fix: require file:line citations
- Also: persistent validator pool accumulating codebase context

### #895: Plans Over-Specify
- Plans contain complete code, executor just copy-pastes
- When implementation reveals better approach, plan's code is wrong
- Community split: intent-level vs verbose for model tiering

### #512: Token Consumption
- Plans typically 1750+ lines
- $50+ per project with Opus just for planning
- Monolithic plan files expensive to re-read

### #750: High Token Usage
- using-superpowers injected into EVERY session whether needed or not

### #551: No Cross-Session Memory
- New sessions repeat work
- No context about what was tried/decided/ruled out

### #429: No Agent Teams Support
- Only knows Task tool, not TeammateTool/SendMessage

---

## Structural Gaps

1. **No evaluation/testing framework** — No automated verification beyond subagent review
2. **No cross-session memory** in core
3. **No metrics** — No token tracking, success rates, quality metrics
4. **No rollback/recovery** — No structured recovery from bad subagent output
5. **No plan validation** — No pre-execution plan consistency check
6. **No incremental execution** — Plans must execute fully
7. **No model-awareness** — Skills don't adapt per model
8. **Rigid TDD** — Excessive for config changes
9. **No security review** in core
10. **No adversarial testing** in core

---

## Notable Fork: REPOZY/superpowers-optimized

Adds:
- 3-tier routing: micro/lightweight/full pipeline
- 9 safety hooks
- OWASP-aligned security review
- Red-team adversarial agent with auto-fix
- Cross-session memory stack
- Self-consistency verification
- Subagent guard hook

---

## Ecosystem

| Repo | Stars | Purpose |
|------|-------|---------|
| superpowers | 115,130 | Core |
| superpowers-marketplace | 734 | Curated plugins |
| superpowers-skills | 578 | Community skills |
| superpowers-lab | 249 | Experimental |
| superpowers-chrome | 224 | Browser control |

Community skills include: systematic-debugging, when-stuck, collision-zone-thinking, remembering-conversations, etc.

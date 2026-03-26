# Harnessed — Positioning & Design Rationale

## Core Positioning

**Superpowers = process discipline (HOW to write code)**
**Harnessed = quality verification (IS the code actually correct)**

These are complementary, not competitive. Users can install both.

---

## Problem Statement

Current single-agent coding tools (Claude Code, Codex, Cursor) suffer from:

1. **Self-evaluation bias** — Agent says "done" but code has bugs (31% disagreement with humans)
2. **No independent verification** — Generator and evaluator share same context and assumptions
3. **Context degradation** — Quality drops after ~35 minutes or 60% context utilization
4. **Phantom completion** — Even Superpowers' two-stage review can produce plausible-sounding pass reports without actually verifying code
5. **No quality metrics** — Users have no visibility into success rates, costs, or iteration counts

---

## Research-Backed Design Decisions

| Decision | Evidence |
|----------|----------|
| Independent evaluator subagent | Agent-as-Judge: 0.3% vs 31% disagreement |
| Spec-based acceptance criteria | Addy Osmani's framework; ALMAS; Anthropic sprint contracts |
| Context resets over compaction | JetBrains: observation masking beats LLM summary |
| Bounded agents with clear roles | OpenObserve: "super agent" failed, bounded agents succeeded |
| Anti-rationalization design | Superpowers: proven to prevent LLM shortcutting |
| 3-tier task routing | REPOZY fork: eliminates overhead for trivial tasks |
| File-based communication | Hightouch: pointers in context, data on disk |
| Execution-based verification | AI code: 42% pass initially → 93% after QA agent |

---

## Target Skills

| Skill | What It Does | Industry Pattern |
|-------|-------------|-----------------|
| **using-harnessed** | Meta-skill: when to invoke which skill | Superpowers meta-skill pattern |
| **contract-writing** | Generate testable acceptance criteria before coding | Sprint contracts + Spec-driven dev |
| **independent-qa** | Dispatch isolated evaluator subagent | Agent-as-Judge + context isolation |
| **context-lifecycle** | Structured handoff at 70% utilization | JetBrains observation masking + anchored summary |
| **verification-gate** | Execute (not just review) before declaring done | OpenObserve Sentinel pattern |
| **adaptive-routing** | Route micro/light/full based on task size | REPOZY 3-tier routing |

---

## Compatibility

- Works standalone
- Works alongside Superpowers (complementary, not conflicting)
- Claude Code plugin format (.claude-plugin/)
- Potential: Cursor, Codex, OpenCode support via platform detection

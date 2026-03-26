# Evaluation & QA Patterns for AI Coding Agents

## 1. LLM-as-Judge / Agent-as-Judge

### Core Concept
Use a separate LLM to evaluate outputs from the coding agent. Assessing code is easier than generating it.

### Approaches
- **Pairwise Comparison**: 80%+ agreement with human preferences
- **Reference-Free by Criteria**: Score on dimensions (correctness, style, security)
- **Reference-Based**: Compare against golden references
- **Agent-as-Judge**: Evaluates entire trajectory, not just output; uses tools to verify
  - On DevAI benchmark: **0.3% disagreement** with human majority vote
  - Single LLM judge: **31% disagreement**

### Bias Mitigation
- **Position Bias**: Randomize response positions
- **Verbosity Bias**: Use clear quality criteria
- **Self-Enhancement Bias**: Use a DIFFERENT model as evaluator
- Multiple evaluations + voting + alternate ordering

### Implementation Best Practices
- Binary classification (correct/incorrect) is most reliable
- Temperature near 0 for consistency
- Structured JSON outputs
- More capable model as evaluator when possible

---

## 2. Automated QA Architectures

### The Problem — Quantified
- AI-generated code passes only **42%** of tests initially → **93%** after QA agent
- AI PRs contain **1.7x more issues** than human PRs
- **1.4x more critical bugs**
- **2.74x higher XSS vulnerability rates**

### OpenObserve "Council of Agents" (Production)

| Phase | Agent | Function |
|-------|-------|----------|
| 1 | Analyst | Extracts selectors, maps workflows, identifies edge cases |
| 2 | Architect | Creates prioritized test plans (P0/P1/P2) |
| 3 | Engineer | Generates Playwright test code |
| 4 | **Sentinel** | Audits for violations, anti-patterns, security. **Blocks on critical** |
| 5 | Healer | Runs tests, diagnoses, fixes, iterates up to 5x |
| 6 | Scribe | Documents findings |

**Results:** 380→700+ tests; flaky tests reduced 85%; analysis time 6-10x faster.

**Key insight:** One "super agent" failed. Bounded agents with clear responsibilities work dramatically better.

### Recommended QA Stack
1. Layer 1: Coding agent (Claude Code, Cursor, etc.)
2. Layer 2: CI/CD pipeline (lint, type check, existing tests)
3. Layer 3: **Dedicated AI testing agent** — independent, reasons about user flows, generates executable tests

---

## 3. Self-Evaluation Bias

### The Problem
When coding agent generates both implementation and tests in one session, both share identical assumptions. "Having a student grade their own exam."

### Failure Modes
- Same-agent blind spots (shared misconceptions)
- Limited scope (unit isolation, no cross-service detection)
- Maintenance orphaning (tests go stale)
- Self-refine convergence (loops on suboptimal solutions)

### Solutions
1. **Independent evaluation model** — Different model judges
2. **Multi-agent debate** — Each agent's findings challenged by others
3. **Agent-as-Judge** — Dedicated judge with equivalent capability
4. **Spec-based verification** — Spec as contract, not code itself

---

## 4. Multi-Agent Code Review (Production Systems)

### Anthropic Code Review (Mar 2026)
- Multiple specialized agents in parallel → verify and rank → post comments
- **54% of PRs** receive substantive comments
- **<1% false positive rate**
- **84% of large PRs** (>1000 lines) flagged critical issues
- ~100% engineer agreement

### HubSpot Sidekick
- Judge agent evaluates comments before posting
- **90% reduction** in time-to-first-feedback
- **80% thumbs-up** from developers

### Four-Agent Specialized Pattern

| Agent | Focus |
|-------|-------|
| Security | Auth, validation, dependencies |
| Performance | Complexity, queries, caching |
| Architecture | Patterns, coupling, interface contracts |
| Domain Logic | Business rules, state, consistency |

Cross-validation: agents challenge each other → <1% false positive.

---

## 5. Context Window Management

### Degradation Facts
- All 18 frontier models exhibit degradation before capacity limits
- **30%+ accuracy drop** for middle-position information ("Lost in the Middle")
- **65% of enterprise AI failures** attributed to context drift/memory loss
- Success rate decreases after **35 minutes**; doubling duration **quadruples** failures

### Strategy Comparison

| Strategy | Approach | Result |
|----------|----------|--------|
| Compaction | Summarize at 70% utilization | Standard, works well |
| Observation Masking (JetBrains) | Replace old observations with placeholders | 2.6% higher solve, 52% cheaper than LLM summary |
| Anchored Iterative Summary | Extend summaries incrementally | 4.04 accuracy vs Anthropic 3.74 |
| Sub-agent delegation | 50-200 token summaries | 90.2% improvement over single agent |
| ACON (failure-driven) | Optimize compression via paired trajectories | 26-54% memory reduction, 95%+ accuracy |

### Compression Ratios

| Content | Ratio |
|---------|-------|
| Old conversation | 3:1 to 5:1 |
| Tool outputs | 10:1 to 20:1 |
| Recent 5-7 turns | No compression |
| System prompt | No compression |

### What Does NOT Work
- Bigger windows don't prevent rot
- RAG/embeddings alone have mathematical ceiling
- Post-hoc (reactive) compaction — proactive is far better

---

## 6. Spec-Driven Development

### Addy Osmani's 5 Elements
1. Context (background, stack, structure)
2. Task (clear goal)
3. Constraints (must/must not)
4. Edge Cases (pitfalls)
5. Acceptance Criteria (verifiable)

### Three-Tier Boundary System
- **Always Do**: Safe independent actions
- **Ask First**: High-impact requiring review
- **Never Do**: Absolute prohibitions

### ALMAS Framework (Sprint-Based)
- Sprint Agent (PM + Scrum Master): refines tasks, acceptance criteria, effort
- Supervisor: allocates to suitable LLMs
- Developer: implements
- Summary Agent: context compression
- Control Agent: coordinates

---

## 7. Key Research Papers

1. **Agent-as-a-Judge** (Aug 2025) — 0.3% disagreement with humans
2. **CodeJudgeBench** (Jul 2025) — 26 LLMs, 5352 pairs; thinking models outperform
3. **ALMAS** (Oct 2025) — Agile multi-agent framework
4. **JetBrains Observation Masking** (Dec 2025) — Better than LLM summarization
5. **Chroma Context Rot** (2025) — 18 frontier models all degrade

---

## 8. Commercial Tool Architectures

### Devin (Cognition AI)
- Planner (strategy) + Coder (implementation) + Critic (adversarial review) + Browser (docs)
- Devin Review catches ~30% more issues
- PR merge rate: 34% → 67% over 18 months

### OpenAI Codex
- Sealed sandbox per task, internet disabled
- RL-trained on real coding tasks
- `/responses/compact` for auto compaction
- Prompt caching: linear not quadratic

### Cursor
- Up to 8 parallel agents in isolated Ubuntu VMs with git worktrees
- 61.3 CursorBench, 73.7 SWE-bench Multilingual

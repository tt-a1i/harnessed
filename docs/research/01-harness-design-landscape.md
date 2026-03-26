# Harness Design Landscape Research

## Definition

**Harness design** (harness engineering) is the discipline of designing systems, constraints, and feedback loops that wrap around AI coding agents to make them reliable in production. The term entered mainstream use in early 2026.

A harness is NOT the agent itself. It is the complete infrastructure governing how the agent operates: tools, guardrails, feedback loops, and observability.

**Core equation: Agent = Model + Harness**

Phil Schmid's analogy:
- Model = CPU (raw processing)
- Context Window = RAM (limited, volatile)
- Agent Harness = Operating System (curates context, handles boot, provides drivers)
- Agent = Application (user-specific logic)

---

## Key Publications

### Anthropic — "Effective Harnesses for Long-Running Agents" (Nov 2025)

Author: Justin Young.

**Core problem:** Agents work in discrete sessions with no memory between shifts.

**Two-part architecture:**

1. **Initializer Agent** — First session establishes: `init.sh`, `claude-progress.txt`, initial git commit, comprehensive feature requirements list (200+ features).

2. **Coding Agent** — Subsequent sessions: read progress + git history, select single feature, make incremental progress, leave structured updates via git commits.

**Key details:**
- Feature list in JSON (not Markdown) — models less likely to inappropriately modify JSON
- Agents can only modify the `passes` field
- Every session starts with `pwd`, git logs, feature list, dev server, basic tests
- Critical failure: agents marking features complete without e2e testing → solution: Puppeteer MCP

### Anthropic — "Harness Design for Long-Running Application Development" (Mar 2026)

Author: Prithvi Rajasekaran.

**Three-agent architecture:**

1. **Planner** — Transforms 1-4 sentence prompts into comprehensive specs. Avoids granular technical details.
2. **Generator** — React/Vite/FastAPI/SQLite stack. Incremental implementation, git version control.
3. **Evaluator** — Playwright MCP for real UI interaction. Grades against sprint contracts + discovered bugs.

**Sprint Contracts** — Pre-implementation "done" criteria bridging user stories and testable implementations.

**Four evaluation criteria for frontend:**
1. Design Quality (coherence)
2. Originality (penalizes template defaults, "AI slop")
3. Craft (hierarchy, spacing, contrast)
4. Functionality (usability, task completion)

**Critical finding:** "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work — even when quality is obviously mediocre."

**Benchmarks:**

Retro Game Maker (Opus 4.5):
| Setup | Duration | Cost | Result |
|-------|----------|------|--------|
| Solo agent | 20 min | $9 | Non-functional |
| Full harness | 6 hours | $200 | Polished, 16-feature |

DAW (Opus 4.6):
| Phase | Duration | Cost |
|-------|----------|------|
| Total | 3h 50min | $124.70 |

### OpenAI — "Harness Engineering: Leveraging Codex" (Feb 2026)

1M+ lines of code, zero human-written. 3 engineers, 5 months, 3.5 PRs/engineer/day.

**Three-category framework:**
1. **Context Engineering** — Living knowledge base, observability access, browser navigation
2. **Architectural Constraints** — Custom linters + LLM monitoring, enforced module boundaries
3. **"Garbage Collection"** — Periodic agents identifying inconsistencies, violations, entropy

Key: "When the agent struggles, treat it as a signal: identify what is missing."

### Martin Fowler / Thoughtworks (Feb 2026)

Author: Birgitta Bockeler.

- Harnesses may become the successor to service templates
- Tech stack convergence: organizations selecting stacks for "AI-friendliness"
- Legacy codebases may resist harness retrofitting → pre-AI vs post-AI divide
- Gap: OpenAI writeup lacks "verification of functionality and behaviour"

---

## Production Implementations

### Stripe — "Minions"
- 1,300+ AI PRs per week
- Multiple smaller agents in parallel on decomposed subtasks
- Six-layer governance: sandbox isolation, deterministic gates, self-healing caps
- Agents cannot modify code outside assigned boundaries

### Shopify — "Roast"
- AI code review on every PR above thresholds
- Structured, actionable feedback by category
- Multi-agent routing: specialized agents for catalog, themes, storefront

### Hightouch
- Planning/execution separation: `make_plan`, `execute_step`, `update_plan`
- File buffering for large datasets (pointer in context, data on disk)
- Dynamic subagents as "context firewalls"
- Fan-out: hundreds of parallel calls to cheap models for classification

### Manus
- Rewrote harness 5 times in 6 months
- "Stochastic Graduate Descent"
- Key lesson: every piece of hand-coded logic is a liability when the next model ships

---

## The "Big Model vs Big Harness" Debate

**Big Model side:**
- Boris Cherny (Claude Code): "all the secret sauce is in the model"
- Noam Brown: "scaffolds will be replaced by reasoning models"
- Scale AI SWE-Atlas: harness choice produces "negligible differences"

**Big Harness side:**
- Jerry Liu: "The Model Harness is Everything"
- Pi Blog: optimizing harness improved performance across 15 LLMs "in one afternoon"
- Aaron Levie: "The force multiplier of the agent harness right now is crazy"
- Same model scored 78% in one harness, 42% in another

**Reality:** Both matter. The optimal harness changes with each model release.

---

## Open Source Implementations

| Project | Description |
|---------|-------------|
| LangChain Deep Agents | Planning tools, filesystem backend, subagent spawning |
| OpenHarness | Code-first SDK based on Vercel AI SDK |
| Composio Agent Orchestrator | Parallel agents in isolated worktrees |
| DeerFlow 2.0 (ByteDance) | SuperAgent harness with skill system |
| HiClaw (Alibaba) | Collaborative multi-agent OS |

---

## Key Quantitative Thresholds

- Context degradation starts at **60% utilization**
- Compact at **70% utilization**
- Agents degrade after **35 minutes** continuous work
- Doubling task duration **quadruples** failure rates
- At 95% per-step reliability over 20 steps: **36% combined success**
- Signal-to-noise can drop to **2.5%** after multi-file searches

---

## Practical Recommendations (Consensus)

1. **Build to Delete** — Manus rewrote 5x; every model release changes optimal structure
2. **Start Simple** — Robust atomic tools; let model plan; add complexity after real failures
3. **Separate Planning and Execution** — Never let agents write code until plan is reviewed
4. **Documentation as Living System** — Update AGENTS.md whenever agents fail
5. **Verification is Non-Negotiable** — Code compiled, tests run, schemas checked, never trust blindly
6. **Constrain to Enable** — More reliability = more constraints, not fewer

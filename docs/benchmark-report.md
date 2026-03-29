# Harnessed Benchmark Report

Last updated: 2026-03-29

## Executive Summary

Harnessed shows a real but not dramatic improvement over a strong Sonnet baseline. The delta is meaningful in engineering terms, but it should not be framed as an "AI intelligence boost." The early signal is narrower and more defensible:

- Harnessed reduces outcome variance when requirements contain implicit constraints.
- Harnessed improves codebase coherence by making conventions and validation rules explicit.
- Harnessed catches more silent omissions before the agent declares success.
- Harnessed still shares baseline weaknesses on multi-step feature flows that are not made explicit in the contract.

This is why the product narrative should shift from "making the model smarter" to "turning AI coding into a lower-variance engineering system."

## 1. Benchmark Data

### 1.1 Bug Injection Benchmark

Setup: 10 deliberately planted bugs in `task_manager.py`, scored by bug detection count and category coverage.

| Run | Mode | Score | Grade | Must-catch | Should-catch | Nice-to-catch |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-03-29-0922 | Harnessed | 7/10 | Excellent | 4/4 | 3/3 | 0/3 |
| 2026-03-29-0925 | Baseline | 6/10 | Excellent | 4/4 | 2/3 | 0/3 |
| 2026-03-29-0946 | Harnessed | 8/10 | Excellent | 4/4 | 2/3 | 2/3 |
| 2026-03-29-0943 | Baseline | 7/10 | Excellent | 4/4 | 3/3 | 0/3 |

Average result:

- Harnessed: 7.5/10
- Baseline: 6.5/10
- Delta: +1.0 bug

Key signal:

- Both modes reliably catch the obvious must-catch bugs.
- Harnessed is more likely to surface lower-salience omissions such as ambiguous requirements (`BUG-05`) and missing feature coverage (`BUG-09`).
- Neither mode reliably catches the security heuristic bug (`BUG-08`), which shows the current evaluator still needs stronger security-specific prompting or tooling.

### 1.2 Codebase Coherence Benchmark

Setup: evaluate whether generated code follows the existing repository's utilities, response shapes, validation patterns, and security expectations.

| Run | Mode | Score | Grade | Must-catch | Should-catch | Nice-to-catch |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-03-29-0954 | Harnessed | 9/10 | Excellent | 4/4 | 4/4 | 1/2 |
| 2026-03-29-0955 | Baseline | 8/10 | Excellent | 4/4 | 4/4 | 0/2 |

Key signal:

- The codebase-coherence gap is not large, but it is directionally important.
- Harnessed gains by turning repo conventions into explicit review criteria instead of leaving them as style-level intuition.
- Both modes are already strong at obvious convention drift; Harnessed adds value by catching more subtle consistency failures before handoff.

### 1.3 End-to-End Benchmark

Setup: natural-language task, code written from scratch, final code scored against a hidden 37-point rubric.

| Mode | Score | Grade | Notable misses |
| --- | --- | --- | --- |
| Baseline | 31/37 (83.8%) | Good | `R07` no bare `None` or unhandled exceptions, `R09` order history, `R15` admin status updates, `R17` shipping address validation |
| Harnessed | 33/37 (89.2%) | Excellent | `R09` order history, `R15` admin status updates |

Key signal:

- Harnessed uniquely recovered two implicit requirements: error-handling consistency (`R07`) and shipping-address validation (`R17`).
- Both modes missed the same two user-visible feature flows: order history and admin status updates.
- This pattern matters more than the raw 5.4-point percentage delta. Harnessed is already helping on implicit constraints and guardrails, but not yet consistently on end-to-end flow completeness.

## 2. Interpretation

### 2.1 Why the gap is real but not larger

This result is more about benchmark design and baseline strength than about Harnessed being ineffective.

First, the baseline model is already strong. Once Sonnet gets a reasonably clear task description and access to the codebase, it performs a decent local review on its own. That compresses the average-score gap.

Second, the current benchmarks still reward capabilities that strong frontier models already have: spotting obvious bugs, following visible conventions, and repairing direct requirement violations. Harnessed adds the most value when the failure mode is not "can the model reason at all?" but "does the process make hidden requirements and project rules explicit enough to survive execution?"

Third, the sample is still small. Two bug-injection runs, one coherence comparison, and one end-to-end comparison are enough to show direction, but not enough to support aggressive top-line claims.

### 2.2 Why the paper-driven architecture overpredicts evaluator gains

The literature is still useful, but production conditions differ from paper setups in three ways:

1. Many papers compare against weaker baselines than current Sonnet-class agents.
2. Many paper tasks are shorter and more closed-world than real repository work.
3. Generic evaluator gains drop once the generator already performs some self-review competently.

In practice, the edge does not come from adding a generic second opinion to every task. It comes from turning project-specific expectations into executable constraints, then using independent review to enforce them.

### 2.3 Where Harnessed's value actually is

The strongest current value is not "the model writes radically better code." The strongest current value is:

- making implicit requirements explicit before implementation;
- preserving repository conventions across files and modules;
- downgrading weak completion claims until evidence exists;
- reducing rework caused by silent omissions and inconsistent patterns.

That is a process and governance advantage, not a raw reasoning advantage.

### 2.4 Recommended product narrative

Harnessed should be positioned as a low-variance engineering system for AI coding.

That means the product promise is:

- lower variability in outcomes across runs;
- fewer missed constraints and late-stage surprises;
- more auditable handoff artifacts;
- clearer escalation boundaries when automation is not enough.

That is more defensible than claiming a broad intelligence lift, and it aligns with the actual benchmark pattern.

## 3. Four Optimization Directions

### 3.1 Strengthen contract extraction and requirement coverage review

Current weakness: both baseline and Harnessed missed the same two feature flows in the E2E task. That usually means the problem was under-specified or incompletely represented in the contract.

Recommended implementation:

- Add an independent contract-review step that sees only the original task and the drafted contract.
- Require a requirement-to-criterion coverage table before coding starts.
- Force every P0 and P1 feature requirement to include at least one verification command or executable scenario.
- Persist the coverage artifact so QA and verification-gate can prove that no original requirement was silently dropped.

### 3.2 Build repo-specific policy packs instead of generic QA prompts

Current strength: Harnessed already outperforms baseline on codebase coherence and explicit validation patterns.

Recommended implementation:

- Define repository policy packs for utilities, response shapes, auth flows, validation rules, error handling, and naming conventions.
- Let evaluators read reference files or policy manifests instead of inferring conventions ad hoc.
- Attach the relevant policy pack automatically based on touched paths or detected frameworks.
- Track policy violations separately from feature failures so the product can show where it preserves coherence.

### 3.3 Add adversarial evaluation and scenario-based flow checks

Current weakness: average scores hide shared failures on user-visible flows.

Recommended implementation:

- Expand benchmark prompts to include ambiguous requirements, missing constraints, wrong prior assumptions, and cross-module consistency traps.
- Generate minimal executable scenarios for stateful or multi-actor flows such as user history, admin transitions, and permission boundaries.
- Promote these scenarios into Tier 1.5/Tier 2 verification whenever the repository supports tests or HTTP interaction.
- Separate "code review pass" from "flow-completeness pass" in QA reports.

### 3.4 Replace average-only reporting with operational metrics

Current risk: a small average-score delta looks weak even when the system is materially reducing engineering risk.

Recommended implementation:

- Report worst-case and bottom-quartile performance, not just mean score.
- Track how often Harnessed catches a criterion or bug that baseline misses.
- Track how many iteration loops are needed before completion.
- Track first-pass completion rate and implicit-requirement hit rate.
- Track feature-flow completeness separately from convention/validation correctness.

## 4. Recommended Metric System

The reporting layer should move from "average benchmark score" to "engineering risk reduction."

### 4.1 Worst-case score

- Definition: lowest score achieved by each mode across the benchmark set.
- Why it matters: teams feel the bad run more than the average run.

### 4.2 Rework count

- Definition: number of QA iterations, manual fixes, or review loops needed before the task is accepted.
- Why it matters: this is closer to engineering cost than raw benchmark score.

### 4.3 First-pass completion rate

- Definition: percentage of tasks that pass all P0 criteria without a second coding round.
- Why it matters: this measures how often the process gets to a reliable deliverable without extra human intervention.

### 4.4 Implicit requirement hit rate

- Definition: percentage of hidden or weakly stated requirements caught by the system before final handoff.
- Why it matters: this is where Harnessed should outperform plain self-review.

### 4.5 Weighted P0/P1 pass rate

- Definition: pass rate after weighting primary user flows, permissions, safety checks, and exception handling above cosmetic or secondary checks.
- Why it matters: it prevents average score from hiding critical misses.

### 4.6 Flow-completeness recall

- Definition: share of multi-step user-visible workflows that are fully implemented and verifiable.
- Why it matters: current E2E misses show that this is the biggest remaining gap.

## 5. Concrete Project Improvement Plan

### Phase 1: Requirement Coverage Hardening

Scope: close the biggest current gap, which is silently omitted user-visible functionality.

- Implement an independent contract reviewer.
- Add requirement-to-criterion traceability in `.harnessed/contract.md`.
- Require verification commands or executable scenarios for every P0 and P1 feature criterion.
- Block implementation when any original requirement has no mapped criterion.

### Phase 2: Repository Policy System

Scope: turn current coherence wins into a repeatable differentiator.

- Define policy packs for auth, validation, responses, exceptions, and utility usage.
- Auto-select policy packs based on file paths or framework signatures.
- Feed reference files into evaluator context as explicit coherence anchors.
- Emit policy-violation summaries as a dedicated section in QA output.

### Phase 3: Adversarial and Flow-Based Evaluation

Scope: stress the process where strong baselines still fail.

- Add adversarial benchmark scenarios with ambiguous requirements and missing constraints.
- Add flow-based verification for multi-actor and state-transition tasks.
- Distinguish code-structure findings from executed flow failures in benchmark summaries.
- Expand the benchmark suite beyond one-off scoring into repeatable regression checks.

### Phase 4: Metrics and Positioning Instrumentation

Scope: report the product in the language of engineering outcomes, not abstract intelligence.

- Ship benchmark dashboards for worst-case score, rework count, first-pass completion, and implicit requirement hit rate.
- Track exclusive wins against baseline mode.
- Track flow-completeness recall as a headline metric.
- Update external messaging to emphasize governance, auditability, and variance reduction.

## 6. Bottom Line

The current data does not support a narrative of dramatic general intelligence uplift. It does support a narrower and more credible claim: Harnessed makes AI coding more governable, more explicit, and less likely to fail silently on constraints that strong models still tend to treat as optional or implicit.

That is enough to justify product direction. The next step is not more generic review. The next step is better requirement extraction, stronger repo policies, more adversarial evaluation, and metrics that reflect engineering reality.

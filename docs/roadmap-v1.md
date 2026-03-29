# Harnessed v1.0 Roadmap

Based on architecture-level threat modeling, design pattern comparison, and extensibility analysis.

## Benchmark-Driven Priorities (March 2026)

Harnessed is already showing a real quality delta over baseline: it catches more explicit invariants, improves codebase coherence, and reduces silent convention drift through isolated QA. The next gains are unlikely to come from "more review" in the abstract. They will come from stronger requirement coverage before coding, more repository-specific guardrails during review, more adversarial verification of user-visible flows, and better metrics that describe engineering risk rather than average score.

### 1. Contract Extraction and Requirement Coverage

Goal: stop silent feature omissions before implementation begins.

- Add an independent contract-review subagent that sees only the original request and the drafted contract.
- Require a requirement-to-criterion coverage map before code generation starts.
- Require verification commands or executable scenarios for every P0 and P1 feature criterion.
- Persist coverage artifacts in `.harnessed/` so QA and verification-gate can prove that no original requirement was dropped.

### 2. Repository Policy Packs

Goal: turn current codebase-coherence wins into a repeatable product advantage.

- Define policy packs for auth, validation, responses, exception handling, and approved utilities.
- Auto-select relevant policy packs based on touched files or detected frameworks.
- Feed evaluators reference files or manifests instead of relying on ad hoc convention inference.
- Report policy violations separately from feature misses so coherence improvements remain visible.

### 3. Adversarial Evaluation and Flow Verification

Goal: expose the failure modes that average scoring currently hides.

- Add adversarial benchmark scenarios with ambiguous requirements, missing constraints, and wrong prior assumptions.
- Add executable user-flow and admin-flow checks for multi-step stateful tasks.
- Promote these scenarios into Tier 1.5 or Tier 2 verification whenever the repo supports tests or HTTP interaction.
- Separate code-review PASS from flow-completeness PASS in QA output and benchmark reporting.

### 4. Metrics and Positioning Instrumentation

Goal: measure and communicate engineering risk reduction, not vague model uplift.

- Track worst-case score and bottom-quartile score in addition to averages.
- Track rework count, first-pass completion rate, and implicit-requirement hit rate.
- Track exclusive wins versus baseline mode to show where Harnessed adds unique value.
- Track flow-completeness recall as a headline metric for end-to-end tasks.

---

## High Priority

### Contract Review Step
After contract-writing, dispatch a lightweight subagent that receives ONLY the user's original request and the proposed contract. Its job: "What requirements from the user's request are not covered by these criteria?" This catches the single biggest design weakness: the agent that codes also defines what "done" means.

- Addresses: gaming the contract (Threat 2), context firewall gap (Pattern 4)
- Trigger: Large tasks mandatory, Standard tasks optional
- Cost: ~0.3x additional token per task
- **Status: PARTIALLY IMPLEMENTED** — Step 6b in contract-writing does self-verification (requirement→criterion mapping), but uses the same agent, not an independent subagent. The independent subagent approach remains a v1.1 goal.

### Criteria Priority Tiers (P0/P1/P2)
Add priority levels to contract criteria:
- P0 (blocking): FAIL on P0 = BLOCKED
- P1 (important): FAIL on P1 = ITERATE
- P2 (nice-to-have): FAIL on P2 does not block SHIP

Currently all criteria are equal weight, which means a cosmetic issue blocks SHIP the same as a security issue.

### Configuration File (`.harnessed/config.md`)
User-overridable settings without forking:
- `max_iterations`: default 3
- `spec_source`: auto | path | standalone
- `additional_anti_rationalization`: project-specific entries
- `tier2_indicators`: additional patterns
- `evaluator_model`: highest | specific model name

---

## Medium Priority

### Evaluator Model Configuration
Allow specifying a different model for the evaluator subagent. Cross-model evaluation eliminates shared blind spots. Default: use the most capable available model.

### ITERATE Triage Read (Back-Pressure)
When processing an ITERATE result, read only FAIL/PARTIAL entries + overview. Skip PASS entries to conserve context. Full report remains on disk for verification-gate and user.

### Security Checklist
When contract criteria touch auth, input handling, or API endpoints, append a security-focused checklist to the evaluator prompt (OWASP top patterns, common XSS/injection vectors). Not a separate agent — an addendum to the existing evaluator.

- **Status: PARTIALLY IMPLEMENTED** — Security checks (XSS, SQL injection, auth bypass, hardcoded secrets) are now always present in the evaluator Tier 1 code review. The conditional/context-aware triggering (only when criteria touch auth/input) remains a future enhancement.

### Skill Format Documentation
Document in spec: frontmatter fields, directory layout, supporting files, user-invocable meaning, how to wire new skills into the meta-skill routing.

---

## Low Priority (v1.1+)

### Per-Criterion Evaluation
For Large tasks, dispatch N evaluator subagents each reviewing one criterion with relevant diff hunks only. OpenObserve model. Increases cost but dramatically improves evaluation depth for complex diffs.

### Cross-Session Memory
Read archived QA reports to identify recurring failure patterns. "This component has failed QA 3 times on error handling edge cases." Makes QA smarter over time.

- **Status: PARTIALLY IMPLEMENTED** — `.harnessed/failure-patterns.md` tracks recurring failures within a project and informs contract-writing. However, it does not read archived QA reports or aggregate across sessions — it records patterns as they occur.

### Archive Rotation
Delete .harnessed/archive/ entries older than 30 days or limit to last 20 entries.

### Confidence-Based Routing
If model self-assessment confidence is high and task is Standard, optionally skip contract and go straight to code + QA. Lets the harness shrink as models improve. Configurable dial: `contract_required: always | standard_and_large | large_only | never`.

### Dynamic Skill Discovery
New skills auto-discovered from skills/ directory without editing meta-skill. Skill frontmatter controls trigger conditions. v0.1 uses manual routing (explicit and debuggable).

---

## Architecture Decisions to Preserve

These are strengths, not limitations — do not change:

1. **File-based communication** — artifacts on disk, not in context. Survives compaction.
2. **Single evaluator for v0.1** — specialization is premature at 4 skills.
3. **Context isolation** — evaluator cannot see generator reasoning. Most important design property.
4. **Modular skill architecture** — each skill deletable independently. Harness shrinks as models improve.
5. **Task-size routing** — micro/standard/large is the right granularity.

---

## Known Inherent Limitations

Cannot be fully fixed by design changes:

1. **Same model blind spots** — evaluator shares model-level knowledge gaps with generator. Mitigated by cross-model eval (configurable), not eliminable.
2. **Contract-writing bias** — the coder writes the spec. Mitigated by contract review step, user review for Large tasks.
3. **Evaluator attention ceiling** — LLM evaluator is equivalent to a 15-minute PR review, not a deep audit. Sufficient for Standard tasks, insufficient for security-critical systems.

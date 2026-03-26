# Harnessed v1.0 Roadmap

Based on architecture-level threat modeling, design pattern comparison, and extensibility analysis.

---

## High Priority

### Contract Review Step
After contract-writing, dispatch a lightweight subagent that receives ONLY the user's original request and the proposed contract. Its job: "What requirements from the user's request are not covered by these criteria?" This catches the single biggest design weakness: the agent that codes also defines what "done" means.

- Addresses: gaming the contract (Threat 2), context firewall gap (Pattern 4)
- Trigger: Large tasks mandatory, Standard tasks optional
- Cost: ~0.3x additional token per task

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

### Skill Format Documentation
Document in spec: frontmatter fields, directory layout, supporting files, user-invocable meaning, how to wire new skills into the meta-skill routing.

---

## Low Priority (v1.1+)

### Per-Criterion Evaluation
For Large tasks, dispatch N evaluator subagents each reviewing one criterion with relevant diff hunks only. OpenObserve model. Increases cost but dramatically improves evaluation depth for complex diffs.

### Cross-Session Memory
Read archived QA reports to identify recurring failure patterns. "This component has failed QA 3 times on error handling edge cases." Makes QA smarter over time.

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

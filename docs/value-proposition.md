# Harnessed: Turn AI Coding Into a Low-Variance Engineering System

## The Problem

AI coding agents are no longer failing only because they lack raw capability. Strong models can often produce useful code on the first try. The persistent problem is that AI coding remains high-variance: implicit requirements stay implicit, repository conventions drift across files, and agents declare success before there is enough evidence that the delivered code is actually complete.

This is not just a prompt-quality problem. Research demonstrates that LLMs exhibit **self-preference bias**: when asked to judge outputs, they favor responses that resemble their own style, regardless of actual quality [1][2]. In coding contexts, this means an agent that writes code and then reviews its own code is structurally biased toward concluding that the code is correct. But self-evaluation bias is only one source of the larger issue: delivery quality is unstable because constraints are not explicit enough, review is not proportionate to risk, and completion claims are often based on assertion instead of evidence.

The consequences are concrete:
- Agents declare tasks "done" when requirements are incomplete
- Cross-file patterns drift away from the codebase's actual conventions
- Silent omissions survive until human review or production use
- Rework increases because the process detects gaps too late

Harnessed exists to reduce that variance. It turns implicit requirements into explicit contracts, forces evidence-backed verification, and routes work through stronger review only when the risk justifies it. The goal is not to claim that AI coding suddenly becomes much smarter. The goal is to make AI coding more governable, more auditable, and less likely to fail silently.

---

## Practical Signal From Early Benchmarks

Our current benchmark data shows a real but bounded quality delta over a strong Sonnet baseline:

- End-to-end task quality improved from **31/37 (83.8%)** to **33/37 (89.2%)**
- Bug-injection detection improved from **6.5/10 average** to **7.5/10 average**
- Codebase-coherence review improved from **8/10** to **9/10**

These numbers should not be read as a dramatic intelligence jump. They should be read as evidence that Harnessed reduces missed constraints, catches more implicit validation and error-handling issues, and preserves repository coherence more reliably. The product value is lower variance in delivery quality, not a claim that the underlying model has become universally better at every coding task.

---

## Core Mechanisms and Their Evidence Base

### 1. Independent Evaluation (Separation of Generator and Reviewer)

**Problem:** Self-evaluation is biased. The same model that wrote code cannot reliably judge it.

**Evidence:**
- LLMs systematically prefer their own outputs and can even recognize which outputs are theirs [1][2]
- Dedicated evaluator models, separated from the generator, produce judgments more aligned with human assessment [5][7]
- Anthropic's production guidance identifies the evaluator-optimizer pattern — where a separate evaluator grades a generator's work — as a core architecture for effective coding agents [11]

**Harnessed's approach:** The QA evaluator runs as an isolated subagent. It sees only the code diff, the acceptance contract, and project context. It never sees the generator's reasoning, self-assessment, or conversation history. This information barrier is the foundation of independent judgment.

**Honest boundary:** Independent evaluators also have bias [5]. Harnessed reduces self-evaluation bias; it does not eliminate all bias. Confidence and uncertainty are first-class outputs in every QA report.

---

### 2. Contract-Driven Development (Explicit Acceptance Criteria Before Code)

**Problem:** When acceptance criteria are implicit, both the generator and the evaluator operate on assumptions. The generator builds what it thinks is right; the evaluator checks what it thinks was asked for. Neither may match what the user actually needs.

**Evidence:**
- CodeT demonstrates that generating explicit tests alongside code, then using those tests to filter candidates, significantly improves code selection quality [9]
- AlphaCodium shows that multi-stage flows with explicit specification understanding, test reasoning, and iterative validation outperform single-shot generation [10]
- Competition-level evaluation research confirms that external, executable, standardized criteria are more reliable than model-to-model judgment [12]

**Harnessed's approach:** Before any code is written, a testable contract is generated: explicit acceptance criteria, each independently verifiable, each atomic and unambiguous. After drafting, every user requirement is mapped to at least one criterion and gaps are filled. The evaluator grades against this contract — not against its own interpretation of the task.

**Honest boundary:** Contracts are only as good as the requirement understanding at drafting time. If the user's intent is ambiguous and the contract doesn't capture it, downstream verification will be precise but may miss the real need. For large tasks, Harnessed requires explicit user review of the contract before coding begins.

---

### 3. Evidence-Based Verification Gate (Proof, Not Assertion)

**Problem:** Agents routinely claim completion without proof. "I implemented it correctly" is an assertion, not evidence.

**Evidence:**
- Anthropic's agent design guidance emphasizes that coding agents work best when they rely on verifiable external evidence — tool outputs, test results, execution traces — rather than self-reported confidence [11]
- The broader LLM-as-judge literature shows that structured evaluation with explicit rubrics produces more reliable and consistent judgments [6][7]

**Harnessed's approach:** The verification gate requires concrete evidence for every automatable criterion: file:line citations, test names, command outputs, or HTTP response data. QA confirmation from the evaluator is supplementary context, not primary evidence. Self-review notes are background information, never proof. No completion signal is permitted until the gate passes.

**Honest boundary:** Evidence-based verification works well for code-verifiable requirements. For criteria that require human judgment (visual design, UX feel, complex interaction patterns), the gate honestly marks them as pending human review rather than fabricating automated evidence.

---

### 4. Multi-Evaluator Review (Corroboration for High-Risk Work)

**Problem:** A single evaluator, even an independent one, can miss issues or exhibit its own blind spots.

**Evidence:**
- ChatEval demonstrates that multiple evaluators debating and cross-checking produce more stable, human-aligned judgments than a single evaluator [13]
- MetaGPT shows that encoding role separation and intermediate verification into multi-agent workflows reduces cascading hallucination [14]

**Harnessed's approach:** Standard tasks use a single primary evaluator. High-risk tasks (auth, security, payments, destructive operations, public endpoints) escalate to corroborated review with a second independent evaluator. Security-sensitive tasks add a dedicated security reviewer. When evaluators materially disagree, a tie-break reviewer resolves the conflict. If tie-break cannot resolve it, the issue escalates to the user.

**Honest boundary:** More evaluators increase cost and latency. The multi-evaluator path is reserved for high-risk work where the cost of a missed issue outweighs the cost of additional review time.

---

### 5. Risk Classification and Calibration Governance

**Problem:** Not all tasks carry equal risk, but agents often apply uniform (usually insufficient) scrutiny. Additionally, evaluators may drift over time without anyone noticing.

**Evidence:**
- Industrial code review studies show that AI review adds value but also adds cycle time and friction [16][17]. Applying maximum friction to every task creates adoption resistance.
- The LLM-as-judge literature documents position bias, length bias, and self-enhancement bias in evaluator models [5]. Without calibration, these biases compound silently.

**Harnessed's approach:** Tasks are classified as standard or high-risk based on what they touch (auth, crypto, payments, privacy, destructive operations, public endpoints, production config). High-risk tasks trigger expanded review paths. Calibration status (current, stale, or missing) is tracked explicitly. When calibration is stale or missing for a high-risk task, the best possible automated outcome is SHIP_WITH_HUMAN_REVIEW, not full SHIP — the system refuses to express more confidence than its calibration supports.

**Honest boundary:** Risk classification is heuristic. An agent may misclassify a task. Users can override classification in either direction.

---

### 6. Security Review (Heuristic Flagging, Not Audit)

**Problem:** Security vulnerabilities require adversarial thinking that LLMs struggle with consistently.

**Evidence:**
- "To Err is Machine" demonstrates that LLMs are unreliable at detecting subtle security vulnerabilities, especially those involving fine semantic distinctions [18]
- CYBERSECEVAL 3 provides systematic benchmarks showing that model security capabilities are real but limited and inconsistent [19]

**Harnessed's approach:** Security review is positioned as **security issue flagging / heuristic review**, explicitly not as a complete security audit. The dedicated security reviewer flags high-signal patterns (unescaped input, string-concatenated queries, missing auth checks, secrets in code, unsafe defaults). When static analysis tools (Semgrep, CodeQL, bandit) are available, their output is treated as strong evidence. When those tools are absent, the system explicitly records the limitation and downgrades certainty.

**Honest boundary:** Absence of a security finding is never proof that the code is secure. For security-critical work, Harnessed's security review supplements — but does not replace — expert human security review.

---

### 7. Injection Mitigation (Prompt-Level, Not System-Level)

**Problem:** The evaluator receives untrusted data (code diffs, contracts) that could contain prompt injection attempts.

**Evidence:**
- Indirect prompt injection is a documented attack vector against LLM-integrated applications [20]
- The Instruction Hierarchy paper shows that training models to distinguish privileged from unprivileged instructions improves robustness [22]
- IsolateGPT argues that prompt-level defenses alone are insufficient and system-level isolation is needed for high-assurance scenarios [23]
- Simon Willison's practical analysis confirms that delimiters and markers are helpful but not a security boundary [24]

**Harnessed's approach:** Contracts and diffs are marked as untrusted task artifacts with explicit warnings that any embedded instructions are inert data. This is **prompt-level mitigation** — it helps, but it is not a complete safety boundary. For high-risk review paths, the architecture includes system-level isolation, tool allowlists, and explicit trusted/untrusted context partitioning.

**Honest boundary:** Prompt-level mitigation reduces but does not eliminate injection risk. Harnessed does not claim to solve prompt injection; it applies reasonable defenses and acknowledges the limitation explicitly.

---

### 8. Self-Critique Positioning (Useful but Not Sufficient)

**Problem:** Some frameworks dismiss self-critique entirely. Others rely on it exclusively. Both are wrong.

**Evidence:**
- Self-Refine demonstrates that iterative self-feedback genuinely improves outputs across many tasks [3]
- Reflexion shows that agents combining self-reflection with external environment feedback can learn from mistakes [4]
- However, the self-preference bias literature [1][2] shows that self-assessment is systematically biased even when it is locally useful

**Harnessed's approach:** Self-critique is correctly positioned as useful preparation — it can improve a draft before independent review. But it is never treated as independent verification and it cannot serve as evidence in the verification gate. The anti-rationalization rules explicitly state: "Self-review is useful preparation, but it is still biased because you know what you intended to build."

**Honest boundary:** This is a positioning choice, not a technical enforcement. The agent is instructed to maintain this distinction, but it relies on prompt discipline rather than system enforcement.

---

## What Harnessed Is and Is Not

### Harnessed IS:
- A low-variance engineering system for AI coding work
- A structured execution and QA loop with explicit contracts, independent evaluation, and evidence-based gates
- A way to reduce missed requirements, convention drift, and late-stage rework
- A risk-aware framework that applies proportionate scrutiny and reports uncertainty honestly

### Harnessed is NOT:
- An intelligence booster that makes every model dramatically smarter
- A guarantee of code correctness
- A replacement for human security review on critical systems
- A system with zero evaluator bias
- A complete defense against prompt injection
- A substitute for comprehensive test suites

The value of Harnessed is not that it makes AI coding perfect, or even uniformly better on every benchmark. The value is that it turns AI coding into a more **accountable and governable engineering system** — with explicit criteria, independent review, concrete evidence, honest uncertainty reporting, and clearer boundaries for when human judgment is still required.

---

## References

[1] Wataoka et al. "Self-Preference Bias in LLM-as-a-Judge." 2024. https://arxiv.org/abs/2410.21819

[2] Panickssery et al. "LLM Evaluators Recognize and Favor Their Own Generations." 2024. https://arxiv.org/abs/2404.13076

[3] Madaan et al. "Self-Refine: Iterative Refinement with Self-Feedback." 2023. https://arxiv.org/abs/2303.17651

[4] Shinn et al. "Reflexion: Language Agents with Verbal Reinforcement Learning." 2023. https://arxiv.org/abs/2303.11366

[5] Zheng et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." 2023. https://arxiv.org/abs/2306.05685

[6] Liu et al. "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment." 2023. https://aclanthology.org/2023.emnlp-main.153/

[7] Kim et al. "Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models." 2024. https://arxiv.org/abs/2405.01535

[8] Li et al. "Can LLMs Replace Human Evaluators? An Empirical Study of LLM-as-a-Judge in Software Engineering." 2025. https://doi.org/10.1145/3728963

[9] Chen et al. "CodeT: Code Generation with Generated Tests." 2022. https://arxiv.org/abs/2207.10397

[10] Ridnik et al. "Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering." 2024. https://arxiv.org/abs/2401.08500

[11] Anthropic. "Building Effective Agents." 2024. https://www.anthropic.com/engineering/building-effective-agents

[12] Huang et al. "Competition-Level Problems are Effective LLM Evaluators." 2024. https://aclanthology.org/2024.findings-acl.803/

[13] Chan et al. "ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate." 2023. https://arxiv.org/abs/2308.07201

[14] Hong et al. "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework." 2023. https://arxiv.org/abs/2308.00352

[15] Qian et al. "ChatDev: Communicative Agents for Software Development." 2023. https://arxiv.org/abs/2307.07924

[16] Arakelyan et al. "Automated Code Review In Practice." 2024. https://arxiv.org/abs/2412.18531

[17] Choudhuri et al. "Rethinking Code Review Workflows with LLM Assistance." 2025. https://arxiv.org/abs/2505.16339

[18] Alqarni et al. "To Err is Machine: Vulnerability Detection Challenges LLM Reasoning." 2024. https://arxiv.org/abs/2403.17218

[19] Bhatt et al. "CYBERSECEVAL 3: Advancing the Evaluation of Cybersecurity Risks and Capabilities in Large Language Models." 2024. https://arxiv.org/abs/2408.01605

[20] Greshake et al. "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." 2023. https://arxiv.org/abs/2302.12173

[21] Xue et al. "WebInject: Prompt Injection Attack to Web Agents." 2025. https://arxiv.org/abs/2505.11717

[22] Wallace et al. "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions." 2024. https://arxiv.org/abs/2404.13208

[23] Wu et al. "IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems." 2024. https://arxiv.org/abs/2403.04960

[24] Simon Willison. "Delimiters won't save you from prompt injection." 2023. https://simonwillison.net/2023/May/11/delimiters-wont-save-you/

# Harnessed Skill Alignment Review

Last updated: 2026-03-29

## Executive Summary

基于当前产品新定位：Harnessed 不是"让模型更聪明的智力外挂"，而是"把 AI coding 变成低波动、可治理的工程系统"。按这个标准回看当前核心 skill 实现，结论很明确：

- `contract-writing` 已经开始强调隐含需求，但还停留在同一代理自提需求、自写 contract、自做 coverage 自检的闭环里。
- `independent-qa` 和 `evaluator-prompt` 仍然过于通用，缺少 repo-specific policy、reference files、flow completeness 这类真正能压低波动源的输入与输出结构。
- `verification-gate` 目前更像"证据存在性检查"，还不是"证据是否足以证明结论"的质量门。
- anti-rationalization 规则能防明显偷懒，但还不够覆盖真实世界里那些"看起来合规、实际很弱"的退化版本。

如果要让 Harnessed 真正贴合新定位，下一步最该补的是：`requirement coverage artifact`、`repo policy substrate`、`flow completeness review`、`evidence strength`。

## Part I: Core Skill Review

### Finding 1: Reviewer context is too generic for a repo-governance product

Severity: critical

Evidence:

- `skills/independent-qa/SKILL.md:86` 到 `skills/independent-qa/SKILL.md:98` 规定 reviewer 只看到 contract、diff、stack、tier、commands 等通用上下文。
- `skills/independent-qa/evaluator-prompt.md:50` 到 `skills/independent-qa/evaluator-prompt.md:57` 的 project context 也只有 stack、tier、mode、risk、commands。
- `skills/independent-qa/evaluator-prompt.md:70` 甚至在找不到实现时要求 reviewer "search the broader codebase"。

问题：

这会让 repo conventions 重新退回成模型在评审时的临场推断。对一个以"降低 convention drift"和"让项目规则显式化"为卖点的系统，这个设计太弱。Harnessed 需要让 reviewer 基于 policy packs 和 reference files 做判断，而不是靠模型自己悟。

Implication:

- 现有架构更像一个通用 QA reviewer，而不是一个 repo-aware governance layer。
- 这会直接限制 codebase coherence benchmark 上的可持续优势。

### Finding 2: QA output is criterion-centric, not flow-centric

Severity: critical

Evidence:

- `skills/independent-qa/evaluator-prompt.md:61` 到 `skills/independent-qa/evaluator-prompt.md:72` 以"for EACH criterion"为主循环。
- `skills/independent-qa/evaluator-prompt.md:115` 到 `skills/independent-qa/evaluator-prompt.md:127` 的输出中心也是 criteria passed。
- `skills/independent-qa/SKILL.md:150` 虽然提到 weak evidence 要降级，但没有把 flow completeness 作为单独的检查对象。

问题：

这会导致一个危险退化：大多数 criteria 通过，但关键用户流或管理员流缺失，系统仍然可能给出一个看起来不错的整体结果。最近 benchmark 已经暴露出这个问题：Harnessed 在隐含校验和异常路径上领先，但和 baseline 一样漏掉了完整的 user/admin feature flow。

Implication:

- 当前 QA 更擅长抓结构性和局部性问题，不够擅长守住 end-to-end completeness。
- 这与"低波动工程系统"叙事不一致，因为企业用户最在意的就是关键 flow 不能掉。

### Finding 3: Verification Gate checks that evidence exists, not that it proves the claim

Severity: high

Evidence:

- `skills/verification-gate/SKILL.md:48` 到 `skills/verification-gate/SKILL.md:57` 要求每条 criterion 给一种 primary evidence。
- `skills/verification-gate/SKILL.md:72` 到 `skills/verification-gate/SKILL.md:79` 的 gap check 只要求 automatable criterion 有 primary evidence。
- `skills/verification-gate/SKILL.md:101` 到 `skills/verification-gate/SKILL.md:103` 的 summary 模板直接写 `Verified: Yes`。

问题：

这还是"有证据"逻辑，不是"证据足以证明该结论"逻辑。对行为型 claim，`file:line` 最多能证明代码存在，不能证明行为成立；真正的证明通常需要测试、执行结果、HTTP smoke、static analysis 或更强的行为证据。

Implication:

- Harnessed 很容易在治理层面看起来严格，但在 epistemic quality 上仍然偏弱。
- 这会削弱产品叙事中最重要的部分：evidence-backed delivery。

### Finding 4: Contract-writing still lacks a first-class requirement coverage artifact

Severity: high

Evidence:

- `skills/contract-writing/SKILL.md:68` 到 `skills/contract-writing/SKILL.md:76` 已要求识别 explicit and implicit requirements，并做 coverage verification。
- 但这个 coverage verification 没有落成单独工件，也没有独立 challenge step。

问题：

当前 contract-writing 虽然方向是对的，但它仍然是一个同代理闭环。系统没有把"原始需求 -> contract criterion -> verification evidence"这条链条结构化落盘，也没有在 coding 之前引入独立 requirement coverage review。

Implication:

- contract extraction 仍然容易被生成代理的主观理解绑架。
- QA 和 gate 后续也无法证明"所有原始需求都被纳入了治理链条"。

### Finding 5: Anti-rationalization rules are still missing the most realistic failure patterns

Severity: medium-high

Evidence:

- `skills/contract-writing/SKILL.md:89` 到 `skills/contract-writing/SKILL.md:97`
- `skills/independent-qa/SKILL.md:206` 到 `skills/independent-qa/SKILL.md:214`
- `skills/verification-gate/SKILL.md:141` 到 `skills/verification-gate/SKILL.md:149`
- `skills/using-harnessed/SKILL.md:89` 到 `skills/using-harnessed/SKILL.md:98`

问题：

这些 anti-rationalization 规则已经能防"完全跳过步骤"，但还没覆盖更常见的软退化场景：

- 隐含需求先不落盘，边写边补
- repo policy 不明说，默认 reviewer 自己会懂
- 大多数 criteria 过了，就忽略关键 flow 缺失
- 引了一条 file:line，就默认证据已足够

Implication:

- 系统能防明显违规，但还不够防形式合规、实质空心的 workflow。

## Part II: Structural Gaps in the Current Design

### 1. Requirement extraction is still self-contained

系统还没有把 requirement inventory、coverage map、implicit requirement challenge 做成独立工件和独立校验步骤。

### 2. Repo-specific policy is not a first-class input

当前 repo conventions 主要存在于"让 evaluator 自己看代码理解"这一层，缺少 policy substrate。

### 3. Flow completeness is not a first-class output

当前输出结构偏 criterion-level correctness，没有单列关键 flow 完整性。

### 4. Evidence strength is under-modeled

系统能区分证据类型，但还没有系统区分证据证明力。

## Part III: External Research Scan

下面是本轮最值得保留的阅读列表，重点筛选 2023-2026 年能直接影响 Harnessed 路线的条目。

### Recommended Reading List

1. **Building Effective Agents** (2024, Anthropic Engineering)
   - 结论：最有效的 agent 系统，优势通常来自 workflow design、tooling interface、明确的 checkpoints，而不是无限增强自治。
   - 对 Harnessed 的启示：workflow engineering 本身就是产品，不是模型升级的附属品。

2. **Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering** (2024, CodiumAI / arXiv)
   - 结论：多阶段、test-based、iterative flow 比单轮 prompt 优化有效得多。
   - 启示：Harnessed 应继续押注 contract -> code -> QA -> gate 这类分层流程，但要把 contract extraction 做得更硬。

3. **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** (2024, Princeton / arXiv)
   - 结论：agent 成败高度受 ACI 影响，接口设计和环境表面非常关键。
   - 启示：repo-specific policy 不能只是一段 prompt，需要成为 agent 可消费的 interface substrate。

4. **LLM-Based Test-Driven Interactive Code Generation** (2024, IEEE TSE)
   - 结论：测试最重要的作用之一是澄清意图，不只是事后验收。
   - 启示：Harnessed 的 contract extraction 可以把测试、反例、失败样例前移成 requirement clarification 工具。

5. **Towards Formal Verification of LLM-Generated Code from Natural Language Prompts** (2025, arXiv)
   - 结论：高风险任务中，可以把自然语言意图转成更形式化的查询，再验证代码是否满足。
   - 启示：不必追求全面形式化，但可以对关键路径做 partial formalization。

6. **PropertyGPT: LLM-driven Formal Verification of Smart Contracts through Retrieval-Augmented Property Generation** (2025, NDSS)
   - 结论：形式化验证真正的瓶颈常常是 properties 从哪里来；检索历史 property 和人工规则很有效。
   - 启示：Harnessed 最该做的不是幻想 verifier 无中生有，而是从 tests、review、lint、security checklist 里抽 property。

7. **Code Gradients: Towards Automated Traceability of LLM-Generated Code** (2024, RE)
   - 结论：requirements 到 code 的 traceability 应成为 LLM coding 系统的中间层，而不是事后补丁。
   - 启示：Harnessed 应该产出 requirement-to-change trace，而不是只有 contract 和 QA 报告。

8. **Establishing Traceability Between Natural Language Requirements and Software Artifacts by Combining RAG and LLMs** (2024, ER)
   - 结论：requirements 与代码之间的语义鸿沟需要 RAG + 多索引 + 结构化工件链接来弥合。
   - 启示：repo-specific policy 的底层应是 artifact linking，而不是纯上下文堆砌。

9. **LiSSA: Toward Generic Traceability Link Recovery Through Retrieval-Augmented Generation** (2025, ICSE)
   - 结论：traceability 不应只局限在 requirements-to-code，应该覆盖多种软件工件。
   - 启示：Harnessed 后续可以把 issue、PR、design doc、tests、ownership 一并纳入治理上下文。

10. **Helping Developers Adopt Generative AI: Four Practical Strategies for Organizations** (2025, Google DORA)
    - 结论：大规模采用 AI 的关键是透明度、探索空间、明确政策和可解释的边界，而不是单个模型效果。
    - 启示：repo-specific policy 要降低不确定性，而不是单纯增加摩擦。

11. **Fostering Developers’ Trust in Generative Artificial Intelligence** (2024, Google DORA)
    - 结论：开发者 trust 与明确 policy、快速反馈、边界清晰度高度相关。
    - 启示：verification gate 应被设计成 trust-building feedback system，而不是只有阻断功能。

12. **OWASP Top 10 for LLM Applications / GenAI Security guidance** (2025 edition)
    - 结论：企业级 GenAI 治理重点是 prompt injection、output handling、supply chain、excessive agency、data leakage。
    - 启示：Harnessed 的 enterprise narrative 应该落到 guardrails、auditability、least privilege 和 bounded autonomy 上。

## Part IV: Implications for Harnessed

### 1. Contract Extraction

最值得做的是把 repo 里的隐式约束提取成可验证 contract，而不是试图一开始就发明一套高度形式化语言。

建议优先提取这些来源：

- tests 和 golden cases
- CI 失败模式
- lint / type / static rules
- PR review 常见拒绝理由
- issue / ADR / design doc 里的约束表达
- security / compliance checklist

分层思路：

- L0: repo conventions / forbidden patterns
- L1: executable examples / tests
- L2: structural invariants / schema / ownership boundaries
- L3: high-risk path partial formal specs

### 2. Repo-Specific Policy

这个方向值得当成 Harnessed 的核心资产，而不是一个附属 prompt。

policy pack 应优先覆盖：

- 哪些目录允许自动改、哪些必须审批
- 哪些命令可以直接运行
- 哪些测试是最低门槛
- 哪些文件类型禁止自动修改
- 哪些模式必须引用 repo 内依据
- 哪些变更必须走 security / migration / schema gate

### 3. Verification Gate

短期最优路径不是全面形式化验证，而是分层 verification：

- syntax / type / build
- targeted tests
- regression tests
- static analysis / secret scan / policy scan
- sandbox execution for risky changes
- critical-path partial formal checks

关键不是 gate 有多严，而是 failure feedback 是否足够结构化，能指导下一轮修复。

### 4. DX Friction

对开发者来说，摩擦主要来自不确定性，而不是单纯延迟。

Harnessed 应降低这些不确定性：

- 为什么当前改动被拦
- 依据的是哪条 repo 规则
- 还缺什么证据才能继续
- 哪些测试是必须，哪些只是建议

最重要的是"可解释的阻断"，而不是"静默失败"。

### 5. Enterprise Positioning

最可信的企业叙事不是"更聪明的 coding agent"，而是：

- repo-specific guardrails
- auditable policy enforcement
- verification-backed delivery
- bounded autonomy
- trust-preserving defaults

## Part V: Recommended Shortlist

### Priority 1: Build a requirement coverage artifact

新增 `.harnessed/coverage.md`，记录：

- 原始需求清单
- 隐含需求清单
- criterion 映射
- 尚未覆盖项
- 对应验证方式

### Priority 2: Make repo-specific policy first-class

新增可注入 evaluator 的 policy pack / reference file layer，不再默认 reviewer 自己去猜项目约定。

### Priority 3: Add flow completeness as a top-level review dimension

对 user/admin 多步流程给出单独 verdict，不能被总体 criteria pass rate 稀释。

### Priority 4: Upgrade verification-gate from evidence presence to evidence strength

把 "What evidence exists?" 提升成 "Why does this evidence prove the claim?"

### Priority 5: Treat low-friction transparency as product scope

让 Harnessed 明确告诉开发者：规则来源、阻断原因、缺失证据、下一步动作。

## Bottom Line

如果只选一条最值得继续押注的主线，我会选：

**把 repo 里的隐式约束提取出来，变成 agent 可执行、可验证、可审计的 contract + policy substrate。**

这条线同时连接了：

- contract extraction
- repo-specific policy
- verification quality
- enterprise governance
- developer trust

这也最符合 Harnessed 现在已经在 benchmark 里显现出来的真实优势。

# Harnessed：把 AI 编程从高波动流程变成可治理的工程系统

## 问题

AI 编程代理的问题，已经不只是原始能力不够。强模型经常能在第一轮写出可用代码，真正持续存在的问题是结果波动很大：隐含需求没有被显式化，跨文件约定容易漂移，代理在证据不足时就宣布完成。

这不只是提示词问题。研究表明，LLM 存在**自偏好偏差**：当被要求评判输出时，它们会偏好与自己风格相似的回答，而不一定偏好实际质量更高的回答 [1][2]。在编程场景下，这意味着一个写了代码又审查自己代码的代理，在结构上就偏向于得出"代码是正确的"这一结论。但自评偏差只是更大问题的一部分：如果约束没有被显式写出来、审查强度没有按风险分层、完成声明没有基于证据，那么交付质量就会持续高波动。

后果是具体的：
- 代理在需求不完整时就声明任务"完成"
- 跨文件实现逐渐偏离项目真实约定
- 隐性遗漏要到人工审查或后续返工时才暴露
- 因为发现问题太晚，返工成本上升

Harnessed 的目标就是降低这种波动。它把隐含需求变成显式验收标准，把完成判断建立在证据上，并且只在风险值得时才升级审查强度。它不是在宣称 AI 编程突然变得更聪明，而是在把 AI 编程变成更可验证、更可追踪、更可升级、也更可治理的工程流程。

---

## 早期 Benchmark 给出的实际信号

当前 benchmark 数据说明，Harnessed 相比强基线确实有提升，但这不是那种可以表述成"智力跃迁"的提升：

- 端到端任务质量从 **31/37（83.8%）** 提升到 **33/37（89.2%）**
- Bug 注入测试从 **平均 6.5/10** 提升到 **平均 7.5/10**
- 代码库一致性测试从 **8/10** 提升到 **9/10**

这些数据更适合被解释为：Harnessed 更稳定地补上了隐含校验和异常处理，更稳定地把实现拉回项目既有约定，也更不容易让遗漏需求悄悄混进交付物。真正的价值是降低交付波动，而不是宣称底层模型在所有编程任务上都明显更强。

---

## 核心机制及其证据基础

### 1. 独立评估（生成者与审查者分离）

**问题：** 自评估是有偏差的。写代码的模型不能可靠地评判自己的代码。

**证据：**
- LLM 会系统性偏好自己的输出，甚至能识别哪些输出是自己的 [1][2]
- 与生成器分离的专用评估模型，产生的判断与人工评估更一致 [5][7]
- Anthropic 的生产指南将评估器-优化器模式——由单独的评估器对生成器的工作评分——确定为有效编程代理的核心架构 [11]

**Harnessed 的方案：** QA 评估器作为隔离的子代理运行。它只看到代码 diff、验收合约和项目上下文。它永远看不到生成器的推理、自我评估或对话历史。这个信息壁垒是独立判断的基础。

**诚实边界：** 独立评估器也有偏差 [5]。Harnessed 降低自评偏差；它不消除所有偏差。Confidence 和 Uncertainty 是每份 QA 报告的一等输出。

---

### 2. 合约驱动开发（编码前的显式验收标准）

**问题：** 当验收标准是隐含的，生成器和评估器都在基于假设工作。生成器构建它认为正确的东西；评估器检查它认为被要求的东西。两者都可能不匹配用户的实际需求。

**证据：**
- CodeT 证明，在代码旁生成显式测试，然后用这些测试筛选候选方案，能显著提升代码选择质量 [9]
- AlphaCodium 表明，具有显式规格理解、测试推理和迭代验证的多阶段流程优于单次生成 [10]
- 竞赛级评估研究确认，外部的、可执行的、标准化的评价标准比模型互评更可靠 [12]

**Harnessed 的方案：** 在写任何代码之前，先生成一份可测试的合约：显式的验收标准，每一条都可独立验证，每一条都是原子的和明确的。起草后，每个用户需求都映射到至少一条标准，遗漏会被补充。评估器按这份合约评分——而不是按它自己对任务的理解。

**诚实边界：** 合约的质量取决于起草时对需求的理解。如果用户意图模糊且合约未能捕获，下游验证会很精确但可能偏离真正需求。对于大型任务，Harnessed 要求用户在编码前明确审查合约。

---

### 3. 基于证据的验证门（证明，而非断言）

**问题：** 代理经常在没有证据的情况下声称完成。"我正确实现了它"是断言，不是证据。

**证据：**
- Anthropic 的代理设计指南强调，编程代理在依赖可验证的外部证据——工具输出、测试结果、执行跟踪——而非自报告的信心时，效果最好 [11]
- 更广泛的 LLM-as-judge 文献表明，带有显式评分标准的结构化评估产生更可靠和一致的判断 [6][7]

**Harnessed 的方案：** 验证门要求每个可自动化标准都有具体证据：file:line 引用、测试名称、命令输出或 HTTP 响应数据。评估器的 QA 确认是补充上下文，不是主要证据。自审查笔记是背景信息，永远不是证据。在门通过之前，不允许发出任何完成信号。

**诚实边界：** 基于证据的验证对代码可验证需求效果好。对于需要人工判断的标准（视觉设计、UX 感受、复杂交互模式），门会诚实地标记为待人工复核，而不是伪造自动化证据。

---

### 4. 多评估器审查（高风险工作的交叉验证）

**问题：** 单个评估器，即使是独立的，也可能遗漏问题或有自己的盲点。

**证据：**
- ChatEval 证明，多个评估器辩论和交叉检查产生的判断比单个评估器更稳定、更接近人工评估 [13]
- MetaGPT 表明，将角色分离和中间验证编码到多代理工作流中可以减少级联幻觉 [14]

**Harnessed 的方案：** 标准任务使用单个主评估器。高风险任务（认证、安全、支付、破坏性操作、公开端点）升级为交叉审查，有第二个独立评估器。安全敏感任务增加专用安全审查器。当评估器之间存在实质性分歧时，tie-break 审查器解决冲突。如果 tie-break 仍无法解决，问题升级给用户。

**诚实边界：** 更多评估器增加成本和延迟。多评估器路径仅用于高风险工作，因为在这些场景下遗漏问题的代价超过额外审查时间的代价。

---

### 5. 风险分级和校准治理

**问题：** 并非所有任务风险相同，但代理通常施加统一的（通常不足的）审查。此外，评估器可能随时间漂移而无人察觉。

**证据：**
- 工业代码审查研究表明 AI 审查增加价值但也增加周期时间和摩擦 [16][17]。对每个任务施加最大摩擦会产生采纳阻力。
- LLM-as-judge 文献记录了评估模型中的位置偏差、长度偏差和自增强偏差 [5]。没有校准，这些偏差会默默累积。

**Harnessed 的方案：** 任务根据涉及的内容（认证、加密、支付、隐私、破坏性操作、公开端点、生产配置）分为标准或高风险。高风险任务触发扩展审查路径。校准状态（current、stale 或 missing）被显式跟踪。当高风险任务的校准过时或缺失时，最好的自动化结果是 SHIP_WITH_HUMAN_REVIEW，不是完整的 SHIP——系统拒绝表达超出其校准支撑的信心。

**诚实边界：** 风险分级是启发式的。代理可能错误分类任务。用户可以双向覆盖分类。

---

### 6. 安全审查（启发式标记，而非审计）

**问题：** 安全漏洞需要 LLM 难以一致展现的对抗性思维。

**证据：**
- "To Err is Machine" 证明 LLM 在检测细微安全漏洞方面不可靠，尤其面对细微语义差异时 [18]
- CYBERSECEVAL 3 提供系统性基准测试，表明模型安全能力真实但有限且不一致 [19]

**Harnessed 的方案：** 安全审查定位为**安全问题标记/启发式审查**，明确不是完整的安全审计。专用安全审查器标记高信号模式（未转义输入、字符串拼接查询、缺失认证检查、代码中的密钥、不安全默认值）。当静态分析工具（Semgrep、CodeQL、bandit）可用时，其输出被视为强证据。当这些工具不可用时，系统明确记录限制并降低确定性。

**诚实边界：** 没有发现安全问题绝不等于代码是安全的。对于安全关键工作，Harnessed 的安全审查是补充——而非替代——专家人工安全审查。

---

### 7. 注入缓解（提示层，而非系统层）

**问题：** 评估器接收不可信数据（代码 diff、合约），这些可能包含提示注入尝试。

**证据：**
- 间接提示注入是 LLM 集成应用的已记录攻击向量 [20]
- 指令层级论文表明，训练模型区分特权和非特权指令可提高鲁棒性 [22]
- IsolateGPT 认为仅靠提示层防御不够，高保证场景需要系统级隔离 [23]
- Simon Willison 的实践分析确认分隔符和标记有帮助但不是安全边界 [24]

**Harnessed 的方案：** 合约和 diff 被标记为不可信任务产物，附有明确警告，声明其中嵌入的任何指令都是惰性数据。这是**提示层缓解**——有帮助，但不是完整的安全边界。对于高风险审查路径，架构包括系统级隔离、工具允许列表和显式的可信/不可信上下文分区。

**诚实边界：** 提示层缓解降低但不消除注入风险。Harnessed 不声称解决了提示注入；它施加合理的防御并明确承认限制。

---

### 8. 自我批评的正确定位（有用但不充分）

**问题：** 一些框架完全否定自我批评。另一些完全依赖它。两者都是错的。

**证据：**
- Self-Refine 证明迭代自我反馈确实在很多任务上改善了输出 [3]
- Reflexion 表明将自我反思与外部环境反馈结合的代理可以从错误中学习 [4]
- 然而，自偏好偏差文献 [1][2] 表明，自评估即使在局部有用时也是系统性有偏的

**Harnessed 的方案：** 自我批评被正确定位为有用的准备——它可以在独立审查前改善草稿。但它永远不被视为独立验证，不能作为验证门的证据。反合理化规则明确表述："自审查是有用的准备，但它仍然是有偏的，因为你知道自己打算构建什么。"

**诚实边界：** 这是定位选择，不是技术强制。代理被指示维护这一区分，但它依赖提示纪律而非系统强制。

---

## Harnessed 是什么和不是什么

### Harnessed 是：
- 一个降低 AI 编程波动的工程治理系统
- 一个具有显式验收标准、独立评估和基于证据门控的结构化执行与 QA 流程
- 一个减少遗漏需求、约定漂移和后期返工的机制
- 一个按风险施加比例审查、并对不确定性保持诚实的系统

### Harnessed 不是：
- 一个让所有模型都显著变聪明的"智力外挂"
- 代码正确性的保证
- 关键系统人工安全审查的替代品
- 零评估器偏差的系统
- 提示注入的完整防御
- 全面测试套件的替代品

Harnessed 的价值，不在于让 AI 编程完美，甚至也不在于让每个 benchmark 都出现巨大分差。它真正的价值在于把 AI 编程变成一个更**可验证、可追踪、可升级、可治理**的工程系统：有显式标准、独立审查、具体证据、诚实的不确定性报告，以及清晰的人机升级边界。

---

## 参考文献

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

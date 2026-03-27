# Review Changelog

138 improvements across 16 review rounds. Each entry documents an issue found and fixed during iterative subagent-driven review.

## Why We Did This

Harnessed 的核心主张是：AI 不能可靠地评估自己的工作。这个主张如果要有说服力，Harnessed 自身的质量必须经得起独立审查。

我们用 Harnessed 倡导的同一种方法来审查 Harnessed 本身——派遣独立的 Opus 4.6 子代理，从不同角度审查代码和设计，每一轮都不知道上一轮的结论。这不是自我检查，而是用隔离的评估者反复验证同一套代码。

### 审查带来了什么

**可靠性：** 修复了 2 个会导致管线卡死的数据流缺陷（迭代计数被覆写、MANUAL_REVIEW_NEEDED 死锁），以及 7 个在特定条件下会静默失败的边界情况（合并冲突、并发会话、Hook 输出损坏等）。这些问题在日常使用中不一定触发，但一旦触发就是无声的失败——最危险的那种 bug。

**一致性：** 消除了 16 处设计文档与实际实现之间的偏差。Spec 说的是一套流程，代码做的是另一套。对于一个依赖精确指令驱动 LLM 行为的插件来说，文档和实现不一致意味着 LLM 可能按照错误的流程执行。

**完整性：** 补全了互补模式（Superpowers 共存）下的数据流——原来验证门和 QA 评估器读取的是不同的合约来源，现在统一为 `.harnessed/contract.md`。补全了上下文预算、二进制文件处理、非 Git 仓库回退等实际使用中会遇到的场景。

**可用性：** 重写了安装说明（分 A/B 路径、验证步骤），增加了故障排查和自定义章节。一个用户装不上的工具，质量再好也没有意义。

**可扩展性：** 提前埋入 `{MODE}` 占位符、`contract-format.md` 单一事实来源、`qa-state.md` 状态持久化。这些不改变当前行为，但让 v1.0 路线图上的功能（优先级分级、逐条评估、配置文件）从"需要重构"变成"直接插入"。

### 审查方法论

| 轮次 | 角度 | 核心问题 |
|------|------|----------|
| 1 | 结构 | 插件能被 Claude Code 正确发现和加载吗？ |
| 2 | 功能 | 每个 Skill 的指令是否完整、无遗漏？ |
| 3 | 模拟 | 真实使用场景下会遇到什么问题？ |
| 4 | 竞品 | 和 Superpowers / Cursor Rules / Aider 比有什么差距？ |
| 5 | 威胁 | 架构层面有哪些可以被利用或绕过的弱点？ |
| 6 | 语义 | 指令的措辞是否会导致 LLM 产生偏差行为？ |
| 7 | 边界 | 异常状态（压缩、崩溃、并发）下数据流是否完整？ |
| 8 | 漂移 | 文档还能准确描述实际行为吗？ |
| 9 | 收尾 | 所有已知问题是否全部解决？ |
| 10 | 验证强化 | 无测试项目的执行验证是否完备？ |
| 11 | 评估器扩展 | 安全、类型、陈旧性等维度是否覆盖？ |
| 12 | 验证门与文档同步 | 验证门流程和文档是否一致？ |
| 13 | 边界情况与引用同步 | 非 Git、空 diff、用户覆写等边界是否处理？ |
| 14 | 会话钩子与状态整合 | 钩子可靠性和迭代状态是否健壮？ |
| 15 | 评估器模板与评分 | Tier 1.5 输出结构和评分优先级是否完整？ |
| 16 | 防篡改与文档同步 | QA 轮次间的合约完整性和文档一致性是否保障？ |

每一轮都由独立的子代理执行，不携带上一轮的上下文。这和 Harnessed 对用户代码做的事情完全一样：独立评估，每一轮都是新鲜的视角。

---

## Round 1: Structural Review

| # | Issue | Fix |
|---|-------|-----|
| 1 | hooks/ directory inside .claude-plugin/ (wrong location) | Moved to plugin root |
| 2 | hooks.json used flat array format instead of three-level nesting | Rewritten to matcher/hooks/type format |
| 3 | plugin.json author as bare string | Changed to object `{"name": "Harnessed"}` |
| 4 | Hook output missing hookEventName field | Added `"hookEventName": "SessionStart"` |
| 5 | session-start fallback path wrong (../../ instead of ../) | Fixed relative path |
| 6 | All 4 SKILL.md descriptions contained workflow summaries (CSO violation) | Trimmed to triggering conditions only |
| 7 | Meta-skill too large (~800 words) for session injection | Moved detail to reference.md, reduced to ~648 words |

## Round 2: Functional Review

| # | Issue | Fix |
|---|-------|-----|
| 8 | Contract-writing missing minimum criterion rule | Added: every contract must have at least 1 criterion |
| 9 | Independent-qa missing empty diff handling | Added: STOP if git diff produces no output |
| 10 | Independent-qa missing non-git repo handling | Added: collect full file contents as fallback |
| 11 | Verification-gate missing micro task path | Added: lighter verification for micro tasks |
| 12 | Evaluator prompt missing MANUAL_REVIEW_NEEDED grade | Added as per-criterion grade option |
| 13 | No guidance for handling requirement changes mid-task | Added: update contract, re-run QA |
| 14 | Grading rubric missing concrete examples | Added examples for each grade level |

## Round 3: Usage Simulation

| # | Issue | Fix |
|---|-------|-----|
| 15 | Meta-skill lacks artifact lifecycle management | Added: archive stale artifacts on new task |
| 16 | No task disambiguation (new vs continuation) | Added: ask user when ambiguous |
| 17 | Missing timestamp format for archive files | Specified: YYYYMMDD-HHMMSS |
| 18 | Evaluator could see generator reasoning via conversation context | Strengthened context isolation instructions |
| 19 | No guidance for committed-but-not-diffable changes | Added: suggest `git diff HEAD~1` |
| 20 | Contract-writing missing refactor classification guidance | Clarified: refactors need regression criteria |
| 21 | Verification-gate Step 3 gap checklist incomplete | Added: check for unresolved ITERATE/BLOCKED |

## Round 4: Competitive Analysis (vs Superpowers, Cursor Rules, Aider)

| # | Issue | Fix |
|---|-------|-----|
| 22 | README lacked compelling value proposition | Rewrote with statistics and pipeline diagram |
| 23 | No example QA report in README | Added realistic localStorage key mismatch example |
| 24 | Installation instructions incomplete | Added git clone + cp + chmod steps |
| 25 | No .gitignore for .harnessed/ artifacts | Created .gitignore + documented in README |
| 26 | Missing LICENSE file | Added MIT license |
| 27 | No cost estimate for users | Added: ~1.5x token usage section |
| 28 | Design principles not articulated | Added 4 principles (Verification > Process, etc.) |
| 29 | Skills table missing from README | Added with invocation and purpose columns |
| 30 | Complementary mode explanation unclear in README | Added dedicated section |

## Round 5: Architectural Threat Model

| # | Issue | Fix |
|---|-------|-----|
| 31 | "Execution result wins" rule dangerous (shared assumptions) | Changed to asymmetric rule: execution FAIL wins, but PASS doesn't dismiss code review |
| 32 | No pre-flight checks before expensive evaluator dispatch | Added Step 2b: run linter/type-check/tests first |
| 33 | Subagent permissions wrong (read+execute, missing write) | Fixed to read, write, and execute |
| 34 | Priority hierarchy vs HARD-GATE contradiction | Clarified: HARD-GATEs prevent agent rationalization, not user override |
| 35 | Contract gaming risk undocumented | Documented in roadmap: contract review step planned |
| 36 | Same-model blind spots undocumented | Documented in roadmap: cross-model eval planned |
| 37 | Evaluator attention ceiling undocumented | Documented as known inherent limitation |
| 38 | No roadmap for future improvements | Created docs/roadmap-v1.md |
| 39 | Config values hardcoded with no override path | Documented in roadmap: config file planned |
| 40 | No security checklist for auth/input criteria | Documented in roadmap: security addendum planned |

## Round 6: Deep Semantic Review (Opus 4.6)

| # | Issue | Fix |
|---|-------|-----|
| 41 | Evaluator framed as "skeptical engineer" (negativity bias) | Reframed as "independent code auditor" (evidence-based) |
| 42 | Asymmetric execution rule described in prose (hard to parse) | Reformatted as table |
| 43 | No quality constraint on evaluator output | Added: each finding must be detailed enough for unfamiliar developer |
| 44 | Anti-rationalization missing "impatient user" pattern | Added: "User impatience is about communication, not quality" |
| 45 | Anti-rationalization missing "second attempt" pattern | Added: "Knowing the previous failure doesn't guarantee the fix is correct" |
| 46 | Anti-rationalization missing "no tests" pattern | Added: "Tier 1 code review alone catches logic errors" |
| 47 | Contract-writing missing requirement changes section | Added: update contract, assess existing code, re-run QA |
| 48 | Contract-writing missing refactor classification | Added: "Refactors have the strictest contract: behavior must be IDENTICAL" |
| 49 | Grading rubric PASS lacked concrete example | Added: API 404 check example |
| 50 | Grading rubric PARTIAL lacked concrete example | Added: case-insensitive search Unicode example |
| 51 | Grading rubric FAIL lacked concrete example | Added: plaintext password storage example |
| 52 | Grading rubric MANUAL_REVIEW_NEEDED lacked concrete example | Added: dark mode visual consistency example |
| 53 | SHIP grade definition did not exclude MANUAL_REVIEW_NEEDED | Added: "Criteria graded MANUAL_REVIEW_NEEDED are excluded from this count" |
| 54 | Evaluator prompt "cut corners" phrase not in implementation | Removed from spec (spec drift, fixed in Round 8) |
| 55 | Missing iteration count persistence guidance | Added to SKILL.md (improved in Round 7) |
| 56 | Contract format embedded inline (no single source of truth) | Extracted in Round 9 |
| 57 | Context budget heuristic vague | Clarified in Round 9 |
| 58 | Evaluator timeout/token limits unaddressed | Addressed via Step 4b retry mechanism |

## Round 7: Lifecycle Edge Cases, Data Flow, Extensibility

| # | Issue | Fix |
|---|-------|-----|
| 59 | **[BROKEN]** Iteration count appended to qa-report.md, overwritten by evaluator | Created separate `.harnessed/qa-state.md` for persistence |
| 60 | **[BROKEN]** MANUAL_REVIEW_NEEDED criteria block verification-gate (deadlock) | Added exception: listed under "Pending Human Review" section |
| 61 | Complementary mode: verification-gate reads raw spec, evaluator gets normalized contract | Both now read from `.harnessed/contract.md` in all modes |
| 62 | {VERIFICATION_COMMANDS} empty in complementary mode | Synthesis instructions now require generating verification commands |
| 63 | Git diff command ambiguous ("staged + unstaged" but no exact command) | Specified `git diff HEAD` throughout |
| 64 | qa-report.md staleness check prescribed but mechanism undefined | Defined: compare file mtime against `dispatched_at` in qa-state.md |
| 65 | Concurrent sessions clobber `.harnessed/` artifacts silently | Documented as unsupported in README and reference.md |
| 66 | Hook silent failure (exits 0 with garbage JSON, agent unaware) | Added output validation before JSON emission |
| 67 | No merge conflict detection before QA dispatch | Added Step 2c: check `.git/MERGE_HEAD` |
| 68 | {MODE} placeholder missing for future per-criterion evaluation | Added to evaluator-prompt.md and SKILL.md placeholder list |
| 69 | Contract format duplicated (inline in SKILL.md, no single source) | Created `contract-format.md` as standalone reference |
| 70 | Verification-gate summary template missing "Pending Human Review" section | Added section for MANUAL_REVIEW_NEEDED criteria |
| 71 | qa-state.md missing from artifact directory listings | Added to README.md and reference.md |
| 72 | Concurrent sessions note missing from reference.md | Added alongside directory listing |

## Round 8: Spec Drift + Developer Experience

### Spec.md sync (16 drifts)

| # | Issue | Fix |
|---|-------|-----|
| 73 | qa-state.md missing from File Communication Protocol table | Added row |
| 74 | qa-report.md author ambiguous ("independent-qa" vs evaluator subagent) | Clarified: "evaluator subagent (dispatched by independent-qa)" |
| 75 | Iteration mechanism describes wrong persistence (qa-report.md not qa-state.md) | Updated with qa-state.md format and compaction-survival rationale |
| 76 | Evaluator persona: spec says "skeptical senior engineer", implementation says "code auditor" | Updated spec to "independent code auditor" |
| 77 | Spec quotes nonexistent evaluator text ("cut corners") | Updated to actual text |
| 78 | Tier 2 indicators incomplete (missing go.mod, tests/ dir, specific ports) | Added all indicators with commands |
| 79 | Complementary mode flow wrong (spec says skip contract.md, impl writes it) | Updated to reflect contract.md written in both modes |
| 80 | Pre-flight checks (Step 2b) not in spec | Added section |
| 81 | Git state checks (Step 2c) not in spec | Added section |
| 82 | Evaluator output verification (Step 4b) not in spec | Added section |
| 83 | Context budget management not in spec | Added ~80K token budget with fallback strategies |
| 84 | Non-git repository handling not in spec | Added fallback description |
| 85 | Artifact lifecycle (archiving) not in spec | Added section |
| 86 | MANUAL_REVIEW_NEEDED effect on overall grade not described | Added: excluded from count, does not block SHIP |
| 87 | contract-format.md missing from plugin structure tree | Added to tree |
| 88 | Hook matcher, Cursor support, "priority tags" claim inaccurate | Updated loading mechanism section |

### README DX improvements

| # | Issue | Fix |
|---|-------|-----|
| 89 | "What It Does" preamble repeats "Why" section | Tightened to one-line lead-in |
| 90 | Installation as single cp command, no verification step | Restructured: Option A/B, numbered post-install steps |
| 91 | .gitignore step easy to miss (afterthought paragraph) | Made numbered installation step |
| 92 | No way to verify installation worked | Added: `bash harnessed/hooks/session-start` verification |
| 93 | chmod instruction on wrong path + redundant after git clone | Moved to blockquote note for zip downloads only |
| 94 | No documentation on how to opt out of QA | Added Customization section (skip QA, skip contract, disable entirely) |
| 95 | No troubleshooting section | Added: 4 common failure modes with solutions |
| 96 | Artifacts tree missing archive/ subdirectory | Added to tree |

## Round 9: Final Polish

| # | Issue | Fix |
|---|-------|-----|
| 97 | No guidance for binary files in git diff (non-diffable assets) | Added: note binary changes to evaluator, mark as MANUAL_REVIEW_NEEDED |
| 98 | "Iron Law" terminology in spec.md/plan.md, "HARD-GATE" in skill files | Unified to HARD-GATE across all files |
| 99 | Orchestrator notes section ambiguous (might be sent to evaluator) | Added bold note: "Do NOT send to evaluator subagent" |
| 100 | `lsof` not available on all Linux distros | Added `ss -tlnp` as Linux alternative |
| 101 | "Auto-generated files" in context budget vague | Added concrete examples (lock files, minified, dist/, build/, API clients) |
| 102 | qa-state.md not included in artifact archival lifecycle | Added as step 3 in archive sequence |

## Round 10: Verification Hardening

| # | Issue | Fix |
|---|-------|-----|
| 103 | Projects with dev server but no test suite skip execution verification entirely | Added Tier 1.5 HTTP smoke tests (start server, hit key endpoints, check status codes) |
| 104 | Failure patterns not learned across sessions (same mistakes repeat) | Added project-level learning via `.harnessed/failure-patterns.md` with decay rule |
| 105 | Contract-writing has no step to verify coverage of implementation surface | Added coverage verification step (6b) in contract-writing |

## Round 11: Evaluator & Spec Expansion

| # | Issue | Fix |
|---|-------|-----|
| 106 | Evaluator Tier 1 code review missing security-specific checks | Added security checklist (XSS, SQL injection, auth bypass, secrets exposure) |
| 107 | TypeScript compilation errors conflated with runtime errors in evaluator guidance | Added explicit TypeScript compilation vs runtime error discrimination guidance |
| 108 | No mechanism to detect stale qa-state.md against current code | Added code staleness check (`head_commit` field in qa-state.md) |
| 109 | Evaluator penalizes bugs that existed before the current task | Added pre-existing bugs discrimination rule in evaluator mindset |
| 110 | Projects using Superpowers with no spec have no fallback for contract synthesis | Added Superpowers fallback for missing specs |
| 111 | Tier 1.5 execution result treated symmetrically (PASS and FAIL weighted equally) | Added Tier 1.5 asymmetric execution rule (FAIL wins, PASS is informational) |
| 112 | spec.md out of sync with Round 10–11 features | Synced spec.md with all new features |

## Round 12: Verification Gate & Documentation Sync

| # | Issue | Fix |
|---|-------|-----|
| 113 | Staleness check buried inside verification-gate flow (easy to skip) | Promoted verification-gate staleness check to explicit Step 0 |
| 114 | Evaluator subagent filesystem access not clearly stated | Clarified evaluator subagent has full filesystem access |
| 115 | README.md missing three-tier verification, failure patterns, and workflow updates | Synced README.md with three-tier verification, failure patterns, workflows |
| 116 | README.zh-CN.md diverged from English README | Synced README.zh-CN.md with same changes |

## Round 13: Edge Cases & Reference Sync

| # | Issue | Fix |
|---|-------|-----|
| 117 | Verification-gate Step 0 staleness check fails on non-git projects | Fixed: skip staleness check for non-git projects |
| 118 | Empty diff produces confusing evaluator output with no recovery | Added empty diff recovery path (offer `git diff HEAD~1`) |
| 119 | HARD-GATE wording implies user cannot override (contradicts design intent) | Added explicit user override clause in HARD-GATE |
| 120 | reference.md missing all Round 10–12 features | Updated reference.md with all new features |
| 121 | contract-format.md complementary mode synthesis rules incomplete | Expanded contract-format.md complementary mode synthesis rules |

## Round 14: Session Hook, Iteration State & Consolidation

| # | Issue | Fix |
|---|-------|-----|
| 122 | Session-start hook sed fallback breaks on BSD/macOS (silent failure) | Rewrote session-start hook: replaced broken sed fallback with perl chain, printf over heredoc |
| 123 | Iteration state transitions described in prose (ambiguous for LLM execution) | Added 5-step iteration state management pseudocode |
| 124 | Independent-qa has no pointer to contract-format.md (readers miss format rules) | Added cross-reference to contract-format.md from independent-qa |
| 125 | Contract-writing criteria rules lack guidance for MANUAL_REVIEW_NEEDED outcomes | Added MANUAL_REVIEW_NEEDED guidance to contract-writing criteria rules |
| 126 | Superpowers detection logic scattered across multiple files | Consolidated Superpowers detection into canonical 3-step algorithm in spec |
| 127 | Roadmap items implemented but not marked | Marked 3 roadmap items as PARTIALLY IMPLEMENTED |

## Round 15: Evaluator Template, Grading & Reference Sync

| # | Issue | Fix |
|---|-------|-----|
| 128 | Evaluator output template missing Tier 1.5 in Verification Tier field | Added Tier 1.5 as a valid value in the Verification Tier field |
| 129 | Evaluator output template has no section for Tier 1.5 execution results | Added HTTP Smoke Tests subsection for Tier 1.5 execution results |
| 130 | Evaluator output template {Y} in Criteria Passed ambiguous (could include MANUAL_REVIEW_NEEDED) | Clarified: {Y} excludes criteria graded MANUAL_REVIEW_NEEDED |
| 131 | Grading rubric lacks severity precedence rule (BLOCKED vs ITERATE vs SHIP ordering) | Added rule 6: severity precedence BLOCKED > ITERATE > SHIP |
| 132 | reference.md Tier 1 described as "Static analysis" (wrong) and listed phantom Tier 3 | Fixed Tier 1 description to "Code review"; removed phantom Tier 3 |
| 133 | Both READMEs: SHIP/ITERATE/BLOCKED grades undefined inline; failure-patterns.md absent from EN artifact tree; ZH README missing English link | Added inline SHIP/ITERATE/BLOCKED definitions; added failure-patterns.md to EN artifact tree; added English README link to ZH README |

## Round 16: Tamper Detection, Stale References & Spec Sync

| # | Issue | Fix |
|---|-------|-----|
| 134 | independent-qa has no tamper detection between QA rounds (contract could be silently modified) | Added contract_hash field to qa-state.md; independent-qa now records and verifies hash on each round |
| 135 | independent-qa still contains two stale "1 or 2" tier references (should be "1, 1.5, or 2") | Fixed both remaining stale references to reflect the three-tier system |
| 136 | contract-writing MUST NOT list contains duplicate subjective quality entries | Merged duplicate subjective entries into a single consolidated rule |
| 137 | README.md Tier 2 description incorrectly included "dev servers" (Tier 1.5 only) | Fixed Tier 2 description: removed "dev servers", now correctly scoped to Tier 1.5 |
| 138 | spec.md missing grading precedence rule, iteration algorithm not synced to 6-step, qa-state.md absent from artifact lifecycle | Added grading precedence rule; synced iteration algorithm to 6-step with contract_hash; added qa-state.md to artifact lifecycle section |

---

## Summary by Category

| Category | Count |
|----------|-------|
| Data flow / state management fixes | 15 |
| Edge case handling | 18 |
| Anti-rationalization patterns | 7 |
| Spec/docs sync | 25 |
| Developer experience | 13 |
| Evaluator quality | 14 |
| Plugin structure / hooks | 10 |
| Contract/grading system | 13 |
| Competitive / positioning | 8 |
| Verification hardening | 4 |
| Evaluator template & grading | 6 |
| Tamper detection & spec sync | 5 |
| **Total** | **138** |

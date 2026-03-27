# Harnessed

[English](README.md)

AI 编程代理的独立质量验证。代码未经隔离评估器确认，就不算完成。

## 为什么需要

AI 编程代理会自己评估自己的工作——然后经常判断失误。研究表明，自我评估与独立评估有 31% 的分歧率，AI 生成的代码在全面测试中仅有 42% 的首次通过率。解决方法很简单：不要让写代码的那个代理来评判代码。

## 做了什么

Harnessed 为 AI 编程工作流添加独立 QA 循环：

```
独立模式：     任务 → 合约 → 编码 → 独立 QA → 修复循环 → 验证门 → 完成
互补模式(SP)： 任务 → SP 规划 → 编码 → 独立 QA → 修复循环 → 验证门 → 完成
微任务：       任务 → 编码 → 验证门 → 完成
```

- **合约编写** — 编码前生成可测试的验收标准。起草完成后，系统会将每个用户需求映射到至少一条标准，补充遗漏。
- **独立 QA** — 隔离的评估子代理按合约逐条评分
- **验证门** — 需要结构化证据（file:line 引用）才能声明"完成"。验证门会检查 QA 之后代码是否发生变化，如果变了则重新运行 QA。

## 安装

### Claude Code（插件市场 — 推荐）

```bash
# 注册 Harnessed 市场（一次性）
claude plugin marketplace add tt-a1i/harnessed

# 安装插件
claude plugin install harnessed
```

更新自动完成 — Claude Code 启动时自动同步插件。

### 手动安装（备选）

```bash
# 克隆仓库
git clone https://github.com/tt-a1i/harnessed.git

# 方式 A：作为项目插件安装（仅当前项目）
cp -r harnessed/ your-project/harnessed/

# 方式 B：全局安装（所有项目可用）
cp -r harnessed/ ~/.claude/plugins/harnessed/
```

> 如果下载的是 zip 而非 git clone，请运行 `chmod +x harnessed/hooks/session-start`。

### 安装后

1. 将 `.harnessed/` 添加到项目的 `.gitignore` — Harnessed 会在此写入 QA 产物
2. 验证：启动新的 Claude Code 会话 — 第一次编码任务时应看到 Harnessed 提示"I'll draft acceptance criteria before coding"

### 与 Superpowers 配合使用

Harnessed 自动检测 Superpowers。两者同时安装时：

- Superpowers 负责规划、TDD 和流程纪律
- Harnessed 负责独立 QA 和验证
- 无重复、无冲突

两者同时安装时，Harnessed QA 在 Superpowers 流程完成后运行。如果检测到 Superpowers 但没有 spec 文件，Harnessed 回退到独立模式。

## 工作原理

### 独立模式（无 Superpowers）

1. 你给出一个编码任务
2. **合约编写** 生成可测试的验收标准 → `.harnessed/contract.md`
3. 代理编写代码
4. **独立 QA** 派遣隔离的评估子代理
   - 评估器看到：diff + 合约 + 项目上下文
   - 评估器看不到：生成器的推理过程或自我评估
   - 评估器对每条标准评分：PASS / FAIL / PARTIAL / MANUAL_REVIEW_NEEDED
   - 总体评级：**SHIP**（全部通过，可以完成）/ **ITERATE**（发现问题，代理修复后重跑 QA）/ **BLOCKED**（根本性问题，需要你介入）
5. 如果 ITERATE：代理修复问题，QA 重新运行（最多 3 轮）
6. 如果 SHIP：**验证门** 收集每条标准的 file:line 证据
7. 任务完成，附完整审计记录

### 互补模式（与 Superpowers 配合）

与上述相同，但跳过合约编写（使用 Superpowers 的规格说明代替）。

### 三层验证

- **Tier 1（代码审查）** — 始终可用。评估器阅读 diff 并检查标准。
- **Tier 1.5（HTTP 冒烟测试）** — 当检测到开发服务器运行但没有测试套件时自动激活。评估器使用 curl/HTTP 请求对实时服务器验证行为。
- **Tier 2（执行验证）** — 检测到测试框架时自动启用。评估器运行测试并与应用交互。

### 项目级学习

- `.harnessed/failure-patterns.md` 跨任务追踪复现的失败类别
- 编写合约时，出现次数 ≥ 2 的模式会被用来指导验收标准
- 单次出现的模式 90 天后自动清理

## QA 报告示例

独立 QA 运行后，Harnessed 在 `.harnessed/qa-report.md` 生成结构化报告：

```markdown
# QA Report

## Overview
- **Verification Tier:** 2
- **Overall Grade:** ITERATE
- **Criteria Passed:** 7/9
- **Critical Issues:** 0

## Per-Criterion Evaluation

### Criterion: "选中的主题在页面刷新后保持不变"
- **Grade:** FAIL
- **Evidence:** src/hooks/useTheme.ts:24 — 调用了 localStorage.setItem，但第 8 行的 getItem 读取了错误的 key（"theme" vs "color-theme"）
- **Finding:** 主题偏好以 "color-theme" 为 key 写入 localStorage，但以 "theme" 为 key 读回，因此永远无法持久化。
- **Action Required:** 统一 useTheme.ts 第 8 行和第 24 行的 localStorage key。

### Criterion: "暗色模式应用于所有 UI 元素"
- **Grade:** PARTIAL
- **Evidence:** src/components/Header.tsx:15 — className 不包含 theme 变量
- **Finding:** Header 组件未消费 theme context。暗色模式下背景仍为白色。
- **Action Required:** 在 Header.tsx 中引入并应用 theme class。
```

## 技能

| 技能 | 调用方式 | 用途 |
|------|---------|------|
| using-harnessed | 会话启动时自动加载 | 路由到其他技能，管理模式 |
| contract-writing | `harnessed:contract-writing` | 生成验收标准 |
| independent-qa | `harnessed:independent-qa` | 派遣隔离的 QA 评估器 |
| verification-gate | `harnessed:verification-gate` | 收集完成证据 |

## 产物

所有 Harnessed 产物写入项目根目录的 `.harnessed/`：

```
.harnessed/
├── contract.md              # 验收标准（两种模式均写入）
├── qa-report.md             # QA 评估报告
├── qa-state.md              # 迭代计数与派遣时间戳
├── verification-summary.md  # 完成证据
├── failure-patterns.md      # 跨任务复现的失败模式
└── archive/                 # 前次任务的归档产物
```

**注意：** 不支持在同一项目目录下运行多个 Claude Code 会话。每个会话写入同一个 `.harnessed/` 目录，无文件锁 — 产物可能被互相覆盖。

## 成本

每轮 QA 派遣一个评估子代理。典型任务使用 1-2 轮 QA。预计 token 用量约为不使用 Harnessed 时的 1.5 倍。权衡：在用户发现 bug 之前捕获它们，还是之后。

## 自定义

- **跳过某次任务的 QA：** 告诉 Claude "跳过 QA" 或 "把这个当微任务处理"
- **跳过合约：** 告诉 Claude "跳过合约，直接 QA"
- **完全禁用：** 告诉 Claude "不要运行 Harnessed" — 它会照做，但会注明验证被跳过
- Harnessed 始终尊重用户的明确指令。自动化门禁阻止的是*代理*自行跳过验证，而非用户选择跳过。

## 设计原则

1. **验证 > 流程** — 有验证结果的简单计划，胜过无验证结果的精细计划
2. **独立性 > 全面性** — 快速的独立检查比深入的自我审查捕获更多问题
3. **证据 > 断言** — "它能工作，因为 file:42 显示 X" 胜过 "它能工作，因为我写对了"
4. **怀疑 > 信任** — 默认立场是"证明它能工作"而非"假设它能工作"

## 故障排查

**Harnessed 未加载（首次任务没有生成合约）：**
- 手动运行 hook：`bash harnessed/hooks/session-start` — 应输出包含元技能的 JSON
- 如果报错，检查是否安装了 `python3`（用于 JSON 转义）
- 如果下载的是 zip，确保 hook 可执行：`chmod +x harnessed/hooks/session-start`

**QA 评估器未能生成报告：**
- 通常是评估器 prompt 过大。尝试缩小 diff 或减少标准数量。
- 重试一次后，Harnessed 将任务标记为 BLOCKED 并上报给你。

**产物出现在 git status 中：**
- 将 `.harnessed/` 添加到项目的 `.gitignore`

**并发会话：**
- 不支持在同一项目运行多个 Claude Code 会话 — 会话共享 `.harnessed/` 且无文件锁

## 许可证

MIT

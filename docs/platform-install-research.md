# Platform Installation Research

> 调研结论，尚未实际验证。验证通过后再写入各平台 README。

## Codex CLI 安装 Harnessed

### 前提
- 已安装 Codex CLI：`npm install -g @openai/codex` 或 `brew install --cask codex`
- macOS 12+ / Ubuntu 20.04+ / Windows 11 WSL2
- ChatGPT 登录或 OpenAI API key

### 安装步骤

1. 复制插件目录到项目：
```bash
mkdir -p ./plugins
cp -r platforms/codex/ ./plugins/harnessed/
```

2. 在项目根目录创建 `.agents/plugins/marketplace.json`：
```json
{
  "name": "local-repo",
  "plugins": [
    {
      "name": "harnessed",
      "source": {
        "source": "local",
        "path": "./plugins/harnessed"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

3. 启用 hooks（在 `~/.codex/config.toml` 中）：
```toml
[features]
codex_hooks = true
```

4. 重启 Codex，在 CLI 中输入 `/plugins` 确认插件已出现。

### 插件目录结构要求
```
harnessed/
├── .codex-plugin/
│   └── plugin.json      # 必须
├── skills/               # skills 由 plugin.json 指定路径
├── hooks.json            # 由 plugin.json 指定
├── agents/               # custom agents（TOML 格式）
└── ...
```

### 注意事项
- 没有 `codex plugin install` shell 命令，安装方式是目录 + marketplace.json + 重启
- hooks 仍属 experimental，Windows 当前禁用
- marketplace 支持 repo-local（`.agents/plugins/marketplace.json`）和全局（`~/.agents/plugins/marketplace.json`）
- `source.path` 必须是相对 marketplace root 的 `./...` 路径

---

## OpenCode 安装 Harnessed

### 前提
- 已安装 OpenCode：`curl -fsSL https://opencode.ai/install | bash` 或 `brew install anomalyco/tap/opencode` 或 `npm install -g opencode-ai`
- 至少一个模型提供商的 API key 或 OpenCode Zen 认证

### 安装步骤

1. 复制文件到项目目录：
```bash
cp -r platforms/opencode/.opencode/ .opencode/
cp platforms/opencode/opencode.json opencode.json
```

2. 启动 OpenCode，自动加载：
```bash
opencode
```

无需额外 install 命令，启动时自动发现。

### 全局安装（可选，所有项目可用）
```bash
cp -r platforms/opencode/.opencode/plugins/ ~/.config/opencode/plugins/
cp -r platforms/opencode/.opencode/skills/ ~/.config/opencode/skills/
cp -r platforms/opencode/.opencode/commands/ ~/.config/opencode/commands/
cp -r platforms/opencode/.opencode/agents/ ~/.config/opencode/agents/
```

### 自动发现路径（启动时按顺序加载）
1. `~/.config/opencode/opencode.json`
2. `opencode.json`（项目级）
3. `~/.config/opencode/plugins/`
4. `.opencode/plugins/`

### 各组件放置位置
| 组件 | 项目级 | 全局 |
|------|--------|------|
| Plugins | `.opencode/plugins/*.ts` | `~/.config/opencode/plugins/*.ts` |
| Skills | `.opencode/skills/<name>/SKILL.md` | `~/.config/opencode/skills/<name>/SKILL.md` |
| Commands | `.opencode/commands/*.md` | `~/.config/opencode/commands/*.md` |
| Agents | `.opencode/agents/*.md` | `~/.config/opencode/agents/*.md` |

### npm 插件方式（可选）
在 `opencode.json` 中声明：
```json
{
  "plugin": ["harnessed-opencode"]
}
```
OpenCode 启动时自动用 Bun 安装，缓存在 `~/.cache/opencode/node_modules/`。

### 外部依赖
如果插件有 npm 依赖，在 `.opencode/package.json` 中声明，OpenCode 启动时自动 `bun install`。

### 注意事项
- 没有 SessionStart additionalContext 等价机制，入口靠 plugin events + commands 组合
- Skills 兼容 `.claude/skills` 和 `.agents/skills` 路径
- Agent 通过 Markdown frontmatter 注册，文件名即 agent 名
- Windows 推荐 WSL

---

## 待验证事项

- [ ] Codex：本地 marketplace 安装后 `/plugins` 能否看到 Harnessed
- [ ] Codex：SessionStart hook 是否正常触发并注入 meta-skill
- [ ] Codex：custom agent (evaluator.toml) 是否能被调用
- [ ] OpenCode：插件 harnessed.ts 是否正常加载（session.created 事件）
- [ ] OpenCode：/harnessed-run 等 commands 是否可见可用
- [ ] OpenCode：evaluator agent 是否能作为 subagent 被调用
- [ ] 两个平台：.harnessed/ 产物是否正常生成

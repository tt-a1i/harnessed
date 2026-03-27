# Codex Adapter MVP

Codex packages Harnessed as a `.codex-plugin` bundle with skills, hooks, and optional custom agents.
This MVP keeps the core artifact protocol unchanged and mirrors the current Claude-authored workflow text while Codex-specific wording stabilizes.

## Included pieces

- `.codex-plugin/plugin.json` - plugin manifest
- `hooks.json` - SessionStart bootstrap for the meta-skill
- `skills/` - Codex skill payloads copied from the current Claude-authored workflow
- `agents/` - evaluator and support agent stubs
- `config.sample.toml` - sample feature flags for hooks and subagents

## Notes

- Codex hooks are still experimental upstream.
- The shared `.harnessed/` artifact protocol stays unchanged.
- This adapter is additive: root-level Claude files remain the compatibility surface for existing users.

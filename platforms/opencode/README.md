# OpenCode Adapter MVP

OpenCode uses a combination of plugin events, custom commands, skills, and subagents.
This MVP preserves the core artifact protocol and provides explicit workflow entrypoints while a more automated bootstrap layer evolves.

## Included pieces

- `.opencode/plugins/harnessed.ts` - startup and compaction glue
- `.opencode/skills/` - Harnessed workflow skills for OpenCode
- `.opencode/commands/` - explicit workflow entrypoints
- `.opencode/agents/` - evaluator and support subagent stubs
- `opencode.json` - minimal config shell for the adapter

## Notes

- OpenCode does not expose a direct SessionStart additionalContext equivalent, so this adapter leans on commands plus plugin events.
- The shared `.harnessed/` artifact protocol stays unchanged.
- This adapter is additive and does not change the root Claude package layout.

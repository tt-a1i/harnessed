# Multi-Platform Migration Plan

## Phase A - Core extraction
- move protocol definitions into `core/protocol/`
- move canonical prompts into `core/prompts/`
- move reusable policies into `core/rules/`
- document state machine and artifact protocol in `core/docs/`

## Phase B - Claude adapter stabilization
- mirror current Claude-facing package under `platforms/claude/`
- keep root Claude layout unchanged for existing users
- use root package as compatibility facade until generator tooling is mature

## Phase C - Codex MVP
- provide `.codex-plugin/plugin.json`
- provide `hooks.json` and SessionStart bootstrap
- provide evaluator custom agent
- provide local marketplace example

## Phase D - OpenCode MVP
- provide `.opencode/plugins/harnessed.ts`
- provide explicit workflow commands
- provide evaluator subagent definition
- use plugin events for lightweight guardrails and compaction support

## Phase E - Convergence
- add generation or sync tooling from `core/` to adapters
- replace manual copy steps with repeatable adapter rendering
- add parity tests for protocol files and prompts

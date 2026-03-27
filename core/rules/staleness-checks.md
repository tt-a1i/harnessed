# Staleness Check Rules

## Before QA dispatch
- stop on active merge conflict
- gather `git diff HEAD`
- include untracked files in evaluator context

## Before verification gate
- compare current `HEAD` with `qa-state.md.head_commit`
- compare current contract hash with `qa-state.md.contract_hash`
- if either differs, re-run QA before claiming completion

# Core Architecture

Harnessed is split into a platform-neutral core and platform-specific adapters.

## Core responsibilities
- define the artifact protocol in `.harnessed/`
- define prompt templates and grading semantics
- define routing, tier detection, state transitions, and failure-pattern policy

## Adapter responsibilities
- inject or expose Harnessed entrypoints on each host platform
- map host-specific hooks, skills, commands, and subagents to the core workflow
- keep user-facing installation paths stable for that platform

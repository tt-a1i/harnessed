#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]

COPIES = [
    ('core/skills/using-harnessed/SKILL.md', 'platforms/claude/skills/using-harnessed/SKILL.md'),
    ('core/skills/using-harnessed/SKILL.md', 'platforms/codex/skills/using-harnessed/SKILL.md'),
    ('core/skills/using-harnessed/SKILL.md', 'platforms/opencode/.opencode/skills/using-harnessed/SKILL.md'),
    ('core/skills/contract-writing/SKILL.md', 'platforms/claude/skills/contract-writing/SKILL.md'),
    ('core/skills/contract-writing/SKILL.md', 'platforms/codex/skills/contract-writing/SKILL.md'),
    ('core/skills/contract-writing/SKILL.md', 'platforms/opencode/.opencode/skills/contract-writing/SKILL.md'),
    ('core/skills/independent-qa/SKILL.md', 'platforms/claude/skills/independent-qa/SKILL.md'),
    ('core/skills/independent-qa/SKILL.md', 'platforms/codex/skills/independent-qa/SKILL.md'),
    ('core/skills/independent-qa/SKILL.md', 'platforms/opencode/.opencode/skills/independent-qa/SKILL.md'),
    ('core/skills/verification-gate/SKILL.md', 'platforms/claude/skills/verification-gate/SKILL.md'),
    ('core/skills/verification-gate/SKILL.md', 'platforms/codex/skills/verification-gate/SKILL.md'),
    ('core/skills/verification-gate/SKILL.md', 'platforms/opencode/.opencode/skills/verification-gate/SKILL.md'),
    ('core/protocol/contract-format.md', 'platforms/claude/skills/contract-writing/contract-format.md'),
    ('core/protocol/contract-format.md', 'platforms/codex/skills/contract-writing/contract-format.md'),
    ('core/protocol/contract-format.md', 'platforms/opencode/.opencode/skills/contract-writing/contract-format.md'),
    ('core/prompts/evaluator-prompt.md', 'platforms/claude/skills/independent-qa/evaluator-prompt.md'),
    ('core/prompts/evaluator-prompt.md', 'platforms/codex/skills/independent-qa/evaluator-prompt.md'),
    ('core/prompts/evaluator-prompt.md', 'platforms/opencode/.opencode/skills/independent-qa/evaluator-prompt.md'),
    ('core/prompts/grading-rubric.md', 'platforms/claude/skills/independent-qa/grading-rubric.md'),
    ('core/prompts/grading-rubric.md', 'platforms/codex/skills/independent-qa/grading-rubric.md'),
    ('core/prompts/grading-rubric.md', 'platforms/opencode/.opencode/skills/independent-qa/grading-rubric.md'),
    ('core/prompts/security-reviewer-prompt.md', 'platforms/claude/skills/independent-qa/security-reviewer-prompt.md'),
    ('core/prompts/security-reviewer-prompt.md', 'platforms/codex/skills/independent-qa/security-reviewer-prompt.md'),
    ('core/prompts/security-reviewer-prompt.md', 'platforms/opencode/.opencode/skills/independent-qa/security-reviewer-prompt.md'),
    ('core/prompts/tie-break-reviewer-prompt.md', 'platforms/claude/skills/independent-qa/tie-break-reviewer-prompt.md'),
    ('core/prompts/tie-break-reviewer-prompt.md', 'platforms/codex/skills/independent-qa/tie-break-reviewer-prompt.md'),
    ('core/prompts/tie-break-reviewer-prompt.md', 'platforms/opencode/.opencode/skills/independent-qa/tie-break-reviewer-prompt.md'),
]


def main() -> None:
    for src_rel, dst_rel in COPIES:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        print(f'synced {src_rel} -> {dst_rel}')


if __name__ == '__main__':
    main()

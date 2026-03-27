#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
skill_path = root / 'platforms' / 'codex' / 'skills' / 'using-harnessed' / 'SKILL.md'
if not skill_path.exists():
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'SessionStart',
            'additionalContext': 'Harnessed Codex adapter: meta-skill not found.'
        }
    }))
else:
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'SessionStart',
            'additionalContext': skill_path.read_text()
        }
    }))

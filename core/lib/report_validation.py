from __future__ import annotations

from pathlib import Path


def has_qa_header(path: str | Path) -> bool:
    text = Path(path).read_text()
    return text.lstrip().startswith('# QA Report')

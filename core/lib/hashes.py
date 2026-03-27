from __future__ import annotations

import hashlib
from pathlib import Path


def md5_file(path: str | Path) -> str:
    data = Path(path).read_bytes()
    return hashlib.md5(data).hexdigest()

from __future__ import annotations

import re
from typing import Any

SENSITIVE = re.compile(r"password|secret|token|api[_-]?key|credential|authorization|cookie|private[_-]?key", re.I)


def redact(value: Any, key: str = "") -> Any:
    if SENSITIVE.search(key):
        return "<REDACTED>"
    if isinstance(value, dict):
        return {k: redact(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value

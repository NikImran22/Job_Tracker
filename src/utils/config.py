"""Application configuration loaded from ``src/.env.local`` and environment."""

from __future__ import annotations

import os
from pathlib import Path


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        value = value.strip().strip("\"'")
        if key:
            values[key] = value
    return values


_env_file = Path(__file__).resolve().parents[1] / ".env.local"
_file_config = _read_env_file(_env_file)

# Variables in the process environment take precedence over .env.local.
config = {**_file_config, **os.environ}

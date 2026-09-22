#!/usr/bin/env python3
"""SEAL v2 compose entry — delegates to agentic_irc/scripts/seal.py (issue #5)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agentic_compose import delegate_to_agentic  # noqa: E402


def main(argv: list[str] | None = None) -> None:
    args = argv if argv is not None else sys.argv[1:]
    raise SystemExit(delegate_to_agentic("seal.py", args))


if __name__ == "__main__":
    main()

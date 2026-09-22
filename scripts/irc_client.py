#!/usr/bin/env python3
"""Thin IRC client entry for irc-skill (P1 stub). No exe drop; env-driven host/port."""
from __future__ import annotations

import argparse
import os
import sys


def _env_host_port() -> tuple[str | None, int | None]:
    host = (os.environ.get("AGENTIC_IRC_HOST") or "").strip() or None
    port_raw = (os.environ.get("AGENTIC_IRC_PORT") or "").strip()
    port: int | None = None
    if port_raw:
        try:
            port = int(port_raw)
        except ValueError:
            print("INFO invalid AGENTIC_IRC_PORT", file=sys.stderr)
            return host, None
    return host, port


def main() -> None:
    p = argparse.ArgumentParser(
        description="irc-skill client stub (P1). Set AGENTIC_IRC_HOST and AGENTIC_IRC_PORT to connect."
    )
    p.add_argument("--host", default="", help="IRC host (else AGENTIC_IRC_HOST)")
    p.add_argument("--port", type=int, default=0, help="IRC port (else AGENTIC_IRC_PORT)")
    args = p.parse_args()

    env_host, env_port = _env_host_port()
    host = (args.host or env_host or "").strip()
    port = args.port or env_port or 0

    if not host or not port:
        print(
            "INFO irc-skill P1 stub: host/port UNKNOWN (U2). "
            "Set AGENTIC_IRC_HOST and AGENTIC_IRC_PORT or pass --host/--port when P2 locks behaviour.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    # P1: no wire implementation until U1–U6; confirm resolution only.
    print(f"INFO target {host}:{port} (stub; no connection in P1)")
    raise SystemExit(0)


if __name__ == "__main__":
    main()

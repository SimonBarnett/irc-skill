#!/usr/bin/env python3
"""Serve the SMIRC-like static UI for independent local testing (#20)."""
from __future__ import annotations

import argparse
import http.server
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "ui" / "smirc"

REQUIRED_HOOKS = (
    'data-testid="smirc-channel-list"',
    'data-testid="smirc-chat-pane"',
    'data-testid="smirc-user-list"',
    'data-testid="smirc-chat-tabs"',
    'data-testid="smirc-image-drop"',
)


def validate_ui_tree() -> list[str]:
    errors: list[str] = []
    index = UI_DIR / "index.html"
    if not index.is_file():
        errors.append(f"missing {index}")
        return errors
    text = index.read_text(encoding="utf-8")
    for hook in REQUIRED_HOOKS:
        if hook not in text:
            errors.append(f"index.html missing {hook}")
    for name in ("smirc.css", "smirc.js"):
        if not (UI_DIR / name).is_file():
            errors.append(f"missing {UI_DIR / name}")
    return errors


class SmircHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Serve irc-skill SMIRC UI (static demo).")
    p.add_argument("--host", default="127.0.0.1", help="Bind address (default 127.0.0.1)")
    p.add_argument("--port", type=int, default=8765, help="TCP port (default 8765)")
    p.add_argument(
        "--demo",
        action="store_true",
        help="Demo mode (default); static assets only, no IRC connect.",
    )
    p.add_argument(
        "--check-only",
        action="store_true",
        help="Validate ui/smirc layout hooks and exit (BT0).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = validate_ui_tree()
    if errors:
        for err in errors:
            print("ERROR:", err, file=sys.stderr)
        return 1
    if args.check_only:
        print("smirc-ui: layout hooks OK")
        return 0
    if not args.demo:
        print("INFO: use --demo for the documented independent test entry.", file=sys.stderr)
    host, port = args.host, args.port
    with socketserver.TCPServer((host, port), SmircHandler) as httpd:
        httpd.allow_reuse_address = True
        url = "http://%s:%s/" % (host, port)
        print("SMIRC UI (%s) at %s" % ("demo" if args.demo else "static", url))
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

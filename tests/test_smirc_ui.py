"""BT0 tests for SMIRC-like UI scaffold (#20). No network."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVE = ROOT / "scripts" / "smirc_ui_serve.py"
INDEX = ROOT / "ui" / "smirc" / "index.html"

HOOKS = (
    "smirc-channel-list",
    "smirc-chat-pane",
    "smirc-user-list",
    "smirc-chat-tabs",
    "smirc-image-drop",
)


def test_smirc_static_assets_present():
    assert INDEX.is_file()
    assert (ROOT / "ui" / "smirc" / "smirc.js").is_file()
    assert (ROOT / "docs" / "smirc-ui-layout.md").is_file()


def test_smirc_layout_hooks_in_index():
    text = INDEX.read_text(encoding="utf-8")
    for hook in HOOKS:
        assert f'data-testid="{hook}"' in text


def test_smirc_serve_check_only():
    proc = subprocess.run(
        [sys.executable, str(SERVE), "--check-only"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "layout hooks OK" in proc.stdout


def test_smirc_serve_help_no_secrets():
    proc = subprocess.run(
        [sys.executable, str(SERVE), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    out = proc.stdout + proc.stderr
    assert "PASSWORD" not in out.upper()
    assert "XAI_API_KEY" not in out

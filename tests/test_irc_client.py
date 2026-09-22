"""No-network unit tests for irc-skill client config (P2)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "scripts" / "irc_client.py"
sys.path.insert(0, str(ROOT / "scripts"))
import irc_client as mod  # noqa: E402


def test_tls_for_port_6697():
    assert mod.tls_for(6697, False, False) is True
    assert mod.tls_for(6667, False, False) is False
    assert mod.tls_for(6667, True, False) is True
    assert mod.tls_for(6697, False, True) is False


def test_dry_run_subprocess_no_password():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("AGENTIC_IRC_"):
            del env[key]
    proc = subprocess.run(
        [sys.executable, str(CLIENT), "--dry-run", "--host", "example.test", "--port", "6697"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert proc.returncode == 0
    out = proc.stdout + proc.stderr
    assert "example.test:6697" in out
    assert "PASSWORD" not in out.upper()


def test_missing_host_port_exit_2():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("AGENTIC_IRC_"):
            del env[key]
    proc = subprocess.run(
        [sys.executable, str(CLIENT), "--dry-run"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert proc.returncode == 2

"""No-network unit tests for irc-skill client config (P2)."""
from __future__ import annotations

import importlib.util
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


def test_dry_run_agentic_compose_flag():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("AGENTIC_IRC_"):
            del env[key]
    proc = subprocess.run(
        [
            sys.executable,
            str(CLIENT),
            "--dry-run",
            "--agentic-compose",
            "--host",
            "example.test",
            "--port",
            "6697",
        ],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert proc.returncode == 0
    assert "agentic-compose" in proc.stdout


def test_compose_scripts_present():
    root = ROOT / "scripts"
    assert (root / "agentic_compose.py").is_file()
    assert (root / "irc_seal.py").is_file()
    assert (root / "irc_filexfer.py").is_file()


def test_resolve_agentic_scripts_when_installed():
    mod_path = ROOT / "scripts" / "agentic_compose.py"
    spec = importlib.util.spec_from_file_location("agentic_compose", mod_path)
    assert spec and spec.loader
    ac = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ac)
    path = ac.resolve_agentic_scripts()
    # Optional on CI; on dev boxes with agentic-irc skill it should resolve.
    if path is not None:
        assert (path / "seal.py").is_file()


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

"""Offline tests for install_skill.py (#21)."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install_skill.py"

EXPECTED_LEAFLETS = (
    "irc-skill",
    "irc-skill-setup",
    "irc-skill-use",
    "irc-skill-monitor",
    "harvest-irc-skill",
)


def test_install_skill_copies_all_leaflets():
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["GROK_HOME"] = tmp
        proc = subprocess.run(
            [sys.executable, str(INSTALL)],
            capture_output=True,
            text=True,
            env=env,
            cwd=str(ROOT),
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        grok = Path(tmp)
        for name in EXPECTED_LEAFLETS:
            leaflet = grok / "skills" / name / "SKILL.md"
            assert leaflet.is_file(), f"missing installed {leaflet}"
            text = leaflet.read_text(encoding="utf-8")
            assert f"name: {name}" in text or f"name:{name}" in text.replace(" ", "")

        client = grok / "skills" / "irc-skill" / "scripts" / "irc_client.py"
        assert client.is_file()

#!/usr/bin/env python3
"""Copy irc-skill leaflet + scripts into $GROK_HOME/skills/irc-skill/."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

SKILL = "irc-skill"
CLIENT_SCRIPTS = ("irc_client.py", "install_skill.py")


def main() -> None:
    grok = Path(os.environ.get("GROK_HOME", Path.home() / ".grok")).expanduser()
    root = Path(__file__).resolve().parents[1]
    dest = grok / "skills" / SKILL
    dest.mkdir(parents=True, exist_ok=True)

    src_leaflet = root / ".grok" / "skills" / SKILL / "SKILL.md"
    if not src_leaflet.is_file():
        raise SystemExit(f"missing skill leaflet: {src_leaflet}")
    shutil.copy2(src_leaflet, dest / "SKILL.md")
    print(dest / "SKILL.md")

    scripts_dest = dest / "scripts"
    scripts_dest.mkdir(parents=True, exist_ok=True)
    for name in CLIENT_SCRIPTS:
        sp = root / "scripts" / name
        if sp.is_file():
            shutil.copy2(sp, scripts_dest / name)
            print(scripts_dest / name)


if __name__ == "__main__":
    main()

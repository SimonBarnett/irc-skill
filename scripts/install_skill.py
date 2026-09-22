#!/usr/bin/env python3
"""Copy irc-skill leaflets + client scripts into $GROK_HOME/skills/."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

PRIMARY_SKILL = "irc-skill"
CLIENT_SCRIPTS = (
    "irc_client.py",
    "install_skill.py",
    "agentic_compose.py",
    "irc_seal.py",
    "irc_filexfer.py",
)


def install_leaflets(root: Path, grok: Path) -> None:
    skills_src = root / ".grok" / "skills"
    if not skills_src.is_dir():
        raise SystemExit(f"missing skills tree: {skills_src}")
    for skill_dir in sorted(skills_src.iterdir()):
        if not skill_dir.is_dir():
            continue
        leaflet = skill_dir / "SKILL.md"
        if not leaflet.is_file():
            continue
        name = skill_dir.name
        dest = grok / "skills" / name
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(leaflet, dest / "SKILL.md")
        print(dest / "SKILL.md")


def main() -> None:
    grok = Path(os.environ.get("GROK_HOME", Path.home() / ".grok")).expanduser()
    root = Path(__file__).resolve().parents[1]

    install_leaflets(root, grok)

    dest = grok / "skills" / PRIMARY_SKILL
    dest.mkdir(parents=True, exist_ok=True)
    scripts_dest = dest / "scripts"
    scripts_dest.mkdir(parents=True, exist_ok=True)
    for name in CLIENT_SCRIPTS:
        sp = root / "scripts" / name
        if sp.is_file():
            shutil.copy2(sp, scripts_dest / name)
            print(scripts_dest / name)


if __name__ == "__main__":
    main()

# irc-skill

New product repo. The locked brief is [docs/functional-spec.md](docs/functional-spec.md).

An **IRC client installed as an agent skill**, not a pile of per-platform port executables.

MRB home: [GitHub issue #1](https://github.com/SimonBarnett/irc-skill/issues/1).

## Install (skill, not exe ports)

From a clone of this repository:

```bash
python scripts/install_skill.py
```

This copies `.grok/skills/irc-skill/SKILL.md` and client scripts into `$GROK_HOME/skills/irc-skill/` (default `~/.grok/skills/irc-skill`). You can also copy those paths manually.

The thin client entry (P1 stub):

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py --help
```

Do not use `dist/*.exe` or a `ports/` exe kit as the documented install path.

## Validate (BT0)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-IrcSkill.ps1
```

Build plan: [docs/build-and-test-plan.md](docs/build-and-test-plan.md).

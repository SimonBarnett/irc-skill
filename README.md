# irc-skill

New product repo. The locked brief is [docs/functional-spec.md](docs/functional-spec.md).

An **IRC client installed as an agent skill**, not a pile of per-platform port executables.

MRB home: [GitHub issue #1](https://github.com/SimonBarnett/irc-skill/issues/1).

## Install (skill, not exe ports)

From a clone of this repository:

```bash
python scripts/install_skill.py
```

This copies every leaflet under `.grok/skills/*/` into `$GROK_HOME/skills/<name>/` and client scripts into `$GROK_HOME/skills/irc-skill/scripts/` (default `~/.grok`). You can also copy those paths manually.

| Skill | Job |
|-------|-----|
| `irc-skill` | Index + install |
| `irc-skill-setup` | First-run env, TLS 6697, dry-run, identity home |
| `irc-skill-use` | Connect, JOIN, stdin/outbox, optional compose |
| `irc-skill-monitor` | Health checks without requiring live IRC in CI |
| `harvest-irc-skill` | CAST IRON learnings back into this repo (`docs/skill-harvest-log.md`) |

The Python IRC client (P2):

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py --help
```

Configure via `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT`, `AGENTIC_IRC_NICK`, `AGENTIC_IRC_PASSWORD` or matching CLI flags. Use `--dry-run` to print the resolved target without connecting.

**SEAL + file transfer (#5):** install the [agentic-irc](https://github.com/SimonBarnett/agentic_irc) skill, then use `scripts/irc_seal.py`, `scripts/irc_filexfer.py`, and `scripts/irc_client.py --agentic-compose --channel …` (compose path; see skill leaflet).

Do not use `dist/*.exe` or a `ports/` exe kit as the documented install path.

## SMIRC-like UI (#20)

Independently testable static UI (channels left, chat tabs bottom, user list). Layout MUST and UNKNOWN gates: [docs/smirc-ui-layout.md](docs/smirc-ui-layout.md).

```bash
python scripts/smirc_ui_serve.py --demo
```

## Validate (BT0)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-IrcSkill.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-SmircUi.ps1
```

Build plans: [docs/build-and-test-plan.md](docs/build-and-test-plan.md), [docs/build-and-test-plan-p2.md](docs/build-and-test-plan-p2.md), [docs/build-and-test-plan-sft.md](docs/build-and-test-plan-sft.md), [docs/build-and-test-plan-smirc-ui-2026-09-22.md](docs/build-and-test-plan-smirc-ui-2026-09-22.md).

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Test-IrcClientParse.ps1
python -m pytest tests/ -q
```

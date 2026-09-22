---
name: irc-skill
description: >
  Install and use the irc-skill IRC client as an agent skill (not per-platform
  exe ports). Use when the user says IRC client skill, install irc-skill,
  /irc-skill, skill install for IRC, or wants the product client from
  SimonBarnett/irc-skill instead of copying executables around.
---

# irc-skill

IRC **client** distributed as an **installable agent skill** (`SKILL.md` + scripts). Operators install the skill pack; they do **not** ship a tree of per-OS / per-arch standalone `exe` drops as the install story.

Locked brief: `docs/functional-spec.md` in [SimonBarnett/irc-skill](https://github.com/SimonBarnett/irc-skill). MRB home: GitHub issue #1.

This product is **not** a replacement for `SimonBarnett/agentic_irc` (fleet TLS connector, SEAL, talk-seat TSR). Use `agentic_irc` for bobiverse wire until a later FR says otherwise.

## Hard gate — install as skill

From a clone of this repo:

```bash
python scripts/install_skill.py
```

That copies this leaflet and `scripts/` into `$GROK_HOME/skills/irc-skill/` (default `~/.grok/skills/irc-skill`). Or copy `.grok/skills/irc-skill/` and `scripts/` there manually.

Then invoke the Python IRC client (P2):

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py --help
```

Set `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT`, `AGENTIC_IRC_NICK`, and `AGENTIC_IRC_PASSWORD` (or pass `--host`, `--port`, `--nick`, `--password`). TLS is used on port **6697** or when `--tls` is set. Check resolution without connecting:

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py --dry-run --host YOUR_HOST --port 6697 --nick YOUR_NICK
```

Do not print or commit passwords. This skill is **not** a substitute for `agentic_irc` fleet SEAL/talk-seat tooling.

Do **not** document or rely on `dist/*.exe`, `ports/`, or any exe kit as how to get the client.

## MUST NOT

- Port or vendor platform `exe` trees as the install path (spec L4, N4).
- Commit passwords, Ergo PASS, API keys, or `password=` / `XAI_API_KEY=` assignments in git (L6).
- Stamp **ready for human UAT** (L7; Bob only).
- Invent instance URLs, nicks, or credentials (N2). Use env `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT`, `AGENTIC_IRC_NICK`, `AGENTIC_IRC_PASSWORD` or CLI flags only.

## P2 client

`scripts/irc_client.py` connects over TLS (6697 or `--tls`), registers with NICK/USER/PASS when configured, and stays up until interrupted. Optional `--channel` JOIN after welcome. No hard-coded servers.

## Triggers

IRC client skill, install irc-skill, `/irc-skill`, skill install for IRC, irc-skill repo, not 90s exe ports.

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

Then invoke the thin client entry (P1 stub until U1–U6 are locked):

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py --help
```

Do **not** document or rely on `dist/*.exe`, `ports/`, or any exe kit as how to get the client.

## MUST NOT

- Port or vendor platform `exe` trees as the install path (spec L4, N4).
- Commit passwords, Ergo PASS, API keys, or `password=` / `XAI_API_KEY=` assignments in git (L6).
- Stamp **ready for human UAT** (L7; Bob only).
- Invent instance URLs, nicks, or credentials (N2). Host/port for P1: env `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT` if set (same family as `agentic_irc`); otherwise treat as UNKNOWN (U2) and exit with guidance.

## P1 client stub

`scripts/irc_client.py` is a thin Python entry the skill points at. It does not embed fleet URLs. Connection behaviour expands in P2 after Simon locks UNKNOWN U1–U6.

## Triggers

IRC client skill, install irc-skill, `/irc-skill`, skill install for IRC, irc-skill repo, not 90s exe ports.

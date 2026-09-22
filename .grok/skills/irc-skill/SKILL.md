---
name: irc-skill
description: >
  Index for the irc-skill IRC client skill pack (install + pointers). Use when
  the user says IRC client skill, install irc-skill, /irc-skill, skill install
  for IRC, or SimonBarnett/irc-skill instead of exe ports. For a specific job
  load irc-skill-setup, irc-skill-use, or irc-skill-monitor; harvest via
  harvest-irc-skill.
---

# irc-skill

IRC **client** distributed as **installable agent skills** (`SKILL.md` + scripts). Operators install the skill pack; they do **not** ship per-OS `exe` drops as the install story.

| Skill | Job |
|-------|-----|
| **irc-skill-setup** | First-run: install, env, TLS 6697, dry-run, `genkey` once per home |
| **irc-skill-use** | Daily: connect, JOIN, stdin/outbox, optional `--agentic-compose` |
| **irc-skill-monitor** | Health: process/log, dry-run, 433/`_l`, do not kill another seat's home |
| **harvest-irc-skill** | CAST IRON: client learnings write back to this repo |

Load the row that matches the operator question; this file is the index.

Locked brief: `docs/functional-spec.md` in [SimonBarnett/irc-skill](https://github.com/SimonBarnett/irc-skill). MRB home: GitHub issue #1.

P2 client + **compose** with `SimonBarnett/agentic_irc` for **SEAL v2** and **FILE v1** (issue [#5](https://github.com/SimonBarnett/irc-skill/issues/5)). This skill does not replace the fleet talk-seat TSR; it reuses `agentic_irc` crypto/wire scripts instead of inventing a second stack.

## Hard gate — install as skill

From a clone of this repo:

```bash
python scripts/install_skill.py
```

That copies **every** leaflet under `.grok/skills/*/` into `$GROK_HOME/skills/<name>/` and client `scripts/` into `$GROK_HOME/skills/irc-skill/scripts/` (default `~/.grok`). Or copy those paths manually.

Then invoke the Python IRC client (P2):

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py --help
```

Set `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT`, `AGENTIC_IRC_NICK`, and `AGENTIC_IRC_PASSWORD` (or pass `--host`, `--port`, `--nick`, `--password`). TLS is used on port **6697** or when `--tls` is set. Check resolution without connecting:

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py --dry-run --host YOUR_HOST --port 6697 --nick YOUR_NICK
```

Do not print or commit passwords.

### SEAL and file transfer (#5)

Install the **agentic-irc** skill (or clone that repo) so `~/.grok/skills/agentic-irc/scripts/seal.py` exists. Use the same `AGENTIC_IRC_HOME` identity as fleet agents (`python …/seal.py genkey` once per home).

Compose wrappers (delegate to agentic_irc; no second crypto):

```bash
python ~/.grok/skills/irc-skill/scripts/irc_seal.py genkey
python ~/.grok/skills/irc-skill/scripts/irc_seal.py pubkey
python ~/.grok/skills/irc-skill/scripts/irc_filexfer.py offer --help
```

Live client with outbox drain + SEAL/FILE receive on a channel:

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py \
  --host YOUR_HOST --port 6697 --nick YOUR_NICK --channel '#your-room' --agentic-compose
```

Prepare offers with `irc_filexfer.py offer` (writes `outbox.txt` under `AGENTIC_IRC_HOME`); the compose client sends complete outbox lines and accepts tier **M** chunks or tier **S** SEAL envelopes.

Do **not** document or rely on `dist/*.exe`, `ports/`, or any exe kit as how to get the client.

## MUST NOT

- Port or vendor platform `exe` trees as the install path (spec L4, N4).
- Commit passwords, Ergo PASS, API keys, or `password=` / `XAI_API_KEY=` assignments in git (L6).
- Stamp **ready for human UAT** (L7; Bob only).
- Invent instance URLs, nicks, or credentials (N2). Use env `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT`, `AGENTIC_IRC_NICK`, `AGENTIC_IRC_PASSWORD` or CLI flags only.

## P2 client

`scripts/irc_client.py` connects over TLS (6697 or `--tls`), registers with NICK/USER/PASS when configured, and stays up until interrupted. On **433 nick-in-use**, it retries **once** with the same nick plus suffix `_l` (logged to stderr); **464** still fails closed. Optional `--channel` JOIN after welcome. `--agentic-compose` adds SEAL/FILE handling via agentic_irc. No hard-coded servers.

## Triggers

IRC client skill, install irc-skill, `/irc-skill`, skill install for IRC, irc-skill repo, not 90s exe ports.

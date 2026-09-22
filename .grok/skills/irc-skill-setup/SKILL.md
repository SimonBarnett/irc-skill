---
name: irc-skill-setup
description: >
  First-run setup for the irc-skill IRC client: clone/install, GROK_HOME,
  AGENTIC_IRC_HOME, TLS 6697, dry-run before live connect, genkey once per home.
  Use when the user says set up IRC client, first run irc-skill, install IRC
  skill, configure AGENTIC_IRC, /irc-skill-setup, or new machine IRC client.
---

# irc-skill-setup

**Job:** get a clean machine ready to run the [irc-skill](https://github.com/SimonBarnett/irc-skill) Python client — without live credentials in git.

Index leaflet: `.grok/skills/irc-skill/SKILL.md`. Daily use: `irc-skill-use`. Health: `irc-skill-monitor`.

## Prerequisites

- Python **3.x** that can run `scripts/irc_client.py` (no pinned minor version in this repo).
- Clone `SimonBarnett/irc-skill` (or use an existing worktree).

## Install the skill pack

```bash
python scripts/install_skill.py
```

Copies every leaflet under `.grok/skills/*/` into `$GROK_HOME/skills/<name>/` (default `~/.grok`). Client scripts land in `$GROK_HOME/skills/irc-skill/scripts/`.

## Environment (names only — no secrets in git)

| Variable | Purpose |
|----------|---------|
| `GROK_HOME` | Agent skill root (default `~/.grok`) |
| `AGENTIC_IRC_HOME` | Per-seat identity dir (keys, outbox); same convention as fleet `agentic_irc` |
| `AGENTIC_IRC_HOST` | IRC server hostname |
| `AGENTIC_IRC_PORT` | Usually **6697** (TLS) |
| `AGENTIC_IRC_NICK` | Nick at register |
| `AGENTIC_IRC_PASSWORD` | Server PASS if required — **env or CLI only**, never commit |

TLS: port **6697** or `--tls` on other ports. See `docs/functional-spec.md`.

## First-run checklist

1. Run `install_skill.py` (above).
2. `python …/irc_client.py --dry-run --host YOUR_HOST --port 6697 --nick YOUR_NICK` — must exit 0 and show resolved target **without** printing PASSWORD.
3. For SEAL/compose: install **agentic-irc** skill; `python …/irc_seal.py genkey` **once per** `AGENTIC_IRC_HOME`.
4. Only then connect for real (see `irc-skill-use`).

Do **not** use `dist/*.exe` or `ports/` as the install path.

## MUST NOT

- Commit passwords, `password=`, API keys, or Ergo PASS in git.
- Invent hosts, nicks, or credentials (use env/CLI placeholders).
- Replace the fleet talk-seat TSR (`agentic_irc`); this repo is the **client** skill only.
- Stamp ready for human UAT.

## Triggers

set up IRC client, first run irc-skill, configure AGENTIC_IRC, install IRC skill pack, /irc-skill-setup.

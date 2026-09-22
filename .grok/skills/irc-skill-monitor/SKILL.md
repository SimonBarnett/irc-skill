---
name: irc-skill-monitor
description: >
  Monitor whether the irc-skill client is alive: process/log checks, dry-run
  resolution, 433/_l collision, listen silence vs QUIT. Use when the user says
  monitor IRC client, is IRC up, stuck client, 433 nick, /irc-skill-monitor.
---

# irc-skill-monitor

**Job:** decide if the IRC **client** is healthy — **without** requiring a live Ergo server in CI or this skill.

Setup: `irc-skill-setup`. Use: `irc-skill-use`.

## What "up" means

- A `irc_client.py` process you started is still running (not exited on **464** or fatal error).
- stderr shows registration / JOIN (or expected dry-run output if you are only checking config).
- The seat's `AGENTIC_IRC_HOME` is the one you intend — **do not** `Stop-Process` or delete another agent's home.

## Quick checks (offline-safe)

1. **Config resolution:**  
   `python …/irc_client.py --dry-run --host YOUR_HOST --port 6697 --nick YOUR_NICK`  
   Exit 0 ⇒ host/port/nick resolve; no password in output.

2. **433 / `_l`:** if logs show nick retry to `nick_l`, another session may hold the base nick — expected once; persistent 433 needs operator action.

3. **Silence vs dead:** no PRIVMSG for a while is normal. Process gone, or QUIT in log, is **down**. Distinguish from idle listen.

4. **Logs:** stderr from the client process; optional compose lines when `--agentic-compose` is on.

No live IRC server is required for dry-run or this leaflet. A future `scripts/irc_monitor.py` helper is optional; not required for #21.

## MUST NOT

- Kill processes tied to a **different** `AGENTIC_IRC_HOME` / another agent's talk seat.
- Commit passwords or require live Ergo in automated tests for this skill.
- Stamp ready for human UAT.

## Triggers

monitor IRC client, is IRC client up, stuck IRC, 433 nick, listen silence, /irc-skill-monitor.

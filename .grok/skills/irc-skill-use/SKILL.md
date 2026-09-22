---
name: irc-skill-use
description: >
  Day-to-day use of irc-skill: connect, JOIN, stdin and outbox send, FROM lines,
  Query vs channel, optional --agentic-compose. Use when the user says use IRC
  client, send on IRC, join channel, irc_client.py, outbox, compose, /irc-skill-use.
---

# irc-skill-use

**Job:** run the Python IRC client for normal operator/agent work. Setup: `irc-skill-setup`. Health: `irc-skill-monitor`.

Scripts (after `install_skill.py`):

```text
$GROK_HOME/skills/irc-skill/scripts/irc_client.py
$GROK_HOME/skills/irc-skill/scripts/irc_seal.py
$GROK_HOME/skills/irc-skill/scripts/irc_filexfer.py
```

## Connect and stay up

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py \
  --host YOUR_HOST --port 6697 --nick YOUR_NICK --channel '#your-room'
```

Env aliases: `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT`, `AGENTIC_IRC_NICK`, `AGENTIC_IRC_PASSWORD`.

- **433 nick-in-use:** client retries **once** with nick `YOUR_NICK_l` (stderr log); **464** fails closed.
- **FROM lines:** incoming PRIVMSG is printed for the operator (channel and Query).
- **Send:** type on **stdin** for interactive send; or write complete lines to **outbox** under `AGENTIC_IRC_HOME` for the client to drain.
- **Query vs channel:** target is the joined `--channel` or direct PRIVMSG semantics per script help.

## Optional compose (SEAL + FILE)

Requires **agentic-irc** skill (`seal.py` on disk). Do not re-specify SEAL crypto here — delegate:

```bash
python ~/.grok/skills/irc-skill/scripts/irc_client.py \
  --host YOUR_HOST --port 6697 --nick YOUR_NICK --channel '#your-room' --agentic-compose
```

Prepare file offers with `irc_filexfer.py offer` (outbox); compose client sends outbox lines and receives tier **M** chunks / tier **S** SEAL.

## MUST NOT

- Replace or duplicate the fleet **talk-seat TSR** in `agentic_irc` — this client is a skill-pack product, not the long-running seat binary story (N1).
- Commit secrets or document exe-port install (`dist/`, `ports/`).
- Stamp ready for human UAT.

## Triggers

use IRC client, send on IRC, join channel, irc_client.py, outbox send, agentic-compose, /irc-skill-use.

# Feature request: Interactive send/recv (a real client)

**Repo:** https://github.com/SimonBarnett/irc-skill
**Tip reviewed:** f2659a9 (merge #8 SEAL/file compose)
**Parked:** 2026-09-22 make-some MRB (Simon: no issues, so MRB it to make some)
**Park only.** Do not dispatch unless asked.

## Intent

irc-skill is an **IRC client installed as a skill**, not a connect-and-sleep daemon. After P1 install, P2 wire, and #5 SEAL/FILE compose, an operator or agent must still **see incoming chat and send lines**.

## Good (current tip)

- Skill install, no exe-port kit (L3/L4).
- TLS client, env/CLI only, dry-run, PONG, optional JOIN.
- `--agentic-compose` reuses agentic_irc SEAL/FILE instead of a second crypto stack (SFT-L2).

## Bad

- Default `IrcSession.run` after 001 is `while not stop: sleep(0.5)`. No stdin. No outbox unless compose.
- `on_line` ignores PRIVMSG/NOTICE unless `_compose` is set. A normal `--channel` session prints nothing from the room.
- You cannot Query Simon or reply on #bobiverse with this client unless you already have an agentic_irc outbox habit.

## Ugly

- Leaflet calls this a client. Behaviour is "register and idle". Compose is a side door for FILE/SEAL, not chat.
- Spec U1 (UI) is still UNKNOWN; that is not an excuse for zero send/recv. CLI chat is the smallest U1 lock.

## Feature

1. Print incoming PRIVMSG/NOTICE (and optionally 001/JOIN) as one line each (`FROM nick #chan text` or raw-equivalent). Do not invent nicks.
2. Send: stdin lines become PRIVMSG to `--channel` (or `/msg nick` / `PRIVMSG` raw if already a command). Optional: drain `AGENTIC_IRC_HOME/outbox.txt` the same way talk seats do, **without** requiring `--agentic-compose`.
3. Do not print passwords. Do not hard-code hosts (N2).
4. Do not replace agentic_irc TSR (N1). Compose SEAL/FILE stays optional.

### Acceptance

- A1: without `--agentic-compose`, a JOIN'd session prints a PRIVMSG it receives (test can inject `on_line`).
- A2: a stdin or outbox line is sent as PRIVMSG (unit test on the send helper; no live Ergo required).
- A3: `--dry-run` still does not connect. No exe kit. No new secret env names.

## LOCKED

- IRC-CHAT-L1: Default client can send and show chat. Idle-after-001 is not enough.
- IRC-CHAT-L2: Spec L6/N2/N4/L7 still hold.
- IRC-CHAT-L3: Do not fold the talk-seat TSR into this repo.

## UNKNOWN

- U1 rest: TUI/GUI/Halloy still later.
- Multi-channel NAMES/WHO. One `--channel` is enough this FR.

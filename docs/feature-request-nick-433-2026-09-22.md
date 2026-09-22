# Feature request: Survive 433 nick-in-use

**Repo:** https://github.com/SimonBarnett/irc-skill
**Tip reviewed:** f2659a9
**Parked:** 2026-09-22 make-some MRB
**Park only.** Do not dispatch unless asked.

## Intent

A skill client used on a busy Ergo (two seats per box, `_l` collisions) must **not die on the first 433**. Fleet talk seats already hit this.

## Good

- 433/464/ERROR are detected and logged.
- Registration waits for 001 with a timeout.

## Bad

- `on_line` **stops the session** on 433. Second seat or leftover `_l` = dead client.
- No alternate nick, no retry, no keep-trying NICK.

## Ugly

- Spec U6 left SASL/nick rules to agentic_irc. This product still connects as its own NICK. One 433 makes the P2 client useless on the same net the fleet uses.

## Feature

On 433, try one documented alt (e.g. `nick_` then `nick_l` or timestamp suffix — pick one, test it). Do not loop forever. Log the chosen nick. Do not invent instance URLs. SASL remains UNKNOWN (not this FR).

### Acceptance

- A1: injected 433 then 001 → session continues with the alt nick (unit test).
- A2: 464 still fails closed (bad PASS).
- A3: No secrets, no exe kit.

## LOCKED

- IRC-433-L1: 433 is recoverable once; 464 is not.
- IRC-433-L2: L6/N2/N4/L7 still hold.

## UNKNOWN

- Full SASL / account registration (U6).
- How `_l` listen nicks compose with this client (stay agentic_irc).

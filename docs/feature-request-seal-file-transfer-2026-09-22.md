# Feature request: SEAL and file transfer support (2026-09-22)

**Issue:** https://github.com/SimonBarnett/irc-skill/issues/5  
**Spec:** docs/functional-spec.md  
**Prior:** #4 P2 working skill client (wire register + PONG; no SEAL, no file xfer).

Simon on GitHub issue #5 (`requirement`): `must suppot the seal and file tyranmsfer.`

## Gap vs current tree

`scripts/irc_client.py` is a generic IRC client: TLS/plain socket, NICK/USER/PASS from `AGENTIC_IRC_*` or flags, PONG, optional JOIN. The skill leaflet still says this product is **not** a substitute for `agentic_irc` fleet SEAL / talk-seat tooling.

No SEAL (encrypted secret boxes). No file transfer (chunked or path-drop). Those live in `SimonBarnett/agentic_irc` / the agentic-file skill today.

## LOCKED for this FR

| ID | Requirement |
|----|-------------|
| SFT-L1 | irc-skill must **support SEAL** and **file transfer** (the ask on #5). |
| SFT-L2 | Do not replace `agentic_irc` wholesale (spec N1) unless a later lock says fold it. Prefer compose or an explicit in-skill path that does not invent a second fleet connector. |
| SFT-L3 | Host/port/nick/pass stay CLI or existing `AGENTIC_IRC_*` names only. No new secret env names. No hard-coded instance URLs. |
| SFT-L4 | No secrets in git. No `password=` / `XAI_API_KEY=` assignments. No exe-port install kit (L4/N4). |
| SFT-L5 | Do not break P1 install-as-skill or the P2 client entry `scripts/irc_client.py`. |

## UNKNOWN (still)

| ID | Item |
|----|------|
| SFT-U1 | In-process SEAL vs shell-out / compose with `agentic_irc`. |
| SFT-U2 | File transfer shape (clear chunks, sealed payload, or path drop). |
| SFT-U3 | How this interacts with spec U4 (compose vs clean client) and U6 (SASL / nick rules). |
| SFT-U4 | UI for send/recv files (spec U1). |

## Out of this FR

P2 live connect / dry-run / BT0 (issue #4). Halloy/GUI. Mode 3 thin exe (U5). Worker UAT stamp (L7; Bob only).

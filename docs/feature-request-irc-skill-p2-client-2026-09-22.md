# Feature request: P2 working skill client (2026-09-22)

**Spec:** docs/functional-spec.md  
**Prior:** #1 P1 leaflet + stub `scripts/irc_client.py` MERGED PASS-nits (PR #2).  
**Plan:** docs/build-and-test-plan-p2.md  

Simon on `#bobiverse`: `marchhare - keep bob joibbing it`.

## Gap vs current tree

P1 stub exits 0 after printing `INFO target host:port (stub; no connection in P1)`. No TLS socket, no NICK/PASS, no send/recv.

## LOCKED for this FR

| ID | Requirement |
|----|-------------|
| P2-L1 | `scripts/irc_client.py` is a real Python IRC client entry (still not an `exe` kit). |
| P2-L2 | Host/port/nick/pass only from CLI flags or existing `AGENTIC_IRC_*` env (`HOST`, `PORT`, `NICK`, `PASSWORD`). Do not invent new secret names. Do not hard-code instance URLs. |
| P2-L3 | TLS when port is 6697 or `--tls` is set. No password printed. |
| P2-L4 | Do not replace `agentic_irc` (N1). |
| P2-L5 | Update skill leaflet: P1 stub language becomes P2 invoke. |
| P2-L6 | BT0 still exits 0. Add a no-network test for arg/env parse + dry-run. |

## UNKNOWN (still)

U1 UI, U5 Mode 3 thin exe, U6 extra nick/SASL rules — out of this FR.

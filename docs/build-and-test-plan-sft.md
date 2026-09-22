# Build and test plan: SEAL + file transfer (#5)

**Date:** 2026-09-22  
**Repo:** SimonBarnett/irc-skill  
**FR:** docs/feature-request-seal-file-transfer-2026-09-22.md  
**Issue:** https://github.com/SimonBarnett/irc-skill/issues/5  

## Goals

P1/P2 stay. Add **SEAL** and **file transfer** support to the skill client without replacing `agentic_irc` and without an exe kit. Open a PR. Never push `main`. Never merge. No worker UAT stamp.

## Non-goals

- Wholesale rewrite of `agentic_irc`
- New secret env names or hard-coded instance URLs
- Halloy/GUI, Mode 3 thin exe
- Breaking P2 `--dry-run` / TLS connect

## Locked constants

| Name | Value |
|------|--------|
| MRB issue | #5 |
| Entry | `scripts/irc_client.py` plus skill leaflet |
| Env | existing `AGENTIC_IRC_*` only |
| SEAL | v2 boxes as used by `agentic_irc` (compose or in-skill; do not invent a third crypto) |
| File | skill documents send/recv; no secrets in git |

## BT0

Existing `tools/Validate-IrcSkill.ps1` still exits 0. Add a no-network test that SEAL/file flags or skill text exist and do not print passwords.

## Definition of done

- Skill + client can send/receive a SEAL line and a file (or compose `agentic_irc`/`agentic-file` without a second fleet stack)
- README/skill updated
- PR URL, BT0 evidence
- No `exe` kit, no invented URLs

## Kickoff

Read the spec, SFT FR, and this plan. Implement #5 only. Open a PR. Never push `main`. Never merge. Do not set password= or API key assignments. Do not invent instance URLs. Do not stamp ready for human UAT.

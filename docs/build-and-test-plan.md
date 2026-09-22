# Build and test plan: irc-skill

**Date:** 2026-09-22  
**Repo:** SimonBarnett/irc-skill  
**Spec:** docs/functional-spec.md  
**Issue:** https://github.com/SimonBarnett/irc-skill/issues/1  

## Goals

1. P1: ship an installable agent skill that is the IRC **client** (operators/agents install a skill, not a zip of ported `exe`s).
2. Keep `docs/functional-spec.md` LOCKED constants. Do not invent instance URLs or credentials.
3. Open a PR. Never push `main`. Never merge. No worker UAT stamp.

## Non-goals

- Replacing `SimonBarnett/agentic_irc` fleet connector / SEAL / talk-seat TSR (N1).
- Halloy replacement UI unless spec U1 is later locked.
- Mode 3 thin-exe field path (U5) unless a later FR says fold it.
- Ready for human UAT (Bob only).

## Locked constants

| Name | Value |
|------|--------|
| MRB issue | #1 |
| Skill path | `.grok/skills/irc-skill/SKILL.md` |
| Skill name | `irc-skill` |
| Install story | skill leaflet + scripts in-repo; `python scripts/install_skill.py` or copy into `$GROK_HOME/skills/irc-skill` |
| Forbidden install | per-OS / per-arch standalone `exe` tree as the way to get the client |

## Phase order

| Phase | Exit criteria |
|-------|----------------|
| P0 | Spec + this plan on the repo (parked). |
| P1 | Skill + install script + README install section + BT0 validator. PR open. |
| P2 | Client behaviour after Simon locks U1–U6 or a follow-on FR. |

## Suggested tree (P1)

```
.grok/skills/irc-skill/SKILL.md
scripts/install_skill.py
scripts/irc_client.py   # thin client entry the skill invokes; no exe drop
tools/Validate-IrcSkill.ps1
docs/functional-spec.md
docs/build-and-test-plan.md
README.md
```

`irc_client.py` for P1 may be a stub that connects only if later FRs lock host/port. Do not hard-code secrets. Default host/port if needed: document as UNKNOWN (U2) or read env `AGENTIC_IRC_*` already used by `agentic_irc` — do not invent new secret names.

## BT0 — Structure (required before MRB)

From repo root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-IrcSkill.ps1
```

**Pass:** exit `0`. Checks:

- `.grok/skills/irc-skill/SKILL.md` exists with `name: irc-skill`
- Skill says install-as-skill, not port-exe
- `scripts/install_skill.py` exists
- No `dist/*.exe` or `ports/` exe kit as the documented install
- Spec + this plan present

## BT1 — Skill walkthrough (manual)

1. Open the skill. Confirm triggers (IRC client, skill install, `/irc-skill`).
2. Confirm MUST NOT: no 90s exe ports; no secrets in git; no worker UAT stamp.

## Definition of done (first ticket / #1)

- P1 tree landed on a branch
- BT0 exits 0
- PR URL in the job reply
- No push to `main`, no merge, no UAT stamp

## Kickoff (`Start-BobBuild -Goal`)

Read `docs/functional-spec.md` and this plan. Implement **P1 only** for issue #1. Open a PR. Paste BT0 output. Never push `main`. Never merge. Do not set password= or API key assignments. Do not invent Ergo/Libera URLs. Do not stamp ready for human UAT.

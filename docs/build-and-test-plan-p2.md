# Build and test plan: irc-skill P2 client

**Date:** 2026-09-22  
**Repo:** SimonBarnett/irc-skill  
**FR:** docs/feature-request-irc-skill-p2-client-2026-09-22.md  
**Spec:** docs/functional-spec.md  

## Goals

Turn the P1 stub into a working Python IRC client invoked by the skill. Keep install-as-skill. Open a PR. Never push `main`. Never merge. No worker UAT stamp.

## Non-goals

- Halloy / GUI (U1)
- Replacing `agentic_irc`
- New secret env names
- Hard-coded `irc.ntsa.uk` or other instance URLs
- Mode 3 thin exe (U5)

## Locked constants

| Name | Value |
|------|--------|
| Entry | `scripts/irc_client.py` |
| Env | `AGENTIC_IRC_HOST`, `AGENTIC_IRC_PORT`, `AGENTIC_IRC_NICK`, `AGENTIC_IRC_PASSWORD` |
| TLS | default on for port 6697 or `--tls` |
| Dry-run | `--dry-run` prints resolved target (no password) and exits 0 without connecting |

## BT0

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-IrcSkill.ps1
```

Plus a no-network check (pytest or a small `tools/Test-IrcClientParse.ps1`) that `--dry-run --host example.test --port 6697` exits 0 and does not print `PASSWORD`.

## Definition of done

- Live connect path exists when env/flags set (TLS)
- `--dry-run` and missing host/port still fail closed
- Skill text updated
- BT0 + parse test in PR
- No `exe` kit, no secrets in git

## Kickoff

Read the spec, P2 FR, and this plan. Implement P2 only. Open a PR. Paste test output. Never push `main`. Never merge. Do not set password= or API key assignments. Do not invent instance URLs. Do not stamp ready for human UAT.

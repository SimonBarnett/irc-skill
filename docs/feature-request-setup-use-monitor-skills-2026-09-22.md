# Feature request: setup / use / monitor skills

**Repo:** https://github.com/SimonBarnett/irc-skill
**Issue:** [#21](https://github.com/SimonBarnett/irc-skill/issues/21) (Simon title: *Can we fill in some more skills to set up use and monitor the IRC client*)
**Tip reviewed:** 507af33 (master after #13 + later 433/chat land)
**Parked:** 2026-09-22 (Simon: crack on — unowned open issue)
**Not #20.** UI / SMIRC-like surface stays [issue #20](https://github.com/SimonBarnett/irc-skill/issues/20). This FR is skills only.

## Intent

An operator or agent who has never touched this repo must be able to **set up** the client, **use** it day-to-day, and **monitor** whether it is still alive — by loading skills, not by reading the whole README + functional spec + four FRs. Simon asked for more skills covering those three jobs. One mashed leaflet is not three skills.

## Good (current tip)

- One installable leaflet (`.grok/skills/irc-skill/SKILL.md`) + `install_skill.py`.
- No exe-port kit (L3/L4). Env/CLI only. Dry-run. Interactive chat + optional compose (#5, #11).
- 433 nick retry parked/landed separately (#12). Spec L6/N1/N2/L7 still hold.

## Bad

- Only **one** skill exists. Setup, use, and monitor are three triggers mashed into one description. An agent looking for "monitor the IRC client" will not load `irc-skill`.
- `install_skill.py` copies **only** `irc-skill` + a hard-coded script list. Extra leaflets cannot install until the installer knows them.
- No first-run checklist skill: Python/deps, `GROK_HOME`, `AGENTIC_IRC_HOME`, TLS 6697, `genkey` once, `--dry-run` before a live connect.
- No use skill that says: stdin/outbox send, FROM print, Query vs channel, compose is optional, do not replace the talk-seat TSR.
- No monitor skill: what process/log to look at, what "up" means, 433/`_l` collision, listen silence, do not `Stop-Process` another seat's home.

## Ugly

- CAST IRON (`harvest-agent-skills`) routes "IRC client-as-skill" to **this repo's harvest skill**. There is no `.grok/skills/harvest-irc-skill/SKILL.md`. Learnings stay in `~/.grok` or get dumped into `agentic_irc` by habit.
- Leaflet still reads like a product brochure. Operators get lost between `agentic_irc` (fleet TSR) and this client.
- `Validate-IrcSkill.ps1` only asserts the one leaflet. Missing skills cannot fail CI.

## Feature (do this)

Split the product into **four** installable skills. Do **not** invent a GUI (that is #20). Do **not** fold the talk-seat TSR into this repo (N1).

| Skill | Job |
|-------|-----|
| `irc-skill-setup` | First-run: clone/install, env names, home dirs, TLS 6697, dry-run, `genkey` once per home, no secrets in git. |
| `irc-skill-use` | Daily: `irc_client.py` connect/JOIN, stdin + outbox send, FROM print, optional `--agentic-compose`. Point at scripts; do not re-specify SEAL crypto. |
| `irc-skill-monitor` | Health: client still registered; log/`--dry-run` resolution; 433/`_l`; do not kill another `AGENTIC_IRC_HOME`; silence vs QUIT. No live Ergo required in CI. |
| `harvest-irc-skill` | CAST IRON foundation: learnings about **this client** write back here (`.grok/skills/` + `docs/skill-harvest-log.md`). Empty harvest = no commit. Wire/TSR playbooks still go to `agentic_irc`. |

Keep the existing `irc-skill` leaflet as the index (install + pointers to the three jobs). Update `install_skill.py` to copy every `.grok/skills/*/SKILL.md` (or an explicit list that includes the four). Update `Validate-IrcSkill.ps1` so each leaflet exists, has `name:`, and mentions its job.

### Acceptance

- A1: `.grok/skills/irc-skill-setup/SKILL.md`, `irc-skill-use/SKILL.md`, `irc-skill-monitor/SKILL.md`, `harvest-irc-skill/SKILL.md` exist with YAML `name:` matching the folder.
- A2: `install_skill.py` copies those leaflets (and existing scripts). A dry test or validator proves dest paths after a temp `GROK_HOME`.
- A3: `Validate-IrcSkill.ps1` fails if any of the four is missing. Existing parse/dry-run tests stay green.
- A4: README names the three jobs + harvest. No exe kit. No new secret env names. No UAT stamp.
- A5: `docs/skill-harvest-log.md` exists with a seed entry. Monitor skill does not require a live server.

## LOCKED

- IRC-SUM-L1: Three operator skills (setup / use / monitor) plus harvest foundation. Not one leaflet pretending to be all four.
- IRC-SUM-L2: Spec L3/L4/L6/L7 and N1/N2/N4 still hold.
- IRC-SUM-L3: Do not implement #20 UI in this FR.
- IRC-SUM-L4: Harvest here is **this client**. Fleet TSR / Ergo / Halloy / SEAL wire stays `agentic_irc`.

## UNKNOWN

- Whether setup should pin a Python version (leave unset; require 3.x that already runs `irc_client.py`).
- Whether monitor grows a `scripts/irc_monitor.py` later. Leaflet + validator is enough this FR; a helper is optional if tests stay offline.

## MUST NOT

- Second-loop #20 or change SMIRC/UI scope.
- Stamp ready for human UAT.
- Commit passwords or invent hosts.

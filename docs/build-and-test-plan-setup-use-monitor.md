# Build and test plan — setup / use / monitor skills

**FR:** docs/feature-request-setup-use-monitor-skills-2026-09-22.md
**Issue:** #21

## Build

1. Add `.grok/skills/irc-skill-setup/SKILL.md`, `irc-skill-use/SKILL.md`, `irc-skill-monitor/SKILL.md`, `harvest-irc-skill/SKILL.md` (YAML `name:` + triggers + MUST NOT).
2. Keep `.grok/skills/irc-skill/SKILL.md` as the index; point at the three jobs + harvest.
3. Teach `scripts/install_skill.py` to copy every new leaflet (temp `GROK_HOME` must receive them).
4. Extend `tools/Validate-IrcSkill.ps1` for A1–A3 (missing leaflet = FAIL).
5. README: setup / use / monitor / harvest. Seed `docs/skill-harvest-log.md`.
6. Do not implement #20 UI. Do not add an exe kit. No live Ergo in CI.

## Test

- `Validate-IrcSkill.ps1` exit 0 with all four leaflets; fails if one is deleted (can be a pytest that invokes the validator or a small install-to-temp test).
- Existing `python -m pytest tests/ -q` and `Test-IrcClientParse.ps1` stay green.
- Optional: `install_skill.py` with `GROK_HOME` = temp dir; assert the four `SKILL.md` dest files.
- No live server. No UAT stamp.

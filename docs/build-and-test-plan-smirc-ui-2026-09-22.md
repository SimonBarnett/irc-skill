# Build/test plan: SMIRC-like UI (#20)

1. Survey current irc-skill tree + any UI stubs.
2. Park/implement independently testable UI matching A1–A4.
3. Add/adjust tests or BT0 validate path.
4. Open PR linking #20.

## Delivered paths

| Path | Role |
|------|------|
| `ui/smirc/` | Static SMIRC layout (channels left, tabs bottom, users right) |
| `docs/smirc-ui-layout.md` | Layout MUST + DM/SEAL/file UNKNOWN gates |
| `scripts/smirc_ui_serve.py` | Independent test server (`--demo`, `--check-only`) |

## BT0 (no live IRC)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-SmircUi.ps1
python -m pytest tests/test_smirc_ui.py -q
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-IrcSkill.ps1
python -m pytest tests/ -q
```

Manual: `python scripts/smirc_ui_serve.py --demo` → open printed URL; drag an image onto **Drop image**; open a user **DM** and hit SEAL/File stubs.
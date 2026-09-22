# SMIRC-like UI layout (#20)

**Issue:** https://github.com/SimonBarnett/irc-skill/issues/20  
**FR:** [feature-request-smirc-ui-2026-09-22.md](feature-request-smirc-ui-2026-09-22.md)

This document locks the **MUST** layout for the irc-skill SMIRC-parity surface. Live IRC wiring remains P2 / compose; demo mode needs no server credentials.

## MUST (A1)

| Region | Placement | Test hook |
|--------|-----------|-----------|
| Channel list | Vertical column on the **left** | `data-testid="smirc-channel-list"` |
| Chat transcript + input | **Center** main pane | `data-testid="smirc-chat-pane"` |
| User list | Vertical column on the **right** | `data-testid="smirc-user-list"` |
| Open chats | **Tabs along the bottom** (one tab per buffer) | `data-testid="smirc-chat-tabs"` |

Channels sort alphabetically in demo; selecting a channel opens or focuses its tab. Users in the right rail are scoped to the active channel buffer in demo.

## DM, SEAL, file transfer (A2)

Direct-message tabs use the same bottom tab strip (`/msg nick` semantics in product terms).

| Action | UI entry | Wire / gate |
|--------|----------|-------------|
| Open DM | Double-click user or **DM** on user row | Demo: local tab only. Live: **UNKNOWN** until UI binds `irc_client.py` stdin/outbox. |
| SEAL | **SEAL** on DM tab toolbar | Delegates to `scripts/irc_seal.py` + agentic_irc; live path **UNKNOWN** in this scaffold. |
| File offer | **File** on DM tab toolbar | Delegates to `scripts/irc_filexfer.py offer`; live path **UNKNOWN** in this scaffold. |

No passwords or API keys in the UI repo; operators use `AGENTIC_IRC_*` env or CLI on the Python client.

## Image drag into chat (A3)

The chat input area accepts file drops. In demo, a dropped image is shown inline as a preview attachment line in the transcript.

| Hook | Purpose |
|------|---------|
| `data-testid="smirc-image-drop"` | Drop target on the compose row |
| `window.__smircLastDrop` | Test hook: `{ name, type, size }` of last accepted image drop (browser only) |

Upload to IRC wire is **UNKNOWN**; demo records intent only.

## Independent test entry (A4)

From repo root:

```bash
python scripts/smirc_ui_serve.py --demo
```

Then open the printed URL (default `http://127.0.0.1:8765/`). Static assets live under `ui/smirc/`.

BT0 (no browser required):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-SmircUi.ps1
python -m pytest tests/test_smirc_ui.py -q
```

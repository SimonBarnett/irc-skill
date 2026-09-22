# FR: Independent SMIRC-like IRC UI (issue #20)

**Issue:** https://github.com/SimonBarnett/irc-skill/issues/20  
**Ask (Simon):** Where is the UI — independently testable with all UI
(channels down left, chats as tabs at the bottom) like SMIRC; user list;
direct messaging UI for seal and file transfer; drag images into chat.

## Summary

Deliver (or skill-document + scaffold) an independently testable IRC client
UI matching SMIRC layout conventions:
- Channel list on the left
- Chat panes as tabs at the bottom
- User list
- DM UI supporting seal + file transfer
- Drag-and-drop images into chat

## Gap vs master

irc-skill today is agent skill / tooling oriented; no SMIRC-parity UI surface
is parked as MUST. This FR locks the UI product ask for MRB.

## Acceptance

- A1: Documented UI layout MUST (left channels, bottom chat tabs, user list).
- A2: DM path for seal + file transfer described or stubbed with UNKNOWN gates.
- A3: Image drag-into-chat called out with test hook or UNKNOWN.
- A4: Independently testable entry (script, web, or desktop) referenced from README/docs.
- A5: No invented credentials or server secrets.

Workers do not stamp ready for human UAT.
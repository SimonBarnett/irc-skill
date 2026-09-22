# Build and test plan — interactive chat

**FR:** docs/feature-request-interactive-chat-2026-09-22.md

pytest: inject PRIVMSG into `on_line`, assert a printed FROM-like line; assert send helper emits `PRIVMSG #chan :text`. Existing parse/dry-run tests stay green. Validate-IrcSkill.ps1 still 0. No live server in CI.

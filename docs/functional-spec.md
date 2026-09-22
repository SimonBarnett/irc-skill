# Functional spec: IRC client as a skill (LOCKED)

**Product:** `SimonBarnett/irc-skill` — an IRC client that operators and agents **install as a skill**, not a family of ported executables shipped around like 1990s shareware.

**Source:** Simon Query to `marchhare-23624` 2026-09-22: new repo containing the functional spec for an IRC client installed as a skill, rather than porting exes around like the 90s.

**MRB home:** GitHub issue #1 in this repo (opened with this park).

This is a **new product**. It is not a rewrite of `SimonBarnett/agentic_irc` (TLS fleet connector, SEAL, talk seats). That repo stays the wire kit unless a later FR says otherwise.

## LOCKED

| ID | Requirement |
|----|-------------|
| L1 | New public repo `SimonBarnett/irc-skill` holds the functional spec under `/docs`. |
| L2 | The product is an **IRC client**. |
| L3 | Distribution is a **skill** (installable agent skill pack: `SKILL.md` + scripts/docs the agent follows). |
| L4 | **Not** a 1990s port model: do not ship or copy around per-OS / per-arch standalone `exe` drops as the way to get a client. |
| L5 | Spec lives at `docs/functional-spec.md`. Feature requests are extra `docs/feature-request-*.md` + issues labeled `feature-request`. |
| L6 | No secrets in git. Do not commit passwords, Ergo PASS, or API key assignments. |
| L7 | Workers do not stamp ready for human UAT. Bob only. |

## MUST NOT

| ID | Rule |
|----|------|
| N1 | Replace `agentic_irc` fleet connector / SEAL / talk-seat TSR without a later FR. |
| N2 | Invent instance URLs, nicks, or credentials. |
| N3 | Generate review PDFs. Keep a source PDF only if one was supplied (none was). |
| N4 | Port or vendor a pile of platform `exe`s as the install story. |

## UNKNOWN

| ID | Item |
|----|------|
| U1 | UI surface (TUI, GUI, Halloy replacement, or agent-driven only). |
| U2 | Protocol scope (generic IRC vs fleet Ergo `irc.ntsa.uk:6697` only). |
| U3 | Implementation language and runtime. |
| U4 | How this skill composes with `agentic_irc` scripts vs a clean client. |
| U5 | Mode 3 / `airc-moot-thin.exe` field path — stay or fold later. |
| U6 | Channels, SASL, and nick rules beyond what `agentic_irc` already locks. |

## Acceptance IDs

| ID | Acceptance |
|----|------------|
| A1 | This markdown is on `main` at `docs/functional-spec.md`. |
| A2 | Issue #1 is the MRB home and links this file. |
| A3 | README points at the spec. |
| A4 | No platform `exe` tree is the documented install path. |
| A5 | Phase 0 does not implement a client until Simon says go / dispatch. |

## Phase order

| Phase | Deliverable |
|-------|-------------|
| P0 | Park this spec + issue #1 (this commit). |
| P1 | Skill leaflet + install story (no port-exe kit). |
| P2 | Client behaviour vs LOCKED/UNKNOWN once Simon fills U1–U6 or says go. |

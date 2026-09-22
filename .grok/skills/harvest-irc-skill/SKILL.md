---
name: harvest-irc-skill
description: >
  CAST IRON harvest for SimonBarnett/irc-skill: write repeatable client learnings
  into this repo .grok/skills and docs/skill-harvest-log.md. Use when you learn
  something about the IRC client skill product, harvest irc-skill, CAST IRON
  irc-skill, or /harvest-irc-skill. Wire/TSR/Ergo playbooks stay agentic_irc.
---

# harvest-irc-skill

**Foundation skill** for [SimonBarnett/irc-skill](https://github.com/SimonBarnett/irc-skill). Fleet CAST IRON routing: client-as-skill harvests **here**; Ergo, talk seats, SEAL wire, moot, Halloy harvest to **agentic_irc** (`harvest-agent-skills` table).

## When to harvest

During the job, if you learned a **repeatable** procedure about **this client** (install, setup, use, monitor, compose wrappers):

1. Edit or add `.grok/skills/*/SKILL.md` in **this** repo (one home per fact).
2. Append a dated line to `docs/skill-harvest-log.md`.
3. Commit and push on a work branch / PR — not `main` unless your process says otherwise.

**Empty harvest: no commit.** Do not commit "nothing found".

## Do not harvest here

- Ergo firewall, Watch-Bobiverse, invite-airc, dumb agent, moot chair — **agentic_irc**.
- Bob fleet / MRB / build loop — **agentic_build** (`harvest-agent-skills`).

## Write rules

- Frontmatter `name:` matches folder name.
- Triggers in `description`. ASCII in body.
- Run `tools/Validate-IrcSkill.ps1` after skill edits.

## MUST NOT

- Force-push, secrets, `password=` / `XAI_API_KEY=` in git.
- Claim ready for human UAT.
- Duplicate agentic_irc wire docs in this repo.

## Triggers

harvest irc-skill, CAST IRON irc client, skill harvest this repo, /harvest-irc-skill.

---
id: 1
title: "Should the desktop build move to Electron Forge?"
status: resolved
opened: 2018-01-01
decision_ref: null
---

Tracked as issue #632: a request to integrate Electron Forge, blocked on
two upstream Forge issues (`electron/forge#1041`, configuring the
executable output directory; `electron/forge#3457`, `npm install`
modifying `.zshrc`). Closed **not planned** — the upstream blockers were
never the real question; `electron-builder` (already in use per
`decisions/0001`) kept doing the job.

`decision_ref` is left `null` on purpose: this didn't graduate into an ADR
of its own. The standing decision is still `decisions/0001` — Forge was
one alternative considered against it, and the project's own tooling
(`electron-builder.json` in `publish/`) is the record of what was actually
kept.

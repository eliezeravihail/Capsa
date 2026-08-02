---
name: electron-updater
version: "6.8.9"
ecosystem: npm
license: MIT
tier: allow
direct: true
decision_ref: null
added: 2017-11-17
links:
  - {rel: depends_on, to: decisions/0001-electron-for-desktop-app}
---

The only production `dependencies` entry in `package.json` — everything
else the app ships is either bundled Electron itself or a devDependency.
Handles auto-update for the desktop build. `decision_ref` stays `null`:
that field is for the decision that *admits* a `review`/`deny`-tier
dependency (SPEC §4.6), and MIT needs no admission at `allow` tier — the
`depends_on` link records why this package exists here without
overloading a field that means something more specific.

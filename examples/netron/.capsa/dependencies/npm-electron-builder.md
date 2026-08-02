---
name: electron-builder
version: "26.15.3"
ecosystem: npm
license: MIT
tier: allow
direct: true
decision_ref: null
added: 2017-11-16
---

devDependency: packages the Electron app into the per-platform installers
`publish/electron-builder.json` configures — `.dmg`/`.zip` (macOS),
`.deb`/`.rpm` (Linux, per `decisions/
0002-linux-packaging-deb-and-rpm-only.md`), `nsis` (Windows).

---
id: 5
title: "Ship a native desktop app for macOS, Linux, and Windows"
level: must
status: met
opened: 2017-11-16
verification:
  status: verified
  method: manual
  evidence_ref: "publish/electron-builder.json; releases/0003-v9.2.0.md lists .dmg/.deb/.rpm/.exe artifacts"
  checked_at: 2026-08-02
links:
  - {rel: implements, to: components/viewer/components/desktop/component}
  - {rel: constrained_by, to: decisions/0002-linux-packaging-deb-and-rpm-only}
---

README.md's install section names a download for each of macOS (`.dmg`,
or `brew install --cask netron`), Linux (`.deb`/`.rpm`), and Windows
(`.exe`, or `winget install`). `opened` is dated to `Add package.json`
(2017-11-16), the commit that starts the Electron build's paper trail —
see `decisions/0001-electron-for-desktop-app.md` for why Electron
specifically, and `decisions/0002` for how the Linux side of this
requirement changed shape without changing what it demands.

---
title: "Desktop host"
status: active
created: 2017-11-22
code_globs: ["source/desktop.mjs", "publish/**"]
links:
  - {rel: implements, to: requirements/0005-desktop-app-distribution}
  - {rel: constrained_by, to: decisions/0001-electron-for-desktop-app}
---

The Electron wrapper around the browser view, packaged per
`publish/electron-builder.json` into native installers for macOS, Linux,
and Windows.

**Boundaries.** Owns window chrome, native menus, auto-update
(`electron-updater`), and file-association handling. Never touches format
parsing — that stays in `components/formats/`.

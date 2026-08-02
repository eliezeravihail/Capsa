---
id: 1
title: "Build the desktop app on Electron, wrapping the same browser view"
status: accepted
date: 2017-11-22
supersedes: null
superseded_by: null
discussion_ref: null
tags: [desktop, architecture]
---

## Context

The project already had a working browser-based viewer
(`source/browser.js`). Native installers were wanted for macOS, Linux, and
Windows without maintaining a second UI implementation.

## Decision

Wrap the existing browser view in Electron rather than write native UI per
platform. `Add Electron view wrapper` (2017-11-22) and `App.js to load
view-electron.html` (2017-11-22) are the first commits of the desktop
build; `publish/electron-builder.json` (added the same month) configures
the per-platform packaging on top of it.

## Consequences

One rendering codebase serves the browser, the desktop app, and (via
`source/server.py`) the local Python-served page. A UI bug fixed once is
fixed in all three. The cost is carried by `electron-updater` (production
dependency, `dependencies/npm-electron-updater.md`) and by
`electron`/`electron-builder` in devDependencies — the desktop build's
only real dependency weight.

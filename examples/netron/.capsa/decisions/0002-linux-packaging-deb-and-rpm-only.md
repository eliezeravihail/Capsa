---
id: 2
title: "Linux: ship .deb and .rpm only — drop AppImage and Snap"
status: accepted
date: 2025-12-26
supersedes: null
superseded_by: null
discussion_ref: null
tags: [desktop, linux, packaging]
---

## Context

Netron had shipped AppImage, Snap, `.deb`, and `.rpm` builds for Linux.
Issue/PR #1500 ("Linux Support") states two independent problems: AppImage
builds broke on an upstream Electron issue
(`electron/electron#42510`), and Snap was dropped for "maintenance
complexity" — a judgment call, not a forcing bug, and recorded as one.

## Decision

Ship `.deb` (Debian/Ubuntu) and `.rpm` (Fedora/Red Hat) only.
`publish/electron-builder.json`'s `linux.target` lists exactly
`[{"target":"deb"},{"target":"rpm"}]` — no `AppImage`, no `snap`. Commits
`Remove AppImage arm64 support (#1500)` (2025-09-08) and `Remove Snap and
AppImage support (#1500)` (2025-12-26) carry this out.

## Consequences

Requirement 0005 ("ship a native desktop app for macOS, Linux, and
Windows") is unaffected — it names platforms, not package formats, and
still holds. A Linux user on a distribution that only consumes AppImage or
Snap packages loses a supported install path; the trade was made for
maintainer load on a single-maintainer project (`insights/dev/
single-maintainer.md`), not for a technical requirement on the format
side.

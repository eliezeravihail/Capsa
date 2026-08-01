---
title: "moov atom is written last, so a truncated file is unplayable"
kind: risk
severity: S3
status: triaged
source: agent
owner: david
opened: 2026-07-23
triaged: 2026-07-23
links:
  - {rel: affects, to: components/mux/component}
---

A recording interrupted by a crash or a full disk leaves the `moov` atom
unwritten, and the whole file is unreadable — not merely truncated. Faststart
(moov first) costs a second pass; a periodic flush costs nothing but only
recovers to the last flush.

Filed as a risk rather than a bug: current behaviour matches the format, and
the loss only shows up on an abnormal exit. Named here because it is the
component's most likely way to fail a user.

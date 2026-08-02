---
title: "moov atom is written last, so a truncated file is unplayable"
kind: risk
severity: S3
status: triaged
source: "an agent, reviewing failure-mode coverage"
owner: sam
opened: 2026-07-23
triaged: 2026-07-23
links:
  - {rel: affects, to: interfaces/recording-format}
---

A recording interrupted by a crash or a full disk leaves the `moov` atom
unwritten, and the whole file is unreadable — not merely truncated. Faststart
(moov first) costs a second pass; a periodic flush costs nothing but only
recovers to the last flush.

Filed as a risk rather than a bug: current behaviour matches the format, and
the loss only shows up on an abnormal exit. Named here because it is the
component's most likely way to fail a user.

That it affects the muxer is not written down anywhere in this file — the file
is *inside* `components/mux/`, and a link saying so would restate the path
(SPEC §5.13). The one link is the fact the tree cannot hold: the risk reaches
past this component to the format promise made at the root.

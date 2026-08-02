---
title: "Capture"
status: active
created: 2026-07-01
code_globs: ["src/capture/**"]
tags: [core]
---

Grabs frames from the screen and hands them to the muxer with a monotonic
timestamp attached.

**Boundaries.** Owns frame acquisition and timing. Knows nothing about
container formats or encoding — it produces frames, not files.

**Interfaces.** `capture.stream()` yields `(frame, timestamp)`.

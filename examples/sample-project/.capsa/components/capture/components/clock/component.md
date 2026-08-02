---
title: "Capture clock"
status: active
created: 2026-07-01
code_globs: ["src/capture/clock.py"]
links:
  - {rel: anchored_to, to: insights/code/frame-timing}
---

The monotonic time source every frame timestamp derives from. Split out of
capture because the A/V desync class of bugs all traced back to it, and a
part with its own failure history is worth naming.

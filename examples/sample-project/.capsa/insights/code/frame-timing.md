---
kind: code
title: "Frame timestamps must come from the capture clock, not wall time"
created: 2026-07-22
updated: null
code_globs: ["src/capture/clock.py", "src/capture/loop.py"]
tags: [timing]
links:
  - {rel: anchored_to, to: components/capture/components/clock/component}
---

Wall-clock timestamps drift under load and produced the A/V desync class of
bugs. All frame timing flows from the monotonic capture clock; if you touch
these files, preserve that invariant.

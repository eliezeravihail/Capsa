---
title: "Muxer"
status: active
created: 2026-07-01
code_globs: ["src/mux/**"]
links:
  - {rel: depends_on, to: components/capture/component}
---

Writes frames into a container. Owns everything about the file on disk:
atom layout, offsets, finalisation.

**Boundaries.** Never touches timing — a timestamp arrives with the frame
and is written as given.

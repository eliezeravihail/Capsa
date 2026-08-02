---
title: "Muxer"
status: active
created: 2026-07-01
code_globs: ["src/mux/**"]
links:
  - {rel: depends_on, to: ../capture/component}
---

Writes frames into a container. Owns everything about the file on disk:
atom layout, offsets, finalisation.

**Boundaries.** Never touches timing — a timestamp arrives with the frame
and is written as given.

The dependency on `capture` is a sibling edge: in the tree the two are the
same distance from the root, which says nothing about one needing the other.
It is written relatively (`../capture/…`) because both ends live under
`components/` — move that directory and the edge is still true and still
resolves.

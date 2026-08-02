---
title: "Recording file format (MP4, faststart)"
status: stable
created: 2026-07-01
since: "1.0.0"
code_globs: ["src/mux/**"]
links:
  - {rel: exposes, to: components/mux/component}
---

What a recording produced by this tool is, as a promise to anything that reads
one: MP4, H.264 video, AAC audio, `moov` atom first.

Its own record because the promise outlives any one release: a file written by
1.0 must still open in 3.0, and a consumer needs to know when that promise
changed, not to infer it from a changelog.

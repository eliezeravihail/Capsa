---
title: "MLIR"
status: active
created: 2023-05-07
code_globs: ["source/mlir.js"]
links:
  - {rel: implements, to: requirements/0003-experimental-format-support}
---

**Experimental tier (README.md)**, not production — stated here in prose
because `status` has no `experimental` value (`components/formats/
component.md` explains why). `active` describes that the component
exists and is maintained, not that it carries the same support bar as
`components/formats/components/onnx`.

First added 2023-05-07, then extended by many further commits reusing the
same PR/issue number (`Add MLIR support (#1044)`) through 2026 — MLIR
support grew dialect-by-dialect rather than landing complete in one
change; `requirements/0003-experimental-format-support.md` dates its own
`opened` to this same first commit.

---
title: "ONNX"
status: active
created: 2017-12-01
code_globs: ["source/onnx.js", "source/onnx-proto.js", "source/onnx-metadata.json"]
links:
  - {rel: implements, to: requirements/0002-support-primary-formats}
---

Production tier (README.md). The format used in README's own linked
sample model (squeezenet) — Netron's most-cited example format.
`issues/0001-unsigned-32-bit-integer-decoding.md` affected this parser
through the shared `components/serialization/` layer.

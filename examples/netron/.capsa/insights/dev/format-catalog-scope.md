---
kind: dev
title: "70 format parsers exist in source/; 8 got their own component record"
created: 2026-08-02
tags: [components, scope]
---

`source/*.js` holds one parser module per model format — roughly 70 of
them, from `acuity.js` to `xmodel.js`. `components/formats/` owns all of
them via `code_globs`, but only eight have their own nested
`components/formats/components/<slug>/` record: `onnx`, `pytorch`,
`tflite`, `keras`, `coreml`, `tensorflow`, `caffe` (README's "production"
tier), and `mlir` (README's "experimental" tier, as one worked example of
that status).

This is a scope choice made for this capsule, stated so it isn't mistaken
for completeness: the other ~62 formats are real, shipped, and covered by
`components/formats/component.md`'s `code_globs`, but do not have their
own component record naming their individual boundaries, dependencies, or
issues. A reader who needs `armnn` or `paddle` at component granularity
will not find it here — that's a gap in this capsule's coverage, not in
Netron.

---
title: "Formats"
status: active
created: 2017-11-01
code_globs: ["source/*.js", "source/*-metadata.json", "source/*-schema.js", "source/*-proto.js"]
---

Owns every format-specific parser module: one file per format
(`source/<format>.js`), most paired with a `-metadata.json` and/or
`-schema.js`/`-proto.js` file for that format's type definitions. Roughly
70 formats live here — see `insights/dev/format-catalog-scope.md` for
which ones got their own nested component record
(`components/formats/components/<slug>/`) and which are covered only by
this component's `code_globs`.

**Boundaries.** A format module reads bytes via `components/serialization/`
and produces a format-agnostic graph for `components/viewer/` to render.
It never renders anything itself and never reads another format's module.

**The production/experimental split.** README.md names two tiers:
production (ONNX, TensorFlow Lite, PyTorch, torch.export, ExecuTorch,
TorchScript, TensorFlow, Core ML, OpenVINO, Keras, Caffe, Darknet,
Safetensors, NumPy — `requirements/0002`) and experimental (MLIR, JAX,
GGUF, RKNN, ncnn, MNN, PaddlePaddle, scikit-learn — `requirements/0003`).
The component schema's `status` enum has no `experimental` value, so each
nested format component states its tier in prose rather than in a field
that doesn't have room for it.

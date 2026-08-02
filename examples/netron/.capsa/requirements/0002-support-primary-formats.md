---
id: 2
title: "Support the formats README lists as primary, at production quality"
level: must
status: met
opened: 2017-12-04
verification:
  status: verified
  method: test
  evidence_ref: "test/models.json + `npm test <format>` (CONTRIBUTING.md)"
  checked_at: 2026-08-02
links:
  - {rel: implements, to: components/formats/component}
---

README.md states plainly: "Netron supports ONNX, TensorFlow Lite, PyTorch,
torch.export, ExecuTorch, TorchScript, TensorFlow, Core ML, OpenVINO,
Keras, Caffe, Darknet, Safetensors and NumPy." Thirteen formats, no hedge —
this is the bar the project holds itself to, distinct from the
"experimental" list in requirement 0003.

`test/models.json` catalogs real sample model files per format, and
`CONTRIBUTING.md` documents `npm test [format]` as the way to validate a
change against them — this is the checkable form of "supported": a format
without a passing entry here does not meet this requirement's bar for
that format specifically.

---
title: "PyTorch"
status: active
created: 2018-01-01
code_globs: ["source/pytorch.js", "source/pytorch-metadata.json"]
links:
  - {rel: implements, to: requirements/0002-support-primary-formats}
---

Production tier (README.md). README additionally lists `torch.export`,
`ExecuTorch`, and `TorchScript` as separate named formats — related to
PyTorch but each with its own parser module (`executorch.js`, and
TorchScript handled within `pytorch.js`), not folded into this component.

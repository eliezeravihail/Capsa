---
title: "Keras"
status: active
created: 2017-12-15
code_globs: ["source/keras.js", "source/keras-proto.js", "source/keras-metadata.json"]
links:
  - {rel: implements, to: requirements/0002-support-primary-formats}
---

Production tier (README.md). README's own linked sample model for this
format (mobilenet.h5) is read through `components/serialization/`'s
`hdf5.js` — Keras's legacy `.h5` save format.

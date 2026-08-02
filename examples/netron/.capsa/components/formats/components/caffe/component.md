---
title: "Caffe"
status: active
created: 2017-12-01
code_globs: ["source/caffe.js", "source/caffe-proto.js", "source/caffe-metadata.json"]
links:
  - {rel: implements, to: requirements/0002-support-primary-formats}
---

Production tier (README.md). Caffe2 is a separate module
(`caffe2.js`/`caffe2-proto.js`/`caffe2-metadata.json`) not covered by this
component — README does not list Caffe2 among the named formats, so it
sits under `components/formats/component.md`'s general `code_globs`
without a nested record of its own, same as the ~62 formats
`insights/dev/format-catalog-scope.md` accounts for.

---
title: "Serialization"
status: active
created: 2017-11-01
code_globs: ["source/protobuf.js", "source/flatbuffers.js", "source/flexbuffers.js", "source/json.js", "source/xml.js", "source/zip.js", "source/tar.js", "source/gzip.js", "source/hdf5.js", "source/hickle.js", "source/pickle.js", "source/python.js"]
---

The shared codec layer every format parser in `components/formats/` reads
through: protobuf and flatbuffers decoding, container formats (zip, tar,
gzip, hdf5), and Python's own serialization formats (pickle) since several
frameworks ship models as pickled Python objects.

**Boundaries.** Format-agnostic by construction — nothing here knows
what an ONNX tensor or a Keras layer is, only how to decode the bytes.
`issues/0001-unsigned-32-bit-integer-decoding.md` is filed here (and
cross-linked to the one format component it visibly broke) because the
defect was in this shared layer, not in any one format's own code.

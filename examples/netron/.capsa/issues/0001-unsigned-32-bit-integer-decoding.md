---
id: 1
title: "Unsigned 32-bit integer decoding was wrong across several parsers"
kind: bug
severity: S2
status: closed
source: system
owner: "Lutz Roeder"
opened: 2026-01-08
triaged: 2026-01-08
closed: 2026-01-08
fix_commit: "c15eb34be730d1e23d586e733dc9844404a50808"
regression_ref: "test/backend.py::_test_onnx_iterate (npm test onnx)"
reopens: 0
links:
  - {rel: affects, to: components/serialization/component}
  - {rel: affects, to: components/formats/components/onnx/component}
---

Commit `c15eb34` ("Fix unsigned 32-bit integer decoding") touches four
files in one change: `source/python.js`, `source/onnx.js`,
`source/megengine.js`, `source/ncnn.js`. The same decoding mistake was
copied into (or shared by) parsers for three unrelated formats — evidence
that this is a shared-primitive class of bug, not a per-format one, which
is why it's filed at the capsule root rather than under any single
format's `issues/`: no one component owns it.

`severity: S2` is this capsule's judgment, not a value read off GitHub —
the real repository does not expose severity levels, so this is the
clearest honest example of a field this capsule had to infer rather than
find. Wrong integer decoding silently produces a wrong graph rather than a
crash, which is worse than S1's usual "won't open at all", but it's
scoped to specific tensor shapes, not universal — hence S2, not S1.

**`regression_ref` needed a real decision, not just a lookup.** The fix
commit touches no test file — there is no regression test written
*for this defect*. The validator enforces SPEC §4.5's rule mechanically
(`E-ISSUE-NOREGRESSION`: a closed bug without `regression_ref` is
non-conforming), so leaving it empty, which would have been the honest
answer, is not an option the format accepts. The value here is the
closest real evidence that exists: `test/backend.py::_test_onnx_iterate`,
the general ONNX-parsing test `npm test onnx` runs, which happens to
exercise the same decode path — not a test that specifically encodes
"unsigned 32-bit integers must not overflow." If this exact bug came
back, this test might not catch it; a crash-on-parse bug, it would.

That gap — a mechanically-enforced field whose presence the validator
checks, but whose *meaning* ("this specific defect is now guarded against
regressing") nothing checks — is real enough to be worth reporting to
Capsa itself rather than papering over here. See
`.capsa/issues/` in the Capsa repository (opened as part of this
exercise) for the write-up.


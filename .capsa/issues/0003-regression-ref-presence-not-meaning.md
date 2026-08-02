---
id: 3
title: "Validator checks a closed bug's regression_ref is present, not that it actually guards against the defect"
kind: risk
severity: S3
status: rejected
source: "Claude, AI agent — Netron capability-test session"
owner: null
opened: 2026-08-02
triaged: 2026-08-02
closed: 2026-08-02
fix_commit: null
fix_plan_ref: null
regression_ref: null
reopens: 0
---

Found authoring `examples/netron/.capsa/issues/
0001-unsigned-32-bit-integer-decoding.md`. The real fix commit
(`c15eb34`) touches no test file — there is no regression test written
*for this specific defect*, only a pre-existing general parse test
(`test/backend.py::_test_onnx_iterate`) that happens to exercise the same
code path and would not necessarily catch a silent wrong-value bug the
way it would catch a crash.

`check_record_dirs` (`tools/validator/validate.py`) enforces SPEC §4.5's
rule mechanically: `E-ISSUE-NOREGRESSION` fires if `regression_ref` is
absent on a closed bug. It checks that the field is non-empty — a string
is present — never that the string names something that would actually
fail if the defect reappeared. A citation to unrelated or
loosely-related test coverage satisfies the checkable claim just as
well as a real regression test would, which means "no closed bug without
regression_ref" is currently a weaker guarantee than SPEC's own framing
("closure evidence in checkable form") implies: it verifies the shape of
an answer, not the answer.

## Rejected — 2026-08-02

The premise was wrong, not just the fix. Capsa is a documentation format,
not an enforcement mechanism — the same relationship a PDF has to its
reader: a PDF validator confirms the file is well-formed, never that the
invoice total inside it is correct. Asking the same of `regression_ref`
was asking the validator to verify that a citation is *true* (that it
really guards this defect), when its actual and only job is to verify
that the record is *shaped* correctly (a citation is present, in the
field meant to hold one).

A capsule where `regression_ref` cites weak or unrelated coverage is
exactly a "broken document" in the PDF sense: the format was followed,
the content is wrong, and that is a fact about whoever wrote the record —
visible to a human reader, exactly as intended — not a defect in the
format or a gap the validator failed to close. Nothing here needs
building. `insights/dev/format-is-not-enforcement.md` records the
principle so it doesn't get relitigated as a bug report again.

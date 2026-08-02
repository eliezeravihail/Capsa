---
id: 3
title: "Validator checks a closed bug's regression_ref is present, not that it actually guards against the defect"
kind: risk
severity: S3
status: triaged
source: agent
owner: null
opened: 2026-08-02
triaged: 2026-08-02
closed: null
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

Not proposing a fix here — verifying that a cited test actually exercises
the fixed code path is likely undecidable in general (it would require
running the test against the pre-fix code and confirming it fails, which
the read-only validator by design does not do). Filed so the limit of
what this check actually guarantees is a visible fact instead of an
implied one — the same principle SPEC §2.3 already applies to
verification blocks generally.

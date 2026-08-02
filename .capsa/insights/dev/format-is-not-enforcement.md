---
kind: dev
title: "Capsa documents; it does not enforce — the validator checks shape, never truth"
created: 2026-08-02
tags: [validator, method]
links:
  - {rel: learned_from, to: issues/0003-regression-ref-presence-not-meaning}
---

A format that checks its own conformance is not the same thing as a
format that guarantees the reality its records describe. PDF is the clean
comparison: a PDF validator confirms the file is well-formed; it has and
needs no opinion on whether the invoice total on page 4 is correct. A
document that follows the format but states something false is a broken
*document*, not evidence the format needs more rules.

Capsa's validator draws the same line. It checks that a `regression_ref`
is present on a closed bug (SPEC §4.5) — a shape check: does the field
hold a citation. It was never checking, and structurally cannot check,
whether that citation actually guards the specific defect. A capsule
where the citation is weak or unrelated is a capsule someone wrote
carelessly, exactly as a PDF with a wrong invoice number is a document
someone typed carelessly — visible to a reader, not a validator defect.

**The test going forward, before filing a gap as a Capsa issue:** does
the format lack *vocabulary* to write something true (no field or address
form exists to state it, so the author is forced into prose or a false
value)? That's a real gap — `issues/0001` (no honest `source` value for a
solo maintainer) and `issues/0002` (no structured way to cite an external
source) are both this kind. Or does the validator merely fail to catch a
*false statement made in valid shape*? That's not a gap — no validator
for any format does that, and asking Capsa's to is asking it to stop
being a passive format and start being the enforcement mechanism
principle 1 already rules out.

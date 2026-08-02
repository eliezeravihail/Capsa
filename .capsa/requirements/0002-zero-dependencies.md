---
id: 2
title: "The reference validator is dependency-free"
level: must
status: met
opened: 2026-08-02
verification:
  status: verified
  method: test
  evidence_ref: "tools/validator/validate.py"
  checked_at: 2026-08-02
---

`tools/validator/validate.py` runs on the standard library alone, PyYAML
used when present and a stdlib-only mini-parser otherwise. The format is
the contract; a checker should never be a prerequisite for reading one.
Both parser paths are asserted to produce identical findings.

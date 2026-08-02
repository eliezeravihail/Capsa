---
id: 1
title: "Record the screen with pause/resume"
level: must
status: met
opened: 2026-07-02
verification:
  status: verified
  method: test
  evidence_ref: "tests/test_capture.py::test_pause_resume"
  checked_at: 2026-07-20
scoped_status:
  - {scope: requirements/0002-run-on-macos, status: unmet}
targets:
  - {metric: pause_resume_gap_ms, op: "<=", value: 40, unit: ms}
plan_refs: [1]
decision_refs: [1]
---

The core promise: a user can start a recording, pause it mid-way, resume,
and end with a single continuous file.

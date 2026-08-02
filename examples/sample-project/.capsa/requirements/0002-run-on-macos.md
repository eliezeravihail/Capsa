---
id: 2
title: "Record on macOS as well as Windows"
level: should
status: unmet
opened: 2026-07-02
verification:
  status: unverified
  method: none
  evidence_ref: null
  checked_at: null
---

Windows is the primary target. macOS is wanted but not blocking, which is why
this is `should` and not `must`.

Filed as a requirement rather than as a "platform" record, because that is
what it is: a constraint on the code. Where a platform needs code of its own,
that code is a component and gets a component record. Other requirements name
this one in `scoped_status` when they hold on Windows but not here.

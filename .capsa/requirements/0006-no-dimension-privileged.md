---
id: 6
title: "The format names no dimension of variation"
level: must
status: met
opened: 2026-08-02
verification:
  status: verified
  method: manual
  evidence_ref: "project/SPEC.md#2.5"
  checked_at: 2026-08-02
links:
  - {rel: implements, to: decisions/0002-no-record-type-per-dimension}
---

No record type exists for "platform", "language", "region", or any other
axis a product might vary along. A constraint on the code is a requirement
of the code; where it has code of its own, that code is a component. A
type per dimension has no principled end.

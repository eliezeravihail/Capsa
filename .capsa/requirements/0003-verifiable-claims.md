---
id: 3
title: "A claim subject to compliance checking is a field, not prose"
level: must
status: met
opened: 2026-08-02
verification:
  status: verified
  method: manual
  evidence_ref: "core/PRINCIPLES.md#Grammar"
  checked_at: 2026-08-02
---

A license tier, a requirement's satisfaction, an issue's closure evidence,
a release's contents — each is a structured frontmatter field with an
evidence reference. `status: verified` without `evidence_ref` is
non-conforming (SPEC §2.3); a missing verification block reads as
`unverified`, never as an implied pass.

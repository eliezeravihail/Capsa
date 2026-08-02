---
id: 4
title: "Placement determines applicability — no record declares its own scope"
level: must
status: met
opened: 2026-08-02
verification:
  status: verified
  method: manual
  evidence_ref: "core/PRINCIPLES.md#Placement"
  checked_at: 2026-08-02
links:
  - {rel: implements, to: decisions/0001-placement-determines-applicability}
---

A record applies to the node holding it and to everything beneath it; a
root record applies capsule-wide. What binds a node is derived by walking
from it to the root — never declared with a scope field, a glob, or an
`applies_to`. Filing the record correctly is what states its scope.

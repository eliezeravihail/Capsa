---
id: 1
title: "The format is passive — no active mechanism of any kind"
level: must
status: met
opened: 2026-07-29
verification:
  status: verified
  method: manual
  evidence_ref: "SPEC.md#1-principles (§1.1); repo contains no executable but the read-only validator"
  checked_at: 2026-07-29
plan_refs: [1]
decision_refs: [1]
---

A capsule must be data only. Nothing in the standard may run on its own;
consumers bring their own behavior.

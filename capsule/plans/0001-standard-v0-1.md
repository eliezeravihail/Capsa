---
id: 1
title: "Author the v0.1.0 standard: spec, schemas, templates, example, validator"
kind: initiative
status: completed
opened: 2026-07-29
completed: 2026-07-29
priority: P1
milestone: "v0.1.0"
requirement_refs: [1, 2, 3]
decision_refs: [1, 2]
---

## Goal
First complete, self-consistent version of the standard.

## Work breakdown
- [x] REQUIREMENTS.md ledger
- [x] SPEC.md normative format
- [x] schema/ (9 JSON Schemas)
- [x] templates/ + examples/sample-capsule
- [x] validator (read-only, stdlib-only), calibrated known-good/known-bad

## Verification
`python3 validator/validate.py examples/sample-capsule` → conforming.

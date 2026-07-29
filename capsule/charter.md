---
updated: 2026-07-29
---

# Charter — Capsa

## Vision
A standard, passive, portable file format for a project's management
capsule — requirements, plans, decisions, discussions, issues,
dependencies & licenses, releases, insights — readable by humans and
machines from plain files inside the project's own repository.

## Constraints
- No active mechanism, ever: no hooks, daemons, or services (only an
  optional read-only validator).
- Zero dependencies: stdlib-only tooling; the format is the contract.
- Checkable claims are formal fields with evidence references, not prose.

## Ground rules
- Source-of-truth order: SPEC.md > schema/ > validator/ > templates/ >
  examples/. Never patch the validator to accept what the spec forbids.
- Any spec change bumps capsa_version (SemVer).
- This capsule is the project's own record — Capsa is managed with Capsa.

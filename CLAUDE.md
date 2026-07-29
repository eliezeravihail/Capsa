# Capsa — working on this repository

This repository IS the Capsa standard: a passive file format for a
project-management capsule. There is deliberately no runtime here — do not
add hooks, daemons, services, or anything that runs on its own. The only
executable is the optional read-only validator.

- Source of truth order: SPEC.md > schema/ > validator/ > templates/ >
  examples/. A change starts at the spec and flows outward; never patch the
  validator to accept what the spec forbids.
- REQUIREMENTS.md is the requirement ledger. Struck-through lines are
  decisions, not garbage — never delete them.
- Any spec change bumps capsa_version per SPEC §6 and updates VERSION.
- Keep the example capsule conforming: run
  `python3 validator/validate.py examples/sample-capsule` before declaring
  work complete. Calibrate after validator changes: induce a known-bad,
  confirm it fails, restore.
- The validator must stay stdlib-only (PyYAML optional). No dependencies,
  ever — dependency-freedom is requirement B4, not a preference.

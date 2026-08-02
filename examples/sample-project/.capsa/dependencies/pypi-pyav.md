---
name: pyav
version: "12.0.5"
ecosystem: pypi
license: BSD-3-Clause
tier: allow
direct: true
decision_ref: null
hash: "sha256:0f1c3b7d8e9a4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5"
added: 2026-07-04
links:
  - {rel: constrained_by, to: "@acme/policies/license-tiers"}
---

Python bindings over FFmpeg used by the capture pipeline.

The `links` entry above is an **external** address (core §Addresses): the
licence policy that puts BSD-3-Clause in the `allow` tier is company-wide, so
it lives in the organization capsule and not here. It deliberately does not
resolve when this capsule is read alone, and that is not an error — a project
capsule ships inside its product repo and must stay valid wherever it lands.

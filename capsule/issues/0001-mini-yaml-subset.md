---
id: 1
title: "Built-in YAML mini-parser covers only the capsule subset"
kind: risk
severity: S3
status: triaged
source: system
owner: maintainer
opened: 2026-07-29
triaged: 2026-07-29
reopens: 0
---

Without PyYAML the validator falls back to a subset parser (flat keys,
inline lists, one nested block). Exotic-but-valid YAML frontmatter could
parse differently. Mitigation: keep templates within the subset; document
the subset; PyYAML is used when present.

---
id: 1
title: "Issue `source` enum (ceo | system | agent) has no honest value for an open-source maintainer or a community report"
kind: risk
severity: S3
status: triaged
source: agent
owner: null
opened: 2026-08-02
triaged: 2026-08-02
closed: null
fix_commit: null
fix_plan_ref: null
regression_ref: null
reopens: 0
---

Found authoring `examples/netron/.capsa/` — a capsule for a real,
external, single-maintainer open-source project
(github.com/lutzroeder/netron), built as a capability test.

Every issue's `source` field (SPEC §4.5) must be `ceo`, `system`, or
`agent`. All three assume an organizational structure this project — and
any solo-maintainer or community-driven open-source project — doesn't
have: there is no CEO, and the bug in
`examples/netron/.capsa/issues/0001-unsigned-32-bit-integer-decoding.md`
was found and fixed by the human maintainer himself, not by an automated
system and not by an AI agent. `system` was used there as the
least-inaccurate available value, which is exactly the failure mode a
closed enum should not have: a real fact with no honest field value to
hold it.

Not proposing a fix here — widening the enum (`maintainer`? `community`?
`external`?) is a real design decision about the org/company assumptions
baked into this record type, not a mechanical correction. Filed so the
gap is visible rather than silently worked around a second time.

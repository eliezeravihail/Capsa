---
id: 1
title: "Issue `source` enum (ceo | system | agent) has no honest value for an open-source maintainer or a community report"
kind: risk
severity: S3
status: closed
source: "Claude, AI agent — Netron capability-test session"
owner: null
opened: 2026-08-02
triaged: 2026-08-02
closed: 2026-08-02
fix_commit: "6191bf84760ee56d31b1712ff4a74bc14c3eac6f"
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

## Resolved — 2026-08-02

Widening the enum would have kept the same mistake in a bigger box —
whatever values got added, some real project would fall outside them
again. Checked first whether `source` was pulling weight anywhere else in
the spec: it isn't. No conformance rule reads it — unlike `severity` or
`status`, which gate real checks. A required field with a closed
vocabulary that does no checkable work, and forces a false answer when
reality doesn't fit, is exactly the pattern this project has been
removing all along (`platforms/`, `applies_to`).

**Fix:** `source` is now `string|null`, OPTIONAL, no enum — a name and a
capacity, e.g. `"Lutz Roeder, maintainer"`. This is documentation, not
enforcement or authority (`insights/dev/format-is-not-enforcement.md`),
so a name is exactly what it should hold. `project/SPEC.md` §4.5,
`tools/validator/validate.py`, and `project/templates/issue.md` all
updated; `examples/netron/.capsa/issues/
0001-unsigned-32-bit-integer-decoding.md`'s `source` now reads
`"Lutz Roeder, maintainer"` — accurate, not the closest available lie.

---
id: 2
title: "No structured way to cite an external, non-capsule source (a GitHub issue/PR, an RFC) as a decision's evidence"
kind: risk
severity: S3
status: closed
source: "Claude, AI agent — Netron capability-test session"
owner: null
opened: 2026-08-02
triaged: 2026-08-02
closed: 2026-08-02
fix_commit: null
fix_plan_ref: null
regression_ref: null
reopens: 0
---

Found authoring `examples/netron/.capsa/decisions/
0002-linux-packaging-deb-and-rpm-only.md`, a decision whose real-world
source is a public GitHub issue (lutzroeder/netron#1500) this capsule has
no capsule of its own to point at.

`links[].to` (core §Addresses) accepts an internal path or an external
`@capsule-slug/path` — another *Capsa capsule*. There is no third form for
"a URL to something that isn't a capsule at all": a GitHub issue, a
mailing-list thread, an RFC, a Stack Overflow answer someone actually
based a decision on. `ADDR` in the reference validator
(`tools/validator/validate.py`) would reject such a value outright — it
doesn't match the internal-path pattern, the relative-address pattern, or
the `@slug/...` pattern.

By contrast, a `verification` block's `evidence_ref` (core-adjacent, SPEC
§2.3) is explicitly documented as accepting "a path/commit/URL" — the
format already treats a bare URL as legitimate evidence in one place and
not in the other. The workaround used in the Netron capsule was prose (a
sentence in the decision's Context section naming the issue number),
which works for a human reader and is invisible to anything checking
links mechanically — exactly the gap `links` exists to close (core
§Links: "a checkable claim ... not prose").

## Resolved — 2026-08-02

Third address form, not a dedicated field: a `source_ref` would have
solved this for decisions and nothing else, when the same need — cite a
real, non-capsule source — applies to any record carrying `links`. **Web**
joins internal-absolute, internal-relative, and external-capsule (core
§Addresses, 0.6.0): `http://`/`https://`, recognized by prefix like every
other address form, checked for shape and never resolved — a network
request from a passive validator would violate principle 1 outright, so
this isn't "exempt like `@slug`," it's categorically excluded.

`examples/netron/.capsa/decisions/
0002-linux-packaging-deb-and-rpm-only.md` now carries
`links: [{rel: discussed_in, to: "https://github.com/lutzroeder/netron/pull/1500"}]`
in place of the prose citation that motivated this issue.

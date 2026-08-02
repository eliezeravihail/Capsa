---
id: 4
title: "The <ecosystem>-<name>.md filename rule is unsatisfiable for npm scoped packages"
kind: bug
severity: S2
status: closed
source: "Claude, AI agent — Netron capability-test session"
owner: null
opened: 2026-08-02
triaged: 2026-08-02
closed: 2026-08-02
fix_commit: "f17cb0f298093078692a2f48b67220191aed8704"
fix_plan_ref: null
regression_ref: "examples/netron/.capsa/dependencies/npm-@playwright--test.md — this real dependency stays in the corpus and fails E-DEP-NAME again if the escaping regresses"
reopens: 0
---

Found authoring `examples/netron/.capsa/dependencies/
npm-playwright-test.md` — a real dependency, `@playwright/test`, one of
five direct dependencies in Netron's own `package.json`. Reproduces
against the shipped validator, not a hypothetical:

```
$ python3 tools/validator/validate.py examples/netron/.capsa
E-DEP-NAME  examples/netron/.capsa/dependencies/npm-playwright-test.md:
  filename should be npm-@playwright/test.md (SPEC §2.2)
```

SPEC §2.2/§4.6 names a dependency file `<ecosystem>-<name>.md`, and
`check_record_dirs` (`tools/validator/validate.py`) enforces
`f.name == f"{eco}-{name}.md"` literally. A filesystem cannot hold `/` in
a filename, and npm's scoped-package convention (`@scope/name`) —
`@playwright/test`, `@babel/core`, `@types/node`, all common — puts a `/`
inside the one field the naming rule concatenates verbatim. There is no
escaping or sanitization rule in the spec for this case. The only
conforming options today are: pick a filename that no longer matches
`name` exactly (defeats the rule's own purpose — the filename is supposed
to be *derived from* the identity, not diverge from it), or accept
permanent non-conformance for any capsule that depends on a scoped npm
package, which is a large fraction of any real-world JavaScript project's
dependency tree.

This is the one finding from the Netron exercise closest to a plain bug
rather than a design tension: the rule was written against `pypi`-style
flat names and never re-examined against `npm`'s real naming convention,
which the `ecosystem` enum (SPEC §4.6) already commits to supporting
directly.

## Resolved — 2026-08-02

`/` escapes to `--` in the *derived filename only* — `name` keeps the
real, unescaped identifier (project SPEC §2.2, 0.8.0):
`@playwright/test` → `npm-@playwright--test.md`. Reversible, deterministic,
and it doesn't touch the one thing that has to stay accurate — the
identity a consumer actually reads.

`examples/netron/.capsa/dependencies/npm-@playwright--test.md` (renamed
from the deliberately-broken `npm-playwright-test.md`) is the live proof:
the capsule that motivated this issue now validates clean on this record,
with no other change.

---
id: 4
title: "The <ecosystem>-<name>.md filename rule is unsatisfiable for npm scoped packages"
kind: bug
severity: S2
status: triaged
source: "Claude, AI agent — Netron capability-test session"
owner: null
opened: 2026-08-02
triaged: 2026-08-02
closed: null
fix_commit: null
fix_plan_ref: null
regression_ref: null
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

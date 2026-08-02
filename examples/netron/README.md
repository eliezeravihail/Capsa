# Netron — a Capsa capsule for a real, external project

This is not a fictional demo like [`examples/sample-project`](../sample-project).
It's a Capsa capsule authored against the actual source, history, and
public documentation of [Netron](https://github.com/lutzroeder/netron)
(MIT), an existing open-source project this repository has no other
connection to.

It exists as a capability test: can the format faithfully document a
large, real, single-maintainer project — one Capsa had no part in
designing — using nothing but what the project's own repository and
public GitHub pages expose? Every record here cites its evidence (a
commit SHA, a file, a dated tag, a linked issue/PR) rather than asserting
facts on the capsule's own authority.

Four friction points surfaced while building it, filed against Capsa
itself rather than smoothed over here: one is fixed, one was re-examined
and rejected, two are still open.

- **`.capsa/issues/0001-source-enum-assumes-a-company.md`** — **fixed.**
  An issue's `source` (`ceo | system | agent`) had no honest value for
  "the solo open-source maintainer found and fixed this himself" — the
  actual case for `issues/0001-unsigned-32-bit-integer-decoding.md`
  below. Checked first whether the field did any checkable work anywhere
  in the spec — it didn't, unlike `severity`/`status` — so the fix wasn't
  a bigger enum, it was dropping the enum: `source` is now an optional
  free-text name and capacity (`"Lutz Roeder, maintainer"`), documentation
  rather than a forced category.
- **`.capsa/issues/0002-external-citation-has-no-structured-link.md`** —
  `links[].to` can address an internal record or another Capsa capsule,
  but has no way to cite an external, non-capsule source (a GitHub
  issue/PR, an RFC) as structured data; it falls back to prose. Open.
- **`.capsa/issues/0003-regression-ref-presence-not-meaning.md`** —
  **rejected.** The original finding was that the validator checks a
  closed bug's `regression_ref` is *present* without checking that the
  cited evidence actually guards the specific defect. Correct as an
  observation, wrong as a complaint: Capsa documents, it doesn't enforce
  truth, the same way a PDF validator confirms a file is well-formed and
  has no opinion on whether the invoice total inside it is right. See
  `.capsa/insights/dev/format-is-not-enforcement.md`.
- **`.capsa/issues/0004-scoped-package-name-breaks-dependency-filename.md`**
  — the `<ecosystem>-<name>.md` naming rule is unsatisfiable for any npm
  scoped package (`@playwright/test`, `@babel/core`, ...), since a
  filename can't hold `/`. Reproduces live in this capsule's own
  `dependencies/npm-playwright-test.md`, left deliberately
  non-conforming rather than hidden. Open.

See `examples/netron/.capsa/insights/dev/` for what else this exercise
found — a single-maintainer project with no organization capsule to
write, 802 releases where 3 were recorded on purpose, and a project
identity seven years younger than its own commit history.

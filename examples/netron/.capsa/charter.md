---
updated: 2026-08-02
---

# Charter — Netron

## Vision

A viewer for neural network, deep learning, and machine learning models —
open the model file, see the graph. No conversion step, no server required
to look at a model, no dependency on the framework that produced it.

## Constraints

- Client-side by default: the browser build (`source/browser.js`, hosted at
  netron.app) parses and renders a model entirely in the page. A server
  (`source/server.py`) exists to serve local files to that page, not to do
  the parsing.
- MIT-licensed; a dependency that would force a stronger copyleft on the
  distributed app is out of bounds without an admitting decision.
- One project, three distribution shapes from the same source: browser,
  Electron desktop app (macOS/Linux/Windows), and a `pip`-installable
  Python package exposing the same viewer.
- New format support is additive and isolated: one parser module
  (`source/<format>.js`) plus its metadata/schema files. A parser must not
  reach into another format's module.

## Ground rules

- `npm run lint` and `npm test [format]` before a change lands
  (`CONTRIBUTING.md`).
- A format is documented as `production` (README's primary list) or
  `experimental` (README's second list); this capsule mirrors that
  distinction on each format component (§ components/formats).

## Note on this capsule

Netron is a real, existing open-source project (MIT, github.com/lutzroeder/
netron); this `.capsa/` was authored by reading its actual source tree,
`package.json`/`pyproject.toml`, `README.md`, `CONTRIBUTING.md`,
`CITATION.cff`, and 10,000+ commits and 800+ tags of real history — not
invented. It was built as a capability test for Capsa: can the format
faithfully document a large, real, single-maintainer project it had no
part in designing? Records here cite the evidence they're drawn from
(a commit SHA, a file, a dated tag) instead of asserting facts about the
project on the capsule's own authority.

**Team, from the commit history.** Every one of Netron's 10,147 commits in
the cloned history is authored by Lutz Roeder. There is no second name to
record as a `members/` entry in an organization capsule — the honest
statement of "the team" here is that it is one person. That itself is
recorded (`insights/dev/single-maintainer.md`).

**Not exhaustive by design.** `source/` holds parser modules for roughly 70
model formats. Individually componentizing all of them would test typing
stamina, not the format — a handful are broken out as real
`components/formats/components/<slug>/` records (the README's
highest-profile production and experimental formats); the rest are
described, not enumerated, in `components/formats/component.md`. See
`insights/dev/format-catalog-scope.md` for exactly what was and wasn't
covered.

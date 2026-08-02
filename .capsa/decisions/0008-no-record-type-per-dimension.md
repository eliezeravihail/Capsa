---
id: 8
title: "The format names no dimension of variation: a platform is a requirement, or a component"
status: accepted
date: 2026-08-02
supersedes: null
superseded_by: null
discussion_ref: null
tags: [core, scale, axes]
links:
  - {rel: supersedes, to: decisions/0006-axes-and-contract-lifecycles}
---

## Context

0.4.0 introduced two "axes" — `lines/` and `platforms/` — as closed sets of
records a `scoped_status` entry could name. The `lines/` half answers a real
question: a product maintaining 26.x and 25.x at once has releases and
backports that belong to one stream or the other, and nothing else in the
format says which.

The `platforms/` half does not survive the same examination. "Runs on
Windows" is a **constraint on the code**, which is what a requirement is.
Where Windows and iPad need genuinely different code, that code is already
two **components**, each with its own record and its own `code_globs`. So the
type was a third name for something the format could state twice already, and
storing it a third time is what principle 4 forbids.

The decisive objection is the one that generalises. Nothing distinguishes
"platform" from the other dimensions a real product varies along — language,
accessibility target, regulatory regime, customer tier, deployment topology.
Admitting a record type for one of them is an argument for admitting all of
them, and the list has no principled end. A format that picks a favourite
dimension has made an arbitrary choice and then hard-coded it.

## Decision

`platforms/` is removed. §4.14 is retired rather than reused, so an older
document's reference to it still lands somewhere truthful.

`scoped_status[].scope` stops being `line:<slug>` / `platform:<slug>` and
becomes an ordinary internal address that must resolve to an existing record —
`lines/25-x`, `components/ios`, `requirements/0012-a11y`. The format
therefore enumerates no dimensions at all, while keeping the property that
made the closed vocabulary worth having: a scope that names nothing real is a
finding, not a string that silently means nothing.

The `lines/` type stays. A release line is not a constraint on code and not a
part of the system; it is a stream of releases, and `line` on a release plus
`fix_commits` on an issue have nothing else to point at.

## Consequences

Breaking for any capsule that used platforms, and the migration is a re-filing
rather than a rewrite: a platform that constrains shared code becomes a
requirement, a platform with code of its own becomes a component, and each
`scope: "platform:x"` becomes the address of whichever it became. The example
capsule here was migrated exactly that way, which is also what demonstrates
that the replacement is not a loss of expressiveness.

The format got smaller. That is worth saying out loud in a young spec, where
the pressure runs the other way: every real need met by an existing type
should be met by that type, and a new type has to earn itself by naming
something the format genuinely cannot say.

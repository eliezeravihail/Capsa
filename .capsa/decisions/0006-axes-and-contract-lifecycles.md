---
id: 6
title: "Facts that vary by release line or platform are exceptions on a scalar status, and axis values are records rather than strings"
status: accepted
date: 2026-08-01
supersedes: null
superseded_by: null
discussion_ref: null
tags: [scale, axes, interfaces]
links:
  - {rel: constrained_by, to: decisions/0005-graph-capsule}
---

## Context

Testing the format against a large, long-lived product surfaced facts it could
not hold without flattening them into something false. A requirement is met on
Windows and unmet on iPad. A bug is fixed on the current line and backported to
a maintained one as a *different commit*. A plugin API appeared in 1.0, was
deprecated in 2.4, and removed in 3.0, and every consumer needs all three
dates. A scalar `status`, a single `fix_commit`, and a changelog cannot say any
of it.

## Decision

Three shapes, chosen to add as little vocabulary as possible.

**One mechanism for both axes, not two.** Release lines and platforms are the
same problem — a fact that varies along a named dimension — so they share
`scoped_status` rather than getting a bespoke field each. Two bespoke
mechanisms would have drifted apart the first time one gained a feature.

**`scoped_status` states only the exceptions.** The scalar `status` stays the
project-wide answer. Enumerating every axis value would duplicate the default,
which §1.4 forbids, and would make adding a platform a rewrite of every
requirement.

**Axis values are records, not strings.** `lines/` and `platforms/` close the
set, which is what turns `platform:ipda` from a value that silently means
nothing into a typo a checker catches. The same reasoning promotes `milestone`
from a free string on a plan to a record: a string carries no date, two plans
can spell it differently, and nothing can check either.

**Interfaces are records because their lifecycle is not the project's.**
`since` / `deprecated_in` / `removed_in` are the promise a consumer plans
against.

## Consequences

`fix_commit` stays and gains `fix_commits` beside it rather than being
replaced: the single-commit case is the common one, and breaking it to express
the rarer one would be a poor trade. The cost is two fields that can disagree,
which the spec resolves by naming `fix_commit` the fix on the default line.

`targets` states a bar and the verification block states the measurement. Kept
separate on purpose: raising a target must not overwrite the record of what was
last measured, or the history of whether the product ever met the old bar is
lost.

Everything here is additive. Nothing in a 0.3.0 capsule changes meaning, and
`milestone` as a free string stays legal — deprecated, not removed, because
removing it would break capsules to buy nothing.

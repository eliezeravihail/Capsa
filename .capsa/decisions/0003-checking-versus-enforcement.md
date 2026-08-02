---
id: 3
title: "The validator checks conformance, never truth — but an operator MAY enforce more, on top, without forking it"
status: accepted
date: 2026-08-02
supersedes: null
superseded_by: null
discussion_ref: null
tags: [core, validator, governance]
links:
  - {rel: constrained_by, to: issues/0003-regression-ref-presence-not-meaning}
---

## Context

`issues/0003-regression-ref-presence-not-meaning.md` proposed that the
validator's check for a closed bug's `regression_ref` be strengthened, since
presence of the field doesn't mean the cited evidence actually guards the
defect. That issue was rejected: Capsa is a documentation format, not an
enforcement mechanism, the same relationship a PDF has to its reader — a
PDF validator confirms a well-formed file and has no opinion on whether
the invoice total inside it is correct.

The rejection left a real question unanswered: if Capsa itself won't
verify a claim's truth, does that mean *nobody* can — or does an operator
who wants stricter guarantees than the format promises have a supported
way to add them?

## Decision

The reference validator's job stays exactly what it was: grammar
conformance, never truth. But an operator MAY layer additional,
environment-specific enforcement on top, without forking the reference
validator, via two things now made explicit in `core/PRINCIPLES.md`
(§Checking):

1. **The findings shape is stable and public** — `{code, severity, path,
   field, detail, message}` — so an operator's own checker (in any
   language, checking anything it wants, including things the read-only
   validator structurally cannot: cross-referencing `fix_commit` against
   git history, calling out to a policy service) can emit findings in the
   same shape and merge cleanly with the reference validator's.
2. **`X-` is reserved for operator-defined codes**, mirroring the `x-`
   prefix already reserved for private `rel` vocabulary. A format's own
   codes never collide with it, so a finding is always unambiguous about
   which authority is speaking: the format's grammar, or an operator's
   policy.

## Consequences

Nothing about existing checks changes. This is additive documentation
and a naming reservation — no capsule that conformed before stops
conforming, and no new field exists to fill in. What changes is that the
distinction between "the format won't check this" and "nobody can check
this" is now written down instead of implied, closing the reading of the
0003 rejection that would have been: *therefore stricter enforcement has
no home in Capsa's world*. It does — just not inside the format's own
conformance rules.

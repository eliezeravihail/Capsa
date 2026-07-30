---
id: 4
title: "The validator's human and machine-readable output are one rendering each of a single findings list, never two collections"
status: accepted
date: 2026-07-30
supersedes: null
superseded_by: null
discussion_ref: null
tags: [validator, machine-readable]
---

## Context

Criterion c1 of the locked acceptance contract (decision 0003, option A)
requires that a calling program — not a human at a terminal — can obtain the
validator's findings in a form it can parse programmatically, alongside the
existing human-readable text. Before any implementation, the risk was named
explicitly: if the machine-readable form is produced by a second,
independently-populated collection (or a second pass over the capsule), nothing
keeps it in sync with the human text. A check added, changed, or fixed on one
side and not the other silently disagrees with itself — the exact failure mode
findings-collection exists to prevent, now aimed at the validator's own output.

## Decision

`validator/validate.py` keeps exactly one findings list, appended to by `err()`
as checks run (`{"path": str, "message": str}` per entry). Both output forms —
the existing human text (`NON-CONFORMING — N finding(s): ...`) and the new
`--json` output (`{"conforming": bool, "findings": [...]}`) — are rendered from
that same list at the end of `validate()`, in the same function, from the same
run. Neither collects independently; there is no second pass and no second
list. `--json` is opt-in via a CLI flag; the default behaviour and exit codes
(0 conforming, 1 findings, 2 not a capsule) are unchanged.

## Consequences

- A calling program (e.g. an orchestration engine) parses `--json` and never
  the human text, which stays free-form and may reword without notice.
- Any future check that calls `err()` automatically appears in both renderings
  — there is no second place to remember to update, and so no way for the two
  to disagree.
- `findings` is cleared at the start of `validate()`, making repeated in-process
  calls (e.g. from a test, or a caller validating several capsules without
  re-invoking the interpreter) independent of each other.

## Alternatives considered

- **A separate `--json` code path that re-runs the checks into its own list.**
  Rejected: doubles the maintenance surface for zero benefit, and is precisely
  the divergence risk this decision exists to close.
- **JSON as the only output, with the CLI pretty-printing it for humans.**
  Not chosen for this round: keeps the existing human wording exactly as
  written (a smaller, more reviewable diff over a stable, hand-tuned format);
  revisit if the two renderings ever need to diverge in structure, not just
  presentation.

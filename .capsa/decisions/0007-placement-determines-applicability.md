---
id: 7
title: "Where a record sits is what it applies to; no record declares its own scope"
status: accepted
date: 2026-08-01
supersedes: null
superseded_by: null
discussion_ref: null
tags: [core, placement, links, addresses]
links:
  - {rel: constrained_by, to: decisions/0005-graph-capsule}
---

## Context

0.3.0 made the capsule a graph and derived a record's owning component from
its path. What it did not say is what *else* the path means. A reader holding
one node still had no rule for finding the requirements and decisions in force
there, so the only mechanism available was to traverse links — and a traversal
is conditional on depth, on filtering, on whatever budget the reader has. An
obligation that is only discoverable by traversal is an obligation that can be
missed by a correctly implemented reader.

The alternative considered first was a scope field on the record that
constrains — `applies_to: components/render/**` — so the constraint could be
written once and be found by everything inside that glob. It was rejected. A
scope field is a second statement of a fact the path already makes: filing the
decision in `components/render/decisions/` says the same thing, and says it in
the one place principle 4 allows. Two authorities on the same question is the
condition under which they disagree, and a glob additionally invents a
matching language that has to be specified, implemented identically by every
consumer, and defended against overreach.

The objection that motivated the scope field — a decision taken today that
constrains a component authored a year ago — turns out not to need it. The
decision is filed under that component now; the old records beneath it need no
edit, because nothing about them ever recorded what governs them.

## Decision

**Placement is a statement of scope** (core §Placement). A record applies to
the node holding it and to everything beneath it; a record at the root applies
capsule-wide. What binds a node is therefore the walk from that node to the
root, and it is derived, never declared. No `applies_to`, no scope field, no
globs — the format gains no new field at all.

**A format must classify its record types as normative or descriptive**
(project SPEC §2.7), since the walk is meaningless until it is written down
which types carry an obligation. The test is whether removing the record would
make something permissible beneath it that is not permissible now.

**Addresses may be relative** (`./…`, `../…`), resolved against the directory
holding the record. A reference inside one subtree should be relative, so
moving the subtree is a directory drag with nothing to edit; a reference
across subtrees should stay absolute, where a move genuinely does change the
relationship.

**A link may not restate the tree.** An edge whose target is an ancestor of
the record carrying it is non-conforming — the same rule as "the owner is
derived from the path and must not be stored", applied to edges.

## Consequences

The link is demoted, and that is the point. It stops being the mechanism by
which obligations are discovered and becomes a pointer to the facts the tree
cannot hold — sibling dependencies, direction, cross-branch relevance,
cross-capsule references. Two things follow: there are far fewer edges to keep
true, and a broken one costs less, because the obligation it pointed at is
still found by the walk and only the provenance has aged.

The cost is that a move is now semantically loaded: dragging a component to a
new parent changes what governs it. That is judged correct rather than
hazardous — re-parenting a component *is* that act — but it means a
reorganisation is a review-worthy change, not a tidy-up.

The rule against tree-restating links is the first non-additive change in the
format's history. It was written against evidence: the example capsule shipped
in the same branch carried exactly that anti-pattern
(`components/mux/issues/moov-atom-ordering` linking `affects` to
`components/mux/component`), and it was found by a human reading the diff, not
by any check. The validator now catches it, and was calibrated against that
reinstated defect before being trusted.

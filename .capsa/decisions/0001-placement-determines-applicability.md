---
id: 1
title: "Where a record sits is what it applies to; no record declares its own scope"
status: accepted
date: 2026-08-02
supersedes: null
superseded_by: null
discussion_ref: null
tags: [core, placement, links, addresses]
---

## Context

A reader holding one node in the capsule needs a way to find the
requirements and decisions in force there. The mechanism first considered
was `links`: traverse edges from the node and collect what constrains it.
That mechanism has a structural weakness — a traversal is conditional on
depth, on filtering, on whatever budget a reader applies — so an obligation
reachable only by traversing can be missed by a correctly implemented
reader.

A second option was a scope field on the record that constrains —
`applies_to: components/render/**` — written once at the source and matched
against every node inside it. This was rejected. A scope field is a second
statement of a fact the path already makes: filing the decision under
`components/render/decisions/` says the same thing, in the one place
"single home" allows. Two authorities on the same question is the
condition under which they can disagree.

## Decision

**Placement is a statement of scope.** A record applies to the node holding
it and to everything beneath it; a record at the root applies capsule-wide.
What binds a node is therefore the walk from that node to the root, derived
rather than declared. No `applies_to`, no scope field, no globs.

A format must classify each of its record types as **normative** (binds the
subtree) or **descriptive** (states a local fact and binds nothing), since
the walk is only meaningful once that distinction is written down.

A reference inside one subtree is written as a relative address (`./…`,
`../…`), so moving the subtree is a directory drag with nothing to edit. A
link whose target is an ancestor of the record carrying it is refused — the
path already states it.

## Consequences

`links` is demoted from the mechanism that discovers obligations to a
pointer for what the tree cannot express — a dependency between siblings, a
reference across branches, a link into another capsule. There are far fewer
edges to keep true, and a stale one costs less: the obligation it pointed at
is still found by the walk, and only the provenance has aged.

The cost is that moving a directory is now a semantically loaded act:
re-parenting a component changes what governs it. That is judged correct —
it is what re-parenting means — but it makes a reorganisation
review-worthy rather than a tidy-up.

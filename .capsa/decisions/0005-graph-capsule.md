---
id: 5
title: "A capsule is a graph — a containment tree plus typed links — kept in files, with a derived index for querying"
status: accepted
date: 2026-08-01
supersedes: null
superseded_by: null
discussion_ref: null
tags: [core, graph, retrieval]
---

## Context

The requirement driving this: an agent must receive **only the relevant
neighbourhood** of what it is working on, not the whole capsule. At fifty
records that is a preference; at the scale this format claims to target — a
long-lived product with tens of thousands of records — it decides whether the
format is usable at all.

Three mechanics blocked it. There was no component axis, so nothing described
the system's own structure and every directory was one unsorted pile. Edges
carried their meaning in the *field name*, so every kind of link had to be
declared in advance, per record type, by whoever wrote the format spec — an
insight could not link to a decision, not because it was forbidden but
because no field existed. And the project format identified records by a
sequential `NNNN` in a flat directory, which assumes a single writer: several
authors on branches each allocating the next number collide by construction,
in the one field that identifies the record.

The alternative considered seriously was abandoning files for a graph
database. It was rejected: git is the backup, history, diff, review and
audit layer this whole system rests on, and a graph database would require
re-implementing all of it. Scale does not force the move either — at order
10⁵ nodes and 10⁶ edges, k-hop traversal is milliseconds in SQLite or in
memory. A dedicated graph database is not indicated at any plausible project
scale.

## Decision

The capsule is a graph kept in files: a **containment tree** (the component
directory structure) plus **typed `links`** in the core grammar. Identity is
the **path**, so no allocation is needed. Addresses are internal or external
(`@capsule/path`); internal ones must resolve, external ones may dangle.
Anything queryable — an edge table, embeddings — is a derived index, rebuilt
from the Markdown and never a source of truth.

## Consequences

**A capsule stays self-contained.** Making an unresolved *external* link a
non-error is what preserves that: a project capsule ships inside its product
repo and has to stay valid wherever it lands. It follows that strong links
point inward, from the capsule that stays home to the one that travels — and
that is what lets the project and organization formats federate instead of
being merged into one.

**Referential integrity becomes the checker's job.** Files have no foreign
keys, so an edge can point at a deleted record and nothing objects. Rule 7 of
§5 is not bookkeeping; it is the only thing that makes the links trustworthy
enough to compute a neighbourhood from, and it is the point at which, if
neglected, the argument for a database becomes correct.

**Structure selects; similarity only ranks.** A neighbourhood is computed
from the tree and the edges — deterministic and complete. Semantic search is
useful for ordering what is already selected, never for choosing it: a brief
that silently omits a constraining decision is wrong in a way a similarity
score cannot detect.

**Repair stays outside the format.** The checker gained stable codes and
severities precisely so a repair tool can exist *elsewhere* — a tool that
rewrites records is a maintenance mechanism, which principle 1 refuses.

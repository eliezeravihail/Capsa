---
id: 2
title: "The format names no dimension of variation: a platform is a requirement, or a component"
status: accepted
date: 2026-08-02
supersedes: null
superseded_by: null
discussion_ref: null
tags: [core, scale, axes]
---

## Context

A record type for release lines is a real need: a product maintaining
several maintenance streams at once has releases and backports that belong
to one stream or another, and nothing else in the format says which.

A record type for platforms does not survive the same test. "Runs on
Windows" is a **constraint on the code**, which is what a requirement
already is. Where two platforms need genuinely different code, that code is
already two components, each with its own record and its own `code_globs`.
A dedicated type would be a third name for something the format could
already say twice.

The decisive objection generalises. Nothing distinguishes "platform" from
the other dimensions a real product varies along — language, accessibility
target, regulatory regime, customer tier. A record type for one is an
argument for a record type for all, and that list has no principled end.

## Decision

The format defines no record type for a dimension of variation. A fact that
varies is stated with `scoped_status`, whose `scope` is an ordinary internal
address that must resolve to **any** existing record — a release line, a
component, a requirement — rather than a value from a closed vocabulary.

## Consequences

The format enumerates no dimensions, while keeping what a closed vocabulary
was worth: a scope naming nothing real is still a finding, not a string
that silently means nothing. A project that varies by platform, language,
or regulation files that variation using the record types it already has —
requirements and components — rather than waiting for the format to grow a
type for it.

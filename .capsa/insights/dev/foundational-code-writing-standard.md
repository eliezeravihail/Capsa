---
kind: dev
title: "Foundational code-writing standard — applies to every task that touches code"
created: 2026-08-01
scope: universal
tags: [conduct, code-quality, standard]
---

Three non-negotiable requirements bind every task that writes or changes code.
They are stated as universal conduct because they are the ones observed to be
dropped under pressure, and each is enforceable in review.

**a. Do not guess, and do not invent assumptions — verify instead.**
Before asserting how something behaves, where it lives, or what an interface
returns, check it: read the code, run it, or measure it. An unverified claim
presented as fact is the failure this whole system exists to refuse. When a
fact cannot be verified, say so plainly rather than filling the gap with a
guess.

**b. Quality code is the top obligation — write to accepted modern-programming
principles.** In particular: encapsulation (hide state behind behaviour);
separation into parts that communicate through explicit interfaces, not through
each other's internals; object-oriented modelling when the domain is objects;
and no code smells (duplication, long functions, feature envy, leaky
abstractions, dead code). On conflict, quality outranks speed — a fast result
that is unmaintainable is a net loss.

**c. Write generic, extensible, maintainable code — never bury values in the
source.** No magic literals, no hardcoded strings, no magic constants inline.
Give every such value a name and a single home: an enum for a closed set, a
configuration for a tunable, an environment variable for a deployment- or
secret-bearing value. The test is: a maintainer must be able to change the
value in one obvious place without reading the algorithm around it.

Single source of truth is scoped by what the value *is*, not by which files it
happens to appear in. A value intrinsic to one implementation — a class, or one
language's port of a shared spec — has one home *per implementation*: a
reference port legitimately keeps the same render constant in both its Python
and its JS copy, bound honest by a parity test, and that is correct, not a
compromise to apologise for. A value that is a single product fact — a site
name, a domain, a brand colour decided once — has exactly one home for the
*whole system*; the same literal copied into eight files is the violation this
rule targets. So ask of each constant: "is this an implementation detail of one
unit, or one fact the whole product shares?" and give it a home at that scope —
no wider, no narrower.

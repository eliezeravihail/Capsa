# Capsa core — principles & grammar (every format inherits this)

**Version 0.4.0.** The **core** is the conceptual infrastructure shared by every
capsa format. It defines *how* a capsule is shaped — **never which records
exist** (that is each format's decision).

The key words MUST, SHOULD, and MAY are used as in RFC 2119.

## Principles
1. **Passive** — data, not a program. No runtime, hooks, or daemons.
2. **Readable** — every record is UTF-8 Markdown: YAML frontmatter (machine
   fields) + prose body (for people).
3. **Portable & self-contained** — a `.capsa/` directory in a repo; depends on
   nothing outside itself.
4. **Single home** — each fact lives in exactly one record; records reference by
   id/slug/path, never duplicate. Derivable data (roadmaps, indexes,
   **embeddings**) is computed by consumers, never stored.
5. **Truth, not run-state** — a capsule holds durable truth; live operational
   state (who is working now, counters, telemetry) MUST NOT be written to it.
6. **Versioned by a field** — a capsule declares `capsa_core` and its `format`.
7. **Verifiable by construction** — a checkable claim is a structured
   frontmatter field with an evidence ref, not prose.

## Grammar
- Record = `--- <yaml frontmatter> ---` + Markdown body.
- Dates ISO-8601 (`YYYY-MM-DD`); timestamps RFC-3339.
- `*_ref` / `*_refs` hold the id/slug of another record, or a path.
- Unknown frontmatter keys are permitted and MUST be preserved by writers.
- The `verification` block (`status` / `method` / `evidence_ref` / `checked_at`)
  wherever a claim is checkable; a missing block means `unverified`.

### Placement

A capsule is a **containment tree** of directories, and placement in that tree
is not filing convenience — it is a statement about scope:

> **A record applies to the node that holds it and to everything beneath it.**
> A record at the root applies to the whole capsule.

Two things follow, and they are the reason this is stated in the core rather
than left to each format.

**Applicability is derivable, so it is never declared.** What binds a given
node is the walk from that node to the root, taking the normative records
found at each level. No record carries a field naming its scope. Such a field
would be a second statement of a fact the path already makes — principle 4
forbids that — and, being separate, it could come to disagree with the path
while both looked authoritative.

**Moving a directory changes what governs its contents, and that is correct.**
Re-parenting a component *is* the act of placing it under a different set of
rules. A capsule where the layout and the rules can be changed independently
has two answers to "what applies here".

A format MUST classify each of its record types as **normative** (binds the
subtree) or **descriptive** (states a local fact and binds nothing), because
the walk is only meaningful once that distinction is written down. Core does
not name record types, so core does not make the classification.

The tree therefore already expresses containment, ownership, and scope. What
it cannot express — a dependency between siblings, a direction, relevance
across branches, anything crossing capsules — is what `links` is for.

### Addresses

Every reference — a `*_ref` value, a `links[].to` — is an **address**:

- **Internal, absolute** — a path relative to the capsule's format directory,
  without the `.md` suffix: `decisions/0004-tile-cache`,
  `components/render/component`. A format MAY additionally accept a bare
  id/slug where its own numbering makes that unambiguous.
- **Internal, relative** — an address beginning with `./` or `../`, resolved
  against the directory holding the record that carries it:
  `../component`, `./issues/tiling-seam`.
- **External** — `@<capsule-slug>/<path>`, where `<capsule-slug>` is the
  identity declared in the target capsule's manifest:
  `@acme/policies/license-tiers`.

The `@` prefix is REQUIRED on an external address so that internal and external
are distinguishable **without knowing which capsules are attached** — a checker
reading one capsule alone must be able to tell them apart. A leading `./` or
`../` is likewise the only marker of a relative address: anything else is
absolute from the format directory, so the two are told apart without knowing
where the reading started.

A relative address MUST NOT resolve above the format directory. After
resolution it is an ordinary internal address and obeys the same rules.

**Relative is what makes a subtree portable.** An absolute address breaks when
its subtree is moved, even though both endpoints moved together and neither
fact changed — the same failure the derived-owner rule avoids. So: a reference
to a record **inside the same subtree** SHOULD be relative, and one **crossing
subtrees** SHOULD be absolute, where a move genuinely does change the
relationship and ought to be re-examined.

**Resolution.** An **internal** address that does not resolve is an error: a
capsule must be internally whole. An **external** address that does not resolve
is **not** an error, because principle 3 says a capsule depends on nothing
outside itself — it MUST stay valid, and answerable, with no other capsule
attached. External links are enrichment that degrades cleanly; an unresolved one
is reported only by a check run over several attached capsules together.

It follows that **strong links point inward**: a capsule that travels (a project
capsule ships inside its product repo) should be pointed *at*, rather than
depend on pointing *out*. An organization capsule, which stays home, is the
natural holder of cross-capsule edges.

### Links

`*_ref` fields carry an edge's meaning in the **field name**, so every edge must
be declared in advance, per record type, by whoever writes the format spec.
`links` is the general form — any record MAY carry it, and a new kind of edge
needs no spec change:

```yaml
links:
  - {rel: implements,     to: requirements/0003-verifiable-claims}
  - {rel: constrained_by, to: "@acme/policies/license-tiers"}
```

- `rel` and `to` are both REQUIRED. `rel` is a lowercase token; `to` is an
  address.
- **Core vocabulary:** `implements`, `enacts`, `constrained_by`,
  `discussed_in`, `supersedes`, `superseded_by`, `fixed_by`, `admitted_by`,
  `includes`, `fixes`, `meets`, `depends_on`, `affects`, `owns`,
  `anchored_to`, `learned_from`, `moved_to`, `aims_at`, `exposes`.
- An unknown `rel` MUST be preserved and MAY be traversed by consumers.
  Private vocabulary SHOULD use an `x-` prefix.
- **An edge is authored in ONE direction; the inverse is computed by consumers,
  never stored.** Requiring both endpoints to carry it would make every link a
  two-file write — the operation that conflicts under concurrent editing — and
  would duplicate a fact, which principle 4 forbids.

- **A link MUST NOT restate the tree.** An edge whose target is an ancestor of
  the record carrying it is non-conforming: the path already says it, and
  principle 4 does not stop applying because the duplicate is a link rather
  than a field. An issue filed at `components/mux/issues/moov-ordering` does
  not link `affects: components/mux/component`; it *is* in `mux`.

`links` **complements** `*_ref` fields and does not replace them: where a format
has already named an edge in a field, that field stays authoritative.

Consequence worth stating, because it is the reason `links` exists at all: with
placement carrying containment and scope, an explicit edge is reserved for the
facts placement cannot hold, and there are few of them. That matters beyond
tidiness — placement is written once, when the record is filed, whereas an edge
must be *kept true* for as long as both endpoints exist. Fewer edges is
therefore less that can silently go stale, and a broken one costs less: the
obligation it pointed at is still in force, since the walk found it, and only
the provenance pointer has aged.

Together the two give a consumer what it needs to read a large capsule without
reading all of it — a node's ancestors, its neighbourhood in the tree, and a
bounded number of hops over `rel`-filtered edges. Which of those a consumer
takes, how far, and in what order is the consumer's concern; the capsule adds
no mechanism for it and expresses no opinion about it.

### Tombstones

A record MAY be replaced by a **tombstone**: frontmatter keeping its `title`,
plus `status: moved` and a `moved_to` link, with the body reduced to a pointer.

```yaml
status: moved
links: [{rel: moved_to, to: "@acme/insights/calibrate-instruments"}]
```

The record now lives at the target. This exists so that promoting a record
between capsules — an insight found in a project and later recognised as
organisational — keeps principle 4 (single home) instead of being done by
copy-paste, and does not sever the history.

## Manifest
Every capsule has `core/capsule.yaml` declaring `capsa_core`, `format`, and the
capsule's identity. Records live under the **format** directory beside `core/`.

## Versioning
`capsa_core` is `MAJOR.MINOR.PATCH`: PATCH clarifies, MINOR is additive and
backward-compatible, MAJOR is breaking (a consumer MUST refuse a MAJOR it does
not support). A format versions itself independently through `format_version`.

Changelog:
- **0.4.0** — placement as a statement of scope, and the normative/descriptive
  duty it puts on a format (§Placement); relative internal addresses
  (§Addresses); a link may not restate the tree (§Links). The first two are
  additive. The third is a **restriction**: a 0.3.0 capsule carrying an
  ancestor link stops conforming until that link is deleted, which loses no
  information — the path states it.
- **0.3.0** — `aims_at` and `exposes` join the core vocabulary. Additive, and
  strictly a convenience: an unknown `rel` was always legal. A vocabulary that
  never grows is one writers stop reading.
- **0.2.0** — addresses (internal / external `@slug/path`, with resolution
  rules), `links`, tombstones. All additive; a capsule conforming to 0.1.0
  conforms to 0.2.0 unchanged.

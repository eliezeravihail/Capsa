# Capsa core — principles & grammar (every format inherits this)

**Version 0.3.0.** The **core** is the conceptual infrastructure shared by every
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

### Addresses

Every reference — a `*_ref` value, a `links[].to` — is an **address**:

- **Internal** — a path relative to the capsule's format directory, without the
  `.md` suffix: `decisions/0004-tile-cache`, `components/render/component`.
  A format MAY additionally accept a bare id/slug where its own numbering makes
  that unambiguous.
- **External** — `@<capsule-slug>/<path>`, where `<capsule-slug>` is the
  identity declared in the target capsule's manifest:
  `@acme/policies/license-tiers`.

The `@` prefix is REQUIRED on an external address so that internal and external
are distinguishable **without knowing which capsules are attached** — a checker
reading one capsule alone must be able to tell them apart.

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

`links` **complements** `*_ref` fields and does not replace them: where a format
has already named an edge in a field, that field stays authoritative.

Consequence worth stating, because it is the reason `links` exists: a
containment tree (a format's directory layout) plus typed edges is enough for a
consumer to compute a **bounded, deterministic neighbourhood** of any record —
its ancestors, plus k hops over edges filtered by `rel`. That is what lets a
consumer load only the relevant part of a large capsule instead of all of it.
The query is a consumer's concern and adds no mechanism to a capsule.

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
- **0.3.0** — `aims_at` and `exposes` join the core vocabulary. Additive, and
  strictly a convenience: an unknown `rel` was always legal. A vocabulary that
  never grows is one writers stop reading.
- **0.2.0** — addresses (internal / external `@slug/path`, with resolution
  rules), `links`, tombstones. All additive; a capsule conforming to 0.1.0
  conforms to 0.2.0 unchanged.

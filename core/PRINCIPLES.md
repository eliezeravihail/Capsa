# Capsa core — principles & grammar (every format inherits this)

The **core** is the conceptual infrastructure shared by every capsa format. It
defines *how* a capsule is shaped — **never which records exist** (that is each
format's decision).

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

## Manifest
Every capsule has `core/capsule.yaml` declaring `capsa_core`, `format`, and the
capsule's identity. Records live under the **format** directory beside `core/`.

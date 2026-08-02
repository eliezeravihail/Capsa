# Capsa tools

Tools operate **on** capsules; capsules stay passive (core principle 1).

- **validator** — checks a capsule against the core grammar and its format's
  record rules (`SPEC.md` §5), read-only and dependency-free.

**Extending enforcement, without forking.** The validator checks
conformance to the grammar, never that a conforming record is true (core
§Checking) — the same relationship a PDF validator has to a PDF's content.
An operator that wants more than that (verifying a `regression_ref`
against git history, a private policy check, anything Capsa itself has no
way to know) writes its own checker and emits findings in the same
`{code, severity, path, field, detail, message}` shape, using an `X-`
prefixed code. The two outputs merge; nothing about the reference
validator needs to change to make room for it.

A capsule's structure (records, `links`, the component tree) is enough for a
consumer to build a derived index — embeddings, a vector store, a graph
database — for faster or richer retrieval. Any such index is rebuildable from
the files at any time; the capsule stays the source of truth (core principle
4). Building one is outside this repository's scope.

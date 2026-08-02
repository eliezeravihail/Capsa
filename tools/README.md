# Capsa tools

Tools operate **on** capsules; capsules stay passive (core principle 1).

- **validator** — checks a capsule against the core grammar and its format's
  record rules (`SPEC.md` §5), read-only and dependency-free.

A capsule's structure (records, `links`, the component tree) is enough for a
consumer to build a derived index — embeddings, a vector store, a graph
database — for faster or richer retrieval. Any such index is rebuildable from
the files at any time; the capsule stays the source of truth (core principle
4). Building one is outside this repository's scope.

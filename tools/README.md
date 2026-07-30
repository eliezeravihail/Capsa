# Capsa tools

Tools operate **on** capsules; capsules stay passive (core principle 1).

- **validator** — checks a capsule against the core grammar + its format's
  record schemas.
- **embeddings / RAG plugin** — on load, builds a vector index from a capsule's
  records (insights, decisions, …) so a consumer retrieves only the relevant
  subset (RAG) instead of loading the whole capsule. Derived and rebuildable —
  the capsule stays the source of truth. See HaMenahel
  `docs/plans/data-architecture-capsa-db-rag.md`.

# aharon — insights

> Append-only. One line per insight: `- YYYY-MM-DD · <insight>`.
> Mark superseded insights with [stale]; never delete.
> Written by the role during shifts; harvested here by the HaMenahel
> engine at goal boundaries (engine commits, engine pushes — never an agent).

- 2026-07-30 · When the CEO's goal is an open "continue development of X"
  with no explicit ask, and X is a spec/standard that already dogfoods itself
  (a `.capsa/` capsule managing capsa), the highest-signal move is NOT to
  brainstorm new features — it's to read the standard's own dogfooding trail
  (`.capsa/issues/`, `.capsa/decisions/`, `.capsa/insights/dev/`) and diff what
  the spec *claims* against what the reference implementation *actually
  checks*. That diff (here: SPEC.md explicitly names cross-record "checkable
  claims" — e.g. "no open S1 at release", "every must requirement met before
  release" — that `validator/validate.py` never implements, plus zero
  referential-integrity checking on any `*_ref`/`*_refs` field) is a concrete,
  low-risk, low-effort, zero-version-bump concept direction that beats
  speculative tooling (scaffold/migrate CLIs) built on a single past
  occurrence (the one manual 0.1→0.2 rename) — don't recommend generalizing
  from n=1.
- 2026-07-30 · A useful sub-technique for finding real spec ambiguities fast:
  read every schema `enum` and cross-reference field against the prose in
  SPEC.md looking for (a) a claim in prose with no supporting schema field
  (e.g. "no unknown license at release" — but release records have no field
  linking to dependencies at all), and (b) two record types that sound
  redundant (here: root `charter.md` vs. `plans/*.md` with `kind: charter`,
  never reconciled in the text). Both surfaced directly from a straight
  read-through, no speculation needed.

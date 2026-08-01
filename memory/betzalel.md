# betzalel — insights

> Append-only. One line per insight: `- YYYY-MM-DD · <insight>`.
> Mark superseded insights with [stale]; never delete.
> Written by the role during shifts; harvested here by the HaMenahel
> engine at goal boundaries (engine commits, engine pushes — never an agent).

- 2026-08-01 · Byte-identical refactor: naming a literal as a constant with the SAME value and preserving concatenation order keeps output bytes identical — golden SHAs must NOT move (if a golden changes, the refactor is wrong, not the golden). It also doesn't weaken mutation coverage: a golden pins the concatenated output regardless of whether the value is a literal or a named const.
- 2026-08-01 · When a core file must load standalone (node `require` with no sibling files) AND mirror a cross-language port, satisfy SRP at the class/function level WITHIN one file per runtime, not by splitting into multiple files. A multi-file core split breaks standalone-require and doubles the port-symmetry surface. Extract collaborating units (renderer fn, permalink codec, shared geometry iterator) but keep them co-located.
- 2026-08-01 · Preserve a tested public API by keeping the methods as thin delegating facades over the extracted units. This achieves separation-of-concerns without editing acceptance tests — which the mutation harness re-runs and which encode the CEO's locked criteria. Editing tests to fit a refactor is the risk to refuse.
- 2026-08-01 · Cross-runtime "single source of truth" for a constant (Python↔JS port) cannot be one physical source without a build step or the core reading an external file (both disproportionate / break standalone-load). The correct answer is two named constants bound by the existing parity test — the TEST is the enforcement mechanism; say so explicitly in the ADR.
- 2026-08-01 · Own the coverage gap: if the automated gate (pytest here) never executes the browser UI, splitting the UI is guarded only by index.html-parse + manual smoke. State this as a real limit rather than implying the suite covers the app.js split. Give the developer an explicit manual smoke checklist and point at any existing headless harness (repo had a Playwright one) as an optional follow-up.
- 2026-08-01 · De-literalise in place FIRST (swap magic numbers for config/constants + dedupe helpers), commit, THEN extract modules — so the module split is pure code-motion with no behaviour change riding along. Smallest-diff-first + parity-checked-early makes each step independently bisectable.

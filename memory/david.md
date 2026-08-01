# david — insights

> Append-only. One line per insight: `- YYYY-MM-DD · <insight>`.
> Mark superseded insights with [stale]; never delete.
> Written by the role during shifts; harvested here by the HaMenahel
> engine at goal boundaries (engine commits, engine pushes — never an agent).

- 2026-08-01 · Byte-exact reference-port refactor (MazeForge): the safe order is
  extract the shared SEAM verbatim (e.g. wall_segments) and verify against
  goldens+parity in its OWN step BEFORE extracting the renderer that consumes it.
  Highest byte-risk (segment order) then fails loudly in isolation, not buried.
- 2026-08-01 · Naming a literal must keep the IDENTICAL value or the golden SHA
  moves. Splitting one f-string across adjacent string literals is byte-safe only
  if you preserve the trailing space (`'...width="2" '` + `'stroke-linecap...'`).
  Verified by test, not by eye.
- 2026-08-01 · pytest never executes app.js/render.js/play.js/export.js. Wrote a
  ~80-line node vm shim (fake document/canvas/Blob/URL) that LOADS all UI modules
  and ASSERTS behaviour: an end-to-end keyboard solve must flip the win banner,
  and SVG-export bytes must equal core toSvg(22,10). "Execute, don't read and
  conclude" — this is the only gate that sees UI logic errors.
- 2026-08-01 · Preserve exotic user-facing strings (smart quotes “”, ·, ×, —,
  ’) across a wholesale file rewrite by diffing the exact lines against a backup
  in Python (byte compare), or use targeted edits whose match strings never touch
  those lines. Don't retype them and hope.
- 2026-08-01 · During in-place deliteralization, `const PAD = config.board.PAD`
  (local alias sourced from config) is a low-risk bridge: every existing PAD
  reference keeps working, no literal remains, and the alias evaporates when the
  code later moves into its module. Do the big literal-swap BEFORE the split so
  the split stays pure code-motion.
- 2026-08-01 · Stayed in lane on a real duplication (two identical polyline loops
  in draw()): the design scoped the smells precisely and did NOT list it, so I
  moved it verbatim and filed a suggestion rather than refactoring off-contract.
  Out-of-scope cleanup is a note to the architect, not a keyboard decision.


# shlomo — insights

> Append-only. One line per insight: `- YYYY-MM-DD · <insight>`.
> Mark superseded insights with [stale]; never delete.
> Written by the role during shifts; harvested here by the HaMenahel
> engine at goal boundaries (engine commits, engine pushes — never an agent).

- 2026-08-01 · When auditing a small input-taking site for XSS, find the single validation choke point first (here: one allowlist regex in the Maze constructor), then verify no sink bypasses it — far faster than tracing every sink cold, and it names the real fragility.
- 2026-08-01 · When the same block is duplicated N times, rank the copies by which one a test pins. The dangerous copy is the UNtested one (here the PNG wall-loop, not covered by the golden SVG SHA) — it drifts silently. Duplication severity = f(test coverage of each copy), not just count.
- 2026-08-01 · Flag "safe only because an upstream validator is strict" as a latent finding even when currently exploit-free: an SVG aria-label / URL query that interpolates a value unescaped re-opens XSS or breaks round-trips the moment the shared validator is relaxed. Recommend self-sufficient escaping at each boundary.
- 2026-08-01 · On a "zero-behaviour-change" refactor, the highest-value check is that each retained facade passes args positionally to the extracted free function with IDENTICAL defaults (to_svg→render_svg, toSvg→renderSvg) — that is WHY byte-pinned goldens can't move. Verify the delegation, don't just trust the green golden.
- 2026-08-01 · A duplication the developer self-discloses is usually the mild one; the dangerous one is the copy nobody mentions. Here david flagged a 2× polyline dup (cosmetic, same-file, both branches drawn) while the flagship 4× wall-loop — the copy with an UNtested instance — was the one actually eliminated. Rank disclosed-vs-silent, not just count.
- 2026-08-01 · "Single source of truth" enforced by a cross-runtime parity TEST (two physical literals bound by a test) is a legitimate answer when a shared file or build step would break a load-bearing constraint (core must require() standalone, zero-dep). Accept it, but state the guarantee is "a test fails on drift," not "one textual location."


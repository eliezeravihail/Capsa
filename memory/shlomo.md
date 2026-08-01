# shlomo — insights

> Append-only. One line per insight: `- YYYY-MM-DD · <insight>`.
> Mark superseded insights with [stale]; never delete.
> Written by the role during shifts; harvested here by the HaMenahel
> engine at goal boundaries (engine commits, engine pushes — never an agent).

- 2026-08-01 · When auditing a small input-taking site for XSS, find the single validation choke point first (here: one allowlist regex in the Maze constructor), then verify no sink bypasses it — far faster than tracing every sink cold, and it names the real fragility.
- 2026-08-01 · When the same block is duplicated N times, rank the copies by which one a test pins. The dangerous copy is the UNtested one (here the PNG wall-loop, not covered by the golden SVG SHA) — it drifts silently. Duplication severity = f(test coverage of each copy), not just count.
- 2026-08-01 · Flag "safe only because an upstream validator is strict" as a latent finding even when currently exploit-free: an SVG aria-label / URL query that interpolates a value unescaped re-opens XSS or breaks round-trips the moment the shared validator is relaxed. Recommend self-sufficient escaping at each boundary.


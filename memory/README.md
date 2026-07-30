# Role memory — per-agent insights notebooks

One file per role. Copied into every goal workspace (`memory/`), and new
lines are harvested back here by HaMenahel when the goal completes —
so lessons accumulate across goals.

Rules (enforced by convention + review):
- APPEND-ONLY. One insight per line: `- YYYY-MM-DD · <insight>`.
- Never delete or rewrite old lines; mark superseded ones with `[stale]`.
- An insight is something that improves the NEXT task: a working method, a
  pitfall, a postmortem conclusion, a fragile area of the code.
- Task-specific state does NOT belong here — it dies with the task card.
- shlomo is read-only: it reports insights inside its review verdict, and
  MOSHE appends them to `memory/shlomo.md` on its behalf.

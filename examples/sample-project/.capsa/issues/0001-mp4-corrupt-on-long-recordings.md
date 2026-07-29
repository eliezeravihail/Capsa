---
id: 1
title: "MP4 corrupt when recording exceeds 2GB"
kind: bug
severity: S1
status: closed
source: ceo
owner: david
opened: 2026-07-21
triaged: 2026-07-21
closed: 2026-07-22
fix_commit: "a3f9c1d2e"
fix_plan_ref: null
regression_ref: "tests/test_mux.py::test_large_file_finalize"
reopens: 0
---

Recordings over 2GB produced an unplayable file: the muxer never wrote the
moov atom on 32-bit offset overflow. Fixed by enabling 64-bit offsets; the
regression test records a synthetic >2GB stream and asserts playability.

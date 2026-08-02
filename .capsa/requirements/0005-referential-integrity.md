---
id: 5
title: "Every internal reference resolves; nothing is checked by faith"
level: must
status: met
opened: 2026-08-02
verification:
  status: verified
  method: test
  evidence_ref: "tools/validator/validate.py::check_links"
  checked_at: 2026-08-02
---

A graph kept in plain files has no foreign keys, so a checker is the only
enforcement there is. Every internal `links[].to` and `scoped_status[].scope`
must resolve to an existing record (external `@capsule/path` addresses are
exempt — a capsule stays valid alone). A link whose target is an ancestor
of the record carrying it is refused: the path already states it.

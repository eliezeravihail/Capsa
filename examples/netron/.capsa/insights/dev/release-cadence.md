---
kind: dev
title: "802 tags on one repository — releases are near-continuous, not events"
created: 2026-08-02
tags: [releases, process]
---

`git tag | wc -l` returns 802. Across ~10,150 commits that is roughly one
tag per thirteen commits — closer to a version-stamped commit stream than
to the traditional idea of "a release" as a curated, deliberated moment.

This capsule documents three releases (`releases/0001` through `0003`)
out of 802 real tags — the oldest, one mid-history major bump, and the
current one — chosen for what each shows about the project's shape, not
because the other 799 don't exist or don't matter. Recording all 802
would not make this capsule more accurate; it would make the signal (a
few releases worth understanding) indistinguishable from the noise (a
version bump on every merge). See the write-up filed against Capsa itself
for the format-level question this raised: there's no field on a release
distinguishing "routine" from "worth a human reading years later," so a
reader with all 802 records has no structural way to tell which is which
short of reading every one.

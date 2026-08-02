---
kind: dev
title: "Every commit in the cloned history — 10,147 of them — is authored by one person"
created: 2026-08-02
tags: [team, risk]
---

`git log --format='%aN' | sort | uniq -c` returns exactly one line: Lutz
Roeder. No co-maintainer, no bot account, no second name anywhere in
10,000+ commits and 800+ tags. This is not a gap in this capsule's
research — it's the actual shape of the project's authorship.

Consequence for this capsule: there is no `organization/` capsule to
write for Netron. An organization format models a company's roster,
roles, and team structure; a solo maintainer has no team to model, and
inventing role/team records to satisfy the format's shape would document
a fiction. The honest statement of "who works on this" is this insight,
in the project capsule, not a one-member organization capsule elsewhere.

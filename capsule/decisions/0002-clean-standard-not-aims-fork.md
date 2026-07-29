---
id: 2
title: "Start clean (Capsa) instead of extending aims; aims stays as-is"
status: accepted
date: 2026-07-29
tags: [scope]
---

## Context
aims proved the artifact discipline (ADRs, plans, memory tree) but couples
it to solo-session hooks, and its name (AI Manager System) no longer fits
a passive standard.

## Decision
Create Capsa as a clean standard inspired by aims. aims remains untouched.

## Consequences
No migration burden on aims; Capsa adds the missing primitives (formal
requirements, issues, dependencies/licensing, releases, dev/design
insights, the verification block).

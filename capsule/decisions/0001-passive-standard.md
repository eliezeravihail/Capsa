---
id: 1
title: "Capsa is a passive file-format standard, not software with an API"
status: accepted
date: 2026-07-29
discussion_ref: null
tags: [architecture]
---

## Context
Earlier designs considered an API-exposing capsule library and an optional
hooks layer for solo self-maintenance.

## Decision
The standard is passive data only. Updating is external — whoever operates
on a project writes its capsule. No hooks ship with the standard; anyone
may build them on top, separately.

## Consequences
Nothing to run or maintain; the format is the entire contract; consumers
implement their own read/write against SPEC + schema.

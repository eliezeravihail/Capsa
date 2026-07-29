---
id: 1
title: "Use FFmpeg (LGPL build) for encoding, dynamically linked"
status: accepted
date: 2026-07-04
supersedes: null
superseded_by: null
discussion_ref: 1
tags: [licensing, media]
---

## Context
We need H.264 encoding. Native encoders mean months of work; FFmpeg is the
industry standard but its default build includes GPL components.

## Decision
Use the LGPL build of FFmpeg, dynamically linked, so the proprietary binary
remains compliant.

## Consequences
- `ffmpeg` enters `dependencies/` at tier `review` with this decision as
  its admitting record.
- Static linking is off the table without revisiting this ADR.

## Alternatives considered
Native x264 binding (GPL — rejected); OS-native encoders (platform lock-in).

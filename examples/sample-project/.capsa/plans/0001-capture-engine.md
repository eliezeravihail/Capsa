---
id: 1
title: "Capture engine with pause/resume"
kind: initiative
status: completed
opened: 2026-07-03
completed: 2026-07-19
priority: P1
target_date: 2026-07-20
requirement_refs: [1]
decision_refs: [1]
links:
  - {rel: aims_at, to: milestones/1-0-ga}
---

## Goal
Implement the capture pipeline satisfying requirement 0001.

## Work breakdown
- [x] frame capture loop — 30fps, region select
- [x] pause/resume without file split
- [x] MP4 mux via ffmpeg

## Verification
`pytest tests/test_capture.py` green; manual 10-minute session.

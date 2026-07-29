---
kind: dev
title: "Calibrate the validator on known-bad before trusting green"
created: 2026-07-29
tags: [method]
---

During authoring, the validator caught a real error (a code-kind insight
filed under insights/dev/) only because we ran it before commit; and an
induced violation confirmed it actually fails. A checker that has never
seen a defect proves nothing — calibrate on known-good AND known-bad.

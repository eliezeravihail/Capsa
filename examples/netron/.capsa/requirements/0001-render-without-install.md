---
id: 1
title: "Open and render a model in the browser with nothing installed"
level: must
status: met
opened: 2017-12-04
verification:
  status: verified
  method: manual
  evidence_ref: "https://netron.app — source/browser.js is the browser entry point"
  checked_at: 2026-08-02
---

README.md's install section leads with "**Browser**: Start the browser
version" before any download instructions. `source/browser.js` parses and
renders a model client-side; `source/server.py` exists only to serve local
files to that page (`components/viewer/components/browser`,
`components/viewer/components/python-package`).

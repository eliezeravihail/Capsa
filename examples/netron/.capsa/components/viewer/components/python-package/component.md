---
title: "Python package host"
status: active
created: 2017-12-04
code_globs: ["source/server.py", "package.py", "pyproject.toml"]
links:
  - {rel: implements, to: requirements/0004-python-package-api}
  - {rel: exposes, to: interfaces/python-api}
---

`pip install netron` gets a local HTTP server (`source/server.py`) that
serves the same browser view to a tab it opens, plus the `netron` CLI and
`netron.start()` API (`interfaces/python-api.md`) that launch it.

**Boundaries.** `server.py` serves files and hosts the page; it does not
parse models. `netron:main`'s job ends at "open a browser tab pointed at
this local server."

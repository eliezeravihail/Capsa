---
title: "Python package: `netron [FILE]` CLI and `netron.start(file)` API"
status: stable
created: 2017-12-04
since: "1.0.0"
code_globs: ["pyproject.toml", "source/server.py"]
links:
  - {rel: exposes, to: components/viewer/components/python-package/component}
---

`pyproject.toml` declares `[project.scripts] netron = "netron:main"` — the
CLI. README.md documents the same package importable as
`netron.start('[FILE]')`. Both forms open a local server
(`source/server.py`) and a browser tab pointed at it; the promise to
anything scripting against this package is that both entry points keep
working the same way release to release, independent of which model
formats are added or dropped underneath them.

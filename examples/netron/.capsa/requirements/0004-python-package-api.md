---
id: 4
title: "Ship a pip-installable package with a Python API and a CLI"
level: must
status: met
opened: 2017-12-04
verification:
  status: verified
  method: manual
  evidence_ref: "pyproject.toml [project.scripts]: netron = \"netron:main\""
  checked_at: 2026-08-02
links:
  - {rel: implements, to: components/viewer/components/python-package/component}
  - {rel: meets, to: interfaces/python-api}
---

README.md: "`pip install netron`, then run `netron [FILE]` or
`netron.start('[FILE]')`." Both the CLI form and the importable form are
promised in one line — `interfaces/python-api.md` records this as the
contract, since it is a promise to anything that imports `netron`, with a
lifecycle independent of any one release.

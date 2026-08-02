---
name: "@playwright/test"
version: "1.62.1"
ecosystem: npm
license: Apache-2.0
tier: allow
direct: true
decision_ref: null
added: 2025-08-10
---

devDependency: drives `test/browser.spec.js` and `test/desktop.spec.js` —
end-to-end tests against the rendered viewer, not just the parsers.
Apache-2.0, the one non-MIT license among Netron's direct dependencies;
still `allow` tier on its own terms.

**This filename used to be impossible to get right.** `name` is
`@playwright/test`, and a filename can't hold `/`. Filed as
`.capsa/issues/0004-scoped-package-name-breaks-dependency-filename.md` in
the Capsa repository, and fixed there (project SPEC §2.2, 0.8.0): `/`
escapes to `--` in the derived filename only, never in `name` itself —
`npm-@playwright--test.md`, which is this file.

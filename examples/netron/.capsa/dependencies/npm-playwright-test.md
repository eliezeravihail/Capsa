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

**This record is deliberately left non-conforming.** SPEC §2.2 names this
file `npm-@playwright/test.md` — but `/` cannot appear in a filename, and
`name` here is the real npm identifier, not a sanitized stand-in for one.
There is no escaping convention in the format for an ecosystem whose
identifiers routinely contain path separators (npm scoped packages:
`@playwright/test`, `@babel/core`, `@types/node`...). Filed as
`.capsa/issues/0004-scoped-package-name-breaks-dependency-filename.md`
in the Capsa repository itself.

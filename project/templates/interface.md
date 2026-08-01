---
title: "<The contract others depend on>"
status: proposed        # proposed | stable | deprecated | removed
created: <YYYY-MM-DD>
since: null             # version it first shipped in
deprecated_in: null     # REQUIRED once status is deprecated or removed
removed_in: null        # REQUIRED once status is removed
code_globs: []
links: []               # e.g. {rel: exposes, to: components/<slug>/component}
---

The contract, stated as a promise to whoever depends on it.

**Compatibility.** What callers may rely on, and what may change under them.

**Migration.** Filled in when this is deprecated — where consumers go instead.

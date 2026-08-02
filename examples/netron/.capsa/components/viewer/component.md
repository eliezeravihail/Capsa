---
title: "Viewer"
status: active
created: 2017-11-01
code_globs: ["source/app.js", "source/view.js", "source/grapher.js", "source/dagre.js", "source/worker.js", "source/index.js", "source/index.html", "source/grapher.css"]
---

The rendering core: takes a parsed model graph (produced by a
`components/formats/` parser) and lays it out and draws it — node
positions via `dagre.js`, the interactive canvas via `grapher.js`,
`worker.js` for off-main-thread work on large graphs.

**Boundaries.** Knows nothing about any specific model format — it
consumes the format-agnostic graph representation the parser layer
produces. Format modules never reach into this layer's internals directly;
they hand back a graph.

One implementation, three hosts: `components/viewer/components/browser`,
`components/viewer/components/desktop`, and `components/viewer/components/
python-package` each embed this same view rather than re-implement it —
the point of `decisions/0001-electron-for-desktop-app.md`.

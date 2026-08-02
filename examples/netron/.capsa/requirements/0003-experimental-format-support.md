---
id: 3
title: "Offer experimental support for a second tier of emerging formats"
level: should
status: met
opened: 2023-05-07
verification:
  status: verified
  method: manual
  evidence_ref: "README.md § experimental formats; source/mlir.js added iteratively (see releases)"
  checked_at: 2026-08-02
links:
  - {rel: implements, to: components/formats/component}
---

README.md's second line: "Netron has experimental support for MLIR, JAX,
GGUF, RKNN, ncnn, MNN, PaddlePaddle and scikit-learn." `should`, not
`must` — README itself draws the line, and the project's own component
statuses in `components/formats/components/` mirror it (a component's
`status` field has no `experimental` value, so this is stated in each
such component's body rather than forced into a field that doesn't have
room for it — see `insights/dev/format-catalog-scope.md`).

`opened` is dated to when MLIR support first started landing
(`Add MLIR support (#1044)`, 2023-05-07 — the first of many incremental
commits reusing the same PR/issue number over the next three years)
rather than to the project's founding — this requirement describes a tier
that grew later, not an original goal.

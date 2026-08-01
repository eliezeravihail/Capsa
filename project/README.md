# Capsa — project format

The **project** capsule format: what one project needs, plans, decides,
discusses, fixes, ships, and learns. Record types: `requirements`, `plans`,
`decisions`, `discussions`, `issues`, `dependencies`, `releases`, `insights`,
`components`, `interfaces`, `milestones`, `lines`, `platforms`, `charter`.

- **Normative spec:** [`SPEC.md`](./SPEC.md)
- **Schemas:** [`schema/`](./schema/) — one per record type, mirroring the spec
- **Templates:** [`templates/`](./templates/) — a starting file per record type

It inherits the shared grammar — addresses, `links`, tombstones, the
verification block — from [`../core/PRINCIPLES.md`](../core/PRINCIPLES.md),
which every capsa format inherits and which defines no record types of its own.

A capsule of this format is installed as `.capsa/` at the root of the product
repository. Validate one with
[`../tools/validator/validate.py`](../tools/validator/validate.py).

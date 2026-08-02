# Capsa — project format

The **project** capsule format: what one project needs, plans, decides,
discusses, fixes, ships, and learns. Record types: `requirements`, `plans`,
`decisions`, `discussions`, `issues`, `dependencies`, `releases`, `insights`,
`components`, `interfaces`, `milestones`, `lines`, `charter`.

- **Normative spec:** [`SPEC.md`](./SPEC.md)
- **Templates:** [`templates/`](./templates/) — a starting file per record type

It inherits the shared grammar — placement, addresses, `links`, tombstones,
the verification block — from [`../core/PRINCIPLES.md`](../core/PRINCIPLES.md),
which every capsa format inherits and which defines no record types of its own.
Core requires each format to say which of its record types are **normative**
(bind their subtree) and which are **descriptive**; this format's answer is
[`SPEC.md` §2.7](./SPEC.md).

A capsule of this format is installed as `.capsa/` at the root of the product
repository. Validate one with
[`../tools/validator/validate.py`](../tools/validator/validate.py).

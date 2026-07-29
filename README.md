# Capsa

*A unified, portable project-management capsule — in plain, readable files.*

**Capsa** is a **standard file format**, not a program. It defines how a
project carries its own management truth — requirements, planning,
decisions, discussions, bugs & risks, dependencies & licenses, releases,
and development/design insights — as human-readable files that live
**inside the project's own repository**.

A Capsa capsule has **no active mechanism**: no hooks, no daemon, nothing
to run or maintain. It is passive data in an agreed format. Any tool — an
orchestration engine, a solo AI coding session, or a human with a text
editor — can read and write it, as long as it follows the spec.

## Why

Project-essential knowledge (why a decision was made, what a bug was and
how it was fixed, what the design rationale is) is **part of the project**.
It should travel with the project, survive any tool, and be readable
without one. Locking it inside an external management system makes that
system a foreign owner of the project's own truth.

Capsa puts that truth back where it belongs — in the project — in a format
that is:

- **Portable.** It's just files in the repo. Clone the project, get its
  full management history. Delete every tool; the capsule remains whole.
- **Readable.** Every record is Markdown a human can read, with a small
  YAML frontmatter header a machine can parse. One file serves both.
- **Dependency-free.** No runtime, no service, no library to install. The
  format *is* the contract.
- **Tool-agnostic.** The spec is the only thing consumers agree on. Version
  coordination is a single `capsa_version` field — not a protocol.

## What's in a capsule

Installed into a target project as a single `.capsa/` directory (the
accepted dot-directory convention, like `.git/` or `.github/`):

```
.capsa/
├── capsule.yaml          # manifest: capsa_version, project identity, status
├── charter.md            # the project's upfront vision, constraints, ground rules
├── requirements/         # NNNN-slug.md — needs, formally trackable to met/unmet with evidence
├── plans/                # NNNN-slug.md — initiatives with work-breakdown, priority, target date
├── decisions/            # NNNN-slug.md — architecture decisions (ADRs), append-only
├── discussions/          # NNNN-slug.md — substantive considerations (may graduate to a decision)
├── issues/               # NNNN-slug.md — bugs / risks / tasks, with lifecycle & severity
├── dependencies/         # <eco>-<name>.md — one record per dependency: license, tier, decision
├── NOTICES               # generated third-party attribution (from dependencies/)
├── releases/             # NNNN-vX.Y.Z.md — what shipped, when, from which commit
└── insights/
    ├── dev/              # development insights — lessons, rationale, what failed
    ├── design/           # design insights — UX, product, visual-language reasoning
    └── code/             # code-anchored notes (carry `code_globs`)
```

A distinguishing property: **claims that can be checked are formal fields,
not prose.** A requirement's `met` status, a dependency's license `tier`, a
closed bug's `regression_ref`, a release's included issues — all are
structured frontmatter with evidence references, so any tool can compute
compliance in code (*"no deny-tier dependency without an admitting
decision"*, *"no open S1 at release"*). Prose explains; fields prove.

Every record is `<frontmatter> + <Markdown body>`. The frontmatter fields
are defined per record type in [`SPEC.md`](./SPEC.md) and enforced by the
JSON Schemas in [`schema/`](./schema/). Copy-ready starters live in
[`templates/`](./templates/); a filled example is in
[`examples/`](./examples/).

## Using it

Capsa is passive, so "using it" just means reading and writing the files
per the spec:

- **A human** reads `.capsa/` in any editor, or on GitHub.
- **An orchestration engine** (e.g. a multi-agent team manager) is the
  writer: it reads the capsule to load project context and writes records
  back as part of its normal commits. Capsa holds the project truth; the
  engine holds only live run-state and cross-project views.
- **A solo AI session** can read and append records directly.

Want self-maintaining behavior (auto-consolidation, planning nudges)? That
lives **on top of** Capsa, as a separate optional layer — it is not part of
the standard. The standard stays passive on purpose.

## Validating a capsule (optional)

The format is the source of truth; validation is a convenience, never
required. A dependency-free checker is provided:

```sh
python3 validator/validate.py path/to/project/.capsa
```

It checks the manifest and every record's frontmatter against
[`schema/`](./schema/). It only reads — it never writes or "fixes."

## Status

`capsa_version` **0.2.0** — see [`VERSION`](./VERSION) and
[`SPEC.md`](./SPEC.md). The format is young; the shape is deliberately
small so it can stabilize.

## License

The Capsa specification and this repository are released under the MIT
License — see [`LICENSE`](./LICENSE). Capsules you create are yours; the
format imposes nothing on their contents.

---

*Capsa is the Latin word for the cylindrical case that held rolled
manuscripts — a portable box of readable records. That is exactly what
this is.*

# Proposal 0001 — typed links and the component tree

**Status:** draft, for review. Nothing is adopted; no file under `core/`,
`project/`, `organization/`, `SPEC.md`, `schema/`, `validator/`,
`templates/` or `examples/` is changed by this document.

**Written against:** `main` @ `f9b8f6b` — i.e. *after* the umbrella reframe
(`core/` + format family), the organization format v0.1.0, and the
validator's `--json`.

**Problem it addresses:** an agent must be able to receive *only the
relevant neighbourhood* of what it is working on. That is a graph query,
and three mechanics in the current grammar prevent one.

---

## 1. Baseline — what already exists

Recorded so this proposal is read against the real repository, not an
earlier picture of it:

- **`core/PRINCIPLES.md`** — shared principles and record grammar; declares
  explicitly that the core defines *no* record types.
- **The umbrella** — `core/` · `project/` · `organization/` · `tools/`, with
  a manifest declaring `capsa_core`, `format`, `format_version`.
- **`organization/SPEC.md` v0.1.0** — members, roles, teams, onboarding,
  presets, insights, managed-project pointers; optional `charter.md` and
  `policies/`. Issues/discussions/decisions are *deliberately* absent.
- **`SPEC.md` v0.2.0** — the project format, still at the root, moving to
  `project/SPEC.md` in the tidy-up (per `project/README.md`).
- **`validator --json`** — findings emitted from the same list as the human
  text (#1).

Three things this proposal does **not** re-propose, because they exist:
capsule kinds (solved better as `format:` + a shared core), team/role
records (organization format), and a machine-readable validator mode.

## 2. What is still missing

**(a) No component axis.** Nothing in the project format describes the
system itself — modules, boundaries, ownership. Decisions record *changes*
to architecture; `charter.md` holds vision; but "what is the architecture
now" has no home. This is also the natural partition key for every other
record type (issues per component, requirements per subsystem, ownership
per component). Without it, each directory is one unsorted pile — the
failure mode that shows up at tens of thousands of records, not at fifty.

**(b) Untyped edges.** The core grammar says `*_ref`/`*_refs` hold "the
id/slug of another record, or a path". The *meaning* of an edge is carried
by the **field name**, which means every edge must be declared in advance,
per record type, by whoever writes the format spec. An insight cannot link
to a decision, a discussion cannot link to an issue, a requirement cannot
link to a component — not because it is forbidden, but because no field
exists and adding one is a spec change. A general graph cannot be built
this way, and neither can a neighbourhood query.

**(c) Two sibling formats identify records differently.** The organization
format uses `<slug>.md`; the project format uses sequential `NNNN-slug.md`.
Under one shared core that is an inconsistency, and the project side is the
one that breaks: sequential numbering in a flat directory has a capacity
ceiling (9999) and, worse, assumes a **single writer** — many contributors
on branches each claiming the next number is a merge-conflict machine by
design. The organization format already demonstrates the fix, and the
project format already contains two non-sequential precedents of its own
(insights by path, dependencies by `(ecosystem, name)`).

## 3. Proposed changes

### C1 — Typed links (`core/PRINCIPLES.md`, grammar)

Add one general edge to the core grammar, available to every format:

```yaml
links:
  - {rel: implements,     to: requirements/0003-verifiable-claims}
  - {rel: depends_on,     to: components/color-engine/component}
  - {rel: constrained_by, to: "@acme/policies/license-tiers"}
```

- `rel` is a lowercase token; `to` is an address (C2). Both REQUIRED.
- **Core vocabulary:** `implements`, `enacts`, `constrained_by`,
  `discussed_in`, `supersedes`, `superseded_by`, `fixed_by`, `admitted_by`,
  `includes`, `fixes`, `meets`, `depends_on`, `affects`, `owns`,
  `anchored_to`, `learned_from`, `moved_to`.
- An unknown `rel` MUST be preserved and MAY be traversed (consistent with
  the existing "unknown keys are preserved" rule). Private vocabulary
  SHOULD use an `x-` prefix.
- **Edges are authored in one direction only; the inverse is computed by
  consumers, never stored.** Requiring both endpoints to carry the edge
  would make every link a two-file write — the operation that conflicts
  under concurrent editing — and would duplicate a fact, which principle 4
  forbids.

`links` **complements** the existing `*_ref`/`*_refs` fields; it does not
remove them. Where a format has already named an edge in a field
(`member_refs`, `plan_refs`), that field stays authoritative and readable.
`links` is what makes edges expressible *without* a spec change. For the
project format the mapping is:

| existing field | equivalent link |
|---|---|
| `plan.requirement_refs` | plan → `implements` → requirement |
| `plan.decision_refs` | plan → `enacts` → decision |
| `requirement.decision_refs` | requirement → `constrained_by` → decision |
| `decision.discussion_ref` | decision → `discussed_in` → discussion |
| `issue.fix_plan_ref` | issue → `fixed_by` → plan |
| `dependency.decision_ref` | dependency → `admitted_by` → decision |
| `release.plan_refs` | release → `includes` → plan |
| `release.issue_refs` | release → `fixes` → issue |
| `release.requirement_refs` | release → `meets` → requirement |

### C2 — Addresses, within and across capsules (`core/PRINCIPLES.md`)

The core currently says a ref holds "an id/slug or a path" without saying
how a *cross-capsule* reference is written — while the organization format
already needs one (`projects/<slug>.md` carries `capsule_ref?`). Specify it
once, in the core:

- **Internal** — a path relative to the capsule's format directory:
  `components/render/component`, `decisions/0004-tile-cache`.
- **External** — `@<capsule-slug>/<path>`, where `<capsule-slug>` is the
  identity in the target's `core/capsule.yaml`: `@acme/policies/license-tiers`.

The `@` prefix is REQUIRED for external addresses so internal and external
are distinguishable **without knowing which capsules are attached** — a
validator run against one capsule must be able to tell them apart.

**Resolution rules** — this is where portability (principle 3) is kept:

- An **internal** address that does not resolve is an **error**.
- An **external** address that does not resolve is **not an error** at
  capsule level. A project capsule MUST stay valid, and its neighbourhood
  queries answerable, with no other capsule attached; external links are
  enrichment that degrades cleanly. Unresolved external links are reported
  only by a union-level check, when both capsules are present.
- Consequently **strong links point inward**: `organization → project`
  edges ("this team owns that component", "this insight was learned there")
  live in the organization capsule, which never travels. A project MAY link
  outward to org policy; it MUST NOT depend on it to be readable.

This is what makes the two formats *federate* rather than merge, and it is
the reason the split into two homes costs nothing in cross-referencing.

### C3 — Path identity in the project format (`SPEC.md` §2.2)

Align the project format with the organization format:

- A record's **identity is its path** relative to the format directory,
  `.md` removed.
- Filenames MUST be kebab-case, OPTIONALLY prefixed `NNNN-`. The prefix
  carries **ordering only**; it need not be unique-and-monotonic, and MAY
  be omitted for new records.
- `id` becomes OPTIONAL, retained for compatibility. Where a filename
  carries `NNNN-` **and** `id` is present, they MUST agree (today's rule,
  unchanged).

### C4 — The component tree (`project/`)

A project capsule MAY carry a component tree. A component is a directory
holding a `component.md`, and MAY hold its own records and nested
components:

```
project/
├── requirements/                  cross-cutting records stay at the top
├── decisions/
└── components/
    ├── render/
    │   ├── component.md
    │   ├── issues/tiling-seam.md
    │   ├── decisions/0003-tile-cache.md
    │   └── components/tiling/component.md
    └── color-engine/component.md
```

- Any record type valid at the format root is valid inside a component
  directory, with identical fields and rules.
- A record's **owning component** is derived from its path — the nearest
  ancestor directory containing a `component.md` — and MUST NOT be
  duplicated into frontmatter (principle 4: nothing derivable is stored).
- A record at the root has no owning component; that means *cross-cutting*,
  never *unassigned*.

This is the containment tree, the same shape source code already has: a
module tree plus an import graph. It supplies the "ancestors" half of a
neighbourhood query (§5).

**Component record** (`**/component.md`):

| field | req | type | notes |
|---|---|---|---|
| `title` | ✓ | string | |
| `status` | ✓ | enum | `planned` \| `active` \| `deprecated` \| `retired` |
| `created` | ✓ | date | |
| `code_globs` | | string[] | paths in the product repo this component owns |
| `links` | | link[] | C1 |

Checkable claims: *an `active` component SHOULD declare `code_globs`*
(warning — a component may be non-code); *sibling components SHOULD NOT
have overlapping `code_globs`* (overlap makes "who owns this file"
unanswerable).

Proposed for the **project** format only. The organization format
deliberately admits a type only where it is earned, and an organization has
no components.

### C5 — Tombstones (`core/PRINCIPLES.md`)

A record MAY be replaced by a tombstone: frontmatter keeping its `title`,
plus `status: moved` and a `moved_to` link; body reduced to a pointer.

```yaml
status: moved
links: [{rel: moved_to, to: "@acme/insights/calibrate-instruments"}]
```

Needed because promotion is routine, not exceptional: an insight is
normally discovered inside a project and only later recognised as
organisational — and the two formats now have two different insight homes
(`project/insights/{dev,design,code}/` vs `organization/insights/<slug>.md`).
Without a specified move, "single home" is violated by copy-paste in the
first week.

### C6 — Referential integrity (conformance)

A conforming capsule additionally satisfies:

- every `links[].rel` is a lowercase token and every `links[].to` is a
  syntactically valid address;
- every **internal** link target resolves to an existing record (external
  targets exempt, C2);
- every directory containing record subdirectories under `components/`
  contains a `component.md`.

This is the one real cost of a graph kept in files rather than a database:
there are no foreign keys, so an edge can point at a deleted record and
nothing complains. Enforcing it in the checker is what makes "a graph in
files" a fact instead of an aspiration — and it is the point where, if
neglected, the argument for a graph database becomes correct.

### C7 — Findings carry stable codes and severity (`tools/`, validator)

`--json` exists and emits `{"path", "message"}`. For a **repair** tool to
act on a finding it needs an identifier that is not prose:

```json
{"code": "E-LINK-DANGLING", "severity": "error",
 "path": "components/render/issues/tiling-seam.md",
 "field": "links[1].to", "detail": "components/tiling/component",
 "message": "internal link target does not resolve"}
```

Severity is separately required by C4, whose claims are warnings rather
than errors — a distinction the current findings list cannot express.

**Repair itself does not belong in Capsa.** The repository's rule — the
only executable is the optional read-only validator — is a deliberate
boundary, and a `--fix` flag crosses it: a tool that rewrites records is a
maintenance mechanism, which principle 1 refuses. Repair belongs to the
operator's maintenance screen, where writing is already what the tool does.
Capsa's job is to make repair *possible* without the operator having to
pattern-match prose to decide what to repair.

## 4. Compatibility

All of it is additive: `links` is a new optional field, `NNNN-` stays
legal, `id` stays legal, `*_refs` stay authoritative, and the component
tree is optional. Every capsule conforming today still conforms.

Sequencing note: `SPEC.md` is due to move to `project/SPEC.md`
(`project/README.md`). C3 and C4 touch that file heavily, so doing the move
**first** and this proposal **after** avoids rewriting the same lines
twice.

Outward flow if adopted, in order: `core/PRINCIPLES.md` (C1, C2, C5) →
`project/SPEC.md` (C3, C4) → `schema/` (`links`; `id` required→optional;
a component schema) → `validator/` (path identity, link integrity, codes +
severity) → `templates/` → `examples/` (the sample project grows a small
component tree, so the tree is exercised rather than only described).

## 5. Neighbourhood retrieval (informative — not part of the format)

Stated only to show the format supports it. It is a consumer concern and
adds no mechanism to a capsule.

Given a seed record, its neighbourhood is: its **ancestors in the
containment tree** (the owning component and that component's parents — the
context it sits in), plus **k hops over `links` filtered by `rel`**, plus a
token budget. Deterministic and complete by construction.

Semantic similarity is useful for *ranking within* that set — never for
selecting it. A brief that silently omits a constraining decision is wrong
in a way a similarity score cannot detect. This matters because
`tools/README.md` currently describes the RAG plugin as retrieving "only
the relevant subset"; structural closure should select, and similarity
should rank inside it.

The queryable graph is a derived index (an edge table built at load,
disposable, rebuilt from Markdown) — consistent with principle 4, which
already names embeddings as derived. At the scale this targets — order 10⁵
nodes, 10⁶ edges — k-hop traversal is milliseconds in SQLite or in memory;
a dedicated graph database is not indicated at any plausible project scale.

## 6. Identified, deliberately not proposed here

Kept visible rather than dropped. Each is real; none is required to make
retrieval work, which is what this proposal is for.

- **Interface / contract records** — a plugin API or a file format has its
  own lifecycle (versions, deprecation) and is among the longest-lived
  truths in a large product. Cheap once components exist.
- **Parallel release lines** — a large product maintains several major
  versions at once. One monotonic `releases/` list cannot express lines, a
  single `fix_commit` cannot express a backport, and a scalar requirement
  `status` cannot express "met in 26, unmet in the maintained 25".
- **Platform axis** — one requirement at different statuses per platform.
- **Milestone as a record** — `milestone` is a free string on plans today,
  so nothing can hang dates off it and no consistency check is possible.
- **Quantitative targets** (performance budgets, coverage). The
  verification block is already shaped to carry these.

## 7. Proposed additions to `REQUIREMENTS.md`

Additions only; nothing deleted.

```markdown
## E. Structure and retrieval

- [ ] E1. **Typed links** — a general, machine-traversable edge between any
      two records, in the CORE grammar, so a new edge is not a spec change;
      authored in one direction, inverse computed — core
- [ ] E2. **Addresses** — internal paths and external `@slug/path`;
      internal must resolve, external may dangle, so a capsule stays
      self-contained (principle 3) and formats federate — core
- [ ] E3. **Path identity** — a record is identified by its path; no
      central number allocation, so concurrent authors never contend
      (the organization format already does this) — project
- [ ] E4. **Component tree** — a project capsule may describe the system's
      own structure; records nest under the component they belong to; the
      owning component is derived from the path, never stored — project
- [ ] E5. **Promotion preserves single home** — a record moves between
      capsules leaving a tombstone, never a copy — core
- [ ] E6. **Referential integrity** — internal links must resolve; a graph
      kept in files has no foreign keys, so the checker is the enforcement
- [ ] E7. **Selective retrieval is possible in principle** — tree plus
      typed edges suffice to compute a bounded, deterministic neighbourhood
      of any record; the query itself is a consumer concern and adds no
      mechanism to the format

## F. Tooling boundary

- [ ] F1. **The validator stays read-only** — repair is a maintenance
      mechanism and belongs to the operator, not to the format
- [ ] F2. **Findings carry stable codes and severity** — so an operator's
      repair tool never has to parse prose to decide what to repair
```

## 8. Open questions

1. **Does the operator run the validator, or re-implement its checks?** It
   must stay stdlib-only, and HaMenahel importing from this repo couples
   them. Options: vendor it, invoke as a subprocess, or validate inside the
   hydrator (which parses everything anyway) and keep this validator as the
   independent reference.
2. **Do components nest without limit?** Unlimited is simpler to specify; a
   cap is easier to render. Recommendation: unlimited, and let a UI
   collapse.
3. **Should `links` be allowed in the organization format immediately?**
   It is core grammar, so formally yes. But that format's restraint — a
   type is earned, not presumed — is worth honouring: adopt it there when
   an edge is actually needed.

# Capsa as an umbrella — and the Organization format

**Status:** draft · reframes capsa as a *family of formats* · specs the
Organization format. Supersedes the earlier "organization category" draft.

## 0. Reframe: capsa is an umbrella, not one format

capsa is an **idea**, not a single file layout: a capsule is durable,
human-readable, portable, **single-home truth — never run-state**, carried as
Markdown-with-frontmatter records a generic checker can verify. That idea is
not specific to a project. It is the shape of *any* memory an organization
wants to keep in the open.

So capsa is an **umbrella repo**: one shared **core** (principles + record
grammar) and a **family of formats** that specialize it. Each format has its
own record vocabulary and **lives in its own place** — they are *different
formats saved in different places*, not two modes of one file:

| format | what it remembers | where it lives |
|---|---|---|
| **project** | one project's needs, plans, decisions, issues, releases | `.capsa/` in the product repo |
| **organization** | the company: people, roles, teams, know-how, policies, the projects it runs | the organization-brain repo (its own home) |
| *(future)* | e.g. a personal capsule, a portfolio capsule | its own home |

## 1. The shared core (every format inherits)

- **Passive · readable · portable · single-home · truth-not-run-state ·
  versioned-by-a-field · verifiable-by-construction** (the SPEC §1 principles).
- **Grammar:** every record is UTF-8 Markdown = YAML frontmatter (machine
  fields) + prose body (for people). ISO-8601 dates; `*_ref`/`*_refs` link
  records by id/slug; unknown keys preserved.
- **The verification block** (SPEC §2.3) wherever a claim is checkable.
- A manifest declares which core + which format a capsule conforms to.
- **The core defines NO record types.** *What* records exist — requirements,
  members, issues — is each **format's** decision, never the core's. The core
  is only the conceptual infrastructure: grammar, refs, verification, manifest,
  versioning.

## 2. Two shapes: the umbrella repo, and a deployed capsule

**a) The umbrella repo** — `capsa/`: the idea, the format specs, the tools.
```
capsa/
├── core/            shared principles + grammar + schema fragments
├── project/         the project-format spec · schema · templates
├── organization/    the organization-format spec · schema · templates
└── tools/           validator · (later) a records→embeddings / vector-search plugin
```

**b) A deployed capsule** — `core/` is only the **declaration** (the manifest:
identity + which core + which format); the **format dir** holds all the records.
No record types live in `core/`.
```
# in a project repo                    # in the live-system folder (the org brain)
.capsa/                                .capsa/
├── core/                              ├── core/
│    capsule.yaml                      │    capsule.yaml
│    (format: project, core X.Y)       │    (format: organization, core X.Y)
└── project/                           └── organization/
     requirements · plans ·                members · roles · teams ·
     decisions · issues · releases ·       onboarding · insights ·
     dependencies · insights · charter     presets · projects
```

The org capsule's `.capsa/` sits **inside** the live-system folder, **beside**
the runtime DB — capsule = durable truth, DB = run-state, siblings not nested.
Same idea, different format, different place.

## 3. The Organization format — think like a company

A company is a **persistent entity that outlives its members**. People (agents
*and* humans) join, work, and leave; the **roles, teams, decisions, policies,
and know-how persist**. The organization capsule is that persistent memory,
kept in the open so it survives any single person walking out the door.

### 3.1 Manifest — `.capsa/capsule.yaml` (in the org-brain repo)

```yaml
capsa_core: "0.1.0"          # shared core it conforms to
format: organization         # which family member this is
format_version: "0.1.0"
organization:
  name: "Avihail"            # REQUIRED
  slug: avihail              # REQUIRED
  created: 2026-07-30        # OPTIONAL
status: active               # planning|active|maintained|paused|archived
```

### 3.2 Record types

**Member** (`members/<slug>.md`) — a person on the team, **agent or human**.
| field | req | type | notes |
|---|---|---|---|
| `slug` `name` | ✓ | string | file name / human name |
| `kind` | ✓ | enum | `agent` \| `human` |
| `role_ref` | ✓ | string | the role filled (→ `roles/`) |
| `status` | ✓ | enum | `onboarding`\|`active`\|`paused`\|`departed` |
| `joined` | ✓ | date | `left` set on departure |
| `model_tier` `tools` | | | agents only — tier + permission-relevant caps |
| `insight_refs` | | string[] | insights this member authored |
| `contact` | | string | humans |

**Role** (`roles/<slug>.md`) — a position independent of who fills it:
`title`, `responsibilities[]`, `raci`, `required_skills[]`, `permissions_ref`,
`onboarding_ref`.

**Team** (`teams/<slug>.md`) — a grouping (teams are part of the company):
`name`, `purpose`, `member_refs[]`, `role_refs[]`, `preset_ref`, `status`.

**Onboarding** (`onboarding/<slug>.md`) — a path to bring a new/replacement
member up to speed **from captured knowledge**: `scope` (`org`/`role`/`team`),
`reading_refs[]` (charter, decisions, insights), `steps[]`, `status`.

**Preset** (`presets/<slug>.md`) — a reusable staffing config (replaces the
ad-hoc `presets.json`): `name`, `member_slugs[]`, `formality`.

**Policy** (`policies/<slug>.md`) — a company rule (security/permissions/
conduct/egress), with a `verification` block when machine-checkable.

**Managed project** (`projects/<slug>.md`) — a pointer to a project the company
runs; the truth lives in *that* project's own capsule (single-home). Fields:
`name`, `repo`, `capsule_ref`, `registered`, `status`.

**Insight** (`insights/<slug>.md`) — the know-how that persists across
turnover; each links its author (`member_ref`) and domain (`role_ref`). An
org-format type in its own right, not borrowed from the project format.

**Optional, only if the org wants them:** `charter.md` (mission, values, ground
rules) and `policies/` (company rules — the Policy type above).

**Deliberately absent:** `issues/`, `discussions/`, `decisions/`. Presuming an
organization keeps those is a guess imported from the project format — a format
earns a record type only where the org genuinely needs one.

## 4. The continuity loop — the point of an org capsule

1. A member works → accumulates `insights/`, linked from their `members/` record.
2. They leave → `status: departed`, `left` set. **The insights remain.**
3. A replacement joins → `status: onboarding`, follows `onboarding/<role>`,
   which reads the role's insights + charter + decisions → **inherits the
   know-how instead of starting cold.**
4. Identical for **agents and humans** — a person leaving no longer takes the
   company's memory with them.

## 5. What stays out — run-state (core principle 5)

Who is working *now*, cost/turn counters, the event stream, in-flight boards —
the operating tool's concern, **never** written to a capsule. This is what lets
the runtime DB shrink to a rebuildable run-state cache: every durable company
fact lives here, in the open.

## 6. Tools & semantic search — in the umbrella

Tools live in the umbrella repo (`capsa/tools/`) and operate on any capsule.
Anything derivable is computed, never stored — so a **plugin that converts
records to embeddings** and serves **vector search** over `insights/`,
`decisions/`, `discussions/` is exactly such a tool: optional, and rebuildable
from the Markdown. The capsule stays the source of truth; the embedding/vector
store is a cache you can delete and regenerate. Everything that does *not* need
vector search stays a plain, ordered, human-readable record.

## 7. Open questions

- Core vs format versioning — one `capsa_core` shared, each format its own
  `format_version`? (Proposed above.)
- Where exactly does the org-brain capsule sit relative to `HM_ORG_DIR` — at
  its root as `.capsa/`, or is the whole brain the capsule?
- One org capsule per company, or one per business unit for large orgs?

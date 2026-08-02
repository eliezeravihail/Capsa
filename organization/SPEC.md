# Capsa — organization format (v0.2.0)

The **organization** capsule: a company's durable memory — its people (agents
*and* humans), roles, teams, presets, know-how, and the projects it runs. It
inherits the [core](../core/PRINCIPLES.md) and lives in the organization-brain
repo (in HaMenahel: `HM_ORG_DIR`, backed up). Rationale + operating model
(DB cache, RAG, MD-wins): see `../docs/organization-format.md`.

## Manifest — `core/capsule.yaml`
```yaml
capsa_core: "0.4.0"
format: organization
format_version: "0.2.0"
organization: { name, slug, created }
status: planning|active|maintained|paused|archived
```

## Record types (under `organization/`)

- **Member** (`members/<slug>.md`) — agent *or* human. `slug`, `name`,
  `kind` (agent|human), `role_ref`, `status`
  (onboarding|active|paused|departed), `joined`, `left?`, `model_tier?`,
  `tools?[]`, `insight_refs?[]`, `contact?`. On departure the record flips to
  `departed`; the insights it authored persist.
- **Role** (`roles/<slug>.md`) — `slug`, `title`, `responsibilities[]`,
  `raci?`, `required_skills?[]`, `permissions_ref?`, `onboarding_ref?`.
- **Team** (`teams/<slug>.md`) — `slug`, `name`, `purpose`, `member_refs[]`,
  `role_refs[]`, `preset_ref?`, `status`.
- **Onboarding** (`onboarding/<slug>.md`) — `slug`, `scope` (org|role|team),
  `scope_ref?`, `title`, `reading_refs[]`, `steps[]`, `status`. Brings a
  new/replacement member up to speed from captured knowledge.
- **Preset** (`presets/<slug>.md`) — `slug`, `name`, `member_slugs[]`,
  `formality`.
- **Insight** (`insights/<slug>.md`) — the know-how that persists across
  turnover; links `member_ref` (author) + `role_ref` (domain).
- **Managed project** (`projects/<slug>.md`) — a *pointer* only; the project's
  truth lives in its own capsule. `slug`, `name`, `repo?`, `capsule_ref?`,
  `registered`, `status`.

## Optional
`charter.md` (mission / values / ground rules) · `policies/` (company rules).

## Placement — normative and descriptive

Core §Placement requires each format to say which of its record types bind
their subtree. The test is the same one the project format uses: would
removing this record permit something beneath it that is not permitted now?

| Type | | Why |
|---|---|---|
| `policies/` | **normative** | a company rule; it is the obligation |
| `charter.md` | **normative** | the frame everything sits inside |
| `roles/` | **normative** | responsibilities and permissions bind whoever fills the role |
| `onboarding/` | **normative** | what a member is required to have read |
| `members/`, `teams/`, `presets/` | descriptive | who exists, and how they are grouped |
| `insights/` | descriptive | what was learned; it informs, it does not bind |
| `projects/` | descriptive | a pointer; the truth is in that project's capsule |

An organization capsule MAY nest: a team is a directory holding a
`team.md` and its own `members/`, `roles/`, `policies/`, and nested teams —
the same shape the project format gives a component. A flat capsule (every
record directory at the root) stays conforming; nesting is what lets a
division's policy bind its own people without binding the whole company.

The consequence is the one the format exists for: **what governs a member is
the walk from that member's record up to the root** — their role, their
team's policies, the company's policies, the charter. It is derived from
where they sit, never declared on the record, and it changes correctly when
someone is moved between teams.

This is a second, independent walk from the project format's. What binds a
*person* comes from the organization tree; what binds a piece of *work* comes
from the project tree. They meet only in a reader that holds both, and
neither capsule references the other to make it happen.

## Deliberately absent
`issues/`, `discussions/`, `decisions/` — presuming an organization keeps those
is a guess imported from the project format. A type is earned only where the
org genuinely needs it.

## Changelog
- **0.2.0** — the normative/descriptive classification core v0.4.0 requires,
  and optional team nesting, so what governs a member is derived by walking up
  from their record. Additive: a flat v0.1.0 capsule conforms unchanged.

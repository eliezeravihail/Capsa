# Capsa — organization format (v0.1.0)

The **organization** capsule: a company's durable memory — its people (agents
*and* humans), roles, teams, presets, know-how, and the projects it runs. It
inherits the [core](../core/PRINCIPLES.md) and lives in the organization-brain
repo (in HaMenahel: `HM_ORG_DIR`, backed up). Rationale + operating model
(DB cache, RAG, MD-wins): see `../docs/organization-format.md`.

## Manifest — `core/capsule.yaml`
```yaml
capsa_core: "0.1.0"
format: organization
format_version: "0.1.0"
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

## Deliberately absent
`issues/`, `discussions/`, `decisions/` — presuming an organization keeps those
is a guess imported from the project format. A type is earned only where the
org genuinely needs it.

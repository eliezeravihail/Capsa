# Capsa — Requirements

The requirement list this format is built against. Every item was approved
explicitly; items later found wrong are struck through with a reason, never
deleted. The spec (`SPEC.md`) must satisfy every unstruck line; `[x]` means
the current spec covers it, with the section noted.

## A. What a capsule must CONTAIN (project truth, single home)

- [x] A1. **Charter** — upfront vision, constraints, ground rules — §4.8
- [x] A2. **Requirements** — the project's needs, formally trackable to
      met/unmet with evidence — §4.1
- [x] A3. **Plans** — initiatives that decompose into sub-tasks; work-items
      end, the project does not — §4.2
- [x] A4. **Decisions (ADR)** — append-only, supersede-only — §4.3
- [x] A5. **Discussions** — substantive considerations, may graduate to a
      decision — §4.4
- [x] A6. **Issues** — bugs, risks, and tasks: severity, lifecycle, single
      owner, fix + regression evidence, reopen count — §4.5
- [x] A7. **Dependencies & licensing** — per-item license (SPDX), tier,
      admitting decision, hash; generated `NOTICES` — §4.6
- [x] A8. **Insights** — development, design, and code-anchored knowledge;
      not limited to code — §4.9
- [x] A9. **Releases** — what shipped, when, from which commit, containing
      which work — §4.7
- [x] A10. **Roadmap signals** — priority, target date, milestone on plans
      (roadmap is derived, not stored) — §4.2

## B. What a capsule must BE (format properties)

- [x] B1. **Passive** — zero active mechanism: no hooks, daemons, or
      anything that runs — §1.1
- [x] B2. **Human-readable** — Markdown + YAML frontmatter; one file serves
      human and machine — §1.2, §2.1
- [x] B3. **Portable & self-contained** — a directory inside the project's
      repo; survives without any tool — §1.3
- [x] B4. **Dependency-free** — the format is the contract; validation is
      optional and read-only — §1.1, §5
- [x] B5. **Single home / no duplication** — each fact lives in exactly one
      record; cross-references, never copies — §1.4
- [x] B6. **Version by field** — `capsa_version` in the manifest; no
      protocol, no negotiation — §1.6, §6
- [x] B7. **Tool-agnostic** — engine, solo AI session, or human editor are
      equal citizens — §1, §5
- [x] B8. **Formally verifiable fields** — every claim subject to automated
      compliance checking is a structured field with an evidence reference,
      not prose (license tier, requirement satisfaction, issue closure
      evidence, release integrity) — §2.3, §4.1, §4.5, §4.6, §4.7

## C. What a capsule must NOT contain (lives elsewhere)

- [x] C1. No API-exposing software or service — the capsule is data — §1.1
- [x] C2. No live run-state (shifts, turns, cost, telemetry) — that is the
      operator's disposable runtime layer — §1.5
- [x] C3. No company-wide policy (license allow/deny tiers policy, SLA
      targets) — capsules carry facts; policy lives with the operator — §4.6
- [x] C4. No cross-project/company-brain insights — only this project's —
      §4.9
- [x] C5. No product code — the capsule describes the project, the repo
      holds the product — §2

## D. Interoperability

- [x] D1. A consumer tolerates unknown files and unknown frontmatter keys
      (forward compatibility) and preserves them on write — §2, §2.1
- [x] D2. A writer must leave the capsule conforming — §5
- [x] D3. Deliberate exclusions (C1-C5) are documented so they are not
      re-litigated as "gaps" — this file

## E. Structure and retrieval (0.3.0)

The requirement behind all of these: an agent must be able to receive **only
the relevant neighbourhood** of what it is working on. That is a graph query,
and E1-E4 are what make one expressible.

- [x] E1. **Typed links** — a general, machine-traversable edge between any
      two records, defined in the CORE grammar so a new kind of edge is not a
      spec change; authored in one direction, inverse computed by consumers —
      core §Links
- [x] E2. **Addresses** — internal paths and external `@slug/path`; internal
      must resolve, external may dangle, so a capsule stays self-contained
      (B3) and formats federate instead of merging — core §Addresses
- [x] E3. **Path identity** — a record is identified by its path; no central
      number allocation, so concurrent authors never contend (the sibling
      organization format already identifies this way) — §2.2
- [x] E4. **Component tree** — a project capsule may describe the system's
      own structure; records nest under the component they own; the owning
      component is derived from the path, never stored (B5) — §2.4, §4.10
- [x] E5. **Promotion preserves single home** — a record moves between
      capsules leaving a tombstone, never a copy — core §Tombstones
- [x] E6. **Referential integrity** — internal links must resolve. A graph
      kept in files has no foreign keys, so the checker is the only
      enforcement there is — §5.7
- [x] E7. **Selective retrieval is possible in principle** — tree plus typed
      edges suffice to compute a bounded, deterministic neighbourhood of any
      record. The query itself is a consumer's concern and adds no mechanism
      to the format (B1) — §2.4, core §Links

## F. Tooling boundary (0.3.0)

- [x] F1. **The validator stays read-only** — repair is a maintenance
      mechanism, which B1 refuses; it belongs to the operator, not the format
- [x] F2. **Findings carry stable codes and severity** — so an operator's
      repair tool acts on `code`, never on `message`. Deciding what to repair
      by matching words in prose breaks on the first rewording, silently
- [x] F3. **The dependency-free path is checked, not assumed** — the
      stdlib-only parser must produce the same findings as PyYAML. It was
      silently dropping `links` when inline mappings were unhandled, which
      made E6 unverifiable on exactly the machines B4 exists for

## Decisions taken during requirement gathering (recorded, not deleted)

- Discussions are a separate lightweight type, not folded into decisions —
  a consideration is worth keeping before (or without) any decision.
- The validator is included despite "no mechanism": it *checks*, it never
  *maintains*. Read-only, run-on-demand, optional.
- Effort estimates, sprint ceremony, team rosters, and stored metrics are
  deliberately excluded: methodology and operator concerns, and metrics are
  derivable from records (storing them would duplicate).
- ~~Ship a hooks layer for solo self-maintenance~~ — rejected: we will not
  maintain a mechanism we do not use. The format is open for others to
  build one on top.

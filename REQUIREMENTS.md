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

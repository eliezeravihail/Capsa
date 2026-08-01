#!/usr/bin/env python3
"""Capsa capsule validator — read-only, stdlib-only, optional.

Usage:  python3 validator/validate.py [--json] path/to/capsule

Checks conformance rules SPEC.md §5 — manifest, per-type frontmatter, names,
verification evidence, the component tree, and link integrity. It only reads;
it never writes or "fixes". Repair is the operator's job, not the format's:
a tool that rewrites records is a maintenance mechanism, and the format is
passive by construction (core principle 1).

Exit 0 = conforming (warnings may still be present), 1 = at least one error,
2 = not a capsule.

`--json` prints
`{"conforming": bool, "findings": [{"code", "severity", "path", "field",
"detail", "message"}, ...]}` to stdout instead of the human text — the exact
same findings, not a separately-derived summary
(decisions/0004-single-findings-source.md).

`code` is the stable identifier: a program decides what to do from it, never
from `message`, which is free text and may be reworded at any time. Codes are
`E-*` (error — non-conforming) or `W-*` (warning — the spec says SHOULD, so
the capsule still conforms).

The spec is the source of truth; this checker mirrors schema/ for the
subset of YAML that capsule frontmatter actually uses (flat scalar keys,
inline lists, one-level nested blocks like `verification:`). PyYAML is
used when available; otherwise a built-in mini-parser covers that subset.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# frontmatter parsing
# --------------------------------------------------------------------------

def parse_scalar(s: str):
    s = s.strip()
    if s in ("null", "~", ""):
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s):
        return float(s)
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [] if not inner else [parse_scalar(x) for x in _split_inline(inner)]
    if s.startswith("{") and s.endswith("}"):
        # Inline mapping — `links:` entries are written this way.
        inner = s[1:-1].strip()
        out = {}
        for part in _split_inline(inner) if inner else []:
            k, sep, v = part.partition(":")
            if sep:
                out[k.strip().strip("\"'")] = parse_scalar(v)
        return out
    return s


def _split_inline(inner: str) -> list[str]:
    parts, depth, cur, quote = [], 0, "", None
    for ch in inner:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            cur += ch
        elif ch in "[{":
            depth += 1
            cur += ch
        elif ch in "]}":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def mini_yaml(text: str) -> dict:
    """Parse the YAML subset used by capsule frontmatter, without PyYAML.

    Covers: flat scalars, inline lists, inline mappings, one-level nested
    blocks (`verification:`), and block lists whose items are scalars or
    mappings (`links:`). A key with an empty value is ambiguous until the
    next line decides it — `verification:` opens a mapping, `links:` opens a
    list — so the placeholder is created as a mapping and converted on the
    first `- ` item.

    Dependency-freedom is requirement B4, so this path is not a fallback in
    the "degraded" sense: it is the one that must be right when PyYAML is
    absent. It was silently dropping `links` before inline mappings were
    handled here, which made link integrity unverifiable on exactly the
    machines the guarantee is for.
    """
    out: dict = {}
    # frame = [indent, container, parent, key] — parent/key let an empty
    # mapping placeholder be replaced by a list once a `- ` item proves it.
    stack: list[list] = [[0, out, None, None]]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()
        frame = stack[-1]
        target = frame[1]
        if line.startswith("- ") or line == "-":
            if isinstance(target, dict) and not target and frame[2] is not None:
                target = frame[2][frame[3]] = []      # it was a list after all
                frame[1] = target
            if isinstance(target, list):
                item = line[2:].strip() if len(line) > 1 else ""
                # `- key: value` starts a block mapping item.
                if item and not item.startswith(("{", "[")) and ":" in item:
                    k, _, v = item.partition(":")
                    d = {k.strip(): parse_scalar(v)}
                    target.append(d)
                    stack.append([indent + 2, d, None, None])
                else:
                    target.append(parse_scalar(item))
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.split(" #")[0] if not rest.strip().startswith(('"', "'")) else rest
        if not isinstance(target, dict):
            continue
        if rest.strip() == "":
            child: dict = {}
            target[key] = child
            stack.append([indent + 2, child, target, key])
        else:
            target[key] = parse_scalar(rest)
    return out


try:  # pragma: no cover - environment dependent
    import yaml  # type: ignore

    def load_yaml(text: str) -> dict:
        return yaml.safe_load(text) or {}
except Exception:  # PyYAML absent — use the subset parser
    load_yaml = mini_yaml


FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None
    try:
        data = load_yaml(m.group(1))
    except Exception as exc:
        return f"YAML error: {exc}"
    return data if isinstance(data, dict) else {}


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
# One structured list, appended to as checks run. Both renderings at the
# bottom of validate() — human text and --json — read from this SAME list;
# neither ever collects its own (decisions/0004-single-findings-source.md).
findings: list[dict] = []


def err(path, msg, code, field=None, detail=None, severity="error"):
    """Record one finding.

    `code` is the stable identifier a program acts on; `message` is free text
    for a human and may be reworded at any time. They are deliberately
    separate: a caller deciding what to repair by matching words in the
    message would break on the first rewording, silently. A repair tool is
    the operator's, not this validator's — this only has to make one
    possible.
    """
    findings.append({"code": code, "severity": severity, "path": str(path),
                     "field": field, "detail": detail, "message": msg})


def warn(path, msg, code, field=None, detail=None):
    """A finding that does not make the capsule non-conforming — the spec
    says SHOULD, not MUST."""
    err(path, msg, code, field, detail, severity="warning")


def is_date(v) -> bool:
    return isinstance(v, str) and bool(DATE.match(v)) or hasattr(v, "isoformat")


def need(fm, path, field, kinds=None, enum=None):
    if field not in fm or fm[field] is None:
        err(path, f"missing required field `{field}`", "E-FIELD-MISSING", field)
        return None
    v = fm[field]
    if kinds and not isinstance(v, kinds):
        err(path, f"`{field}` has wrong type ({type(v).__name__})",
            "E-FIELD-TYPE", field, type(v).__name__)
    if enum and v not in enum:
        err(path, f"`{field}`={v!r} not in {sorted(enum)}",
            "E-FIELD-ENUM", field, str(v))
    return v


def check_verification(fm, path, required):
    v = fm.get("verification")
    if v is None:
        if required:
            err(path, "missing required `verification` block",
                "E-VERIF-MISSING", "verification")
        return
    if not isinstance(v, dict):
        err(path, "`verification` must be a mapping", "E-VERIF-TYPE",
            "verification")
        return
    status = need(v, path, "status", str, {"verified", "unverified", "failed"})
    if status == "verified" and not v.get("evidence_ref"):
        err(path, "verification.status=verified without evidence_ref (SPEC §2.3)",
            "E-VERIF-NOEVIDENCE", "verification.evidence_ref")


# SPEC §2.2 (0.3.0): identity is the PATH. A name is kebab-case with an
# OPTIONAL `NNNN-` ordering prefix — no longer required, and no longer
# required to be unique or monotonic, because a central counter assumes a
# single writer and collides the moment two branches both allocate.
NAME = re.compile(r"^(?:(\d+)-)?[a-z0-9][a-z0-9-]*\.md$")
# Releases name their slug after the version (SPEC §2.2), so dots are legal.
NAME_RELEASE = re.compile(r"^(?:(\d+)-)?[a-z0-9][a-z0-9.-]*\.md$")


def records(dirpath: Path, pattern=NAME):
    """Yield (file, frontmatter) for every record in one directory."""
    for f in sorted(dirpath.glob("*.md")):
        m = pattern.match(f.name)
        if not m:
            err(f, "filename must be kebab-case, optionally NNNN- prefixed "
                   "(SPEC §2.2)", "E-NAME", detail=f.name)
            continue
        fm = frontmatter(f)
        if fm is None or isinstance(fm, str):
            err(f, fm or "missing frontmatter (--- fences)", "E-FRONTMATTER")
            continue
        # `id` is optional now; when a name carries NNNN- and `id` is present
        # too, they must still agree — a record whose two identities disagree
        # is worse than one with a single identity.
        if m.group(1) is not None and fm.get("id") is not None:
            if fm.get("id") != int(m.group(1)):
                err(f, f"frontmatter id={fm.get('id')} != filename number "
                       f"{int(m.group(1))}", "E-ID-MISMATCH", "id",
                    str(fm.get("id")))
        yield f, fm


def axis_values(root: Path) -> dict[str, set[str]]:
    """The closed sets a `scoped_status` scope may name (SPEC §2.5).

    Both axes are records rather than free strings precisely so that
    `platform:ipda` is a typo a checker can catch instead of a value that
    silently means nothing.
    """
    out = {"line": set(), "platform": set()}
    for axis, d in (("line", "lines"), ("platform", "platforms")):
        p = root / d
        if p.is_dir():
            out[axis] = {f.stem for f in p.glob("*.md")}
    return out


OPS = ("<=", ">=", "<", ">", "==")
METRIC = re.compile(r"^[a-z][a-z0-9_]*$")
SCOPE = re.compile(r"^(line|platform):([a-z0-9]+(?:-[a-z0-9]+)*)$")


def check_scoped_status(fm, f, axes) -> None:
    """Conformance rule 9."""
    rows = fm.get("scoped_status")
    if rows is None:
        return
    if not isinstance(rows, list):
        err(f, "`scoped_status` must be a list", "E-SCOPE-TYPE", "scoped_status")
        return
    for i, row in enumerate(rows):
        field = f"scoped_status[{i}]"
        if not isinstance(row, dict) or "scope" not in row or "status" not in row:
            err(f, "each scoped_status entry needs `scope` and `status`",
                "E-SCOPE-SHAPE", field)
            continue
        m = SCOPE.match(str(row["scope"]))
        if not m:
            err(f, f"scope {row['scope']!r} must be line:<slug> or "
                   f"platform:<slug>", "E-SCOPE-SYNTAX", f"{field}.scope",
                str(row["scope"]))
            continue
        axis, slug = m.group(1), m.group(2)
        if slug not in axes[axis]:
            err(f, f"scope {row['scope']!r} names no record in {axis}s/",
                "E-SCOPE-DANGLING", f"{field}.scope", str(row["scope"]))


def check_targets(fm, f) -> None:
    """Conformance rule 10."""
    rows = fm.get("targets")
    if rows is None:
        return
    if not isinstance(rows, list):
        err(f, "`targets` must be a list", "E-TARGET-TYPE", "targets")
        return
    for i, row in enumerate(rows):
        field = f"targets[{i}]"
        if not isinstance(row, dict):
            err(f, "each target must be a mapping", "E-TARGET-SHAPE", field)
            continue
        metric = row.get("metric")
        if not isinstance(metric, str) or not METRIC.match(metric):
            err(f, f"target metric {metric!r} is not a lowercase token",
                "E-TARGET-METRIC", f"{field}.metric", str(metric))
        if row.get("op") not in OPS:
            err(f, f"target op {row.get('op')!r} not in {list(OPS)}",
                "E-TARGET-OP", f"{field}.op", str(row.get("op")))
        if not isinstance(row.get("value"), (int, float)) or \
                isinstance(row.get("value"), bool):
            err(f, f"target value {row.get('value')!r} is not a number",
                "E-TARGET-VALUE", f"{field}.value", str(row.get("value")))


def check_status_companion(fm, f, status, pairs) -> None:
    """Conformance rule 11 — a status that implies a date/version must carry
    it. `deprecated` with no `deprecated_in` is the shape that leaves a
    consumer unable to plan a migration."""
    for want, companion in pairs:
        if status == want and not fm.get(companion):
            err(f, f"status={want} without `{companion}`",
                f"E-{companion.upper().replace('_', '')}-MISSING", companion)


def check_record_dirs(base: Path, root: Path | None = None) -> None:
    """Validate every record directory under `base`.

    Called for the capsule root and for each component directory: a
    record owned by a component is the same record, under the same
    rules, and must not drift into a second dialect (SPEC §2.4).
    """

    root = base if root is None else root
    axes = axis_values(root)

    for f, fm in records(base / "requirements") if (base / "requirements").is_dir() else []:
        need(fm, f, "title", str)
        need(fm, f, "level", str, {"must", "should", "may"})
        status = need(fm, f, "status", str,
                      {"proposed", "accepted", "met", "unmet", "dropped"})
        if not is_date(fm.get("opened")):
            err(f, "`opened` must be a date", "E-DATE", "opened")
        check_verification(fm, f, required=True)
        v = fm.get("verification") or {}
        if status == "met" and (not isinstance(v, dict) or v.get("status") != "verified"):
            err(f, "status=met but verification.status != verified (SPEC §4.1)",
                "E-REQ-MET-UNVERIFIED", "status")
        check_scoped_status(fm, f, axes)
        check_targets(fm, f)

    for f, fm in records(base / "plans") if (base / "plans").is_dir() else []:
        need(fm, f, "title", str)
        need(fm, f, "kind", str, {"charter", "initiative", "maintenance"})
        need(fm, f, "status", str, {"draft", "in_progress", "completed", "abandoned"})
        if not is_date(fm.get("opened")):
            err(f, "`opened` must be a date", "E-DATE", "opened")
        if fm.get("priority") not in (None, "P1", "P2", "P3"):
            err(f, f"priority {fm.get('priority')!r} invalid",
                "E-FIELD-ENUM", "priority", str(fm.get("priority")))

    for f, fm in records(base / "decisions") if (base / "decisions").is_dir() else []:
        need(fm, f, "title", str)
        need(fm, f, "status", str, {"proposed", "accepted", "superseded", "deprecated"})
        if not is_date(fm.get("date")):
            err(f, "`date` must be a date", "E-DATE", "date")

    for f, fm in records(base / "discussions") if (base / "discussions").is_dir() else []:
        need(fm, f, "title", str)
        need(fm, f, "status", str, {"open", "resolved", "archived"})
        if not is_date(fm.get("opened")):
            err(f, "`opened` must be a date", "E-DATE", "opened")

    for f, fm in records(base / "issues") if (base / "issues").is_dir() else []:
        need(fm, f, "title", str)
        kind = need(fm, f, "kind", str, {"bug", "risk", "task"})
        status = need(fm, f, "status", str,
                      {"new", "triaged", "in_progress", "awaiting_verification",
                       "closed", "rejected"})
        need(fm, f, "source", str, {"ceo", "system", "agent"})
        if fm.get("severity") not in (None, "S1", "S2", "S3", "S4"):
            err(f, f"severity {fm.get('severity')!r} invalid",
                "E-FIELD-ENUM", "severity", str(fm.get("severity")))
        if not is_date(fm.get("opened")):
            err(f, "`opened` must be a date", "E-DATE", "opened")
        if status == "closed" and kind == "bug":
            if not fm.get("fix_commit"):
                err(f, "closed bug without fix_commit (SPEC §4.5)",
                    "E-ISSUE-NOFIX", "fix_commit")
            if not fm.get("regression_ref"):
                err(f, "closed bug without regression_ref (SPEC §4.5)",
                    "E-ISSUE-NOREGRESSION", "regression_ref")
        check_verification(fm, f, required=False)

    dep_dir = base / "dependencies"
    if dep_dir.is_dir():
        for f in sorted(dep_dir.glob("*.md")):
            fm = frontmatter(f)
            if fm is None or isinstance(fm, str):
                err(f, fm or "missing frontmatter")
                continue
            name = need(fm, f, "name", str)
            need(fm, f, "version", str)
            eco = need(fm, f, "ecosystem", str, {"pypi", "npm", "vendored-js", "other"})
            tier = need(fm, f, "tier", str, {"allow", "review", "deny", "unknown"})
            need(fm, f, "direct", bool)
            if eco and name and f.name != f"{eco}-{name}.md":
                err(f, f"filename should be {eco}-{name}.md (SPEC §2.2)",
                    "E-DEP-NAME", detail=f.name)
            if tier == "deny" and fm.get("decision_ref") is None:
                err(f, "deny-tier dependency without admitting decision_ref "
                    "(SPEC §4.6)", "E-DEP-DENY-NODECISION", "decision_ref")

    for f, fm in records(base / "releases", NAME_RELEASE) if (base / "releases").is_dir() else []:
        need(fm, f, "version", str)
        commit = need(fm, f, "commit", str)
        if commit and len(str(commit)) < 7:
            err(f, "`commit` must be a sha (>=7 chars)", "E-RELEASE-COMMIT", "commit")
        if not is_date(fm.get("date")):
            err(f, "`date` must be a date", "E-DATE", "date")
        line = fm.get("line")
        if line and line not in axes["line"]:
            err(f, f"release line {line!r} names no record in lines/",
                "E-LINE-DANGLING", "line", str(line))

    ins = base / "insights"
    if ins.is_dir():
        for sub in ("dev", "design", "code"):
            for f in sorted((ins / sub).glob("*.md")) if (ins / sub).is_dir() else []:
                fm = frontmatter(f)
                if fm is None or isinstance(fm, str):
                    err(f, fm or "missing frontmatter", "E-FRONTMATTER")
                    continue
                kind = need(fm, f, "kind", str, {"dev", "design", "code"})
                need(fm, f, "title", str)
                if not is_date(fm.get("created")):
                    err(f, "`created` must be a date", "E-DATE", "created")
                if kind and kind != sub:
                    err(f, f"kind={kind} but file is under insights/{sub}/ "
                        f"(SPEC §4.9)", "E-INSIGHT-KINDDIR", "kind", str(kind))
                if kind == "code" and not fm.get("code_globs"):
                    err(f, "kind=code requires non-empty code_globs (SPEC §4.9)",
                        "E-INSIGHT-NOGLOBS", "code_globs")

    for f, fm in records(base / "interfaces") if (base / "interfaces").is_dir() else []:
        need(fm, f, "title", str)
        st = need(fm, f, "status", str,
                  {"proposed", "stable", "deprecated", "removed"})
        if not is_date(fm.get("created")):
            err(f, "`created` must be a date", "E-DATE", "created")
        # A removed contract must name both dates: the deprecation is what
        # gave consumers time, and dropping it rewrites that history.
        check_status_companion(fm, f, st, [("deprecated", "deprecated_in"),
                                           ("removed", "removed_in")])
        if st == "removed" and not fm.get("deprecated_in"):
            err(f, "status=removed without `deprecated_in`",
                "E-DEPRECATEDIN-MISSING", "deprecated_in")

    for f, fm in records(base / "milestones") if (base / "milestones").is_dir() else []:
        need(fm, f, "title", str)
        st = need(fm, f, "status", str,
                  {"planned", "active", "reached", "missed", "cancelled"})
        if not is_date(fm.get("target_date")):
            err(f, "`target_date` must be a date", "E-DATE", "target_date")
        check_status_companion(fm, f, st, [("reached", "reached")])

    for f, fm in records(base / "lines") if (base / "lines").is_dir() else []:
        need(fm, f, "title", str)
        st = need(fm, f, "status", str, {"active", "maintained", "eol"})
        if not is_date(fm.get("created")):
            err(f, "`created` must be a date", "E-DATE", "created")
        check_status_companion(fm, f, st, [("eol", "eol_date")])

    for f, fm in records(base / "platforms") if (base / "platforms").is_dir() else []:
        need(fm, f, "title", str)
        need(fm, f, "status", str,
             {"supported", "best_effort", "deprecated", "unsupported"})
        if not is_date(fm.get("created")):
            err(f, "`created` must be a date", "E-DATE", "created")


# The record directories a component (or the capsule root) may hold.
RECORD_DIRS = ("requirements", "plans", "decisions", "discussions", "issues",
               "dependencies", "releases", "insights", "interfaces",
               "milestones", "lines", "platforms")


def component_dirs(base: Path):
    """Every component directory under `base/components/`, depth-first.

    A component is a directory holding `component.md`; nesting is unlimited
    (SPEC §2.4), so this recurses through each component's own `components/`.
    """
    comps = base / "components"
    if not comps.is_dir():
        return
    for d in sorted(p for p in comps.iterdir() if p.is_dir()):
        yield d
        yield from component_dirs(d)


def check_components(root: Path) -> None:
    """The component tree — SPEC §2.4, §4.10, and conformance rule 8."""
    owned_globs: dict[Path, list[tuple[Path, str]]] = {}
    for d in component_dirs(root):
        rec = d / "component.md"
        holds = [x for x in RECORD_DIRS if (d / x).is_dir()] or \
                ([(d / "components")] if (d / "components").is_dir() else [])
        if not rec.is_file():
            # Rule 8: a directory carrying records or nested components must
            # say what component they belong to. Without it, the owning
            # component of those records is underivable — and the owner is
            # derived from the path, never stored, so there is nowhere else
            # to look.
            if holds:
                err(d, "directory under components/ holds records or nested "
                       "components but has no component.md (SPEC §5.8)",
                    "E-COMPONENT-MISSING")
            continue
        fm = frontmatter(rec)
        if fm is None or isinstance(fm, str):
            err(rec, fm or "missing frontmatter (--- fences)", "E-FRONTMATTER")
            continue
        need(fm, rec, "title", str)
        status = need(fm, rec, "status", str,
                      {"planned", "active", "deprecated", "retired"})
        if not is_date(fm.get("created")):
            err(rec, "`created` must be a date", "E-DATE", "created")
        globs = fm.get("code_globs") or []
        if status == "active" and not globs:
            warn(rec, "active component declares no code_globs (SPEC §4.10)",
                 "W-COMPONENT-NOGLOBS", "code_globs")
        if isinstance(globs, list):
            owned_globs.setdefault(d.parent, []).extend(
                (rec, str(g)) for g in globs)
        # Records owned by this component get exactly the root's checks.
        check_record_dirs(d, root)

    # Overlapping ownership among siblings makes "who owns this file"
    # unanswerable, which is the question the tree exists to answer.
    for _parent, entries in owned_globs.items():
        seen: dict[str, Path] = {}
        for rec, g in entries:
            if g in seen and seen[g] != rec:
                warn(rec, f"code_globs entry {g!r} is also claimed by "
                          f"{seen[g]} (SPEC §4.10)",
                     "W-COMPONENT-GLOBOVERLAP", "code_globs", g)
            seen.setdefault(g, rec)


REL = re.compile(r"^[a-z][a-z0-9_-]*$")
ADDR = re.compile(r"^@?[A-Za-z0-9][A-Za-z0-9._/-]*$")


def record_paths(root: Path) -> set[str]:
    """Every record's identity — its path from the capsule root, no `.md`
    (SPEC §2.2). This is the set an internal link must land in."""
    out = set()
    for f in root.rglob("*.md"):
        out.add(f.relative_to(root).as_posix()[:-3])
    return out


def check_links(root: Path) -> None:
    """`links` integrity — SPEC §5.6-7, core §Addresses / §Links.

    Internal targets must resolve; external (`@capsule/path`) ones must not
    be resolved here at all. A capsule is self-contained (SPEC §1.3), so it
    has to stay valid with no other capsule attached — an external link is
    enrichment, and checking it here would make a project capsule's validity
    depend on what happens to be checked out beside it.
    """
    known = record_paths(root)
    for f in sorted(root.rglob("*.md")):
        fm = frontmatter(f)
        if not isinstance(fm, dict):
            continue
        links = fm.get("links")
        if links is None:
            continue
        if not isinstance(links, list):
            err(f, "`links` must be a list", "E-LINK-TYPE", "links")
            continue
        for i, ln in enumerate(links):
            field = f"links[{i}]"
            if not isinstance(ln, dict):
                err(f, "each link must be a mapping with `rel` and `to`",
                    "E-LINK-TYPE", field)
                continue
            rel, to = ln.get("rel"), ln.get("to")
            if not isinstance(rel, str) or not REL.match(rel):
                err(f, f"link `rel` {rel!r} is not a lowercase token",
                    "E-LINK-REL", f"{field}.rel", str(rel))
            if not isinstance(to, str) or not ADDR.match(to):
                err(f, f"link `to` {to!r} is not a valid address",
                    "E-LINK-ADDR", f"{field}.to", str(to))
                continue
            if to.startswith("@"):
                continue                      # external — deliberately unchecked
            if to.removesuffix(".md") not in known:
                err(f, f"internal link target {to!r} does not resolve",
                    "E-LINK-DANGLING", f"{field}.to", to)


def validate(root: Path, *, fmt: str = "text") -> int:
    findings.clear()  # a fresh run, not accumulation across repeat calls
    man_path = root / "capsule.yaml"
    if not man_path.exists():
        msg = f"not a capsule: {man_path} missing"
        if fmt == "json":
            print(json.dumps({"conforming": False, "error": msg, "findings": []}))
        else:
            print(msg)
        return 2
    man = frontmatter_free_yaml(man_path)
    if isinstance(man, str):
        err(man_path, man)
        man = {}
    ver = need(man, man_path, "capsa_version", str)
    if ver and not re.fullmatch(r"\d+\.\d+\.\d+", ver):
        err(man_path, f"capsa_version {ver!r} is not MAJOR.MINOR.PATCH",
            "E-MANIFEST-VERSION", "capsa_version", str(ver))
    proj = man.get("project")
    if not isinstance(proj, dict):
        err(man_path, "missing `project` mapping", "E-MANIFEST-PROJECT", "project")
    else:
        need(proj, man_path, "name", str)
        slug = need(proj, man_path, "slug", str)
        if slug and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            err(man_path, f"slug {slug!r} is not kebab-case",
                "E-MANIFEST-SLUG", "project.slug", str(slug))
    need(man, man_path, "status", str,
         {"planning", "active", "maintained", "paused", "archived"})

    check_record_dirs(root)
    check_components(root)
    check_links(root)


    # A warning does not make a capsule non-conforming: the spec says SHOULD,
    # and reporting a SHOULD as a failure would make the checker disagree with
    # the document it checks.
    errors = [f for f in findings if f["severity"] == "error"]
    conforming = not errors
    if fmt == "json":
        print(json.dumps({"conforming": conforming, "findings": findings},
                         ensure_ascii=False))
    elif conforming and not findings:
        print("conforming capsule ✔")
    else:
        head = ("conforming capsule ✔ — with"
                if conforming else f"NON-CONFORMING — {len(errors)} error(s),")
        print(f"{head} {len(findings) - len(errors)} warning(s):")
        for f in findings:
            mark = "!" if f["severity"] == "error" else "?"
            print(f"  {mark} [{f['code']}] {f['path']}: {f['message']}")
    return 0 if conforming else 1


def frontmatter_free_yaml(path: Path):
    """capsule.yaml is bare YAML (no --- fences)."""
    try:
        data = load_yaml(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"YAML error: {exc}"
    return data if isinstance(data, dict) else {}


if __name__ == "__main__":
    args = sys.argv[1:]
    fmt = "json" if "--json" in args else "text"
    args = [a for a in args if a != "--json"]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    sys.exit(validate(Path(args[0]), fmt=fmt))

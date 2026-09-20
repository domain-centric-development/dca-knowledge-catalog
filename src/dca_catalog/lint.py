"""Semantic lint for a built bundle — mechanical checks only, no LLM.

Catches the health problems a generated+authored knowledge graph drifts into:
broken cross-links, stale source pointers, and authored nodes that are not wired
into the graph. Deterministic; sorted output. Exit 1 on any ERROR (broken links,
stale resources), 0 otherwise — pass ``--strict`` to fail on warnings too.

    python -m dca_catalog.lint            # lint the repo bundle
    python -m dca_catalog.lint --strict   # warnings fail the build too
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from .generate import _GENERATED_DIRS, _EXTENSIBLE_ZONE, _parse_front, _repo_root_default
from .okf import RESERVED

_EXTENSIBLE_DIRS = tuple(name for name, _t, _b in _EXTENSIBLE_ZONE)
_ALL_PREFIXES = tuple(f"/{d}/" for d in _GENERATED_DIRS + _EXTENSIBLE_DIRS)
_GENERATED_PREFIXES = tuple(f"/{d}/" for d in _GENERATED_DIRS)
_LINK_RE = re.compile(r"\]\((/[^)]+)\)")

# Controlled tag vocabulary for authored (extensible-zone) nodes — keep in sync
# with SPEC.md "Tag taxonomy". Generated-zone tags are consistent by
# construction; authored nodes get a WARN on tags outside this list so the
# vocabulary doesn't drift one synonym at a time.
_TAG_VOCABULARY = frozenset({
    # node kind (mirrors the directory)
    "recipe", "decision", "pitfall", "template", "note",
    # architecture style / category
    "tactical", "strategic", "hexagonal", "layered", "onion", "governance",
    "port-in", "port-out",
    # layer
    "domain", "application", "adapter", "infrastructure",
    # building blocks & concepts
    "aggregate", "entity", "value-object", "use-case", "repository",
    "domain-event", "integration-event", "events", "outbox", "specification",
    "factory", "domain-service", "gateway", "port", "dto",
    "bounded-context", "shared-kernel", "subdomain", "context-map",
    "anti-corruption-layer", "package-structure", "feature", "naming", "testing",
    "archunit", "archunitnet", "reference", "spring", "modulith", "rest", "persistence", "bootstrap",
    "cqrs", "event-sourcing", "security", "performance", "migration",
    "error-handling",
})

# (severity, kind, path, detail)
Finding = tuple


def _concept_files(bundle: Path) -> list[Path]:
    return sorted(p for p in bundle.rglob("*.md") if p.name not in RESERVED)


def _links(text: str) -> list[str]:
    """Bundle-relative link targets that point into the catalog graph."""
    return [t for t in _LINK_RE.findall(text) if t.startswith(_ALL_PREFIXES)]


def lint(bundle: Path, repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    files = _concept_files(bundle)
    registry = bundle / "redirects.json"
    redirects = json.loads(registry.read_text()) if registry.exists() else {}
    inbound: dict[str, int] = {}

    parsed: dict[Path, tuple[dict, str, list[str]]] = {}
    for p in files:
        text = p.read_text(encoding="utf-8")
        try:
            fm, body = _parse_front(text)
        except ValueError as exc:
            findings.append(("ERROR", "frontmatter", p.relative_to(bundle).as_posix(), str(exc)))
            fm, body = {}, text
        targets = _links(text)
        parsed[p] = (fm, body, targets)
        rel = p.relative_to(bundle).as_posix()
        for t in targets:
            if t.lstrip("/") != rel:  # self-links don't count as inbound
                inbound[t.lstrip("/")] = inbound.get(t.lstrip("/"), 0) + 1

    # Template concept nodes and their language children: the prose is written once in the
    # concept node, the code once per language below it. Collected first so both directions
    # (child without parent, parent whose applies_to does not match its children) can be checked.
    template_children: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        rel = p.relative_to(bundle).as_posix()
        parts = rel.split("/")
        if parts[0] == "template" and len(parts) == 3:
            template_children[f"template/{parts[1]}.md"].append(p)

    for p in files:
        fm, body, targets = parsed[p]
        rel = p.relative_to(bundle).as_posix()
        top = rel.split("/", 1)[0]
        parts = rel.split("/")
        is_template_child = parts[0] == "template" and len(parts) == 3

        # 1. broken links (every zone)
        for t in targets:
            target, _, anchor = t.lstrip("/").partition("#")
            if target in redirects:
                findings.append(("ERROR", "legacy-rule-link", rel, t))
            if not (bundle / target).exists():
                findings.append(("ERROR", "broken-link", rel, t))

        # 1b. rule mechanics — every Rule node names what it selects and what it checks
        if fm.get("type") == "Rule":
            if fm.get("status") not in {"enforced", "informational", "retired"}:
                findings.append(("ERROR", "rule-status", rel, str(fm.get("status"))))
            for field in (() if fm.get("status") == "retired" else ("selects", "checks")):
                if not str(fm.get(field) or "").strip():
                    findings.append(("ERROR", "undescribed-rule", rel, f"missing '{field}' frontmatter"))

        # 2. stale resource — generated node's source file vanished
        for key in ("resource", "resource_dotnet"):
            resource = fm.get(key)
            if resource and not (repo_root / resource).exists():
                findings.append(("ERROR", "stale-resource", rel, resource))

        # 3 & 4. authored-node health (extensible zone)
        if top in _EXTENSIBLE_DIRS:
            review = fm.get("review")
            if not review or not fm.get("owner") or not fm.get("evidence"):
                findings.append(("WARN", "editorial-metadata", rel, "authored node needs review, owner and evidence; missing review is non-normative"))
            if review and review not in {"draft", "reviewed", "superseded"}:
                findings.append(("ERROR", "editorial-review", rel, str(review)))
            if review == "superseded" and not fm.get("superseded_by"):
                findings.append(("ERROR", "editorial-superseded", rel, "superseded requires superseded_by"))
            for evidence in fm.get("evidence", []):
                target = str(evidence).lstrip("/").split("#", 1)[0]
                if str(evidence).startswith("/") and not (bundle / target).exists():
                    findings.append(("ERROR", "editorial-evidence", rel, str(evidence)))
            successor = fm.get("superseded_by")
            if successor and not (bundle / str(successor).lstrip("/").split("#", 1)[0]).exists():
                findings.append(("ERROR", "editorial-successor", rel, str(successor)))
            if not is_template_child and not any(t.startswith(_GENERATED_PREFIXES) for t in targets):
                findings.append(
                    ("WARN", "unanchored-authored", rel, "no link into the generated skeleton")
                )
            if not is_template_child and inbound.get(rel, 0) == 0:
                findings.append(
                    ("INFO", "orphan", rel, "no inbound links from other nodes")
                )
            # 4b. template language children — one concept node, one code node per language
            if is_template_child:
                parent = str(fm.get("parent") or "").lstrip("/")
                if not parent:
                    findings.append((
                        "ERROR", "template-child-parent", rel,
                        "a language node under template/<concept>/ needs `parent:` naming its concept node",
                    ))
                elif not (bundle / parent).exists():
                    findings.append(("ERROR", "template-child-parent", rel, f"parent {parent} does not exist"))
                elif parent != f"template/{parts[1]}.md":
                    findings.append((
                        "ERROR", "template-child-parent", rel,
                        f"parent is {parent}, expected template/{parts[1]}.md",
                    ))
            if rel in template_children:
                if "```" in body:
                    findings.append((
                        "ERROR", "template-parent-code", rel,
                        "a concept node with language children carries no code fence — the code "
                        "belongs in the child, so a further language stays one more file",
                    ))
                declared = {str(x) for x in (fm.get("applies_to") or [])}
                provided = set()
                for child in template_children[rel]:
                    child_fm, _, _ = parsed[child]
                    provided.update(str(x) for x in (child_fm.get("applies_to") or []))
                if declared != provided:
                    findings.append((
                        "ERROR", "template-applies-to", rel,
                        f"applies_to {sorted(declared)} but its language children provide "
                        f"{sorted(provided)}",
                    ))

            # 5. tag vocabulary drift (see SPEC.md "Tag taxonomy")
            tags = fm.get("tags") or []
            if isinstance(tags, str):
                tags = [tags]
            for tag in tags:
                if tag not in _TAG_VOCABULARY:
                    findings.append(
                        ("WARN", "unknown-tag", rel,
                         f"'{tag}' not in the SPEC.md tag taxonomy (add it there + lint.py, or use a listed tag)")
                    )

    return sorted(findings, key=lambda f: (f[1], f[2], f[3]))



def cited_drafts(bundle: Path, run_dir: Path) -> list[Finding]:
    """Which nodes a delivery run leaned on that are still proposals.

    A `review: draft` node is explicitly non-normative, so a stage that decided a design question
    from one decided it from a proposal — and says so in its file. Reviewing the whole authored zone
    on stock is the wrong order; what a run actually cites is the list worth reading. Point this at a
    project's run artefacts (`tasks/`) and it names exactly those.
    """
    findings: list[Finding] = []
    cited: dict[str, set[str]] = {}
    for path in sorted(run_dir.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for target in _LINK_RE.findall(text) + re.findall(r"[`(](/[\w./-]+\.md)", text):
            rel = target.lstrip("/").split("#", 1)[0]
            if rel.split("/", 1)[0] in _EXTENSIBLE_DIRS and (bundle / rel).exists():
                cited.setdefault(rel, set()).add(path.name)
    for rel, files in sorted(cited.items()):
        fm, _ = _parse_front((bundle / rel).read_text(encoding="utf-8"))
        review = str(fm.get("review") or "").strip()
        if review != "reviewed":
            findings.append((
                "WARN", "cited-draft", rel,
                f"leaned on by {', '.join(sorted(files))} but review is "
                f"{review or 'missing'} — a proposal decided a design question",
            ))
    return findings

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint a built DCA OKF bundle.")
    parser.add_argument("--bundle", type=Path, default=None, help="bundle dir (default: <catalog>/bundle)")
    parser.add_argument("--repo-root", type=Path, default=_repo_root_default())
    parser.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    parser.add_argument(
        "--cited-by",
        type=Path,
        default=None,
        help="a delivery run's artefact dir (e.g. a project's tasks/): report the nodes it cites "
             "that are still review: draft, so reviewing follows use instead of stock",
    )
    args = parser.parse_args(argv)
    bundle = (args.bundle or (Path(__file__).resolve().parents[2] / "bundle")).resolve()
    if not bundle.exists():
        print(f"No bundle at {bundle} — run `python -m dca_catalog.generate` first.")
        return 2

    findings = lint(bundle, args.repo_root.resolve())
    if args.cited_by:
        run_dir = args.cited_by.resolve()
        if not run_dir.exists():
            print(f"No run artefacts at {run_dir}.")
            return 2
        findings = findings + cited_drafts(bundle, run_dir)
    if not findings:
        print(f"lint: clean ({sum(1 for _ in _concept_files(bundle))} nodes)")
        return 0

    counts: dict[str, int] = {}
    for severity, kind, rel, detail in findings:
        counts[severity] = counts.get(severity, 0) + 1
        print(f"  {severity:5} {kind:20} {rel}  →  {detail}")
    print(f"lint: {', '.join(f'{n} {s}' for s, n in sorted(counts.items()))}")

    fail = any(s == "ERROR" for s, *_ in findings)
    if args.strict:
        fail = fail or any(s == "WARN" for s, *_ in findings)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())

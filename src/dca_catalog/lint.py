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
import re
import sys
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
    inbound: dict[str, int] = {}

    parsed: dict[Path, tuple[dict, str, list[str]]] = {}
    for p in files:
        text = p.read_text(encoding="utf-8")
        fm, body = _parse_front(text)
        targets = _links(text)
        parsed[p] = (fm, body, targets)
        rel = p.relative_to(bundle).as_posix()
        for t in targets:
            if t.lstrip("/") != rel:  # self-links don't count as inbound
                inbound[t.lstrip("/")] = inbound.get(t.lstrip("/"), 0) + 1

    for p in files:
        fm, body, targets = parsed[p]
        rel = p.relative_to(bundle).as_posix()
        top = rel.split("/", 1)[0]

        # 1. broken links (every zone)
        for t in targets:
            if not (bundle / t.lstrip("/")).exists():
                findings.append(("ERROR", "broken-link", rel, t))

        # 1b. rule mechanics — every Rule node names what it selects and what it checks
        if fm.get("type") == "Rule":
            for field in ("selects", "checks"):
                if not str(fm.get(field) or "").strip():
                    findings.append(("ERROR", "undescribed-rule", rel, f"missing '{field}' frontmatter"))

        # 2. stale resource — generated node's source file vanished
        for key in ("resource", "resource_dotnet"):
            resource = fm.get(key)
            if resource and not (repo_root / resource).exists():
                findings.append(("ERROR", "stale-resource", rel, resource))

        # 3 & 4. authored-node health (extensible zone)
        if top in _EXTENSIBLE_DIRS:
            if not any(t.startswith(_GENERATED_PREFIXES) for t in targets):
                findings.append(
                    ("WARN", "unanchored-authored", rel, "no link into the generated skeleton")
                )
            if inbound.get(rel, 0) == 0:
                findings.append(
                    ("INFO", "orphan", rel, "no inbound links from other nodes")
                )
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint a built DCA OKF bundle.")
    parser.add_argument("--bundle", type=Path, default=None, help="bundle dir (default: <catalog>/bundle)")
    parser.add_argument("--repo-root", type=Path, default=_repo_root_default())
    parser.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    args = parser.parse_args(argv)
    bundle = (args.bundle or (Path(__file__).resolve().parents[2] / "bundle")).resolve()
    if not bundle.exists():
        print(f"No bundle at {bundle} — run `python -m dca_catalog.generate` first.")
        return 2

    findings = lint(bundle, args.repo_root.resolve())
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

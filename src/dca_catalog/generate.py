"""Generate the OKF bundle from the DCA reference implementation.

Usage:  python -m dca_catalog.generate [--repo-root PATH] [--out PATH]
                                       [--mirror PATH ...] [--no-default-mirror]

Deterministic: same sources -> byte-identical bundle (no timestamps).

After writing the canonical bundle (--out), the freshly built tree is mirrored
to each --mirror dir and, unless --no-default-mirror is given, to the dca-core
plugin so /dca-knowledge ships a vendored copy that never drifts from source.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from . import adrs, docs, linker, markers, rules
from .okf import Node, RESERVED

# Generated zone — derived from the sources, wiped and rebuilt on every run.
_GENERATED_DIRS = ("book", "guide", "marker", "rule", "adr", "process")

# Extensible zone — authored (by a human or an LLM), survives regeneration.
# Each entry: (dir, OKF node type, blurb). Node *files* are authored; their
# index.md is still generated (a content catalog scanned from disk).
_EXTENSIBLE_ZONE = (
    ("recipe", "Recipe", "Task playbooks — ordered steps to build a DCA construct."),
    ("decision", "Decision", "Decision guides for design forks (which pattern, when)."),
    ("pitfall", "Pitfall", "Anti-patterns and the rules/ADRs that forbid them."),
    ("template", "Template", "Domain-free code skeletons to fill in."),
    ("note", "Note", "Compounded query answers — synthesis made permanent."),
)

# Human-readable blurb per top-level category, shown in the root index.
_CATEGORY_BLURB = {
    "book": "The comprehensive DCA guide — chapters and appendices (full text).",
    "guide": "The compact implementation guide — patterns, governance, supplementary guides (full text).",
    "marker": "Architectural marker interfaces — the contracts a new application implements.",
    "rule": "ArchUnit rules — the enforceable, machine-checkable architecture.",
    "adr": "Architecture Decision Records — the patterns used and why.",
    "process": "How-to processes for keeping the architecture's conventions.",
    **{name: blurb for name, _type, blurb in _EXTENSIBLE_ZONE},
}

# Short authoring hint appended to each extensible-zone index.md.
_ZONE_HINT = {
    name: (
        f"**Extensible zone — authored, not generated from sources.** "
        f"`{name}/` nodes are written by a human or an LLM and **survive** `generate` "
        f"(only this `index.md` is regenerated). Add one as `{name}/<slug>.md` with "
        f"frontmatter `type: {ntype}`, `title:`, `tags: [{name}]`, then link into the "
        f"skeleton with bundle-relative links (e.g. `[UseCase](/marker/port-in/usecase.md)`)."
    )
    for name, ntype, _blurb in _EXTENSIBLE_ZONE
}


def _repo_root_default() -> Path:
    # src/dca_catalog/generate.py -> dca_catalog -> src -> dca-knowledge-catalog -> repo root
    return Path(__file__).resolve().parents[3]


# vendored copy shipped with the dca-core plugin so /dca-knowledge has a catalog
# even when the plugin is installed in another project.
_DEFAULT_MIRROR_REL = "dca-marketplace/plugins/dca-core/skills/dca-knowledge/catalog"


# Link-section headings emitted by the generator at the end of a node body —
# preserved verbatim during redaction so the graph edges keep resolving.
_LINK_HEADINGS = ("## Sections", "## Related markers", "## Related ADRs")

_REDACT_NOTICE = (
    "> **Full text not included in this public bundle.** This node keeps its metadata and\n"
    "> graph links; the verbatim text lives in the non-public source (see `resource:`). Use\n"
    "> an in-repo or privately vendored full catalog for deep quotes."
)


def _redact_node(text: str) -> str:
    """Strip a node's verbatim body, keeping frontmatter, a one-line description
    (already public via the directory index) and the trailing link sections."""
    if not text.startswith("---"):
        return text
    head_end = text.find("\n---\n", 3)
    if head_end == -1:
        return text
    front, body = text[: head_end + 5], text[head_end + 5 :]

    # keep everything from the first link-section heading on
    link_idx = len(body)
    for heading in _LINK_HEADINGS:
        idx = body.find(f"\n{heading}\n")
        if idx != -1:
            link_idx = min(link_idx, idx)
    links = body[link_idx:].rstrip("\n")

    prose = body[:link_idx]
    description = next(
        (ln.strip() for ln in prose.splitlines()
         if ln.strip() and not ln.lstrip().startswith(("#", ">", "|", "`", "-", "*", "!"))),
        "",
    )
    parts = [front.rstrip("\n"), ""]
    if description:
        parts += [description, ""]
    parts.append(_REDACT_NOTICE)
    if links:
        parts += ["", links.lstrip("\n")]
    return "\n".join(parts).rstrip("\n") + "\n"


def _mirror(out: Path, dests: list[Path], redact_dirs: tuple[str, ...] = ()) -> None:
    """Replace each dest with a fresh copy of the canonical bundle at ``out``.

    Nodes under ``redact_dirs`` (top-level bundle dirs) are copied with their
    verbatim bodies stripped (frontmatter, description and link sections stay),
    so mirrors meant for publication don't ship non-public full text. Reserved
    files (``index.md``/``log.md``) are navigation and stay as-is.
    """
    for dest in dests:
        dest = dest.resolve()
        if dest == out:
            continue
        if dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(out, dest)
        for d in redact_dirs:
            directory = dest / d
            if not directory.exists():
                continue
            for path in sorted(directory.rglob("*.md")):
                if path.name in RESERVED:
                    continue
                path.write_text(_redact_node(path.read_text(encoding="utf-8")), encoding="utf-8")


def _parse_front(text: str) -> tuple[dict, str]:
    """Minimal frontmatter reader for authored extensible-zone nodes."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    head, body = text[3:end].strip("\n"), text[end + 4:].lstrip("\n")
    fm: dict = {}
    for line in head.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                fm[key.strip()] = [
                    v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()
                ]
            else:
                fm[key.strip()] = value.strip('"')
    return fm, body


def _load_authored(out: Path) -> list[Node]:
    """Read authored nodes from the extensible zone so they flow into counts and
    indexes uniformly. Their files are never rewritten — only catalogued."""
    nodes: list[Node] = []
    for name, _type, _blurb in _EXTENSIBLE_ZONE:
        directory = out / name
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name in RESERVED:
                continue
            fm, body = _parse_front(path.read_text(encoding="utf-8"))
            if not fm.get("type"):
                continue  # not an OKF node — skip
            nodes.append(
                Node(
                    path=path.relative_to(out).as_posix(),
                    frontmatter=fm,
                    body=body,
                    meta={"authored": True},
                )
            )
    return nodes


def _scaffold_extensible(out: Path) -> None:
    """Ensure the extensible-zone directories exist (empty is fine)."""
    for name, _type, _blurb in _EXTENSIBLE_ZONE:
        (out / name).mkdir(parents=True, exist_ok=True)


def _description(node: Node) -> str:
    fm = node.frontmatter
    if fm["type"] == "Marker":
        text = node.body.strip()
    elif fm["type"] == "Rule":
        text = str(fm.get("rule", ""))
    elif fm["type"] == "ADR":
        text = str(fm.get("pattern", ""))
    else:
        # Chapter / Guide / Section / Process: first meaningful body line
        text = next(
            (ln for ln in node.body.splitlines() if ln.strip() and not ln.lstrip().startswith(("#", ">", "|", "`", "-", "*"))),
            str(fm["title"]),
        )
    text = " ".join(text.split())
    return (text[:117] + "...") if len(text) > 120 else text


def _build_indexes(nodes: list[Node], extra_dirs: tuple[str, ...] = ()) -> dict[str, str]:
    """Build an index.md for every directory (progressive disclosure).

    ``extra_dirs`` are top-level directories that must appear even when empty
    (the extensible-zone dirs, so the zone is discoverable before it has nodes).
    """
    node_by_path = {n.path: n for n in nodes}
    children_dirs: dict[str, set[str]] = defaultdict(set)
    children_files: dict[str, list[str]] = defaultdict(list)

    all_dirs: set[str] = {""}
    for n in nodes:
        parts = n.path.split("/")
        for i in range(len(parts) - 1):
            d = "/".join(parts[:i + 1])
            all_dirs.add(d)
            parent = "/".join(parts[:i]) if i > 0 else ""
            children_dirs[parent].add(d)
        parent = "/".join(parts[:-1])
        children_files[parent].append(n.path)

    for d in extra_dirs:
        all_dirs.add(d)
        children_dirs[""].add(d)

    indexes: dict[str, str] = {}
    for d in sorted(all_dirs):
        title = "DCA Knowledge Catalog" if d == "" else d.rsplit("/", 1)[-1]
        lines = [f"# {title}", ""]
        if d == "":
            lines.append(
                "Knowledge for building Domain-Centric Architecture applications. "
                "**Generated zone** (book, guide, marker, rule, adr, process) is derived "
                "from the sources and rebuilt on every run; the book and guide (full text) "
                "are the main body, the marker contracts, ArchUnit rules and ADRs the "
                "skeleton they anchor to. **Extensible zone** (recipe, decision, pitfall, "
                "template, note) is authored by a human or an LLM and survives "
                "regeneration. See `log.md`."
            )
            lines.append("")
            router = "recipe/build-a-dca-application.md"
            if router in node_by_path:
                lines.append(
                    f"**Building something?** Start at "
                    f"[{node_by_path[router].frontmatter['title']}]({router}) — "
                    "the task router mapping construction tasks to recipes."
                )
                lines.append("")
        for sub in sorted(children_dirs.get(d, [])):
            name = sub.rsplit("/", 1)[-1]
            blurb = _CATEGORY_BLURB.get(sub, "")
            rel = name + "/index.md"
            count = sum(1 for p in node_by_path if p.startswith(sub + "/"))
            suffix = f" — {blurb}" if blurb else ""
            lines.append(f"- [{name}/]({rel}) ({count}){suffix}")
        if children_dirs.get(d) and children_files.get(d):
            lines.append("")
        for path in sorted(children_files.get(d, [])):
            node = node_by_path[path]
            rel = path.rsplit("/", 1)[-1]
            lines.append(f"- [{node.frontmatter['title']}]({rel}) — {_description(node)}")
        if d in _ZONE_HINT:
            if not children_files.get(d) and not children_dirs.get(d):
                lines.append("_No nodes yet._")
            lines.append("")
            lines.append(_ZONE_HINT[d])
        indexes[(d + "/" if d else "") + "index.md"] = "\n".join(lines).rstrip() + "\n"
    return indexes


def _log_md(counts: dict[str, int]) -> str:
    extensible = sum(counts.get(t, 0) for _n, t, _b in _EXTENSIBLE_ZONE)
    lines = [
        "# Changelog",
        "",
        "## v0.1",
        "",
        "Generated bundle: the DCA book and implementation guide (full text, as "
        "Chapter/Guide containers + Section nodes), anchored to the reference "
        "implementation's marker interfaces, ArchUnit rules and ADRs.",
        "",
        "### Generated zone (rebuilt from sources)",
        f"- Chapters (book): {counts.get('Chapter', 0)}",
        f"- Guides: {counts.get('Guide', 0)}",
        f"- Sections: {counts.get('Section', 0)}",
        f"- Markers: {counts.get('Marker', 0)}",
        f"- Rules: {counts.get('Rule', 0)}",
        f"- ADRs: {counts.get('ADR', 0)}",
        f"- Process: {counts.get('Process', 0)}",
        "",
        "### Extensible zone (authored, preserved across regeneration)",
    ]
    for _name, ntype, _blurb in _EXTENSIBLE_ZONE:
        lines.append(f"- {ntype}: {counts.get(ntype, 0)}")
    lines.append(f"- Total authored: {extensible}")
    return "\n".join(lines) + "\n"


def generate(repo_root: Path, out: Path) -> dict[str, int]:
    marker_nodes = markers.extract(repo_root)
    rule_nodes = rules.extract(repo_root)
    adr_nodes = adrs.extract(repo_root)
    doc_nodes = docs.extract(repo_root)
    linker.link(marker_nodes, rule_nodes, adr_nodes)
    linker.link_docs(doc_nodes, marker_nodes, rule_nodes, adr_nodes)

    nodes = marker_nodes + rule_nodes + adr_nodes + doc_nodes

    paths = [n.path for n in nodes]
    if len(set(paths)) != len(paths):
        dupes = sorted({p for p in paths if paths.count(p) > 1})
        raise SystemExit(f"Duplicate node paths (slug collision): {dupes}")

    # Zone-aware wipe: rebuild the generated zone, PRESERVE authored node files in
    # the extensible zone (only their index.md is regenerated).
    out.mkdir(parents=True, exist_ok=True)
    for d in _GENERATED_DIRS:
        if (out / d).exists():
            shutil.rmtree(out / d)
    for name, _type, _blurb in _EXTENSIBLE_ZONE:
        if (out / name / "index.md").exists():
            (out / name / "index.md").unlink()
    for reserved in RESERVED:
        if (out / reserved).exists():
            (out / reserved).unlink()
    _scaffold_extensible(out)

    for node in nodes:
        target = out / node.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(node.render(), encoding="utf-8")

    # Authored nodes are catalogued (counts + indexes) but never rewritten.
    authored = _load_authored(out)
    index_nodes = nodes + authored

    counts: dict[str, int] = defaultdict(int)
    for n in index_nodes:
        counts[n.frontmatter["type"]] += 1

    extra_dirs = tuple(name for name, _type, _blurb in _EXTENSIBLE_ZONE)
    for rel, content in _build_indexes(index_nodes, extra_dirs).items():
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        (out / rel).write_text(content, encoding="utf-8")
    (out / "log.md").write_text(_log_md(counts), encoding="utf-8")

    assert "index.md" in RESERVED and "log.md" in RESERVED  # spec invariants
    return dict(counts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the DCA OKF bundle.")
    parser.add_argument("--repo-root", type=Path, default=_repo_root_default())
    parser.add_argument(
        "--out", type=Path, default=None, help="bundle output dir (default: <catalog>/bundle)"
    )
    parser.add_argument(
        "--mirror", type=Path, action="append", default=[],
        help="extra dir to mirror the built bundle into (repeatable)",
    )
    parser.add_argument(
        "--no-default-mirror", action="store_true",
        help="skip the vendored copy shipped with the dca-core plugin",
    )
    parser.add_argument(
        "--mirror-redact", action="append", default=None, metavar="DIR",
        help="top-level bundle dir whose node bodies are stripped in mirrors "
             "(repeatable; default: book — the book is not public). "
             "Pass --mirror-redact none to disable.",
    )
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    out = (args.out or (Path(__file__).resolve().parents[2] / "bundle")).resolve()
    counts = generate(repo_root, out)
    total = sum(counts.values())
    print(f"Generated {total} nodes -> {out}")
    for kind in ("Chapter", "Guide", "Section", "Marker", "Rule", "ADR", "Process"):
        print(f"  {kind}: {counts.get(kind, 0)}")

    mirrors = list(args.mirror)
    if not args.no_default_mirror:
        mirrors.append(repo_root / _DEFAULT_MIRROR_REL)
    mirrors = [m for m in mirrors if m.resolve() != out]
    redact = tuple(args.mirror_redact) if args.mirror_redact is not None else ("book",)
    if redact == ("none",):
        redact = ()
    if mirrors:
        _mirror(out, mirrors, redact_dirs=redact)
        for m in mirrors:
            suffix = f" (redacted: {', '.join(redact)})" if redact else ""
            print(f"Mirrored -> {m}{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

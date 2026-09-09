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
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from . import docs, linker, markers, process, reference, rules, retrieval
from .mirror import mirror_bundle as _mirror, strip_resource as _strip_resource  # noqa: F401 — re-exported for tests
from .okf import Node, RESERVED

# Generated zone — derived from the sources, wiped and rebuilt on every run.
_GENERATED_DIRS = ("guide", "marker", "rule", "process", "reference", "evidence")

# Extensible zone — authored (by a human or an LLM), survives regeneration.
# Each entry: (dir, OKF node type, blurb). Node *files* are authored; their
# index.md is still generated (a content catalog scanned from disk).
_EXTENSIBLE_ZONE = (
    ("recipe", "Recipe", "Task playbooks — ordered steps to build a DCA construct."),
    ("decision", "Decision", "Decision guides for design forks (which pattern, when)."),
    ("pitfall", "Pitfall", "Anti-patterns and the rules that forbid them."),
    ("template", "Template", "Domain-free code skeletons to fill in."),
    ("note", "Note", "Compounded query answers — synthesis made permanent."),
)

# Human-readable blurb per top-level category, shown in the root index.
_CATEGORY_BLURB = {
    "guide": "The compact implementation guide — patterns, governance, supplementary guides (full text).",
    "marker": "Architectural marker interfaces — the contracts a new application implements.",
    "rule": "ArchUnit rules — the enforceable, machine-checkable architecture.",
    "process": "How-to processes for keeping the architecture's conventions.",
    "reference": "The two classes every rule is parameterised by — DcaLayout (settings, defaults, patterns) and DcaArchitecture (how contexts and modules are discovered).",
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


def _parse_front(text: str) -> tuple[dict, str]:
    """Read the documented flat scalar/flow-list subset; never ignore YAML syntax."""
    if not text.startswith("---\n"):
        if text.startswith("---"):
            raise ValueError("invalid frontmatter delimiter")
        return {}, text
    end = text.find("\n---\n", 3)
    if end < 0:
        raise ValueError("unterminated frontmatter")

    def scalar(value: str) -> str:
        if value.startswith('"'):
            try:
                result = json.loads(value)
            except ValueError as exc:
                raise ValueError("invalid quoted scalar") from exc
            if not isinstance(result, str):
                raise ValueError("expected string scalar")
            return result
        if value.startswith("'"):
            if not re.fullmatch(r"'(?:[^']|'')*'", value):
                raise ValueError("invalid single-quoted scalar")
            return value[1:-1].replace("''", "'")
        if not value or value[0] in "-?:,[]{}#&*!|>%@`" or re.search(r":\s|\s#", value):
            raise ValueError("unsupported scalar syntax; quote the value")
        return value

    fm: dict = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)", line)
        if not match:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = match.groups()
        value = value.strip()
        if key in fm:
            raise ValueError(f"duplicate frontmatter key: {key}")
        if value.startswith("["):
            if not value.endswith("]"):
                raise ValueError("unterminated flow list")
            inner = value[1:-1].strip()
            items, position = [], 0
            token_re = re.compile(r'\s*("(?:[^"\\]|\\.)*"|\'(?:[^\']|\'\')*\'|[^,]+?)\s*(,|$)')
            while position < len(inner):
                token = token_re.match(inner, position)
                if not token:
                    raise ValueError("invalid flow list")
                items.append(scalar(token.group(1).strip()))
                position = token.end()
                if token.group(2) and position == len(inner):
                    raise ValueError("trailing list comma")
            fm[key] = items
        else:
            fm[key] = scalar(value)
    return fm, text[end + 5:].lstrip("\n")


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
    # Flatten links to their text: an index entry is a one-line blurb, and
    # truncating a line that still carries link markup can cut mid-target and
    # emit a mangled, dangling link.
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", " ".join(text.split()))
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
                "**Generated zone** (guide, marker, rule, process) is derived from the "
                "sources and rebuilt on every run; the implementation guide (full text) "
                "is the main body, the marker contracts and ArchUnit rules the skeleton "
                "it anchors to, and `reference/` describes the layout and discovery "
                "classes every rule is parameterised by. **Extensible zone** (recipe, decision, pitfall, template, "
                "note) is authored by a human or an LLM and survives regeneration. "
                "See `log.md`."
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
        "Generated bundle: the DCA implementation guide (full text, as Guide "
        "containers + Section nodes), anchored to the reference implementation's "
        "marker interfaces and ArchUnit rules.",
        "",
        "### Generated zone (rebuilt from sources)",
        f"- Guides: {counts.get('Guide', 0)}",
        f"- Sections: {counts.get('Section', 0)}",
        f"- Markers: {counts.get('Marker', 0)}",
        f"- Rules: {counts.get('Rule', 0)}",
        f"- Process: {counts.get('Process', 0)}",
        f"- Reference: {counts.get('Reference', 0)}",
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
    process_nodes = process.extract(repo_root)
    reference_nodes = reference.extract(repo_root)
    doc_nodes = docs.extract(repo_root)
    linker.link(marker_nodes, rule_nodes)
    linker.link_docs(doc_nodes, marker_nodes)
    linker.link_reference(rule_nodes, reference_nodes)

    nodes = marker_nodes + rule_nodes + process_nodes + reference_nodes + doc_nodes
    nodes += retrieval.evidence_slices(nodes)

    paths = [n.path for n in nodes]
    if len(set(paths)) != len(paths):
        dupes = sorted({p for p in paths if paths.count(p) > 1})
        raise SystemExit(f"Duplicate node paths (slug collision): {dupes}")

    # Seed missing extensible nodes from the canonical source graph so fresh outputs have its link closure.
    canonical_authored = repo_root / "dca-knowledge-catalog/bundle"
    if canonical_authored.resolve() != out.resolve():
        for zone, _, _ in _EXTENSIBLE_ZONE:
            for source in sorted((canonical_authored / zone).rglob("*.md")):
                if source.name in RESERVED:
                    continue
                target = out / source.relative_to(canonical_authored)
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, target)

    # Reviewed authored inputs override only explicitly owned nodes. Other extensible nodes survive.
    authored_source = repo_root / "dca-knowledge-catalog/authored"
    if authored_source.exists():
        for source in sorted(authored_source.rglob("*.md")):
            relative = source.relative_to(authored_source)
            if relative.parts[0] not in {name for name, _, _ in _EXTENSIBLE_ZONE} or source.name in RESERVED:
                raise ValueError(f"invalid authored source: {relative}")
            _parse_front(source.read_text(encoding="utf-8"))
            target = out / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    # Capture legacy identities before wiping generated files. Persist the mapping once;
    # later title changes must never manufacture new title-based identities.
    redirect_file = out / "redirects.json"
    redirects = json.loads(redirect_file.read_text()) if redirect_file.exists() else {}
    by_id = {n.frontmatter["id"]: n.path for n in rule_nodes if "id" in n.frontmatter}
    for node in rule_nodes:
        for rule_id in node.meta.get("retired_ids", []):
            by_id[rule_id] = f"rule/retired.md#{rule_id.lower()}"
            for old in list(redirects):
                if redirects[old].endswith(f"/{rule_id.lower()}.md"):
                    redirects[old] = by_id[rule_id]
    for old in sorted((out / "rule").rglob("*.md")):
        fm, _ = _parse_front(old.read_text(encoding="utf-8"))
        target = by_id.get(fm.get("id"))
        previous = old.relative_to(out).as_posix()
        if target and previous != target:
            redirects.setdefault(previous, target)
    # Fresh builds use the checked-in migration registry, not current titles.
    canonical = repo_root / "dca-knowledge-catalog/bundle/redirects.json"
    if canonical.exists() and canonical.resolve() != redirect_file.resolve():
        for old, target in json.loads(canonical.read_text()).items():
            redirects.setdefault(old, target)
    for old, target in list(redirects.items()):
        target_id = Path(target.split("#", 1)[0]).stem.upper()
        if target_id in by_id:
            redirects[old] = by_id[target_id]
    # Id paths of retired rules also migrate to their anchored registry entry.
    for node in rule_nodes:
        for rule_id in node.meta.get("retired_ids", []):
            for old in sorted((out / "rule").rglob(f"{rule_id.lower()}.md")):
                redirects[old.relative_to(out).as_posix()] = by_id[rule_id]
    for name, _, _ in _EXTENSIBLE_ZONE:
        for authored_path in sorted((out / name).rglob("*.md")):
            original = authored_path.read_text(encoding="utf-8")
            migrated = re.sub(
                r"(\]\()/([^ )#]+)(#[^ )]+)?(\))",
                lambda m: m[1] + "/" + redirects.get(m[2], m[2]) + (m[3] or "") + m[4],
                original,
            )
            if migrated != original:
                authored_path.write_text(migrated, encoding="utf-8")

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
    (out / "redirects.json").write_text(json.dumps(redirects, indent=2, sort_keys=True) + "\n", encoding="utf-8")

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

    (out / "rule/index-compact.md").write_text(retrieval.compact_index(index_nodes), encoding="utf-8")
    retrieval.write_manifest(repo_root, out, dict(counts))

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
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    out = (args.out or (Path(__file__).resolve().parents[2] / "bundle")).resolve()
    counts = generate(repo_root, out)
    total = sum(counts.values())
    print(f"Generated {total} nodes -> {out}")
    for kind in ("Guide", "Section", "Marker", "Rule", "Process", "Reference"):
        print(f"  {kind}: {counts.get(kind, 0)}")

    mirrors = list(args.mirror)
    if not args.no_default_mirror:
        mirrors.append(repo_root / _DEFAULT_MIRROR_REL)
    mirrors = [m for m in mirrors if m.resolve() != out]
    if mirrors:
        _mirror(out, mirrors)
        for m in mirrors:
            print(f"Mirrored -> {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

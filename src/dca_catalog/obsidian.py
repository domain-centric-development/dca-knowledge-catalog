"""Obsidian view of the bundle — a derived export plus a guarded import.

The canonical bundle uses OKF **bundle-relative** links (leading ``/``), which
LLMs/agents and the conformance tests rely on but Obsidian does not resolve as
internal links. The **export** copies the bundle and rewrites those links to
**file-relative** paths (``../marker/...``) that Obsidian (and GitHub, and plain
markdown viewers) resolve — so the graph view and backlinks work. It also adds
an ``aliases`` frontmatter line (the node title) for wikilink autocompletion and
vault settings that make Obsidian write markdown links, not wikilinks. A
previously opened vault's ``.obsidian`` state survives re-export.

The **import** closes the loop for the extensible zone only: authored nodes
(``recipe/ decision/ pitfall/ template/ note/``) edited in the vault are written
back to the canonical bundle with links rewritten to bundle-relative form and
wikilinks converted to markdown links. Edits to generated-zone files are
reported and ignored — those are derived from the sources. After an import, run
``generate`` (re-catalogues indexes) and ``lint`` (OKF health) — the import
itself never touches indexes.

    python -m dca_catalog.obsidian                        # export -> bundle-obsidian/
    python -m dca_catalog.obsidian --import               # vault -> bundle (extensible zone)
    python -m dca_catalog.obsidian --bundle B --out DIR   # explicit paths
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import shutil
import sys
from pathlib import Path

from .generate import _GENERATED_DIRS, _EXTENSIBLE_ZONE, _parse_front
from .okf import RESERVED

_EXTENSIBLE_DIRS = tuple(n for n, _t, _b in _EXTENSIBLE_ZONE)
_ZONE_DIRS = _GENERATED_DIRS + _EXTENSIBLE_DIRS
_PREFIXES = tuple(f"/{d}/" for d in _ZONE_DIRS)
# markdown link whose target is a bundle-relative path into the graph
_LINK_RE = re.compile(r"\]\((/[^)]+)\)")
# any markdown link target (import direction)
_ANY_LINK_RE = re.compile(r"\]\(([^)]+)\)")
# Obsidian wikilink: [[target]] or [[target|label]] (no embeds)
_WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)(#[^\]|]*)?(?:\|([^\]]+))?\]\]")
_TITLE_LINE_RE = re.compile(r"^title: (.+)$", re.MULTILINE)
_SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)

# graph-view color per node type directory (Obsidian graph.json colorGroups)
_GRAPH_COLORS = {
    "guide": 0x72B7B2,     # teal
    "marker": 0xF58518,    # orange
    "rule": 0xE45756,      # red
    "process": 0x9D755D,   # brown
    "reference": 0x4C78A8, # blue
    "recipe": 0x54A24B,    # green
    "decision": 0xEECA3B,  # yellow
    "pitfall": 0xFF9DA6,   # rose
    "template": 0x439894,  # dark teal
    "note": 0xBAB0AC,      # grey
}


# --------------------------------------------------------------------------- export

def _rewrite(text: str, from_rel: str) -> str:
    """Rewrite leading-slash graph links in one file to file-relative paths."""
    from_dir = posixpath.dirname(from_rel)

    def repl(m: re.Match) -> str:
        target = m.group(1)
        if not target.startswith(_PREFIXES):
            return m.group(0)  # leave non-graph absolute links (e.g. external prose)
        rel = posixpath.relpath(target.lstrip("/"), from_dir or ".")
        return f"]({rel})"

    return _LINK_RE.sub(repl, text)


def _alias_line(title_value: str) -> str:
    return f"aliases: [{title_value}]"


def _add_alias(text: str) -> str:
    """Insert ``aliases: [<title>]`` after the frontmatter title so wikilink /
    quick-switcher autocompletion finds nodes by title, not just slug."""
    if not text.startswith("---") or "\naliases:" in text.split("\n---", 1)[0]:
        return text
    head_end = text.find("\n---", 3)
    if head_end == -1:
        return text
    head = text[:head_end]
    m = _TITLE_LINE_RE.search(head)
    if not m:
        return text
    insert_at = m.end()
    return text[:insert_at] + "\n" + _alias_line(m.group(1)) + text[insert_at:]


def _merge_json(path: Path, updates: dict) -> None:
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            data = {}
    data.update(updates)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _vault_config(out: Path) -> None:
    """Vault settings: markdown links (never wikilinks) so authored edits stay
    OKF-importable; graph colors per node type. Merges into any existing state
    Obsidian wrote, so opening the vault does not get undone by re-export."""
    vault = out / ".obsidian"
    vault.mkdir(exist_ok=True)
    _merge_json(vault / "app.json", {
        "useMarkdownLinks": True,
        "newLinkFormat": "relative",
        "alwaysUpdateLinks": True,
    })
    graph = vault / "graph.json"
    data = {}
    if graph.exists():
        try:
            data = json.loads(graph.read_text(encoding="utf-8"))
        except ValueError:
            data = {}
    groups = data.get("colorGroups")
    if not groups:
        data["colorGroups"] = [
            {"query": f'path:"{d}"', "color": {"a": 1, "rgb": rgb}}
            for d, rgb in _GRAPH_COLORS.items()
        ]
        graph.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return
    # Existing groups are the user's to tune, so they are never overwritten — but a
    # group for a directory the bundle no longer has colors nothing, and a vault that
    # keeps listing it suggests the zone is still there.
    kept = [g for g in groups if not _names_missing_dir(g.get("query"), vault.parent)]
    if len(kept) != len(groups):
        data["colorGroups"] = kept
        graph.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _names_missing_dir(query: object, out: Path) -> bool:
    """True for a plain ``path:"<dir>"`` query whose directory is gone from the vault."""
    if not isinstance(query, str):
        return False
    m = re.fullmatch(r'path:"([^"/]+)"', query.strip())
    return bool(m) and not (out / m.group(1)).is_dir()


def export(bundle: Path, out: Path) -> int:
    """Write an Obsidian-compatible copy of ``bundle`` to ``out``. Returns file count.

    A pre-existing ``out/.obsidian`` (workspace state, plugins, appearance) is
    preserved; only our link-format and graph-color settings are (re)applied.
    """
    saved_obsidian = None
    if (out / ".obsidian").exists():
        saved_obsidian = out.parent / f".{out.name}-obsidian-keep"
        if saved_obsidian.exists():
            shutil.rmtree(saved_obsidian)
        shutil.move(str(out / ".obsidian"), str(saved_obsidian))
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(bundle, out)
    if saved_obsidian is not None:
        shutil.move(str(saved_obsidian), str(out / ".obsidian"))
    count = 0
    for path in sorted(out.rglob("*.md")):
        rel = path.relative_to(out).as_posix()
        text = path.read_text(encoding="utf-8")
        rewritten = _rewrite(text, rel)
        if path.name not in RESERVED:
            rewritten = _add_alias(rewritten)
        if rewritten != text:
            path.write_text(rewritten, encoding="utf-8")
        count += 1
    _vault_config(out)
    return count


# --------------------------------------------------------------------------- import

def _slug_map(vault: Path) -> dict[str, str]:
    """basename (no .md) -> vault-relative path; ambiguous basenames dropped."""
    seen: dict[str, str | None] = {}
    for p in vault.rglob("*.md"):
        if p.name in RESERVED or ".obsidian" in p.parts:
            continue
        rel = p.relative_to(vault).as_posix()
        stem = p.stem
        seen[stem] = None if stem in seen else rel
    return {k: v for k, v in seen.items() if v is not None}


def _to_bundle_links(text: str, from_rel: str, slugs: dict[str, str], problems: list[str]) -> str:
    """Rewrite one vault file's links to canonical OKF form: wikilinks ->
    markdown links, file-relative targets -> bundle-relative (leading ``/``)."""
    from_dir = posixpath.dirname(from_rel)

    def wiki(m: re.Match) -> str:
        target, anchor, label = m.group(1).strip(), m.group(2) or "", m.group(3)
        rel = None
        cand = target[:-3] if target.endswith(".md") else target
        if "/" in cand:  # path-style wikilink
            norm = posixpath.normpath(posixpath.join(from_dir, cand) if not cand.startswith("/") else cand.lstrip("/"))
            if (norm.split("/", 1)[0] in _ZONE_DIRS):
                rel = norm + ".md"
        if rel is None:
            rel = slugs.get(posixpath.basename(cand))
        if rel is None:
            problems.append(f"{from_rel}: unresolved wikilink [[{m.group(1)}]] (left as-is)")
            return m.group(0)
        text_label = label or posixpath.basename(cand)
        return f"[{text_label}](/{rel}{anchor})"

    def md(m: re.Match) -> str:
        target = m.group(1)
        if target.startswith("/") or _SCHEME_RE.match(target) or target.startswith("#"):
            return m.group(0)
        path_part, _, anchor = target.partition("#")
        if not path_part.endswith(".md"):
            return m.group(0)
        norm = posixpath.normpath(posixpath.join(from_dir, path_part))
        if norm.startswith("..") or norm.split("/", 1)[0] not in _ZONE_DIRS:
            return m.group(0)
        suffix = f"#{anchor}" if anchor else ""
        return f"](/{norm}{suffix})"

    return _ANY_LINK_RE.sub(md, _WIKILINK_RE.sub(wiki, text))


def _strip_injected_alias(text: str) -> str:
    """Remove the alias line the export injected (title-identical), so a
    no-edit roundtrip leaves the canonical bundle byte-identical."""
    head_end = text.find("\n---", 3)
    if not text.startswith("---") or head_end == -1:
        return text
    head = text[:head_end]
    m = _TITLE_LINE_RE.search(head)
    if not m:
        return text
    injected = "\n" + _alias_line(m.group(1))
    if head[m.end():m.end() + len(injected)] == injected:
        return text[:m.end()] + text[m.end() + len(injected):]
    return text


def import_back(vault: Path, bundle: Path) -> tuple[int, list[str]]:
    """Write extensible-zone edits from ``vault`` back into ``bundle``.

    Returns (files changed, problem messages). Generated-zone edits and vault
    deletions are reported, never applied. Frontmatter must carry a non-empty
    ``type`` — invalid nodes are rejected.
    """
    problems: list[str] = []
    changed = 0
    slugs = _slug_map(vault)

    for d in _EXTENSIBLE_DIRS:
        vdir = vault / d
        if not vdir.exists():
            continue
        for p in sorted(vdir.rglob("*.md")):
            if p.name in RESERVED:
                continue
            rel = p.relative_to(vault).as_posix()
            text = p.read_text(encoding="utf-8")
            canonical = _strip_injected_alias(
                _to_bundle_links(text, rel, slugs, problems)
            )
            fm, _body = _parse_front(canonical)
            if not fm.get("type"):
                problems.append(f"{rel}: REJECTED — frontmatter has no non-empty `type` (OKF requires it)")
                continue
            dest = bundle / rel
            if dest.exists() and dest.read_text(encoding="utf-8") == canonical:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(canonical, encoding="utf-8")
            changed += 1
            print(f"  imported {rel}")
        # deletions: present in bundle, gone from vault — report only
        bdir = bundle / d
        if bdir.exists():
            for p in sorted(bdir.rglob("*.md")):
                if p.name in RESERVED:
                    continue
                rel = p.relative_to(bundle).as_posix()
                if not (vault / rel).exists():
                    problems.append(f"{rel}: deleted in vault — NOT deleted from bundle (remove by hand if intended)")

    # generated-zone edits: report and ignore
    for d in _GENERATED_DIRS:
        vdir = vault / d
        if not vdir.exists():
            continue
        for p in sorted(vdir.rglob("*.md")):
            if p.name in RESERVED:
                continue
            rel = p.relative_to(vault).as_posix()
            src = bundle / rel
            expected = None
            if src.exists():
                expected = _add_alias(_rewrite(src.read_text(encoding="utf-8"), rel))
            if expected is None:
                problems.append(f"{rel}: new file in generated zone — ignored (derived from sources)")
            elif p.read_text(encoding="utf-8") != expected:
                problems.append(f"{rel}: edited in generated zone — ignored (edit the source and regenerate)")

    return changed, problems


# --------------------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export or import the Obsidian view of the bundle.")
    parser.add_argument("--bundle", type=Path, default=None, help="canonical bundle (default: <catalog>/bundle)")
    parser.add_argument("--out", type=Path, default=None, help="vault dir (default: <catalog>/bundle-obsidian)")
    parser.add_argument("--import", dest="do_import", action="store_true",
                        help="import extensible-zone edits from the vault back into the bundle")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[2]
    bundle = (args.bundle or (root / "bundle")).resolve()
    out = (args.out or (root / "bundle-obsidian")).resolve()
    if not bundle.exists():
        print(f"No bundle at {bundle} — run `python3 -m dca_catalog.generate` first.")
        return 2

    if args.do_import:
        if not out.exists():
            print(f"No vault at {out} — export one first (`python3 -m dca_catalog.obsidian`).")
            return 2
        changed, problems = import_back(out, bundle)
        for msg in problems:
            print(f"  WARN {msg}")
        print(f"Import: {changed} authored node(s) written back to {bundle}")
        if changed:
            print("Now run: make generate && make lint  (re-catalogue indexes, check OKF health)")
        return 1 if any("REJECTED" in m for m in problems) else 0

    n = export(bundle, out)
    print(f"Obsidian view: {n} notes -> {out}  (open this folder as a vault)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Extract Marker nodes from the ``dca-building-blocks`` library.

Source: ``dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/**/*.java``
Each marker interface / annotation becomes one OKF ``Marker`` node carrying the
contract a new application implements (signature, methods, what it extends).

The bundle keeps its own four-way category taxonomy (``tactical``, ``strategic``,
``port-in``, ``port-out``) — stable node paths for links from the authored zone
— while the ``package`` frontmatter records the library package the type
actually lives in (``ddd.strategic.relationships`` for the context-map
annotations, for instance).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .okf import Node, slugify

MARKER_REL = "dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks"

# package sub-path (under buildingblocks/) -> bundle category directory.
# Longest match wins, so ``ddd/strategic/relationships`` is checked before ``ddd/strategic``.
_CATEGORY = {
    "ddd/tactical": "tactical",
    "ddd/strategic/relationships": "strategic",
    "ddd/strategic": "strategic",
    "hexagonal/port/in": "port-in",
    "hexagonal/port/out": "port-out",
}
_PACKAGE_RE = re.compile(r"^package\s+([\w.]+);", re.MULTILINE)

# Anchored at column 0 so example declarations inside javadoc (` * public ...`)
# are not mistaken for the real top-level type declaration.
_DECL_RE = re.compile(
    r"^public\s+(?:abstract\s+)?(interface|class|@interface)\s+(\w+)", re.MULTILINE
)
_METHOD_RE = re.compile(
    r"(?m)^\s*([A-Za-z_][\w<>\[\],\?\. ]*\s+\w+\([^)]*\))(?:\s+default\s+[^;{]+)?\s*;"
)


def _category(path: Path) -> str:
    rel = path.as_posix()
    for key in sorted(_CATEGORY, key=len, reverse=True):
        if f"/buildingblocks/{key}/" in rel:
            return _CATEGORY[key]
    print(
        f"WARNING: marker {path.name} is in no known building-blocks sub-package "
        f"({', '.join(_CATEGORY)}) — defaulting to 'tactical'. Add the package to "
        f"markers._CATEGORY.",
        file=sys.stderr,
    )
    return "tactical"


def _first_sentence(javadoc: str) -> str:
    text = []
    for line in javadoc.splitlines():
        line = line.strip().lstrip("*").strip()
        if line.startswith("/**") or line == "/" or line.startswith("@"):
            continue
        if line:
            text.append(line)
    joined = " ".join(text)
    joined = re.sub(r"<[^>]+>", "", joined)  # drop inline HTML tags
    joined = re.sub(r"\{@\w+\s+([^}]*)\}", r"\1", joined)  # {@code x} -> x
    joined = re.sub(r"\s+", " ", joined).strip()
    m = re.search(r"^(.*?\.)(\s|$)", joined)
    return (m.group(1) if m else joined).strip()


def _signature(source: str, decl_start: int) -> str:
    """Declaration text from 'public' up to the body-opening brace."""
    brace = source.index("{", decl_start)
    sig = source[decl_start:brace]
    return re.sub(r"\s+", " ", sig).strip()


def _display_title(name: str, signature: str) -> str:
    """Simple name plus top-level generic parameter names, e.g. Repository<T, ID>."""
    m = re.search(rf"{re.escape(name)}\s*<(.+?)>\s*(?:extends|implements|$)", signature)
    if not m:
        return ("@" + name) if "@interface" in signature else name
    params, depth, current = [], 0, ""
    for ch in m.group(1):
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif ch == "," and depth == 0:
            params.append(current.strip())
            current = ""
            continue
        current += ch
    params.append(current.strip())
    short = [p.split(" extends ")[0].split()[0] for p in params if p.strip()]
    return f"{name}<{', '.join(short)}>"


def _strip_own_generics(signature: str, name: str) -> str:
    """Remove the type's own generic parameter block so the supertype-clause
    parser doesn't trip over the ``extends`` keyword inside a generic bound."""
    idx = signature.find(name + "<")
    if idx < 0:
        return signature
    start = idx + len(name)
    depth, i = 0, start
    while i < len(signature):
        if signature[i] == "<":
            depth += 1
        elif signature[i] == ">":
            depth -= 1
            if depth == 0:
                return signature[:start] + signature[i + 1 :]
        i += 1
    return signature


def _split_top_level(raw: str) -> list[str]:
    depth, current, parts = 0, "", []
    for ch in raw:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
            continue
        current += ch
    parts.append(current.strip())
    return [re.sub(r"<.*", "", p).strip() for p in parts if p.strip()]


def _supertypes(signature: str, name: str) -> list[str]:
    """Supertypes from the ``extends``/``implements`` clauses (generics removed)."""
    sig = _strip_own_generics(signature, name)
    types: list[str] = []
    em = re.search(r"\bextends\s+(.+?)(?:\s+implements\b|$)", sig)
    if em:
        types += _split_top_level(em.group(1))
    im = re.search(r"\bimplements\s+(.+)$", sig)
    if im:
        types += _split_top_level(im.group(1))
    return types


def extract(repo_root: Path) -> list[Node]:
    base = repo_root / MARKER_REL
    nodes: list[Node] = []
    for path in sorted(base.rglob("*.java")):
        source = path.read_text(encoding="utf-8")
        decl = _DECL_RE.search(source)
        if not decl:
            continue
        kind, name = decl.group(1), decl.group(2)
        signature = _signature(source, decl.start())
        category = _category(path)

        javadoc = source[: decl.start()]
        last_doc = javadoc.rfind("/**")
        description = _first_sentence(javadoc[last_doc:]) if last_doc >= 0 else ""

        body_start = source.index("{", decl.start())
        body = source[body_start + 1 :]
        methods = [re.sub(r"\s+", " ", m).strip() for m in _METHOD_RE.findall(body)]

        is_annotation = kind == "@interface"
        title = _display_title(name, signature)
        extends = _supertypes(signature, name)

        fm = {
            "type": "Marker",
            "title": title,
            "category": category,
            "kind": "annotation" if is_annotation else ("class" if kind == "class" else "interface"),
            "signature": signature,
        }
        pkg = _PACKAGE_RE.search(source)
        if pkg:
            fm["package"] = pkg.group(1)
        if extends:
            fm["extends"] = extends
        if methods:
            fm["methods"] = methods
        rel = path.relative_to(repo_root).as_posix()
        fm["resource"] = rel
        fm["tags"] = [category, "marker"]

        node = Node(
            path=f"marker/{category}/{slugify(name)}.md",
            frontmatter=fm,
            body=description or f"Marker for {name}.",
            meta={"name": name, "kind": "marker", "extends": extends},
        )
        nodes.append(node)
    return nodes

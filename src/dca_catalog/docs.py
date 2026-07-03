"""Extract Chapter/Guide + Section nodes from the book and the implementation guide.

These two are the *main* body of the catalog; the marker/rule/ADR nodes are the
concrete anchoring beneath them.

Hybrid granularity: each markdown file becomes a container node (``Chapter`` for
``dca-book/``, ``Guide`` for ``implementing-domain-centric-architecture/``) plus
one ``Section`` child node per ``##`` heading. Section bodies carry the **full
verbatim text** so the bundle is self-contained.
"""

from __future__ import annotations

import re
from pathlib import Path

from .okf import Node, bundle_link, slugify

BOOK_REL = "dca-book"
GUIDE_REL = "implementing-domain-centric-architecture"

# files that are meta/tooling, not knowledge content
_SKIP = {"CLAUDE.md", "adr-template.md", "RESTRUCTURING-PLAN.md"}

_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def _split_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (preamble, [(h2_title, section_body), ...]).

    Fence-aware: ``## `` lines inside ```code fences``` do not start a section.
    """
    lines = text.splitlines()
    preamble: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    current: list[str] | None = None
    in_fence = False
    fence_marker = ""
    seen_h1 = False

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence = False
            (current if current is not None else preamble).append(line)
            continue

        if not in_fence and not seen_h1 and re.match(r"^#\s+\S", line):
            seen_h1 = True
            continue  # drop the H1 (becomes the container title)

        if not in_fence and re.match(r"^##\s+\S", line):
            title = line.lstrip("#").strip()
            sections.append((title, []))
            current = sections[-1][1]
            continue

        (current if current is not None else preamble).append(line)

    return (
        "\n".join(preamble).strip(),
        [(t, "\n".join(b).strip()) for t, b in sections],
    )


def _dedupe(slug: str, used: set[str]) -> str:
    if slug not in used:
        used.add(slug)
        return slug
    i = 2
    while f"{slug}-{i}" in used:
        i += 1
    used.add(f"{slug}-{i}")
    return f"{slug}-{i}"


def _process_dir(repo_root: Path, rel_dir: str, source: str, container_type: str, top: str) -> list[Node]:
    base = repo_root / rel_dir
    nodes: list[Node] = []
    for path in sorted(base.glob("*.md")):
        if path.name in _SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        h1 = _H1_RE.search(text)
        title = h1.group(1).strip() if h1 else path.stem
        stem = path.stem if path.stem.lower() != "readme" else "readme"
        preamble, sections = _split_sections(text)
        resource = path.relative_to(repo_root).as_posix()

        container_path = f"{top}/{stem}.md"
        container = Node(
            path=container_path,
            frontmatter={
                "type": container_type,
                "title": title,
                "source": source,
                "resource": resource,
                "tags": [source, container_type.lower()],
            },
            body=preamble or f"{title}.",
            meta={"name": title, "kind": "document"},
        )
        nodes.append(container)

        used: set[str] = set()
        section_links: list[tuple[str, str]] = []
        for sec_title, sec_body in sections:
            if not sec_title.strip():
                continue
            slug = _dedupe(slugify(sec_title) or "section", used)
            spath = f"{top}/{stem}/{slug}.md"
            section_links.append((sec_title, bundle_link(spath)))
            nodes.append(
                Node(
                    path=spath,
                    frontmatter={
                        "type": "Section",
                        "title": sec_title,
                        "chapter": title,
                        "source": source,
                        "resource": resource,
                        "tags": [source, "section"],
                    },
                    body=sec_body or f"{sec_title}.",
                    meta={"name": sec_title, "kind": "section", "scan_text": sec_body},
                )
            )
        container.add_section("Sections", section_links)
    return nodes


def extract(repo_root: Path) -> list[Node]:
    return (
        _process_dir(repo_root, BOOK_REL, "book", "Chapter", "book")
        + _process_dir(repo_root, GUIDE_REL, "guide", "Guide", "guide")
    )

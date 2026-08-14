"""Extract Guide + Section nodes from the implementation guide.

The guide is the *main* body of the catalog; the marker and rule nodes are the
concrete anchoring beneath it.

Hybrid granularity: each markdown file becomes a ``Guide`` container node plus
one ``Section`` child node per ``##`` heading. Section bodies carry the **full
verbatim text** so the bundle is self-contained.

Verbatim text carries the *source* documents' relative links (``./README.md``,
``./spring-modulith.md#packaging-rules``), which point at nothing once the text
lives in a bundle node. Extraction therefore runs in two passes: pass one parses
every guide file into its node layout and heading anchors, pass two rewrites
those links onto bundle nodes while emitting the nodes. Every relative link in
guide text must end up on a node — a guide that links a non-source document
(the book is not public, so a reader could not follow it) is a guide bug, not
something this module papers over.

``_process_dir`` stays parameterised even with a single caller: it is the seam
that made adding a second prose source free, and would be the seam again.
"""

from __future__ import annotations

import re
from pathlib import Path

from .okf import Node, bundle_link, slugify
from .process import NODE_PATH as _ADR_PROCESS_NODE, TEMPLATE_REL as _ADR_TEMPLATE_REL

GUIDE_REL = "implementing-domain-centric-architecture"

# files that are meta/tooling, not knowledge content
_SKIP = {"CLAUDE.md", "adr-template.md", "RESTRUCTURING-PLAN.md"}

# Guide files that carry no Guide node of their own but *are* represented in the
# bundle by another node type. Links to them are rewritten onto that node.
_ALIASES = {Path(_ADR_TEMPLATE_REL).name: _ADR_PROCESS_NODE}

_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_HEADING_RE = re.compile(r"^(#{2,6})\s+(\S.*?)\s*$")

# A markdown link to a relative ``.md`` target, with an optional #anchor.
# Absolute (OKF) targets and URLs are left alone.
_REL_LINK_RE = re.compile(r"(\[[^\]]*\]\()(?!/|\w+:)([^)\s#]+\.md)(#[^)\s]*)?(\))")

# Inline code spans, so a backticked link *example* is never rewritten.
_CODE_SPAN_RE = re.compile(r"`+[^`]*`+")


def _norm_anchor(text: str) -> str:
    """Compare anchors across slug dialects.

    GitHub drops ``&`` and leaves the surrounding spaces, yielding a double dash
    (``references--further-reading``) where :func:`slugify` collapses to one.
    Normalising both sides makes the comparison dialect-independent.
    """
    return re.sub(r"-+", "-", text.strip().lower()).strip("-")


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


def _sub_headings(body: str) -> list[str]:
    """Heading titles (H2..H6) inside a section body, fences excluded."""
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence = False
            continue
        if in_fence:
            continue
        match = _HEADING_RE.match(line)
        if match:
            out.append(match.group(2))
    return out


class _Document:
    """One parsed guide file: its node layout plus its anchor targets."""

    def __init__(self, path: Path, repo_root: Path, top: str) -> None:
        text = path.read_text(encoding="utf-8")
        h1 = _H1_RE.search(text)
        self.path = path
        self.title = h1.group(1).strip() if h1 else path.stem
        self.stem = path.stem if path.stem.lower() != "readme" else "readme"
        self.resource = path.relative_to(repo_root).as_posix()
        self.container_path = f"{top}/{self.stem}.md"
        self.preamble, sections = _split_sections(text)

        used: set[str] = set()
        # (title, body, bundle path) per section, in document order
        self.sections: list[tuple[str, str, str]] = []
        # normalised anchor -> bundle path of the node that carries that heading
        self.anchors: dict[str, str] = {}
        for sec_title, sec_body in sections:
            if not sec_title.strip():
                continue
            slug = _dedupe(slugify(sec_title) or "section", used)
            spath = f"{top}/{self.stem}/{slug}.md"
            self.sections.append((sec_title, sec_body, spath))
            for heading in [sec_title, *_sub_headings(sec_body)]:
                self.anchors.setdefault(_norm_anchor(slugify(heading)), spath)

    def target_for(self, anchor: str) -> str:
        """Bundle path a link into this document should point at.

        An anchor resolves to the node carrying that heading; an unknown anchor
        (or none) falls back to the container node.
        """
        if anchor:
            return self.anchors.get(_norm_anchor(anchor), self.container_path)
        return self.container_path


def _rewrite_line(line: str, base_dir: Path, docs: dict[Path, _Document]) -> str:
    def replace(match: re.Match) -> str:
        target = (base_dir / match.group(2)).resolve()
        doc = docs.get(target)
        if doc is not None:
            anchor = (match.group(3) or "").lstrip("#")
            return match.group(1) + bundle_link(doc.target_for(anchor)) + match.group(4)
        if target.parent == base_dir and target.name in _ALIASES:
            return match.group(1) + bundle_link(_ALIASES[target.name]) + match.group(4)
        return match.group(0)  # not represented in the bundle — leave it alone

    # Code spans are masked rather than skipped over: link *text* is regularly
    # backticked (``[`spring-modulith.md`](spring-modulith.md)``), so splitting
    # the line at them would tear the link apart before the regex sees it.
    spans: list[str] = []

    def mask(match: re.Match) -> str:
        spans.append(match.group(0))
        return f"\x00{len(spans) - 1}\x00"

    masked = _REL_LINK_RE.sub(replace, _CODE_SPAN_RE.sub(mask, line))
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], masked)


def _rewrite_links(text: str, base_dir: Path, docs: dict[Path, _Document]) -> str:
    """Point relative ``.md`` links at bundle nodes, leaving code blocks intact."""
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence = False
            out.append(line)
            continue
        out.append(line if in_fence else _rewrite_line(line, base_dir, docs))
    return "\n".join(out)


def _process_dir(repo_root: Path, rel_dir: str, source: str, container_type: str, top: str) -> list[Node]:
    base = (repo_root / rel_dir).resolve()
    parsed = [
        _Document(path, repo_root, top)
        for path in sorted(base.glob("*.md"))
        if path.name not in _SKIP
    ]
    docs = {doc.path.resolve(): doc for doc in parsed}

    nodes: list[Node] = []
    for doc in parsed:
        container = Node(
            path=doc.container_path,
            frontmatter={
                "type": container_type,
                "title": doc.title,
                "source": source,
                "resource": doc.resource,
                "tags": [source, container_type.lower()],
            },
            body=_rewrite_links(doc.preamble, base, docs) or f"{doc.title}.",
            meta={"name": doc.title, "kind": "document"},
        )
        nodes.append(container)

        section_links: list[tuple[str, str]] = []
        for sec_title, sec_body, spath in doc.sections:
            body = _rewrite_links(sec_body, base, docs)
            section_links.append((sec_title, bundle_link(spath)))
            nodes.append(
                Node(
                    path=spath,
                    frontmatter={
                        "type": "Section",
                        "title": sec_title,
                        "chapter": doc.title,
                        "source": source,
                        "resource": doc.resource,
                        "tags": [source, "section"],
                    },
                    body=body or f"{sec_title}.",
                    meta={"name": sec_title, "kind": "section", "scan_text": body},
                )
            )
        container.add_section("Sections", section_links)
    return nodes


def extract(repo_root: Path) -> list[Node]:
    return _process_dir(repo_root, GUIDE_REL, "guide", "Guide", "guide")

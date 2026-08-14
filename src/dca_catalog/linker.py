"""Cross-link nodes into a navigable graph.

Deterministic, string-based: scan rule bodies and guide sections for marker type
references, then emit reciprocal bundle-relative link sections. Over-linking is
tolerated (OKF treats links as soft); links are sorted for stable output.
"""

from __future__ import annotations

import re

from .okf import Node, bundle_link

# ArchUnit constant -> marker simple name
_CONST_MARKER = {
    "REPOSITORY_MARKER": "Repository",
    "OUTPUT_PORT_MARKER": "OutputPort",
    "INPUT_PORT_MARKER": "InputPort",
}

_REF_RE = re.compile(
    r"(?:implement|beAssignableTo|areAssignableTo|isAssignableTo|doNotImplement)"
    r"\w*\(\s*(\w+)|(\w+)\.class|\bextends\s+(\w+)"
)
# generic words skipped in free prose to avoid noise (still matched via .class etc.)
_PROSE_SKIP = {"Id", "Value", "Entity", "Store"}


def _link(node: Node) -> tuple[str, str]:
    return (str(node.frontmatter["title"]), bundle_link(node.path))


def _marker_refs(text: str, markers: dict[str, Node], prose: bool) -> set[str]:
    found: set[str] = set()
    for m in _REF_RE.finditer(text):
        name = m.group(1) or m.group(2) or m.group(3)
        if name in markers:
            found.add(name)
        elif name in _CONST_MARKER and _CONST_MARKER[name] in markers:
            found.add(_CONST_MARKER[name])
    for const, name in _CONST_MARKER.items():
        if const in text and name in markers:
            found.add(name)
    # word-boundary prose matches for distinctive marker names
    for name in markers:
        if name in _PROSE_SKIP and prose:
            continue
        distinctive = len(name) >= 8 or any(c.isupper() for c in name[1:]) or name == "Factory"
        if distinctive and re.search(rf"\b{re.escape(name)}\b", text):
            found.add(name)
    return found


def link(markers: list[Node], rules: list[Node]) -> None:
    by_name = {n.meta["name"]: n for n in markers}
    rule_nodes = [n for n in rules if n.meta.get("kind") == "rule"]

    governed_by: dict[str, list[Node]] = {name: [] for name in by_name}

    # Rule -> markers
    for rule in rule_nodes:
        names = _marker_refs(rule.meta["scan_text"], by_name, prose=False)
        targets = sorted((by_name[n] for n in names), key=lambda x: x.path)
        rule.add_section("Applies to markers", [_link(m) for m in targets])
        for n in names:
            governed_by[n].append(rule)

    _link_markers_back(markers, governed_by)


def _link_markers_back(markers, governed_by):
    by_name = {n.meta["name"]: n for n in markers}
    # Marker -> extends / governed-by
    for marker in markers:
        extends = [by_name[e] for e in marker.meta.get("extends", []) if e in by_name]
        marker.add_section(
            "Extends", [_link(e) for e in sorted(extends, key=lambda x: x.path)]
        )
        govs = sorted(governed_by[marker.meta["name"]], key=lambda x: x.path)
        marker.add_section("Governed by", [_link(r) for r in govs])


def _title_pattern(name: str) -> re.Pattern:
    """Regex matching a marker name in a section title, tolerating the spaced
    form ("AggregateRoot" -> "Aggregate Roots") and simple plurals."""
    words = re.findall(r"[A-Z][a-z0-9]*|[a-z0-9]+", name)
    parts = []
    for i, word in enumerate(words):
        if i == len(words) - 1:  # pluralize the last word
            if word.endswith("y"):
                parts.append(re.escape(word[:-1]) + "(?:y|ies)")
            else:
                parts.append(re.escape(word) + "(?:e?s)?")
        else:
            parts.append(re.escape(word))
    return re.compile(r"\b" + r"[ -]?".join(parts) + r"\b", re.IGNORECASE)


# "Discussed in" thresholds: a section is a primary discussion of a marker when
# its title names the marker, or the body mentions it densely. Capped to keep
# the reverse edge low-noise (90+ sections mention Repository in passing).
_DISCUSS_MIN_MENTIONS = 4
_DISCUSS_MAX_LINKS = 10


def link_docs(docs: list[Node], markers: list[Node]) -> None:
    """Anchor guide Section nodes to the skeleton by linking the markers they
    name. Markers link back to the sections that primarily discuss them
    ("Discussed in") — title match or dense mentions."""
    by_name = {n.meta["name"]: n for n in markers}
    name_res = {name: _title_pattern(name) for name in by_name}
    # marker name -> list of (title_matched, mention_count, section node)
    discussed_in: dict[str, list[tuple[bool, int, Node]]] = {name: [] for name in by_name}

    for node in docs:
        if node.meta.get("kind") != "section":
            continue
        text = node.meta.get("scan_text", "")
        names = _marker_refs(text, by_name, prose=True)
        mtargets = sorted((by_name[n] for n in names), key=lambda x: x.path)
        node.add_section("Related markers", [_link(m) for m in mtargets])

        title = str(node.frontmatter.get("title", ""))
        for name in by_name:
            in_title = bool(name_res[name].search(title))
            mentions = len(name_res[name].findall(text))
            if in_title or mentions >= _DISCUSS_MIN_MENTIONS:
                discussed_in[name].append((in_title, mentions, node))

    for marker in markers:
        # title matches first, then densest mentions; path as deterministic tiebreak
        ranked = sorted(
            discussed_in[marker.meta["name"]],
            key=lambda t: (not t[0], -t[1], t[2].path),
        )[:_DISCUSS_MAX_LINKS]
        sections = sorted((n for _t, _c, n in ranked), key=lambda x: x.path)
        marker.add_section("Discussed in", [_link(s) for s in sections])

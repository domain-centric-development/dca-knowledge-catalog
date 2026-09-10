"""OKF node model and markdown writer.

A :class:`Node` is one OKF concept document. The writer emits YAML frontmatter
(mandatory ``type`` first) followed by the body and any cross-link sections.
Output is deterministic — no timestamps, stable key/section ordering — so the
generated ``bundle/`` is byte-identical for the same sources (CI-checkable).
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

# Reserved OKF filenames that are not concept documents.
RESERVED = {"index.md", "log.md", "index-compact.md"}


def slugify(text: str) -> str:
    """Turn an arbitrary title into a stable, link-safe ASCII slug.

    Accented letters lose their diacritics (``ä`` -> ``a``), ``ß`` becomes ``ss``; anything
    else outside ASCII is treated as a separator. File names therefore never depend on the
    file system's Unicode normalisation.
    """
    text = unicodedata.normalize("NFKD", text.strip().lower().replace("ß", "ss"))
    out = []
    prev_dash = False
    for ch in text:
        if not ch.isascii():
            continue
        if ch.isalnum():
            out.append(ch)
            prev_dash = False
        elif not prev_dash:
            out.append("-")
            prev_dash = True
    return "".join(out).strip("-")


def _yaml_scalar(value: str) -> str:
    """Emit a YAML scalar, quoting when needed.

    Assumes single-line scalars (titles, signatures, slugs) — multi-line content
    belongs in the node *body*, not frontmatter. A newline here would produce
    invalid YAML, so fail loudly rather than emit a broken bundle.
    """
    assert "\n" not in value, f"newline in YAML scalar: {value!r}"
    if value == "":
        return '""'
    needs_quote = any(c in value for c in ':#{}[],&*!|>%@`"()') or value[0] in " '\"" or value[-1] == " "
    if needs_quote:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def _yaml_value(value) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(_yaml_scalar(str(v)) for v in value) + "]"
    return _yaml_scalar(str(value))


@dataclass
class LinkSection:
    """A ``## Heading`` block of bundle-relative markdown links."""

    heading: str
    # list of (link text, bundle-relative target path)
    links: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class Node:
    """One OKF concept document."""

    # bundle-relative path, e.g. "marker/port-out/repository.md"
    path: str
    # ordered frontmatter; ``type`` is forced first on write
    frontmatter: dict
    # markdown body (intro prose / code block) shown before link sections
    body: str = ""
    sections: list[LinkSection] = field(default_factory=list)
    # generator-internal data used by the linker; never rendered to disk
    meta: dict = field(default_factory=dict)

    @property
    def directory(self) -> str:
        return self.path.rsplit("/", 1)[0] if "/" in self.path else ""

    def add_section(self, heading: str, links: list[tuple[str, str]]) -> None:
        if links:
            self.sections.append(LinkSection(heading, links))

    def render(self) -> str:
        fm = self.frontmatter
        lines = ["---", f"type: {_yaml_value(fm['type'])}"]
        for key, value in fm.items():
            if key == "type":
                continue
            lines.append(f"{key}: {_yaml_value(value)}")
        lines.append("---")
        out = "\n".join(lines) + "\n"
        if self.body.strip():
            out += "\n" + self.body.strip() + "\n"
        for sec in self.sections:
            out += f"\n## {sec.heading}\n\n"
            for text, target in sec.links:
                out += f"- [{text}]({target})\n"
        return out.rstrip() + "\n"


def bundle_link(to_path: str) -> str:
    """Bundle-relative link target (leading ``/``) per the OKF spec."""
    return "/" + to_path

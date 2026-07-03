"""Extract ADR (used-pattern) nodes + the "creating-an-adr" Process node.

ADR source: ``ai-architecture-sample/docs/architecture/adr/adr-*.md``
The ADRs document the *architectural patterns used* (decision + rationale +
consequences). We keep the pattern-level content and **drop code blocks and
e-commerce domain examples** — the catalog is about the architecture, not the
sample's domain.

Process source: ``implementing-domain-centric-architecture/adr-template.md``
"""

from __future__ import annotations

import re
from pathlib import Path

from .okf import Node

ADR_REL = "ai-architecture-sample/docs/architecture/adr"
TEMPLATE_REL = "implementing-domain-centric-architecture/adr-template.md"

_TITLE_RE = re.compile(r"^#\s+ADR-(\d+)\s*:\s*(.+?)\s*$", re.MULTILINE)
_STATUS_RE = re.compile(r"\*\*Status\*\*\s*:?\s*(.+)")
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def _strip(text: str) -> str:
    """Drop code blocks / HTML / emoji-noise and collapse whitespace."""
    text = _FENCE_RE.sub("", text)
    text = re.sub(r"^>.*$", "", text, flags=re.MULTILINE)  # blockquotes (often book quotes)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _sections(source: str) -> dict[str, str]:
    out: dict[str, str] = {}
    parts = re.split(r"^##\s+(.+?)\s*$", source, flags=re.MULTILINE)
    # parts[0] is the preamble; then (heading, body) pairs
    for i in range(1, len(parts), 2):
        out[parts[i].strip().lower()] = parts[i + 1]
    return out


def _status(source: str) -> str:
    m = _STATUS_RE.search(source)
    if not m:
        return "accepted"
    raw = m.group(1)
    raw = re.sub(r"[^A-Za-z \-]", "", raw).strip()  # drop ✅/🟡 emoji
    return raw.split()[0].lower() if raw else "accepted"


def _decision(sections: dict[str, str]) -> str:
    body = sections.get("decision", "")
    bold = _BOLD_RE.search(body)
    if bold:
        return re.sub(r"\s+", " ", bold.group(1)).strip().rstrip(".") + "."
    clean = _strip(body)
    m = re.match(r"(.*?\.)(\s|$)", clean)
    return (m.group(1) if m else clean[:240]).strip()


def _consequences(sections: dict[str, str]) -> list[str]:
    body = sections.get("consequences", "")
    labels: list[str] = []
    for line in body.splitlines():
        m = re.match(r"\s*(?:[✅⚠️❌📌]|[-*])\s*\*\*(.+?)\*\*", line)
        if m:
            labels.append(m.group(1).strip())
    if labels:
        return labels[:8]
    # fall back to first bolded items anywhere in the section
    return [b.strip() for b in _BOLD_RE.findall(body)][:6]


def _tags(title: str) -> list[str]:
    keywords = {
        "aggregate": "aggregate", "repository": "repository", "event": "events",
        "domain": "domain", "hexagonal": "hexagonal", "bounded context": "strategic",
        "shared kernel": "strategic", "open host": "strategic", "value object": "value-object",
        "use case": "use-case", "factory": "factory", "specification": "specification",
        "naming": "naming", "viewmodel": "adapter", "package": "package-structure",
    }
    low = title.lower()
    tags = ["adr"] + sorted({tag for kw, tag in keywords.items() if kw in low})
    return tags


def _extract_adrs(repo_root: Path) -> list[Node]:
    base = repo_root / ADR_REL
    nodes: list[Node] = []
    for path in sorted(base.glob("adr-*.md")):
        source = path.read_text(encoding="utf-8")
        tm = _TITLE_RE.search(source)
        if not tm:
            continue
        number, short_title = tm.group(1), tm.group(2)
        full_title = f"ADR-{number}: {short_title}"
        sections = _sections(source)
        decision = _decision(sections)
        consequences = _consequences(sections)
        status = _status(source)

        body_lines = [decision]
        if consequences:
            body_lines.append("\n**Consequences:** " + " · ".join(consequences))

        fm = {
            "type": "ADR",
            "title": full_title,
            "adr": int(number),
            "status": status,
            "pattern": decision,
            "resource": path.relative_to(repo_root).as_posix(),
            "tags": _tags(short_title),
        }
        nodes.append(
            Node(
                path=f"adr/{path.stem}.md",
                frontmatter=fm,
                body="\n".join(body_lines).strip(),
                meta={"name": full_title, "kind": "adr", "scan_text": source},
            )
        )
    return nodes


def _process_node(repo_root: Path) -> Node:
    template = (repo_root / TEMPLATE_REL).read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(.+?)\s*$", template, flags=re.MULTILINE)
    skip = {"template metadata", "how to use this template", "notes"}
    skeleton = [h.strip() for h in headings if h.strip().lower() not in skip]

    body = (
        "How to record an architectural decision in this project, so a new "
        "application keeps the same decision log format (Michael Nygard style).\n\n"
        "## Steps\n\n"
        "1. Copy the ADR template and number it sequentially: `adr-XXX-short-title.md` "
        "(next available number).\n"
        "2. Use a descriptive title that states *what* is being decided.\n"
        "3. Fill in every section (below) — brief is fine, but each adds context.\n"
        "4. Set `Status` (Proposed → Accepted → Deprecated/Superseded by ADR-YYY). "
        "Never delete a superseded ADR; mark it and link the replacement.\n"
        "5. Update the ADR index/README and get it reviewed.\n"
        "6. Where the decision is machine-enforceable, add or reference an ArchUnit "
        "rule and link it from the ADR.\n\n"
        "## Section skeleton\n\n"
        + "\n".join(f"- **{h}**" for h in skeleton)
        + "\n\n## When to write an ADR\n\n"
        "Significant, hard-to-reverse decisions; choices between viable alternatives; "
        "patterns used across the codebase. Skip trivial or easily reversible details."
    )
    return Node(
        path="process/creating-an-adr.md",
        frontmatter={
            "type": "Process",
            "title": "How to write an ADR",
            "resource": TEMPLATE_REL,
            "tags": ["adr", "process", "governance"],
        },
        body=body,
        meta={"name": "How to write an ADR", "kind": "process"},
    )


def extract(repo_root: Path) -> list[Node]:
    return _extract_adrs(repo_root) + [_process_node(repo_root)]

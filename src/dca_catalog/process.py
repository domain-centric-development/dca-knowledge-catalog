"""Extract the "creating-an-adr" Process node.

Source: ``implementing-domain-centric-architecture/adr-template.md``

The catalog records how to *write* an architectural decision, not the decisions
of any one project: a record like "ADR-030" is a fact about the reference
implementation, and a reader building their own application has no such file.
"""

from __future__ import annotations

import re
from pathlib import Path

from .okf import Node

TEMPLATE_REL = "implementing-domain-centric-architecture/adr-template.md"
# The template is not a Guide node, so guide links to it are rewritten here
# instead (see ``docs._ALIASES``).
NODE_PATH = "process/creating-an-adr.md"


def _fillable_template(text: str) -> str:
    """The copyable part of the template: everything before its meta sections.

    ``## Template Metadata`` and what follows explain how to *use* the template;
    those are already distilled into the Steps and When-to-write sections below.
    """
    cut = text.find("\n## Template Metadata")
    body = (text[:cut] if cut != -1 else text).rstrip()
    return body.removesuffix("---").rstrip()


def _process_node(repo_root: Path) -> Node:
    template = (repo_root / TEMPLATE_REL).read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(.+?)\s*$", template, flags=re.MULTILINE)
    skip = {"template metadata", "how to use this template", "notes"}
    skeleton = [h.strip() for h in headings if h.strip().lower() not in skip]
    # the template's own fences are ``` — the wrapper needs a longer marker
    fillable = _fillable_template(template)
    fence = "`" * max(4, max((len(m) for m in re.findall(r"^`{3,}", fillable, re.M)), default=3) + 1)

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
        "patterns used across the codebase. Skip trivial or easily reversible details.\n\n"
        "## The template\n\n"
        "Copy this into `adr-XXX-short-title.md` and fill it in. The `**Example:**` "
        "blocks show the expected depth — replace them, don't keep them.\n\n"
        f"{fence}markdown\n{fillable}\n{fence}"
    )
    return Node(
        path=NODE_PATH,
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
    return [_process_node(repo_root)]

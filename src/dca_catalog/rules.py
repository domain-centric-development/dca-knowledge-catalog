"""Extract Rule nodes from the reference implementation's ArchUnit tests.

Source: ``ai-architecture-sample/src/test-architecture/groovy/.../*ArchUnitTest.groovy``
Each Spock feature method (``def "<rule statement>"() { ... }``) becomes one OKF
``Rule`` node. The method name is already a human-readable rule statement; the
body is carried verbatim as a fenced code block (lossless, no semantic parsing).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .okf import Node, slugify

RULES_REL = "ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture"

# test class -> bundle category directory
_CATEGORY = {
    "DddTacticalPatternsArchUnitTest": "tactical",
    "DddAdvancedPatternsArchUnitTest": "advanced",
    "DddStrategicPatternsArchUnitTest": "strategic",
    "HexagonalArchitectureArchUnitTest": "hexagonal",
    "OnionArchitectureArchUnitTest": "onion",
    "LayeredArchitectureArchUnitTest": "layered",
    "PackageCyclesArchUnitTest": "cycles",
    "NamingConventionsArchUnitTest": "naming",
    "UseCasePatternsArchUnitTest": "usecase",
}

# Test classes that match the *ArchUnitTest.groovy glob but carry no extractable
# rules (base/helper). Listed explicitly so a *new* unmapped test class warns
# loudly instead of being silently dropped from the catalog.
_KNOWN_NON_RULE = {"BaseArchUnitTest"}

_METHOD_RE = re.compile(r'def\s+"((?:[^"\\]|\\.)*)"\s*\(\s*\)\s*\{')
_BECAUSE_RE = re.compile(r'\.because\(\s*"((?:[^"\\]|\\.)*)"')


def _method_body(source: str, brace_open: int) -> str:
    depth, i = 0, brace_open
    while i < len(source):
        ch = source[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return source[brace_open + 1 : i]
        i += 1
    return source[brace_open + 1 :]


def _dedent(body: str) -> str:
    lines = [ln for ln in body.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    indents = [len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()]
    pad = min(indents) if indents else 0
    return "\n".join(ln[pad:] if len(ln) >= pad else ln for ln in lines)


def _assertion_block(body: str) -> str:
    """The executable content of the feature's assertion block (``expect:`` or ``then:``).

    Setup in ``given:``/``when:`` is not an assertion, so it must not count towards deciding
    whether a rule checks anything. A feature whose ``given:`` computes two unread variables
    and whose ``expect:`` is the literal ``true`` enforces nothing, however busy it looks.
    """
    stripped = re.sub(r"//.*", "", body)
    stripped = re.sub(r"/\*.*?\*/", "", stripped, flags=re.DOTALL)
    lines, collecting = [], False
    for ln in stripped.splitlines():
        label = ln.strip()
        if label in ("expect:", "then:"):
            collecting = True
            continue
        if label in ("given:", "when:", "where:", "cleanup:", "setup:"):
            collecting = False
            continue
        if collecting and label:
            lines.append(label)
    return "\n".join(lines).strip()


def _status(body: str) -> str:
    if "disabled" in body.lower():
        return "disabled"
    assertion = _assertion_block(body)
    # A feature whose only assertion is the literal `true` documents a pattern rather than
    # enforcing one — checked before check(), since setup may call anything.
    if re.fullmatch(r"true\b.*", assertion, re.DOTALL):
        return "informational"
    # Anything that actually runs an ArchUnit rule against the classes is enforced,
    # regardless of diagnostics/prints alongside it.
    if "check(" in assertion or "check(" in body:
        return "enforced"
    # A diagnostic/print-only feature (no .check()) documents rather than enforces.
    if "Diagnostic" in body or "println" in body:
        return "informational"
    return "enforced"


def _constraint(title: str) -> str:
    """The rule as a single-line, actionable precondition an LLM satisfies while
    generating code. The Spock method name is already a ``X must Y`` statement —
    normalize whitespace and trailing punctuation so it is machine-addressable."""
    return " ".join(title.split()).rstrip(".") + "."


def _because(body: str, title: str) -> str:
    m = _BECAUSE_RE.search(body)
    if not m:
        return title.rstrip(".") + "."
    text = m.group(1).replace('\\"', '"')
    # Spock GString interpolation -> readable placeholder
    text = re.sub(r"\$\{[^}]*\}", "<context>", text)
    return text.rstrip(".") + "."


def extract(repo_root: Path) -> list[Node]:
    base = repo_root / RULES_REL
    nodes: list[Node] = []
    for path in sorted(base.glob("*ArchUnitTest.groovy")):
        class_name = path.stem
        category = _CATEGORY.get(class_name)
        if category is None:
            if class_name not in _KNOWN_NON_RULE:
                print(
                    f"WARNING: ArchUnit test class {class_name!r} is not mapped in "
                    f"rules._CATEGORY — its rules are excluded from the catalog. "
                    f"Add it to _CATEGORY or _KNOWN_NON_RULE.",
                    file=sys.stderr,
                )
            continue
        source = path.read_text(encoding="utf-8")
        rel = path.relative_to(repo_root).as_posix()
        for m in _METHOD_RE.finditer(source):
            title = m.group(1).replace('\\"', '"')
            body = _method_body(source, m.end() - 1)
            status = _status(body)
            code = _dedent(body)
            fm = {
                "type": "Rule",
                "title": title,
                "rule": _because(body, title),
                "constraint": _constraint(title),
                "enforced_by": f"{class_name}#{title}",
                "status": status,
                "test_class": class_name,
                "resource": rel,
                "tags": [category, "archunit"],
            }
            node = Node(
                path=f"rule/{category}/{slugify(title)}.md",
                frontmatter=fm,
                body=f"```groovy\n{code}\n```",
                meta={"name": title, "kind": "rule", "scan_text": body},
            )
            nodes.append(node)
    return nodes

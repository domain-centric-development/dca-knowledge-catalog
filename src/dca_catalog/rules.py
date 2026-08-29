"""Extract Rule nodes from the ``dca-archunit`` rule library.

Sources (both under ``dca-java/``):

* ``rules.json`` — the rule catalog the library renders from its own code
  (``./gradlew :dca-archunit:rulesCatalog``): one entry per rule with the
  stable id (``DCA-TAC-006``), the rule set, the title and the rationale.
  Titles are *resolved* — a rule whose title embeds a configured suffix is
  rendered for the default layout — so this file, not the Java source, is the
  authority for what a rule says.
* ``dca-archunit/src/main/java/.../rules/<Set>Rules.java`` — the implementation.
  The ``DcaRule.of(...)`` / ``DcaRule.check(...)`` expression that constructs a
  rule is carried verbatim as a fenced code block (lossless, no semantic
  parsing) and scanned by the linker for marker references.

Each rule becomes one OKF ``Rule`` node. Node paths are derived from the title
so links from the authored zone stay stable across implementation changes.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from .okf import Node, slugify

JAVA_REL = "dca-java"
RULES_JSON_REL = f"{JAVA_REL}/rules.json"
DOTNET_REL = "dca-dotnet"
DOTNET_RULES_JSON_REL = f"{DOTNET_REL}/rules.json"
DOTNET_RULES_SRC_REL = f"{DOTNET_REL}/src/DomainCentric.ArchRules/Rules"
RULES_SRC_REL = f"{JAVA_REL}/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules"

# rule set name (as in rules.json / DcaRuleSet.name()) -> implementing class
_RULE_SET_CLASS = {
    "layered": "LayeredRules",
    "onion": "OnionRules",
    "hexagonal": "HexagonalRules",
    "tactical": "TacticalPatternRules",
    "strategic": "StrategicPatternRules",
    "contextmap": "ContextMapRules",
    "advanced": "AdvancedPatternRules",
    "usecase": "UseCaseRules",
    "naming": "NamingRules",
    "cycles": "CycleRules",
}

_FACTORY_RE = re.compile(r"DcaRule\.(?:of|check)\s*\(")


def _expression_at(source: str, id_literal: str) -> str | None:
    """The ``DcaRule.of(...)``/``DcaRule.check(...)`` call that carries ``id_literal``."""
    at = source.find(f'"{id_literal}"')
    if at < 0:
        return None
    start = max((m.start() for m in _FACTORY_RE.finditer(source, 0, at)), default=-1)
    if start < 0:
        return None
    open_paren = source.index("(", start)
    depth, i, in_string, escaped = 0, open_paren, False, False
    while i < len(source):
        ch = source[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        elif ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return source[start : i + 1]
        i += 1
    return source[start:]


def _dedent(code: str) -> str:
    lines = code.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return ""
    # The expression starts mid-line (`return DcaRule.of(`); keep the arguments indented
    # by one continuation step (4) relative to it, as google-java-format wrote them.
    indents = [len(ln) - len(ln.lstrip()) for ln in lines[1:] if ln.strip()]
    pad = max(0, (min(indents) if indents else 0) - 4)
    return "\n".join([lines[0].strip()] + [ln[pad:] if len(ln) >= pad else ln for ln in lines[1:]])


def _status(title: str, code: str) -> str:
    """``enforced`` unless the rule is documentation-only.

    A rule is informational when its title says so (``Diagnostic: …``) or when
    its check body is empty (``arch -> {}``) — it then exists to carry doctrine
    into the catalog, never to fail a build.
    """
    if title.startswith("Diagnostic"):
        return "informational"
    if re.search(r"arch\s*->\s*\{\s*\}", code):
        return "informational"
    return "enforced"


def _constraint(title: str) -> str:
    """The rule as a single-line, actionable precondition an LLM satisfies while
    generating code. The title is already an ``X must Y`` statement — normalize
    whitespace and trailing punctuation so it is machine-addressable."""
    return " ".join(title.split()).rstrip(".") + "."


def _dotnet_catalog(repo_root: Path) -> tuple[dict[str, dict], dict[str, str]]:
    """``(ported, not_applicable)`` from ``dca-dotnet/rules.json`` — ported entries keyed by
    id; not-applicable ids mapped to the reason. Both empty when the file is absent."""
    path = repo_root / DOTNET_RULES_JSON_REL
    if not path.exists():
        print(f"WARNING: {path} not found — rule nodes list the Java implementation only.", file=sys.stderr)
        return {}, {}
    ported: dict[str, dict] = {}
    not_applicable: dict[str, str] = {}
    for entry in json.loads(path.read_text(encoding="utf-8")):
        if entry.get("status") == "n/a":
            not_applicable[entry["id"]] = entry["reason"]
        else:
            ported[entry["id"]] = entry
    return ported, not_applicable


def _dotnet_class(rule_set: str) -> str:
    return _RULE_SET_CLASS.get(rule_set, "DotnetRules")


def extract(repo_root: Path) -> list[Node]:
    dotnet_ported, dotnet_na = _dotnet_catalog(repo_root)
    catalog_path = repo_root / RULES_JSON_REL
    if not catalog_path.exists():
        raise SystemExit(
            f"{catalog_path} not found — run `./gradlew :dca-archunit:rulesCatalog` in {JAVA_REL}/ first."
        )
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    sources: dict[str, str] = {}
    nodes: list[Node] = []
    for entry in entries:
        rule_set, rule_id, title, rationale = (
            entry["set"], entry["id"], entry["title"], entry["rationale"],
        )
        class_name = _RULE_SET_CLASS.get(rule_set)
        if class_name is None:
            print(
                f"WARNING: rule set {rule_set!r} ({rule_id}) is not mapped in rules._RULE_SET_CLASS — "
                f"its rules are excluded from the catalog.",
                file=sys.stderr,
            )
            continue
        src_path = repo_root / RULES_SRC_REL / f"{class_name}.java"
        if class_name not in sources:
            sources[class_name] = src_path.read_text(encoding="utf-8") if src_path.exists() else ""
        expression = _expression_at(sources[class_name], rule_id)
        if expression is None:
            print(f"WARNING: no DcaRule expression found for {rule_id} in {class_name}.java", file=sys.stderr)
            code = ""
        else:
            code = _dedent(expression)
        implementations = ["java"] + (["dotnet"] if rule_id in dotnet_ported else [])
        fm = {
            "type": "Rule",
            "id": rule_id,
            "title": title,
            "rule": rationale.rstrip(".") + ".",
            "constraint": _constraint(title),
            "enforced_by": f"{class_name}#{rule_id}",
            "status": _status(title, code),
            "rule_set": rule_set,
            "implementations": implementations,
            "resource": (Path(RULES_SRC_REL) / f"{class_name}.java").as_posix(),
            "tags": [rule_set, "archunit"],
        }
        if rule_id in dotnet_na:
            fm["not_applicable_dotnet"] = dotnet_na[rule_id]
        body = f"```java\n{code}\n```" if code else ""
        dotnet_ported.pop(rule_id, None)
        nodes.append(
            Node(
                path=f"rule/{rule_set}/{slugify(title)}.md",
                frontmatter=fm,
                body=body,
                meta={"name": title, "kind": "rule", "scan_text": code},
            )
        )
    # Rules that exist only in the .NET library (rule set ``dotnet``, ids DCA-NET-…).
    for rule_id, entry in sorted(dotnet_ported.items()):
        rule_set, title, rationale = entry["set"], entry["title"], entry["rationale"]
        class_name = _dotnet_class(rule_set)
        nodes.append(
            Node(
                path=f"rule/{rule_set}/{slugify(title)}.md",
                frontmatter={
                    "type": "Rule",
                    "id": rule_id,
                    "title": title,
                    "rule": rationale.rstrip(".") + ".",
                    "constraint": _constraint(title),
                    "enforced_by": f"{class_name}#{rule_id}",
                    "status": "enforced",
                    "rule_set": rule_set,
                    "implementations": ["dotnet"],
                    "resource": (Path(DOTNET_RULES_SRC_REL) / f"{class_name}.cs").as_posix(),
                    "tags": [rule_set, "archunitnet"],
                },
                body="",
                meta={"name": title, "kind": "rule", "scan_text": ""},
            )
        )
    return nodes

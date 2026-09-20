"""Extract Rule nodes from the ``dca-archunit`` rule library.

Sources (both under ``dca-java/``):

* ``rules.json`` — the rule catalog the library renders from its own code
  (``./gradlew :dca-archunit:rulesCatalog``): one entry per rule with the
  stable id (``DCA-TAC-006``), the rule set, the title, the rationale and the
  two mechanics texts ``selects`` (which classes the rule looks at) and
  ``checks`` (what it asserts, including what does not count). Both are
  mandatory — a rule without them fails generation.
  Titles are *resolved* — a rule whose title embeds a configured suffix is
  rendered for the default layout — so this file, not the Java source, is the
  authority for what a rule says.
* ``dca-archunit/src/main/java/.../rules/<Set>Rules.java`` — the implementation.
  The ``DcaRule.of(...)`` / ``DcaRule.check(...)`` expression that constructs a
  rule — including its ``.selecting(...).checking(...)`` completion — is carried
  verbatim as a fenced code block (lossless, no semantic parsing) and scanned by
  the linker for marker references. The private helpers the expression calls
  (``publishAfterSaving()``, ``repositoryInterfaces(arch)``, …) are copied into
  the node too, so the node is readable without the source; the
  ``DcaArchitecture`` methods it uses are listed by name.

Each rule becomes one OKF ``Rule`` node. Node paths use immutable rule ids, independent of titles.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from .okf import Node

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
    "errors": "ErrorHandlingRules",
}

_FACTORY_RE = re.compile(r"DcaRule\.(?:of|check|informational)\s*\(", re.I)


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
                return source[start : _chain_end(source, i + 1)]
        i += 1
    return source[start:]


def _chain_end(source: str, i: int) -> int:
    """End of the ``.selecting(...).checking(...)`` chain that follows a factory
    call: the position of the terminating ``;`` (exclusive)."""
    n = len(source)
    while i < n:
        j = i
        while j < n and source[j].isspace():
            j += 1
        if j < n and source[j] == ".":
            k = source.index("(", j)
            depth, in_string, escaped = 0, False, False
            while k < n:
                ch = source[k]
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
                        break
                k += 1
            i = k + 1
            continue
        return i
    return n


_CALL_RE = re.compile(r"(?<![\w.])([a-z]\w*)\s*\(")
_MEMBER_CALL_RE = re.compile(r"\.([a-z]\w*)\s*\(")
_JAVA_KEYWORDS = frozenset(
    "if for while do switch catch synchronized return new throw super this try assert".split()
)
_ARCH_CALL_RE = re.compile(r"\barch\.(\w+)\s*\(")
_SHARED_HELPER_CLASSES = ("IntraClassCalls", "TypeInspection", "CollectedViolations", "AnnotationRoles", "DomainMetadata", "OperationPolicy", "EventFreeAggregate")


def _method_source(source: str, name: str) -> str | None:
    """The declarations of method ``name`` in ``source`` (every overload) — javadoc
    included, bodies matched by braces — or ``None`` when the class declares no such
    method."""
    found = _method_sources(source, name)
    return "\n\n".join(found) if found else None


def _method_sources(source: str, name: str) -> list[str]:
    found: list[str] = []
    for m in re.finditer(rf"(?m)^  (?! )(?:(?:public|private|protected|static|final|synchronized)\s+)*[\w<>\[\],?. ]+?\s+{re.escape(name)}\s*\(", source):
        start = m.start()
        # take the javadoc directly above, if any
        before = source[:start]
        doc = before.rstrip()
        if doc.endswith("*/"):
            doc_start = doc.rfind("/**")
            if doc_start >= 0:
                start = doc_start
        brace = source.find("{", m.end())
        semi = source.find(";", m.end())
        if brace < 0 or (0 <= semi < brace):
            continue  # abstract/interface declaration — not a helper body
        depth, i, in_string, escaped = 0, brace, False, False
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
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    found.append(_dedent_block(source[start : i + 1]))
                    break
            i += 1
    return found


def _dedent_block(code: str) -> str:
    lines = code.splitlines()
    indents = [len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()]
    pad = min(indents) if indents else 0
    return "\n".join(ln[pad:] if len(ln) >= pad else ln for ln in lines)


def _helpers(expression: str, class_source: str, shared: dict[str, str]) -> tuple[list[tuple[str, str, str]], list[str]]:
    """``([(class, name, source)], [DcaArchitecture method names])``: the helper
    methods the expression calls — transitively, within the rule class and the
    shared helper classes of the rules package — and the ``arch.*`` methods used
    anywhere along the way. Rules from ``DcaRule`` itself and ArchUnit's fluent
    API are not methods of these classes and are skipped naturally."""
    found: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    arch_methods: set[str] = set()
    queue: list[tuple[str, str]] = [("", expression)]
    while queue:
        owner, code = queue.pop(0)
        arch_methods.update(_ARCH_CALL_RE.findall(code))
        for name in dict.fromkeys(_CALL_RE.findall(code)):
            if name in _JAVA_KEYWORDS:
                continue
            candidates = [("", class_source)] + [(c, src) for c, src in shared.items() if owner == c]
            for cls, src in candidates:
                if (cls, name) in seen:
                    continue
                body = _method_source(src, name)
                if body is None:
                    continue
                seen.add((cls, name))
                found.append((cls, name, body))
                queue.append((cls, body))
                break
        # methods invoked on the shared helper classes (``calls.entryPointsOf(unit)``,
        # ``TypeInspection.instanceFields(current)``) — embedded when that class is in play
        referenced = [c for c in shared if f"{c}." in code or f"new {c}(" in code or f" {c} " in code or owner == c]
        for name in dict.fromkeys(_MEMBER_CALL_RE.findall(code)):
            for cls in referenced:
                if (cls, name) in seen:
                    continue
                body = _method_source(shared[cls], name)
                if body is None:
                    continue
                seen.add((cls, name))
                found.append((cls, name, body))
                queue.append((cls, body))
                break
    return found, sorted(arch_methods)


def _body(code: str, selects: str, checks: str, helpers, arch_methods, dotnet: dict | None) -> str:
    parts = [f"## Selection\n\n{selects}", f"## Check\n\n{checks}"]
    if (
        dotnet
        and dotnet.get("selects")
        and dotnet.get("checks")
        and (dotnet["selects"] != selects or dotnet["checks"] != checks)
    ):
        parts.append(
            "## .NET reading\n\n**Selection.** "
            + dotnet.get("selects", "")
            + "\n\n**Check.** "
            + dotnet.get("checks", "")
        )
    if code:
        parts.append(f"## Implementation\n\n```java\n{code}\n```")
    if helpers:
        blocks = []
        for cls, name, src in helpers:
            label = f"{cls}.{name}" if cls else name
            blocks.append(f"### `{label}`\n\n```java\n{src}\n```")
        parts.append("## Helpers\n\n" + "\n\n".join(blocks))
    if arch_methods:
        parts.append(
            "## Architecture queries\n\n"
            "[DcaArchitecture](/reference/architecture.md) methods the rule relies on: "
            + ", ".join(f"`{m}()`" for m in arch_methods)
            + " - how they resolve packages is described there and in "
            "[DcaLayout](/reference/layout.md)."
        )
    return "\n\n".join(parts)


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


def _catalog(path: Path) -> tuple[list[dict], list[dict]]:
    """Legacy arrays and the versioned rules/retired envelope are accepted."""
    data = json.loads(path.read_text(encoding="utf-8"))
    entries, retired = (data, []) if isinstance(data, list) else (data["rules"], data.get("retired", []))
    ids = [e["id"] for e in entries + retired]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate active/retired id in {path}")
    for entry in entries:
        if entry.get("status", "enforced") not in {"enforced", "informational", "n/a"}:
            raise ValueError(f"invalid rule status: {entry}")
    for entry in retired:
        if not all(entry.get(key) for key in ("id", "reason", "replacement", "since")):
            raise ValueError(f"incomplete retirement: {entry}")
    return entries, retired


def _dotnet_catalog(repo_root: Path) -> tuple[dict[str, dict], dict[str, str]]:
    """``(ported, not_applicable)`` from ``dca-dotnet/rules.json`` — ported entries keyed by
    id; not-applicable ids mapped to the reason. Both empty when the file is absent."""
    path = repo_root / DOTNET_RULES_JSON_REL
    if not path.exists():
        print(f"WARNING: {path} not found — rule nodes list the Java implementation only.", file=sys.stderr)
        return {}, {}
    ported: dict[str, dict] = {}
    not_applicable: dict[str, str] = {}
    for entry in _catalog(path)[0]:
        if entry.get("status") == "n/a":
            not_applicable[entry["id"]] = entry["reason"]
        else:
            ported[entry["id"]] = entry
    return ported, not_applicable


def _dotnet_class(rule_set: str) -> str:
    return _RULE_SET_CLASS.get(rule_set, "DotnetRules")


def _cs_evidence(repo_root: Path, rule_set: str, rule_id: str) -> str:
    path = repo_root / DOTNET_RULES_SRC_REL / (_dotnet_class(rule_set) + ".cs")
    if not path.exists():
        return ""
    source = path.read_text(encoding="utf-8")
    expression = _expression_at(source, rule_id)
    if not expression:
        raise ValueError(f"no C# rule expression for {rule_id}")
    body = "### C# expression\n\n```csharp\n" + _dedent(expression) + "\n```\n"
    # Shared policy helpers carry the semantics behind short factory expressions.
    for name in ("OperationPolicy", "DomainMetadata", "EventFreeAggregate", "IntraClassCalls"):
        if name + "." in expression or "new " + name + "(" in expression:
            helper = path.parent / (name + ".cs")
            body += "\n### C# helper " + name + "\n\n```csharp\n" + helper.read_text().strip() + "\n```\n"
    return body


def extract(repo_root: Path) -> list[Node]:
    dotnet_ported, dotnet_na = _dotnet_catalog(repo_root)
    catalog_path = repo_root / RULES_JSON_REL
    if not catalog_path.exists():
        raise SystemExit(
            f"{catalog_path} not found — run `./gradlew :dca-archunit:rulesCatalog` in {JAVA_REL}/ first."
        )
    entries, retired = _catalog(catalog_path)
    retired_by_id = {entry["id"]: entry for entry in retired}
    dotnet_path = repo_root / DOTNET_RULES_JSON_REL
    if dotnet_path.exists():
        for entry in _catalog(dotnet_path)[1]:
            if entry["id"] in retired_by_id and retired_by_id[entry["id"]] != entry:
                raise ValueError(f"conflicting retirement: {entry['id']}")
            retired_by_id[entry["id"]] = entry
    if set(retired_by_id) & ({e["id"] for e in entries} | set(dotnet_ported)):
        raise ValueError("retired id remains active in another implementation")
    sources: dict[str, str] = {}
    shared_sources = {
        c: (repo_root / RULES_SRC_REL / f"{c}.java").read_text(encoding="utf-8")
        for c in _SHARED_HELPER_CLASSES
        if (repo_root / RULES_SRC_REL / f"{c}.java").exists()
    }
    undescribed = [e["id"] for e in entries if not e.get("selects") or not e.get("checks")]
    if undescribed:
        raise SystemExit(
            f"{len(undescribed)} rule(s) in {RULES_JSON_REL} carry no selects/checks text: "
            + ", ".join(undescribed)
            + " — every rule must describe its mechanics (DcaRule.selecting/checking)."
        )
    nodes: list[Node] = []
    for entry in entries:
        rule_set, rule_id, title, rationale = (
            entry["set"], entry["id"], entry["title"], entry["rationale"],
        )
        selects, checks = entry["selects"], entry["checks"]
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
        helpers, arch_methods = _helpers(code, sources[class_name], shared_sources) if code else ([], [])
        fm = {
            "type": "Rule",
            "id": rule_id,
            "title": title,
            "rule": rationale.rstrip(".") + ".",
            "constraint": _constraint(title),
            "selects": selects,
            "checks": checks,
            "enforced_by": f"{class_name}#{rule_id}",
            "status": entry.get("status", _status(title, code)),
            "rule_set": rule_set,
            "implementations": implementations,
            "resource": (Path(RULES_SRC_REL) / f"{class_name}.java").as_posix(),
            "tags": [rule_set, "archunit"],
        }
        if rule_id in dotnet_na:
            fm["not_applicable_dotnet"] = dotnet_na[rule_id]
        dotnet_entry = dotnet_ported.pop(rule_id, None)
        body = _body(code, selects, checks, helpers, arch_methods, dotnet_entry)
        if dotnet_entry:
            if "## .NET reading" not in body:
                body += "\n\n## .NET reading\n"
            body += "\n" + _cs_evidence(repo_root, rule_set, rule_id)
            fm["resource_dotnet"] = (Path(DOTNET_RULES_SRC_REL) / (_dotnet_class(rule_set) + ".cs")).as_posix()
        scan_text = code + "\n" + "\n".join(src for _, _, src in helpers)
        nodes.append(
            Node(
                path=f"rule/{rule_set}/{rule_id.lower()}.md",
                frontmatter=fm,
                body=f"# {title}\n\n" + body,
                meta={"name": title, "kind": "rule", "scan_text": scan_text},
            )
        )
    # Rules that exist only in the .NET library (rule set ``dotnet``, ids DCA-NET-…).
    for rule_id, entry in sorted(dotnet_ported.items()):
        rule_set, title, rationale = entry["set"], entry["title"], entry["rationale"]
        class_name = _dotnet_class(rule_set)
        nodes.append(
            Node(
                path=f"rule/{rule_set}/{rule_id.lower()}.md",
                frontmatter={
                    "type": "Rule",
                    "id": rule_id,
                    "title": title,
                    "rule": rationale.rstrip(".") + ".",
                    "constraint": _constraint(title),
                    "selects": entry.get("selects", ""),
                    "checks": entry.get("checks", ""),
                    "enforced_by": f"{class_name}#{rule_id}",
                    "status": entry.get("status", "enforced"),
                    "rule_set": rule_set,
                    "implementations": ["dotnet"],
                    "resource": (Path(DOTNET_RULES_SRC_REL) / f"{class_name}.cs").as_posix(),
                    "tags": [rule_set, "archunitnet"],
                },
                body=(
                    f"## Selection\n\n{entry['selects']}\n\n## Check\n\n{entry['checks']}\n\n" + _cs_evidence(repo_root, rule_set, rule_id)
                    if entry.get("selects") and entry.get("checks")
                    else ""
                ),
                meta={"name": title, "kind": "rule", "scan_text": ""},
            )
        )
    if retired_by_id:
        body = ["# Retired rules", "", "Retired ids are never reused. They no longer enforce a check."]
        for rule_id, entry in sorted(retired_by_id.items()):
            body.extend(["", f"## {rule_id}", "", entry["reason"], "",
                         f"Replacement: {entry['replacement']}", "", f"Since: {entry['since']}"])
        nodes.append(Node(
            path="rule/retired.md",
            frontmatter={"type": "Reference", "title": "Retired rules", "tags": ["governance"]},
            body="\n".join(body),
            meta={"retired_ids": sorted(retired_by_id)},
        ))
    return nodes

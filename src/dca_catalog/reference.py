"""Extract Reference nodes for the two classes every rule is parameterised by.

* ``reference/layout.md`` — ``DcaLayout`` (Java) and its .NET twin: every
  setting with its default and ``with*`` override, the derived package/namespace
  patterns, the building-block package constants, the third-party packages the
  domain may use, and the framework annotation/type names the rules look for.
* ``reference/architecture.md`` — ``DcaArchitecture`` (Java) and its .NET
  twin: how bounded contexts, the shared kernel and module roots are discovered
  and every public query the rules select through (``allApplicationPatterns()``,
  ``moduleRoots()``, ``contextName(...)``, …).

Everything is rendered from the sources — javadoc, XML doc comments, the
constants and the default-building code — never typed by hand, so a changed
default cannot drift from the node. Without these two nodes a reader cannot
answer "does rule X apply to my package Y?" from the catalog alone.
"""

from __future__ import annotations

import re
from pathlib import Path

from .markers import _javadoc_markdown, _mask, _unescape
from .okf import Node

JAVA_SRC_REL = "dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit"
DOTNET_SRC_REL = "dca-dotnet/src/DomainCentric.ArchRules"

_SECTION_RE = re.compile(r"(?m)^  // -{20,}\n  // (.+?)\n  // -{20,}\n")
_DEFAULT_RE = re.compile(r"defaults\.(\w+) = (\"[^\"]*\"|[\w.()]+);")
_CONST_RE = re.compile(r"public static final String (\w+) =\s*\"([^\"]*)\";")
_LIST_CONST_RE = re.compile(r"(\w+) =\s*List\.of\((.*?)\);", re.S)
_WITH_RE = re.compile(r"(?m)^  public DcaLayout (with\w+|allowingInDomain)\(")
_JAVA_PUBLIC_RE = re.compile(
    r"(?m)^  (?! )(?:@\w+(?:\([^)]*\))?\s+)*public\s+(?!class\b|interface\b|enum\b|record\b)"
    r"(?:static\s+|final\s+)*(?:<[^>]+>\s+)?[\w<>\[\],?. ]+?\s+(\w+)\s*\("
)
_XML_SUMMARY_RE = re.compile(r"///\s?(.*)")
_CS_PUBLIC_RE = re.compile(r"^    public\s+(?!sealed class|class|record|const|static class)(.+?)(?:\s*=>|\s*\{|\s*;|$)")


# --------------------------------------------------------------------------- java

def _class_javadoc(source: str) -> str:
    decl = re.search(r"(?m)^public\s+(?:final\s+)?(?:class|record)\s+\w+", source)
    if not decl:
        return ""
    before = source[: decl.start()]
    start = before.rfind("/**")
    return _javadoc_markdown(before[start:]) if start >= 0 else ""


def _javadoc_before(source: str, pos: int) -> str:
    """The javadoc block that ends right before ``pos`` (annotations and
    whitespace between them tolerated), rendered to markdown; ``""`` if none."""
    before = source[:pos]
    # skip annotations like @Override / @Deprecated(since = "...") between doc and member
    stripped = re.sub(r"(?:@\w+(?:\([^)]*\))?\s*)+$", "", before.rstrip()).rstrip()
    if not stripped.endswith("*/"):
        return ""
    start = stripped.rfind("/**")
    return _javadoc_markdown(stripped[start:]) if start >= 0 else ""


def _sections(source: str) -> list[tuple[int, str]]:
    return [(m.start(), m.group(1).strip()) for m in _SECTION_RE.finditer(source)]


def _section_at(sections: list[tuple[int, str]], pos: int) -> str:
    title = ""
    for start, name in sections:
        if start < pos:
            title = name
    return title


def _clean_header(header: str) -> str:
    header = re.sub(r"@\w+(?:\([^)]*\))?", "", header)
    header = re.sub(r"\s+", " ", header).strip()
    header = re.sub(r"\s*\(\s*", "(", header)
    header = re.sub(r"\s*\)", ")", header)
    header = re.sub(r"\s*,\s*", ", ", header)
    return header.removeprefix("public ")


def _java_public_methods(source: str) -> list[tuple[str, str, str]]:
    """``(section, header, javadoc_md)`` for every public method of the top-level
    class, in declaration order. Nested classes (indented deeper) are skipped."""
    masked = _mask(source)
    sections = _sections(source)
    result: list[tuple[str, str, str]] = []
    for m in _JAVA_PUBLIC_RE.finditer(masked):
        start = m.start()
        # header runs to the first '{' or ';' at the member's own depth
        i = masked.index("(", m.end() - 1)
        depth = 0
        while i < len(masked):
            ch = masked[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif depth == 0 and ch in "{;":
                break
            i += 1
        header = _clean_header(source[start:i])
        header = re.sub(r"\s+throws\s+[\w.,\s]+$", "", header)
        result.append((_section_at(sections, start), header, _javadoc_before(source, start)))
    return result


def _java_defaults(source: str) -> list[tuple[str, str]]:
    body = source[source.index("forBasePackage(String basePackage)") :]
    body = body[: body.index("return new DcaLayout")]
    return [(name, value.strip('"')) for name, value in _DEFAULT_RE.findall(body)]


def _java_constants(source: str) -> list[tuple[str, str]]:
    return _CONST_RE.findall(source)


def _java_list_constant(source: str, name: str) -> list[str]:
    for const, items in _LIST_CONST_RE.findall(source):
        if const == name:
            return re.findall(r"\"([^\"]*)\"", items)
    return []


def _java_setters(source: str) -> dict[str, str]:
    """``with*`` method name -> first sentence of its javadoc (may be empty)."""
    out: dict[str, str] = {}
    for m in _WITH_RE.finditer(source):
        doc = _javadoc_before(source, m.start())
        out[m.group(1)] = doc.split("\n\n")[0].strip()
    return out


def _java_pattern_methods(source: str) -> list[tuple[str, str]]:
    """``(header, javadoc)`` of the derived-name and pattern accessors."""
    result = []
    for section, header, doc in _java_public_methods(source):
        if section.startswith("Derived package names"):
            result.append((header, doc))
    return result


def _framework_annotations(source: str) -> list[tuple[str, str, str]]:
    """``(component, fqn, description)`` for ``FrameworkAnnotations.spring()``."""
    params = re.findall(r"@param (\w+) (.+?)(?=\n \* @param|\n \*/)", source, re.S)
    descriptions = {name: re.sub(r"\s*\n\s*\*\s*", " ", text).strip() for name, text in params}
    masked = _mask(source)
    components = re.findall(r"^\s{4}String (\w+),?\)?", source[: masked.index("{")], re.M)
    spring = source[masked.index("spring()") :]
    values = re.findall(r"\"([\w.]+)\"", spring[: spring.index(";")])
    return [(c, v, _unescape(descriptions.get(c, ""))) for c, v in zip(components, values)]


# --------------------------------------------------------------------------- .net

def _xml_to_markdown(lines: list[str]) -> str:
    text = "\n".join(lines)
    text = re.sub(r"<see cref=\"([^\"]+)\"\s*/>", lambda m: f"`{m.group(1).split('.')[-1]}`", text)
    text = re.sub(r"<paramref name=\"([^\"]+)\"\s*/>", r"`\1`", text)
    text = re.sub(r"<c>(.*?)</c>", r"`\1`", text, flags=re.S)
    text = re.sub(r"<code>(.*?)</code>", lambda m: "\n```csharp\n" + m.group(1).strip("\n") + "\n```\n", text, flags=re.S)
    text = re.sub(r"<b>(.*?)</b>", r"**\1**", text, flags=re.S)
    text = re.sub(r"<em>(.*?)</em>", r"*\1*", text, flags=re.S)
    text = re.sub(r"</?para>", "\n\n", text)
    text = re.sub(r"</?(?:summary|remarks)>", "\n\n", text)
    text = re.sub(r"<param name=\"(\w+)\">(.*?)</param>", r"- `\1`: \2", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _cs_class_doc(source: str) -> str:
    decl = re.search(r"(?m)^public (?:sealed |static )?(?:class|record) \w+", source)
    if not decl:
        return ""
    doc_lines = [m.group(1) for m in _XML_SUMMARY_RE.finditer(source[: decl.start()])]
    # only the block directly above the declaration: after the last blank line
    block: list[str] = []
    for line in source[: decl.start()].splitlines():
        s = line.strip()
        if s.startswith("///"):
            block.append(s[3:].lstrip(" "))
        elif s and not s.startswith("["):
            block = []
    return _xml_to_markdown(block if block else doc_lines)


def _cs_public_members(source: str) -> list[tuple[str, str]]:
    """``(signature, summary_md)`` for every public member of the top-level type
    (4-space indent). Nested types' members (8 spaces) are skipped."""
    members: list[tuple[str, str]] = []
    doc: list[str] = []
    for line in source.splitlines():
        s = line.strip()
        if line.startswith("    ///"):
            doc.append(s[3:].lstrip(" "))
            continue
        m = _CS_PUBLIC_RE.match(line)
        if m and line.startswith("    public") and not line.startswith("     "):
            sig = m.group(1).strip()
            sig = re.sub(r"\s+", " ", sig)
            members.append((sig, _xml_to_markdown(doc)))
        if not line.startswith("    [") and s:
            doc = []
    return members


def _cs_consts(source: str) -> list[tuple[str, str]]:
    return re.findall(r"public const string (\w+) = \"([^\"]*)\";", source)


def _cs_default_third_party(source: str) -> list[str]:
    m = re.search(r"DefaultThirdPartyAllowedInDomain =\s*new\[\] \{(.*?)\};", source, re.S)
    if not m:
        return []
    items = []
    for raw in m.group(1).split(","):
        raw = raw.strip()
        if raw.startswith('"'):
            items.append(raw.strip('"'))
        elif raw:
            const = dict(_cs_consts(source)).get(raw)
            items.append(const or raw)
    return items


def _cs_defaults(source: str) -> list[tuple[str, str]]:
    ctor = re.search(r"private DcaLayout\((.*?)\)\s*\{", source, re.S)
    names = re.findall(r"\w+ (\w+),?", ctor.group(1)) if ctor else []
    factory = re.search(r"ForRootNamespace\(string rootNamespace\) =>\s*new\((.*?)\);", source, re.S)
    args = [a.strip() for a in factory.group(1).split(",")] if factory else []
    return [(n, a.strip('"')) for n, a in zip(names, args) if n != "rootNamespace"]


def _cs_setters(source: str) -> list[str]:
    return re.findall(r"public DcaLayout (With\w+|AllowingInDomain)\(", source)


def _framework_types(source: str) -> list[tuple[str, str, str]]:
    params = dict(re.findall(r"<param name=\"(\w+)\">(.*?)</param>", source, re.S))
    decl_end = re.search(r"\)\s*\n\{", source)
    components = re.findall(r"^\s{4}string (\w+),?\)?$", source[: decl_end.start()] if decl_end else source, re.M)
    values = re.findall(r"\"([\w.]+)\"", source[source.index("AspNetCore()") :])
    return [(c, v, _xml_to_markdown([params.get(c, "")])) for c, v in zip(components, values)]


# --------------------------------------------------------------------------- render

def _table(headers: list[str], rows: list[list[str]]) -> str:
    def cell(v: str) -> str:
        return v.replace("|", "\\|").replace("\n", " ")

    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def _layout_body(java: str, annotations: str, cs: str, types: str) -> str:
    setters = _java_setters(java)
    defaults = _java_defaults(java)
    parts = [_class_javadoc(java)]

    rows = []
    for name, value in defaults:
        if name in ("thirdPartyPackagesAllowedInDomain", "frameworkAnnotations"):
            continue
        if name == "basePackage":
            rows.append(["`basePackage`", "the argument of `forBasePackage(...)`", "constructor only", "Root package of the application; everything the rules govern lies below it."])
            continue
        setter = "with" + name[0].upper() + name[1:]
        rows.append([f"`{name}`", f"`{value}`", f"`{setter}(...)`" if setter in setters else "constructor only", setters.get(setter, "")])
    parts.append("## Settings and defaults (Java)\n\nCreate the default layout with `DcaLayout.forBasePackage(String)`; every setting has a fluent override.\n\n" + _table(["Setting", "Default", "Override", "Meaning"], rows))

    third = _java_list_constant(java, "DEFAULT_THIRD_PARTY_ALLOWED_IN_DOMAIN")
    parts.append(
        "## Third-party packages the domain may depend on (Java default)\n\n"
        + "\n".join(f"- `{p}`" for p in third)
        + "\n\nReplace the list with `withThirdPartyPackagesAllowedInDomain(List)` or extend it with `allowingInDomain(String...)`."
    )

    parts.append(
        "## Building-block package constants (Java)\n\n"
        + _table(["Constant", "Pattern"], [[f"`{n}`", f"`{v}`"] for n, v in _java_constants(java)])
    )

    pat_rows = []
    methods = [(h, d) for h, d in _java_pattern_methods(java) if not h.endswith("toString()")]
    wildcard = {re.match(r"\w+ (\w+)\(\)", h).group(1): d for h, d in methods if re.match(r"\w+ \w+\(\)$", h)}
    for header, doc in methods:
        if not doc:
            m = re.match(r"\w+ (\w+)\(String contextPackage\)", header)
            sibling = wildcard.get(m.group(1), "") if m else ""
            if sibling:
                first = re.match(r"`([^`]+)`", sibling)
                if first:
                    doc = "`" + first.group(1).replace("base.*.", "<contextPackage>.") + "` - the same pattern below the given context or module package."
        pat_rows.append([f"`{header}`", doc.replace("\n", " ")])
    parts.append(
        "## Derived package names and patterns (Java)\n\n"
        "ArchUnit pattern syntax: `..` any number of sub-packages, `*` exactly one segment. The no-argument "
        "wildcard accessors match direct children of the base package only; the rules select through "
        "[DcaArchitecture](/reference/architecture.md) instead, which works at any depth.\n\n"
        + _table(["Accessor", "Yields"], pat_rows)
    )

    fa = _framework_annotations(annotations)
    parts.append(
        "## Framework annotations the rules look for (Java, `FrameworkAnnotations.spring()`)\n\n"
        "Annotations are matched by fully qualified name; the rule library has no framework dependency. "
        "Replace the set with `withFrameworkAnnotations(FrameworkAnnotations.of(...))` for another container.\n\n"
        + _table(["Role", "Default annotation", "Used for"], [[f"`{c}`", f"`{v}`", d] for c, v, d in fa])
    )

    # ---- .NET
    parts.append("## .NET twin: `DcaLayout` in `DomainCentric.ArchRules`\n\n" + _cs_class_doc(cs))
    cs_setters = _cs_setters(cs)
    rows = []
    for name, value in _cs_defaults(cs):
        if name in ("thirdPartyNamespacesAllowedInDomain", "frameworkTypes"):
            continue
        setter = "With" + name[0].upper() + name[1:]
        rows.append([f"`{name[0].upper() + name[1:]}`", f"`{value}`", f"`{setter}(...)`" if setter in cs_setters else "constructor only"])
    parts.append("### Settings and defaults (.NET)\n\nCreate the default layout with `DcaLayout.ForRootNamespace(string)`.\n\n" + _table(["Setting", "Default", "Override"], rows))
    parts.append(
        "### Third-party namespaces the domain may depend on (.NET default)\n\n"
        + "\n".join(f"- `{p}`" for p in _cs_default_third_party(cs))
        + "\n\nNote the difference to Java: the whole `DomainCentric.BuildingBlocks` namespace is allowed, strategic and `Ports.In` markers included."
    )
    parts.append(
        "### Building-block namespace constants (.NET)\n\n"
        + _table(["Constant", "Namespace"], [[f"`{n}`", f"`{v}`"] for n, v in _cs_consts(cs)])
    )
    pat_rows = []
    for sig, doc in _cs_public_members(cs):
        if "Pattern" in sig or "Namespace =>" in sig or sig.startswith("static string"):
            pat_rows.append([f"`{sig}`", doc.replace("\n", " ")])
    parts.append(
        "### Derived namespaces and patterns (.NET)\n\n"
        "Patterns are .NET regular expressions over full namespace names for ArchUnitNET's `ResideInNamespaceMatching`.\n\n"
        + _table(["Member", "Yields"], pat_rows)
    )
    ft = _framework_types(types)
    parts.append(
        "### Framework types the rules look for (.NET, `FrameworkTypes.AspNetCore()`)\n\n"
        + _table(["Role", "Default type", "Used for"], [[f"`{c}`", f"`{v}`", d] for c, v, d in ft])
        + "\n\n.NET has no `@Service`/`@Component`-style stereotypes; the Java rules that depend on them have no .NET reading and are listed as not applicable in the rule catalog."
    )
    return "\n\n".join(p for p in parts if p.strip())


def _architecture_body(java: str, cs: str) -> str:
    parts = [_class_javadoc(java)]
    parts.append(
        "## How the rules find their subjects (Java)\n\n"
        "- **Bounded contexts** are declared: a package whose `package-info` carries `@BoundedContext`, at any depth below the base package. `boundedContexts()` lists them; `contextName(...)` names one relative to the base package (`sales.order`).\n"
        "- **The shared kernel** is the package carrying `@SharedKernel` (`sharedKernelPackage()`).\n"
        "- **Module roots** are structural: the shortest package prefix below the base package whose next segment is a layer segment (`domain`, `application`, `adapter`). No annotation is needed, so a module that is deliberately not a bounded context is still governed by the layer rules. The shared kernel is a module root when it owns a layer; `isolatedModuleRoots()` is every module root except the shared kernel.\n"
        "- The `all*Patterns()` accessors expand over **module roots**, the `context*Patterns()` accessors over **declared bounded contexts**. Rule nodes name the accessors they use under *Architecture queries*."
    )
    current = None
    blocks: list[str] = []
    for section, header, doc in _java_public_methods(java):
        if section != current:
            current = section
            blocks.append(f"### {section or 'Construction and access'}")
        blocks.append(f"#### `{header}`" + (f"\n\n{doc}" if doc else ""))
    parts.append("## Java API: `DcaArchitecture`\n\n" + "\n\n".join(blocks))

    parts.append("## .NET twin: `DcaArchitecture` in `DomainCentric.ArchRules`\n\n" + _cs_class_doc(cs))
    rows = [[f"`{sig}`", doc.replace("\n", " ")] for sig, doc in _cs_public_members(cs)]
    parts.append("### .NET API\n\n" + _table(["Member", "Summary"], rows))
    return "\n\n".join(p for p in parts if p.strip())


def extract(repo_root: Path) -> list[Node]:
    java_dir = repo_root / JAVA_SRC_REL
    cs_dir = repo_root / DOTNET_SRC_REL

    def read(path: Path) -> str:
        return path.read_text(encoding="utf-8") if path.exists() else ""

    layout_java = read(java_dir / "DcaLayout.java")
    annotations_java = read(java_dir / "FrameworkAnnotations.java")
    arch_java = read(java_dir / "DcaArchitecture.java")
    layout_cs = read(cs_dir / "DcaLayout.cs")
    types_cs = read(cs_dir / "FrameworkTypes.cs")
    arch_cs = read(cs_dir / "DcaArchitecture.cs")
    if not layout_java or not arch_java:
        raise SystemExit(f"{java_dir} lacks DcaLayout.java / DcaArchitecture.java — cannot render reference nodes")

    nodes = [
        Node(
            path="reference/layout.md",
            frontmatter={
                "type": "Reference",
                "title": "DcaLayout",
                "subject": "layout",
                "resource": f"{JAVA_SRC_REL}/DcaLayout.java",
                "resource_dotnet": f"{DOTNET_SRC_REL}/DcaLayout.cs",
                "tags": ["reference", "archunit", "archunitnet"],
            },
            body=_layout_body(layout_java, annotations_java, layout_cs, types_cs),
            meta={"name": "DcaLayout", "kind": "reference"},
        ),
        Node(
            path="reference/architecture.md",
            frontmatter={
                "type": "Reference",
                "title": "DcaArchitecture",
                "subject": "architecture",
                "resource": f"{JAVA_SRC_REL}/DcaArchitecture.java",
                "resource_dotnet": f"{DOTNET_SRC_REL}/DcaArchitecture.cs",
                "tags": ["reference", "archunit", "archunitnet"],
            },
            body=_architecture_body(arch_java, arch_cs),
            meta={"name": "DcaArchitecture", "kind": "reference"},
        ),
    ]
    return nodes

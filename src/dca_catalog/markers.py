"""Extract Marker nodes from the ``dca-building-blocks`` library.

Source: ``dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/**/*.java``
Each marker interface / annotation becomes one OKF ``Marker`` node carrying the
contract a new application implements (signature, methods, what it extends).

The bundle keeps its own five-way category taxonomy (``tactical``, ``strategic``,
``port-in``, ``port-out``, ``application`` — execution abstractions that are no ports) — stable node paths for links from the authored zone
— while the ``package`` frontmatter records the library package the type
actually lives in (``ddd.strategic.relationships`` for the context-map
annotations, for instance).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .okf import Node, slugify

MARKER_REL = "dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks"

# package sub-path (under buildingblocks/) -> bundle category directory.
# Longest match wins, so ``ddd/strategic/relationships`` is checked before ``ddd/strategic``.
_CATEGORY = {
    "ddd/tactical": "tactical",
    "ddd/strategic/relationships": "strategic",
    "ddd/strategic": "strategic",
    "hexagonal/port/in": "port-in",
    "hexagonal/port/out": "port-out",
    "application": "application",
}
_PACKAGE_RE = re.compile(r"^package\s+([\w.]+);", re.MULTILINE)

# Anchored at column 0 so example declarations inside javadoc (` * public ...`)
# are not mistaken for the real top-level type declaration.
_DECL_RE = re.compile(
    r"^public\s+(?:abstract\s+)?(interface|class|@interface)\s+(\w+)", re.MULTILINE
)
_NESTED_TYPE_RE = re.compile(r"\b(?:class|interface|enum|record|@interface)\b")
_ANNOTATION_RE = re.compile(r"@\w+(?:\([^)]*\))?")
_TYPE_PARAMS_RE = re.compile(r"^(?:public\s+)?(?:abstract\s+)?(?:interface|class|@interface)\s+\w+\s*(<)")


def _mask(source: str, literals: bool = True) -> str:
    """Replace comments — and, unless ``literals`` is false, string/char literals —
    with spaces of equal length so braces, semicolons and parentheses inside them
    cannot confuse the scanner. Positions are preserved, so slices of one mask
    index into the source and into the other mask."""
    out = list(source)
    i, n = 0, len(source)

    def blank(a: int, b: int) -> None:
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        ch = source[i]
        nxt = source[i + 1] if i + 1 < n else ""
        if ch == "/" and nxt == "*":
            end = source.find("*/", i + 2)
            end = n if end < 0 else end + 2
            blank(i, end)
            i = end
        elif ch == "/" and nxt == "/":
            end = source.find("\n", i)
            end = n if end < 0 else end
            blank(i, end)
            i = end
        elif ch in "\"'":
            j = i + 1
            while j < n and source[j] != ch:
                j += 2 if source[j] == "\\" else 1
            end = min(j + 1, n)
            if literals:
                blank(i + 1, end - 1)
            i = end
        else:
            i += 1
    return "".join(out)


def _members(body: str, masked_body: str, type_name: str) -> list[str]:
    """Method declarations of a type body (interface, class or annotation).

    ``body`` has comments blanked, ``masked_body`` comments *and* literals. Walks
    the masked body at brace depth 0. A member header is the text from the
    previous member's terminator (``;`` or the closing brace of its body) up to
    the next ``;`` or ``{``. Headers with a parameter list that are neither a
    constructor nor a nested type are methods; a header ending in ``{`` is a
    method with a body (class method or ``default`` method), whose body is then
    skipped as a whole. An annotation element's array default (``default {}``)
    is the one brace that belongs to the header — it runs on to the ``;``."""
    methods: list[str] = []
    depth, start, i, n = 0, 0, 0, len(masked_body)
    in_array_default = False
    while i < n:
        ch = masked_body[i]
        if depth == 0 and ch == "{" and body[start:i].rstrip().endswith("default"):
            in_array_default = True
            depth = 1
        elif depth == 0 and ch in ";{":
            _add_method(methods, body[start:i], type_name)
            if ch == "{":
                depth = 1
            start = i + 1
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and in_array_default:
                in_array_default = False
            elif depth == 0:
                start = i + 1
            if depth < 0:  # closing brace of the type itself
                break
        i += 1
    return methods


def _add_method(methods: list[str], header: str, type_name: str) -> None:
    header = _ANNOTATION_RE.sub("", header)
    header = re.sub(r"\s+", " ", header).strip()
    header = re.sub(r"\{\s*\}", "{}", header)
    if "(" not in header or _NESTED_TYPE_RE.search(header):
        return
    if header.startswith("private ") or " private " in header.split("(", 1)[0]:
        return  # not part of the contract an implementor sees
    if header.startswith("=") or "=" in header.split("(", 1)[0]:
        return  # field initialiser such as ``List<X> xs = new ArrayList<>()``
    name = header.split("(", 1)[0].split()[-1]
    if name == type_name:
        return  # constructor
    header = re.sub(r"\bfinal\s+", "", header)
    header = re.sub(r"\s*\(\s*", "(", header)
    header = re.sub(r"\s*\)", ")", header)
    header = re.sub(r"\s*,\s*", ", ", header)
    methods.append(header)


def _type_parameters(signature: str) -> str | None:
    """The type's own generic parameter block, verbatim without the angle brackets,
    e.g. ``T extends AggregateRoot<T, ID>, ID extends Id``."""
    m = _TYPE_PARAMS_RE.search(signature)
    if not m:
        return None
    start = m.end(1)
    depth, i = 1, start
    while i < len(signature) and depth > 0:
        if signature[i] == "<":
            depth += 1
        elif signature[i] == ">":
            depth -= 1
        i += 1
    return signature[start : i - 1].strip()


def _modifiers(signature: str) -> list[str]:
    head = signature.split("interface", 1)[0].split("class", 1)[0]
    return [w for w in head.split() if w in ("public", "abstract", "final", "sealed")]


def _category(path: Path) -> str:
    rel = path.as_posix()
    for key in sorted(_CATEGORY, key=len, reverse=True):
        if f"/buildingblocks/{key}/" in rel:
            return _CATEGORY[key]
    print(
        f"WARNING: marker {path.name} is in no known building-blocks sub-package "
        f"({', '.join(_CATEGORY)}) — defaulting to 'tactical'. Add the package to "
        f"markers._CATEGORY.",
        file=sys.stderr,
    )
    return "tactical"


def _first_sentence(javadoc: str) -> str:
    text = []
    for line in javadoc.splitlines():
        line = line.strip().lstrip("*").strip()
        if line.startswith("/**") or line == "/" or line.startswith("@"):
            continue
        if line:
            text.append(line)
    joined = " ".join(text)
    joined = re.sub(r"<[^>]+>", "", joined)  # drop inline HTML tags
    joined = re.sub(r"\{@\w+\s+([^}]*)\}", r"\1", joined)  # {@code x} -> x
    joined = re.sub(r"\s+", " ", joined).strip()
    m = re.search(r"^(.*?\.)(\s|$)", joined)
    return (m.group(1) if m else joined).strip()


def _javadoc_markdown(javadoc: str) -> str:
    """The type's javadoc main description as markdown: paragraphs, ``<ul>``
    lists, ``<pre>`` code blocks, inline tags resolved. Block tags (``@see``,
    ``@param``, ``@since``, …) end the description. Everything the source says
    about the contract reaches the node — nobody should need the sources jar."""
    lines: list[str] = []
    for raw in javadoc.splitlines():
        line = raw.strip()
        if line.startswith("/**"):
            line = line[3:].strip()
        if line.endswith("*/"):
            line = line[:-2].strip()
        if line.startswith("*"):
            line = line[1:]
        if line.startswith(" "):
            line = line[1:]
        lines.append(line.rstrip())
    text = "\n".join(lines)
    text = re.split(r"(?m)^\s*@(?:see|param|return|throws|since|author|version|deprecated)\b", text)[0]

    # <pre> blocks first — their content is code and must not go through the
    # inline-tag or HTML handling. ``<pre>{@code ...}</pre>`` is the javadoc idiom
    # for a code sample: drop the {@code} wrapper, keep the lines as they are.
    out: list[str] = []
    pos = 0
    for m in re.finditer(r"<pre>(.*?)</pre>", text, re.S):
        out.append(_javadoc_prose(text[pos : m.start()]))
        code = m.group(1)
        code = re.sub(r"^\s*\{@code\s*", "", code)
        code = re.sub(r"\}\s*$", "", code) if re.match(r"^\s*\{@code", m.group(1)) else code
        code = re.sub(r"\{@(?:literal|code)\s+([^}]*)\}", r"\1", code)
        code = _html_unescape(code).strip("\n")
        out.append("```java\n" + code + "\n```")
        pos = m.end()
    out.append(_javadoc_prose(text[pos:]))
    md = "\n\n".join(part for part in out if part.strip())
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md


def _javadoc_prose(text: str) -> str:
    """Javadoc prose (no ``<pre>``) to markdown: inline tags, ``<p>``, ``<ul>``/``<li>``, ``<b>``."""
    text = _unescape(text)  # inline tags may span lines — resolve before line handling
    out: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        stripped = re.sub(r"</?(?:ul|ol)>", "", stripped)
        stripped = re.sub(r"^<li>\s*", "- ", stripped)
        stripped = re.sub(r"</li>", "", stripped)
        stripped = re.sub(r"^<p>\s*", "", stripped)
        stripped = re.sub(r"</?p>", "", stripped)
        stripped = re.sub(r"<b>(.*?)</b>", r"**\1**", stripped)
        stripped = re.sub(r"<(?:i|em)>(.*?)</(?:i|em)>", r"*\1*", stripped)
        stripped = re.sub(r"<[^>]+>", "", stripped)
        out.append(_html_unescape(stripped))
    return "\n".join(out)


def _html_unescape(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"')


def _unescape(text: str) -> str:
    text = re.sub(
        r"\{@code\s+([^}]*)\}",
        lambda m: "`" + re.sub(r"\s*\n\s*", " ", m.group(1).strip()) + "`",
        text,
    )
    text = re.sub(r"\{@literal\s+([^}]*)\}", lambda m: m.group(1).strip(), text)
    text = re.sub(r"\{@link\s+(?:[\w.]+)?#?([^}\s]+)[^}]*\}", r"`\1`", text)
    return _html_unescape(text)


def _signature(source: str, decl_start: int) -> str:
    """Declaration text from 'public' up to the body-opening brace."""
    brace = source.index("{", decl_start)
    sig = source[decl_start:brace]
    return re.sub(r"\s+", " ", sig).strip()


def _display_title(name: str, signature: str) -> str:
    """Simple name plus top-level generic parameter names, e.g. Repository<T, ID>."""
    m = re.search(rf"{re.escape(name)}\s*<(.+?)>\s*(?:extends|implements|$)", signature)
    if not m:
        return ("@" + name) if "@interface" in signature else name
    params, depth, current = [], 0, ""
    for ch in m.group(1):
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif ch == "," and depth == 0:
            params.append(current.strip())
            current = ""
            continue
        current += ch
    params.append(current.strip())
    short = [p.split(" extends ")[0].split()[0] for p in params if p.strip()]
    return f"{name}<{', '.join(short)}>"


def _strip_own_generics(signature: str, name: str) -> str:
    """Remove the type's own generic parameter block so the supertype-clause
    parser doesn't trip over the ``extends`` keyword inside a generic bound."""
    idx = signature.find(name + "<")
    if idx < 0:
        return signature
    start = idx + len(name)
    depth, i = 0, start
    while i < len(signature):
        if signature[i] == "<":
            depth += 1
        elif signature[i] == ">":
            depth -= 1
            if depth == 0:
                return signature[:start] + signature[i + 1 :]
        i += 1
    return signature


def _split_top_level(raw: str) -> list[str]:
    depth, current, parts = 0, "", []
    for ch in raw:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
            continue
        current += ch
    parts.append(current.strip())
    return [re.sub(r"<.*", "", p).strip() for p in parts if p.strip()]


def _supertypes(signature: str, name: str) -> list[str]:
    """Supertypes from the ``extends``/``implements`` clauses (generics removed)."""
    sig = _strip_own_generics(signature, name)
    types: list[str] = []
    em = re.search(r"\bextends\s+(.+?)(?:\s+implements\b|$)", sig)
    if em:
        types += _split_top_level(em.group(1))
    im = re.search(r"\bimplements\s+(.+)$", sig)
    if im:
        types += _split_top_level(im.group(1))
    return types


def extract(repo_root: Path) -> list[Node]:
    base = repo_root / MARKER_REL
    nodes: list[Node] = []
    for path in sorted(base.rglob("*.java")):
        source = path.read_text(encoding="utf-8")
        decl = _DECL_RE.search(source)
        if not decl:
            continue
        kind, name = decl.group(1), decl.group(2)
        signature = _signature(source, decl.start())
        category = _category(path)

        javadoc = source[: decl.start()]
        last_doc = javadoc.rfind("/**")
        description = _first_sentence(javadoc[last_doc:]) if last_doc >= 0 else ""
        contract = _javadoc_markdown(javadoc[last_doc:]) if last_doc >= 0 else ""

        masked = _mask(source)
        no_comments = _mask(source, literals=False)
        body_start = masked.index("{", decl.start())
        methods = _members(no_comments[body_start + 1 :], masked[body_start + 1 :], name)

        is_annotation = kind == "@interface"
        title = _display_title(name, signature)
        extends = _supertypes(signature, name)

        fm = {
            "type": "Marker",
            "title": title,
            "category": category,
            "kind": "annotation" if is_annotation else ("class" if kind == "class" else "interface"),
            "signature": signature,
        }
        pkg = _PACKAGE_RE.search(source)
        if pkg:
            fm["package"] = pkg.group(1)
        generics = _type_parameters(signature)
        if generics:
            fm["generics"] = generics
        if kind == "class":
            fm["modifiers"] = _modifiers(signature)
        if extends:
            fm["extends"] = extends
        if methods:
            fm["methods"] = methods
        rel = path.relative_to(repo_root).as_posix()
        fm["resource"] = rel
        fm["tags"] = [category, "marker"]

        node = Node(
            path=f"marker/{category}/{slugify(name)}.md",
            frontmatter=fm,
            body=contract or description or f"Marker for {name}.",
            meta={"name": name, "kind": "marker", "extends": extends},
        )
        nodes.append(node)
    return nodes

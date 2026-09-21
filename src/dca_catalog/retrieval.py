"""Deterministic retrieval artifacts: compact index, evidence slices and provenance manifest."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from .mirror import strip_resource
from .okf import Node, slugify


def evidence_slices(nodes: list[Node], threshold: int = 16_000) -> list[Node]:
    """Keep the complete node; expose its fence-aware level-three sections separately."""
    result = []
    for node in nodes:
        if len(node.render().encode()) <= threshold:
            continue
        chunks, current, heading, fenced = [], [], "Overview", False
        for line in node.body.splitlines(keepends=True):
            if line.lstrip().startswith(("```", "~~~")):
                fenced = not fenced
            if not fenced and line.startswith("### "):
                if current:
                    chunks.append((heading, "".join(current)))
                heading, current = line[4:].strip(), []
            current.append(line)
        if current:
            chunks.append((heading, "".join(current)))
        names = {}
        targets = []
        for heading, body in chunks:
            stem = slugify(heading) or "overview"
            occurrence = names.get(stem, 0)
            names[stem] = occurrence + 1
            slug = stem + (f"-{occurrence}" if occurrence else "")
            anchor_slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
            anchor = "" if heading == "Overview" else "#" + anchor_slug + (f"-{occurrence}" if occurrence else "")
            path = "evidence/" + node.path.removesuffix(".md") + "/" + slug + ".md"
            result.append(Node(path, {
                "type": "Reference", "title": f"{node.frontmatter['title']} — {heading}",
                "tags": ["reference"], "evidence_for": "/" + node.path + anchor,
            }, f"[Full node and context](/{node.path}{anchor}). This is an evidence excerpt; retain the parent selection and caveats.\n\n" + body))
            targets.append((heading, "/" + path))
        node.add_section("Evidence slices", targets)
    return result


def compact_index(nodes: list[Node]) -> str:
    def excerpt(value: str) -> str:
        text = " ".join(value.split())
        return (text[:237] + "…" if len(text) > 240 else text).replace("|", "\\|")
    lines = ["# Compact rule lookup", "", "Look up the id first. Excerpts route retrieval; read the full selection/check and language evidence before applying a rule.", "", "| Id | Title | Selects (excerpt) | Checks (excerpt) | Languages | Status |", "|---|---|---|---|---|---|"]
    for node in sorted((n for n in nodes if n.frontmatter.get("type") == "Rule"), key=lambda n: n.frontmatter["id"]):
        fm = node.frontmatter
        lines.append(f"| [{fm['id']}](/{'/'.join(node.path.split('/'))}) | {excerpt(fm['title'])} | {excerpt(fm['selects'])} | {excerpt(fm['checks'])} | {', '.join(fm['implementations'])} | {fm['status']} |")
    lines.extend(["", "[Retired ids and replacements](/rule/retired.md)", ""] if any(n.path == "rule/retired.md" for n in nodes) else [""])
    return "\n".join(lines)


def bundle_digest(bundle: Path) -> str:
    """SHA256 of sorted path/NUL/content/NUL; resource frontmatter normalized for mirrors."""
    digest = hashlib.sha256()
    for path in sorted(p for p in bundle.rglob("*") if p.is_file() and p.name != "manifest.json"):
        content = path.read_bytes()
        if path.suffix == ".md":
            content = strip_resource(content.decode()).encode()
        digest.update(path.relative_to(bundle).as_posix().encode() + b"\0" + content + b"\0")
    return digest.hexdigest()


def _revision(path: Path, files: list[Path]) -> str | None:
    # A generated-output commit must not invalidate its own manifest.
    if not files:
        return None
    result = subprocess.run(["git", "-C", str(path), "log", "-1", "--format=%H", "--",
                             *(p.relative_to(path).as_posix() for p in files)], capture_output=True, text=True)
    return result.stdout.strip() or None if result.returncode == 0 else None


def _dirty(path: Path, files: list[Path]) -> bool:
    """Whether any file the generator read is uncommitted.

    The revision alone is not a snapshot claim: a bundle generated from a dirty tree names a commit
    that does not contain the content it was built from. The content digest is still correct, but a
    reader who checks out the revision to see what a rule does gets different code. Recording it
    makes that caveat machine-readable instead of a sentence in SPEC.md.
    """
    if not files:
        return False
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain", "--",
                             *(p.relative_to(path).as_posix() for p in files)], capture_output=True, text=True)
    return bool(result.stdout.strip()) if result.returncode == 0 else False


def write_manifest(repo_root: Path, bundle: Path, counts: dict[str, int]) -> None:
    from .docs import _SKIP, _is_content
    sources = {}
    # Only files the generator actually reads: a commit elsewhere in these repositories must not move the manifest.
    inputs = {
        "dca-guide": ["**/*.md"],
        "dca-java": ["dca-building-blocks/src/main/**/*.java", "dca-archunit/src/main/**/*.java", "rules.json", "gradle.properties"],
        "dca-dotnet": ["src/DomainCentric.ArchRules/**/*.cs", "src/*/*.csproj", "rules.json"],
        "dca-knowledge-catalog": ["src/**/*.py", "authored/**/*.md"],
    }
    for name, patterns in inputs.items():
        repo = repo_root / name
        if not repo.exists():
            continue
        files = sorted({p for pattern in patterns for p in repo.glob(pattern)
                        if p.is_file() and not {"bin", "obj", "__pycache__"}.intersection(p.parts)
                        and not (name == "dca-guide" and (p.name in _SKIP or not _is_content(p, repo)))})
        digest = hashlib.sha256()
        for path in files:
            digest.update(path.relative_to(repo).as_posix().encode() + b"\0" + path.read_bytes() + b"\0")
        entry = {"revision": _revision(repo, files), "source_sha256": digest.hexdigest()}
        if _dirty(repo, files):
            entry["dirty"] = True
        if name == "dca-knowledge-catalog":
            # The bundle is committed into this very repository: the commit that carries the manifest cannot be
            # named by the manifest, and the last input-touching commit would move as soon as sources and bundle
            # land together (the freshness gate would then reject the commit). Content digest only.
            entry = {"revision": None, "source_sha256": digest.hexdigest(),
                     "note": "own repository: the carrying commit is the revision; content digest only"}
        sources[name] = entry
    versions = {}
    props = repo_root / "dca-java/gradle.properties"
    if props.exists():
        versions["java"] = dict(re.findall(r"^(\w*Version)=(.+)$", props.read_text(), re.M))
    versions["dotnet"] = {}
    for path in sorted((repo_root / "dca-dotnet/src").glob("*/*.csproj")):
        match = re.search(r"<Version>([^<]+)</Version>", path.read_text())
        if match:
            versions["dotnet"][path.stem] = match[1]
    manifest = {"format": "dca-bundle-manifest-v1", "digest_algorithm": "sha256:sorted-path-NUL-resource-normalized-content-NUL", "bundle_sha256": bundle_digest(bundle), "sources": sources, "library_versions": versions, "counts": dict(sorted(counts.items()))}
    (bundle / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

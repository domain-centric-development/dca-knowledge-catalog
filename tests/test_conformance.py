"""OKF conformance + content tests for the generated bundle.

Regenerates the bundle into a temp dir and validates it against the OKF spec
and the catalog's own invariants. Also asserts idempotence (deterministic output).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from dca_catalog import docs, generate, lint, obsidian, process
from dca_catalog.okf import RESERVED

# tests/test_conformance.py -> tests -> dca-knowledge-catalog -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def bundle(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("bundle")
    generate.generate(REPO_ROOT, out)
    return out


def _split_frontmatter(text: str) -> tuple[dict, str]:
    assert text.startswith("---\n"), "missing frontmatter"
    _, fm_block, body = text.split("---\n", 2)
    fm: dict = {}
    for line in fm_block.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm, body


def _concept_files(bundle: Path) -> list[Path]:
    return [p for p in bundle.rglob("*.md") if p.name not in RESERVED]


def test_counts(bundle: Path):
    types: dict[str, int] = {}
    for p in _concept_files(bundle):
        fm, _ = _split_frontmatter(p.read_text(encoding="utf-8"))
        types[fm["type"]] = types.get(fm["type"], 0) + 1
    # skeleton from dca-java (building blocks + rule library) plus the .NET-only rules of
    # dca-dotnet (DCA-NET) — exact (regression guard)
    assert types["Marker"] == 29
    assert types["Rule"] == 120
    assert types["Process"] == 1
    assert types["Reference"] == 2
    # the book and the sample's ADRs are deliberately not in the bundle
    assert "Chapter" not in types
    assert "ADR" not in types
    # guide full text — lower bounds (content evolves)
    assert types.get("Guide", 0) >= 10
    assert types.get("Section", 0) >= 100


def test_every_concept_has_nonempty_type(bundle: Path):
    for p in _concept_files(bundle):
        fm, _ = _split_frontmatter(p.read_text(encoding="utf-8"))
        assert fm.get("type"), f"{p} has no type"


def test_required_fields_per_type(bundle: Path):
    for p in _concept_files(bundle):
        fm, _ = _split_frontmatter(p.read_text(encoding="utf-8"))
        t = fm["type"]
        if t == "Marker":
            assert fm.get("signature"), f"{p} marker missing signature"
        elif t == "Rule":
            assert fm.get("rule"), f"{p} rule missing rule"
            assert fm.get("constraint"), f"{p} rule missing constraint"
            assert fm.get("enforced_by"), f"{p} rule missing enforced_by"
        elif t in ("Guide", "Section"):
            assert fm.get("title"), f"{p} {t} missing title"
            assert fm.get("source") == "guide", f"{p} {t} bad source"


def test_reserved_indexes_present(bundle: Path):
    assert (bundle / "index.md").exists()
    assert (bundle / "log.md").exists()
    # every directory containing concepts has an index.md
    dirs = {p.parent for p in _concept_files(bundle)}
    for d in dirs:
        assert (d / "index.md").exists(), f"missing index.md in {d}"


def test_bundle_relative_links_resolve(bundle: Path):
    # Only validate links into our own top-level dirs; copied guide prose may
    # carry unrelated absolute links that are not part of the OKF graph.
    prefixes = ("/guide/", "/marker/", "/rule/", "/process/", "/reference/")
    link_re = re.compile(r"\]\((/[^)]+)\)")
    broken = []
    for p in bundle.rglob("*.md"):
        for target in link_re.findall(p.read_text(encoding="utf-8")):
            if target.startswith(prefixes) and not (bundle / target.lstrip("/")).exists():
                broken.append((str(p.relative_to(bundle)), target))
    assert not broken, f"broken bundle-relative links: {broken}"


def test_relative_links_are_rewritten_onto_bundle_nodes(bundle: Path):
    """Verbatim guide text carries source-relative links; they must be rewritten.

    A leftover means the guide links a document the bundle has no node for —
    e.g. the book, which is not a source and not public. Fix the guide, not this.
    """
    link_re = re.compile(r"\]\((?!/|\w+:|#)([^)\s#]+\.md)(#[^)\s]*)?\)")
    dangling = []
    for p in bundle.rglob("*.md"):
        for target, _anchor in link_re.findall(p.read_text(encoding="utf-8")):
            if not (p.parent / target).exists():
                dangling.append((str(p.relative_to(bundle)), target))

    assert not dangling, f"unrewritten relative links: {dangling}"


def test_adr_template_links_land_on_the_process_node(bundle: Path):
    # the template is _SKIPped as a Guide, but the bundle has it as a Process node
    text = (bundle / "guide" / "readme" / "quick-navigation.md").read_text(encoding="utf-8")
    assert f"](/{process.NODE_PATH})" in text


def test_anchored_links_resolve_to_the_section_node(bundle: Path):
    # H2 anchor -> that section's node; sub-heading anchor -> its enclosing section
    text = (bundle / "guide" / "spring-modulith" / "core-concepts.md").read_text(encoding="utf-8")
    assert "](/guide/readme/java-package-structure.md)" in text

    # dialect divergence: GitHub keeps the '&' spacing as '--', slugify collapses it
    refs = (bundle / "guide" / "clean-architecture-comparison" / "key-references.md")
    assert "](/guide/readme/references-further-reading.md)" in refs.read_text(encoding="utf-8")


def test_rewrite_leaves_code_alone_and_handles_backticked_link_text(tmp_path):
    guide = tmp_path / docs.GUIDE_REL
    guide.mkdir(parents=True)
    (guide / "README.md").write_text("# Main\n\n## Packaging Rules\n\nrules.\n", encoding="utf-8")
    (guide / "other.md").write_text(
        "# Other\n\n## Links\n\n"
        "See [`README.md`](README.md) and [rules](./README.md#packaging-rules).\n\n"
        "```\nsee [x](./README.md)\n```\n\n"
        "Inline `[y](./README.md)` stays.\n",
        encoding="utf-8",
    )

    body = next(n for n in docs.extract(tmp_path) if n.path == "guide/other/links.md").body
    assert "[`README.md`](/guide/readme.md)" in body, "backticked link text broke the rewrite"
    assert "[rules](/guide/readme/packaging-rules.md)" in body
    assert "see [x](./README.md)" in body, "rewrote inside a code fence"
    assert "`[y](./README.md)`" in body, "rewrote inside an inline code span"


def test_process_node_carries_the_fillable_adr_template(bundle: Path):
    """The knowledge base must hand out the template itself, not just describe it.

    ``template/`` is the authored zone, so the copyable text lives in the generated
    Process node — sourced from adr-template.md, hence never stale.
    """
    text = (bundle / process.NODE_PATH).read_text(encoding="utf-8")
    assert "## The template" in text
    fenced = text.split("## The template", 1)[1]
    assert "````markdown" in fenced, "template not wrapped in a longer fence than its own"
    assert fenced.count("````") == 2, "unbalanced wrapper fence"
    for heading in ("# ADR-NNN:", "## Context", "## Decision", "## Consequences"):
        assert heading in fenced, f"template missing {heading}"
    # the meta sections are distilled into Steps/When-to-write, not duplicated
    assert "## Template Metadata" not in fenced


def test_bundle_never_links_out_to_a_sibling_project(bundle: Path):
    """The catalog stands on its own: it is *generated from* the guide and the
    sample, and must not link back at either (nor at the non-public book)."""
    outward = re.compile(r"\]\([^)]*(dca-ecommerce-sample|dca-book|dca-guide)[^)]*\)")
    hits = []
    for p in bundle.rglob("*.md"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if outward.search(line):
                hits.append((str(p.relative_to(bundle)), line.strip()[:80]))
    assert not hits, f"links out of the bundle: {hits}"


def test_bundle_never_cites_specific_adr_records(bundle: Path):
    """A reader building their own application has no ADR-0xx files, so a citation
    would point at nothing. Only the Process node (built from the ADR template) may
    carry ADR numbers — they are fictional examples teaching the practice. A hit
    means a *source* (guide text, marker javadoc, ArchUnit `.because()`) acquired
    an ADR reference: fix it there."""
    adr_ref = re.compile(r"ADR-\d+")
    hits = []
    for zone in ("guide", "marker", "rule"):
        for p in (bundle / zone).rglob("*.md"):
            for line in p.read_text(encoding="utf-8").splitlines():
                if adr_ref.search(line):
                    hits.append((str(p.relative_to(bundle)), line.strip()[:80]))
    assert not hits, f"ADR citations in the bundle: {hits}"


def test_bundle_is_tool_agnostic():
    """The catalog is pure doctrine — how DCA is used, enforced by markers and
    ArchUnit — for *any* LLM or harness. Tooling (Claude Code, the dca-core
    plugin, slash commands) consumes the graph; the graph never mentions the
    tooling. Scans the committed bundle so authored extensible-zone nodes are
    covered too (the generated fixture would miss them)."""
    committed = Path(__file__).resolve().parents[1] / "bundle"
    tool_ref = re.compile(r"claude|dca-core|dca-marketplace|slash command|plugin skill|/dca-\w", re.IGNORECASE)
    hits = []
    for p in committed.rglob("*.md"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("resource: "):
                continue  # provenance path (e.g. dca-java/dca-building-blocks/...), not tooling
            if tool_ref.search(line):
                hits.append((str(p.relative_to(committed)), line.strip()[:80]))
    assert not hits, f"tool-specific references in the bundle: {hits}"


def test_mirror_drops_the_resource_frontmatter(tmp_path):
    """The vendored copy ships to projects that do not have the source repos, so
    a ``resource:`` path there points at nothing. The canonical bundle keeps it."""
    out = tmp_path / "bundle"
    generate.generate(REPO_ROOT, out)
    assert any("\nresource:" in p.read_text(encoding="utf-8") for p in out.rglob("*.md"))

    mirror = tmp_path / "mirror"
    generate._mirror(out, [mirror])
    for p in mirror.rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        front = text.split("\n---\n", 1)[0] if text.startswith("---\n") else ""
        assert "resource:" not in front, f"{p} still carries resource:"

    # body text is untouched — a YAML example in a fence keeps its resource: line
    node = mirror / "note" / "_fence.md"
    node.write_text("---\ntype: Note\nresource: x\n---\n\n```yaml\nresource: keep-me\n```\n", encoding="utf-8")
    assert "resource: keep-me" in generate._strip_resource(node.read_text(encoding="utf-8"))
    assert "\nresource: x" not in generate._strip_resource(node.read_text(encoding="utf-8"))


def test_mirror_cli_resolves_local_and_git_sources(tmp_path):
    """``dca_catalog.mirror`` is the consumer-facing entry point: it mirrors an
    already-built bundle (no source repos needed) from a local bundle dir, a
    local catalog repo, or a git URL into another project."""
    import subprocess

    from dca_catalog import mirror

    repo = tmp_path / "src-repo"
    (repo / "bundle").mkdir(parents=True)
    (repo / "bundle" / "index.md").write_text("# root\n", encoding="utf-8")
    (repo / "bundle" / "node.md").write_text(
        "---\ntype: Note\ntitle: N\nresource: gone\n---\n\nbody\n", encoding="utf-8"
    )

    # local catalog repo (bundle/ inside)
    dest = tmp_path / "via-repo"
    assert mirror.main(["--from", str(repo), "--to", str(dest)]) == 0
    assert (dest / "index.md").exists()
    assert "resource:" not in (dest / "node.md").read_text(encoding="utf-8")

    # local bundle dir directly
    dest2 = tmp_path / "via-bundle"
    assert mirror.main(["--from", str(repo / "bundle"), "--to", str(dest2)]) == 0
    assert (dest2 / "node.md").exists()

    # git URL (shallow clone of a local file:// repo)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x"],
        cwd=repo, check=True,
    )
    dest3 = tmp_path / "via-git"
    assert mirror.main(["--from", f"file://{repo}", "--to", str(dest3)]) == 0
    assert (dest3 / "index.md").exists()
    assert "resource:" not in (dest3 / "node.md").read_text(encoding="utf-8")


def test_no_links_into_removed_zones(bundle: Path):
    """The resolve check above only sees prefixes it knows about, so a link into
    a dir that left ``_GENERATED_DIRS`` would be dangling *and* invisible."""
    gone = []
    for p in bundle.rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        for prefix in ("](/book/", "](/adr/"):
            if prefix in text:
                gone.append((str(p.relative_to(bundle)), prefix))
    assert not gone, f"links into removed zones: {gone}"


def test_extensible_dirs_scaffolded(bundle: Path):
    # the authored zone is always present and discoverable, even when empty
    for name in ("recipe", "decision", "pitfall", "template", "note"):
        assert (bundle / name).is_dir(), f"missing extensible dir {name}"
        assert (bundle / name / "index.md").exists(), f"missing {name}/index.md"


def test_extensible_zone_survives_regeneration(tmp_path):
    out = tmp_path / "bundle"
    generate.generate(REPO_ROOT, out)

    authored = out / "note" / "_survives.md"
    authored.write_text(
        "---\ntype: Note\ntitle: Survivor\ntags: [note]\n---\n\n"
        "Authored node. Links [IntegrationEvent](/marker/tactical/integrationevent.md).\n",
        encoding="utf-8",
    )

    counts = generate.generate(REPO_ROOT, out)  # regenerate over the same dir

    assert authored.exists(), "authored extensible-zone node was wiped by regeneration"
    assert counts.get("Note") == 1, "authored node not counted"
    assert "Survivor" in (out / "note" / "index.md").read_text(), "authored node not catalogued"
    # generated zone still rebuilt correctly alongside it
    assert (out / "marker" / "tactical" / "integrationevent.md").exists()


def test_lint_clean(bundle: Path):
    findings = lint.lint(bundle, REPO_ROOT)
    errors = [f for f in findings if f[0] == "ERROR"]
    assert not errors, f"lint ERRORs in generated bundle: {errors}"
    warns = [f for f in findings if f[0] == "WARN"]
    assert not warns, f"lint WARNs in generated bundle: {warns}"


def test_lint_catches_problems(tmp_path):
    bundle = tmp_path / "b"
    (bundle / "marker").mkdir(parents=True)
    (bundle / "note").mkdir()
    (bundle / "marker" / "x.md").write_text(
        "---\ntype: Marker\ntitle: X\nresource: dca-java/GONE.java\n---\n\n"
        "broken [link](/rule/nope/none.md)\n",
        encoding="utf-8",
    )
    (bundle / "note" / "floating.md").write_text(
        "---\ntype: Note\ntitle: Floating\n---\n\nno skeleton link\n", encoding="utf-8"
    )
    kinds = {f[1] for f in lint.lint(bundle, REPO_ROOT)}
    assert {"broken-link", "stale-resource", "unanchored-authored", "orphan"} <= kinds


def test_obsidian_export_rewrites_links(bundle: Path, tmp_path):
    graph_dirs = ("guide", "marker", "rule", "process", "reference",
                  "recipe", "decision", "pitfall", "template", "note")
    leading = re.compile(r"\]\((/(?:" + "|".join(graph_dirs) + r")/[^)]+)\)")

    # unit: leading-slash graph links become file-relative, others untouched
    src = "see [a](/marker/x.md) and [ext](/other/y) and [b](/rule/z.md)"
    rewritten = obsidian._rewrite(src, "note/n.md")
    assert "](../marker/x.md)" in rewritten and "](../rule/z.md)" in rewritten
    assert "](/other/y)" in rewritten  # non-graph absolute link left alone

    out = tmp_path / "vault"
    obsidian.export(bundle, out)

    # a generated node with cross-links (present in the fixture build)
    node_rel = "marker/port-out/repository.md"
    # canonical bundle keeps OKF leading-slash links (export is non-destructive)
    assert leading.search((bundle / node_rel).read_text())

    # export: zero leading-slash graph links remain anywhere
    for p in out.rglob("*.md"):
        assert not leading.search(p.read_text(encoding="utf-8")), f"{p} still leading-slash"

    # spot-check: that node's rewritten graph links resolve on disk
    node = out / node_rel
    rel = re.compile(r"\]\(((?:\.\./)+(?:guide|marker|rule|process)/[^)]+\.md)\)")
    targets = rel.findall(node.read_text(encoding="utf-8"))
    assert targets, "expected rewritten relative graph links"
    for target in targets:
        assert (node.parent / target).resolve().exists(), f"unresolved: {target}"
    assert (out / ".obsidian" / "app.json").exists()


def test_marker_discussed_in(bundle: Path):
    # reverse edge: markers link the sections that primarily discuss them
    text = (bundle / "marker" / "port-out" / "repository.md").read_text(encoding="utf-8")
    assert "## Discussed in" in text
    links = re.findall(r"\]\((/guide/[^)]+\.md)\)",
                       text.split("## Discussed in", 1)[1])
    assert 0 < len(links) <= 10, f"expected 1..10 discussed-in links, got {len(links)}"
    for target in links:
        assert (bundle / target.lstrip("/")).exists(), f"unresolved: {target}"


def test_obsidian_roundtrip_is_noop(bundle: Path, tmp_path):
    # export then import with no edits must leave the bundle byte-identical
    import shutil

    b = tmp_path / "b"
    shutil.copytree(bundle, b)
    authored = b / "note" / "roundtrip.md"
    authored.write_text(
        "---\ntype: Note\ntitle: \"Roundtrip\"\ntags: [note]\n---\n\n"
        "Links [Repository](/marker/port-out/repository.md).\n",
        encoding="utf-8",
    )
    before = {p.relative_to(b).as_posix(): p.read_text(encoding="utf-8")
              for p in b.rglob("*.md")}

    vault = tmp_path / "vault"
    obsidian.export(b, vault)
    changed, problems = obsidian.import_back(vault, b)

    assert changed == 0, "no-edit roundtrip wrote files back"
    assert not [m for m in problems if "REJECTED" in m]
    after = {p.relative_to(b).as_posix(): p.read_text(encoding="utf-8")
             for p in b.rglob("*.md")}
    assert before == after, "roundtrip changed the canonical bundle"

    # export injects an alias line; the canonical node has none
    assert 'aliases: ["Roundtrip"]' in (vault / "note" / "roundtrip.md").read_text()
    assert "aliases:" not in authored.read_text()


def test_obsidian_import_authored_edit(bundle: Path, tmp_path):
    import shutil

    b = tmp_path / "b"
    shutil.copytree(bundle, b)
    vault = tmp_path / "vault"
    obsidian.export(b, vault)

    # authored in the vault: wikilink + relative link + missing-type reject
    (vault / "note" / "from-vault.md").write_text(
        "---\ntype: Note\ntitle: \"From Vault\"\ntags: [note]\n---\n\n"
        "See [[usecase|the marker]] and [process](../process/index.md).\n",
        encoding="utf-8",
    )
    (vault / "note" / "no-type.md").write_text(
        "---\ntitle: Broken\n---\n\nbody\n", encoding="utf-8"
    )
    # generated-zone edit must be ignored
    gen = vault / "marker" / "port-out" / "repository.md"
    gen.write_text(gen.read_text(encoding="utf-8") + "\nHACK\n", encoding="utf-8")

    changed, problems = obsidian.import_back(vault, b)

    imported = (b / "note" / "from-vault.md").read_text(encoding="utf-8")
    assert "[the marker](/marker/port-in/usecase.md)" in imported  # wikilink converted
    assert "](/process/index.md)" in imported  # relative -> bundle-relative
    assert changed == 1
    assert not (b / "note" / "no-type.md").exists()
    assert any("no-type.md" in m and "REJECTED" in m for m in problems)
    assert any("repository.md" in m and "generated zone" in m for m in problems)
    assert "HACK" not in (b / "marker" / "port-out" / "repository.md").read_text()


def test_root_index_router_line(bundle: Path, tmp_path):
    import shutil

    b = tmp_path / "b"
    shutil.copytree(bundle, b)
    assert "Building something?" not in (b / "index.md").read_text()
    (b / "recipe" / "build-a-dca-application.md").write_text(
        "---\ntype: Recipe\ntitle: \"Build a DCA application\"\ntags: [recipe, bootstrap]\n---\n\n"
        "Router. [UseCase](/marker/port-in/usecase.md)\n",
        encoding="utf-8",
    )
    generate.generate(REPO_ROOT, b)
    root = (b / "index.md").read_text(encoding="utf-8")
    assert "Building something?" in root
    assert "(recipe/build-a-dca-application.md)" in root


def test_lint_flags_unknown_tag(tmp_path):
    b = tmp_path / "b"
    (b / "marker").mkdir(parents=True)
    (b / "note").mkdir()
    (b / "marker" / "x.md").write_text(
        "---\ntype: Marker\ntitle: X\n---\n\nok\n", encoding="utf-8"
    )
    (b / "note" / "tagged.md").write_text(
        "---\ntype: Note\ntitle: T\ntags: [note, made-up-synonym]\n---\n\n"
        "[x](/marker/x.md)\n",
        encoding="utf-8",
    )
    findings = lint.lint(b, REPO_ROOT)
    assert any(k == "unknown-tag" and "made-up-synonym" in d for _s, k, _r, d in findings)
    assert not any(k == "unknown-tag" and "'note'" in d for _s, k, _r, d in findings)


def test_idempotent(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    generate.generate(REPO_ROOT, a)
    generate.generate(REPO_ROOT, b)
    files_a = sorted(p.relative_to(a).as_posix() for p in a.rglob("*.md"))
    files_b = sorted(p.relative_to(b).as_posix() for p in b.rglob("*.md"))
    assert files_a == files_b
    for rel in files_a:
        assert (a / rel).read_text() == (b / rel).read_text(), f"non-deterministic: {rel}"


# --- marker method extraction -------------------------------------------------

_METHOD_HEADER = re.compile(
    r"^(?:(?:public|protected|default|static|abstract)\s+)*(?:<[^>]+>\s+)?"
    r"[\w.<>\[\],? ]+?\s+\w+\([^()]*\)(?: default .+)?$"
)

_MARKER_ORACLE = {
    "tactical/baseaggregateroot.md": [
        "public void registerEvent(DomainEvent event)",
        "public List<DomainEvent> domainEvents()",
        "public void clearDomainEvents()",
    ],
    "tactical/entity.md": ["ID id()", "default boolean sameIdentityAs(T other)"],
    "application/transactionboundary.md": [
        "<T> T inTransaction(Supplier<T> work)",
        "default void inTransaction(Runnable work)",
    ],
    "strategic/externalupstream.md": [
        "String name()",
        "Upstream.Translation translation()",
        "Interaction interaction()",
        "String[] contractPackages() default {}",
        'String protocol() default ""',
        'String exchanges() default ""',
        'String rationale() default ""',
        "Upstream.Status status() default Upstream.Status.IMPLEMENTED",
    ],
}


def _marker_methods(bundle: Path, rel: str) -> list[str]:
    fm, _ = _split_frontmatter((bundle / "marker" / rel).read_text(encoding="utf-8"))
    raw = fm.get("methods", "")
    assert raw.startswith("[") and raw.endswith("]"), f"{rel}: methods not a list: {raw!r}"
    import json

    return json.loads(raw)


def test_marker_methods_oracle(bundle: Path):
    """Class methods, default methods and annotation-element defaults are extracted
    as declared — the three nodes the regex extractor got wrong, plus the annotation
    with an array default."""
    for rel, expected in _MARKER_ORACLE.items():
        assert _marker_methods(bundle, rel) == expected, rel


def test_marker_methods_are_headers_not_body_fragments(bundle: Path):
    for p in (bundle / "marker").rglob("*.md"):
        if p.name == "index.md":
            continue
        fm, _ = _split_frontmatter(p.read_text(encoding="utf-8"))
        if "methods" not in fm:
            continue
        for m in _marker_methods(bundle, p.relative_to(bundle / "marker").as_posix()):
            assert _METHOD_HEADER.match(m), f"{p.name}: not a method header: {m!r}"
            for forbidden in ("throw ", "return ", "/*", "*/", "@"):
                assert forbidden not in m, f"{p.name}: body fragment leaked: {m!r}"


def test_marker_method_count_matches_source(bundle: Path):
    """Independent count: in google-java-format output every member of a top-level
    type starts at two-space indentation. Count the 2-space-indented, comment-free
    lines that open a non-private, non-constructor member with a parameter list and
    compare with what the scanner extracted — a method the scanner drops or invents
    shows up as a mismatch."""
    from dca_catalog import markers

    base = REPO_ROOT / markers.MARKER_REL
    member_line = re.compile(r"^  (?![ @/*}])(?!private\b)(?!(?:class|interface|enum|record)\b).*\w+\(.*", re.M)
    checked = 0
    for src_path in sorted(base.rglob("*.java")):
        source = src_path.read_text(encoding="utf-8")
        decl = markers._DECL_RE.search(source)
        if not decl:
            continue
        name = decl.group(2)
        body = markers._mask(source, literals=False)[source.index("{", decl.start()) + 1 :]
        # only the outermost body: drop nested type bodies by indentation (4+ spaces stay, 2-space '}' ends nested type)
        expected = 0
        nested = False
        for line in body.splitlines():
            if re.match(r"^  (?:public |protected |static )*(?:@interface|interface|class|enum|record)\b", line):
                nested = True
            elif nested and line.startswith("  }"):
                nested = False
            elif not nested and member_line.match(line) and not re.match(rf"^  (?:public |protected )?{name}\(", line):
                expected += 1
        node = next(bundle.joinpath("marker").rglob(f"{markers.slugify(name)}.md"), None)
        assert node is not None, f"no node for {name}"
        fm, _ = _split_frontmatter(node.read_text(encoding="utf-8"))
        got = len(_marker_methods(bundle, node.relative_to(bundle / "marker").as_posix())) if "methods" in fm else 0
        assert got == expected, f"{name}: scanner {got} vs source {expected}"
        checked += 1
    assert checked >= 20


# --- rule mechanics ----------------------------------------------------------------


def _rule_files(bundle: Path) -> list[Path]:
    return [p for p in (bundle / "rule").rglob("*.md") if p.name != "index.md"]


def test_every_rule_node_describes_selection_and_check(bundle: Path):
    """Decision: the two mechanics texts are mandatory for every rule, so a reader can
    predict from the node alone whether a rule applies and what it will say."""
    for p in _rule_files(bundle):
        fm, body = _split_frontmatter(p.read_text(encoding="utf-8"))
        assert fm.get("selects", "").strip(), f"{p.name}: no selects"
        assert fm.get("checks", "").strip(), f"{p.name}: no checks"
        assert "## Selection" in body and "## Check" in body, f"{p.name}: body lacks Selection/Check"


def test_rule_nodes_embed_referenced_helpers(bundle: Path):
    """Every helper method the implementation block calls that the rule class (or a
    shared helper class of the rules package) defines appears as a `### ...` block in
    the node — nobody should need the sources jar to see what `publishAfterSaving()`
    does."""
    from dca_catalog import rules

    src_dir = REPO_ROOT / rules.RULES_SRC_REL
    class_sources = {p.stem: p.read_text(encoding="utf-8") for p in src_dir.glob("*.java")}
    checked = 0
    for p in _rule_files(bundle):
        fm, body = _split_frontmatter(p.read_text(encoding="utf-8"))
        if "java" not in fm.get("implementations", ""):
            continue
        impl = re.search(r"## Implementation\n\n```java\n(.*?)\n```", body, re.S)
        assert impl, f"{p.name}: no implementation block"
        class_name = fm["enforced_by"].strip('"').split("#")[0]
        source = class_sources[class_name]
        for name in set(rules._CALL_RE.findall(impl.group(1))):
            if name in rules._JAVA_KEYWORDS or rules._method_source(source, name) is None:
                continue
            assert f"### `{name}`" in body, f"{p.name}: helper {name}() not embedded"
            checked += 1
    assert checked >= 20, "expected many helper embeddings across the catalog"


def test_lint_flags_undescribed_rule(tmp_path: Path):
    b = tmp_path / "bundle"
    (b / "rule" / "x").mkdir(parents=True)
    (b / "rule" / "x" / "r.md").write_text(
        "---\ntype: Rule\nid: DCA-X-001\ntitle: t\nrule: r.\nconstraint: c.\nenforced_by: X#DCA-X-001\n"
        "status: enforced\nrule_set: x\nimplementations: [java]\ntags: [x]\n---\n\nbody\n",
        encoding="utf-8",
    )
    kinds = {f[1] for f in lint.lint(b, REPO_ROOT)}
    assert "undescribed-rule" in kinds


# --- reference nodes ----------------------------------------------------------------


def test_reference_nodes_render_every_setting_and_query(bundle: Path):
    """The two reference nodes are rendered from the sources: every `with*` override of
    DcaLayout, every FrameworkAnnotations.spring() name and every public method of
    DcaArchitecture must appear — a new setting or query cannot go missing silently."""
    from dca_catalog import reference

    java = REPO_ROOT / reference.JAVA_SRC_REL
    layout = (bundle / "reference" / "layout.md").read_text(encoding="utf-8")
    arch = (bundle / "reference" / "architecture.md").read_text(encoding="utf-8")

    for setter in re.findall(r"public DcaLayout (with\w+)\(", (java / "DcaLayout.java").read_text()):
        assert f"`{setter}(" in layout, f"{setter} missing from dca-layout.md"
    for fqn in re.findall(r'"(org\.springframework[\w.]+)"', (java / "FrameworkAnnotations.java").read_text()):
        assert fqn in layout, f"{fqn} missing from dca-layout.md"
    assert "`java..`" in layout and "`org.jspecify.annotations..`" in layout
    assert "`System`" in layout and "ForRootNamespace" in layout  # .NET half

    arch_src = (java / "DcaArchitecture.java").read_text()
    for name in set(re.findall(r"(?m)^  public (?:static )?[\w<>\[\],?. ]+? (\w+)\(", arch_src)):
        assert f"{name}(" in arch, f"{name}() missing from dca-architecture.md"
    assert "moduleRoots()" in arch and "AllDomainPatterns()" in arch

    for p in _rule_files(bundle):
        text = p.read_text(encoding="utf-8")
        assert "## Configured by" in text and "/reference/layout.md" in text, p.name


def test_mirror_strips_dotnet_resource():
    text = "---\ntype: Reference\nresource: a/b.java\nresource_dotnet: c/d.cs\ntags: [x]\n---\n\nbody\n"
    stripped = generate._strip_resource(text)
    assert "resource" not in stripped.split("---")[1]
    assert "body" in stripped

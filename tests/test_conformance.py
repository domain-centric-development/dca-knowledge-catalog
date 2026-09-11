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
    from dca_catalog.rules import _catalog
    java_rules, java_retired = _catalog(REPO_ROOT / "dca-java/rules.json")
    net_rules, _ = _catalog(REPO_ROOT / "dca-dotnet/rules.json")
    expected_ids = {r["id"] for r in java_rules + net_rules if r.get("status") != "n/a"}
    assert types["Rule"] == len(expected_ids)
    assert types["Process"] == 1
    assert types["Reference"] == 2 + bool(java_retired) + sum(1 for p in (bundle / "evidence").rglob("*.md") if p.name not in RESERVED)
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
            if target.startswith(prefixes) and not (bundle / target.lstrip("/").split("#", 1)[0]).exists():
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
    text = (bundle / "guide" / "readme" / "the-guide.md").read_text(encoding="utf-8")
    assert f"](/{process.NODE_PATH})" in text


def test_anchored_links_resolve_to_the_section_node(bundle: Path):
    # H2 anchor -> that section's node; sub-heading anchor -> its enclosing section
    text = (bundle / "guide" / "spring-modulith" / "core-concepts.md").read_text(encoding="utf-8")
    assert "](/guide/dependency-structure/layer-dependency-flow.md)" in text

    nested = (bundle / "guide" / "spring-modulith"
              / "progressive-complexity-for-spring-modulith-modules.md")
    assert "](/guide/package-structure/progressive-complexity-principle.md)" in nested.read_text(encoding="utf-8")


def test_anchor_dialects_agree_on_ampersand_headings(tmp_path):
    # GitHub keeps the '&' spacing as '--', slugify collapses it to one dash
    guide = tmp_path / docs.GUIDE_REL
    (guide / "architecture").mkdir(parents=True)
    (guide / "architecture" / "references.md").write_text(
        "# References\n\n## References & Further Reading\n\nbooks.\n", encoding="utf-8")
    (guide / "README.md").write_text(
        "# Main\n\n## Links\n\n"
        "See [refs](./architecture/references.md#references--further-reading).\n", encoding="utf-8")

    nodes = {n.path: n for n in docs.extract(tmp_path)}
    assert "](/guide/references/references-further-reading.md)" in nodes["guide/readme/links.md"].body


def test_a_document_in_a_subdirectory_becomes_a_guide_node(tmp_path):
    guide = tmp_path / docs.GUIDE_REL
    (guide / "topics").mkdir(parents=True)
    (guide / "README.md").write_text(
        "# Main\n\n## Links\n\nSee [modulith](./topics/spring-modulith.md#core-concepts).\n",
        encoding="utf-8")
    (guide / "topics" / "spring-modulith.md").write_text(
        "# Spring Modulith\n\n## Core Concepts\n\nmodules.\n", encoding="utf-8")

    nodes = {n.path: n for n in docs.extract(tmp_path)}
    assert nodes["guide/spring-modulith.md"].frontmatter["resource"] == "dca-guide/topics/spring-modulith.md"
    assert "](/guide/spring-modulith/core-concepts.md)" in nodes["guide/readme/links.md"].body


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
    tool_ref = re.compile(r"claude|dca-core|dca-marketplace|slash command|plugin skill|/dca-(?![a-z]+-\d{3}(?:\.md|/))\w", re.IGNORECASE)
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
    before_counts = generate.generate(REPO_ROOT, out)

    authored = out / "note" / "_survives.md"
    authored.write_text(
        "---\ntype: Note\ntitle: Survivor\ntags: [note]\n---\n\n"
        "Authored node. Links [IntegrationEvent](/marker/tactical/integrationevent.md).\n",
        encoding="utf-8",
    )

    counts = generate.generate(REPO_ROOT, out)  # regenerate over the same dir

    assert authored.exists(), "authored extensible-zone node was wiped by regeneration"
    assert counts.get("Note") == before_counts.get("Note", 0) + 1, "authored node not counted"
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
    assert "## Related mentions in guides (heuristic)" in text
    links = re.findall(r"\]\((/guide/[^)]+\.md)\)",
                       text.split("## Related mentions in guides (heuristic)", 1)[1])
    assert 0 < len(links) <= 10, f"expected 1..10 discussed-in links, got {len(links)}"
    for target in links:
        assert (bundle / target.lstrip("/").split("#", 1)[0]).exists(), f"unresolved: {target}"


def test_obsidian_roundtrip_is_noop(bundle: Path, tmp_path):
    # export then import with no edits must leave the bundle byte-identical
    import shutil

    (tmp_path / "src/dca_catalog").mkdir(parents=True)
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

    (tmp_path / "src/dca_catalog").mkdir(parents=True)
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

    assert not (b / "note" / "from-vault.md").exists()
    imported = (tmp_path / "authored/note/from-vault.md").read_text(encoding="utf-8")
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
    assert "Building something?" in (b / "index.md").read_text()  # canonical authored router is seeded
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
        "protected void registerEvent(DomainEvent event)",
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
    return [p for p in (bundle / "rule").rglob("*.md") if p.name not in RESERVED and _split_frontmatter(p.read_text())[0].get("type") == "Rule"]


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


def test_slugify_is_ascii_only():
    """File names must not depend on the file system's Unicode normalisation."""
    from dca_catalog.okf import slugify

    assert slugify("Default-Regel: Pure Domain Services (90% der Fälle)") == "default-regel-pure-domain-services-90-der-falle"
    assert slugify("Größe & Maß") == "grosse-mass"
    assert slugify("日本語 title").isascii()


def test_real_authored_bundle_survives_title_change(tmp_path, monkeypatch):
    import shutil
    from dca_catalog import rules
    canonical = REPO_ROOT / 'dca-knowledge-catalog/bundle'
    out = tmp_path / 'bundle'
    shutil.copytree(canonical, out)
    before = {p.relative_to(out): p.read_text() for name, _, _ in generate._EXTENSIBLE_ZONE
              for p in (out / name).glob('*.md') if p.name not in RESERVED}
    generate.generate(REPO_ROOT, out)
    import json
    redirects = json.loads((out / 'redirects.json').read_text())
    for relative, text in before.items():
        for old, new in redirects.items():
            text = text.replace('](/' + old + ')', '](/' + new + ')')
        assert (out / relative).read_text() == text
    original_extract = rules.extract
    def renamed(root):
        nodes = original_extract(root)
        for node in nodes:
            if node.frontmatter.get('type') == 'Rule':
                node.frontmatter['title'] = 'Revised title ' + node.frontmatter['id']
        return nodes
    monkeypatch.setattr(rules, 'extract', renamed)
    generate.generate(REPO_ROOT, out)
    assert not [f for f in lint.lint(out, REPO_ROOT) if f[0] in {'ERROR', 'WARN'}]
    snapshot = {p.relative_to(out): p.read_bytes() for p in out.rglob('*') if p.is_file()}
    generate.generate(REPO_ROOT, out)
    assert snapshot == {p.relative_to(out): p.read_bytes() for p in out.rglob('*') if p.is_file()}
    mirror = tmp_path / 'mirror'
    generate._mirror(out, [mirror])
    assert not [f for f in lint.lint(mirror, REPO_ROOT) if f[0] in {'ERROR', 'WARN'}]


@pytest.mark.parametrize('head', [
    'tags:\n  - domain', 'title: |\n  multiline', 'type: Note\ntype: Rule',
    'tags: [a,,b]', 'tags: [a,]', 'tags: [a', 'title: &alias text',
    'title: "unterminated', 'title: {nested: value}', '  title: indented',
])
def test_strict_frontmatter_rejects_unsupported_yaml(head, tmp_path):
    text = '---\n' + head + '\n---\nBody\n'
    with pytest.raises(ValueError):
        generate._parse_front(text)
    (tmp_path / 'note').mkdir()
    (tmp_path / 'note/bad.md').write_text(text)
    assert any(f[:2] == ('ERROR', 'frontmatter') for f in lint.lint(tmp_path, REPO_ROOT))


def test_frontmatter_quoted_list_roundtrip():
    from dca_catalog.okf import Node
    fm = {'type': 'Note', 'title': 'A "quote" \\ path', 'tags': ['one, two', 'three']}
    assert generate._parse_front(Node('note/test.md', fm).render())[0] == fm


def test_optional_retirement_schema(tmp_path):
    import json
    from dca_catalog import rules
    java = tmp_path / 'dca-java'
    java.mkdir()
    registry = {'rules': [], 'retired': [
        {'id': 'DCA-ADV-003', 'reason': 'Duplicate check.',
         'replacement': 'DCA-ADV-001', 'since': '0.4.0'}]}
    (java / 'rules.json').write_text(json.dumps(registry))
    nodes = rules.extract(tmp_path)
    retired = next(n for n in nodes if n.path == 'rule/retired.md')
    assert '## DCA-ADV-003' in retired.body
    assert 'DCA-ADV-001' in retired.body
    assert retired.meta['retired_ids'] == ['DCA-ADV-003']
    registry['retired'][0].pop('replacement')
    (java / 'rules.json').write_text(json.dumps(registry))
    with pytest.raises(ValueError, match='incomplete retirement'):
        rules.extract(tmp_path)


def test_explicit_status_overrides_legacy_derivation(tmp_path):
    import json
    from dca_catalog import rules
    java = tmp_path / 'dca-java'
    java.mkdir()
    (java / 'rules.json').write_text(json.dumps({'rules': [{
        'id': 'DCA-LAY-001', 'set': 'layered', 'title': 'A descriptive title',
        'rationale': 'Documentation', 'selects': 'All classes', 'checks': 'No assertion',
        'status': 'informational'}], 'retired': []}))
    node = rules.extract(tmp_path)[0]
    assert node.path == 'rule/layered/dca-lay-001.md'
    assert node.frontmatter['status'] == 'informational'
    assert node.body.startswith('# A descriptive title')


def test_retirement_migrates_existing_inbound_links(tmp_path, monkeypatch):
    import json
    import shutil
    from dca_catalog import rules
    out = tmp_path / 'bundle'
    shutil.copytree(REPO_ROOT / 'dca-knowledge-catalog/bundle', out)
    generate.generate(REPO_ROOT, out)
    real = rules.extract
    old = 'rule/advanced/dca-adv-003.md'
    (out / 'note/retirement-probe.md').write_text(
        '---\ntype: Note\ntitle: Retirement probe\ntags: [note]\n---\n'
        f'[Retiring rule](/{old})\n')
    def retiring(root):
        from dca_catalog.okf import Node
        return [n for n in real(root) if n.frontmatter.get('id') != 'DCA-ADV-003' and n.path != 'rule/retired.md'] + [Node(
            'rule/retired.md', {'type': 'Reference', 'title': 'Retired rules', 'tags': ['governance']},
            '# Retired rules\n\n## DCA-ADV-003\n\nCovered by DCA-ADV-001.\n\n## DCA-MAP-003\n\nRenderer.\n\n## DCA-TAC-022\n\nValue rules.',
            meta={'retired_ids': ['DCA-ADV-003', 'DCA-MAP-003', 'DCA-TAC-022']})]
    monkeypatch.setattr(rules, 'extract', retiring)
    generate.generate(REPO_ROOT, out)
    assert '](/rule/retired.md#dca-adv-003)' in (out / 'note/retirement-probe.md').read_text()
    assert json.loads((out / 'redirects.json').read_text())[old] == 'rule/retired.md#dca-adv-003'
    assert not [f for f in lint.lint(out, REPO_ROOT) if f[0] == 'ERROR']


def test_framework_member_metadata_roles_are_rendered_from_presets():
    from dca_catalog.reference import _framework_annotations, _framework_types
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    java = root / "dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/FrameworkAnnotations.java"
    roles, presets = _framework_annotations(java.read_text())
    assert {"injectionSite", "persistenceMapping"} <= {r for r, _ in roles}
    for name in ("spring", "jakarta", "quarkus", "micronaut"):
        assert "jakarta.inject.Inject" in presets[name]["injectionSite"]
        assert "jakarta.persistence.Column" in presets[name]["persistenceMapping"]
    assert presets["none"]["injectionSite"] == []
    assert presets["none"]["persistenceMapping"] == []
    cs = root / "dca-dotnet/src/DomainCentric.ArchRules/FrameworkTypes.cs"
    defaults = {r: v for r, v, _ in _framework_types(cs.read_text())}
    assert "System.ComponentModel.DataAnnotations.Schema" in defaults["PersistenceAttributeNamespaces"]
    assert "Microsoft.Extensions.DependencyInjection" in defaults["InjectionAttributeNamespaces"]
    assert defaults["TransactionAttributeNamespaces"] == "(empty)"
    assert defaults["ContainerAttributeNamespaces"] == "(empty)"


def test_reviewed_mapping_mentions_its_selected_marker():
    from dca_catalog.applicability import APPLIES_TO
    from dca_catalog.rules import _catalog
    entries = {r['id']: r for r in _catalog(REPO_ROOT / 'dca-java/rules.json')[0]}
    for rule_id, markers in APPLIES_TO.items():
        assert rule_id in entries
        for marker in markers:
            assert re.search(r'\b' + marker + r'\b', entries[rule_id]['selects']), (rule_id, marker)


def test_exclusion_mention_does_not_create_applicability():
    from dca_catalog import linker
    from dca_catalog.okf import Node
    marker = Node('marker/tactical/value.md', {'type': 'Marker', 'title': 'Value'}, meta={'name': 'Value'})
    rule = Node('rule/custom/dca-custom-001.md', {'type': 'Rule', 'id': 'DCA-CUSTOM-001', 'title': 'Custom', 'selects': 'Classes excluding classes assignable to Value'}, meta={'kind': 'rule', 'scan_text': 'excluding classes assignable to Value'})
    linker.link([marker], [rule])
    assert 'Applies to' not in rule.render()
    assert 'Governed by' not in marker.render()
    assert 'Related mentions (heuristic)' in rule.render()
    positive = Node('rule/tactical/dca-tac-008.md', {'type': 'Rule', 'id': 'DCA-TAC-008', 'title': 'Value boundary', 'selects': 'Types assignable to Value'}, meta={'kind': 'rule', 'scan_text': 'Value.class'})
    linker.link([marker], [positive])
    assert 'Applies to markers' in positive.render()
    assert 'Governed by' in marker.render()


def test_editorial_metadata_and_supersession(tmp_path):
    b = tmp_path / 'bundle'
    (b / 'note').mkdir(parents=True)
    (b / 'note/new.md').write_text('---\ntype: Note\ntitle: New\ntags: [note]\n---\n\nProposal.\n')
    findings = lint.lint(b, REPO_ROOT)
    assert any(f[1] == 'editorial-metadata' and f[0] == 'WARN' for f in findings)
    (b / 'note/new.md').write_text('---\ntype: Note\ntitle: New\ntags: [note]\nreview: superseded\nowner: Maintainers\nevidence: []\n---\n\nOld proposal.\n')
    assert any(f[1] == 'editorial-superseded' and f[0] == 'ERROR' for f in lint.lint(b, REPO_ROOT))
    skill_path = REPO_ROOT / 'dca-marketplace/plugins/dca-core/skills/dca-knowledge/SKILL.md'
    if not skill_path.exists():
        pytest.skip('dca-marketplace checkout not present beside the catalog (CI checks out sources only)')
    skill = skill_path.read_text()
    assert 'draft' in skill and 'superseded' in skill and 'non-normative' in skill


def test_manifest_and_compact_view_are_mirrored(bundle, tmp_path):
    import json
    from dca_catalog.retrieval import bundle_digest
    from dca_catalog.mirror import mirror_bundle
    manifest = json.loads((bundle / 'manifest.json').read_text())
    assert manifest['bundle_sha256'] == bundle_digest(bundle)
    assert manifest['sources']['dca-java']['source_sha256']
    assert manifest['library_versions']['java']['archunitVersion']
    assert 'timestamp' not in json.dumps(manifest).lower()
    mirror = tmp_path / 'mirror'
    mirror_bundle(bundle, [mirror])
    assert (mirror / 'manifest.json').read_bytes() == (bundle / 'manifest.json').read_bytes()
    assert bundle_digest(mirror) == manifest['bundle_sha256']
    compact = (bundle / 'rule/index-compact.md').read_text()
    for p in _rule_files(bundle):
        fm, _ = _split_frontmatter(p.read_text())
        assert fm['id'] in compact
    assert 'Selects (excerpt)' in compact and 'Languages' in compact


def test_all_dotnet_rules_have_extracted_csharp_evidence(bundle):
    from dca_catalog.rules import _catalog, _expression_at, _dotnet_class, DOTNET_RULES_SRC_REL
    entries = [r for r in _catalog(REPO_ROOT / 'dca-dotnet/rules.json')[0] if r.get('status') != 'n/a']
    for entry in entries:
        path = bundle / 'rule' / entry['set'] / (entry['id'].lower() + '.md')
        text = path.read_text()
        source = (REPO_ROOT / DOTNET_RULES_SRC_REL / (_dotnet_class(entry['set']) + '.cs')).read_text()
        assert _expression_at(source, entry['id'])
        assert '```csharp' in text and 'DcaRule.' in text, entry['id']
        if not entry['id'].startswith('DCA-NET-'):
            assert '## .NET reading' in text


def test_evidence_slices_keep_full_nodes_and_ignore_headings_in_code():
    from dca_catalog.okf import Node
    from dca_catalog.retrieval import evidence_slices
    body = '# Full\n\n### First\n\n' + 'long context ' * 20 + '\n```java\n### inside a code fence\n```\n\n### Second\n\nEnd.\n'
    node = Node('rule/example/test.md', {'type': 'Rule', 'title': 'Test'}, body)
    slices = evidence_slices([node], threshold=100)
    assert node.body == body
    assert len(slices) == 3  # overview and two real headings
    assert any('### inside a code fence' in s.body for s in slices)
    assert not any('inside-a-code-fence' in s.path for s in slices)
    assert all('Full node and context' in s.body for s in slices)
    assert [s.path for s in slices] == [s.path for s in evidence_slices([Node(node.path, node.frontmatter, body)], threshold=100)]


def test_templates_have_applicability_and_router_has_both_commands(bundle):
    for p in (bundle / 'template').rglob('*.md'):
        if p.name in RESERVED:
            continue
        fm, _ = _split_frontmatter(p.read_text())
        assert fm.get('applies_to') and fm.get('framework'), p.name
    router = (bundle / 'recipe/build-a-dca-application.md').read_text()
    assert './gradlew test-architecture' in router and 'dotnet test -c Debug' in router


def test_obsidian_import_refuses_read_only_mirror(bundle: Path, tmp_path):
    import shutil
    mirror = tmp_path / "mirror"
    shutil.copytree(bundle, mirror)
    vault = tmp_path / "vault"
    obsidian.export(mirror, vault)
    changed, problems = obsidian.import_back(vault, mirror)
    assert changed == 0
    assert any("REJECTED" in message and "read-only" in message for message in problems)
    assert not (tmp_path / "authored").exists()


def test_template_code_lives_in_language_children(bundle):
    """One concept node per template, one code node per language below it.

    The prose, the evidence and the links are written once; a further language is one more
    file, not a second copy of the node. Enforced here as well as in the lint so a hand-edit
    of the authored zone cannot reintroduce a Java-only node with the code inline.
    """
    concepts = {
        p for p in (bundle / 'template').glob('*.md')
        if p.name not in RESERVED and (bundle / 'template' / p.stem).is_dir()
    }
    assert concepts, 'no template concept node has language children'
    for concept in sorted(concepts):
        fm, body = _split_frontmatter(concept.read_text())
        assert '```' not in body, f'{concept.name} carries code although it has language children'
        children = sorted((bundle / 'template' / concept.stem).glob('*.md'))
        languages = set()
        for child in children:
            if child.name in RESERVED:
                continue
            child_fm, child_body = _split_frontmatter(child.read_text())
            assert child_fm.get('parent') == f'/template/{concept.stem}.md', child.name
            assert '```' in child_body, f'{child.name} is a code node without code'
            languages.update(child_fm.get('applies_to') or [])
        assert set(fm.get('applies_to') or []) == languages, concept.name


def test_cited_draft_reports_only_unreviewed_nodes(bundle: Path, tmp_path):
    """`lint --cited-by` names the authored nodes a run leaned on that are still proposals.

    Reviewing the authored zone on stock is the wrong order; what a run cites is the list worth
    reading. A node that has been reviewed must not appear, or the report becomes noise and gets
    ignored — which is the same as having no report.
    """
    from dca_catalog.lint import cited_drafts

    drafted = reviewed = None
    for path in sorted((bundle / 'decision').glob('*.md')):
        if path.name in RESERVED:
            continue
        fm, _ = _split_frontmatter(path.read_text())
        review = str(fm.get('review') or '')
        if review == 'draft' and drafted is None:
            drafted = path
        if review == 'reviewed' and reviewed is None:
            reviewed = path
    assert drafted and reviewed, 'need one draft and one reviewed decision node for this test'

    run = tmp_path / 'tasks' / 'STORY-1'
    run.mkdir(parents=True)
    (run / 'plan.md').write_text(
        f"Shape from [a](/decision/{drafted.name}) and [b](/decision/{reviewed.name}).\n"
    )
    findings = cited_drafts(bundle, tmp_path / 'tasks')
    named = {rel for _severity, _kind, rel, _detail in findings}
    assert f'decision/{drafted.name}' in named
    assert f'decision/{reviewed.name}' not in named

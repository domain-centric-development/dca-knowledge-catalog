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
    # skeleton from dca-java (building blocks + rule library) — exact (regression guard)
    assert types["Marker"] == 28
    assert types["Rule"] == 107
    assert types["Process"] == 1
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
    prefixes = ("/guide/", "/marker/", "/rule/", "/process/")
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
    outward = re.compile(r"\]\([^)]*(dca-ecommerce-sample|dca-book|implementing-domain-centric-architecture)[^)]*\)")
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
    graph_dirs = ("guide", "marker", "rule", "process",
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

"""OKF conformance + content tests for the generated bundle.

Regenerates the bundle into a temp dir and validates it against the OKF spec
and the catalog's own invariants. Also asserts idempotence (deterministic output).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from dca_catalog import generate, lint, obsidian
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
    # skeleton from the sample app — exact (regression guard)
    assert types["Marker"] == 24
    assert types["Rule"] == 90
    assert types["ADR"] == 28
    assert types["Process"] == 1
    # book + guide full text — lower bounds (content evolves)
    assert types.get("Chapter", 0) >= 25
    assert types.get("Guide", 0) >= 10
    assert types.get("Section", 0) >= 300


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
        elif t == "ADR":
            assert fm.get("pattern"), f"{p} adr missing pattern"
            assert fm.get("status"), f"{p} adr missing status"
        elif t in ("Chapter", "Guide", "Section"):
            assert fm.get("title"), f"{p} {t} missing title"
            assert fm.get("source") in ("book", "guide"), f"{p} {t} bad source"


def test_reserved_indexes_present(bundle: Path):
    assert (bundle / "index.md").exists()
    assert (bundle / "log.md").exists()
    # every directory containing concepts has an index.md
    dirs = {p.parent for p in _concept_files(bundle)}
    for d in dirs:
        assert (d / "index.md").exists(), f"missing index.md in {d}"


def test_bundle_relative_links_resolve(bundle: Path):
    # Only validate links into our own top-level dirs; copied book/guide prose may
    # carry unrelated absolute links that are not part of the OKF graph.
    prefixes = ("/book/", "/guide/", "/marker/", "/rule/", "/adr/", "/process/")
    link_re = re.compile(r"\]\((/[^)]+)\)")
    broken = []
    for p in bundle.rglob("*.md"):
        for target in link_re.findall(p.read_text(encoding="utf-8")):
            if target.startswith(prefixes) and not (bundle / target.lstrip("/")).exists():
                broken.append((str(p.relative_to(bundle)), target))
    assert not broken, f"broken bundle-relative links: {broken}"


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
        "---\ntype: Marker\ntitle: X\nresource: ai-architecture-sample/GONE.java\n---\n\n"
        "broken [link](/rule/nope/none.md)\n",
        encoding="utf-8",
    )
    (bundle / "note" / "floating.md").write_text(
        "---\ntype: Note\ntitle: Floating\n---\n\nno skeleton link\n", encoding="utf-8"
    )
    kinds = {f[1] for f in lint.lint(bundle, REPO_ROOT)}
    assert {"broken-link", "stale-resource", "unanchored-authored", "orphan"} <= kinds


def test_obsidian_export_rewrites_links(bundle: Path, tmp_path):
    graph_dirs = ("book", "guide", "marker", "rule", "adr", "process",
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
    node_rel = "adr/adr-026-transactional-outbox-integration-events.md"
    # canonical bundle keeps OKF leading-slash links (export is non-destructive)
    assert leading.search((bundle / node_rel).read_text())

    # export: zero leading-slash graph links remain anywhere
    for p in out.rglob("*.md"):
        assert not leading.search(p.read_text(encoding="utf-8")), f"{p} still leading-slash"

    # spot-check: that node's rewritten graph links resolve on disk
    node = out / node_rel
    rel = re.compile(r"\]\((\.\./(?:marker|rule|process)/[^)]+\.md)\)")
    targets = rel.findall(node.read_text(encoding="utf-8"))
    assert targets, "expected rewritten relative graph links"
    for target in targets:
        assert (node.parent / target).resolve().exists(), f"unresolved: {target}"
    assert (out / ".obsidian" / "app.json").exists()


def test_marker_discussed_in(bundle: Path):
    # reverse edge: markers link the sections that primarily discuss them
    text = (bundle / "marker" / "port-out" / "repository.md").read_text(encoding="utf-8")
    assert "## Discussed in" in text
    links = re.findall(r"\]\((/(?:book|guide)/[^)]+\.md)\)",
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
        "See [[usecase|the marker]] and [adr](../adr/index.md).\n",
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
    assert "](/adr/index.md)" in imported  # relative -> bundle-relative
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


def test_mirror_redacts_book_bodies(bundle: Path, tmp_path):
    dest = tmp_path / "mirror"
    generate._mirror(bundle, [dest], redact_dirs=("book",))

    # a book section: verbatim body gone, frontmatter + description + links stay
    src_rel = "book/06-application-layer/stores-persistence-for-non-aggregate-data.md"
    original = (bundle / src_rel).read_text(encoding="utf-8")
    redacted = (dest / src_rel).read_text(encoding="utf-8")
    assert "Full text not included" in redacted
    assert len(redacted) < len(original) / 2
    assert redacted.startswith("---\ntype: Section")
    assert "resource:" in redacted
    # graph edges preserved
    for heading in ("## Related markers",):
        if heading in original:
            assert heading in redacted
    # the redacted body must not contain the full prose (spot check a mid-file line)
    assert "record LoginAttempt" not in redacted

    # guide is public — mirrored verbatim
    guide_rel = "guide/readme/java-package-structure.md"
    assert (dest / guide_rel).read_text(encoding="utf-8") == (bundle / guide_rel).read_text(encoding="utf-8")
    # navigation stays intact
    assert (dest / "book" / "index.md").read_text(encoding="utf-8") == (bundle / "book" / "index.md").read_text(encoding="utf-8")


def test_idempotent(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    generate.generate(REPO_ROOT, a)
    generate.generate(REPO_ROOT, b)
    files_a = sorted(p.relative_to(a).as_posix() for p in a.rglob("*.md"))
    files_b = sorted(p.relative_to(b).as_posix() for p in b.rglob("*.md"))
    assert files_a == files_b
    for rel in files_a:
        assert (a / rel).read_text() == (b / rel).read_text(), f"non-deterministic: {rel}"

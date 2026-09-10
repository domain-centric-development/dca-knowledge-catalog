"""Source provenance must survive committing its derived output."""
import subprocess

from dca_catalog.retrieval import _revision


def test_generated_commit_preserves_source_revision(tmp_path):
    def git(*args):
        return subprocess.check_output(["git", "-C", str(tmp_path), "-c", "user.name=Fixture",
                                        "-c", "user.email=fixture@example.invalid", *args], text=True).strip()
    git("init")
    source = tmp_path / "source.py"
    source.write_text("first")
    git("add", ".")
    git("commit", "-m", "source")
    revision = git("rev-parse", "HEAD")
    (tmp_path / "manifest.json").write_text("generated")
    git("add", ".")
    git("commit", "-m", "derived output")
    assert git("rev-parse", "HEAD") != revision
    assert _revision(tmp_path, [source]) == revision
    source.write_text("second")
    git("add", ".")
    git("commit", "-m", "changed source")
    assert _revision(tmp_path, [source]) == git("rev-parse", "HEAD")


def test_manifest_hashes_only_generator_inputs_and_omits_its_own_revision(tmp_path):
    import json
    from dca_catalog.retrieval import write_manifest

    def git(repo, *args):
        return subprocess.check_output(["git", "-C", str(repo), "-c", "user.name=Fixture",
                                        "-c", "user.email=fixture@example.invalid", *args], text=True).strip()
    guide = tmp_path / "dca-guide"; guide.mkdir()
    (guide / "README.md").write_text("guide")
    (guide / "AGENTS.md").write_text("agents")
    git(guide, "init"); git(guide, "add", "."); git(guide, "commit", "-m", "guide")
    guide_rev = git(guide, "rev-parse", "HEAD")
    own = tmp_path / "dca-knowledge-catalog"; (own / "src").mkdir(parents=True)
    (own / "src/gen.py").write_text("x = 1")
    git(own, "init"); git(own, "add", "."); git(own, "commit", "-m", "source")
    bundle = tmp_path / "bundle"; bundle.mkdir()
    write_manifest(tmp_path, bundle, {})
    first = json.loads((bundle / "manifest.json").read_text())["sources"]
    assert first["dca-guide"]["revision"] == guide_rev
    assert first["dca-knowledge-catalog"]["revision"] is None
    # a commit touching only a skipped file (AGENTS.md) must not move the guide entry
    (guide / "AGENTS.md").write_text("agents changed"); git(guide, "commit", "-qam", "agents")
    # committing sources together with the derived output must not move the own entry either
    (own / "bundle").mkdir(); (own / "bundle/manifest.json").write_text("derived"); git(own, "add", "."); git(own, "commit", "-qm", "source+bundle")
    write_manifest(tmp_path, bundle, {})
    second = json.loads((bundle / "manifest.json").read_text())["sources"]
    assert second == first

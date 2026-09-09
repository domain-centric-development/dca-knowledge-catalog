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

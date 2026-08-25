"""Mirror an already-built OKF bundle into another project.

Usage:  python -m dca_catalog.mirror --to PATH [--from SOURCE] [--ref REF]

SOURCE is one of
  - a local bundle directory (contains ``index.md``),
  - a local catalog repository (contains ``bundle/index.md``),
  - a git URL (``git@...``, ``https://...`` or anything ending in ``.git``) —
    shallow-cloned to a temp dir and cleaned up afterwards.
Default: the ``bundle/`` of the repository this module lives in.

Unlike ``dca_catalog.generate`` this needs *no* source repositories — it only
copies a built bundle, dropping the ``resource:`` provenance frontmatter that
names files the consuming project does not have. A mirror is meant to be
regenerated on demand and NOT checked in (add the target to the consuming
project's ``.gitignore``); the one committed mirror is the vendored copy inside
the dca-core plugin, which ``generate`` maintains.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def strip_resource(text: str) -> str:
    """Drop the ``resource:`` frontmatter key, leaving the body untouched.

    Body text may legitimately contain a ``resource:`` line (a YAML example in a
    code fence), so this only rewrites the frontmatter block.
    """
    if not text.startswith("---\n") or text.count("\n---\n", 3) == 0:
        return text
    end = text.index("\n---\n", 3) + 1
    front = "".join(
        line for line in text[:end].splitlines(keepends=True)
        if not line.startswith("resource:")
    )
    return front + text[end:]


def mirror_bundle(bundle: Path, dests: list[Path]) -> None:
    """Replace each dest with a fresh copy of the bundle at ``bundle``.

    The mirror is what ships to other projects, where a source path like
    ``dca-ecommerce-sample/src/main/java/...`` names a repository the reader
    does not have. It must stand on its own, so ``resource:`` is dropped on the
    way out; the canonical bundle keeps it as provenance (and as the basis for
    the lint's stale-resource check).
    """
    bundle = bundle.resolve()
    for dest in dests:
        dest = dest.resolve()
        if dest == bundle:
            continue
        if dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(bundle, dest)
        for node in dest.rglob("*.md"):
            text = node.read_text(encoding="utf-8")
            stripped = strip_resource(text)
            if stripped != text:
                node.write_text(stripped, encoding="utf-8")


def _is_git_url(source: str) -> bool:
    return "://" in source or source.startswith("git@") or source.endswith(".git")


def _bundle_in(root: Path) -> Path:
    """Locate the bundle inside a local directory (the bundle itself, or a repo)."""
    if (root / "index.md").exists():
        return root
    if (root / "bundle" / "index.md").exists():
        return root / "bundle"
    raise SystemExit(
        f"No OKF bundle found at {root} (expected index.md or bundle/index.md)"
    )


def _default_source() -> Path:
    # src/dca_catalog/mirror.py -> dca_catalog -> src -> repo root
    return Path(__file__).resolve().parents[2] / "bundle"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Mirror a built DCA OKF bundle into another project."
    )
    parser.add_argument(
        "--from", dest="source", default=None,
        help="bundle dir, catalog repo dir, or git URL (default: this repo's bundle/)",
    )
    parser.add_argument(
        "--to", dest="dest", type=Path, required=True,
        help="target directory — replaced with the mirrored bundle",
    )
    parser.add_argument(
        "--ref", default=None,
        help="branch or tag to clone when --from is a git URL (default: remote HEAD)",
    )
    args = parser.parse_args(argv)

    if args.source is not None and _is_git_url(args.source):
        with tempfile.TemporaryDirectory(prefix="dca-catalog-") as tmp:
            clone = Path(tmp) / "repo"
            cmd = ["git", "clone", "--depth", "1"]
            if args.ref:
                cmd += ["--branch", args.ref]
            cmd += [args.source, str(clone)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise SystemExit(f"git clone failed:\n{result.stderr.strip()}")
            mirror_bundle(_bundle_in(clone), [args.dest])
    else:
        source = Path(args.source).resolve() if args.source else _default_source()
        mirror_bundle(_bundle_in(source), [args.dest])

    print(f"Mirrored -> {args.dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

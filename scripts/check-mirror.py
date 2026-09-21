#!/usr/bin/env python3
"""The shipped mirror must be the canonical bundle.

`bundle_sha256` in the mirror's own manifest is computed over the mirror's content, so a mirror
that fell behind still carries a self-consistent manifest — it simply describes an older catalog.
Nothing compared the two, so a regenerate that skipped the mirror shipped stale knowledge under a
correct-looking digest, which is the shape of defect the catalog exists to prevent.

Compares the canonical bundle's digest with each mirror's. Mirrors that do not exist are skipped:
a checkout without the marketplace sibling is a normal state, not a failure.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from dca_catalog.retrieval import bundle_digest  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MIRRORS = [
    ROOT.parent / "dca-marketplace/plugins/dca-core/skills/dca-knowledge/catalog",
]


def main() -> int:
    canonical = bundle_digest(ROOT / "bundle")
    failed = False
    for mirror in MIRRORS:
        if not mirror.exists():
            print(f"    {mirror.name}: not in this checkout — skipped")
            continue
        actual = bundle_digest(mirror)
        recorded = json.loads((mirror / "manifest.json").read_text()).get("bundle_sha256")
        where = mirror.relative_to(ROOT.parent)
        if actual != canonical:
            failed = True
            print(f"ERROR: {where} differs from the canonical bundle.\n"
                  f"       canonical {canonical}\n"
                  f"       mirror    {actual}\n"
                  f"       Run the generator (it mirrors by default) and commit both.", file=sys.stderr)
        elif recorded != actual:
            failed = True
            print(f"ERROR: {where}/manifest.json records {recorded}, content hashes to {actual}.",
                  file=sys.stderr)
        else:
            print(f"    {where}: equals the canonical bundle")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

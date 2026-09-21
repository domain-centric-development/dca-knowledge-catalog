#!/usr/bin/env python3
"""Every rule node in the bundle must exist in the library version the manifest names.

The failure this prevents: the bundle documents an id the published jar or package does not have.
A team installs the released library, its agent reads the vendored catalog, cites the id with a
node path, and the rule is not there — and the catalog's grounding rule ("answer only from nodes
you actually read") makes the agent more confident, not less. Nothing else catches it: the manifest
records the versions faithfully and the rule nodes are generated faithfully; they are simply
generated from a different tree than the one that was released.

Compares the ids in bundle/rule/ against `rules.json` at the release tag named in
`library_versions`. A snapshot version is not a release and is skipped with a message. A missing
tag is skipped too — the check cannot speak about a version that was never tagged.

Run from anywhere; exits non-zero on the first library that disagrees.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent

# library key in library_versions -> (sibling checkout, version property, tag prefix)
LIBRARIES = [
    ("java", "archunitVersion", REPO_ROOT / "dca-java", "archunit/v"),
    ("dotnet", "DomainCentric.ArchRules", REPO_ROOT / "dca-dotnet", "archrules/v"),
]


def released_ids(repo: Path, tag: str) -> set[str] | None:
    if subprocess.run(["git", "-C", str(repo), "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
                      capture_output=True).returncode != 0:
        return None
    shown = subprocess.run(["git", "-C", str(repo), "show", f"{tag}:rules.json"],
                           capture_output=True, text=True)
    if shown.returncode != 0:
        return None
    catalog = json.loads(shown.stdout)
    return {rule["id"] for rule in catalog["rules"]}


def main() -> int:
    manifest = json.loads((ROOT / "bundle/manifest.json").read_text())
    versions = manifest["library_versions"]
    bundle_ids = {
        re.sub(r"\.md$", "", path.name).upper()
        for path in (ROOT / "bundle/rule").rglob("dca-*.md")
    }
    if not bundle_ids:
        print("no rule nodes in the bundle — nothing to check", file=sys.stderr)
        return 1

    # An id has to exist in at least one released library: DCA-NET-* only ships in .NET, and a
    # Java rule not applicable in .NET is absent there. Comparing per library would hold each of
    # those against the other; comparing against the union is what the bundle actually claims,
    # because the bundle documents both libraries as one catalog.
    released: set[str] = set()
    checked = []
    for key, prop, repo, prefix in LIBRARIES:
        version = (versions.get(key) or {}).get(prop)
        if not version:
            print(f"    {key}: no {prop} in library_versions — skipped")
            continue
        if version.endswith("-SNAPSHOT"):
            print(f"    {key}: {version} is not a release — skipped")
            continue
        ids = released_ids(repo, prefix + version)
        if ids is None:
            print(f"    {key}: tag {prefix}{version} not found in {repo.name} — skipped")
            continue
        released |= ids
        checked.append(f"{repo.name} {version}")

    if not checked:
        print("    no released library to compare against — nothing checked")
        return 0

    unknown = sorted(bundle_ids - released)
    if unknown:
        print(f"ERROR: {len(unknown)} rule node(s) exist in no released library "
              f"({', '.join(checked)}): " + ", ".join(unknown), file=sys.stderr)
        print("       Release the libraries first, or regenerate the bundle from the released "
              "sources — a consumer installs the release and reads this bundle.", file=sys.stderr)
        return 1

    print(f"    every rule node exists in {' or '.join(checked)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

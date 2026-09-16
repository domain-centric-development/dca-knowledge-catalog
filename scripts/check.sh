#!/usr/bin/env bash
# Freshness + health gate for the DCA OKF catalog. Used by CI and the git
# pre-commit hook. Stdlib-only generator; needs python3 (+ pytest for tests).
#
#   regenerate (no mirror) -> lint -> tests -> assert bundle is not stale
#
# Exit non-zero on any failure. Run from anywhere.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH=src

# As a pre-commit hook under `git commit -a`, git points GIT_INDEX_FILE at a temporary index. The
# generator and the tests run their own git commands (fixture repositories, `git log` on the
# sibling checkouts) and would inherit that variable, corrupting the pending commit and failing on
# trees the fixture repository does not have. Only the freshness diff below may see the hook's
# index: it is the state about to be committed.
HOOK_INDEX="${GIT_INDEX_FILE:-}"
unset GIT_INDEX_FILE

echo "==> generate (no mirror)"
python3 -m dca_catalog.generate --no-default-mirror

echo "==> lint"
python3 -m dca_catalog.lint

echo "==> tests"
if python3 -c "import pytest" 2>/dev/null; then
  python3 -m pytest tests/ -q
else
  echo "    (pytest not installed — skipping; CI installs it)"
fi

# Freshness: the bundle about to be committed (the index — under `git commit -a` the hook's
# temporary one) must already equal a fresh generate. Only meaningful inside a git work tree
# (skipped otherwise).
if [ -n "$HOOK_INDEX" ]; then export GIT_INDEX_FILE="$HOOK_INDEX"; fi
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "==> freshness (git diff bundle/)"
  if ! git -C "$ROOT" diff --quiet -- bundle; then
    echo "ERROR: bundle/ is stale — sources changed but the bundle was not regenerated." >&2
    echo "       Run 'make generate' and commit the result." >&2
    git -C "$ROOT" --no-pager diff --stat -- bundle >&2
    exit 1
  fi
fi

echo "OK: catalog is fresh, linted, and tested."

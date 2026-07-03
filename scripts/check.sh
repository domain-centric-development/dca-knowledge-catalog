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

# Freshness: a committed bundle must already equal a fresh generate. Only
# meaningful inside a git work tree (skipped otherwise).
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

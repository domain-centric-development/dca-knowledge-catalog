#!/usr/bin/env bash
# Smoke check for compose.yaml: the tool services stay isolated in the `tools` profile and the CI image in
# `ci`, so `docker compose up` / `docker compose build` touch nothing and `run --rm <verb>` reaches exactly
# the verbs the README names. Picks `docker compose`, `podman compose` or `podman-compose`, whichever is
# installed; COMPOSE overrides the choice (e.g. COMPOSE=podman-compose).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
if [ -z "${COMPOSE:-}" ]; then
  if command -v docker >/dev/null 2>&1; then COMPOSE="docker compose"
  elif command -v podman >/dev/null 2>&1; then COMPOSE="podman compose"
  else COMPOSE="podman-compose"; fi
fi
$COMPOSE version >/dev/null 2>&1 || { echo "ERROR: '$COMPOSE' is not a working compose CLI" >&2; exit 2; }

services() { $COMPOSE "$@" config --services 2>/dev/null | grep -v '^$' | sort | tr '\n' ' ' | sed 's/ $//'; }
expect() {
  local label="$1" want="$2" got="$3"
  if [ "$got" != "$want" ]; then
    echo "ERROR: $label services: got '$got', want '$want'" >&2
    exit 1
  fi
  echo "    $label: ${got:-<none>}"
}

echo "==> compose smoke ($COMPOSE)"
expect "default profile" "" "$(services)"
expect "profile tools" "check generate python test" "$(services --profile tools)"
expect "profile ci" "ci" "$(services --profile ci)"
echo "OK: tool services isolated in profile 'tools', image in 'ci'."

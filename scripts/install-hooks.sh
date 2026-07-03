#!/usr/bin/env bash
# Install the catalog's git pre-commit hook (dependency-free; no pre-commit
# framework needed). Run once after cloning. Must be inside a git work tree.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GITDIR="$(git -C "$ROOT" rev-parse --git-dir 2>/dev/null || true)"
if [ -z "$GITDIR" ]; then
  echo "Not a git repository: $ROOT — initialise git first." >&2
  exit 1
fi

HOOK="$GITDIR/hooks/pre-commit"
cat > "$HOOK" <<'HOOK_EOF'
#!/usr/bin/env bash
# Auto-installed by dca-knowledge-catalog/scripts/install-hooks.sh
set -euo pipefail
exec "$(git rev-parse --show-toplevel)/scripts/check.sh"
HOOK_EOF
chmod +x "$HOOK"
echo "Installed pre-commit hook -> $HOOK"

# CLAUDE.md

Guidance for Claude Code when working in `dca-knowledge-catalog/`.

## What this is

An OKF (Open Knowledge Format) bundle that captures the **bootstrap skeleton** of
a Domain-Centric Architecture app — marker contracts, ArchUnit rules, ADRs, and
the ADR process — for consumption by an LLM / agentic coding factory. See
[README.md](README.md) and [SPEC.md](SPEC.md).

## ⚠️ `bundle/` is GENERATED — never hand-edit it

The bundle is a **derived artifact** generated from the other sub-projects:

| Bundle content | Generated from |
|----------------|----------------|
| `bundle/book/**` | `dca-book/*.md` (full text, container + section nodes) |
| `bundle/guide/**` | `implementing-domain-centric-architecture/*.md` (full text) |
| `bundle/marker/**` | `ai-architecture-sample/src/main/java/.../sharedkernel/marker/**/*.java` |
| `bundle/rule/**` | `ai-architecture-sample/src/test-architecture/groovy/.../*ArchUnitTest.groovy` |
| `bundle/adr/**` | `ai-architecture-sample/docs/architecture/adr/adr-*.md` |
| `bundle/process/creating-an-adr.md` | `implementing-domain-centric-architecture/adr-template.md` |

The book/guide are the **main body** (full text copied verbatim); marker/rule/ADR
nodes are the **skeleton** they anchor to.

To change the catalog, **edit the source above, then regenerate**:

```bash
PYTHONPATH=src python3 -m dca_catalog.generate   # stdlib-only, no install
PYTHONPATH=src python3 -m dca_catalog.lint        # health check (broken links, stale, orphans)
PYTHONPATH=src python3 -m pytest tests/
```

(Alternative: `pip install -e ".[dev]"` once in a venv, then drop the `PYTHONPATH=src` prefix.)

Never edit files under the **generated zone** directly — they will be overwritten.

### Two zones — what you may edit

The bundle is one OKF graph in two zones (see `SPEC.md`):

| Zone | Dirs | Edit by hand? |
|------|------|---------------|
| **Generated** | `book/ guide/ marker/ rule/ adr/ process/` | ❌ no — derived, wiped + rebuilt each run |
| **Extensible** | `recipe/ decision/ pitfall/ template/ note/` | ✅ yes — authored, **preserved** across `generate` |

`generate` rebuilds the generated zone, preserves authored node files in the
extensible zone, and regenerates every `index.md` + `log.md` (scanning both zones,
so authored nodes are catalogued automatically). To add knowledge that isn't
derived from a source — a task playbook, a design-fork decision, an anti-pattern,
a saved query answer — drop an OKF node (`type:` + `title:` + `tags:` from the
SPEC.md tag taxonomy) into the matching extensible dir; do **not** edit the
generated zone. Authored nodes can also be written **in Obsidian**: `make obsidian`,
edit/author in the vault, then `make obsidian-import` (imports extensible-zone
edits, regenerates indexes, lints).

### Vendored plugin copy (also generated)

`generate` mirrors the freshly built bundle into the dca-core plugin at
`dca-marketplace/plugins/dca-core/skills/dca-knowledge/catalog/` so the
`/dca-knowledge` skill ships a catalog that works in any project with no setup.
That copy is **also a derived artifact — never hand-edit it**; it's byte-identical
to `bundle/` after every run. Disable with `--no-default-mirror`; add more targets
with `--mirror PATH`.

## Generator structure (`src/dca_catalog/`)

- `okf.py` — `Node` model + deterministic markdown/frontmatter writer.
- `docs.py` — parses book/guide `.md` into Chapter/Guide containers + Section
  children (fence-aware `##` splitter; full verbatim text in section bodies).
- `markers.py` — parses marker `.java` (declaration anchored at column 0 to avoid
  matching javadoc example code).
- `rules.py` — parses Spock `def "<rule>"()` methods; body carried verbatim.
- `adrs.py` — parses ADRs (strips code/domain prose) + builds the Process node.
- `linker.py` — string-based cross-linking (rule↔marker↔ADR, section→marker/ADR),
  sorted for determinism.
- `generate.py` — orchestrates; zone-aware (rebuilds the generated zone, preserves the
  authored extensible zone); writes `index.md` per directory + `log.md`; mirrors to the plugin.
- `lint.py` — mechanical health check on a built bundle: broken links (all zones), stale
  `resource:` pointers, unanchored authored nodes, orphans. Exit 1 on ERROR (`--strict` for WARN).
- `obsidian.py` — Obsidian **export + import**. Export (`make obsidian` →
  `bundle-obsidian/`, gitignored): copies the bundle, rewrites leading-slash OKF links
  to file-relative ones Obsidian resolves, injects `aliases:` (title), forces
  markdown-link vault settings, colors the graph per type; existing `.obsidian/` state
  survives re-export. Import (`make obsidian-import`): writes extensible-zone edits
  from the vault back into `bundle/` (relative links + wikilinks → bundle-relative,
  `type:` required); generated-zone edits are reported and ignored. See SPEC.md
  "Obsidian view".

## Invariants to preserve

- **Deterministic output** — no timestamps, sorted links: same sources →
  byte-identical bundle. Verified by `test_idempotent` (two builds compared
  byte-for-byte) and by the `check.sh` freshness gate (git diff over `bundle/` —
  this sub-project is its own git repo, like its siblings; the extensible zone
  is not regenerable, so its history lives here). Regenerating must change
  output only when a source changed.
- **Domain-free skeleton** — the marker/rule/ADR nodes capture the architecture
  and decisions, never the sample's e-commerce domain model. (Book/guide nodes
  may contain illustrative domain examples — that's the source text.)
- **OKF conformance** — every concept has a non-empty `type`; `index.md`/`log.md`
  are reserved; links are bundle-relative (leading `/`).

## Cross-project consistency

This sub-project is downstream of `ai-architecture-sample`. When marker
interfaces, ArchUnit rules, or ADRs change there, regenerate the bundle (see the
root `CLAUDE.md` cross-project checklist). All persisted content is English.

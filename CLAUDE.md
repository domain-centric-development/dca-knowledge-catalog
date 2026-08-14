# CLAUDE.md

Guidance for Claude Code when working in `dca-knowledge-catalog/`.

## What this is

An OKF (Open Knowledge Format) bundle that captures the **bootstrap skeleton** of
a Domain-Centric Architecture app — marker contracts, ArchUnit rules, and the ADR
process — for consumption by an LLM / agentic coding factory. See
[README.md](README.md) and [SPEC.md](SPEC.md).

## ⚠️ `bundle/` is GENERATED — never hand-edit it

The bundle is a **derived artifact** generated from the other sub-projects:

| Bundle content | Generated from |
|----------------|----------------|
| `bundle/guide/**` | `implementing-domain-centric-architecture/*.md` (full text, container + section nodes) |
| `bundle/marker/**` | `ai-architecture-sample/src/main/java/.../sharedkernel/marker/**/*.java` |
| `bundle/rule/**` | `ai-architecture-sample/src/test-architecture/groovy/.../*ArchUnitTest.groovy` |
| `bundle/process/creating-an-adr.md` | `implementing-domain-centric-architecture/adr-template.md` |

The guide is the **main body** (full text copied verbatim); marker and rule nodes
are the **skeleton** it anchors to.

**The book and the sample's ADRs are deliberately not sources.** An ADR records a
decision *one* project made; a reader building their own application has no such
file, so citing "ADR-030" would point at nothing. The book is not public. What
either taught belongs in the guide — fold it in there, and it reaches the bundle
on the next run.

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
| **Generated** | `guide/ marker/ rule/ process/` | ❌ no — derived, wiped + rebuilt each run |
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
That copy is **also a derived artifact — never hand-edit it**. It is a verbatim
copy: every node type in the bundle is public, so nothing is redacted. Disable
mirroring with `--no-default-mirror`; add targets with `--mirror PATH`.

## Generator structure (`src/dca_catalog/`)

- `okf.py` — `Node` model + deterministic markdown/frontmatter writer.
- `docs.py` — parses the guide `.md` into Guide containers + Section
  children (fence-aware `##` splitter; full verbatim text in section bodies).
- `markers.py` — parses marker `.java` (declaration anchored at column 0 to avoid
  matching javadoc example code).
- `rules.py` — parses Spock `def "<rule>"()` methods; body carried verbatim.
- `process.py` — builds the Process node from the ADR template.
- `linker.py` — string-based cross-linking (rule↔marker, section→marker),
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
- **Domain-free skeleton** — the marker/rule nodes capture the architecture
  and decisions, never the sample's e-commerce domain model. (Guide nodes may
  contain illustrative domain examples — that's the source text.)
- **OKF conformance** — every concept has a non-empty `type`; `index.md`/`log.md`
  are reserved; links are bundle-relative (leading `/`).

## Cross-project consistency

This sub-project is downstream of `implementing-domain-centric-architecture` and
of `ai-architecture-sample`'s marker interfaces and ArchUnit tests. When any of
those change, regenerate the bundle (see the root `CLAUDE.md` cross-project
checklist). Changing the sample's ADRs or a book chapter does **not** affect the
bundle. All persisted content is English.

# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, and others) when working in `dca-knowledge-catalog/`.

## What this is

An OKF (Open Knowledge Format) bundle that captures the **bootstrap skeleton** of
a Domain-Centric Architecture app — building-block marker contracts, `dca-archunit` rules, and the ADR
process — for consumption by an LLM / agentic coding factory. See
[README.md](README.md) and [SPEC.md](SPEC.md).

## ⚠️ `bundle/` is GENERATED — never hand-edit it

The bundle is a **derived artifact** generated from the other sub-projects:

| Bundle content | Generated from |
|----------------|----------------|
| `bundle/guide/**` | `dca-guide/*.md` (full text, container + section nodes) |
| `bundle/marker/**` | `dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/**/*.java` |
| `bundle/rule/**` | `dca-java/rules.json` (ids, titles, rationale — regenerate with `./gradlew :dca-archunit:rulesCatalog`) + `dca-java/dca-archunit/src/main/java/.../rules/*Rules.java` (verbatim expression per rule); `dca-dotnet/rules.json` (`dotnet run --project tools/RulesCatalog -- .`) for `implementations`, `not_applicable_dotnet` and the .NET-only `DCA-NET` rules |
| `bundle/process/creating-an-adr.md` | `dca-guide/adr-template.md` |

The guide is the **main body** (full text copied verbatim); marker and rule nodes
are the **skeleton** it anchors to.

**The book and the sample's ADRs are deliberately not sources.** An ADR records a
decision *one* project made; a reader building their own application has no such
file, so citing "ADR-030" would point at nothing. The book is not public. What
either taught belongs in the guide — fold it in there, and it reaches the bundle
on the next run. The precise rule: **bundle knowledge nodes must not cite
reference-implementation ADRs; the ADR process node may contain explicitly
fictional example identifiers** (enforced by
`test_bundle_never_cites_specific_adr_records`, which exempts the process node).

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
That copy is **also a derived artifact — never hand-edit it**. Every node type is
public, so no node is dropped, but the `resource:` frontmatter is: the mirror
travels into projects that do not have the source repositories, where a path like
`dca-java/dca-building-blocks/src/main/java/…` names nothing. The canonical `bundle/`
keeps `resource:` as provenance and as the basis for the lint's stale-resource
check. Disable mirroring with `--no-default-mirror`; add targets with
`--mirror PATH`.

### ⚠️ The bundle stands alone — no links out

The catalog is *generated from* the guide and `dca-java` and must never link back
at either (nor at the sample or the non-public book). A consumer has the bundle and
nothing else, so `../dca-guide/…`, a `dca-java` source
path or a GitHub URL all point at nothing. Content is copied; pointers are
rewritten onto bundle nodes or dropped. Two conformance tests enforce this —
`test_bundle_never_links_out_to_a_sibling_project` and
`test_mirror_drops_the_resource_frontmatter`. A leftover link means a **source**
document acquired an outward reference: fix it there.

## Generator structure (`src/dca_catalog/`)

- `okf.py` — `Node` model + deterministic markdown/frontmatter writer.
- `docs.py` — parses the guide `.md` into Guide containers + Section
  children (fence-aware `##` splitter; full verbatim text in section bodies).
  Relative links in that text (`./spring-modulith.md#packaging-rules`) are
  rewritten onto bundle nodes — an `#anchor` resolves to the section node that
  carries the heading, an unknown one to the container; `adr-template.md` lands
  on the Process node (`_ALIASES`). A link left un-rewritten fails the tests: it
  means the guide points at a document the bundle has no node for (the book),
  which is a **guide** bug — fix the guide, not the generator.
- `markers.py` — parses the building-block `.java` types (declaration anchored at column 0 to
  avoid matching javadoc example code); bundle category from the package path, `package:` kept.
- `rules.py` — reads `dca-java/rules.json` (id, set, resolved title, rationale) and attaches the
  verbatim `DcaRule.of/check(...)` expression from the matching `<Set>Rules.java`; merges
  `dca-dotnet/rules.json` (implementation flag, n/a reasons, `DCA-NET` nodes without code body).
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
- **Tool-agnostic doctrine** — the graph is pure DCA doctrine for *any* LLM or
  agent harness. Tooling consumes the graph; the graph never mentions the
  tooling: no node (either zone) may reference Claude Code, the dca-core plugin,
  the marketplace, slash commands, or any other specific agent product. Enforced
  by `test_bundle_is_tool_agnostic` (scans the committed bundle, both zones).
- **Mirrors are never committed** — a mirror is regenerated on demand
  (`python3 -m dca_catalog.mirror`, see below) and belongs in the consuming
  project's `.gitignore`. The single exception is the vendored copy inside the
  dca-core plugin, which `generate` maintains.

## Cross-project consistency

This sub-project is downstream of `dca-guide` and
of `dca-java`'s building-block markers and `dca-archunit` rules, and of `dca-dotnet`'s rule
catalog. When any of
those change, regenerate the bundle (see the root `AGENTS.md` cross-project
checklist). Changing the sample's ADRs or a book chapter does **not** affect the
bundle. All persisted content is English.

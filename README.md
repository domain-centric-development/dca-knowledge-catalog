# DCA Knowledge Catalog

An **[Open Knowledge Format](SPEC.md) (OKF)** bundle for Domain-Centric
Architecture. Its **main body is the full text of the implementation guide**;
that knowledge is *anchored* to the DCA skeleton — the `dca-building-blocks` marker
contracts you implement and the `dca-archunit` rules you must obey.

It is designed to be **consumed by an LLM / agentic coding factory**: point an
agent at [`bundle/index.md`](bundle/index.md), give it a task ("add an aggregate
root", "design a bounded context"), and it navigates the typed, cross-linked
nodes — from a guide section down to the exact marker contract and the rules
that govern it.

Inspired by Google's [knowledge-catalog/okf](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf).

## What's in the bundle

| Type | ~Count | Source | What it gives an agent |
|------|-------|--------|------------------------|
| `Guide` | 10 | `dca-guide/*.md` | an implementation-guide doc |
| `Section` | ~104 | `##` headings of the above | one concept, **full verbatim text** |
| `Marker` | 29 | `dca-java/dca-building-blocks/**/*.java` | the contract/interface to implement |
| `Rule` | 115 | `dca-java/rules.json` + `dca-archunit/**/rules/*Rules.java`; `dca-dotnet/rules.json` adds the `dotnet` implementation flag, the `not_applicable_dotnet` reasons and the .NET-only `DCA-NET` rules | the enforceable, machine-checkable architecture, with stable ids `DCA-<SET>-<NNN>` |
| `Process` | 1 | `adr-template.md` | how to record a new decision |
| `Recipe` `Decision` `Pitfall` `Template` `Note` | ~69 | **authored** (extensible zone) | task playbooks, design-fork guides, anti-patterns, code skeletons, saved answers |

**Neither the book nor the sample's ADRs are in the bundle.** An ADR records a
decision *one* project made — a reader building their own application has no
`adr-030-…md` to open, so a citation would point at nothing. Knowledge worth
keeping from either belongs in the implementation guide, which is a source.

**Building something?** The bundle's entry point for construction tasks is the
task router [`bundle/recipe/build-a-dca-application.md`](bundle/recipe/build-a-dca-application.md)
— it maps "add an aggregate / use case / bounded context / …" to the recipe,
its rule checklist, and its template.

**Hybrid granularity:** each guide file is a container node plus one `Section`
child per `##` heading (carrying the full text). Nodes cross-reference each
other: sections link the markers they mention; every marker lists the rules that
*govern* it and the sections that *discuss* it; every rule lists the markers it
*applies to*.

**The skeleton layer is about the architecture, not the sample's domain.** The
e-commerce domain model (Cart, Product, …) is deliberately excluded from the
marker/rule nodes — only the contracts and the rules that shape them.

## Regenerate

The `bundle/` has **two zones** (see `SPEC.md`). The **generated zone** (`guide/
marker/ rule/ process/`) is a derived artifact — **never hand-edit it**; edit the
source (the guide / `dca-java` markers and rules) and regenerate. The rule source is
`dca-java/rules.json` — refresh it with `./gradlew :dca-archunit:rulesCatalog` after changing rules — plus `dca-dotnet/rules.json` (`dotnet run --project tools/RulesCatalog -- .`). The **extensible zone**
(`recipe/ decision/ pitfall/ template/ note/`) is authored by hand or by an LLM and
**survives regeneration**.

```bash
PYTHONPATH=src python3 -m dca_catalog.generate   # stdlib-only, no install
PYTHONPATH=src python3 -m dca_catalog.lint        # health check (links, stale, orphans)
```

> Alternative: `pip install -e .` once (needs a venv on PEP-668 systems), then
> plain `python3 -m dca_catalog.generate`.

The run also mirrors the bundle into the dca-core plugin
(`dca-marketplace/plugins/dca-core/skills/dca-knowledge/catalog/`) so the
`/dca-knowledge` skill ships a vendored, always-fresh copy. The mirror is
verbatim — every node type in the bundle is public. Skip mirroring with
`--no-default-mirror`; add targets with `--mirror PATH`.

Output is deterministic (no timestamps) — same sources produce a byte-identical
bundle, so `git diff bundle/` after a regenerate shows exactly what changed.

Options: `--repo-root PATH` (defaults to the repo root), `--out PATH` (defaults
to `./bundle`).

## Consume the catalog in another project

Any project can pull a **standalone, read-only copy** of the graph — no source
repositories, no install, no agent tooling required (the graph is pure,
tool-agnostic DCA doctrine; see `SPEC.md`). The mirror drops the `resource:`
provenance frontmatter, which points at repositories the consumer does not have.

```bash
# from this repo's remote (shallow clone, cleaned up afterwards)
python3 -m dca_catalog.mirror --from <git-url> --to docs/dca-catalog

# or from a local checkout / a built bundle dir
python3 -m dca_catalog.mirror --from ../dca-knowledge-catalog --to docs/dca-catalog
```

(Without an install, run it from a checkout with `PYTHONPATH=src`; with
`pip install`, the `dca-mirror` console script does the same. `--ref TAG`
pins a version when `--from` is a git URL.)

**Do not commit the mirror** — add the target to `.gitignore` and refresh on
demand. It is a read-only copy of the doctrine; project-specific knowledge
belongs in the project, not inside the mirrored graph. The one committed
mirror is the vendored copy inside the dca-core plugin, which `generate`
maintains.

## Add knowledge — the four ways

1. **Source knowledge** (a pattern, a rule, a guide doc): edit the
   *source* — `dca-guide/`, the marker
   markers or rules in `dca-java/` — then
   `make generate && make lint && make test`. Never hand-edit the generated zone.
2. **Authored node, directly**: drop `bundle/{recipe|decision|pitfall|template|note}/<slug>.md`
   with frontmatter `type:` + `title:` + `tags:` (pick tags from the SPEC.md
   [tag taxonomy](SPEC.md#tag-taxonomy)), body that *synthesizes*, and
   bundle-relative links (leading `/`) into the skeleton. `make generate`
   catalogues it into the indexes; `make lint` checks anchoring, links, and tags.
   The node survives every regeneration.
3. **In Obsidian**: `make obsidian`, author/edit in the vault (wikilinks fine —
   the import converts them), then `make obsidian-import` (imports, regenerates,
   lints in one go). See "Browse & author in Obsidian" below.
4. **From a Claude session**: `/dca-knowledge save <note|decision|pitfall|recipe|template> <title>`
   promotes a grounded query answer into a permanent extensible-zone node — the
   catalog compounds instead of re-deriving.

Whichever way: finish with a commit — the pre-commit hook (`make hooks`) runs the
full gate, and the extensible zone has no other backup than this repo's history.

## Test

```bash
pip install -e ".[dev]"
python3 -m pytest tests/
```

Conformance checks: every concept has a non-empty `type`; per-type required
fields are present; all bundle-relative links resolve; output is idempotent;
the extensible zone survives regeneration; lint catches injected problems; and
the node counts match the source inventory.

## CI & git hook

One gate runs generate → lint → tests → a freshness diff (the committed bundle
must equal a fresh regenerate):

```bash
make check          # or: ./scripts/check.sh
make hooks          # install it as a git pre-commit hook (one-time)
```

CI runs the same gate — `.github/workflows/catalog.yml` at the **monorepo root**
(the generator reads its sibling source dirs, so the workflow checks out the whole
tree). Targets: `make generate | lint | test | check | hooks`.

## Browse & author in Obsidian

The canonical bundle uses OKF **bundle-relative** links (leading `/`) that LLMs and
the tests rely on but Obsidian does not resolve. Export a browsable vault (relative
links, aliases, graph view with per-type colors, backlinks) without touching the
canonical bundle — and write authored nodes back:

```bash
make obsidian            # -> bundle-obsidian/ (gitignored; open as an Obsidian vault)
make obsidian-import     # write extensible-zone edits from the vault back to bundle/
                         # (then regenerates indexes + lints)
```

The vault is a **view**: extensible-zone nodes (`recipe/ decision/ pitfall/ template/
note/`) authored or edited there flow back via import (wikilinks and relative links
are rewritten to OKF form); edits to generated files are reported and ignored. Vault
UI state (`.obsidian/`) survives re-export. See SPEC.md "Obsidian view".

Frontmatter (`type`, `tags`, `status`) is plain YAML, so Dataview queries work over it.

## Layout

```
dca-knowledge-catalog/
├── SPEC.md                  # OKF spec adopted for DCA (the 12 node types, tag taxonomy)
├── src/dca_catalog/         # the generator (docs, markers, rules, process, linker, obsidian, lint)
├── tests/                   # conformance tests
├── bundle/                  # the OKF knowledge graph (canonical)
│   ├── index.md  log.md
│   ├── guide/               # GENERATED — full text: container + section nodes
│   ├── marker/  rule/  process/         # GENERATED — the anchoring skeleton
│   └── recipe/  decision/  pitfall/  template/  note/   # AUTHORED — survives regeneration
└── bundle-obsidian/         # gitignored Obsidian view (make obsidian / obsidian-import)
```

*Written with AI assistance — drafted mainly by Claude, reviewed and directed by the author
since 2025.*

## Licence

MIT — see [LICENSE](LICENSE).

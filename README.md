# DCA Knowledge Catalog

An **[Open Knowledge Format](SPEC.md) (OKF)** bundle for Domain-Centric
Architecture. Its **main body is the full text of the DCA book and the
implementation guide**; that knowledge is *anchored* to the reference
implementation's skeleton — the marker contracts you implement, the ArchUnit
rules you must obey, and the ADRs (used patterns) behind them.

It is designed to be **consumed by an LLM / agentic coding factory**: point an
agent at [`bundle/index.md`](bundle/index.md), give it a task ("add an aggregate
root", "design a bounded context"), and it navigates the typed, cross-linked
nodes — from a book/guide section down to the exact marker contract, the rules
that govern it, and the decisions that justify them.

Inspired by Google's [knowledge-catalog/okf](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf).

## What's in the bundle

| Type | ~Count | Source | What it gives an agent |
|------|-------|--------|------------------------|
| `Chapter` | 32 | `dca-book/*.md` | a book chapter (container + sections) |
| `Guide` | 13 | `implementing-domain-centric-architecture/*.md` | an implementation-guide doc |
| `Section` | ~500 | `##` headings of the above | one concept, **full verbatim text** |
| `Marker` | 22 | `sharedkernel/marker/**/*.java` | the contract/interface to implement |
| `Rule` | 87 | `*ArchUnitTest.groovy` | the enforceable, machine-checkable architecture |
| `ADR` | 25 | `docs/architecture/adr/adr-*.md` | the patterns used + rationale + consequences |
| `Process` | 1 | `adr-template.md` | how to record a new decision |

**Hybrid granularity:** each book/guide file is a container node plus one
`Section` child per `##` heading (carrying the full text). Nodes cross-reference
each other: sections link the markers/ADRs they mention; every marker lists the
rules that *govern* it and the ADRs that *reference* it; every rule lists the
markers it *applies to*; every ADR lists the rules that *enforce* it.

**The skeleton layer is about the architecture, not the sample's domain.** The
e-commerce domain model (Cart, Product, …) is deliberately excluded from the
marker/rule/ADR nodes — only the contracts and the decisions that shape them.

## Regenerate

The `bundle/` has **two zones** (see `SPEC.md`). The **generated zone** (`book/ guide/
marker/ rule/ adr/ process/`) is a derived artifact — **never hand-edit it**; edit the
source (marker interfaces / ArchUnit tests / ADRs) and regenerate. The **extensible zone**
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
`/dca-knowledge` skill ships a vendored, always-fresh copy. Skip with
`--no-default-mirror`; add targets with `--mirror PATH`.

Output is deterministic (no timestamps) — same sources produce a byte-identical
bundle, so `git diff bundle/` after a regenerate shows exactly what changed.

Options: `--repo-root PATH` (defaults to the repo root), `--out PATH` (defaults
to `./bundle`).

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
├── SPEC.md                  # OKF spec adopted for DCA (+ the 4 node types)
├── src/dca_catalog/         # the generator (markers, rules, adrs, linker, okf)
├── tests/                   # conformance tests
└── bundle/                  # GENERATED — the OKF knowledge graph
    ├── index.md  log.md
    ├── book/  guide/        # full text: container + section nodes
    └── marker/  rule/  adr/  process/   # the anchoring skeleton
```

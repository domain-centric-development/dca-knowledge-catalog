# Open Knowledge Format — DCA Profile (v0.1)

This catalog adopts the **Open Knowledge Format (OKF)**: knowledge represented as
plain markdown files with YAML frontmatter, organized as a navigable graph that
LLMs/agents consume directly — no SDK, no query language. *If you can `cat` a
file you can read it; if you can `git clone` a repo you can ship it.*

(Reference: Google's [OKF spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).)

## Core rules (from OKF)

- Every non-reserved `.md` file is a **concept document** with YAML frontmatter
  delimited by `---`. The only mandatory frontmatter field is **`type`** — a
  short, self-explanatory string.
- Reserved filenames: **`index.md`** (directory listing for progressive
  disclosure) and **`log.md`** (changelog).
- Concepts link to each other with standard markdown links. This catalog uses
  **bundle-relative** targets (leading `/`, e.g. `/marker/port-out/repository.md`).
- Recommended frontmatter: `title`, `description`/body, `resource` (canonical URI
  of the underlying asset), `tags`. Consumers must tolerate unknown fields.
- Broken links are tolerated (they may mark not-yet-written knowledge), though
  this catalog's generator emits only resolving links.

## Two zones

The bundle is one OKF graph split into two zones:

- **Generated zone** — `guide/`, `marker/`, `rule/`, `process/`.
  Derived from the sources, **wiped and rebuilt on every `generate` run**. Never
  hand-edit (changes are overwritten); edit the source and regenerate.
- **Extensible zone** — `recipe/`, `decision/`, `pitfall/`, `template/`, `note/`.
  Authored by a human or an LLM, **preserved across regeneration**. The node
  *files* are authored; only each directory's `index.md` is regenerated (a
  content catalog scanned from disk). This is the living-wiki layer: query
  answers, playbooks, and decisions accumulate here without re-deriving sources.

Both zones are OKF-conformant (every node carries a non-empty `type`) and link
freely into each other with bundle-relative links.

## DCA node types

This profile defines ten `type` values. All carry `title` and `tags`;
generated-zone nodes also carry `resource` (the canonical source URI).

### `Guide`
A container node for one implementation-guide file.
- `source`: `guide`
- Body: the file's preamble (text before the first `##`).
- Link section: **Sections** (its child section nodes).

### `Section`
One `##` heading of a guide file — the unit of knowledge, carrying the
**full verbatim text** of that section.
- `source`: `guide`
- `chapter`: the parent container title
- Body: the section's complete markdown (sub-headings, code, lists).
- Link section: **Related markers** (anchoring to the skeleton).

### `Marker`
A marker interface / annotation from `sharedkernel/marker` — a contract a new
application implements.
- `category`: `tactical | strategic | port-in | port-out | infrastructure`
- `kind`: `interface | class | annotation`
- `signature`: the Java declaration (generics + supertypes)
- `extends`: supertype marker names (optional)
- `methods`: declared method signatures (optional)
- Link sections: **Extends**, **Governed by** (rules), **Discussed in** (the
  guide sections that primarily discuss the marker — title match or dense
  mentions, capped at 10 to stay low-noise).

### `Rule`
One ArchUnit feature method — an enforceable architecture rule.
- `rule`: the rationale (the `.because(...)` text — the *why*)
- `constraint`: the rule as a single-line actionable precondition (the *what*, from the
  method name) — what an LLM satisfies while generating; recipes surface these as checklists
- `enforced_by`: `<TestClass>#<method>`
- `status`: `enforced | informational | disabled`
- `test_class`: the ArchUnit test class
- Body: the rule's Groovy expression, verbatim, in a fenced block.
- Link section: **Applies to markers**.

### `Process`
A how-to for sustaining the architecture's conventions (currently: how to write
an ADR). Body is the procedure + section skeleton.

### Extensible-zone types (authored)

These five live in the extensible zone. They are optional, may start empty, and
are written by hand or by an LLM (e.g. `/dca-knowledge` saving a query answer).
All require `type` + `title`; `resource` is optional (they synthesize, not mirror).

- **`Recipe`** (`recipe/`) — a task playbook: ordered steps to build a DCA
  construct (e.g. "add a use case"), linking the markers, rules and template it
  touches.
- **`Decision`** (`decision/`) — a guide for a design fork (which pattern when —
  e.g. sync vs async event, domain vs integration event), with the discriminator
  and links to the chosen targets.
- **`Pitfall`** (`pitfall/`) — an anti-pattern and the rule(s) that forbid it;
  powers "is X allowed?" lookups.
- **`Template`** (`template/`) — a domain-free code skeleton to fill in.
- **`Note`** (`note/`) — a compounded query answer: synthesis worth keeping,
  promoted from a one-off `/dca-knowledge` response into a permanent node.

## Tag taxonomy

`tags` is a flat, lowercase, kebab-case vocabulary used to filter before reading
bodies. Generated-zone tags are emitted by the generator and consistent by
construction. **Authored nodes must pick from the controlled vocabulary** —
`lint` WARNs on unknown tags so synonyms don't accumulate (`use-case` vs
`usecase`, `events` vs `event`). The vocabulary lives in `lint.py`
(`_TAG_VOCABULARY`) and is, by group:

- **node kind** (first tag, mirrors the directory): `recipe`, `decision`,
  `pitfall`, `template`, `note`
- **style/category**: `tactical`, `strategic`, `hexagonal`, `layered`, `onion`,
  `governance`, `port-in`, `port-out`
- **layer**: `domain`, `application`, `adapter`, `infrastructure`
- **building blocks & concepts**: `aggregate`, `entity`, `value-object`,
  `use-case`, `repository`, `domain-event`, `integration-event`, `events`,
  `outbox`, `specification`, `factory`, `domain-service`, `gateway`, `port`,
  `dto`, `bounded-context`, `shared-kernel`, `subdomain`, `context-map`,
  `anti-corruption-layer`, `package-structure`, `naming`, `testing`, `archunit`,
  `spring`, `modulith`, `rest`, `persistence`, `bootstrap`, `cqrs`,
  `event-sourcing`, `security`, `performance`, `migration`

To introduce a new tag: add it to this list **and** to `_TAG_VOCABULARY` in
`lint.py` in the same change.

## Obsidian view (export / import)

The canonical bundle is the OKF source of truth; an Obsidian vault is a derived
**view** of it (`make obsidian` → `bundle-obsidian/`, gitignored):

- **Export** rewrites bundle-relative links to file-relative ones Obsidian
  resolves, injects `aliases: [<title>]` for autocompletion, applies vault
  settings that force markdown links (never wikilinks), colors the graph per
  node type, and preserves any existing `.obsidian/` state across re-export.
- **Import** (`make obsidian-import`) writes **extensible-zone** edits from the
  vault back into the canonical bundle: file-relative links and wikilinks are
  rewritten to bundle-relative markdown links, frontmatter must carry a
  non-empty `type` (rejected otherwise). Edits to generated-zone files are
  reported and ignored — edit the source and regenerate instead. Vault
  deletions are reported, never applied. A no-edit roundtrip leaves the bundle
  byte-identical.

The loop is: `make obsidian` → edit/author in Obsidian → `make obsidian-import`
(runs import + `generate` + `lint`).

## Conformance

A bundle conforms when every non-reserved `.md` has parseable frontmatter with a
non-empty `type`, each directory holding concepts has an `index.md`, and the
reserved-file structure is respected. The generator additionally guarantees
deterministic output, resolving bundle-relative links, and **preservation of the
extensible zone across regeneration** (see `tests/`). A built bundle's ongoing health
(no broken links, no stale `resource:` pointers, no unanchored/orphan authored nodes) is
checked by `python3 -m dca_catalog.lint`.

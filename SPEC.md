# Open Knowledge Format — DCA Profile (v0.1)

This catalog pins its profile to **Open Knowledge Format (OKF) v0.1**: knowledge represented as
plain markdown files with YAML frontmatter, organized as a navigable graph that
LLMs/agents consume directly — no SDK, no query language. *If you can `cat` a
file you can read it; if you can `git clone` a repo you can ship it.*

(Reference: Google's [OKF spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).)

## Core rules (from OKF)

- Every non-reserved `.md` file is a **concept document** with YAML frontmatter
  delimited by `---`. The only mandatory frontmatter field is **`type`** — a
  short, self-explanatory string.
- Reserved filenames: **`index.md`** (directory listing for progressive
  disclosure), **`log.md`** (changelog), and **`index-compact.md`** (DCA retrieval extension).
- Concepts link to each other with standard markdown links. This catalog uses
  **bundle-relative** targets (leading `/`, e.g. `/marker/port-out/repository.md`).
- Recommended frontmatter: `title`, `description`/body, `resource` (canonical URI
  of the underlying asset), `tags`. Consumers must tolerate unknown fields.
- Broken links are tolerated (they may mark not-yet-written knowledge), though
  this catalog's generator emits only resolving links.

## Two zones

The bundle is one OKF graph split into two zones:

- **Generated zone** — `guide/`, `marker/`, `rule/`, `process/`, `reference/`, `evidence/`.
  Derived from the sources, **wiped and rebuilt on every `generate` run**. Never
  hand-edit (changes are overwritten); edit the source and regenerate.
- **Extensible zone** — `recipe/`, `decision/`, `pitfall/`, `template/`, `note/`.
  Authored by a human or an LLM, **preserved across regeneration**. The node
  *files* are authored; only each directory's `index.md` is regenerated (a
  content catalog scanned from disk). This is the living-wiki layer: query
  answers, playbooks, and decisions accumulate here without re-deriving sources.

Both zones are OKF-conformant (every node carries a non-empty `type`) and link
freely into each other with bundle-relative links.

## Tool-agnostic doctrine

The catalog captures the *pure doctrine* of Domain-Centric Architecture — how
DCA is applied, how marker interfaces make the architecture explicit, what the
rules are and how ArchUnit enforces them — as an instrument for *any* LLM or
agent harness to build and evolve a project by DCA principles with little
context. Tooling consumes the graph; the graph never mentions the tooling: no
node (either zone) may reference Claude Code, the dca-core plugin, the
marketplace, slash commands, or any other specific agent product. Enforced by
`test_bundle_is_tool_agnostic`.

## DCA node types

This profile defines eleven `type` values. All carry `title` and `tags`;
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
- Body: the section's complete markdown (sub-headings, code, lists). Its
  relative links are rewritten onto bundle nodes so the text stays navigable
  inside the bundle; prose and code are otherwise byte-identical to the source.
- Link section: **Related markers** (anchoring to the skeleton).

### `Marker`
A marker interface / annotation from the `dca-building-blocks` library
(`dev.domaincentric.dca.buildingblocks`) — a contract a new application implements.
- `category`: `tactical | strategic | port-in | port-out | application` (bundle taxonomy; stable node paths; `application` = application-layer execution abstractions such as `TransactionBoundary`, which are no ports)
- `package`: the library package the type lives in (`…ddd.tactical`, `…ddd.strategic`,
  `…ddd.strategic.relationships`, `…hexagonal.port.in`, `…hexagonal.port.out`, `…application`)
- `kind`: `interface | class | annotation`
- `signature`: the Java declaration (generics + supertypes)
- `generics`: the type's own type-parameter block, verbatim without brackets, e.g. `T extends AggregateRoot<T, ID>, ID extends Id` (optional)
- `modifiers`: class modifiers such as `[public, abstract]` (class markers only)
- `extends`: supertype marker names (optional)
- `methods`: declared non-private method headers, comments and annotations stripped, `default`/`public`/`static` modifiers and annotation-element defaults kept — e.g. `default boolean sameIdentityAs(T other)`, `String description() default ""` (optional)
- Link sections: **Extends**, **Governed by** (rules), **Discussed in** (the
  guide sections that primarily discuss the marker — title match or dense
  mentions, capped at 10 to stay low-noise).

### `Rule`
One rule of the `dca-archunit` rule library — an enforceable architecture rule.
- `id`: the stable identifier `DCA-<SET>-<NNN>` (shared with every implementation of the
  rule and with violation messages; never renumbered)
- `rule`: the rationale (the `because(...)` text — the *why*)
- `constraint`: the rule as a single-line actionable precondition (the *what*, from the
  title) — what an LLM satisfies while generating; recipes surface these as checklists
- `selects`: which classes the rule looks at — the set the assertion runs over, in terms of the
  layout (`<module>.application..`, "the configured use-case suffix", marker assignability).
  Mandatory; a class outside this set is never reported.
- `checks`: what the rule asserts about each selected class, including what does *not* satisfy
  it and what it deliberately does not establish. Mandatory.
- `enforced_by`: `<RuleSetClass>#<id>`
- `status`: `enforced | informational | retired`
- `rule_set`: the rule set name (`tactical`, `hexagonal`, `contextmap`, …)
- `implementations`: the languages the rule is implemented in (`java`, `dotnet`; read from
  `dca-java/rules.json` and `dca-dotnet/rules.json`). Rules in the `dotnet` rule set
  (`DCA-NET-…`) exist only in .NET.
- `not_applicable_dotnet` (optional): the reason when the .NET library deliberately does not
  port a Java rule (e.g. it only checks a Spring annotation)
- Body, in this order: **Selection** and **Check** (the two texts above as prose); **.NET
  reading** when the .NET library's texts differ from the Java ones; **Implementation** — the
  rule's `DcaRule.of(...)` / `DcaRule.check(...)` expression with its `.selecting(...).checking(...)`
  completion, verbatim, in a fenced block; **Helpers** — every private helper method the
  expression calls, transitively, copied from the rule class or the rules package's shared
  helper classes, one fenced block each; **Architecture queries** — the `DcaArchitecture`
  methods used, by name. A reader of the node needs no source file to predict the rule.
- Link sections: **Applies to markers**, **Configured by** (the two `Reference` nodes).

### `Process`
A how-to for sustaining the architecture's conventions (currently: how to write
an ADR). Body is the procedure + section skeleton.

### `Reference`
One of the two classes every rule is parameterised by, rendered from the Java source
and its .NET twin — never typed by hand, so a default cannot drift from the node.
- `subject`: `layout | architecture`
- `resource`: the Java source; `resource_dotnet`: the C# source (both dropped in mirrors)
- `reference/layout.md` — `DcaLayout`: every setting with default and `with*` override,
  the third-party packages the domain may use, the building-block package constants, the
  derived patterns, the framework annotations (`FrameworkAnnotations.spring()`) — and the same
  for .NET (`ForRootNamespace`, `FrameworkTypes.AspNetCore()`).
- `reference/architecture.md` — `DcaArchitecture`: how bounded contexts (declared),
  the shared kernel and module roots (structural) are discovered, and every public query the
  rules select through, with its javadoc; the .NET API as a table.
- Link section: **See also** (the other reference node). Every Rule node links both under
  **Configured by**; a rule's *Architecture queries* paragraph names the queries it uses.

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
  `anti-corruption-layer`, `package-structure`, `feature`, `naming`, `testing`, `archunit`,
  `spring`, `modulith`, `rest`, `persistence`, `bootstrap`, `cqrs`,
  `event-sourcing`, `security`, `performance`, `migration`, `error-handling`

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

## Frontmatter subset and stable rule identity

Frontmatter is a flat mapping with unique keys (`[A-Za-z_][A-Za-z0-9_-]*`).
Values are single-line plain strings, JSON double-quoted strings, YAML single-quoted
strings (doubled apostrophe escaping), or inline lists of such strings. Quote strings
with YAML syntax. Block lists, nested mappings, block scalars, aliases, anchors,
comments after values, duplicate keys and malformed delimiters are errors, never
silently discarded. Multiline content belongs in the body.

Rule paths are `rule/<set>/<id-lowercase>.md`; the title is an H1 and may change
without moving the node. `redirects.json` records legacy paths as keys and canonical
paths as values. Generation captures existing legacy nodes before replacing the
rule zone and mechanically migrates authored Markdown links; subsequent runs retain
this registry. Lint rejects links to legacy paths even if a file still exists there.

The rules catalog accepts the legacy JSON array or an object with `rules` and
`retired` arrays. Active entries optionally specify `status: enforced|informational`;
absent status retains title/empty-body detection for Java and enforced for .NET-only
rules. The existing .NET `n/a` records remain supported. Retirement entries require
`id`, `reason`, `replacement` (explanatory text), and `since`; ids cannot occur in both
arrays, be duplicated or remain active in another implementation. The merged registry
renders `rule/retired.md` with `#dca-<set>-<nnn>` anchors. No index is emitted when the
registry is absent or empty. Retired ids are never reassigned.

## Review and retrieval profile (2026-09-09)

Authored source revisions live in `authored/<zone>/<slug>.md`; generator copies them to the output before
link migration/indexing. Fresh outputs seed the canonical authored graph so its links resolve. Do not edit
bundle or mirror files. The owning repository's Obsidian import writes authored sources, then generation publishes them.

Authored frontmatter uses `review: draft|reviewed|superseded`, `owner`, `evidence` (flow list of bundle-relative
links), and `superseded_by` (required resolving link for superseded nodes). Missing review/owner/evidence warns;
invalid review or superseded without a successor errors. Draft, missing-review and superseded nodes are non-normative
proposals/history; generation never promotes them. Existing unreviewed material starts as draft. Reviewed nodes
are the explicitly reviewed source revisions, not a claim that every linked draft has been reviewed.
Reviewing follows **use**, not stock: `lint --cited-by <run artefacts>` reports the authored nodes a delivery
run actually leaned on that are still `draft`. A stage that decided a design question from a draft decided it
from a proposal, and the list of nodes worth reading is therefore the list a run cites — not the whole zone.
Templates also carry `applies_to` (languages) and `framework`; these route retrieval and do not add dependencies.

A template is split into a **concept node** and one **code node per language**: `template/<concept>.md` carries the
prose, the `evidence` and the links and holds **no** code fence; `template/<concept>/<language>.md` carries the
skeleton and names its concept node in `parent`. The concept node's `applies_to` is exactly the union of its
children's, so a language the catalog cannot serve is visible in the metadata instead of hidden. The reason for the
split is that the doctrine is language-independent while the code is not: a further language is then one more file,
never a second copy of the prose, and every node that cites a template keeps citing the one concept path. A code
node needs no link into the generated skeleton and no inbound link — its concept node carries both.

`manifest.json` records source Git revisions, source-content SHA256 digests, declared library versions, node counts
and a bundle SHA256 digest, without timestamps. Digest input is sorted relative path + NUL + content + NUL,
excluding manifest.json; markdown resource/resource_dotnet frontmatter is stripped for hashing. Thus canonical
and mirror share the same verifiable digest although only the canonical copy carries local source provenance.
Uncommitted source changes are represented by content digests; a Git revision alone is not a snapshot claim.
Hashed inputs are exactly the files the generator reads (guide chapters without the skipped agent files, `dca-java`
building-block and rule sources plus `rules.json`/`gradle.properties`, `dca-dotnet` rule sources, `*.csproj` and `rules.json`,
the catalog's own `src/` and `authored/`); a sibling revision is the last commit touching those files. The catalog's own
entry carries no revision: the commit that contains the bundle is its revision, and recording the last input-touching
commit would make every commit that lands sources and bundle together stale under the freshness gate.

`rule/index-compact.md` contains id, title, short selects/checks excerpts, languages and status. Search the id's
row before reading the full node. Excerpts are routing aids; full selection/check and caveats remain authoritative.
Shared rules include extracted C# expressions under `.NET reading`; .NET-only rules include C# evidence too.
Nodes over 16,000 bytes retain their full text and gain fence-aware level-three evidence slices under `evidence/`.
Slice paths derive from parent identity and heading, not mutable rule titles. A slice must be read with parent
selection/check and context. A single very large subsection can still exceed the threshold; no summary replaces it.

Only `applicability.py`'s small reviewed rule-to-marker mapping produces `Governed by` / `Applies to markers`.
Tests require a mapped marker to appear in selects; human review establishes positive selection. Prose/code matches,
including exclusions in selects, produce only explicitly labelled `Related mentions (heuristic)` navigation.

Source provenance records the latest commit affecting the hashed input files, rather than repository HEAD. A commit containing only derived outputs therefore leaves provenance stable. Freshness CI checks out full history to resolve those input commits.

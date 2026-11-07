# Changelog

All notable changes to the DCA Knowledge Catalog. The bundle is a generated artifact; entries
record what the *catalog* gained (node types, generator behaviour, authored-zone content), not
every regeneration.

## [Unreleased]

- Added (WP-121): decision *Ownership as a marker* — an aggregate that belongs to someone implements `Owned<OwnerId>`
  and is loaded through its owner (`DCA-TAC-026`, experimental); the owner changes only through an explicit operation
  after the use case proved the right to it, a guest with a pseudonymous identity is an owner, and where the id itself
  is the secret the aggregate is not `Owned`. *Resource id without an owner* links it and no longer leaves an event
  consumer unscoped; *Where authorization and validation live* and *Add an identity port* say the same. The two
  security pitfalls name their OWASP Top 10 category (A01). The aggregate-root and repository templates link the
  decision. One marker node more (`Owned`).
- Added (WP-121 decision 2): `DCA-HEX-020`, the diagnostic for a role read in an incoming adapter's own code, linked
  from *Authenticated is not authorized* and *Where authorization and validation live*; the decision says the
  claims-only gate is declared on the route in the framework's own form.

- Added (WP-186): decision *A yes/no fact or a state* — a single yes/no fact of an aggregate is a `boolean` field it
  changes by its operation and answers by a predicate; a `boolean` parameter is a flag argument; three or more
  states, or transitions with rules, are an enum or a value; independent facts are separate fields; the glossary may
  decide otherwise. *Build DCA without a framework* no longer says a flag is an enum; *Add an aggregate* and *Add a
  value object* link the decision. `DCA-TAC-025` passes a `boolean` field.

- Changed (WP-171): *Failure channel* and *Return expected refusals as a sealed result* separate the system's own
  infrastructure from a foreign system. The own database or broker failing stays an exception; a foreign system — an
  external system on the context map — that refuses, times out or cannot be reached is declared by its output port as
  an `OutputPortException` and answered as a refusal. A "which one, if any" query answers *none* with an empty value;
  "not found" is a refusal only where the caller names a specific thing. The domain-exception and use-case templates
  and *Add an anti-corruption layer* say the same.

- Added (WP-151): pitfall *A command decided on an earlier read* — a choice shown on one request and acted on by the
  next without the command asking the aggregate again; linked from *Where authorization and validation live*
  (discriminator 3 now says the invariant is asked again at the change) and *Remote effect before local preconditions*.
  *Result shape and assembly* gains the outcome sentence: more than two outcomes are one named outcome value, not
  flags and nullables a caller decodes.

- Fixed: the Obsidian graph colors each node by its top-level directory, in the DCA brand palette. The groups matched
  their directory name anywhere in the path, so the 107 evidence nodes under `evidence/rule/` showed as rules and a
  decision named after a rule did too; `evidence/` had no group at all. Each export now rewrites the exporter's own
  groups and keeps any added by hand.

- Changed: a large rule node (above the evidence-slice threshold) keeps what it selects and checks, its .NET reading and
  its links, and leaves its ArchUnit code — the Java expression, its helpers, the C# expression and helpers — to its
  evidence slices, which already held it in full. `dca-use-012` 41 KB → 8 KB, `dca-use-009` 43 → 8, no rule node above
  15 KB. Measured in the todoapp bench: one read of `dca-use-012` was a fifth of all the catalog a session read.

- Changed (WP-77): the repository adapter templates order `findAll` by a sequence column the database assigns on insert
  (JDBC: `sequence … GENERATED ALWAYS AS IDENTITY`, `ORDER BY sequence`; JPA: a read-only `sequence` field and
  `findAllByOrderBySequenceAsc()`; in-memory: a `LinkedHashMap` that keeps insertion order) instead of
  `ORDER BY created_at, id`, whose tie-break is a random UUID for two rows of one instant; the port contract test
  names the two-rows-one-instant case. New pitfall `ordering-by-timestamp`.

- Fixed: the manifest's own-repository entry no longer records a Git revision (the carrying commit is the revision), so a commit
  that lands generator sources or authored nodes together with the regenerated bundle stays fresh under `scripts/check.sh`;
  hashed sibling inputs are narrowed to what the generator reads (guide agent files and `DomainCentric.BuildingBlocks`
  sources excluded). The marketplace-skill assertion in the conformance tests is skipped when no `dca-marketplace`
  checkout sits beside the catalog (CI checks out sources only).

- Stable id-based rule paths, persistent legacy redirects and mechanical authored-link migration.
- Optional status/retirement schema with an anchored retirement registry.
- Strict frontmatter parsing and whole-bundle conformance checks using real authored nodes.

WP-40 B (2026-09-09): `manifest.json` identifies source revisions/content digests and library versions;
resource-normalized bundle digests also verify mirrors. Exact id retrieval starts with `rule/index-compact.md`.
All .NET implementations carry extracted C# evidence; large full nodes gain heading-based `evidence/` slices.
Authored sources carry review/owner/evidence; draft/superseded are non-normative and never auto-promoted.
Template language/framework metadata and both router verification commands prevent incorrect framework routing.
Only the reviewed `applicability.py` mapping creates normative applicability edges; text matching is labelled heuristic.
All edits go through source inputs and generation, including owning-repository Obsidian import.

WP-39: generic invalid-default/reconstitution pitfall and supplied-fact domain-service guidance; Java aggregate-owned event registration reflected from building-blocks 0.2.0. Final verified bundle: 478 nodes, 60 conformance tests.

## [0.1.0] - 2026-09-08

First public version.

- OKF bundle with ten node types: generated `guide/` (full guide text as container + section
  nodes), `marker/`, `rule/` (Java and .NET, ids `DCA-<SET>-<NNN>`, `selects`/`checks` texts
  with embedded helpers), `process/`, `reference/` (`DcaLayout`, `DcaArchitecture`); authored
  `recipe/`, `decision/`, `pitfall/`, `template/`, `note/` that survive regeneration.
- Deterministic stdlib-only generator (`dca_catalog.generate`), linter (`dca_catalog.lint`),
  read-only mirror for consuming projects (`dca_catalog.mirror`), Obsidian export/import.
- Conformance tests: link integrity, idempotence, tool-agnostic bodies, no outward links, no
  citations of reference-implementation ADRs, ASCII-only file names.
- CI gate (`.github/workflows/check.yml`) that checks out the source repositories as siblings and
  fails when the committed bundle is stale.

Source provenance records the latest commit affecting the hashed input files, rather than repository HEAD. A commit containing only derived outputs therefore leaves provenance stable. Freshness CI checks out full history to resolve those input commits.

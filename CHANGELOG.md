# Changelog

All notable changes to the DCA Knowledge Catalog. The bundle is a generated artifact; entries
record what the *catalog* gained (node types, generator behaviour, authored-zone content), not
every regeneration.

## [Unreleased]

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

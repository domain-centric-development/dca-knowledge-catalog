# Changelog

All notable changes to the DCA Knowledge Catalog. The bundle is a generated artifact; entries
record what the *catalog* gained (node types, generator behaviour, authored-zone content), not
every regeneration.

## [Unreleased]

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

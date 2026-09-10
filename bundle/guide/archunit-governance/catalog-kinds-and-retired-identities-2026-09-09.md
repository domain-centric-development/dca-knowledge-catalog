---
type: Section
title: "Catalog kinds and retired identities (2026-09-09)"
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: dca-guide/archunit-governance.md
tags: [guide, section]
---

Catalog entries distinguish enforced rules from informational diagnostics: LAY-001, STR-001, STR-010, MAP-013,
and Java NAM-002. Test runners and generated catalogs report both counts separately. Informational entries do
not prove architectural correctness or runtime wiring. `kind()` / `Kind` is explicit metadata, independent of severity.

Retired ids are never reused: MAP-003 delegates normalized-name collision handling to the context-map renderer;
ADV-003 is covered by ADV-001's immutable-shape check; TAC-022 is covered by TAC-008..012 for value models,
with enrichment guidance in the guide/catalog. `DcaRules.retired()` / `Retired()` retain reason, replacement and
version. Properties exclusions/severity settings and programmatic exclusions using these ids keep loading and
are reported as retired. Unknown ids still fail. The change is intentional in unreleased 0.4.0 for 0.3.0 consumers.

USE-001 retains consumer redeclaration coverage; LAY-005 checks imported consumer implementations in the reserved
building-blocks output-port namespace/package. An imported original interface passes. Name-discovery rules remain:
unmarked types would otherwise evade marker-only selection. Current counts come from generated `rules.json`,
including status and the separate retirement registry, rather than a hard-coded expected total.

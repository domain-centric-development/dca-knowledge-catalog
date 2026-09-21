---
type: Reference
title: Core Rule Categories — Overview
tags: [reference]
evidence_for: /guide/archunit-governance/core-rule-categories.md
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md). This is an evidence excerpt; retain the parent selection and caveats.

Each category below corresponds to one or more rule sets of the library (`layered`/`onion`, `hexagonal`,
`tactical`, `strategic`, `naming`, `cycles`, `contextmap`, `errors`, …). The code is what the library runs,
written out in plain ArchUnit so you can read what a rule checks — and copy its shape for a rule of
your own.

**Two ArchUnit conveniences are deliberately not used.** `layeredArchitecture()` is reported as a
diagnostic only (`DCA-LAY-001`) because traditional layering contradicts Ports and Adapters — see
that rule's rationale. `onionArchitecture()` is not used either: it implements Palermo's rings
literally, with a fixed placement for domain model, domain services, application services and
adapters. DCA keeps Palermo's claim that all coupling points inward and leaves the filing inside a
layer to the team, so `DCA-ONI-001/002/003` check the dependency direction and the domain's freedom
from framework metadata instead of a ring layout.

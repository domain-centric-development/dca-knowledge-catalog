---
type: Section
title: Onion Architecture
chapter: "References & Further Reading"
source: guide
resource: dca-guide/architecture/references.md
tags: [guide, section]
---

The `onion` rule set (`DCA-ONI-*`) is named after this pattern. DCA keeps its central claim — all
coupling points inward, the domain model at the centre — and does not encode the ring layout itself;
`DCA-ONI-001/002/003` check the dependency direction and the domain's freedom from framework
metadata. Palermo's first ring is also the published support for putting repository *interfaces*
inside the application boundary rather than in infrastructure, which DCA otherwise presents only as
a deviation from Evans and Vernon.

**Articles:**
- **[The Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)** by Jeffrey Palermo (2008)
  - Four-part series; coupling toward the centre, domain model innermost, infrastructure outermost
  - ArchUnit's own `onionArchitecture()` implements these rings — deliberately not used here, see
    `topics/archunit-governance.md`

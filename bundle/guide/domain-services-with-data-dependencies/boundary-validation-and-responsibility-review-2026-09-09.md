---
type: Section
title: "Boundary validation and responsibility (review 2026-09-09)"
chapter: Domain Services with Data Dependencies
source: guide
resource: dca-guide/domain-services-with-data-dependencies.md
tags: [guide, section]
---

State the numeric range and rounding of every monetary value object. Validate invalid defaults at entry and
reconstitution boundaries: a readonly struct can be default-created without its constructor. Reconstitution suppresses
creation events, not representation invariants. Return immutable collection snapshots when an earlier observation
must remain stable after a later aggregate mutation.

Aggregates answer from their own state. The use case retrieves external facts through ports; domain services combine
supplied immutable snapshots, with no repository or remote-port parameter. Moving a resolver/callback from a field to
a method argument does not transfer that business responsibility into the aggregate. A domain-owned gateway needs
an explicit rationale; local password hashing is an example of a computational capability, not a remote lookup.
Keep presentation enrichment separate. Field/dependency rules cannot prove semantic placement, so callback parameters
remain a manual review item.

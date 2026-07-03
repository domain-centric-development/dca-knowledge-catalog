---
type: ADR
title: "ADR-015: ArchUnit for Architecture Governance"
adr: 15
status: accepted
pattern: Use ArchUnit to automatically enforce architectural rules as executable tests.
resource: ai-architecture-sample/docs/architecture/adr/adr-015-archunit-governance.md
tags: [adr]
---

Use ArchUnit to automatically enforce architectural rules as executable tests.

**Consequences:** Automated Enforcement · Fast Feedback · Living Documentation · Prevent Erosion · No Manual Reviews · Onboarding · None identified

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Specification<T>](/marker/tactical/specification.md)

## Enforced by

- [Domain must not access Application Services (Onion Architecture - Domain is innermost layer)](/rule/onion/domain-must-not-access-application-services-onion-architecture-domain-is-innermost-layer.md)
- [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/aggregate-roots-must-not-have-fields-with-other-aggregate-root-types.md)
- [Entities must have an ID field](/rule/tactical/entities-must-have-an-id-field.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)

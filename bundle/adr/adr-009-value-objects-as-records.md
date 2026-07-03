---
type: ADR
title: "ADR-009: Value Objects as Java Records"
adr: 9
status: accepted
pattern: Value Objects SHOULD be implemented as Java records whenever possible.
resource: ai-architecture-sample/docs/architecture/adr/adr-009-value-objects-as-records.md
tags: [adr, value-object]
---

Value Objects SHOULD be implemented as Java records whenever possible.

**Consequences:** Less Boilerplate · Immutability Guaranteed · Value Equality · Clear Intent · Thread-Safe · Modern Java · None for value objects

## Applies to markers

- [Factory](/marker/tactical/factory.md)

## Enforced by

- [Value Object classes should be final (immutability)](/rule/tactical/value-object-classes-should-be-final-immutability.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)

---
type: Marker
title: Store
category: port-out
kind: interface
signature: public interface Store extends OutputPort
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
extends: [OutputPort]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/Store.java
tags: [port-out, marker]
---

Marker interface for Stores — output ports that record or query operational data without an own
aggregate lifecycle.

**Repository vs. Store:**

- Use `y` for **Aggregate Roots** with identity and lifecycle (findById,
save, delete).
- Use `e` for **Value Objects, Events, or operational data** without aggregate
lifecycle (record, count, exists, lookup by key).

**Examples of Stores:**

- `LoginProtectionStore` — records login attempts; queries failure counts
- `AuditLogStore` — appends audit entries; queries by time range
- `EventStore` (Event Sourcing) — specialization for Domain Events

**Rules of thumb:**

- Lookup by key (`findById()`) is allowed on a Store; aggregate lifecycle requires a
Repository
- Need `record()` or `count()`? → `e` (object is recorded, not managed)
- In doubt: if the stored object is a `Value` or a record, it's almost always a Store.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Deviations from the literature](/guide/readme/deviations-from-the-literature.md)
- [Rules of thumb](/guide/repository-vs-store/rules-of-thumb.md)
- [Store](/guide/repository-vs-store/store.md)

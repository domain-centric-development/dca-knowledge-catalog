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
- Use `e` for **Value Objects, Events, or operational data** without
identity-based access (record, count, exists).

**Examples of Stores:**

- `LoginProtectionStore` — records login attempts; queries failure counts
- `AuditLogStore` — appends audit entries; queries by time range
- `EventStore` (Event Sourcing) — specialization for Domain Events

**Rules of thumb:**

- Need `findById()`? → `y` (object has identity)
- Need `record()` or `count()`? → `e` (object is recorded, not managed)
- In doubt: if the stored object is a `Value` or a record, it's almost always a Store.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Store implementations must reside in the adapter.outgoing package](/rule/tactical/store-implementations-must-reside-in-the-adapter-outgoing-package.md)
- [Store interfaces must extend the Store marker, not Repository](/rule/tactical/store-interfaces-must-extend-the-store-marker-not-repository.md)
- [Store interfaces must not declare findById or save methods](/rule/tactical/store-interfaces-must-not-declare-findbyid-or-save-methods.md)
- [Store interfaces must reside in the application layer's shared output-port package](/rule/tactical/store-interfaces-must-reside-in-the-application-layer-s-shared-output-port-package.md)
- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)

## Discussed in

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [DEVIATIONS FROM THE LITERATURE](/guide/readme/deviations-from-the-literature.md)
- [ELEMENTS](/guide/readme/elements.md)
- [RULES](/guide/readme/rules.md)

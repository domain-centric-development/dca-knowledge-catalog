---
type: Note
title: "The Store marker has no governing ArchUnit rules (governance gap)"
tags: [note, governance, archunit, port-out, persistence]
---

The [Store marker](/marker/port-out/store.md) (`Store extends OutputPort`) is documented in the book
([Stores: persistence for non-aggregate data](/book/06-application-layer/stores-persistence-for-non-aggregate-data.md))
and in the guide's Repository-vs-Store section, and it is used in the reference
implementation (`EventPublicationLogStore extends Store`). But unlike
[Repository](/marker/port-out/repository.md) — which carries a full rule set — **no ArchUnit rule
governs Store today**. Nothing mechanically enforces:

1. `*Store` interfaces extend the `Store` marker (not `OutputPort` directly, not `Repository`).
2. Stores do not expose aggregate-lifecycle methods (`findById`, `save`, `delete`) —
   that shape belongs to a Repository per
   [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md).
3. Store implementations live in `adapter/outgoing/`, the interface in `application/shared/`.

Until such rules exist, the doctrine is only documented, not enforced — an LLM or
developer can violate it without `./gradlew test-architecture` failing. When rules are
added to the sample, regenerate the catalog; the Store marker's `Governed by` section
will pick them up automatically.

## Anchors

- Marker: [Store](/marker/port-out/store.md) · [OutputPort](/marker/port-out/outputport.md)
- Decision: [Repository vs Store](/decision/repository-vs-store.md)
- Pitfall: [A Repository for a non-aggregate](/pitfall/repository-for-non-aggregate.md)
- Rule (the Repository-side counterpart): [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)

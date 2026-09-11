---
type: Template
title: "Store skeleton (output port + in-memory outgoing adapter)"
tags: [template, application, port-out, persistence]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/store.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-018.md, /rule/tactical/dca-tac-019.md, /rule/tactical/dca-tac-020.md, /rule/tactical/dca-tac-021.md, /guide/elements.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **Store**: the output port for operational data that has **no aggregate lifecycle** — login attempts, an audit trail, metric snapshots, an event log. Structurally parallel to the [repository template](/template/repository-with-in-memory-adapter.md), but the vocabulary is `record` / `count` / `exists` / query-by-criteria instead of `findById` / `save` / `deleteById`, because the data is *recorded*, not loaded-mutated-saved by identity. The **interface** lives in `application/shared/` and extends the `Store` marker; the **implementation** is a secondary (outgoing) adapter in `adapter/outgoing/persistence/`. Choose Store vs Repository with the [repository-vs-store decision](/decision/repository-vs-store.md) — rule of thumb: need `findById()`? Repository. Need `record()` or `count()`? Store. Replace `{Name}` (the concern) / `{context}` / `{basePackage}` and the entry type.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`store-with-in-memory-adapter/java.md`](/template/store-with-in-memory-adapter/java.md)

## Realizes / governed by

- Marker: [Store](/marker/port-out/store.md) · [OutputPort](/marker/port-out/outputport.md)
- Decisions: [Repository or Store: which output port persists this](/decision/repository-vs-store.md)
- Rules: [extends the Store marker](/rule/tactical/dca-tac-018.md) · [interface in application.shared](/rule/tactical/dca-tac-019.md) · [implementation in adapter.outgoing](/rule/tactical/dca-tac-020.md) · [no findById/save](/rule/tactical/dca-tac-021.md)
- Pitfall: [Repository for a non-aggregate](/pitfall/repository-for-non-aggregate.md) — the mistake this template avoids
- Guide: [Layer elements](/guide/elements.md)
- Sibling template: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)
- Recipe: [Add a store](/recipe/add-a-store.md)

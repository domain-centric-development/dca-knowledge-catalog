---
type: Template
title: "Enriched domain model skeleton (read model combining aggregate + cross-context data)"
tags: [template, domain, value-object, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/value.md, /guide/readme/integration-patterns.md, /guide/readme/elements.md, /guide/readme/java-package-structure.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for an **enriched domain model**: an immutable read model that combines one aggregate's state with fresh data fetched from *other* bounded contexts, and owns the business rules that need data from more than one context. It is a **Value Object** — it implements `Value`, lives in `{context}.domain.model/` next to the aggregate it enriches, has **no identity, no lifecycle, and raises no events**. Assembly happens through a **static factory** that takes the aggregate plus the external data; the aggregate never learns about the external concepts, so bounded-context isolation stays intact. Use this when a read must show aggregate state together with, e.g., current price (Pricing) or stock (Inventory), or must compare persisted vs. current values. Replace `{Name}` (aggregate) / `{context}` / `{basePackage}` / `{External}` (the cross-context data carrier).

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`enriched-domain-model/java.md`](/template/enriched-domain-model/java.md)

## Realizes / governed by

- Marker: [Value](/marker/tactical/value.md)
- Guide: [Enriched Read Model Pattern](/guide/readme/integration-patterns.md) · [Layer elements](/guide/readme/elements.md) · [Java package structure](/guide/readme/java-package-structure.md)
- Related template: [ViewModel](/template/view-model.md)
- Related decision: [Plain query use case or a dedicated read model](/decision/read-model-vs-domain-query.md)

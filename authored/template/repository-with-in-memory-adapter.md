---
type: Template
title: "Repository skeleton (output port + in-memory outgoing adapter)"
tags: [template, application, repository]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /marker/port-out/repository.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md, /rule/tactical/dca-tac-015.md, /rule/tactical/dca-tac-016.md, /rule/naming/dca-nam-004.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a repository: the collection-like output port for one aggregate root. The **interface** is an output port that lives in `application/shared/` and extends `Repository<T, ID>`; the **implementation** is a secondary (outgoing) adapter in `adapter/outgoing/persistence/`. One repository per aggregate root — never per entity. Method names use the ubiquitous language, not generic CRUD. Replace `{Name}` (aggregate) / `{context}` / `{basePackage}`. This template uses a `ConcurrentHashMap` store to match the reference implementation; swap it for a database adapter without touching the port.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`repository-with-in-memory-adapter/java.md`](/template/repository-with-in-memory-adapter/java.md)

## Realizes / governed by

- Marker: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/dca-tac-013.md) · [Repository Interfaces must reside in application output port package](/rule/tactical/dca-tac-014.md) · [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/dca-tac-015.md) · [Repositories must only exist for Aggregate Roots](/rule/tactical/dca-tac-016.md) · [Repository Interfaces must end with 'Repository'](/rule/naming/dca-nam-004.md)
- Guide: [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer rules](/guide/rules.md) · [Port placement](/guide/quick-reference/port-placement.md)
- Recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md) · [Add a bulk operation](/recipe/add-a-bulk-operation.md)
- Sibling template: [Aggregate root skeleton](/template/aggregate-root.md) — where `reconstitute` comes from
- Pitfall: [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)

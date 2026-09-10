---
type: Template
title: "JPA repository adapter (same output port, Spring Data + entity + mapper)"
tags: [template, adapter, persistence, repository]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/repository.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md, /rule/tactical/dca-tac-015.md, /rule/tactical/dca-tac-016.md, /rule/tactical/dca-tac-017.md, /rule/hexagonal/dca-hex-005.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **JPA outgoing adapter** that implements the *same* `{Name}Repository` output port as the [in-memory adapter](/template/repository-with-in-memory-adapter.md). The port and the domain aggregate do not change — only the outgoing adapter is swapped. Three collaborators live behind the boundary in `adapter/outgoing/persistence/jpa/`: a `@Entity` mapping class **separate** from the domain aggregate (so the domain stays persistence-free — the central DCA point), a Spring Data `JpaRepository` interface, and the adapter class that maps between aggregate and entity and implements the port. Replace `{Name}` (aggregate) / `{name}` / `{context}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`jpa-repository-adapter/java.md`](/template/jpa-repository-adapter/java.md)

## Realizes / governed by

- Marker: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/dca-tac-013.md) · [Repository Interfaces must reside in application output port package](/rule/tactical/dca-tac-014.md) · [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/dca-tac-015.md) · [Repositories must only exist for Aggregate Roots](/rule/tactical/dca-tac-016.md) · [Repository methods must not return non-root Entities](/rule/tactical/dca-tac-017.md) · [Outgoing adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-005.md)
- Guide: [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer rules](/guide/readme/rules.md)
- Sibling templates: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md) · [Aggregate root skeleton](/template/aggregate-root.md) — where `reconstitute` comes from
- Pitfall: [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)
- Recipe: [Swap the in-memory adapter for JPA](/recipe/swap-in-memory-for-jpa.md) · [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)

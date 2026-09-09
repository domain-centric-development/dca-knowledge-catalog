---
type: Recipe
title: Bootstrap a new application
tags: [recipe, strategic, bootstrap]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/archunit-governance/core-rule-categories.md, /rule/usecase/dca-use-001.md, /rule/layered/dca-lay-001.md, /rule/strategic/dca-str-002.md, /rule/layered/dca-lay-005.md, /rule/naming/dca-nam-009.md, /marker/port-in/inputport.md, /marker/port-out/outputport.md]
---

Stand up a fresh Domain-Centric Architecture app from nothing: the building-block dependencies, the package skeleton, the rule catalog as a test, and the first bounded context. Get the guardrails in place *before* the domain code, so the rules are green from commit one.

## Steps

1. **Add the building blocks** — the marker interfaces (`InputPort`, `UseCase`, `OutputPort`, `Repository`, `DomainEvent`, `Value`, `@BoundedContext`, …) are a published dependency, never project code: Java `dev.domaincentric:dca-building-blocks` (packages `ddd.tactical`, `ddd.strategic`, `hexagonal.port.in/.out`, `application`), .NET `DomainCentric.BuildingBlocks`. On Spring add `dev.domaincentric:dca-spring` as well — it implements `DomainEventPublisher` and `TransactionBoundary` and auto-configures both. The project's own `sharedkernel/` then holds only universal value objects under `domain/model/` and application-specific shared ports under `application/shared/`; it depends on no bounded context and is annotated `@SharedKernel`.
2. **Lay the package skeleton** — the four-layer template per context (`domain/`, `application/` + `shared/`, `adapter/incoming|outgoing/`, optional `infrastructure/`) and a global `infrastructure/` for cross-cutting config. Package by domain concept.
3. **Add the rule catalog as a test** — `dev.domaincentric:dca-archunit` in the architecture test source set and one class `ArchitectureTest extends DcaArchitectureTest` returning the project's `DcaLayout`; `dca-archunit.properties` scopes and tunes the rules ([Core rule categories](/guide/archunit-governance/core-rule-categories.md) explain what they check). With Spring Modulith, `dev.domaincentric:dca-archunit-spring-modulith` and a second class `ModulithTest extends DcaSpringModulithTest`. Start with the full catalog; scope rule subsets per context by subdomain type later.
3a. **Make transactions real before the first write use case** — an in-memory start has no transaction manager, and `@Transactional` is then silently inert while every rule stays green. Add `spring-boot-transaction`, a `PlatformTransactionManager` bean of your own (a visible placeholder until persistence arrives) and, with Modulith, `spring-modulith-events-api` — see [Declarative transaction without a transaction manager](/pitfall/declarative-transaction-without-a-transaction-manager.md).
4. **Set up ADRs** — copy the ADR template and record the foundational decisions (hexagonal architecture, shared kernel, ArchUnit governance, pattern selection). See [How to write an ADR](/process/creating-an-adr.md).
5. **Add the first bounded context** — classify its subdomain, then follow [Add a bounded context](/recipe/add-a-bounded-context.md) and seed one vertical slice with [Add a use case](/recipe/add-a-use-case.md).
6. **Verify** — `./gradlew build && ./gradlew test-architecture`; the suite is green on an empty-but-correct skeleton.

## Rules to satisfy (build-time checklist)

- [The base InputPort interface must be in the building-blocks port-in package](/rule/usecase/dca-use-001.md)
- [The rules of the layered architecture should be followed](/rule/layered/dca-lay-001.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/dca-str-002.md)
- [The shared kernel's output-port markers must all be interfaces](/rule/layered/dca-lay-005.md)
- [No technical bucket packages — package by domain concept](/rule/naming/dca-nam-009.md)

## Anchors

- Process: [How to write an ADR](/process/creating-an-adr.md)
- Markers: [InputPort](/marker/port-in/inputport.md) · [OutputPort](/marker/port-out/outputport.md) · [@SharedKernel](/marker/strategic/sharedkernel.md) · [@BoundedContext](/marker/strategic/boundedcontext.md)
- Pitfall: [Declarative transaction without a transaction manager](/pitfall/declarative-transaction-without-a-transaction-manager.md)
- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [ArchUnit adoption path](/guide/archunit-governance/adoption-path-tiers.md) · [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md) · [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md) · [Core rule categories](/guide/archunit-governance/core-rule-categories.md) · [Context-specific rule sets](/guide/archunit-governance/context-specific-rule-sets.md) · [Layer elements](/guide/readme/elements.md)
- Then grow it: [Build a DCA application](/recipe/build-a-dca-application.md) (the task router) · [Add a bounded context](/recipe/add-a-bounded-context.md) · [Add a use case](/recipe/add-a-use-case.md)
- Decision: [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)
- Starter files: [Project starter — agent instructions](/template/project-starter-agent-instructions.md) — wires the coding agent to this catalog

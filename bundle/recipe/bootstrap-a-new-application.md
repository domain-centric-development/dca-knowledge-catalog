---
type: Recipe
title: "Bootstrap a new application"
tags: [recipe, strategic, bootstrap]
---

Stand up a fresh Domain-Centric Architecture app from nothing: the shared-kernel marker contracts, the package skeleton, the ArchUnit governance suite, and the first bounded context. Get the guardrails in place *before* the domain code, so the rules are green from commit one. (The `dca-bootstrap` plugin skill automates this, but the steps are tool-agnostic.)

## Steps

1. **Create the shared kernel** — a `sharedkernel/` package holding the marker interfaces (`InputPort`, `UseCase`, `OutputPort`, `Repository`, `DomainEvent`, `Value`, …) under `marker/port/in`, `marker/port/out`, `marker/tactical`, `marker/strategic`, plus universal value objects under `domain/model/`. The shared kernel depends on no bounded context. Annotate it `@SharedKernel`.
2. **Lay the package skeleton** — the four-layer template per context (`domain/`, `application/` + `shared/`, `adapter/incoming|outgoing/`, optional `infrastructure/`) and a global `infrastructure/` for cross-cutting config. Package by domain concept.
3. **Add the ArchUnit suite** — wire the governance rules that enforce the layering, naming, and isolation contracts so architecture erosion fails the build ([ADR-015](/adr/adr-015-archunit-governance.md)). Start with the full suite; scope rule subsets per context by subdomain type later.
4. **Set up ADRs** — copy the ADR template and record the foundational decisions (hexagonal architecture, shared kernel, ArchUnit governance, pattern selection). See [How to write an ADR](/process/creating-an-adr.md).
5. **Add the first bounded context** — classify its subdomain, then follow [Add a bounded context](/recipe/add-a-bounded-context.md) and seed one vertical slice with [Add a use case](/recipe/add-a-use-case.md).
6. **Verify** — `./gradlew build && ./gradlew test-architecture`; the suite is green on an empty-but-correct skeleton.

## Rules to satisfy (build-time checklist)

- [The base InputPort interface must be in the sharedkernel marker port-in package](/rule/usecase/base-inputport-interface-must-be-in-sharedkernel-marker-port-in-package.md)
- [The rules of the layered architecture should be followed](/rule/layered/the-rules-of-the-layered-architecture-should-be-followed.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/shared-kernel-must-not-have-dependencies-on-any-bounded-context.md)
- [sharedkernel.application.port should only contain interfaces (outbound ports)](/rule/layered/sharedkernel-application-port-should-only-contain-interfaces-outbound-ports.md)
- [No technical bucket packages — package by domain concept](/rule/naming/no-technical-bucket-packages-package-by-domain-concept.md)

## Anchors

- Process: [How to write an ADR](/process/creating-an-adr.md)
- Markers: [InputPort](/marker/port-in/inputport.md) · [OutputPort](/marker/port-out/outputport.md) · [@SharedKernel](/marker/strategic/sharedkernel.md) · [@BoundedContext](/marker/strategic/boundedcontext.md)
- ADRs: [ADR-007 Hexagonal Architecture](/adr/adr-007-hexagonal-architecture.md) · [ADR-016 Shared Kernel Pattern](/adr/adr-016-shared-kernel-pattern.md) · [ADR-015 ArchUnit Governance](/adr/adr-015-archunit-governance.md) · [ADR-025 Pattern Selection per Subdomain](/adr/adr-025-pattern-selection-per-subdomain.md)
- Book: [Project setup](/book/03-getting-started/step-1-project-setup.md) · [High-level structure](/book/09-package-structure/high-level-structure.md) · [Base port interfaces](/book/11-shared-kernel/base-port-interfaces.md) · [Marker interfaces](/book/11-shared-kernel/marker-interfaces.md)
- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [ArchUnit adoption path](/guide/archunit-governance/adoption-path-tiers.md)
- Then grow it: [Build a DCA application](/recipe/build-a-dca-application.md) (the task router) · [Add a bounded context](/recipe/add-a-bounded-context.md) · [Add a use case](/recipe/add-a-use-case.md)
- Decision: [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)
- Starter files: [Project starter — CLAUDE.md + conventions](/template/project-starter-claude-md.md) — wires the coding agent to this catalog

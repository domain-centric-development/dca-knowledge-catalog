---
type: Marker
title: "Specification<T>"
category: tactical
kind: interface
signature: "public interface Specification<T>"
methods: ["boolean isSatisfiedBy(T candidate)"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/Specification.java
tags: [tactical, marker]
---

Marker interface for Specifications.

## Governed by

- [Specifications must end with 'Specification'](/rule/advanced/specifications-must-end-with-specification.md)
- [Specifications must not have Spring annotations](/rule/advanced/specifications-must-not-have-spring-annotations.md)

## Referenced by ADRs

- [ADR-002: Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- [ADR-013: Specification Pattern for Business Rules](/adr/adr-013-specification-pattern.md)
- [ADR-015: ArchUnit for Architecture Governance](/adr/adr-015-archunit-governance.md)
- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)

## Discussed in

- [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md)
- [Shared Kernel Structure](/book/11-shared-kernel/shared-kernel-structure.md)
- [Specification Pattern](/book/11-shared-kernel/specification-pattern.md)
- [Tactical DDD Patterns](/book/appendix-a-glossary/tactical-ddd-patterns.md)
- [Domain Layer Examples](/book/appendix-b-reference-implementation/domain-layer-examples.md)
- [Common Patterns](/book/appendix-d-cheat-sheet/common-patterns.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)

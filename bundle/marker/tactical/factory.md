---
type: Marker
title: Factory
category: tactical
kind: interface
signature: public interface Factory
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/Factory.java
tags: [tactical, marker]
---

Marker interface for Factories.

## Governed by

- [Factories must not have Spring annotations](/rule/advanced/factories-must-not-have-spring-annotations.md)
- [Factories must reside in domain package](/rule/advanced/factories-must-reside-in-domain-package.md)
- [Factories should be stateless (only final fields for dependencies)](/rule/advanced/factories-should-be-stateless-only-final-fields-for-dependencies.md)
- [Factories should implement Factory Marker Interface](/rule/advanced/factories-should-implement-factory-marker-interface.md)
- [Enriched Domain Models must be Value Object records](/rule/tactical/enriched-domain-models-must-be-value-object-records.md)

## Referenced by ADRs

- [ADR-002: Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- [ADR-009: Value Objects as Java Records](/adr/adr-009-value-objects-as-records.md)
- [ADR-014: Factory Pattern for Complex Aggregate Creation](/adr/adr-014-factory-pattern.md)
- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)
- [ADR-021: Enriched Domain Model Pattern](/adr/adr-021-enriched-domain-model-pattern.md)
- [ADR-022: ViewModel Pattern for Web Adapters](/adr/adr-022-viewmodel-pattern.md)

## Discussed in

- [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md)
- [Cross-Context Communication](/book/10-bounded-contexts/cross-context-communication.md)
- [Common Patterns](/book/appendix-d-cheat-sheet/common-patterns.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)

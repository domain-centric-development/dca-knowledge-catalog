---
type: Marker
title: DomainService
category: tactical
kind: interface
signature: public interface DomainService
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/DomainService.java
tags: [tactical, marker]
---

Marker interface for Domain Services.

## Governed by

- [Domain Services must implement DomainService Marker Interface and reside in domain.service](/rule/advanced/domain-services-must-implement-domainservice-marker-interface-and-reside-in-domain-service.md)
- [Domain Services must not have Spring annotations](/rule/advanced/domain-services-must-not-have-spring-annotations.md)
- [Domain Services must reside in domain package](/rule/advanced/domain-services-must-reside-in-domain-package.md)
- [Domain Services should be stateless (only final fields for dependencies)](/rule/advanced/domain-services-should-be-stateless-only-final-fields-for-dependencies.md)

## Discussed in

- [Ansatz 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/ansatz-1-domaingateway-pattern.md)
- [Ansatz 2: Strategy/Callback Pattern](/guide/domain-services-with-data-dependencies/ansatz-2-strategy-callback-pattern.md)
- [Default-Regel: Pure Domain Services (90% der Fälle)](/guide/domain-services-with-data-dependencies/default-regel-pure-domain-services-90-der-fälle.md)
- [Problemstellung](/guide/domain-services-with-data-dependencies/problemstellung.md)
- [Vergleich: Wann welchen Ansatz nutzen](/guide/domain-services-with-data-dependencies/vergleich-wann-welchen-ansatz-nutzen.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)

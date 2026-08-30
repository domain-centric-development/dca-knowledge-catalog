---
type: Marker
title: TransactionBoundary
category: application
kind: interface
signature: public interface TransactionBoundary
package: dev.domaincentric.dca.buildingblocks.application
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/application/TransactionBoundary.java
tags: [application, marker]
---

Explicit transaction boundary inside a use case — an application-layer execution abstraction, not an output port.

## Governed by

- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md)
- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-have-a-transaction-boundary.md)

## Discussed in

- [RULES](/guide/readme/rules.md)

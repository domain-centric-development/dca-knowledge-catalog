---
type: Marker
title: UnitOfWork
category: port-out
kind: interface
signature: public interface UnitOfWork extends OutputPort
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
extends: [OutputPort]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/UnitOfWork.java
tags: [port-out, marker]
---

Output port for an explicit transaction boundary inside a use case.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Transactional use cases must not call remote-capable output ports](/rule/usecase/transactional-use-cases-must-not-call-remote-capable-output-ports.md)
- [Use cases that publish domain events must run inside a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-run-inside-a-transaction-boundary.md)

## Discussed in

- [RULES](/guide/readme/rules.md)

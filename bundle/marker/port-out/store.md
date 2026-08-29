---
type: Marker
title: Store
category: port-out
kind: interface
signature: public interface Store extends OutputPort
package: dev.domaincentric.dca.buildingblocks.hexagonal.port.out
extends: [OutputPort]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/hexagonal/port/out/Store.java
tags: [port-out, marker]
---

Marker interface for Stores — output ports that record or query operational data without an own aggregate lifecycle.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Store implementations must reside in the adapter.outgoing package](/rule/tactical/store-implementations-must-reside-in-the-adapter-outgoing-package.md)
- [Store interfaces must extend the Store marker, not Repository](/rule/tactical/store-interfaces-must-extend-the-store-marker-not-repository.md)
- [Store interfaces must reside in the application layer's shared output-port package](/rule/tactical/store-interfaces-must-reside-in-the-application-layer-s-shared-output-port-package.md)

## Discussed in

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [DEVIATIONS FROM THE LITERATURE](/guide/readme/deviations-from-the-literature.md)
- [ELEMENTS](/guide/readme/elements.md)

---
type: Marker
title: "BaseAggregateRoot<T, ID>"
category: tactical
kind: class
signature: "public abstract class BaseAggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> implements AggregateRoot<T, ID>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
extends: [AggregateRoot]
methods: ["throw new IllegalArgumentException(\"Domain event cannot be null\")"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/BaseAggregateRoot.java
tags: [tactical, marker]
---

Abstract base class for Aggregate Roots providing domain event collection.

## Extends

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

---
type: Marker
title: "Entity<T, ID>"
category: tactical
kind: interface
signature: "public interface Entity<T extends Entity<T, ID>, ID extends Id>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
methods: ["ID id()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/Entity.java
tags: [tactical, marker]
---

Marker for Entity.

## Governed by

- [Domain model classes must not have public setter methods](/rule/tactical/domain-model-classes-must-not-have-public-setter-methods.md)
- [Entities must have an ID field](/rule/tactical/entities-must-have-an-id-field.md)
- [Repository methods must not return non-root Entities](/rule/tactical/repository-methods-must-not-return-non-root-entities.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Framework Annotations Rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Complete Test Suites](/guide/archunit-governance/complete-test-suites.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)

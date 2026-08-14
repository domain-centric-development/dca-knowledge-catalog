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

## Discussed in

- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)

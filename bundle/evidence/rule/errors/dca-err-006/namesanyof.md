---
type: Reference
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures — `namesAnyOf`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-006.md#namesanyof"
---

[Full node and context](/rule/errors/dca-err-006.md#namesanyof). This is an evidence excerpt; retain the parent selection and caveats.

### `namesAnyOf`

```java
/**
   * Whether the class refers to one of the named classes — through the import model, or through its
   * class file's constant pool, which also holds the case types of a pattern-matching switch that
   * the import model leaves out.
   */
  private static boolean namesAnyOf(JavaClass type, Set<String> names) {
    if (names.isEmpty()) {
      return false;
    }
    if (type.getDirectDependenciesFromSelf().stream()
        .anyMatch(dependency -> names.contains(dependency.getTargetClass().getName()))) {
      return true;
    }
    return ClassFileReferences.of(type)
        .map(referenced -> referenced.stream().anyMatch(names::contains))
        .orElse(false);
  }
```

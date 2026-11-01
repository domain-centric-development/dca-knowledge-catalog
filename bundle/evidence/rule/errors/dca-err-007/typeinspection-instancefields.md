---
type: Reference
title: "Diagnostic: failures that carry display data or objects instead of ids and figures — `TypeInspection.instanceFields`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-007.md#typeinspectioninstancefields"
---

[Full node and context](/rule/errors/dca-err-007.md#typeinspectioninstancefields). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.instanceFields`

```java
/**
   * The instance fields of a class, inherited ones included, sorted by name so that reports are
   * stable across runs. Static fields — constants, counters — are not part of an object's state.
   */
  static List<JavaField> instanceFields(JavaClass type) {
    return type.getAllFields().stream()
        .filter(field -> !field.getModifiers().contains(JavaModifier.STATIC))
        .sorted(Comparator.comparing(JavaField::getName))
        .toList();
  }
```

---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `classesMatching`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#classesmatching"
---

[Full node and context](/rule/tactical/dca-tac-025.md#classesmatching). This is an evidence excerpt; retain the parent selection and caveats.

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

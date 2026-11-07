---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `classesMatching`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#classesmatching"
---

[Full node and context](/rule/tactical/dca-tac-026.md#classesmatching). This is an evidence excerpt; retain the parent selection and caveats.

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

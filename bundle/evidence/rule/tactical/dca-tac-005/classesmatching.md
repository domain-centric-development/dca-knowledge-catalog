---
type: Reference
title: "Entities must not be instantiated directly from outside the aggregate — `classesMatching`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-005.md#classesmatching"
---

[Full node and context](/rule/tactical/dca-tac-005.md#classesmatching). This is an evidence excerpt; retain the parent selection and caveats.

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `moduleRootOf()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

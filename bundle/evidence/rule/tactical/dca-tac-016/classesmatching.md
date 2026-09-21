---
type: Reference
title: "Repositories must only exist for Aggregate Roots — `classesMatching`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-016.md#classesmatching"
---

[Full node and context](/rule/tactical/dca-tac-016.md#classesmatching). This is an evidence excerpt; retain the parent selection and caveats.

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `rootContextPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

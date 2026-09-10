---
type: Reference
title: "Entities must not be instantiated directly from outside the aggregate — `nonRootEntities`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-005.md#nonrootentities"
---

[Full node and context](/rule/tactical/dca-tac-005.md#nonrootentities). This is an evidence excerpt; retain the parent selection and caveats.

### `nonRootEntities`

```java
private static List<JavaClass> nonRootEntities(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(Entity.class)
              && !c.isAssignableTo(AggregateRoot.class)
              && !c.isInterface());
}
```

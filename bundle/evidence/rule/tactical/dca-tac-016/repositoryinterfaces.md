---
type: Reference
title: "Repositories must only exist for Aggregate Roots — `repositoryInterfaces`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-016.md#repositoryinterfaces"
---

[Full node and context](/rule/tactical/dca-tac-016.md#repositoryinterfaces). This is an evidence excerpt; retain the parent selection and caveats.

### `repositoryInterfaces`

```java
private static List<JavaClass> repositoryInterfaces(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(arch.layout().markers().repository())
              && c.isInterface()
              && !c.getSimpleName().equals(arch.layout().repositorySuffix()));
}
```

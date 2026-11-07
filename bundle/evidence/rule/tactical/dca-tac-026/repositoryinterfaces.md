---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `repositoryInterfaces`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#repositoryinterfaces"
---

[Full node and context](/rule/tactical/dca-tac-026.md#repositoryinterfaces). This is an evidence excerpt; retain the parent selection and caveats.

### `repositoryInterfaces`

```java
private static List<JavaClass> repositoryInterfaces(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          arch.layout().markers().is("repository").test(c)
              && c.isInterface()
              && !c.getSimpleName().equals(arch.layout().repositorySuffix()));
}
```

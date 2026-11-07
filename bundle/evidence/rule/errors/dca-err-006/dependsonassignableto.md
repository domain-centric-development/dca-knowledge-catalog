---
type: Reference
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures — `dependsOnAssignableTo`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-006.md#dependsonassignableto"
---

[Full node and context](/rule/errors/dca-err-006.md#dependsonassignableto). This is an evidence excerpt; retain the parent selection and caveats.

### `dependsOnAssignableTo`

```java
private static boolean dependsOnAssignableTo(
    JavaClass type, DescribedPredicate<JavaClass> target) {
  return type.getDirectDependenciesFromSelf().stream()
      .anyMatch(dependency -> target.test(dependency.getTargetClass()));
}
```

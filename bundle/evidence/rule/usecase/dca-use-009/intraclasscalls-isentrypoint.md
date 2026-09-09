---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `IntraClassCalls.isEntryPoint`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#intraclasscallsisentrypoint"
---

[Full node and context](/rule/usecase/dca-use-009.md#intraclasscallsisentrypoint). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.isEntryPoint`

```java
private boolean isEntryPoint(JavaCodeUnit unit) {
  Set<JavaModifier> modifiers = unit.getModifiers();
  boolean externallyCallable =
      !modifiers.contains(JavaModifier.PRIVATE)
          && !modifiers.contains(JavaModifier.SYNTHETIC)
          && !modifiers.contains(JavaModifier.BRIDGE);
  return externallyCallable || callers.getOrDefault(unit, Set.of()).isEmpty();
}
```

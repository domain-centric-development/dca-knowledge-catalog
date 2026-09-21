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
  if (modifiers.contains(JavaModifier.SYNTHETIC) || modifiers.contains(JavaModifier.BRIDGE)) {
    // A unit the compiler wrote, not a path anyone enters on. The bridge method a generic input
    // port produces - execute(Object) beside execute(Command) - has no caller inside the class,
    // so the "nothing calls it" fallback below would otherwise make it a second entry point and
    // report every use case over a generic port twice.
    return false;
  }
  return !modifiers.contains(JavaModifier.PRIVATE)
      || callers.getOrDefault(unit, Set.of()).isEmpty();
}
```

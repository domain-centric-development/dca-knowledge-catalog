---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `calls`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#calls"
---

[Full node and context](/rule/usecase/dca-use-009.md#calls). This is an evidence excerpt; retain the parent selection and caveats.

### `calls`

```java
private static boolean calls(JavaCodeUnit unit, Class<?> targetType) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(call -> call.getTargetOwner().isAssignableTo(targetType));
}

private static boolean calls(JavaCodeUnit unit, Class<?> targetType, String methodName) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(
          call ->
              call.getTarget().getName().equals(methodName)
                  && call.getTargetOwner().isAssignableTo(targetType));
}
```

---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `calls`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#calls"
---

[Full node and context](/rule/usecase/dca-use-009.md#calls). This is an evidence excerpt; retain the parent selection and caveats.

### `calls`

```java
private static boolean calls(JavaCodeUnit unit, DescribedPredicate<JavaClass> target) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(call -> target.test(call.getTargetOwner()));
}

private static boolean calls(
    JavaCodeUnit unit, DescribedPredicate<JavaClass> target, String methodName) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(
          call ->
              call.getTarget().getName().equals(methodName)
                  && target.test(call.getTargetOwner()));
}
```

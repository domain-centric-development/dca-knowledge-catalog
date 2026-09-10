---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — `callsBoundary`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#callsboundary"
---

[Full node and context](/rule/usecase/dca-use-012.md#callsboundary). This is an evidence excerpt; retain the parent selection and caveats.

### `callsBoundary`

```java
private static boolean callsBoundary(JavaCodeUnit unit) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(call -> call.getTargetOwner().isAssignableTo(TransactionBoundary.class));
}
```

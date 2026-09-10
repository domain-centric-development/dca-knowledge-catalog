---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `IntraClassCalls.callersOf`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#intraclasscallscallersof"
---

[Full node and context](/rule/usecase/dca-use-009.md#intraclasscallscallersof). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.callersOf`

```java
/** The unit itself and every unit that reaches it through calls within the class. */
  Set<JavaCodeUnit> callersOf(JavaCodeUnit unit) {
    return closure(unit, callers);
  }
```

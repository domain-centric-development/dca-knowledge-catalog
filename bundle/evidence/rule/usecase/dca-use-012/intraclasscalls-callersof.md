---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — `IntraClassCalls.callersOf`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#intraclasscallscallersof"
---

[Full node and context](/rule/usecase/dca-use-012.md#intraclasscallscallersof). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.callersOf`

```java
/** The unit itself and every unit that reaches it through calls within the class. */
  Set<JavaCodeUnit> callersOf(JavaCodeUnit unit) {
    return closure(unit, callers);
  }
```

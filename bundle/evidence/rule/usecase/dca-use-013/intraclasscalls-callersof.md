---
type: Reference
title: "Declaratively transactional use cases must not call remote-capable output ports — `IntraClassCalls.callersOf`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-013.md#intraclasscallscallersof"
---

[Full node and context](/rule/usecase/dca-use-013.md#intraclasscallscallersof). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.callersOf`

```java
/** The unit itself and every unit that reaches it through calls within the class. */
  Set<JavaCodeUnit> callersOf(JavaCodeUnit unit) {
    return closure(unit, callers);
  }
```
